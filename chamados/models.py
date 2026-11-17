from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Chamado(models.Model):
    class Urgencia(models.TextChoices):
        BAIXA = "baixa", "Baixa"
        MEDIA = "media", "Média"
        ALTA = "alta", "Alta"

    class Status(models.TextChoices):
        ABERTO = "aberto", "Aberto"
        EM_ANDAMENTO = "em_andamento", "Em andamento"
        CONCLUIDO = "concluido", "Concluído"
        CANCELADO = "cancelado", "Cancelado"

    titulo = models.CharField("título", max_length=150)
    local = models.CharField(max_length=150)
    descricao = models.TextField("descrição")
    urgencia = models.CharField(max_length=10, choices=Urgencia.choices, default=Urgencia.MEDIA)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.ABERTO)
    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="chamados_solicitados",
    )
    tecnico = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="chamados_atribuidos",
        blank=True,
        null=True,
    )
    solucao = models.TextField(blank=True)
    nota_avaliacao = models.PositiveSmallIntegerField(
        "nota da avaliação",
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    criado_em = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        ordering = ["-criado_em", "titulo"]
        verbose_name = "chamado"
        verbose_name_plural = "chamados"

    def __str__(self):
        return self.titulo

    def clean(self):
        super().clean()
        erros = {}
        if self.status == self.Status.CONCLUIDO and not self.solucao.strip():
            erros["solucao"] = "Informe a solução antes de concluir o chamado."
        if self.nota_avaliacao is not None and self.status != self.Status.CONCLUIDO:
            erros["nota_avaliacao"] = "A avaliação só pode ser registrada após a conclusão."
        if erros:
            raise ValidationError(erros)

    def adicionar_comentario(self, autor, mensagem):
        if self.status in (self.Status.CONCLUIDO, self.Status.CANCELADO):
            raise ValidationError("Não é possível comentar um chamado concluído ou cancelado.")
        historico = HistoricoChamado(chamado=self, autor=autor, mensagem=mensagem.strip())
        historico.full_clean()
        historico.save()
        return historico

    def registrar_avaliacao(self, nota):
        if self.status != self.Status.CONCLUIDO:
            raise ValidationError(
                {"nota_avaliacao": "A avaliação só pode ser registrada após a conclusão."}
            )
        if not 1 <= nota <= 5:
            raise ValidationError({"nota_avaliacao": "A nota deve estar entre 1 e 5."})
        self.nota_avaliacao = nota
        self.full_clean()
        self.save(update_fields=["nota_avaliacao"])

    def concluir(self, solucao):
        solucao = (solucao or "").strip()
        if not solucao:
            raise ValidationError({"solucao": "Informe a solução antes de concluir o chamado."})
        self.solucao = solucao
        self.status = self.Status.CONCLUIDO
        self.full_clean()
        self.save(update_fields=["solucao", "status"])


class HistoricoChamado(models.Model):
    chamado = models.ForeignKey(
        Chamado,
        on_delete=models.CASCADE,
        related_name="historico",
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="atualizacoes_chamados",
    )
    mensagem = models.TextField()
    criado_em = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        ordering = ["criado_em", "pk"]
        verbose_name = "registro do histórico"
        verbose_name_plural = "registros do histórico"

    def __str__(self):
        return f"{self.chamado} - {self.autor}: {self.mensagem[:50]}"

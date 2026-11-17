from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase

from chamados.models import Chamado, HistoricoChamado


class RecusasChamadoTests(SimpleTestCase):
    def setUp(self):
        self.solicitante = get_user_model()(username="solicitante")

    def criar_chamado(self, status, solucao=""):
        return Chamado(
            titulo="Lâmpada queimada",
            local="Sala 2",
            descricao="A lâmpada não acende.",
            urgencia=Chamado.Urgencia.MEDIA,
            status=status,
            solicitante=self.solicitante,
            solucao=solucao,
        )

    def test_recusa_comentario_em_chamado_concluido(self):
        chamado = self.criar_chamado(Chamado.Status.CONCLUIDO, "Lâmpada substituída.")

        with self.assertRaisesMessage(
            ValidationError,
            "Não é possível comentar um chamado concluído ou cancelado.",
        ):
            chamado.adicionar_comentario(self.solicitante, "Mais uma informação.")

    def test_recusa_comentario_em_chamado_cancelado(self):
        chamado = self.criar_chamado(Chamado.Status.CANCELADO)

        with self.assertRaisesMessage(
            ValidationError,
            "Não é possível comentar um chamado concluído ou cancelado.",
        ):
            chamado.adicionar_comentario(self.solicitante, "Mais uma informação.")

    def test_recusa_avaliacao_antes_da_conclusao(self):
        chamado = self.criar_chamado(Chamado.Status.EM_ANDAMENTO)

        with self.assertRaisesMessage(
            ValidationError,
            "A avaliação só pode ser registrada após a conclusão.",
        ):
            chamado.registrar_avaliacao(5)

    def test_recusa_nota_fora_do_intervalo(self):
        chamado = self.criar_chamado(Chamado.Status.CONCLUIDO, "Lâmpada substituída.")

        for nota in (0, 6):
            with (
                self.subTest(nota=nota),
                self.assertRaisesMessage(
                    ValidationError,
                    "A nota deve estar entre 1 e 5.",
                ),
            ):
                chamado.registrar_avaliacao(nota)

    def test_recusa_conclusao_sem_solucao(self):
        chamado = self.criar_chamado(Chamado.Status.EM_ANDAMENTO)

        for solucao in (None, "", "   "):
            with (
                self.subTest(solucao=solucao),
                self.assertRaisesMessage(
                    ValidationError,
                    "Informe a solução antes de concluir o chamado.",
                ),
            ):
                chamado.concluir(solucao)

        self.assertEqual(chamado.status, Chamado.Status.EM_ANDAMENTO)
        self.assertEqual(chamado.solucao, "")

    def test_validacao_do_modelo_recusa_conclusao_sem_solucao(self):
        chamado = self.criar_chamado(Chamado.Status.CONCLUIDO)

        with self.assertRaises(ValidationError) as contexto:
            chamado.clean()

        self.assertIn("solucao", contexto.exception.message_dict)

    def test_validacao_do_modelo_recusa_nota_antes_da_conclusao(self):
        chamado = self.criar_chamado(Chamado.Status.ABERTO)
        chamado.nota_avaliacao = 4

        with self.assertRaises(ValidationError) as contexto:
            chamado.clean()

        self.assertIn("nota_avaliacao", contexto.exception.message_dict)


class OperacoesChamadoTests(TestCase):
    def setUp(self):
        usuario = get_user_model()
        self.solicitante = usuario.objects.create_user(username="solicitante")
        self.tecnico = usuario.objects.create_user(username="tecnico")
        self.chamado = Chamado.objects.create(
            titulo="Lâmpada queimada",
            local="Sala 2",
            descricao="A lâmpada não acende.",
            urgencia=Chamado.Urgencia.MEDIA,
            solicitante=self.solicitante,
        )

    def test_adiciona_comentario_em_chamado_aberto(self):
        historico = self.chamado.adicionar_comentario(
            self.solicitante,
            "A lâmpada pisca antes de apagar.",
        )

        self.assertEqual(historico.chamado, self.chamado)
        self.assertEqual(historico.autor, self.solicitante)
        self.assertEqual(historico.mensagem, "A lâmpada pisca antes de apagar.")
        self.assertTrue(HistoricoChamado.objects.filter(pk=historico.pk).exists())

    def test_registra_avaliacao_de_chamado_concluido(self):
        self.chamado.status = Chamado.Status.CONCLUIDO
        self.chamado.solucao = "Lâmpada substituída."
        self.chamado.save(update_fields=["status", "solucao"])

        self.chamado.registrar_avaliacao(5)
        self.chamado.refresh_from_db()

        self.assertEqual(self.chamado.nota_avaliacao, 5)

    def test_conclui_chamado_com_solucao(self):
        self.chamado.tecnico = self.tecnico
        self.chamado.status = Chamado.Status.EM_ANDAMENTO
        self.chamado.save(update_fields=["tecnico", "status"])

        self.chamado.concluir("Lâmpada substituída.")
        self.chamado.refresh_from_db()

        self.assertEqual(self.chamado.status, Chamado.Status.CONCLUIDO)
        self.assertEqual(self.chamado.solucao, "Lâmpada substituída.")

    def test_clean_aceita_chamado_concluido_com_solucao_e_nota(self):
        chamado = Chamado(
            titulo="Lâmpada queimada",
            local="Sala 2",
            descricao="A lâmpada não acende.",
            urgencia=Chamado.Urgencia.MEDIA,
            status=Chamado.Status.CONCLUIDO,
            solicitante=self.solicitante,
            solucao="Lâmpada substituída.",
            nota_avaliacao=4,
        )

        chamado.clean()

    def test_representacao_em_texto_dos_modelos(self):
        self.assertEqual(str(self.chamado), "Lâmpada queimada")
        historico = HistoricoChamado(
            chamado=self.chamado,
            autor=self.solicitante,
            mensagem="Atualização técnica.",
        )

        self.assertEqual(str(historico), "Lâmpada queimada - solicitante: Atualização técnica.")

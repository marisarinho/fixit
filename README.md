# FixIt — Controle de Chamados de Manutenção Interna

Sistema web para colaboradores registrarem pedidos de manutenção e técnicos acompanharem e resolverem esses chamados.

## Estado atual

O repositório já tem a base Django, a esteira inicial e os modelos de domínio com métodos para as três recusas. As telas, autenticação e carga de dados ainda serão implementadas.

## Requisitos locais

- Python 3.12 ou superior, gerenciado pelo `uv`.
- `uv` instalado.

## Preparar e executar

```powershell
uv sync --locked
uv run python manage.py migrate
uv run python manage.py runserver
```

A verificação inicial do Django fica em `http://127.0.0.1:8000/health/`.

## Testes e cobertura

```powershell
uv run python manage.py test --shuffle
uv run python -m coverage run manage.py test --shuffle
uv run python -m coverage report
```

A cobertura mínima está configurada como 95% em `pyproject.toml`.

## Hooks locais

Atualize as revisões dos hooks e instale-os na máquina:

```powershell
uv run python -m pre_commit autoupdate
uv run python -m pre_commit install --install-hooks
uv run python -m pre_commit run --all-files
```

Cada integrante deve configurar a assinatura SSH e instalar os hooks na própria máquina. A assinatura fica ativa pelo Git global; confirme o selo `Verified` no GitHub depois do primeiro push assinado.

## Planejamento e uso de IA

- Escopo e decisões iniciais: `docs/planejamento-inicial.md`.
- Prompts que produziram material mantido: `PROMPTS.md`.
- Instruções de IA para este repositório: `AGENTS.md`.
- Repositório público: [FixIt no GitHub](https://github.com/marisarinho/fixit). Inserir o link compartilhável do Google Docs aprovado antes da entrega.

## Ainda previsto para a entrega

Docker Compose, login e grupos, as telas das dez histórias de usuário, dados iniciais, testes de integração completos, credenciais de demonstração e histórico de commits de ambas as integrantes serão adicionados ao longo do projeto.

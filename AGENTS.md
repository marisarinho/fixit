# Instruções para assistentes de IA

## Contexto e escopo

- O sistema é o FixIt, para chamados de manutenção interna, conforme a proposta aprovada.
- O front-end será feito com templates Django. Não introduza uma API REST ou um front-end separado sem decisão expressa do grupo.
- Os papéis são Solicitante e Técnico. Os três bloqueios obrigatórios são comentários em chamado encerrado, avaliação antes da conclusão e conclusão sem solução.
- A esteira é prioridade antes das regras e dos modelos de domínio.

## Ferramentas e verificações

- Use Python 3.12 ou superior, Django 5.2 ou superior e `uv`.
- Não use pytest. Os testes devem rodar com o executor padrão do Django.
- Separe testes unitários e de integração em `chamados/tests/unit/` e `chamados/tests/integration/`.
- Antes de concluir uma mudança, oriente a executar `uv run python manage.py check`, `uv run python manage.py makemigrations --check` e os testes com cobertura.
- Mantenha o limite de cobertura de 95% configurado em `pyproject.toml`.

## Segurança e processo

- Não grave senhas, tokens ou chaves privadas no repositório. Use `.env.example` apenas com valores de exemplo.
- Atualize `PROMPTS.md` quando um prompt produzir código, configuração ou planejamento que o grupo adotar.
- Mantenha em `docs/` os planos e especificações de IA efetivamente usados.
- Não crie commits nem faça push em nome de uma integrante sem pedido explícito.

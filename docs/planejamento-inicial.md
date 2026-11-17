# Planejamento inicial do FixIt

## Objetivo aprovado

Sistema web para colaboradores registrarem pedidos de manutenção e técnicos acompanharem e resolverem esses chamados.

## Papéis

- **Solicitante:** abre chamados, acompanha os próprios pedidos, cancela chamados abertos, envia comentários enquanto o atendimento está ativo e pode avaliar o atendimento concluído.
- **Técnico:** consulta a fila por urgência, assume chamados, registra atualizações, conclui informando a solução e acompanha os totais por status e urgência.

## Escopo aprovado

1. Abrir chamado com título, local, descrição e urgência.
2. Listar e filtrar os próprios chamados por status.
3. Cancelar chamado que ainda esteja aberto.
4. Adicionar comentários durante o atendimento; recusar comentários após conclusão ou cancelamento.
5. Avaliar o atendimento de 1 a 5; recusar avaliação antes da conclusão.
6. Consultar a fila de chamados abertos ordenada por urgência.
7. Assumir um chamado aberto e indicar que o atendimento começou.
8. Registrar atualizações no histórico do chamado.
9. Concluir um chamado informando a solução; recusar solução em branco.
10. Consultar totais de chamados por status e urgência.

## Direção técnica inicial

- Django com templates, para manter uma única interface de usuário e evitar duplicar as validações numa API.
- SQLite no desenvolvimento e no Docker Compose.
- Usuários do Django com os grupos `Solicitante` e `Técnico`.
- Modelos de domínio previstos: `Chamado` e `HistoricoChamado`.
- A primeira etapa prepara `uv`, testes, cobertura, pre-commit e integração contínua. As regras e os modelos de domínio serão implementados depois dessa base.

## Decisões que precisam ser fechadas antes das regras

- Quais estados contam como chamado ativo para permitir comentários.
- Se cada chamado pode receber apenas uma avaliação e se a avaliação é opcional.
- Se somente o técnico que assumiu o chamado pode atualizá-lo ou concluí-lo.
- Quais transições de estado são permitidas para cancelamento e conclusão.

Este documento registra a direção inicial derivada da proposta aprovada e do planejamento discutido com assistência de IA. Atualizem-no se o grupo mudar alguma decisão.

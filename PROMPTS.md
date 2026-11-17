# Registro de prompts de IA

Registrem aqui os prompts que produziram decisões ou materiais mantidos no projeto. Não é necessário copiar conversas inteiras. Atualizem o resultado após revisão das integrantes.

## 2026-11-17 — Mariana — definição técnica inicial do FixIt

Prompt (Gemini): “gostei do sistema de chamados, oq teriamos que desenhar agora pra fechar esse escopo ?”

Resultado: aceito com ajustes. A ideia de chamados, os papéis e o desenho inicial com `Chamado` e `HistoricoChamado` foram usados no planejamento. As histórias foram revisadas na proposta final, aprovada pelo professor; decisões de estado e autorização continuam pendentes.

## 2026-11-17 — Mariana — base e esteira da primeira semana

Prompt (Codex): “os codigos vc altera e os comandos no terminal vc cola aqui pra eu copiar e execuatr ok? so me deixe a par doq vc esta fazendo noc codigos”

Resultado: aceito com ajustes após execução local. A base Django, o teste de integração e a cobertura passaram; o primeiro teste com `--shuffle` registrou 100%. No Windows, os comandos do pre-commit passaram a ser executados por `python -m pre_commit` porque a política bloqueou o atalho de console.

## 2026-11-17 — Mariana — modelos e regras de recusa

Prompt (Codex): “vamos fzr minha parte que falta. mariana , faça no codigo sem comentarios e me de os comandos pra fazer no terminal”

Resultado: aceito com ajustes. Foram implementados `Chamado`, `HistoricoChamado`, as recusas de comentário, avaliação e conclusão, e testes para os caminhos recusados e aceitos. Mariana gerou e aplicou a migration; 13 testes passaram com `--shuffle`, a cobertura ficou em 100% e os hooks executados passaram.

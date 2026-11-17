# Registro de prompts de IA

Registrem aqui os prompts que produziram decisões ou materiais mantidos no projeto. Não é necessário copiar conversas inteiras. Atualizem o resultado após revisão das integrantes.

## 2026-11-17 — Mariana — definição técnica inicial do FixIt

Prompt (Gemini): “gostei do sistema de chamados, oq teriamos que desenhar agora pra fechar esse escopo ?”

Resultado: aceito com ajustes. A ideia de chamados, os papéis e o desenho inicial com `Chamado` e `HistoricoChamado` foram usados no planejamento. As histórias foram revisadas na proposta final, aprovada pelo professor; decisões de estado e autorização continuam pendentes.

## 2026-11-17 — Mariana — base e esteira da primeira semana

Prompt (Codex): “os codigos vc altera e os comandos no terminal vc cola aqui pra eu copiar e execuatr ok? so me deixe a par doq vc esta fazendo noc codigos”

Resultado provisório: base Django, teste de integração e cobertura aceitos após execução local; o teste passou com `--shuffle` e registrou 100%. Os comandos do pre-commit precisam usar `python -m pre_commit` porque a política do Windows bloqueou o executável de console. A validação dos hooks continua pendente.

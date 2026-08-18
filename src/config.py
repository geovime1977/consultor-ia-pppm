"""Config global do app — flags de feature.

MOSTRAR_PO_UI:
    - False (padrão para a turma da Aula 2): app oculta toda referência a
      Pesquisa Operacional (colunas IA+PO da aba 1, dimensão IA+PO da aba 8,
      textos e título). Dados JSON no disco ficam intactos.
    - True: app volta a mostrar tudo (uso interno da Eixo Estratégico, Motor PO).

Nada aqui executa PO — o app hoje só EXIBE textos curados. Ativar a flag para
True revela o conteúdo estático. Para PO real (solvers, MILP, AHP, SAPEVO-M),
ver docs/ROADMAP-PO.md.
"""

MOSTRAR_PO_UI: bool = False

MOSTRAR_ABA_PILOTOS_PMBOK: bool = False
"""Aba 'Pilotos de IA em PPPM' + referência dos 40 processos PMBOK.

    - False (padrão para a turma): oculta a aba. O app começa direto no
      diagnóstico consultivo (Contexto → Diagnóstico → Mapa → Pilotos → PDF)
      e no método Aula 2 (Priorização + Governança/HITL).
    - True: reexibe a aba com o catálogo dos 16 pilotos e o mapa dos 40
      processos PMBOK como referência opcional (uso interno / próxima turma).
"""

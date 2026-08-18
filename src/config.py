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

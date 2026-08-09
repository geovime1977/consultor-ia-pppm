# consultor-ia-pppm — Guia de Instalação

**Para:** Prof. Dr. José Bezerra
**De:** Geovane Virmecati — Eixo Estratégico
**Sobre:** App que operacionaliza o método da Aula 1 (Formação de Consultores em IA aplicada ao PPPM · BSBr)

---

## O que é este pacote

Uma versão **do seu próprio método** transformada em ferramenta usável. O aluno responde o diagnóstico de maturidade em 5 dimensões, preenche o Mapa 5 Blocos, e o app devolve um PDF com 3 pilotos priorizados — o mesmo entregável da Empresa Alfa que o senhor apresentou no slide 15.

O código é 100% aberto, roda localmente na sua máquina, **não envia dados para nenhum servidor** e **não usa IA em produção** — a recomendação de pilotos é uma regra matemática auditável.

---

## Requisitos

- Computador com **Windows** ou **Mac**
- **Python 3.10** ou mais recente instalado (baixe grátis em https://www.python.org/downloads/)
  - **Windows:** na tela de instalação, **marque a caixa "Add Python to PATH"** antes de clicar em Install
  - **Mac:** o instalador do site do Python já configura tudo
- Cerca de **200 MB de espaço em disco**
- Conexão à internet **apenas na primeira instalação** (para baixar 2 bibliotecas)

---

## Como instalar — 3 passos

### Passo 1 — Descompactar o pacote

Se o pacote veio em `.zip`, dê duplo-clique nele e extraia todos os arquivos para uma pasta à sua escolha (por exemplo, `Desktop/consultor-ia-pppm/`).

Você verá esta estrutura:
```
pacote-entrega/
├── 1-INSTALAR-mac.command       ← instalador Mac
├── 1-INSTALAR-windows.bat       ← instalador Windows
├── 2-RODAR-mac.command          ← abrir o app (Mac)
├── 2-RODAR-windows.bat          ← abrir o app (Windows)
├── consultor-ia-pppm.zip             ← o app comprimido
├── LEIA-ME-PROFESSOR.md         ← este documento
└── LEIA-ME-PROFESSOR.pdf        ← versão PDF deste documento
```

### Passo 2 — Rodar o instalador (uma vez só)

**No Mac:**
1. Dê duplo-clique em **`1-INSTALAR-mac.command`**
2. Se aparecer a mensagem "não pode ser aberto porque é de um desenvolvedor não identificado":
   - Clique com o botão direito no arquivo → **Abrir** → confirme **Abrir**
3. Aguarde uns 2-3 minutos (janela vai mostrar o progresso 1/4, 2/4, 3/4, 4/4)
4. Quando aparecer "Instalação concluída com sucesso", feche a janela.

**No Windows:**
1. Dê duplo-clique em **`1-INSTALAR-windows.bat`**
2. Se o Windows perguntar sobre "Windows protegeu seu PC":
   - Clique em **Mais informações** → **Executar assim mesmo**
3. Aguarde uns 2-3 minutos (janela preta mostra o progresso).
4. Quando aparecer "Instalacao concluida com sucesso", pressione ENTER para fechar.

### Passo 3 — Abrir o app (sempre que quiser usar)

**No Mac:** dê duplo-clique em **`2-RODAR-mac.command`**
**No Windows:** dê duplo-clique em **`2-RODAR-windows.bat`**

O navegador vai abrir automaticamente em `http://localhost:8512` mostrando o app.

Para **encerrar o app**, basta fechar a janela preta/terminal ou pressionar `Ctrl+C` nela.

---

## Como usar o app (5 minutos)

O app tem 5 abas na parte superior. Preencha na ordem:

**Aba 1 — Contexto**
Nome, empresa, porte, número de projetos ativos, se tem PMO, cargo. Clique em "Salvar contexto".

**Aba 2 — Diagnóstico**
5 sliders de 0 a 6, um por dimensão do método:
- Estratégia e valor
- Dados e processos
- Casos de uso
- Governança e HITL
- Benefícios e ROI

O app mostra em tempo real o total (0–30) e o nível resultante (Ausente / Reativo / Experimental / Definido / Otimizado).

**Aba 3 — Mapa 5 Blocos**
5 caixas de texto: Contexto · Dor · Dados · Riscos · Valor. Mínimo 30 caracteres por bloco.

**Aba 4 — Pilotos Recomendados**
O app cruza sua menor pontuação (gargalo) com as palavras-chave que extrai do bloco "Dor" e sugere 3 pilotos priorizados de um catálogo de 12. Cada piloto vem com scoring (Impacto/Viabilidade/Risco), pré-requisitos e ganho esperado.

**Aba 5 — Exportar PDF**
Clique em "Gerar PDF" e depois em "Download". O PDF sai com 7 páginas: Capa · Contexto · Diagnóstico · Mapa · 3 Pilotos · Próximos Passos.

---

## Se algo der errado

**"Python não está instalado" (ao rodar o instalador)**
→ Instale Python de https://www.python.org/downloads/ e rode o instalador de novo.

**"Address already in use" na porta 8512**
→ Outro programa está usando essa porta. Feche outros apps ou reinicie o computador e tente de novo.

**Janela abre e fecha muito rápido no Windows**
→ Abra o Prompt de Comando (cmd), navegue até a pasta do pacote e rode `1-INSTALAR-windows.bat` — assim você vê a mensagem de erro completa.

**Não abre no navegador automaticamente**
→ Abra o navegador manualmente e digite `http://localhost:8512`

**Quero desinstalar tudo**
→ Basta apagar a pasta `consultor-ia-pppm` inteira. Nada foi instalado fora dela — nem no sistema, nem no registro do Windows.

---

## Contato

**Autor:** Geovane Virmecati
**Instituição:** Eixo Estratégico
**Base normativa:** PMI Standard for AI in Portfolio, Program and Project Management (2026)
**Método pedagógico:** Aula 1 do Prof. Dr. José Bezerra — BSBr

Qualquer feedback, melhoria ou pedido de ajuste do catálogo de pilotos: é só me avisar.

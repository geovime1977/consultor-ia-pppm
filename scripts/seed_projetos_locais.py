#!/usr/bin/env python3
"""Cadastra projetos reais de Geovane Virmecati (Eixo Estratégico) no banco.

Dados extraídos de: ~/projetos/*/CLAUDE.md, notas do vault Obsidian
(~/vault/meus-projetos/01 - Profissional/Projetos/) e memory persistente.

Diagnóstico das 5 dimensões: heurística baseada na maturidade observada
(deploy ativo, docs, testes, tempo de vida, uso real). Ajustar manualmente
no app se necessário.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import db  # noqa: E402


PROJETOS_LOCAIS = [
    {
        "nome": "Empresa Alfa (case Bezerra)",
        "empresa": "Empresa Alfa — hipotética",
        "porte": "Médio",
        "cargo_gp": "PMO Manager (case demo)",
        "n_projetos": 28,
        "pmo_ativo": True,
        "estrategia": 4, "dados": 3, "casos_uso": 2, "governanca": 1, "beneficios": 2,
        "mapa_contexto": "Empresa de médio porte em serviços/operações; 1 portfólio de transformação, 3 programas e 28 projetos monitorados pelo PMO. Case apresentado pelo Prof. Dr. José Bezerra na Aula 1 IA-PPPM (BSBr, 2026-08-08, slides 28-30).",
        "mapa_dor": "Projetos atrasam, dados se contradizem, informação chega pouco executiva ao comitê. Equipes usam IA de forma informal para atas, relatórios e análises pontuais — sem método, sem governança e sem métrica de valor.",
        "mapa_dados": "Sistemas de PMO com status reports semanais, atas de reunião, cronogramas em MS Project/Excel, backlog de riscos, feedback de stakeholders — todos descentralizados e com qualidade variável.",
        "mapa_riscos": "Sem governança de IA formal (HITL não previsto), risco de viés de dados sem auditoria, LGPD frouxa em documentos sensíveis, resistência da média gerência a compartilhar dados entre departamentos.",
        "mapa_valor": "Reduzir tempo de consolidação de status executivo (~70%), antecipar risco de aditivo em 30 dias, melhorar aderência a SLA em 15-25%, aumentar velocidade de atendimento em 80% — segundo âncoras do Prof. Bezerra em [01:02:10] e [03:18:25].",
        "pilotos": [
            {"nome": "Assistente de Status Executivo", "impacto": "alto", "viabilidade": "alto", "risco": "baixo"},
            {"nome": "Radar de Riscos e Atrasos", "impacto": "alto", "viabilidade": "medio", "risco": "medio"},
            {"nome": "Análise de SLA", "impacto": "alto", "viabilidade": "alto", "risco": "baixo"},
        ],
        "processos_marcados": [
            ("1.5", "ia", "alta", "Governança da qualidade — gargalo #1 do case (1/6)"),
            ("5.5", "ia", "alta", "Consolidação executiva de comunicações"),
            ("7.2", "ia_po", "alta", "Identificação sistemática de risco de aditivo"),
            ("7.5", "ia", "media", "Implementar respostas com HITL obrigatório"),
        ],
    },
    {
        "nome": "consultor-ia-pppm (Eixo)",
        "empresa": "Eixo Estratégico",
        "porte": "MEI",
        "cargo_gp": "Fundador",
        "n_projetos": 1,
        "pmo_ativo": False,
        "estrategia": 5, "dados": 4, "casos_uso": 5, "governanca": 5, "beneficios": 4,
        "mapa_contexto": "App Streamlit que operacionaliza a Aula 1 do Prof. Dr. José Bezerra (BSBr) sobre IA-PPPM; roda em localhost:8512 com 6 abas.",
        "mapa_dor": "Transformar método pedagógico da aula 1 em ferramenta operacional que gera diagnóstico + Mapa 5 Blocos + 3 pilotos + PDF sem refazer raciocínio manual.",
        "mapa_dados": "PDF da Aula 1, 12 pilotos derivados, catálogo PMBOK 8ª (40 processos × IA × IA+PO), templates de PDF ReportLab.",
        "mapa_riscos": "Método é do Prof. Bezerra — respeitar autoria; alucinação bloqueada por design (v1 100% determinística); testes 28/28 verdes.",
        "mapa_valor": "Consultoria Eixo aplica em cliente em 15min; palestra usa como caso prático; skill vendável no Eixo Skills Pack.",
        "pilotos": [
            {"nome": "Assistente de Diagnóstico IA-PPPM", "impacto": "alto", "viabilidade": "alto", "risco": "baixo"},
            {"nome": "Mapa PMBOK × IA × PO (v1.1)", "impacto": "alto", "viabilidade": "alto", "risco": "baixo"},
        ],
        "processos_marcados": [
            ("1.6", "ia", "alta", "RAG sobre lições da aula 1"),
            ("2.2", "ia", "media", "Coleta requisitos do PMO cliente"),
            ("7.2", "ia_po", "media", "Riscos IA levantados no diagnóstico"),
        ],
    },
    {
        "nome": "equipe-juridica",
        "empresa": "Eixo Estratégico",
        "porte": "MEI",
        "cargo_gp": "Fundador",
        "n_projetos": 1,
        "pmo_ativo": False,
        "estrategia": 5, "dados": 5, "casos_uso": 6, "governanca": 6, "beneficios": 5,
        "mapa_contexto": "Pipeline multi-agente jurídico (gerador→revisor→auditor AHP→orquestrador) em produção na VPS, porta 8507, multi-provider LLM.",
        "mapa_dor": "Automatizar redação e revisão jurídica com validação AHP entre versões concorrentes, mantendo rastreabilidade e explicabilidade da decisão final.",
        "mapa_dados": "Corpus de petições, jurisprudência STF/STJ, prompts calibrados por tipo de peça, histórico de scoring AHP em 200+ execuções.",
        "mapa_riscos": "Responsabilidade civil do advogado; sigilo OAB; alucinação de jurisprudência; loop de correção validado em Jul/17.",
        "mapa_valor": "Reduz tempo de redação em 80% mantendo qualidade auditável; primeiro produto Eixo com PO embedded (AHP).",
        "pilotos": [
            {"nome": "Gerador Jurídico Multi-Provider", "impacto": "alto", "viabilidade": "alto", "risco": "medio"},
            {"nome": "Auditor AHP de Versões", "impacto": "alto", "viabilidade": "alto", "risco": "baixo"},
        ],
        "processos_marcados": [
            ("1.5", "ia_po", "alta", "Garantia da qualidade via auditor AHP"),
            ("1.8", "ia_po", "alta", "Avaliar mudanças entre versões concorrentes"),
            ("7.3", "ia", "media", "Análise de risco jurídico automatizada"),
            ("1.2", "ia", "media", "Orquestrador integra 4 agentes"),
        ],
    },
    {
        "nome": "casos-reais-app",
        "empresa": "Eixo Estratégico",
        "porte": "MEI",
        "cargo_gp": "Fundador",
        "n_projetos": 1,
        "pmo_ativo": False,
        "estrategia": 4, "dados": 4, "casos_uso": 5, "governanca": 3, "beneficios": 5,
        "mapa_contexto": "App Streamlit :8503 que gera casos reais para qualquer curso via OpenAI+web_search; substitui pedidos manuais em disciplinas do MBA.",
        "mapa_dor": "Cada módulo do MBA de Finanças Corporativas precisa de casos brasileiros auditáveis (CVM/B3/RI); coleta manual leva 4h por módulo.",
        "mapa_dados": "APIs OpenAI, web_search, base de tickers B3, templates MD/PPTX/PDF, arquivos de casos gerados por disciplina.",
        "mapa_riscos": "Alucinação em dados financeiros — mitigar exigindo fonte pública auditada (CVM/B3/RI); LGPD não se aplica (dados públicos).",
        "mapa_valor": "Gera módulo completo (MD+PPTX+PDF) em 8min; usado em 3 disciplinas em curso; base para expandir para outros MBAs.",
        "pilotos": [
            {"nome": "Gerador de Casos com Fonte Auditada", "impacto": "alto", "viabilidade": "alto", "risco": "medio"},
        ],
        "processos_marcados": [
            ("2.2", "ia", "alta", "Coleta requisitos didáticos do curso"),
            ("1.5", "gap", "media", "Sem QA formal — depende de leitura humana"),
            ("1.6", "ia", "media", "Arquiva casos gerados para reuso"),
        ],
    },
    {
        "nome": "backtest-win",
        "empresa": "Pessoal",
        "porte": "N/A",
        "cargo_gp": "Autor",
        "n_projetos": 1,
        "pmo_ativo": False,
        "estrategia": 4, "dados": 4, "casos_uso": 4, "governanca": 3, "beneficios": 3,
        "mapa_contexto": "Backtest de estratégia WIN (mini-índice) rodando 100% no Mac com yfinance IBOV proxy; POC v3 fechada com 54 trades.",
        "mapa_dor": "Validar estratégia de congruências (Cong 3/3 responsável por 65% do PnL) antes de investir em MT5/Windows real-time.",
        "mapa_dados": "Séries históricas IBOV yfinance (60m/2y), regras de sinal codificadas, log de 54 trades com WR 77.8% e PF 6.11.",
        "mapa_riscos": "Overfitting ao histórico 2y; 2025 mostrou 60m/2y hostil; buraco de 13h operacional identificado.",
        "mapa_valor": "Prova de conceito para operar WIN via BTG com Pine Script quando validado o edge estatístico.",
        "pilotos": [
            {"nome": "Backtest Vetorizado Cong 3/3", "impacto": "medio", "viabilidade": "alto", "risco": "medio"},
        ],
        "processos_marcados": [
            ("7.3", "ia_po", "alta", "Análise de risco de estratégia — Monte Carlo faltando"),
            ("1.7", "ia_po", "media", "Monitorar performance vs. benchmark IBOV"),
            ("4.2", "ia", "media", "Estimar drawdown máximo via ML"),
        ],
    },
    {
        "nome": "prospec-osint",
        "empresa": "Eixo Estratégico",
        "porte": "MEI",
        "cargo_gp": "Fundador",
        "n_projetos": 1,
        "pmo_ativo": False,
        "estrategia": 4, "dados": 4, "casos_uso": 5, "governanca": 4, "beneficios": 4,
        "mapa_contexto": "App Streamlit :8504 de prospecção B2B em 2 modos: Consultoria (vender PO/Fin Corp) e Emprego Remoto; OpenAI+web_search focado em empresa.",
        "mapa_dor": "Identificar leads B2B qualificados (empresas com dor de otimização/finanças) sem gastar horas em pesquisa manual no LinkedIn e Google.",
        "mapa_dados": "APIs OpenAI e web_search, filtros por setor/porte/localização, templates de e-mail de abordagem, histórico de prospecção Eixo.",
        "mapa_riscos": "LGPD e ToS de LinkedIn — investigação de entidade, não de pessoa física; qualidade variável de fontes públicas.",
        "mapa_valor": "10-15 leads qualificados por sessão; base para vender consultoria Motor PO e mini-apps SaaS Eixo.",
        "pilotos": [
            {"nome": "Prospector B2B Consultoria", "impacto": "alto", "viabilidade": "alto", "risco": "medio"},
            {"nome": "Prospector Emprego Remoto", "impacto": "medio", "viabilidade": "alto", "risco": "baixo"},
        ],
        "processos_marcados": [
            ("5.1", "ia", "alta", "Identificar stakeholders decisores via NER"),
            ("2.2", "ia", "media", "Coleta contexto e dor do lead"),
            ("5.2", "ia_po", "media", "Segmentação SAPEVO-M por perfil de dor"),
        ],
    },
    {
        "nome": "concurso-radar",
        "empresa": "Pessoal",
        "porte": "N/A",
        "cargo_gp": "Autor",
        "n_projetos": 1,
        "pmo_ativo": False,
        "estrategia": 5, "dados": 3, "casos_uso": 4, "governanca": 3, "beneficios": 4,
        "mapa_contexto": "App Streamlit :8506 monitor de concursos públicos em 3 eixos: Analítico, Geoprocessamento, Docência; PND 2026 urgente (set/2026).",
        "mapa_dor": "Não perder edital relevante para o perfil próprio (analítico + geoprocessamento + docência) por falta de monitoramento sistemático.",
        "mapa_dados": "Feeds RSS de sites oficiais (Cebraspe, FGV, Vunesp), calendário de provas, editais anteriores, base de vagas por órgão.",
        "mapa_riscos": "Fontes RSS podem atrasar ou não cobrir 100% dos editais — combinar com watch manual em sites-chave.",
        "mapa_valor": "Alertas antecipados sobre editais alinhados ao perfil; foco no PND 2026 (Plano Nacional de Defesa) como prioridade.",
        "pilotos": [
            {"nome": "Monitor RSS de Editais", "impacto": "medio", "viabilidade": "alto", "risco": "baixo"},
        ],
        "processos_marcados": [
            ("7.6", "ia", "media", "Monitorar riscos de perder edital"),
            ("5.7", "ia", "media", "Classificar comunicações oficiais de bancas"),
        ],
    },
    {
        "nome": "produtos-mini-app (SaaS)",
        "empresa": "Eixo Estratégico",
        "porte": "MEI",
        "cargo_gp": "Fundador",
        "n_projetos": 1,
        "pmo_ativo": False,
        "estrategia": 4, "dados": 3, "casos_uso": 4, "governanca": 3, "beneficios": 4,
        "mapa_contexto": "Primeiro mini-app SaaS vendável do Eixo; Telegram diário com Top 3-5 produtos ML BR / dropship; Starter R$59 / Pro R$99.",
        "mapa_dor": "Empreendedor de e-commerce precisa saber o que está vendendo AGORA no Mercado Livre BR sem gastar horas no radar manual.",
        "mapa_dados": "Scraping Mercado Livre (produtos, preços, vendas estimadas), Google Trends BR, base de curadoria de nichos, histórico de tendências.",
        "mapa_riscos": "ToS do Mercado Livre; sazonalidade brusca (Black Friday); operação self-service sem aparição pessoal do dono (regra estratégica).",
        "mapa_valor": "Semana 1 do build concluída em 25/07; potencial R$ 3-5k/mês recorrente com 30-50 assinantes iniciais.",
        "pilotos": [
            {"nome": "Curador de Produtos ML BR", "impacto": "alto", "viabilidade": "medio", "risco": "medio"},
            {"nome": "Bot Telegram Diário", "impacto": "medio", "viabilidade": "alto", "risco": "baixo"},
        ],
        "processos_marcados": [
            ("4.1", "ia_po", "alta", "Preço-ótimo via SAPEVO-M validou R$59/99"),
            ("1.9", "ia", "media", "Encerrar semana 1 e planejar semana 2"),
            ("7.2", "gap", "media", "Riscos operacionais não sistematizados"),
        ],
    },
    {
        "nome": "pinescript-win-eixo",
        "empresa": "Pessoal",
        "porte": "N/A",
        "cargo_gp": "Autor",
        "n_projetos": 1,
        "pmo_ativo": False,
        "estrategia": 4, "dados": 4, "casos_uso": 3, "governanca": 4, "beneficios": 3,
        "mapa_contexto": "Estratégia WIN em Pine v5 (indicador + strategy) rodando nativo no BTG TradingView com dados WIN real-time.",
        "mapa_dor": "Operar WIN em conta real com regras auditáveis e reproduzíveis, sem depender de decisão discricionária no calor da hora.",
        "mapa_dados": "Cotações WIN real-time BTG, backtest interno TradingView, alertas configurados, git para versionamento das regras.",
        "mapa_riscos": "Diferença entre backtest e execução real (slippage, spread, latência); mudança regulatória CVM; risco de perda de capital.",
        "mapa_valor": "Estratégia auditável rodando na plataforma oficial do BTG; base para operar com disciplina algorítmica.",
        "pilotos": [
            {"nome": "Estratégia WIN Pine v5", "impacto": "medio", "viabilidade": "alto", "risco": "alto"},
        ],
        "processos_marcados": [
            ("1.4", "ia", "media", "Executar estratégia com disciplina algo"),
            ("1.8", "ia", "media", "Mudanças versionadas em git com backup automático"),
            ("7.6", "ia_po", "alta", "Monitorar drawdown vs. limite pré-definido"),
        ],
    },
]


def main() -> int:
    ja = db.contar_projetos()
    if ja > 0:
        print(f"[SKIP] Banco já tem {ja} projeto(s). Rode `python scripts/reset_db.py` se quiser recomeçar.")
        return 0

    inseridos = 0
    for spec in PROJETOS_LOCAIS:
        procs = spec.pop("processos_marcados")
        proj_id = db.salvar_projeto(spec)
        for pid, trat, crit, obs in procs:
            db.salvar_tratamento_pmbok(proj_id, pid, trat, crit, obs)
        inseridos += 1
        print(f"  [+] {spec['nome']} — id={proj_id} ({len(procs)} processos PMBOK marcados)")

    print(f"\n[OK] {inseridos} projetos locais cadastrados.")
    return inseridos


if __name__ == "__main__":
    sys.exit(0 if main() > 0 else 1)

#!/usr/bin/env python3
"""Cadastra os últimos 5 vencedores do PMI Project of the Year Award (2020-2024)
como projetos benchmark para comparação cross-portfólio.

Fonte: PMI.org (site bloqueia scraping direto — dados coletados via WebSearch em
2026-08-08). Cada projeto vem marcado com prefixo `[PMI Award]` para segregar
dos projetos locais reais.

Diagnóstico das 5 dimensões: heurística conservadora (maturidade alta em todas)
já que são projetos premiados internacionalmente. Ajustar se necessário.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import db  # noqa: E402


PMI_AWARDS = [
    {
        "nome": "[PMI Award 2024] Pertamina — One Price Fuel Program",
        "empresa": "Pertamina (estatal energia Indonésia)",
        "porte": "Grande",
        "cargo_gp": "Program Director",
        "n_projetos": 1,
        "pmo_ativo": True,
        "estrategia": 6, "dados": 5, "casos_uso": 6, "governanca": 6, "beneficios": 6,
        "mapa_contexto": "Programa nacional de equalização do preço do combustível em todas as regiões da Indonésia; PMI Project of the Year 2024.",
        "mapa_dor": "Disparidade de preços de combustível entre regiões remotas e capitais dificultava desenvolvimento econômico e mobilidade em áreas isoladas.",
        "mapa_dados": "Cadeia logística de distribuição de combustível para 17 mil ilhas indonésias, custos regionais, subsídios governamentais, política de precificação.",
        "mapa_riscos": "Risco político (mudança de governo), volatilidade cambial, complexidade logística marítima, aceitação social do modelo.",
        "mapa_valor": "Uniformização de preço em território de 17 mil ilhas; impacto social direto em milhões de indonésios em áreas remotas.",
        "pilotos": [],
        "processos_marcados": [
            ("1.1", "ia_po", "alta", "Iniciação em escala nacional com múltiplos entes públicos"),
            ("5.1", "ia_po", "alta", "Análise de redes sociais para stakeholders governamentais e sociedade"),
            ("4.1", "ia_po", "alta", "Portfólio financeiro considerando subsídios e câmbio"),
            ("7.3", "ia_po", "alta", "Monte Carlo em cenários geopolíticos"),
        ],
    },
    {
        "nome": "[PMI Award 2023] Caterpillar — Battery Electric 793 Mining Truck",
        "empresa": "Caterpillar Inc. (EUA)",
        "porte": "Grande",
        "cargo_gp": "Chief Project Engineer",
        "n_projetos": 1,
        "pmo_ativo": True,
        "estrategia": 6, "dados": 6, "casos_uso": 6, "governanca": 6, "beneficios": 5,
        "mapa_contexto": "Primeiro caminhão de mineração de grande porte (Cat 793) 100% elétrico a bateria; PMI Project of the Year 2023.",
        "mapa_dor": "Mineração pesada é grande emissora de GEE; falta alternativa elétrica para caminhões de payload alto usados globalmente.",
        "mapa_dados": "Ciclos operacionais em minas reais, dados de duty cycle, telemetria de frota diesel comparável, ensaios de bateria em condições extremas.",
        "mapa_riscos": "Novidade tecnológica sem análogo comercial; ciclo de vida de bateria em ambiente hostil; retorno econômico incerto na 1ª geração.",
        "mapa_valor": "Prova de conceito de zero-emission mining truck; abre categoria de mercado para transição energética na mineração global.",
        "pilotos": [],
        "processos_marcados": [
            ("6.2", "ia_po", "alta", "MILP para escolher entre baterias/tecnologias alternativas"),
            ("1.5", "ia_po", "alta", "Qualidade em prototipagem via ML+CEP"),
            ("7.2", "ia_po", "alta", "MICMAC de riscos tecnológicos"),
            ("1.6", "ia", "alta", "RAG sobre lições de projetos R&D anteriores"),
        ],
    },
    {
        "nome": "[PMI Award 2022] CDL — Rapid Screening Consortium",
        "empresa": "Creative Destruction Lab (Canadá)",
        "porte": "Média",
        "cargo_gp": "Program Chair",
        "n_projetos": 1,
        "pmo_ativo": False,
        "estrategia": 6, "dados": 5, "casos_uso": 6, "governanca": 5, "beneficios": 6,
        "mapa_contexto": "Consórcio multi-organizacional para triagem rápida de COVID-19 no Canadá durante a pandemia; PMI Project of the Year 2022.",
        "mapa_dor": "Faltava capacidade de screening rápido em locais de trabalho e escolas para manter economia funcionando durante a pandemia.",
        "mapa_dados": "Base epidemiológica canadense, capacidade de testes por laboratório, resultados por local, integrações com sistemas de saúde provinciais.",
        "mapa_riscos": "Regulatório Health Canada; urgência com qualidade; coordenação entre 12 provincias e centenas de organizações privadas.",
        "mapa_valor": "Milhões de testes rápidos coordenados; modelo replicado em outros países; base para futuras respostas rápidas a crises sanitárias.",
        "pilotos": [],
        "processos_marcados": [
            ("5.1", "ia_po", "alta", "Rede de stakeholders multi-organizacional"),
            ("5.5", "ia_po", "alta", "M/M/c para dimensionar capacidade de comunicação"),
            ("6.3", "ia_po", "alta", "Hungarian para alocar recursos entre provincias"),
            ("1.4", "ia", "alta", "Copiloto de coordenação em escala consorcial"),
        ],
    },
    {
        "nome": "[PMI Award 2021] US State Dept — FASTC Training Center",
        "empresa": "GSA / US State Department (EUA)",
        "porte": "Grande",
        "cargo_gp": "Project Executive",
        "n_projetos": 1,
        "pmo_ativo": True,
        "estrategia": 6, "dados": 5, "casos_uso": 5, "governanca": 6, "beneficios": 5,
        "mapa_contexto": "Foreign Affairs Security Training Center do Departamento de Estado dos EUA — complexo de treinamento em segurança diplomática; PMI Project of the Year 2021.",
        "mapa_dor": "Falta de facility unificado para treinamento de segurança diplomática após ataques a embaixadas; treinamento fragmentado em múltiplos locais.",
        "mapa_dados": "Requisitos de treinamento de agências federais, especificações de instalações de segurança, orçamento federal plurianual, cronograma legislativo.",
        "mapa_riscos": "Segurança nacional; orçamento sujeito a shutdown; requisitos técnicos secretos; múltiplas agências federais como stakeholders.",
        "mapa_valor": "Consolidação de treinamento crítico em um único campus com padrões de segurança de última geração para diplomatas americanos.",
        "pilotos": [],
        "processos_marcados": [
            ("1.3", "ia_po", "alta", "MILP make-or-buy em infraestrutura sensível"),
            ("1.7", "ia_po", "alta", "SDS para simular impacto de shutdowns"),
            ("5.2", "ia_po", "media", "Teoria dos Jogos para engajar múltiplas agências"),
            ("7.4", "ia_po", "alta", "Minimax para respostas em contexto adversarial"),
        ],
    },
    {
        "nome": "[PMI Award 2020] TANAP — Trans Anatolian Natural Gas Pipeline",
        "empresa": "SOCAR / BOTAS (Azerbaijão-Turquia)",
        "porte": "Grande",
        "cargo_gp": "Program Director",
        "n_projetos": 1,
        "pmo_ativo": True,
        "estrategia": 6, "dados": 5, "casos_uso": 5, "governanca": 6, "beneficios": 6,
        "mapa_contexto": "Um dos maiores gasodutos do mundo — 1.850 km atravessando toda a Turquia; conecta gás do Cáspio à Europa; PMI Project of the Year 2020.",
        "mapa_dor": "Diversificar fornecimento de gás natural europeu reduzindo dependência de Rússia; conectar reservas do Cáspio (Shah Deniz) à Europa Central.",
        "mapa_dados": "Traçado topográfico de 1.850 km, estudos ambientais, contratos com 4 países atravessados, dados sísmicos, política energética UE.",
        "mapa_riscos": "Geopolíticos altos (Rússia, Irã), sísmicos (Turquia), ambientais (áreas protegidas), atrasos por 4 jurisdições nacionais.",
        "mapa_valor": "Rota alternativa para 16 bcm/ano de gás; independência energética europeia; corredor sul do gás.",
        "pilotos": [],
        "processos_marcados": [
            ("7.1", "ia_po", "alta", "AHP para tolerância a risco geopolítico"),
            ("1.3", "ia_po", "alta", "MILP em aquisições multi-país"),
            ("3.2", "ia_po", "alta", "PERT + Monte Carlo em cronograma de 1850km"),
            ("5.2", "ia_po", "alta", "Teoria dos Jogos com 4 governos"),
            ("4.4", "ia", "alta", "Anomalia em gastos por trecho e por país"),
        ],
    },
]


def main() -> int:
    inseridos = 0
    ja_existentes = 0
    for spec in PMI_AWARDS:
        if db.obter_projeto_por_nome(spec["nome"]):
            ja_existentes += 1
            print(f"  [=] {spec['nome']} já cadastrado — pulando.")
            continue
        procs = spec.pop("processos_marcados")
        proj_id = db.salvar_projeto(spec)
        for pid, trat, crit, obs in procs:
            db.salvar_tratamento_pmbok(proj_id, pid, trat, crit, obs)
        inseridos += 1
        print(f"  [+] {spec['nome']} — id={proj_id} ({len(procs)} processos)")

    print(f"\n[OK] {inseridos} PMI Awards cadastrados ({ja_existentes} já existiam).")
    return inseridos


if __name__ == "__main__":
    sys.exit(0 if main() >= 0 else 1)

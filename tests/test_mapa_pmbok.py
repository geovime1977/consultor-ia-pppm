"""Testes do módulo mapa_pmbok — aba principal do consultor-ia-pppm."""
import json
from pathlib import Path

import pytest

from src import mapa_pmbok


DATA = Path(__file__).resolve().parent.parent / "data"


class TestCarregamentoDados:
    def test_carregar_processos_retorna_lista(self):
        processos = mapa_pmbok.carregar_processos()
        assert isinstance(processos, list)
        assert len(processos) == 40, "PMBOK 8 tem 40 processos"

    def test_todos_processos_tem_campos_obrigatorios(self):
        for p in mapa_pmbok.carregar_processos():
            for campo in ("id", "area", "grupo", "nome", "ia", "ia_po"):
                assert campo in p, f"Processo {p.get('id','?')} sem {campo}"

    def test_carregar_matriz_pilotos_processos(self):
        relacoes = mapa_pmbok._carregar_matriz()
        assert isinstance(relacoes, dict)
        assert len(relacoes) >= 12, "pelo menos os 12 pilotos originais"
        for pid, papeis in relacoes.items():
            assert "primaria" in papeis
            assert "secundaria" in papeis
            assert isinstance(papeis["primaria"], list)

    def test_carregar_pilotos(self):
        pilotos = mapa_pmbok._carregar_pilotos()
        assert len(pilotos) >= 12
        ids = {p["id"] for p in pilotos}
        for original in [
            "assistente-status-executivo",
            "radar-riscos-atrasos",
            "analise-sla",
        ]:
            assert original in ids

    def test_carregar_cases_index(self):
        idx = mapa_pmbok._carregar_cases_index()
        assert isinstance(idx, dict)
        for case_id, case in idx.items():
            assert "setor" in case
            assert "citacao_bezerra" in case


class TestIntegridadeCruzada:
    def test_pilotos_da_matriz_existem_no_catalogo(self):
        pilotos_catalogo = {p["id"] for p in mapa_pmbok._carregar_pilotos()}
        pilotos_matriz = set(mapa_pmbok._carregar_matriz().keys())
        orfaos = pilotos_matriz - pilotos_catalogo
        assert not orfaos, f"Pilotos na matriz sem definição no catálogo: {orfaos}"

    def test_processos_da_matriz_existem_no_pmbok(self):
        processos_ids = {p["id"] for p in mapa_pmbok.carregar_processos()}
        for pid, papeis in mapa_pmbok._carregar_matriz().items():
            for proc_id in papeis.get("primaria", []) + papeis.get("secundaria", []):
                assert proc_id in processos_ids, (
                    f"Piloto {pid} referencia processo inexistente {proc_id}"
                )

    def test_casos_bezerra_dos_processos_existem(self):
        idx_cases = mapa_pmbok._carregar_cases_index()
        for p in mapa_pmbok.carregar_processos():
            for cid in p.get("casos_bezerra", []):
                assert cid in idx_cases, (
                    f"Processo {p['id']} referencia case inexistente {cid}"
                )


class TestBenchmarkCobertura:
    def test_todos_40_processos_tem_metricas(self):
        n = sum(1 for p in mapa_pmbok.carregar_processos() if p.get("metricas"))
        assert n == 40, f"Só {n}/40 processos com métricas — merge incompleto"

    def test_todos_40_processos_tem_formatos_entrada(self):
        n = sum(
            1
            for p in mapa_pmbok.carregar_processos()
            if p.get("formatos_entrada_dados")
        )
        assert n == 40, f"Só {n}/40 processos com formatos — merge incompleto"

    def test_toda_metrica_tem_baseline_e_meta(self):
        for p in mapa_pmbok.carregar_processos():
            for i, m in enumerate(p.get("metricas", [])):
                assert m.get("baseline_mercado"), (
                    f"Processo {p['id']} métrica #{i} sem baseline_mercado"
                )
                assert m.get("meta_com_ia"), (
                    f"Processo {p['id']} métrica #{i} sem meta_com_ia"
                )
                for lado in ("baseline_mercado", "meta_com_ia"):
                    assert m[lado].get("confianca") in ("alta", "media", "baixa"), (
                        f"Processo {p['id']} métrica #{i} lado {lado}: confiança inválida"
                    )

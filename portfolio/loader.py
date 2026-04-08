import json
import os
from django.db import transaction

from .models import (
    TFC, Projeto, Docente, UnidadeCurricular, Tecnologia,
    Classificacao, MakingOf, Formacao, Competencia, Licenciatura
)


# ───────────────────────────────────────────────
# Caminho base para /data
# ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


# ───────────────────────────────────────────────
# LOAD UCs 
# ───────────────────────────────────────────────

import json
import os
from .models import UnidadeCurricular, Licenciatura

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def load_ucs(reset=False):
    path = os.path.join(DATA_DIR, "ULHT260-PT.json")

    if not os.path.exists(path):
        print("❌ Ficheiro base não encontrado")
        return

    if reset:
        UnidadeCurricular.objects.all().delete()
        print("🗑️ UCs apagadas")

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    # Criar licenciatura (1x apenas)
    lic, _ = Licenciatura.objects.get_or_create(
        nome=data.get("courseName", "Computing Engineering"),
        defaults={
            "ano_inicio": 2025,
            "universidade": "ULHT",
        }
    )

    count = 0


    for uc in data.get("courseFlatPlan", []):
        codigo = uc.get("curricularIUnitReadableCode")

        if not codigo:
            continue

        # tentar abrir ficheiro detalhe
        detail_path = os.path.join(DATA_DIR, f"{codigo}-PT.json")

        detail = {}
        if os.path.exists(detail_path):
            with open(detail_path, encoding="utf-8") as f:
                detail = json.load(f)

        UnidadeCurricular.objects.update_or_create(
            codigo=codigo,
            defaults={
                "nome": uc.get("curricularUnitName"),
                "ano": uc.get("curricularYear") or 1,
                "semestre": 1,  # simples e consistente
                "ects": uc.get("ects") or 0,
                "objetivos": detail.get("objectives", ""),
                "programa": detail.get("programme", ""),
                "licenciatura": lic,
            }
        )

        count += 1

    print(f"✅ {count} UCs carregadas")


# ───────────────────────────────────────────────
# LOAD TFCs
# ───────────────────────────────────────────────
def load_tfcs(reset=False):
    path = os.path.join(DATA_DIR, "tfcs_201.json")

    if not os.path.exists(path):
        print("❌ Ficheiro de TFCs não encontrado")
        return

    if reset:
        TFC.objects.all().delete()
        print("🗑️ TFCs apagados")

    with open(path, encoding="utf-8") as f:
        dados = json.load(f)

    if not isinstance(dados, list):
        print("❌ JSON inválido")
        return

    uc = UnidadeCurricular.objects.first()
    if not uc:
        print("❌ Corre load_ucs() primeiro")
        return

    with transaction.atomic():
        for item in dados:
            titulo = item.get("titulo")
            ano = item.get("ano") or 2025

            if not titulo:
                continue

            # 🔁 MAPEAMENTO (JSON → modelo)
            autor = item.get("autor(es)", "Desconhecido")

            

            # 🔁 ORIENTADORES
            orientador_raw = item.get("orientador", "")
            
            orientadores = [
                o.strip()
                for o in orientador_raw.replace(";", ",").split(",")
                if o.strip()
                ]
            # 💻 TECNOLOGIAS
            tecnologias_raw = item.get("Tecnologias usadas", "")
            tecnologias_lista = [
                t.strip()
                for t in tecnologias_raw.replace(";", ",").split(",")
                if t.strip()
                ]
            
            palavras_chave = item.get("Palavras chave", "")
            area = item.get("Áreas", "")

            # 🧱 Criar TFC primeiro
            tfc, _ = TFC.objects.update_or_create(
                titulo=titulo,
                defaults={
                    "ano": ano,
                    "resumo": item.get("sumario", ""),
                    "autor": autor,
                    "estado": "concluido",
                    "unidade_curricular": uc,
                    "palavras_chave": palavras_chave,
                    "area": area,
                    }
                    )
            
            # 🔄 limpar relações
            tfc.orientadores.clear()
            tfc.tecnologias.clear()
            # 👨‍🏫 ORIENTADORES (sem duplicados)
            nomes_orientadores = set()
            
            for nome in orientadores:
                nome_clean = nome.strip()
                if nome_clean.lower() in nomes_orientadores:
                    continue
                
                nomes_orientadores.add(nome_clean.lower())
                docente, _ = Docente.objects.get_or_create(nome=nome_clean)
                tfc.orientadores.add(docente)
                
                
                # 💻 TECNOLOGIAS (sem duplicados)
                nomes_tecnologias = set()
                for nome in tecnologias_lista:
                    nome_clean = nome.strip()
                    if nome_clean.lower() in nomes_tecnologias:
                        continue
                    
                    nomes_tecnologias.add(nome_clean.lower())
                    tec, _ = Tecnologia.objects.get_or_create(nome=nome_clean)
                    tfc.tecnologias.add(tec)
                    

    print("✅ TFCs carregados")
# ───────────────────────────────────────────────
# LOAD TUDO
# ───────────────────────────────────────────────
def load_all():
    load_ucs()
    load_tfcs()


def reset_all():
    print("⚠️ Reset completo da base de dados...")

    # Ordem IMPORTA (dependências!)
    Classificacao.objects.all().delete()
    MakingOf.objects.all().delete()
    Formacao.objects.all().delete()
    Competencia.objects.all().delete()

    TFC.objects.all().delete()
    Projeto.objects.all().delete()

    Tecnologia.objects.all().delete()
    Docente.objects.all().delete()
    UnidadeCurricular.objects.all().delete()
    Licenciatura.objects.all().delete()

    print("✅ Base de dados completamente limpa")
import requests
import json
import os

schoolYear = '202526'
course = 260  # LEI

# ───────────────────────────────────────────────
# Caminho para a pasta data
# ───────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# ───────────────────────────────────────────────
# Loop idiomas
# ───────────────────────────────────────────────
for language in ['PT', 'ENG']:

    # ── Pedido do curso ─────────────────────────
    url = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetCourseDetail'

    payload = {
        'language': language,
        'courseCode': course,
        'schoolYear': schoolYear
    }

    headers = {'content-type': 'application/json'}

    response = requests.post(url, json=payload, headers=headers)
    response_dict = response.json()

    # ── Guardar ficheiro do curso ───────────────
    with open(os.path.join(DATA_DIR, f"ULHT{course}-{language}.json"), "w", encoding="utf-8") as f:
        json.dump(response_dict, f, indent=4)

    print(f"Curso guardado: ULHT{course}-{language}.json")

    # ── Loop UCs ────────────────────────────────
    print("Total UCs:", len(response_dict.get('courseFlatPlan', [])))

    for uc in response_dict.get('courseFlatPlan', []):
        codigo = uc['curricularIUnitReadableCode']
        print("UC:", codigo)

        url_uc = 'https://secure.ensinolusofona.pt/dados-publicos-academicos/resources/GetSIGESCurricularUnitDetails'

        payload_uc = {
            'language': language,
            'curricularIUnitReadableCode': codigo,
        }

        response_uc = requests.post(url_uc, json=payload_uc, headers=headers)
        response_uc_dict = response_uc.json()

        # ── GUARDAR CADA UC (AQUI É O IMPORTANTE) ──
        with open(os.path.join(DATA_DIR, f"{codigo}-{language}.json"), "w", encoding="utf-8") as f:
            json.dump(response_uc_dict, f, indent=4)

print("\n✅ Todos os JSONs foram guardados!")
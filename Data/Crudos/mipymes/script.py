"""
VERSIÓN SIMPLE: Unir MIPYMES
"""

import json
import os

# 1. Listar archivos JSON (excluyendo este script)
archivos = [f for f in os.listdir('.')
           if f.endswith('.json') and f != 'mipymes_unidas.json']

print(f"Uniendo {len(archivos)} archivos MIPYME...")

# 2. Leer todos
datos = []
for archivo in archivos:
    with open(archivo, 'r', encoding='utf-8') as f:
        datos.append(json.load(f))


# 4. Guardar unido
with open('../../Procesados/mipymes_unidad.json', 'w', encoding='utf-8') as f:
    json.dump(datos, f, indent=2, ensure_ascii=False)

print(f"✅ Listo! {len(datos)} MIPYMES unidas")
print("💾 Guardado en: datos/processed/mipymes_unidas.json")
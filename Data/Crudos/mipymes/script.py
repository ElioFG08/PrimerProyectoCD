# agregar_unidad.py
import json
import os

# Unidades para cada producto
unidades = {
    "Spaguetis": "500g",
    "Arroz": "1kg",
    "Azucar": "1kg",
    "Sal": "1kg",
    "Frijoles": "1kg",
    "Aceite": "900ml",
    "Huevos": "unidad",
    "Pollo": "lb",
    "Leche": "unidad",
    "Papel Higienico": "Paquete",
    "Detergente": "500g",
    "Pasta Dental": "tubo"
}

# Procesar cada archivo
for i in range(1, 31):
    nombre_archivo = f"mipyme_{i:02d}.json"

    if not os.path.exists(nombre_archivo):
        print(f"❌ {nombre_archivo} no encontrado")
        continue

    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    for producto in datos["productos"]:
        nombre = producto["nombre"]
        producto["unidad"] = unidades.get(nombre, "unidad")

    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

    print(f"✅ {nombre_archivo}")

print("\n✅ ¡Listo! Campo 'unidad' añadido a 30 archivos")
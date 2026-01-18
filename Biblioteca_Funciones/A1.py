# Biblioteca_Funciones/funciones_analisis1.py
import json

def cargar_datos(ruta):
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def calcular_disponibilidad(datos):
    mipymes = set(d['mipyme_id'] for d in datos)
    productos = {}

    for d in datos:
        prod = d['producto_nombre']
        if prod not in productos:
            productos[prod] = set()
        productos[prod].add(d['mipyme_id'])

    resultados = []
    for prod, mipymes_con in productos.items():
        pct = (len(mipymes_con) / len(mipymes)) * 100
        resultados.append((prod, pct, len(mipymes_con)))

    resultados.sort(key=lambda x: x[1])
    return resultados, len(mipymes)
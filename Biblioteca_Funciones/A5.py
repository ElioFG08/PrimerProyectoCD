
import json
from collections import defaultdict


def cargar_datos(ruta):

    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)

def calcular_promedios_mipymes(datos_mipymes):

    sumas = defaultdict(list)

    for item in datos_mipymes:
        nombre = item['producto_nombre']


        if 'Huevos' in nombre:
            continue

        precio = item['precio_cup']
        sumas[nombre].append(precio)

    # Calcular promedio
    promedios = {}
    for nombre, precios in sumas.items():
        promedios[nombre] = sum(precios) / len(precios)
    return promedios

def calcular_promedios_online(datos_online, tasa_cambio=470):
    """Calcular precio promedio por producto en Online (convertido a CUP)"""
    sumas = defaultdict(list)

    for item in datos_online:
        if item['precio'] is not None:  # Ignorar precios nulos
            nombre = item['nombre']

            # CORRECCIÓN: El continue debe ir ANTES de procesar
            if 'Huevos' in nombre:
                continue  # ← SALTA HUEVOS (mover arriba)

            precio_cup = item['precio'] * tasa_cambio
            sumas[nombre].append(precio_cup)

    # Calcular promedio
    promedios = {}
    for nombre, precios in sumas.items():
        promedios[nombre] = sum(precios) / len(precios)

    return promedios

def generar_comparativa(ruta_mipymes, ruta_online, tasa_cambio=470):

    # 1. Cargar datos
    datos_mipymes = cargar_datos(ruta_mipymes)
    datos_online = cargar_datos(ruta_online)
    promedios_mipymes = calcular_promedios_mipymes(datos_mipymes)
    promedios_online = calcular_promedios_online(datos_online, tasa_cambio)

    # 3. Encontrar productos comunes
    productos_comunes = set(promedios_mipymes.keys()) & set(promedios_online.keys())

    # 4. Crear lista comparativa
    comparativa = []
    for producto in productos_comunes:
        mipyme_cup = promedios_mipymes[producto]
        online_cup = promedios_online[producto]
        diferencia = online_cup - mipyme_cup
        ratio = online_cup / mipyme_cup

        comparativa.append({
            'nombre': producto,
            'mipyme_cup': round(mipyme_cup, 2),
            'online_cup': round(online_cup, 2),
            'diferencia': round(diferencia, 2),
            'ratio': round(ratio, 2)
        })

    # 5. Ordenar por diferencia (mayor a menor)
    comparativa.sort(key=lambda x: x['diferencia'], reverse=True)
    return comparativa

def obtener_top_productos(comparativa, n=3, criterio='diferencia'):
    if criterio == 'diferencia':
        return sorted(comparativa, key=lambda x: x['diferencia'], reverse=True)[:n]
    elif criterio == 'ratio':
        return sorted(comparativa, key=lambda x: x['ratio'], reverse=True)[:n]
    return comparativa[:n]

def guardar_resultados(comparativa, ruta_salida):
    """Guardar resultados en JSON"""
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(comparativa, f, indent=2, ensure_ascii=False)
    print(f"💾 Resultados guardados en: {ruta_salida}")
    return ruta_salida

def preparar_comparativa(ruta_mipymes, ruta_online, tasa_cambio=470):
    return generar_comparativa(ruta_mipymes, ruta_online, tasa_cambio)
import json
from collections import defaultdict

def cargar_datos(ruta):

    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)


def calcular_disponibilidad(datos):

    mipymes = [d['mipyme_id'] for d in datos] #guardo una lista con los id de las mipymes
    productos = {} #diccionario para guardar (producto:lista de las mipymes que disponen de este)

    for d in datos: # d toma valor de cada registro en productos_planos.json
        prod = d['producto_nombre']
        if prod not in productos:
            productos[prod] = 0
        productos[prod] += 1

    resultados = []
    for prod, count in productos.items():
        pct = (count / len(mipymes)) * 100
        resultados.append((prod, pct)),

    resultados.sort(key=lambda x: x[1])
    return resultados,len(mipymes)


def calcular_precios(datos):

    precios_por_producto = {}

    for registro in datos:
        producto = registro['producto_nombre']
        precio = registro['precio_cup']

        if producto not in precios_por_producto:
            precios_por_producto[producto] = []
        precios_por_producto[producto].append(precio)

    resultados = []
    for producto, precios in precios_por_producto.items():
        resultados.append({
            'producto': producto,
            'promedio': sum(precios) / len(precios),
            'min': min(precios),
            'max': max(precios),
            'muestras': len(precios)
        })

    resultados.sort(key=lambda x: x['promedio'])

def calcular_variacion_precios(precios):
    resultados = []
    for p in precios:

        variacion = ((p['max'] - p['min']) / p['min']) * 100
        resultados.append({
            'producto': p['producto'],
            'variacion': variacion,
            'min': p['min'],
            'max': p['max'],
            'promedio': p['promedio']
        })

    resultados.sort(key=lambda x: x['variacion'], reverse=True)
    return resultados



def analizar_asequibilidad(ruta_salarios, productos):

    try:
        with open(ruta_salarios, 'r', encoding='utf-8') as f:
            datos_salarios = json.load(f)

        salarios = datos_salarios.get('Salarios por actividad económica', {})

        productos_basicos = ["Arroz", "Frijoles", "Aceite", "Azucar", "Spaguetis",
                             "Sal", "Pasta Dental", "Detergente"]


        costo_total = 0.0
        for producto in productos_basicos:
            precios = [p['precio_cup'] for p in productos if p['producto_nombre'] == producto]
            if precios:
                costo_total += sum(precios) / len(precios)

        sectores_analizar = ["Educación", "Salud pública y asistencia social",
                             "Construcción", "Suministro de electricidad , gas y agua",
                             "Agricultura , ganadería y silvicultura",
                             "Comercio y reparación de efectos personales"]

        resultados = {}
        for sector in sectores_analizar:
            if sector in salarios:
                salario = salarios[sector]
                porcentaje = (costo_total / salario) * 100 if salario > 0 else 0
                resultados[sector] = {'salario': salario, 'porcentaje': porcentaje}

        if resultados:
            porcentajes = [d['porcentaje'] for d in resultados.values()]
            resumen = {
                'costo_canasta': costo_total,
                'promedio': sum(porcentajes) / len(porcentajes),
                'maximo': max(porcentajes),
                'minimo': min(porcentajes),
                'total_sectores': len(resultados)
            }
        else:
            resumen = {}

        return resultados, costo_total, resumen

    except Exception as e:
        print(f"Error: {e}")
        return {}, 0, {}






def calcular_promedios_mipymes(datos_mipymes):
    sumas = defaultdict(list)
    for item in datos_mipymes:
        nombre = item['producto_nombre']
        if 'Huevos' in nombre: continue
        sumas[nombre].append(item['precio_cup'])

    return {nombre: sum(precios) / len(precios) for nombre, precios in sumas.items()}


def calcular_promedios_online(datos_online, tasa_cambio=470):
    sumas = defaultdict(list)
    for item in datos_online:
        if item['precio'] is not None:
            nombre = item['nombre']
            if 'Huevos' in nombre: continue
            sumas[nombre].append(item['precio'] * tasa_cambio)

    return {nombre: sum(precios) / len(precios) for nombre, precios in sumas.items()}


def generar_comparativa(ruta_mipymes, ruta_online, tasa_cambio=470):

    datos_mipymes = cargar_datos(ruta_mipymes)
    datos_online = cargar_datos(ruta_online)

    promedios_mipymes = calcular_promedios_mipymes(datos_mipymes)
    promedios_online = calcular_promedios_online(datos_online, tasa_cambio)

    productos_comunes = set(promedios_mipymes.keys()) & set(promedios_online.keys())

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

    comparativa.sort(key=lambda x: x['diferencia'], reverse=True)
    return comparativa


def obtener_top_productos(comparativa, n=3, criterio='diferencia'):
    if criterio == 'diferencia':
        return sorted(comparativa, key=lambda x: x['diferencia'], reverse=True)[:n]
    elif criterio == 'ratio':
        return sorted(comparativa, key=lambda x: x['ratio'], reverse=True)[:n]
    return comparativa[:n]


def guardar_resultados(comparativa, ruta_salida):

    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(comparativa, f, indent=2, ensure_ascii=False)
    print(f"💾 Guardado en: {ruta_salida}")
    return ruta_salida

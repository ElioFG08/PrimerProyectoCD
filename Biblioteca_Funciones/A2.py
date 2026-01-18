# Biblioteca_Funciones/precios.py
# Funciones específicas para el Análisis 2

def calcular_precios(datos):

    # 1. Agrupar precios por producto
    precios_por_producto = {}

    for registro in datos:
        producto = registro['producto_nombre']
        precio = registro['precio_cup']

        if producto not in precios_por_producto:
            precios_por_producto[producto] = []

        precios_por_producto[producto].append(precio)

    # 2. Calcular estadísticas para cada producto
    resultados = []

    for producto, precios in precios_por_producto.items():
        promedio = sum(precios) / len(precios)

        resultados.append({
            'producto': producto,
            'promedio': promedio,
            'min': min(precios),
            'max': max(precios),
            'muestras': len(precios)
        })

    # 3. Ordenar por precio promedio (menor->mayor)
    resultados.sort(key=lambda x: x['promedio'])

    return resultados


def encontrar_producto_mas_caro(precios):
    return max(precios, key=lambda x: x['promedio'])


def encontrar_producto_mas_barato(precios):
    return min(precios, key=lambda x: x['promedio'])

def calcular_variacion_precios(precios):
    resultados = []

    for p in precios:
        if p['min'] > 0:  # Evitar división por cero
            variacion = ((p['max'] - p['min']) / p['min']) * 100
        else:
            variacion = 0

        resultados.append({
            'producto': p['producto'],
            'variacion': variacion,
            'min': p['min'],
            'max': p['max'],
            'promedio': p['promedio']
        })

    # Ordenar por mayor variación
    resultados.sort(key=lambda x: x['variacion'], reverse=True)
    return resultados
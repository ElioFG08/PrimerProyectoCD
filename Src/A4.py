# src/analisis4.py

import json
from typing import Dict, List, Tuple

def analizar_asequibilidad(ruta_salarios: str, productos: List[Dict]) -> Tuple[Dict, float, Dict]:

    try:
        # 1. Cargar salarios
        with open(ruta_salarios, 'r', encoding='utf-8') as f:
            datos_salarios = json.load(f)

        salarios = datos_salarios.get('Salarios por actividad económica', {})

        # 2. Calcular costo de 8 productos básicos
        productos_basicos = ["Arroz", "Frijoles", "Aceite", "Huevos",
                             "Azucar", "Spaguetis", "Sal", "Pasta Dental"]

        costo_total = 0.0
        for producto in productos_basicos:
            # Encontrar precios del producto
            precios = [p['precio_cup'] for p in productos if p['producto_nombre'] == producto]
            if precios:
                costo_total += sum(precios) / len(precios)

        # 3. Calcular porcentajes para sectores clave
        sectores_analizar = [
            "Educación",
            "Salud pública y asistencia social",
            "Construcción",
            "Suministro de electricidad , gas y agua",
            "Agricultura , ganadería y silvicultura",
            "Comercio y reparación de efectos personales"
        ]

        resultados = {}
        for sector in sectores_analizar:
            if sector in salarios:
                salario = salarios[sector]
                porcentaje = (costo_total / salario) * 100 if salario > 0 else 0
                resultados[sector] = {
                    'salario': salario,
                    'porcentaje': porcentaje
                }

        # 4. Calcular estadísticas
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
        print(f"Error en análisis: {e}")
        return {}, 0, {}
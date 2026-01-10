"""
BIBLIOTECA COMPLETA DE ANÁLISIS MIPYME
Contiene todas las funciones para los 5 análisis
"""

import json
import os
import statistics
from collections import defaultdict


# ============================================================================
# FUNCIONES BÁSICAS DE CARGA Y GUARDADO
# ============================================================================

def cargar_datos_mipymes(ruta_archivo: str):
    """
    Carga datos desde un archivo JSON de MIPYMES
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        print(f"✅ Datos cargados: {len(datos)} MIPYMES")
        return datos
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {ruta_archivo}")
        print(f"   Directorio actual: {os.getcwd()}")
        return None
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return None


def cargar_datos(ruta_archivo: str):
    """
    Carga cualquier archivo JSON (genérico)
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Archivo no encontrado: {ruta_archivo}")
        return None
    except Exception as e:
        print(f"⚠️  Error cargando {ruta_archivo}: {e}")
        return None


def guardar_json(datos, ruta_archivo: str):
    """
    Guarda datos en un archivo JSON
    """
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)

        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)
        print(f"💾 Guardado: {ruta_archivo}")
        return True
    except Exception as e:
        print(f"❌ Error guardando {ruta_archivo}: {e}")
        return False


# ============================================================================
# FUNCIÓN 1: CREAR ESTRUCTURA PLANA
# ============================================================================

def crear_estructura_plana(mipymes):
    """
    Convierte datos anidados en lista plana de productos
    """
    productos_planos = []

    for mipyme in mipymes:
        # Información básica
        mipyme_id = mipyme.get('Mipyme_id', '')
        municipio = mipyme.get('municipio', '')

        # Convertir coordenadas a float
        try:
            latitud = float(mipyme.get('latitud', 0))
        except:
            latitud = 0.0

        try:
            longitud = float(mipyme.get('longitud', 0))
        except:
            longitud = 0.0

        # Procesar cada producto
        for producto in mipyme.get('productos', []):
            precio = producto.get('precio')

            # Solo productos con precio disponible
            if precio is not None:
                registro = {
                    'mipyme_id': mipyme_id,
                    'municipio': municipio,
                    'latitud': latitud,
                    'longitud': longitud,
                    'producto_id': producto.get('producto_id', ''),
                    'producto_nombre': producto.get('nombre', ''),
                    'precio_cup': float(precio),
                    'unidad': producto.get('unidad', '')
                }
                productos_planos.append(registro)

    print(f"📊 Estructura plana creada: {len(productos_planos)} productos")
    return productos_planos


# ============================================================================
# ANÁLISIS 1: DISPONIBILIDAD
# ============================================================================

def analizar_disponibilidad(mipymes):
    """
    Analiza qué productos son más difíciles de encontrar
    """
    print("📋 Analizando disponibilidad de productos...")

    # Contar productos totales vs disponibles
    conteo_productos = defaultdict(lambda: {'total': 0, 'disponible': 0})
    conteo_municipios = defaultdict(lambda: {'total': 0, 'disponible': 0})

    for mipyme in mipymes:
        municipio = mipyme.get('municipio', 'desconocido')

        for producto in mipyme.get('productos', []):
            nombre = producto.get('nombre', '')

            # Contar por producto
            conteo_productos[nombre]['total'] += 1
            if producto.get('precio') is not None:
                conteo_productos[nombre]['disponible'] += 1

            # Contar por municipio
            conteo_municipios[municipio]['total'] += 1
            if producto.get('precio') is not None:
                conteo_municipios[municipio]['disponible'] += 1

    # Calcular porcentajes
    resultados_productos = {}
    for producto, conteo in conteo_productos.items():
        if conteo['total'] > 0:
            porcentaje = (conteo['disponible'] / conteo['total']) * 100
            resultados_productos[producto] = {
                'total': conteo['total'],
                'disponible': conteo['disponible'],
                'porcentaje_disponible': round(porcentaje, 1)
            }

    resultados_municipios = {}
    for municipio, conteo in conteo_municipios.items():
        if conteo['total'] > 0:
            porcentaje = (conteo['disponible'] / conteo['total']) * 100
            resultados_municipios[municipio] = {
                'total': conteo['total'],
                'disponible': conteo['disponible'],
                'porcentaje_disponible': round(porcentaje, 1)
            }

    # Ordenar por disponibilidad (menor a mayor)
    productos_ordenados = sorted(
        resultados_productos.items(),
        key=lambda x: x[1]['porcentaje_disponible']
    )

    municipios_ordenados = sorted(
        resultados_municipios.items(),
        key=lambda x: x[1]['porcentaje_disponible']
    )

    print(f"  • Productos analizados: {len(resultados_productos)}")
    print(f"  • Municipios analizados: {len(resultados_municipios)}")

    return {
        'por_producto': dict(productos_ordenados),
        'por_municipio': dict(municipios_ordenados)
    }


# ============================================================================
# ANÁLISIS 2: PRECIOS
# ============================================================================

def analizar_precios(productos_planos):
    """
    Analiza precios por producto (promedio, mínimo, máximo)
    """
    print("💰 Analizando precios...")

    # Agrupar precios por producto
    precios_por_producto = defaultdict(list)

    for producto in productos_planos:
        nombre = producto['producto_nombre']
        precios_por_producto[nombre].append(producto['precio_cup'])

    # Calcular estadísticas
    resultados = {}
    for producto, precios in precios_por_producto.items():
        if precios:
            resultados[producto] = {
                'muestras': len(precios),
                'promedio': round(statistics.mean(precios), 1),
                'mediana': round(statistics.median(precios), 1),
                'minimo': min(precios),
                'maximo': max(precios),
                'rango': max(precios) - min(precios),
                'desviacion': round(statistics.stdev(precios), 1) if len(precios) > 1 else 0
            }

    # Ordenar por precio promedio (más caro primero)
    productos_ordenados = sorted(
        resultados.items(),
        key=lambda x: x[1]['promedio'],
        reverse=True
    )

    print(f"  • Productos con precio: {len(resultados)}")

    return dict(productos_ordenados)


# ============================================================================
# ANÁLISIS 3: GEOGRÁFICO
# ============================================================================

def analisis_geografico(productos_planos):
    """
    Analiza precios por ubicación geográfica
    """
    print("📍 Analizando distribución geográfica...")

    # Agrupar por municipio
    precios_por_municipio = defaultdict(list)
    coordenadas_por_municipio = defaultdict(list)

    for producto in productos_planos:
        municipio = producto['municipio']
        precios_por_municipio[municipio].append(producto['precio_cup'])
        coordenadas_por_municipio[municipio].append({
            'lat': producto['latitud'],
            'lon': producto['longitud']
        })

    # Calcular estadísticas por municipio
    resultados = {}
    for municipio, precios in precios_por_municipio.items():
        if precios:
            # Promedio de coordenadas
            coords = coordenadas_por_municipio[municipio]
            lat_prom = sum(c['lat'] for c in coords) / len(coords)
            lon_prom = sum(c['lon'] for c in coords) / len(coords)

            resultados[municipio] = {
                'muestras': len(precios),
                'precio_promedio': round(statistics.mean(precios), 1),
                'precio_minimo': min(precios),
                'precio_maximo': max(precios),
                'latitud_promedio': round(lat_prom, 6),
                'longitud_promedio': round(lon_prom, 6)
            }

    # Ordenar por precio promedio (más caro primero)
    municipios_ordenados = sorted(
        resultados.items(),
        key=lambda x: x[1]['precio_promedio'],
        reverse=True
    )

    print(f"  • Municipios analizados: {len(resultados)}")

    return dict(municipios_ordenados)


# ============================================================================
# ANÁLISIS 4: ASEQUIBILIDAD (con salarios ONEI)
# ============================================================================

def analizar_asequibilidad(productos_planos, salarios_onei):
    """
    Calcula días de salario necesarios para comprar cada producto
    """
    print("💼 Analizando asequibilidad vs salarios ONEI...")

    # Calcular precio promedio por producto
    precios_promedio = {}
    precios_por_producto = defaultdict(list)

    for producto in productos_planos:
        nombre = producto['producto_nombre']
        precios_por_producto[nombre].append(producto['precio_cup'])

    for producto, precios in precios_por_producto.items():
        if precios:
            precios_promedio[producto] = statistics.mean(precios)

    # Calcular días de salario para cada sector
    resultados = {}

    for producto, precio_promedio in precios_promedio.items():
        resultados[producto] = {
            'precio_promedio_cup': round(precio_promedio, 1),
            'dias_salario_por_sector': {}
        }

        for sector, salario_mensual in salarios_onei.items():
            # Calcular días de salario
            salario_diario = salario_mensual / 30
            dias_necesarios = precio_promedio / salario_diario

            resultados[producto]['dias_salario_por_sector'][sector] = {
                'salario_mensual': salario_mensual,
                'dias_necesarios': round(dias_necesarios, 1),
                'porcentaje_salario_mensual': round((precio_promedio / salario_mensual) * 100, 1)
            }

    # Encontrar el producto más caro en términos de días de salario
    if resultados:
        producto_mas_caro = None
        max_dias = 0
        sector_referencia = list(salarios_onei.keys())[0] if salarios_onei else None

        for producto, datos in resultados.items():
            if sector_referencia in datos['dias_salario_por_sector']:
                dias = datos['dias_salario_por_sector'][sector_referencia]['dias_necesarios']
                if dias > max_dias:
                    max_dias = dias
                    producto_mas_caro = producto

        if producto_mas_caro:
            print(f"  • Producto más caro en días de salario: {producto_mas_caro} ({max_dias:.1f} días)")

    return resultados


# ============================================================================
# FUNCIÓN PRINCIPAL CORREGIDA
# ============================================================================

def ejecutar_analisis_completo():
    """Ejecuta todos los análisis y guarda resultados"""

    print("=" * 60)
    print("🚀 EJECUTANDO ANÁLISIS COMPLETO MIPYME")
    print("=" * 60)

    # ======================================================================
    # CONFIGURACIÓN INTELIGENTE DE RUTAS
    # ======================================================================

    print(f"📁 Directorio actual: {os.getcwd()}")

    # Buscar el archivo JSON unido
    rutas_posibles = [
        'Data/Procesados/mipymes_unidas.json',  # Desde raíz
        '../Data/Procesados/mipymes_unidas.json',  # Desde Src/
        '../../Data/Procesados/mipymes_unidas.json',  # Otra posibilidad
    ]

    ruta_encontrada = None
    for ruta in rutas_posibles:
        if os.path.exists(ruta):
            ruta_encontrada = ruta
            print(f"✅ Archivo encontrado: {ruta}")
            break

    if not ruta_encontrada:
        print("❌ ERROR: No se encontró mipymes_unidas.json")
        print("\n🎯 POSIBLES SOLUCIONES:")
        print("1. Asegúrate de ejecutar desde la carpeta correcta:")
        print("   cd 'D:\\Elio\\Data Science\\Curso 25-26\\Programacion\\1erProyectoCD'")
        print("   python Src\\analisis.py")
        print("\n2. O crea el archivo unido primero:")
        print("   cd Data\\Crudos\\mipymes")
        print("   python unir_mipymes.py")
        return

    # ======================================================================
    # 1. CARGAR DATOS MIPYME
    # ======================================================================

    datos = cargar_datos_mipymes(ruta_encontrada)
    if not datos:
        print("❌ No se pudieron cargar los datos.")
        return

    # ======================================================================
    # 2. CREAR ESTRUCTURA PLANA
    # ======================================================================

    productos_planos = crear_estructura_plana(datos)

    # Usar rutas relativas consistentes
    carpeta_procesados = 'Data/Procesados'

    guardar_json(productos_planos, f'{carpeta_procesados}/productos_planos.json')

    # ======================================================================
    # 3. ANÁLISIS 1: DISPONIBILIDAD
    # ======================================================================

    print("\n📊 ANÁLISIS 1: DISPONIBILIDAD")
    disponibilidad = analizar_disponibilidad(datos)
    guardar_json(disponibilidad, f'{carpeta_procesados}/analisis_disponibilidad.json')

    # ======================================================================
    # 4. ANÁLISIS 2: PRECIOS
    # ======================================================================

    print("\n💰 ANÁLISIS 2: PRECIOS")
    precios = analizar_precios(productos_planos)
    guardar_json(precios, f'{carpeta_procesados}/analisis_precios.json')

    # ======================================================================
    # 5. ANÁLISIS 3: GEOGRÁFICO
    # ======================================================================

    print("\n📍 ANÁLISIS 3: GEOGRÁFICO")
    geografico = analisis_geografico(productos_planos)
    guardar_json(geografico, f'{carpeta_procesados}/analisis_geografico.json')

    # ======================================================================
    # 6. ANÁLISIS 4: ASEQUIBILIDAD (con salarios ONEI)
    # ======================================================================

    print("\n💼 ANÁLISIS 4: ASEQUIBILIDAD")

    # Buscar archivo de salarios
    # Buscar archivo de salarios - RUTA CORRECTA
    rutas_salarios = [
        'Data/Crudos/salarios_cuba/salarios.json',  # ← NUEVA RUTA
        '../Data/Crudos/salarios_cuba/salarios.json',

    ]

    salarios_onei = None
    for ruta_sal in rutas_salarios:
        if os.path.exists(ruta_sal):
            salarios_onei = cargar_datos(ruta_sal)
            if salarios_onei:
                break

    if salarios_onei:
        # Extraer solo los salarios
        salarios = salarios_onei.get("Salarios por actividad económica", {})

        if salarios:
            # ANÁLISIS 4: Asequibilidad
            asequibilidad = analizar_asequibilidad(productos_planos, salarios)
            guardar_json(asequibilidad, f'{carpeta_procesados}/analisis_asequibilidad.json')
        else:
            print("⚠️  No se encontraron datos de salarios en el archivo ONEI")
    else:
        print("⚠️  Salarios ONEI no encontrados, omitiendo análisis 4")
        print("   Puedes añadirlos después en: Data/Crudos/salarios_onei.json")

    # ======================================================================
    # RESUMEN FINAL
    # ======================================================================

    print("\n" + "=" * 60)
    print("✅ ANÁLISIS COMPLETADOS")
    print("=" * 60)
    print(f"\n📁 ARCHIVOS GENERADOS EN {carpeta_procesados}/:")
    print("1. productos_planos.json - Estructura plana para análisis")
    print("2. analisis_disponibilidad.json - Análisis 1")
    print("3. analisis_precios.json - Análisis 2")
    print("4. analisis_geografico.json - Análisis 3")

    if salarios_onei and salarios_onei.get("Salarios por actividad económica"):
        print("5. analisis_asequibilidad.json - Análisis 4")

    print("\n🎯 ¡Ahora puedes crear los gráficos en tu notebook!")


# ============================================================================
# EJECUCIÓN DIRECTA
# ============================================================================

if __name__ == "__main__":
    """
    Solo se ejecuta si llamas directamente a este archivo
    """
    ejecutar_analisis_completo()
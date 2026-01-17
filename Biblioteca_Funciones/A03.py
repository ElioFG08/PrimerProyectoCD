# procesar.py
import json
import os


def cargar_datos_procesados():
    """
    Carga directamente los datos ya procesados desde salarios_procesados.json
    """
    # Ir a la carpeta Data/Crudos/salarios_cuba desde Biblioteca_Funciones
    ruta_script = os.path.dirname(__file__)
    ruta_json = os.path.join(ruta_script, '..', 'Data', 'Crudos', 'salarios_cuba', 'salarios_procesados.json')
    ruta_json = os.path.abspath(ruta_json)

    # Cargar datos procesados
    with open(ruta_json, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    return datos


# Ejecutar solo si se llama directamente
if __name__ == "__main__":
    datos = cargar_datos_procesados()

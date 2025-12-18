import json
import os
import glob


def modificar_json(carpeta):
    """
    Modifica todos los archivos JSON en la carpeta especificada.
    Cambia:
    1. producto_id "P008" (pollo) por el que ya tiene
    2. nombre "Pollo" por "Pechuga de pollo"
    3. unidad por "2kg"
    """
    # Buscar todos los archivos JSON en la carpeta
    patron = os.path.join(carpeta, "*.json")
    archivos_json = glob.glob(patron)


    for archivo in archivos_json:
        try:
            # Leer el archivo JSON
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)

            # Modificar la sección de productos
            if "productos" in datos:
                productos_modificados = False

                for producto in datos["productos"]:
                    # Buscar el producto "P008" (Pollo)
                    if producto.get("producto_id") == "P009":
                        # Modificar los campos según los requerimientos
                        producto["nombre"] = "Leche Condensada"
                        productos_modificados = True
                        print(f"✓ Modificado en {os.path.basename(archivo)}: {producto['producto_id']}")
                        break  # Solo hay un producto P008 por archivo

                # Guardar los cambios si se modificó algo
                if productos_modificados:
                    # Guardar el archivo modificado
                    with open(archivo, 'w', encoding='utf-8') as f:
                        json.dump(datos, f, indent=2, ensure_ascii=False)
                else:
                    print(f"✗ No se encontró producto P008 en {os.path.basename(archivo)}")

        except json.JSONDecodeError as e:
            print(f"Error al leer {archivo}: {e}")
        except Exception as e:
            print(f"Error al procesar {archivo}: {e}")


# === AÑADE ESTA PARTE PARA QUE SE EJECUTE ===
if __name__ == "__main__":
    print("=" * 50)
    print("MODIFICADOR DE ARCHIVOS JSON")
    print("=" * 50)

    # Preguntar al usuario
    print("\nOpciones de carpeta:")
    print("1. Usar carpeta actual (donde está este script)")
    print("2. Especificar otra carpeta")

    opcion = input("\nSelecciona (1 o 2): ").strip()

    if opcion == "1":
        carpeta = "./"
    else:
        carpeta = input("Introduce la ruta completa de la carpeta: ").strip()
        # Limpiar comillas si las puso
        carpeta = carpeta.strip('"').strip("'")

    print(f"\n📁 Buscando JSON en: {os.path.abspath(carpeta)}")

    # Ejecutar la función
    modificar_json(carpeta)

    print("\n✅ Proceso completado.")
    input("Presiona Enter para salir...")
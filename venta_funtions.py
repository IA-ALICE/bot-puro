from DB import *

def obtener_nombres_de_categoria():
    """
    Obtiene todos los nombres de la columna 'nombre' de la tabla 'categoria'
    de la base de datos y los devuelve en una lista.
    """
    connection = None
    nombres_categoria = []
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT Nombre FROM Categoria")
        rows = cursor.fetchall()
        for row in rows:
            nombres_categoria.append(row[0])
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Error al conectar o consultar la base de datos: {sqlstate}")
    finally:
        if connection:
            connection.close()
    return nombres_categoria

def imprimir_nombres_de_categoria():
    """
    Obtiene todos los nombres de la columna 'nombre' de la tabla 'categoria'
    de la base de datos y los imprime en la consola como una lista enumerada.
    """
    nombres = obtener_nombres_de_categoria()
    if nombres:
        for indice, nombre in enumerate(nombres):
            print(f"{indice + 1}.- {nombre}")
        print("0.- Volver al menu anterior")
    else:
        print("No se encontraron categorías.")

def mostrar_contenido_categoria(numero_categoria):
    """
    Obtiene el contenido (PDF y PDF_PROMOCION) de una categoría específica
    basándose en el número ingresado por el usuario.
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Obtener el nombre de la categoría basado en el número ingresado
        nombres_categoria = obtener_nombres_de_categoria()
        if 1 <= numero_categoria <= len(nombres_categoria):
            nombre_categoria = nombres_categoria[numero_categoria - 1]
            cursor.execute("SELECT PDF, PDF_PROMOCION FROM Categoria WHERE Nombre = ?", (nombre_categoria,))
            resultado = cursor.fetchone()
            if resultado:
                pdf_link = resultado[0]
                pdf_promo_link = resultado[1]
                print("---------------------------------------------------------------------------")
                print(f"Contenido de la categoría '{nombre_categoria}':")
                print(f"  PDF: {pdf_link if pdf_link else 'No disponible'}")
                print(f"  PDF Promoción: {pdf_promo_link if pdf_promo_link else 'No disponible'}")
            else:
                print(f"No se encontró información para la categoría '{nombre_categoria}'.")
        elif numero_categoria != 0:
            print("Número de categoría inválido.")

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"Error al conectar o consultar la base de datos: {sqlstate}")
    finally:
        if connection:
            connection.close()
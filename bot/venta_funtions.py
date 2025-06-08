import pyodbc
from bot.DB import get_db_connection # Importar desde bot.DB

def obtener_nombres_de_categoria():
    """
    Obtiene los IDs y nombres de las categorías de la tabla 'Categoria'.
    Devuelve una lista de diccionarios {'id': ..., 'nombre': ...}.
    """
    conn = None
    categorias = []
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Usamos 'CategoriaID' como el ID y 'Nombre' como el nombre
        cursor.execute("SELECT CategoriaID, Nombre FROM dbo.Categoria ORDER BY CategoriaID") # <--- CORREGIDO AQUÍ
        rows = cursor.fetchall()
        for row in rows:
            categorias.append({"id": row[0], "nombre": row[1]})
        return categorias
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"ERROR (obtener_nombres_de_categoria): {sqlstate} - {ex}")
        return []
    finally:
        if conn:
            conn.close()

def obtener_contenido_promociones(categoria_id):
    """
    Obtiene el PDF de promoción para una categoría específica por su ID.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Usamos 'CategoriaID' para el WHERE y 'PDF_PROMOCION', 'Nombre' para los resultados
        query = "SELECT Nombre, PDF_PROMOCION FROM dbo.Categoria WHERE CategoriaID = ?" # <--- CORREGIDO AQUÍ
        cursor.execute(query, categoria_id)
        resultado = cursor.fetchone()
        if resultado:
            return {"success": True, "pdf_promo_link": resultado[1], "nombre_categoria": resultado[0]}
        else:
            return {"success": False, "message": "No se encontró promoción para la categoría seleccionada."}
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"ERROR (obtener_contenido_promociones): {sqlstate} - {ex}")
        return {"success": False, "message": "Error al buscar la promoción."}
    finally:
        if conn:
            conn.close()

def obtener_contenido_categoria(categoria_id):
    """
    Obtiene el PDF de catálogo para una categoría específica por su ID.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Usamos 'CategoriaID' para el WHERE y 'PDF', 'Nombre' para los resultados
        query = "SELECT Nombre, PDF FROM dbo.Categoria WHERE CategoriaID = ?" # <--- CORREGIDO AQUÍ
        cursor.execute(query, categoria_id)
        resultado = cursor.fetchone()
        if resultado:
            return {"success": True, "pdf_link": resultado[1], "nombre_categoria": resultado[0]}
        else:
            return {"success": False, "message": "No se encontró categoría o PDF para la categoría seleccionada."}
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"ERROR (obtener_contenido_categoria): {sqlstate} - {ex}")
        return {"success": False, "message": "Error al buscar la categoría."}
    finally:
        if conn:
            conn.close()
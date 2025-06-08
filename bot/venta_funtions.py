from bot.DB import get_db_connection # Importar desde bot.DB
import psycopg2 # Importar psycopg2 para manejar sus errores específicos

def obtener_nombres_de_categoria():
    """
    Obtiene los IDs y nombres de las categorías de la tabla 'categoria'.
    Devuelve una lista de diccionarios {'id': ..., 'nombre': ...}.
    """
    conn = None
    categorias = []
    try:
        conn = get_db_connection()
        if conn is None:
            print("ERROR (obtener_nombres_de_categoria): Fallo en la conexión a la base de datos.")
            return []
        cursor = conn.cursor()
        
        # CORREGIDO: Eliminar comillas dobles y usar nombres de columna en minúsculas
        cursor.execute("SELECT categoriaid, nombre FROM public.categoria ORDER BY categoriaid") 
        
        rows = cursor.fetchall()
        for row in rows:
            categorias.append({"id": row[0], "nombre": row[1]})
        print(f"DEBUG (obtener_nombres_de_categoria): Categorías obtenidas: {categorias}")
        return categorias
    except psycopg2.Error as ex:
        print(f"ERROR (obtener_nombres_de_categoria - psycopg2): {ex.pgcode if hasattr(ex, 'pgcode') else 'N/A'} - {ex.pgerror if hasattr(ex, 'pgerror') else ex}")
        return []
    except Exception as e:
        print(f"ERROR (obtener_nombres_de_categoria - general): {e}")
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
        if conn is None:
            print("ERROR (obtener_contenido_promociones): Fallo en la conexión a la base de datos.")
            return {"success": False, "message": "Fallo en la conexión a la base de datos."}
        cursor = conn.cursor()
        
        # CORREGIDO: Eliminar comillas dobles y usar nombres de columna en minúsculas
        query = "SELECT nombre, pdf_promocion FROM public.categoria WHERE categoriaid = %s" 
        cursor.execute(query, (categoria_id,))
        
        resultado = cursor.fetchone()
        if resultado:
            return {"success": True, "pdf_promo_link": resultado[1], "nombre_categoria": resultado[0]}
        else:
            print(f"DEBUG (obtener_contenido_promociones): No se encontró promoción para CategoriaID {categoria_id}.")
            return {"success": False, "message": "No se encontró promoción para la categoría seleccionada."}
    except psycopg2.Error as ex:
        print(f"ERROR (obtener_contenido_promociones - psycopg2): {ex.pgcode if hasattr(ex, 'pgcode') else 'N/A'} - {ex.pgerror if hasattr(ex, 'pgerror') else ex}")
        return {"success": False, "message": "Error al buscar la promoción."}
    except Exception as e:
        print(f"ERROR (obtener_contenido_promociones - general): {e}")
        return {"success": False, "message": "Error inesperado al buscar la promoción."}
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
        if conn is None:
            print("ERROR (obtener_contenido_categoria): Fallo en la conexión a la base de datos.")
            return {"success": False, "message": "Fallo en la conexión a la base de datos."}
        cursor = conn.cursor()
        
        # CORREGIDO: Eliminar comillas dobles y usar nombres de columna en minúsculas
        query = "SELECT nombre, pdf FROM public.categoria WHERE categoriaid = %s" 
        cursor.execute(query, (categoria_id,))
        
        resultado = cursor.fetchone()
        if resultado:
            return {"success": True, "pdf_link": resultado[1], "nombre_categoria": resultado[0]}
        else:
            print(f"DEBUG (obtener_contenido_categoria): No se encontró catálogo para CategoriaID {categoria_id}.")
            return {"success": False, "message": "No se encontró categoría o PDF para la categoría seleccionada."}
    except psycopg2.Error as ex:
        print(f"ERROR (obtener_contenido_categoria - psycopg2): {ex.pgcode if hasattr(ex, 'pgcode') else 'N/A'} - {ex.pgerror if hasattr(ex, 'pgerror') else ex}")
        return {"success": False, "message": "Error al buscar la categoría."}
    except Exception as e:
        print(f"ERROR (obtener_contenido_categoria - general): {e}")
        return {"success": False, "message": "Error inesperado al buscar la categoría."}
    finally:
        if conn:
            conn.close()
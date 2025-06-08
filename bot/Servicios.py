# bot/Servicios.py
from .DB import get_db_connection
import psycopg2 # Import psycopg2 to handle its specific errors

def obtener_servicios_principales():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            print("ERROR (obtener_servicios_principales): Fallo en la conexión a la base de datos.")
            return []
        cursor = conn.cursor()
        
        # PostgreSQL placeholder is %s, and schema/table/column names often need double quotes
        cursor.execute('SELECT "id", "Servicios" FROM "dbo"."Servicios"') # Use double quotes for schema/table/column names
        
        servicios = []
        for row in cursor.fetchall():
            # psycopg2 by default returns tuples, so access by index
            servicios.append({"id": row[0], "nombre": row[1]})
        print(f"DEBUG (obtener_servicios_principales): Servicios principales obtenidos: {servicios}")
        return servicios
    except psycopg2.Error as e: # Catch psycopg2 specific errors
        print(f"ERROR (obtener_servicios_principales - psycopg2): {e.pgcode if hasattr(e, 'pgcode') else 'N/A'} - {e.pgerror if hasattr(e, 'pgerror') else e}")
        return []
    except Exception as e:
        print(f"ERROR (obtener_servicios_principales - general): {e}")
        return []
    finally:
        if conn:
            conn.close()

def obtener_catalogo_por_servicio(servicio_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            print("ERROR (obtener_catalogo_por_servicio): Fallo en la conexión a la base de datos.")
            return []
        cursor = conn.cursor()
        
        # PostgreSQL placeholder is %s, and schema/table/column names often need double quotes
        cursor.execute(
            'SELECT cs."id", cs."catalogo", cs."precio" ' # Use double quotes
            'FROM "dbo"."Servicios" s '
            'JOIN "dbo"."Servicio_catalogo" sc ON s."id" = sc."id_servicio" ' # Use double quotes
            'JOIN "dbo"."catalogo_servicio" cs ON sc."id_catalogo" = cs."id" ' # Use double quotes
            'WHERE s."id" = %s', # Changed ? to %s
            (servicio_id,)
        )
        catalogo = []
        for row in cursor.fetchall():
            # Asegúrate de que el precio se convierta correctamente si es un tipo numérico en la DB
            catalogo.append({"id": row[0], "nombre_apartado": row[1], "precio": float(row[2]) if row[2] is not None else None})
        print(f"DEBUG (obtener_catalogo_por_servicio): Catálogo para servicio_id {servicio_id}: {catalogo}")
        return catalogo
    except psycopg2.Error as e: # Catch psycopg2 specific errors
        print(f"ERROR (obtener_catalogo_por_servicio - psycopg2): {e.pgcode if hasattr(e, 'pgcode') else 'N/A'} - {e.pgerror if hasattr(e, 'pgerror') else e}")
        return []
    except Exception as e:
        print(f"ERROR (obtener_catalogo_por_servicio - general): {e}")
        return []
    finally:
        if conn:
            conn.close()

def obtener_preguntas_por_catalogo(catalogo_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            print("ERROR (obtener_preguntas_por_catalogo): Fallo en la conexión a la base de datos.")
            return []
        cursor = conn.cursor()
        
        # PostgreSQL placeholder is %s, and schema/table/column names often need double quotes
        cursor.execute(
            'SELECT "id_pregunta_servios", "pregunta" FROM "dbo"."pregunta_servicio" WHERE "id_catalogo_servicio" = %s', # Changed ? to %s
            (catalogo_id,)
        )
        preguntas = []
        for row in cursor.fetchall():
            preguntas.append({"id": row[0], "texto": row[1]})
        print(f"DEBUG (obtener_preguntas_por_catalogo): Preguntas para catalogo_id {catalogo_id}: {preguntas}")
        return preguntas
    except psycopg2.Error as e: # Catch psycopg2 specific errors
        print(f"ERROR (obtener_preguntas_por_catalogo - psycopg2): {e.pgcode if hasattr(e, 'pgcode') else 'N/A'} - {e.pgerror if hasattr(e, 'pgerror') else e}")
        return []
    except Exception as e:
        print(f"ERROR (obtener_preguntas_por_catalogo - general): {e}")
        return []
    finally:
        if conn:
            conn.close()

def obtener_respuestas_de_la_pregunta(pregunta_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            print("ERROR (obtener_respuestas_de_la_pregunta): Fallo en la conexión a la base de datos.")
            return []
        cursor = conn.cursor()
        
        # PostgreSQL placeholder is %s, and schema/table/column names often need double quotes
        cursor.execute(
            'SELECT "respuestas" FROM "dbo"."respuesta_servicios" WHERE "id_pregunta_servios" = %s', # Changed ? to %s
            (pregunta_id,)
        )
        respuestas = []
        for row in cursor.fetchall():
            respuestas.append(row[0])
        print(f"DEBUG (obtener_respuestas_de_la_pregunta): Respuestas para pregunta_id {pregunta_id}: {respuestas}")
        return respuestas
    except psycopg2.Error as e: # Catch psycopg2 specific errors
        print(f"ERROR (obtener_respuestas_de_la_pregunta - psycopg2): {e.pgcode if hasattr(e, 'pgcode') else 'N/A'} - {e.pgerror if hasattr(e, 'pgerror') else e}")
        return []
    except Exception as e:
        print(f"ERROR (obtener_respuestas_de_la_pregunta - general): {e}")
        return []
    finally:
        if conn:
            conn.close()
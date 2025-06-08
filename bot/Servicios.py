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
        
        # CORREGIDO: Nombres de columna en minúsculas y sin comillas dobles
        # Asumiendo 'Servicios' se convirtió a 'servicios' y 'id' a 'id'.
        # Si 'Servicios' es el nombre de la columna que contiene el texto del servicio,
        # su nombre en minúsculas debería ser 'servicios' o 'nombre_servicio', etc.
        # Aquí asumo 'servicios' por ser coherente con el nombre de la tabla.
        cursor.execute('SELECT id, servicios FROM public.servicios') 
        
        servicios = []
        for row in cursor.fetchall():
            servicios.append({"id": row[0], "nombre": row[1]})
        print(f"DEBUG (obtener_servicios_principales): Servicios principales obtenidos: {servicios}")
        return servicios
    except psycopg2.Error as e:
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
        
        # CORREGIDO: Nombres de tablas y columnas en minúsculas y sin comillas dobles
        cursor.execute(
            'SELECT cs.id, cs.catalogo, cs.precio '
            'FROM public.servicios s ' # CORREGIDO: tabla servicios en minúsculas
            'JOIN public.servicio_catalogo sc ON s.id = sc.id_servicio ' # CORREGIDO: tabla servicio_catalogo y columnas id, id_servicio
            'JOIN public.catalogo_servicio cs ON sc.id_catalogo = cs.id ' # CORREGIDO: tabla catalogo_servicio y columnas id_catalogo, id
            'WHERE s.id = %s', # Columna 'id'
            (servicio_id,)
        )
        catalogo = []
        for row in cursor.fetchall():
            catalogo.append({"id": row[0], "nombre_apartado": row[1], "precio": float(row[2]) if row[2] is not None else None})
        print(f"DEBUG (obtener_catalogo_por_servicio): Catálogo para servicio_id {servicio_id}: {catalogo}")
        return catalogo
    except psycopg2.Error as e:
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
        
        # CORREGIDO: Nombres de columnas en minúsculas y sin comillas dobles
        cursor.execute(
            'SELECT id_pregunta_servios, pregunta FROM public.pregunta_servicio WHERE id_catalogo_servicio = %s',
            (catalogo_id,)
        )
        preguntas = []
        for row in cursor.fetchall():
            preguntas.append({"id": row[0], "texto": row[1]})
        print(f"DEBUG (obtener_preguntas_por_catalogo): Preguntas para catalogo_id {catalogo_id}: {preguntas}")
        return preguntas
    except psycopg2.Error as e:
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
        
        # CORREGIDO: Nombres de columnas en minúsculas y sin comillas dobles
        cursor.execute(
            'SELECT respuestas FROM public.respuesta_servicios WHERE id_pregunta_servios = %s',
            (pregunta_id,)
        )
        respuestas = []
        for row in cursor.fetchall():
            respuestas.append(row[0])
        print(f"DEBUG (obtener_respuestas_de_la_pregunta): Respuestas para pregunta_id {pregunta_id}: {respuestas}")
        return respuestas
    except psycopg2.Error as e:
        print(f"ERROR (obtener_respuestas_de_la_pregunta - psycopg2): {e.pgcode if hasattr(e, 'pgcode') else 'N/A'} - {e.pgerror if hasattr(e, 'pgerror') else e}")
        return []
    except Exception as e:
        print(f"ERROR (obtener_respuestas_de_la_pregunta - general): {e}")
        return []
    finally:
        if conn:
            conn.close()
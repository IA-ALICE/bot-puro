# bot/Servicios.py

from .DB import get_db_connection

def obtener_servicios_principales():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        # CORREGIDO: Usar 'Servicios' (nombre de columna en tu tabla) y 'dbo.Servicios' (nombre de tabla)
        cursor.execute('SELECT id, Servicios FROM dbo.Servicios') #
        servicios = []
        for row in cursor.fetchall():
            servicios.append({"id": row[0], "nombre": row[1]})
        print(f"DEBUG (obtener_servicios_principales): Servicios principales obtenidos: {servicios}")
        return servicios
    except Exception as e:
        print(f"ERROR (obtener_servicios_principales): {e}")
        return []
    finally:
        if conn:
            conn.close()

def obtener_catalogo_por_servicio(servicio_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        # CORREGIDO: Usar las uniones correctas con Servicio_catalogo y la columna 'catalogo'
        cursor.execute(
            'SELECT cs.id, cs.catalogo, cs.precio ' #
            'FROM dbo.Servicios s '
            'JOIN dbo.Servicio_catalogo sc ON s.id = sc.id_servicio ' #
            'JOIN dbo.catalogo_servicio cs ON sc.id_catalogo = cs.id ' #
            'WHERE s.id = ?',
            (servicio_id,)
        )
        catalogo = []
        for row in cursor.fetchall():
            # Asegúrate de que el precio se convierta correctamente si es un tipo numérico en la DB
            catalogo.append({"id": row[0], "nombre_apartado": row[1], "precio": float(row[2]) if row[2] is not None else None})
        print(f"DEBUG (obtener_catalogo_por_servicio): Catálogo para servicio_id {servicio_id}: {catalogo}")
        return catalogo
    except Exception as e:
        print(f"ERROR (obtener_catalogo_por_servicio): {e}")
        return []
    finally:
        if conn:
            conn.close()

def obtener_preguntas_por_catalogo(catalogo_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        # CORREGIDO: Nombres de columnas y FK según tu esquema
        cursor.execute(
            'SELECT id_pregunta_servios, pregunta FROM dbo.pregunta_servicio WHERE id_catalogo_servicio = ?', #
            (catalogo_id,)
        )
        preguntas = []
        for row in cursor.fetchall():
            preguntas.append({"id": row[0], "texto": row[1]})
        print(f"DEBUG (obtener_preguntas_por_catalogo): Preguntas para catalogo_id {catalogo_id}: {preguntas}")
        return preguntas
    except Exception as e:
        print(f"ERROR (obtener_preguntas_por_catalogo): {e}")
        return []
    finally:
        if conn:
            conn.close()

def obtener_respuestas_de_la_pregunta(pregunta_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return []
        cursor = conn.cursor()
        # CORREGIDO: Nombres de columnas y FK según tu esquema
        cursor.execute(
            'SELECT respuestas FROM dbo.respuesta_servicios WHERE id_pregunta_servios = ?', #
            (pregunta_id,)
        )
        respuestas = []
        for row in cursor.fetchall():
            respuestas.append(row[0])
        print(f"DEBUG (obtener_respuestas_de_la_pregunta): Respuestas para pregunta_id {pregunta_id}: {respuestas}")
        return respuestas
    except Exception as e:
        print(f"ERROR (obtener_respuestas_de_la_pregunta): {e}")
        return []
    finally:
        if conn:
            conn.close()
import psycopg2
from psycopg2 import OperationalError
import os # Keep this import if you plan to use environment variables later

def get_db_connection():
    """Establece y retorna una conexión a la base de datos PostgreSQL (Supabase) con valores directos."""
    try:
        # Asegúrate de que estos valores son EXACTAMENTE los de tu Supabase
        # y que 'Minecraftbedrock45$' es tu contraseña real.
        connection = psycopg2.connect(
            host='db.yssrtcfsydyzjjnpidri.supabase.co',
            database='postgres',
            user='postgres',
            password='Minecraftbedrock45$',
            port='5432'
        )
        print("Conexión a la base de datos Supabase exitosa.")
        return connection
    except OperationalError as e:
        print(f"CRÍTICO: Error de operación al conectar a la base de datos: {e}")
        # El error "Host desconocido" proviene de aquí si el nombre del host no se puede resolver.
        # Otros errores de OperationalError incluyen Connection refused, password authentication failed, etc.
        print("Esto podría ser debido a credenciales incorrectas, el host no es accesible, o un firewall bloqueando la conexión.")
        return None
    except Exception as e:
        print(f"CRÍTICO: Un error inesperado ocurrió al intentar conectar a la base de datos: {e}")
        return None

# Puedes mantener este bloque para probar solo la conexión a la DB si ejecutas DB.py directamente
if __name__ == '__main__':
    print("Intentando conectar a la base de datos Supabase con valores directos...")
    conn = get_db_connection()
    if conn:
        print("Prueba de conexión local: Establecida y cerrada correctamente.")
        conn.close()
    else:
        print("Prueba de conexión local: Fallo al establecer la conexión. Revisa tus credenciales y la accesibilidad desde tu red.")
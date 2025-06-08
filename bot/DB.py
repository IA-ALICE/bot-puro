import psycopg2
from psycopg2 import OperationalError
import os

def get_db_connection():
    """Establece y retorna una conexión a la base de datos PostgreSQL (Supabase) usando PGBouncer con valores directos."""
    try:
        # ¡IMPORTANTE! Asegúrate de que 'Minecraftbedrock45$' es tu contraseña REAL.
        # Usa el nombre de usuario completo que incluye la referencia del proyecto.
        connection = psycopg2.connect(
            host='DB_HOST',  # Host del Pooler de Supabase
            database='DB_NAME',                         # Nombre de la base de datos
            user='DB_USER',       # ¡Nombre de usuario completo con referencia de proyecto!
            password='DB_PASSWORD',              # Tu contraseña real de Supabase
            port='DB_PORT'                                  # Puerto del Pooler (usualmente 5432 para este pooler)
        )
        print("Conexión a la base de datos Supabase exitosa (via Pooler).")
        return connection
    except OperationalError as e:
        print(f"CRÍTICO: Error de operación al conectar a la base de datos: {e}")
        print("Causas posibles: credenciales incorrectas (usuario/contraseña), el host no es accesible, o un firewall bloqueando la conexión.")
        print("Revisa el nombre de usuario completo ('postgres.yssrtcfsydyzjjnpidri'), la contraseña, y la configuración de 'Allowed IPs' en Supabase.")
        return None
    except Exception as e:
        print(f"CRÍTICO: Un error inesperado ocurrió al intentar conectar a la base de datos: {e}")
        return None

# Ejemplo de prueba (ejecuta este archivo directamente para probar la conexión)
if __name__ == '__main__':
    print("Intentando conectar a la base de datos Supabase con Pooler (valores directos)...")
    conn = get_db_connection()
    if conn:
        print("Prueba de conexión local con Pooler: Establecida y cerrada correctamente.")
        conn.close()
    else:
        print("Prueba de conexión local con Pooler: Fallo al establecer la conexión.")
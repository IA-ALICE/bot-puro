import os
import psycopg2
from psycopg2 import OperationalError

def get_db_connection():
    """Establece y retorna una conexión a la base de datos PostgreSQL (Supabase)."""
    try:
        connection = psycopg2.connect(
            host=os.environ.get('DB_HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            port=os.environ.get('DB_PORT', '5432') # 5432 es el puerto por defecto de PostgreSQL
        )
        print("Conexión a la base de datos Supabase exitosa.")
        return connection
    except OperationalError as e:
        print(f"CRÍTICO: Error de operación al conectar a la base de datos: {e}")
        print("Asegúrate de que las variables de entorno para la base de datos estén configuradas correctamente.")
        return None
    except Exception as e:
        print(f"CRÍTICO: Un error inesperado ocurrió al intentar conectar a la base de datos: {e}")
        return None

# Ejemplo de prueba (opcional, puedes ejecutar python DB.py para probar la conexión)
if __name__ == '__main__':
    # Para probar localmente, puedes configurar las variables de entorno aquí
    # o mejor aún, usar un archivo .env y la librería python-dotenv
    # (¡Pero NO subas .env a tu repositorio Git!)
    # import dotenv
    # dotenv.load_dotenv()

    print("Intentando conectar a la base de datos Supabase...")
    conn = get_db_connection()
    if conn:
        print("Prueba de conexión: Establecida y cerrada correctamente.")
        conn.close()
    else:
        print("Prueba de conexión: Fallo al establecer la conexión.")
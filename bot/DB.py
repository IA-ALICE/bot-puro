import pyodbc

def get_db_connection():
    """Establece y retorna una conexión a la base de datos SQL Server."""
    try:
        connection = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};' # Asegúrate de tener este driver instalado
            'SERVER=DESKTOP-LRGLGH6;'
            'DATABASE=Bd_jyp;'
            'Trusted_Connection=yes;'
        )
        # print("Conexión a la base de datos exitosa.") # Descomentar para depuración
        return connection
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"CRÍTICO: Error al conectar a la base de datos: {sqlstate} - {ex}")
        if sqlstate == '28000':
            print("Detalle: Error de autenticación. Verifique credenciales o configuración de Trusted_Connection.")
        elif sqlstate == '08001':
            print("Detalle: Error de red o instancia. No se pudo establecer conexión con el servidor SQL.")
        elif sqlstate == '42000': # Puede ser "Cannot open database..."
            print(f"Detalle: Error de SQL. Verifique el nombre de la base de datos ('Bd_jyp') o la sintaxis. Mensaje original: {ex}")
        return None
    except Exception as e:
        print(f"CRÍTICO: Un error inesperado ocurrió al intentar conectar a la base de datos: {e}")
        return None

# Ejemplo de prueba (opcional, puedes ejecutar python DB.py para probar la conexión)
# if __name__ == '__main__':
#     print("Intentando conectar a la base de datos...")
#     conn = get_db_connection()
#     if conn:
#         print("Prueba de conexión: Establecida y cerrada correctamente.")
#         conn.close()
#     else:
#         print("Prueba de conexión: Fallo al establecer la conexión.")
from bot.DB import get_db_connection
import psycopg2 # Import psycopg2 to handle its specific errors

def verificar_credenciales(email_o_ruc):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return False, "Fallo en la conexión a la base de datos."
        cursor = conn.cursor()

        # Intenta buscar por Email
        # En psycopg2, el placeholder es %s, no ?
        cursor.execute("SELECT \"ClienteID\", \"Nombre\", \"Email\", \"RUC\" FROM \"dbo\".\"Cliente\" WHERE \"Email\" = %s", (email_o_ruc,))
        cliente = cursor.fetchone()
        if cliente:
            # psycopg2.Row objects (returned by fetchone by default) can be accessed like tuples
            # Adjust indexing based on the order of columns in your SELECT statement
            # Assuming cliente is a tuple: (ClienteID, Nombre, Email, RUC)
            print(f"DEBUG (verificar_credenciales): Cliente encontrado por Email: {cliente[1]}") # cliente[1] is Nombre
            return True, f"Inicio de sesión exitoso como {cliente[1]}."

        # Si no se encuentra por Email, intenta buscar por RUC
        cursor.execute("SELECT \"ClienteID\", \"Nombre\", \"Email\", \"RUC\" FROM \"dbo\".\"Cliente\" WHERE \"RUC\" = %s", (email_o_ruc,))
        cliente = cursor.fetchone()
        if cliente:
            print(f"DEBUG (verificar_credenciales): Cliente encontrado por RUC: {cliente[1]}") # cliente[1] is Nombre
            return True, f"Inicio de sesión exitoso como {cliente[1]}."
        else:
            print("DEBUG (verificar_credenciales): Credenciales incorrectas o no encontradas.")
            return False, "Email o RUC incorrectos o no registrados."

    except psycopg2.Error as ex: # Changed from pyodbc.Error
        # psycopg2.Error objects have attributes like .pgcode and .pgerror
        # ex.pgcode gives the SQLSTATE, ex.pgerror gives the message
        print(f"ERROR (verificar_credenciales): {ex.pgcode if hasattr(ex, 'pgcode') else 'N/A'} - {ex.pgerror if hasattr(ex, 'pgerror') else ex}")
        return False, f"Error al verificar credenciales: {ex}"
    except Exception as e:
        print(f"ERROR (verificar_credenciales - general): {e}")
        return False, f"Error inesperado al verificar credenciales: {e}"
    finally:
        if conn:
            conn.close()
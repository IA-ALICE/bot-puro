from bot.DB import get_db_connection

def verificar_credenciales(email_o_ruc):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return False, "Fallo en la conexión a la base de datos."
        cursor = conn.cursor()

        # Intenta buscar por Email
        cursor.execute("SELECT ClienteID, Nombre, Email, RUC FROM dbo.Cliente WHERE Email = ?", (email_o_ruc,))
        cliente = cursor.fetchone()
        if cliente:
            print(f"DEBUG (verificar_credenciales): Cliente encontrado por Email: {cliente.Nombre}")
            return True, f"Inicio de sesión exitoso como {cliente.Nombre}."

        # Si no se encuentra por Email, intenta buscar por RUC
        cursor.execute("SELECT ClienteID, Nombre, Email, RUC FROM dbo.Cliente WHERE RUC = ?", (email_o_ruc,))
        cliente = cursor.fetchone()
        if cliente:
            print(f"DEBUG (verificar_credenciales): Cliente encontrado por RUC: {cliente.Nombre}")
            return True, f"Inicio de sesión exitoso como {cliente.Nombre}."
        else:
            print("DEBUG (verificar_credenciales): Credenciales incorrectas o no encontradas.")
            return False, "Email o RUC incorrectos o no registrados."

    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        print(f"ERROR (verificar_credenciales): {sqlstate} - {ex}")
        return False, f"Error al verificar credenciales: {ex}"
    except Exception as e:
        print(f"ERROR (verificar_credenciales - general): {e}")
        return False, f"Error inesperado al verificar credenciales: {e}"
    finally:
        if conn:
            conn.close()
from bot.DB import get_db_connection
import psycopg2

def verificar_credenciales(email_o_ruc):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return False, "Fallo en la conexión a la base de datos."
        cursor = conn.cursor()

        # Intenta buscar por Email
        # CORREGIDO: Nombres de columnas a minúsculas y sin comillas dobles
        cursor.execute("SELECT clienteid, nombre, email, ruc FROM public.cliente WHERE email = %s", (email_o_ruc,))
        cliente = cursor.fetchone()
        if cliente:
            print(f"DEBUG (verificar_credenciales): Cliente encontrado por Email: {cliente[1]}")
            return True, f"Inicio de sesión exitoso como {cliente[1]}."

        # Si no se encuentra por Email, intenta buscar por RUC
        # CORREGIDO: Nombres de columnas a minúsculas y sin comillas dobles
        cursor.execute("SELECT clienteid, nombre, email, ruc FROM public.cliente WHERE ruc = %s", (email_o_ruc,))
        cliente = cursor.fetchone()
        if cliente:
            print(f"DEBUG (verificar_credenciales): Cliente encontrado por RUC: {cliente[1]}")
            return True, f"Inicio de sesión exitoso como {cliente[1]}."
        else:
            print("DEBUG (verificar_credenciales): Credenciales incorrectas o no encontradas.")
            return False, "Email o RUC incorrectos o no registrados."

    except psycopg2.Error as ex:
        print(f"ERROR (verificar_credenciales): {ex.pgcode if hasattr(ex, 'pgcode') else 'N/A'} - {ex.pgerror if hasattr(ex, 'pgerror') else ex}")
        return False, f"Error al verificar credenciales: {ex}"
    except Exception as e:
        print(f"ERROR (verificar_credenciales - general): {e}")
        return False, f"Error inesperado al verificar credenciales: {e}"
    finally:
        if conn:
            conn.close()
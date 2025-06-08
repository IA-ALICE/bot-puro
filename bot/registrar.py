import pyodbc
import re # Importar el módulo de expresiones regulares
from bot.DB import get_db_connection

def es_email_valido(email):
    """
    Valida si una cadena de texto tiene el formato de un email.
    """
    if not email:
        return True # Si el email es None o vacío, y no es obligatorio, se considera válido en este contexto
                    # La obligatoriedad de (email O ruc) se maneja en app.py

    email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    return bool(email_regex.match(email))

def es_telefono_valido(telefono):
    """
    Valida si una cadena de texto es un número de teléfono válido (9 dígitos numéricos).
    """
    if not telefono:
        return False # El teléfono es obligatorio y si llega aquí como None/vacío, es inválido.
                     # Nota: la validación de obligatorio ya se hace en app.py, pero es un buen fallback.

    # Regex para 9 dígitos numéricos
    telefono_regex = re.compile(r"^\d{9}$")
    return bool(telefono_regex.match(telefono))

def es_ruc_valido(ruc):
    """
    Valida si una cadena de texto es un RUC válido (11 dígitos numéricos).
    """
    if not ruc:
        return True # Si el RUC es None o vacío, y no es obligatorio (si email existe), se considera válido.
                    # La validación de que Email O RUC deben existir se hace en app.py.

    # Regex para 11 dígitos numéricos
    ruc_regex = re.compile(r"^\d{11}$")
    return bool(ruc_regex.match(ruc))


def registrar_nuevo_cliente(nombre, email=None, telefono=None, ruc=None):
    """
    Registra un nuevo cliente en la base de datos.
    Retorna (True, mensaje_exito, identificador) si es exitoso,
    o (False, mensaje_error, None) si falla.
    """
    conn = None
    try:
        # --- Obtener conexión a la DB ---
        conn = get_db_connection()
        if conn is None:
            return False, "Fallo en la conexión a la base de datos al intentar registrar. Por favor, intente de nuevo más tarde.", None
        cursor = conn.cursor()

        # --- Validaciones de formato y lógica de negocio ---
        if email and not es_email_valido(email):
            return False, "El formato del Email no es válido. Por favor, asegúrate de que sea como 'ejemplo@dominio.com'.", None

        # El teléfono es obligatorio (su existencia se valida en app.py), aquí validamos el formato/longitud
        if not es_telefono_valido(telefono):
            return False, "El número de teléfono debe contener exactamente 9 dígitos numéricos.", None

        if ruc and not es_ruc_valido(ruc): # Solo validar si se proporcionó un RUC
            return False, "El número de RUC debe contener exactamente 11 dígitos numéricos.", None

        # Verificar si el Email ya existe (si se proporcionó)
        if email:
            cursor.execute("SELECT ClienteID FROM dbo.Cliente WHERE Email = ?", (email,))
            if cursor.fetchone():
                print(f"DEBUG (registrar_nuevo_cliente): Email '{email}' ya existe.")
                return False, "El Email ya está en uso. Por favor, intente con otro o inicie sesión.", None

        # Verificar si el RUC ya existe (si se proporcionó)
        if ruc:
            cursor.execute("SELECT ClienteID FROM dbo.Cliente WHERE RUC = ?", (ruc,))
            if cursor.fetchone():
                print(f"DEBUG (registrar_nuevo_cliente): RUC '{ruc}' ya existe.")
                return False, "El RUC ya está en uso. Por favor, intente con otro o inicie sesión.", None
        
        # --- Fin de Validaciones ---

        # Si no existe, inserta el nuevo cliente
        cursor.execute(
            'INSERT INTO dbo.Cliente (Nombre, Email, Telefono, RUC) VALUES (?, ?, ?, ?)',
            (nombre, email, telefono, ruc)
        )
        conn.commit()
        print(f"DEBUG (registrar_nuevo_cliente): Cliente '{nombre}' registrado exitosamente.")
        
        registered_identifier = email if email else ruc # Usar email o ruc como identificador principal
        return True, f"¡Registro exitoso! Te damos la bienvenida {nombre}.", registered_identifier

    except pyodbc.IntegrityError as e:
        sqlstate = e.args[0]
        print(f"ERROR (registrar_nuevo_cliente - pyodbc IntegrityError): {sqlstate} - {e}")
        if conn:
            conn.rollback() # Si hay un error de DB, revertir la transacción
        
        # Este error es para violaciones de unicidad (duplicados de Email o RUC)
        error_msg = str(e)
        if "UNIQUE" in error_msg.upper() or "PRIMARY KEY" in error_msg.upper():
            if "Email" in error_msg:
                return False, "El Email ya está en uso. Por favor, intente con otro o inicie sesión.", None
            elif "RUC" in error_msg:
                return False, "El RUC ya está en uso. Por favor, intente con otro o inicie sesión.", None
            else:
                return False, "Dato duplicado (Email o RUC) ya registrado. Por favor, verifique.", None
        # Para otros errores de integridad que no sean de unicidad (ej. NOT NULL, si no se validaron antes)
        return False, f"Error de integridad de la base de datos al registrar: {str(e)}. Por favor, verifique sus datos.", None
    
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        print(f"ERROR (registrar_nuevo_cliente - pyodbc general): {sqlstate} - {e}")
        if conn:
            conn.rollback() # Si hay un error, revertir la transacción
        return False, f"Ocurrió un error de base de datos al registrar. Por favor, intente de nuevo más tarde.", None
    
    except Exception as e:
        print(f"ERROR (registrar_nuevo_cliente - general): {e}")
        if conn:
            conn.rollback() # Si hay un error, revertir la transacción
        return False, f"Ocurrió un error inesperado al registrar. Por favor, intente de nuevo más tarde.", None
    finally:
        if conn:
            conn.close()
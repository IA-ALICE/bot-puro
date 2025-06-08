from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import os
import secrets

from bot.venta_funtions import obtener_nombres_de_categoria, obtener_contenido_promociones, obtener_contenido_categoria
from bot.Servicios import obtener_servicios_principales, obtener_catalogo_por_servicio, obtener_preguntas_por_catalogo, obtener_respuestas_de_la_pregunta
from bot.iniciar_sesion import verificar_credenciales
from bot.registrar import registrar_nuevo_cliente

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = secrets.token_hex(16)
Session(app)

@app.route('/')
def index():
    session.clear()
    session['context'] = 'main_menu'
    session['last_options'] = []
    session['logged_in_user'] = None
    return render_template('index.html')

@app.route('/api/get_initial_message')
def get_initial_message():
    if 'context' not in session:
        session['context'] = 'main_menu'
    
    logged_in = session.get('logged_in_user') is not None
    response_text = "¡Hola! Soy el Asistente J&P. ¿En qué puedo ayudarte?\n\n" \
                    + get_main_menu_text(logged_in)
    
    return jsonify({"response": response_text, "options": [], "input_type": "number"})

@app.route('/api/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    context = session.get('context', 'main_menu')
    last_options = session.get('last_options', [])
    logged_in = session.get('logged_in_user') is not None
    
    bot_response_text = ""
    bot_options = []
    input_type = "number" # Valor por defecto para input_type

    if context == 'atencion_cliente_menu':
        # ... (Tu código actual para atención al cliente) ...
        bot_response_text = f"Gracias por tu consulta: '{user_message}'. Un agente revisará tu solicitud y se pondrá en contacto contigo. Si deseas hacer otra consulta, puedes escribirla, o selecciona 0 para volver al menú principal."
        bot_options.append({"id": 0, "text": "0. Volver al menú principal"})
        session['context'] = 'atencion_cliente_menu'
        input_type = "text"
        return jsonify({"response": bot_response_text, "options": bot_options, "input_type": input_type})
    
    elif context == 'login_prompt':
        email_o_ruc = user_message.strip()
        if email_o_ruc == "0": # Option 0 to go back from login prompt
            session['context'] = 'main_menu'
            bot_response_text = "Volviendo al menú principal.\n\n" + get_main_menu_text(logged_in)
            input_type = "number"
        else:
            success, message = verificar_credenciales(email_o_ruc)
            if success:
                bot_response_text = f"{message}"
                session['logged_in_user'] = email_o_ruc # Guarda el email o RUC como usuario logeado
                session['context'] = 'main_menu'
                bot_response_text += "\n\n" + get_main_menu_text(True) # Pass True because the user is now logged in
                input_type = "number"
            else:
                bot_response_text = f"{message} Por favor, intente de nuevo con su Email o RUC, o ingrese 0 para volver."
                bot_options.append({"id": 0, "text": "0. Volver al menú principal"})
                session['context'] = 'login_prompt'
                input_type = "text"
        return jsonify({"response": bot_response_text, "options": bot_options, "input_type": input_type})
    
    elif context == 'register_prompt':
        if user_message.strip() == "0": # Option 0 to go back from register prompt
            session['context'] = 'main_menu'
            bot_response_text = "Registro cancelado. Volviendo al menú principal.\n\n" + get_main_menu_text(logged_in)
            input_type = "number"
            return jsonify({"response": bot_response_text, "options": bot_options, "input_type": input_type})

        try:
            parts = [p.strip() for p in user_message.split(',')]
            
            # Asegurar que haya suficientes partes para Nombre y Teléfono (obligatorio)
            # y que email/ruc se manejen como opcionales
            if not (2 <= len(parts) <= 4): # Mínimo 2 (Nombre, Telefono) y Máximo 4 (Nombre, Email, Teléfono, RUC)
                raise ValueError("Número incorrecto de campos. Debe ser 'nombre,email,telefono,ruc' o 'nombre,,telefono,ruc' o 'nombre,email,telefono,'.")
            
            nombre = parts[0]
            email = parts[1] if len(parts) > 1 and parts[1] else None # Email puede ser vacío
            telefono = parts[2] if len(parts) > 2 and parts[2] else None # Teléfono puede ser vacío
            ruc = parts[3] if len(parts) > 3 and parts[3] else None # RUC puede ser vacío

            # Validar que al menos Telefono sea proporcionado y que al menos (Email o RUC) existan
            if not telefono:
                bot_response_text = "El número de teléfono es obligatorio para el registro. Por favor, intente de nuevo o 0 para volver."
                session['context'] = 'register_prompt'
                input_type = "text"
                bot_options.append({"id": 0, "text": "0. Volver al menú principal"})
                return jsonify({"response": bot_response_text, "options": bot_options, "input_type": input_type})

            if not email and not ruc:
                bot_response_text = "Debe proporcionar al menos un Email o un RUC para el registro. Por favor, intente de nuevo o 0 para volver."
                session['context'] = 'register_prompt'
                input_type = "text"
                bot_options.append({"id": 0, "text": "0. Volver al menú principal"})
                return jsonify({"response": bot_response_text, "options": bot_options, "input_type": input_type})

            success, message, registered_identifier = registrar_nuevo_cliente(nombre, email, telefono, ruc)
            if success:
                bot_response_text = f"{message}"
                session['logged_in_user'] = registered_identifier # Log in the user after successful registration
                session['context'] = 'main_menu'
                bot_response_text += "\n\n" + get_main_menu_text(True)
                input_type = "number"
            else:
                # El mensaje de error ya viene de registrar.py con el detalle de la validación
                bot_response_text = f"{message} Por favor, intente de nuevo o 0 para volver."
                bot_options.append({"id": 0, "text": "0. Volver al menú principal"})
                session['context'] = 'register_prompt'
                input_type = "text"
        except ValueError as ve:
            bot_response_text = f"Formato incorrecto: {ve}. Por favor, ingrese 'nombre,email,telefono,ruc' (email y/o ruc pueden ser vacíos, pero el teléfono es obligatorio), o 0 para volver."
            session['context'] = 'register_prompt'
            input_type = "text"
            bot_options.append({"id": 0, "text": "0. Volver al menú principal"})
        except pyodbc.Error as db_error:
            # Captura errores generales de pyodbc que puedan venir de DB.py si la conexión falla completamente
            # (Aunque DB.py ya los maneja al retornar None, esta es una capa adicional)
            print(f"DEBUG: Error de pyodbc en app.py: {db_error}")
            bot_response_text = "Ocurrió un error en la base de datos al procesar su solicitud. Por favor, intente de nuevo o 0 para volver."
            session['context'] = 'register_prompt'
            input_type = "text"
            bot_options.append({"id": 0, "text": "0. Volver al menú principal"})
        except Exception as e:
            # Captura cualquier otra excepción inesperada
            print(f"DEBUG: Error inesperado en app.py: {e}")
            bot_response_text = f"Ocurrió un error inesperado al registrar: {e}. Por favor, intente de nuevo o 0 para volver."
            session['context'] = 'register_prompt'
            input_type = "text"
            bot_options.append({"id": 0, "text": "0. Volver al menú principal"})
        return jsonify({"response": bot_response_text, "options": bot_options, "input_type": input_type})
    
    # --- Resto del código del bot ---
    try:
        choice = int(user_message)
    except ValueError:
        bot_response_text = "Entrada inválida. Por favor, ingrese el número de la opción deseada."
        bot_options = last_options
        return jsonify({"response": bot_response_text, "options": bot_options, "input_type": input_type})

    if context == 'main_menu':
        if choice == 1:
            session['context'] = 'ventas_menu'
            bot_response_text = "--- Menú de Ventas ---\n1. Ver Promociones\n2. Ver Categorías\n0. Volver al menú principal"
        elif choice == 2:
            session['context'] = 'atencion_cliente_menu'
            bot_response_text = "--- Atención al Cliente ---\nPor favor, ingresa tu consulta de forma detallada."
            input_type = "text"
        elif choice == 3:
            session['context'] = 'servicios_menu'
            servicios_principales = obtener_servicios_principales()
            if servicios_principales:
                bot_response_text = "--- SERVICIOS PRINCIPALES DISPONIBLES ---\n"
                indexed_options = []
                for i, sp in enumerate(servicios_principales):
                    # Se muestra el índice + 1 al usuario, pero se guarda el ID real para el backend
                    bot_response_text += f"{i + 1}. {sp['nombre']}\n"
                    indexed_options.append({"id": sp['id'], "text": f"{i + 1}. {sp['nombre']}"})
                bot_response_text += "0. Volver al menú principal"
                indexed_options.append({"id": 0, "text": "0. Volver al menú principal"})
                session['last_options'] = indexed_options
            else:
                bot_response_text = "No hay servicios principales disponibles en este momento."
                bot_options.append({"id": 0, "text": "0. Volver al menú principal"})
                session['context'] = 'main_menu'
        elif choice == 4:
            if logged_in:
                bot_response_text = "Ya has iniciado sesión. Por favor, selecciona una opción válida o 0 para cerrar sesión."
                bot_response_text += "\n\n" + get_main_menu_text(logged_in)
            else:
                session['context'] = 'login_prompt'
                bot_response_text = "Para iniciar sesión, por favor, ingresa tu Email o RUC:"
                input_type = "text"
        elif choice == 5:
            if logged_in:
                bot_response_text = "Ya has iniciado sesión. No puedes registrarte de nuevo sin cerrar sesión. Por favor, selecciona una opción válida o 0 para cerrar sesión."
                bot_response_text += "\n\n" + get_main_menu_text(logged_in)
            else:
                session['context'] = 'register_prompt'
                bot_response_text = "Para registrarte, por favor, ingresa tus datos en el formato: nombre,email,telefono,ruc\n(Email o RUC pueden ser vacíos, pero el teléfono es obligatorio):"
                input_type = "text"
        elif choice == 0:
            if logged_in:
                bot_response_text = "Has cerrado sesión. ¡Hasta pronto!"
                session.clear()
                session['context'] = 'main_menu'
                session['logged_in_user'] = None # Explicitly set to None after logout
                bot_response_text += "\n\n" + get_main_menu_text(False) # Show guest menu after logout
                # REMOVED: bot_options.append({"id": "restart", "text": "Reiniciar Bot"})
            else:
                bot_response_text = "Cerrando la sesión. ¡Hasta pronto!"
                session.clear()
                session['context'] = 'main_menu'
                session['logged_in_user'] = None
                bot_response_text += "\n\n" + get_main_menu_text(False) # Revert to initial menu
                # REMOVED: bot_options.append({"id": "restart", "text": "Reiniciar Bot"})
        else:
            bot_response_text = "Opción no válida. Por favor, seleccione una de las opciones del menú principal."
            bot_response_text += "\n\n" + get_main_menu_text(logged_in)
    
    # Existing context handling... (no changes needed here for the main menu options)
    elif context == 'ventas_menu':
        if choice == 1:
            session['context'] = 'promociones_list'
            categorias = obtener_nombres_de_categoria()
            if categorias:
                bot_response_text = "Seleccione una categoría para ver sus promociones:\n"
                indexed_options = []
                for i, cat in enumerate(categorias):
                    bot_response_text += f"{i + 1}. {cat['nombre']}\n"
                    indexed_options.append({"id": cat['id'], "text": f"{i + 1}. {cat['nombre']}"})
                bot_response_text += "0. Volver al menú anterior"
                indexed_options.append({"id": 0, "text": "0. Volver al menú anterior"})
                session['last_options'] = indexed_options
            else:
                bot_response_text = "No se encontraron promociones/categorías disponibles en este momento."
                bot_options.append({"id": 0, "text": "0. Volver al menú anterior"})
                session['context'] = 'ventas_menu'
        elif choice == 2:
            session['context'] = 'categorias_list'
            categorias = obtener_nombres_de_categoria()
            if categorias:
                bot_response_text = "Seleccione una categoría para ver su contenido:\n"
                indexed_options = []
                for i, cat in enumerate(categorias):
                    bot_response_text += f"{i + 1}. {cat['nombre']}\n"
                    indexed_options.append({"id": cat['id'], "text": f"{i + 1}. {cat['nombre']}"})
                bot_response_text += "0. Volver al menú anterior"
                indexed_options.append({"id": 0, "text": "0. Volver al menú anterior"})
                session['last_options'] = indexed_options
            else:
                bot_response_text = "No se encontraron categorías disponibles en este momento."
                bot_options.append({"id": 0, "text": "0. Volver al menú anterior"})
                session['context'] = 'ventas_menu'
        elif choice == 0:
            session['context'] = 'main_menu'
            bot_response_text = get_main_menu_text(logged_in)
        else:
            bot_response_text = "Opción no válida. Por favor, seleccione una opción del menú de ventas."

    elif context == 'promociones_list':
        if choice == 0:
            session['context'] = 'ventas_menu'
            bot_response_text = "--- Menú de Ventas ---\n1. Ver Promociones\n2. Ver Categorías\n0. Volver al menú principal"
            session['last_options'] = []
        else:
            # Recuperar el ID real de la opción seleccionada por el usuario
            selected_option = next((opt for opt in last_options if opt['text'].split('.')[0] == str(choice)), None)
            if selected_option:
                actual_id = selected_option['id']
                promo_info = obtener_contenido_promociones(actual_id)
                if promo_info["success"]:
                    bot_response_text = f"Aquí está la promoción para {promo_info['nombre_categoria']}:\n{promo_info['pdf_promo_link']}"
                    bot_options.append({"id": 0, "text": "0. Volver a la lista de promociones"})
                    session['context'] = 'promociones_list'
                else:
                    bot_response_text = promo_info["message"] + "\nPor favor, seleccione una opción válida o 0 para volver."
                    bot_options = last_options
                    session['context'] = 'promociones_list'
            else:
                bot_response_text = "Opción no válida. Por favor, seleccione una opción válida o 0 para volver."
                bot_options = last_options
                session['context'] = 'promociones_list'

    elif context == 'categorias_list':
        if choice == 0:
            session['context'] = 'ventas_menu'
            bot_response_text = "--- Menú de Ventas ---\n1. Ver Promociones\n2. Ver Categorías\n0. Volver al menú principal"
            session['last_options'] = []
        else:
            # Recuperar el ID real de la opción seleccionada por el usuario
            selected_option = next((opt for opt in last_options if opt['text'].split('.')[0] == str(choice)), None)
            if selected_option:
                actual_id = selected_option['id']
                cat_info = obtener_contenido_categoria(actual_id)
                if cat_info["success"]:
                    bot_response_text = f"Aquí está el contenido de {cat_info['nombre_categoria']}:\n{cat_info['pdf_link']}"
                    bot_options.append({"id": 0, "text": "0. Volver a la lista de categorías"})
                    session['context'] = 'categorias_list'
                else:
                    bot_response_text = cat_info["message"] + "\nPor favor, seleccione una opción válida o 0 para volver."
                    bot_options = last_options
                    session['context'] = 'categorias_list'
            else:
                bot_response_text = "Opción no válida. Por favor, seleccione una opción válida o 0 para volver."
                bot_options = last_options
                session['context'] = 'categorias_list'

    elif context == 'servicios_menu':
        if choice == 0:
            session['context'] = 'main_menu'
            bot_response_text = get_main_menu_text(logged_in)
            session['last_options'] = []
        else:
            # Obtener el ID real de la opción seleccionada por el usuario
            selected_option = next((opt for opt in last_options if opt['text'].split('.')[0] == str(choice)), None)
            
            if selected_option:
                actual_service_id = selected_option['id']
                servicios_principales = obtener_servicios_principales()
                servicio_elegido = next((s for s in servicios_principales if s['id'] == actual_service_id), None)

                if servicio_elegido:
                    session['current_service_id'] = actual_service_id
                    session['context'] = 'catalogo_menu'
                    catalogo_items = obtener_catalogo_por_servicio(actual_service_id)
                    if catalogo_items:
                        bot_response_text = f"--- APARTADOS DEL CATÁLOGO PARA: {servicio_elegido['nombre']} ---\n"
                        indexed_options = []
                        for i, item in enumerate(catalogo_items):
                            precio_str = f" (Precio: {item['precio']})" if item['precio'] is not None else ""
                            bot_response_text += f"{i + 1}. {item['nombre_apartado']}{precio_str}\n"
                            indexed_options.append({"id": item['id'], "text": f"{i + 1}. {item['nombre_apartado']}{precio_str}"})
                        bot_response_text += "0. Volver a la lista de Servicios Principales"
                        indexed_options.append({"id": 0, "text": "0. Volver a la lista de Servicios Principales"})
                        session['last_options'] = indexed_options
                    else:
                        bot_response_text = f"No hay apartados en el catálogo para '{servicio_elegido['nombre']}'.\n0. Volver a la lista de Servicios Principales"
                        bot_options.append({"id": 0, "text": "0. Volver a la lista de Servicios Principales"})
                        session['context'] = 'servicios_menu'
                else:
                    bot_response_text = "Opción de Servicio Principal no válida. Intente de nuevo."
                    servicios_principales = obtener_servicios_principales()
                    if servicios_principales:
                        bot_response_text += "\n--- SERVICIOS PRINCIPALES DISPONIBLES ---\n"
                        indexed_options = []
                        for i, sp in enumerate(servicios_principales):
                            bot_response_text += f"{i + 1}. {sp['nombre']}\n"
                            indexed_options.append({"id": sp['id'], "text": f"{i + 1}. {sp['nombre']}"})
                        bot_response_text += "0. Volver al menú principal"
                        indexed_options.append({"id": 0, "text": "0. Volver al menú principal"})
                        session['last_options'] = indexed_options
            else:
                bot_response_text = "Opción de Servicio Principal no válida. Intente de nuevo."
                bot_options = last_options # Mantener las últimas opciones si la entrada fue inválida

    elif context == 'catalogo_menu':
        if choice == 0:
            session['context'] = 'servicios_menu'
            servicios_principales = obtener_servicios_principales()
            bot_response_text = "--- SERVICIOS PRINCIPALES DISPONIBLES ---\n"
            indexed_options = []
            for i, sp in enumerate(servicios_principales):
                bot_response_text += f"{i + 1}. {sp['nombre']}\n"
                indexed_options.append({"id": sp['id'], "text": f"{i + 1}. {sp['nombre']}"})
            bot_response_text += "0. Volver al menú principal"
            indexed_options.append({"id": 0, "text": "0. Volver al menú principal"})
            session['last_options'] = indexed_options
        else:
            current_service_id = session.get('current_service_id')
            if current_service_id is None:
                bot_response_text = "Error: No se pudo determinar el servicio principal. Volviendo al menú principal."
                session['context'] = 'main_menu'
                bot_response_text += "\n" + get_main_menu_text(logged_in)
            else:
                # Obtener el ID real de la opción seleccionada por el usuario
                selected_option = next((opt for opt in last_options if opt['text'].split('.')[0] == str(choice)), None)
                
                if selected_option:
                    actual_catalogo_id = selected_option['id']
                    items_catalogo = obtener_catalogo_por_servicio(current_service_id)
                    item_elegido = next((i for i in items_catalogo if i['id'] == actual_catalogo_id), None)

                    if item_elegido:
                        session['current_catalogo_item_id'] = actual_catalogo_id
                        session['context'] = 'preguntas_menu'
                        preguntas = obtener_preguntas_por_catalogo(actual_catalogo_id)
                        if preguntas:
                            bot_response_text = f"--- PREGUNTAS PARA: {item_elegido['nombre_apartado']} ---\n"
                            indexed_options = []
                            for i, p in enumerate(preguntas):
                                bot_response_text += f"{i + 1}. {p['texto']}\n"
                                indexed_options.append({"id": p['id'], "text": f"{i + 1}. {p['texto']}"})
                            bot_response_text += "0. Volver a la lista de Apartados del Catálogo"
                            indexed_options.append({"id": 0, "text": "0. Volver a la lista de Apartados del Catálogo"})
                            session['last_options'] = indexed_options
                        else:
                            bot_response_text = f"No hay preguntas disponibles para '{item_elegido['nombre_apartado']}'.\n0. Volver a la lista de Apartados del Catálogo"
                            bot_options.append({"id": 0, "text": "0. Volver a la lista de Apartados del Catálogo"})
                            session['context'] = 'catalogo_menu'
                    else:
                        bot_response_text = "Opción de Apartado del Catálogo no válida. Intente de nuevo."
                        bot_options = last_options
                        session['context'] = 'catalogo_menu'
                else:
                    bot_response_text = "Opción de Apartado del Catálogo no válida. Intente de nuevo."
                    bot_options = last_options
                    session['context'] = 'catalogo_menu'

    elif context == 'preguntas_menu':
        if choice == 0:
            session['context'] = 'catalogo_menu'
            current_service_id = session.get('current_service_id')
            if current_service_id:
                items_catalogo = obtener_catalogo_por_servicio(current_service_id)
                servicio_principal_nombre = next((s['nombre'] for s in obtener_servicios_principales() if s['id'] == current_service_id), f"Servicio ID {current_service_id}")
                bot_response_text = f"--- APARTADOS DEL CATÁLOGO PARA: {servicio_principal_nombre} ---\n"
                indexed_options = []
                for i, item in enumerate(items_catalogo):
                    precio_str = f" (Precio: {item['precio']})" if item['precio'] is not None else ""
                    bot_response_text += f"{i + 1}. {item['nombre_apartado']}{precio_str}\n"
                    indexed_options.append({"id": item['id'], "text": f"{i + 1}. {item['nombre_apartado']}{precio_str}"})
                bot_response_text += "0. Volver a la lista de Servicios Principales"
                indexed_options.append({"id": 0, "text": "0. Volver a la lista de Servicios Principales"})
                session['last_options'] = indexed_options
            else:
                bot_response_text = "Error: No se pudo cargar el catálogo anterior. Volviendo al menú principal."
                session['context'] = 'main_menu'
                bot_response_text += "\n" + get_main_menu_text(logged_in)
        else:
            current_catalogo_item_id = session.get('current_catalogo_item_id')
            if current_catalogo_item_id is None:
                bot_response_text = "Error: No se pudo determinar el ítem de catálogo. Volviendo al menú principal."
                session['context'] = 'main_menu'
                bot_response_text += "\n" + get_main_menu_text(logged_in)
            else:
                # Obtener el ID real de la opción seleccionada por el usuario
                selected_option = next((opt for opt in last_options if opt['text'].split('.')[0] == str(choice)), None)
                
                if selected_option:
                    actual_pregunta_id = selected_option['id']
                    preguntas = obtener_preguntas_por_catalogo(current_catalogo_item_id)
                    pregunta_elegida = next((p for p in preguntas if p['id'] == actual_pregunta_id), None)

                    if pregunta_elegida:
                        session['current_pregunta_id'] = actual_pregunta_id
                        session['context'] = 'respuestas_menu'
                        respuestas = obtener_respuestas_de_la_pregunta(actual_pregunta_id)
                        if respuestas:
                            bot_response_text = f"--- RESPUESTAS PARA: {pregunta_elegida['texto'][:60]}... ---\n"
                            for res_text in respuestas:
                                bot_response_text += f"- {res_text}\n"
                            bot_response_text += "0. Volver a la lista de Preguntas"
                            bot_options.append({"id": 0, "text": "0. Volver a la lista de Preguntas"})
                        else:
                            bot_response_text = "No se encontraron respuestas para esta pregunta.\n0. Volver a la lista de Preguntas"
                            bot_options.append({"id": 0, "text": "0. Volver a la lista de Preguntas"})
                        session['context'] = 'preguntas_menu' # Se mantiene en preguntas_menu para que al volver, muestre las preguntas nuevamente.
                    else:
                        bot_response_text = "Opción de Pregunta no válida. Intente de nuevo."
                        bot_options = last_options
                        session['context'] = 'preguntas_menu'
                else:
                    bot_response_text = "Opción de Pregunta no válida. Intente de nuevo."
                    bot_options = last_options
                    session['context'] = 'preguntas_menu'

    elif context == 'respuestas_menu':
        if choice == 0:
            session['context'] = 'preguntas_menu'
            current_catalogo_item_id = session.get('current_catalogo_item_id')
            if current_catalogo_item_id:
                preguntas = obtener_preguntas_por_catalogo(current_catalogo_item_id)
                nombre_apartado = next((i['nombre_apartado'] for i in obtener_catalogo_por_servicio(session.get('current_service_id')) if i['id'] == current_catalogo_item_id), f"Apartado ID {current_catalogo_item_id}")
                bot_response_text = f"--- PREGUNTAS PARA: {nombre_apartado} ---\n"
                indexed_options = []
                for i, p in enumerate(preguntas):
                    bot_response_text += f"{i + 1}. {p['texto']}\n"
                    indexed_options.append({"id": p['id'], "text": f"{i + 1}. {p['texto']}"})
                bot_response_text += "0. Volver a la lista de Apartados del Catálogo"
                indexed_options.append({"id": 0, "text": "0. Volver a la lista de Apartados del Catálogo"})
                session['last_options'] = indexed_options
            else:
                bot_response_text = "Error: No se pudo cargar el menú de preguntas anterior. Volviendo al menú principal."
                session['context'] = 'main_menu'
                bot_response_text += "\n" + get_main_menu_text(logged_in)
        else:
            bot_response_text = "Por favor, seleccione 0 para volver al menú de preguntas."
            bot_options.append({"id": 0, "text": "0. Volver a la lista de Preguntas"})

    if session.get('context') == 'unknown':
        session['context'] = 'main_menu'
        bot_response_text = "Lo siento, hubo un error. Volviendo al menú principal.\n\n" + get_main_menu_text(logged_in)
        bot_options = []

    return jsonify({"response": bot_response_text, "options": bot_options, "input_type": input_type})

def get_main_menu_text(is_logged_in):
    """Helper function to generate the main menu text based on login status."""
    menu = "--- Menú Principal ---\n" \
           "1. Venta\n" \
           "2. Atención al Cliente\n" \
           "3. Asistente de Servicios Técnicos\n"
    if is_logged_in:
        menu += "0. Cerrar Sesión"
    else:
        menu += "4. Iniciar Sesión\n" \
                "5. Registrarse" # No option 0 when not logged in initially
    return menu

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
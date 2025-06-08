# bot/Utter.py
# Este archivo contiene los mensajes predefinidos del bot, ahora como constantes.
# Estos mensajes serán utilizados por tu aplicación Flask para construir las respuestas al usuario.

# Mensajes para menús principales
UTTER_MENU_PRINCIPAL = """--- Menú Principal ---
1.- Venta
2.- Atención al Cliente
3.- Asistente de Servicios Técnicos
4.- Iniciar Sesión
5.- Registrarse
0.- Salir del Programa"""

# Mensajes para submenús
UTTER_MENU_VENTA = """--- Menú de Ventas ---
1.- Ver Promociones
2.- Ver Categorías
0.- Volver al menú principal"""

UTTER_MENU_ATENCION = """--- Atención al Cliente ---
Estamos aquí para ayudarle. Puede comunicarse con nosotros a través de los siguientes medios:"""

UTTER_MENU_SERVICIO = """--- Asistente de Servicios Técnicos ---
Bienvenido al Asistente Interactivo de Servicios Técnicos. Seleccione un servicio para empezar:"""

# Mensajes específicos de acción/contexto
UTTER_LOGEO = "Por favor, ingrese sus credenciales (correo o RUC) para iniciar sesión."
UTTER_REGISTRAR = "Complete los siguientes datos para crear una nueva cuenta. ¡Le damos la bienvenida!"
UTTER_PROMOS_DISPONIBLES = "Tenemos promociones destacadas en las siguientes categorías:"
UTTER_CATEGORIAS_DISPONIBLES = "Estas son nuestras categorías de productos:"

# Mensajes de sistema / feedback
UTTER_SESION_CERRADA = "Su sesión ha sido cerrada. ¡Hasta pronto!"
UTTER_SALIENDO_PROGRAMA = "Saliendo del programa. ¡Gracias por usar nuestros servicios!"
UTTER_OPCION_INVALIDA = "La opción ingresada es inválida. Por favor, ingrese una de las opciones disponibles."
UTTER_ENTRADA_INVALIDA = "Entrada inválida. Debe ingresar un valor válido." # Más genérico para evitar 'número' si se esperan otros tipos

# Mensajes de contacto para atención al cliente
CONTACTO_NUMERO = "Teléfono: +51 987 654 321" # Reemplaza con tu número real
CONTACTO_CORREO = "Correo: soporte@jyp.com" # Reemplaza con tu correo real

# Mensajes adicionales que podrían ser útiles
UTTER_VOLVER_MENU_ANTERIOR = "0.- Volver al menú anterior"
UTTER_NO_SERVICIOS_DISPONIBLES = "En este momento no hay servicios principales disponibles."
UTTER_NO_CATALOGO_DISPONIBLE = "No hay apartados en el catálogo para este servicio."
UTTER_NO_PREGUNTAS_DISPONIBLES = "No hay preguntas disponibles para este apartado del catálogo."
UTTER_NO_RESPUESTAS_DISPONIBLES = "No se encontraron respuestas para esta pregunta."
UTTER_PRESIONE_ENTER_CONTINUAR = "Presione Enter para continuar..." # Esto se manejaría en el frontend  
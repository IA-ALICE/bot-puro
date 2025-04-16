# menu.py
from Utter import *
from venta_funtions import *
from DB import get_db_connection
#---------------------------------------------------Validar opciones que ingrese el usuario---------------------------------------
def obtener_opcion(menu_texto, opciones_validas):
    """Obtiene una opción válida del usuario para un menú específico."""
    while True:
        try:
            opcion = int(input(f"{menu_texto}\nIngrese el número de la opción deseada: "))
            if opcion in opciones_validas:
                return opcion
            else:
                print("---------------------------------------------------------------------------")
                print(utter_opcion_invalida)
        except ValueError:
            print("---------------------------------------------------------------------------")
            print(utter_entrada_invalida)

#----------------------------------------------------------------Menú venta--------------------------------------------------------
def menu_venta():
    while True:
        opciones_venta = [0, 1, 2]
        opcion_venta = obtener_opcion(utter_venta, opciones_venta)
        print("---------------------------------------------------------------------------")
        if opcion_venta == 1:
            print(utter_promociones)
            imprimir_nombres_de_categoria()
            opcion_promociones = int(input("Ingrese el número de la categoría para ver sus promociones: "))
            mostrar_contenido_promociones(opcion_promociones)
            input(":Inrese un número para volver al menú anterior")
            print("---------------------------------------------------------------------------")
        elif opcion_venta == 2:
            print(utter_categoria)
            imprimir_nombres_de_categoria()
            opcion_categoria = int(input("Ingrese el número de la categoría para ver su contenido: "))
            mostrar_contenido_categoria(opcion_categoria)
            input("Ingrese un número para volver al menú anterior")
            print("---------------------------------------------------------------------------")
        elif opcion_venta == 0:
            return

#-------------------------------------------------------Menú principal--------------------------------------------------------------
def menu_principal():
    while True:
        opciones_principal = [0, 1, 2, 3, 4, 5]
        opcion = obtener_opcion(utter_menu, opciones_principal)
        print("---------------------------------------------------------------------------")
        if opcion == 1:
            menu_venta()
        elif opcion == 2:
            print(utter_atencion)
            input("Presione Enter para volver al menú principal...")
        elif opcion == 3:
            print(utter_servicio)
            input("Presione Enter para volver al menú principal...")
        elif opcion == 4:
            print(utter_logeo)
            input("Presione Enter para volver al menú principal...")
        elif opcion == 5:
            print(utter_registrar)
            input("Presione Enter para volver al menú principal...")
        elif opcion == 0:
            print(utter_registrar)
            input("Presione Enter para volver al menú principal...")
        elif opcion == 0:
            print("Saliendo del programa.")
            break

#----------------------------------Iniciar menú---------------------------------------------------------------------------------------
if __name__ == "__main__":
    menu_principal()
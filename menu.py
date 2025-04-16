# menu.py
from Utter import *
from DB import get_db_connection

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

def menu_venta():
    while True:
        opciones_venta = [0, 1, 2]
        opcion_venta = obtener_opcion(utter_venta, opciones_venta)
        print("---------------------------------------------------------------------------")
        if opcion_venta == 1:
            print(utter_promociones)
            input(utter_volver)
        elif opcion_venta == 2:
            print(utter_categoria)
            input(utter_volver)
        elif opcion_venta == 0:
            return

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
            print("Saliendo del programa.")
            break

if __name__ == "__main__":
    menu_principal()
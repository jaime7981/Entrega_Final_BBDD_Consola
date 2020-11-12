from tabulate import tabulate
import os
import Lorenzini as ln
import Fernandez as fz
import usefullfunc as psfunc

def ValidacionUsuario():
    print("Iniciar Sesion\n")
    login_nombre_usuario = input("Ingresar nombre de usuario: ")
    login_clave = input("Ingresar clave: ")
    flag_menu_usuario = psfunc.ValidacionUsuario(login_nombre_usuario, login_clave)
    if flag_menu_usuario == False:
        print("Usuario o clave incorrecta")
        return ""
    if flag_menu_usuario == True:
        return login_nombre_usuario

def RegistrarUsuario():
    while True:
        print("Bienvenido a Hubber Eats\nRegistrarse:\n")
        nombre_apellido = "'" + input("Ingresar nombre y apellido: ") + "'"
        nombre_usuario = "'" + input("Ingresar usuario: ") + "'"
        clave_nuevo_usuario = "'" + input("Ingresar clave: ") + "'"
        numero_usuario = input("Ingresar numero de telefono: ")

        if len(clave_nuevo_usuario) <= 6:
            print("Clave no valida")

        if "@" in nombre_usuario \
            and (".com" in nombre_usuario or ".cl" in nombre_usuario)\
            and len(clave_nuevo_usuario) > 6 and len(nombre_usuario) > 8\
            and len(numero_usuario) == 9:
            nuevo_id_usuario = psfunc.SelectQuerry("SELECT id_usuario FROM usuarios")

            crear_usuario = psfunc.InsertQuerry("usuarios", (), (str(len(nuevo_id_usuario) + 1),
                                                            nombre_apellido, 
                                                            nombre_usuario, 
                                                            clave_nuevo_usuario, 
                                                            numero_usuario))

            if crear_usuario == True:
                print("usuario creado con exito")
                break
            else:
                print("Error al crear usuario")
                break

        else:
            print("Usuario no valido")
            break

menu_shoping_cart = []
product_shoping_cart = []

#Programa principal
main = True
print("Bienveido")

while main:
    #Menu de inicio
    login_menu = ["Ingrese querry",
                  "Iniciar Sesion", 
                  "Registrarse", 
                  "Exit",
                  "Ver Usuarios"]
    psfunc.DisplayMenu(login_menu)
    opcion = psfunc.InputOpciones(login_menu)

    if opcion == 1:
        querry = input("Ingresar querry: ")
        psfunc.PrintQuerry(querry)

    elif opcion == 2:
        login_nombre_usuario = ValidacionUsuario()

        while login_nombre_usuario != "":
            #Menu principal
            menu_entrada_usuario = ["Locales", 
                                    "Categorias", 
                                    "Promociones", 
                                    "Direcciones", 
                                    "Carrito", 
                                    "Historial de pedidos", 
                                    "Repartidores", 
                                    "Cerrar Sesion", 
                                    "Exit"]
            psfunc.DisplayMenu(menu_entrada_usuario)
            opcion = psfunc.InputOpciones(menu_entrada_usuario)

            if opcion == 1:
                fz.MenuLocales(login_nombre_usuario, menu_shoping_cart, product_shoping_cart)
            elif opcion == 2:
                pass

            elif opcion == 3:
                pass

            elif opcion == 4:
                pass

            elif opcion == 5:
                pass

            elif opcion == 6:
                ln.Historial_pedidos(login_nombre_usuario)
                pass

            elif opcion == 7:
                ln.Repartidores()
                pass

            elif opcion == 8:
                break

            elif opcion == 9:
                main = False
                psfunc.ClearShopingCart(menu_shoping_cart, product_shoping_cart)
                break

    elif opcion == 3:
        RegistrarUsuario()

    elif opcion == 4:
        main = False
    
    elif opcion == 5:
        psfunc.PrintQuerry("SELECT * FROM usuarios")

psfunc.CloseSV()
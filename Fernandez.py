from tabulate import tabulate
import usefullfunc as psfunc
import os

def AgregarLocal():
    print("Agregar local")
    nombre_local = "'" + input("Nombre local: ") + "'"
    calle_local = "'" + input("Direccion local: ") + "'"
    numero_local = input("Numero local: ")
    comuna_local = "'" + input("Comuna local: ") + "'"
    region_local = "'" + input("Region local: ") + "'"
    aceptar_opcion = input("Esta seguro de esta informacion? (S/N) ")
    if aceptar_opcion == "S":
        psfunc.InsertQuerry("locales", ("nombre", "calle", "numero", "comuna", "region"),
                                (nombre_local,
                                    calle_local,
                                    str(numero_local),
                                    comuna_local,
                                    region_local))

def VerMenus(id_local_seleccionado, menu_shoping_cart, product_shoping_cart):
    while True:
        psfunc.PrintQuerry("SELECT * FROM menues WHERE id_local = " + str(id_local_seleccionado))
        opcion_menues = ["Seleccionar Menu",
                        "Agregar Menu",
                        "Volver Atras"]
        psfunc.DisplayMenu(opcion_menues)
        opcion = psfunc.InputOpciones(opcion_menues)
        if opcion == 1:
            id_menu_seleccionado = psfunc.QuerryOptionIdCheck("SELECT id_menu FROM menues",
                                                              "Ingresar id menu: ")
            if id_menu_seleccionado != 0:
                while True:
                    psfunc.PrintQuerry("SELECT pr.id_local, pr.id_producto, pr.nombre, pr.precio, pr.id_descuento \
                                    FROM productos pr INNER JOIN \
                                    (SELECT mp.id_producto FROM menu_producto mp INNER JOIN \
                                    (SELECT men.id_menu FROM menues men WHERE id_menu = " + str(id_menu_seleccionado) + \
                                    ") AS t1 ON mp.id_menu = t1.id_menu) AS t2 ON pr.id_producto = t2.id_producto")

                    opcion_menues = ["Agregar Menu Al Carrito",
                                     "Eliminar Producto Del Menu",
                                     "Editar Menu",
                                     "Eliminar Menu",
                                     "Descuento",
                                     "Volver Atras"]
                    psfunc.DisplayMenu(opcion_menues)
                    opcion = psfunc.InputOpciones(opcion_menues)

                    if opcion == 1:
                        psfunc.AddToCart(id_menu_seleccionado, False, menu_shoping_cart, product_shoping_cart)
                        print("Menu Agregado Al Carrito")

                    elif opcion == 2:
                        id_producto_seleccionado = psfunc.QuerryOptionIdCheck("SELECT mp.id_producto FROM menu_producto mp INNER JOIN \
                                            (SELECT men.id_menu FROM menues men WHERE id_menu = 20) AS t1 ON mp.id_menu = t1.id_menu",
                                            "Ingresar ID producto: ")
                        if id_producto_seleccionado != 0:
                            delete_product_from_menu = input("Eliminar el producto del menu? (S/N) ")
                            if delete_product_from_menu == "S":
                                psfunc.DeleteQuerry("menu_producto", "id_menu = " + str(id_menu_seleccionado) + \
                                                                " AND id_producto = " + str(id_producto_seleccionado))
                        
                    elif opcion == 3:
                        print("Implementar editar menu")

                    elif opcion == 4:
                        print("Implementar eliminar menu")

                    elif opcion == 5:
                        print("Implementar opcion descuento")

                    elif opcion == 6:
                        break

        elif opcion == 2:
            print("implementar agregar menu")

        elif opcion == 3:
            break

def MenuLocales(login_nombre_usuario, menu_shoping_cart, product_shoping_cart):
    while True:
        psfunc.PrintQuerry("SELECT * FROM locales")
        opciones_locales = ["Seleccionar Local",
                            "Agregar Local",
                            "Volver Atras"]
        psfunc.DisplayMenu(opciones_locales)
        opcion = psfunc.InputOpciones(opciones_locales)
        if opcion == 1:
            id_local_seleccionado = psfunc.QuerryOptionIdCheck("SELECT id_local FROM locales", 
                                                        "Ingresar id local: ")
            if id_local_seleccionado != 0:
                while True:
                    psfunc.PrintQuerry("SELECT * FROM locales WHERE id_local = " + str(id_local_seleccionado))
                    opcion_local_id = ["Editar Local",
                                        "Eliminar Local",
                                        "Ver Menus",
                                        "Volver Atras"]
                    psfunc.DisplayMenu(opcion_local_id)
                    opcion = psfunc.InputOpciones(opcion_local_id)
                    if opcion == 1:
                        print("Implementar editar local")

                    elif opcion == 2:
                        delete_check = input("Seguro que desea eliminar este local (S/N) ")
                        if delete_check == "S":
                            psfunc.DeleteQuerry("locales", "id_local = " + str(id_local_seleccionado))

                    elif opcion == 3:
                        VerMenus(id_local_seleccionado, menu_shoping_cart, product_shoping_cart)

                    elif opcion == 4:
                        break

        elif opcion == 2:
            AgregarLocal()

        elif opcion == 3:
            break

def ShopingCart():
    while True:
        psfunc.PrintQuerry("SELECT * FROM locales")
        opciones_carrito = ["Eliminar Item",
                            "Vaciar Carrito",
                            "Eligir Promocion",
                            "Elegir Direccion",
                            "Confirmar Pedido"
                            "Volver Atras"]
        psfunc.DisplayMenu(opciones_carrito)
        opcion = psfunc.InputOpciones(opciones_carrito)

        if opcion == 1:
            print("No Implementado")

        elif opcion == 2:
            print("No Implementado")

        elif opcion == 3:
            print("No Implementado")

        elif opcion == 4:
            print("No Implementado")

        elif opcion == 5:
            print("No Implementado")

        elif opcion == 6:
            break


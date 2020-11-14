import psycopg2 as svpg
from tabulate import tabulate
con = svpg.connect(database="grupo6", 
                 user="grupo6", 
                 password="99sFKQ", 
                 host="201.238.213.114", 
                 port="54321")

#Devuelve un querry
def SelectQuerry(text):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        return request
    except:
        print("Querry ingresado no valido")

#Tabula e imprime un querry en la consola
def PrintQuerry(text):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        if len(request) == 0:
            print("No hay datos")
            return False
        description = []
        for desc in cur.description:
            description.append(desc[0])
        print(tabulate(request, headers = description, tablefmt="psql"))
        return True
    except:
        print("Querry ingresado no valido")
        return False

#InsertTest("nombre tabla", ("col1", "col2", "col3"), ("dato1", "dato2", "dato3"))
def InsertQuerry(table, lista_columnas, lista_datos):

    lista_d = "(" + ", ".join(lista_datos) + ")"
    lista_c = "(" + ", ".join(lista_columnas) + ")"

    if len(lista_datos) > 0:
        cur = con.cursor()
        if len(lista_c) == 2:
            try:
                insertstr = "INSERT INTO " + table + " VALUES " + lista_d
                cur.execute(insertstr)
                con.commit()
                return True
            except:
                print("Querry ingresado no valido")
                return False
        elif len(lista_c) > 2:
            try:
                insertstr = "INSERT INTO " + table + lista_c + " VALUES " + lista_d
                cur.execute(insertstr)
                con.commit()
                return True
            except:
                print("Querry ingresado no valido")
                return False
    else:
        print("Insert no tiene valores")
        return False

#Elimina una linea de la bbdd
def DeleteQuerry(table, text):
    cur = con.cursor()
    try:
        querry_text = "DELETE FROM " + table + " WHERE " + text
        cur.execute(querry_text)
        con.commit()
        print("Exito al ejecutar DELETE querry")
    except:
        print("Error al intentar eliminar la linea")

def UpdateQuerry(table, set_parameters, where_parameters):
    cur = con.cursor()
    try:
        querry_text = "UPDATE " + table + " SET " + set_parameters + " WHERE " + where_parameters
        cur.execute(querry_text)
        con.commit()
        print("Exito al ejecutar UPDATE querry")
    except:
        print("Error al intentar modificar la linea")

#Muestra en la consola el listado de opciones
def DisplayMenu(lista_menu):
    counter = 1
    for titulo_opcion in lista_menu:
        print(str(counter) + ") " + str(titulo_opcion))
        counter += 1

#Funcion que valida que la opcion ingresada sea un numero del menu
def InputOpciones(menu):
    try:
        opcion = int(input())
        if opcion <= len(menu) and opcion > 0:
            return opcion
        else:
            print("No existe la opcion ingresada")
    except:
        print("Opcion no valida")

#Valida que el usuario y clave ingresada esten en la bbdd 
def ValidacionUsuario(usuario, clave):
    usuarios_and_clave = SelectQuerry("SELECT email, contrasena FROM usuarios")
    for usuarios in usuarios_and_clave:
        if usuario == usuarios[0]:
            if clave == usuarios[1]:
                return True
    return False

#Sirve para verificar que el usuario metio un id que existe en la tabla
def QuerryOptionIdCheck(querry, text):
    try:
        option = int(input(text))
        querry_check = SelectQuerry(querry)
        for check in querry_check:
            if check[0] == option:
                return option
        print("Opcion no valida")
        return 0
    except:
        print("Error de querry")
        return 0

#Vacia el carrito de compras
def ClearShopingCart(menu_shoping_cart,product_shoping_cart):
    menu_shoping_cart.clear()
    product_shoping_cart.clear()

#Agrega un producto o menu al carrito
#True para producto False para menu
def AddToCart(product_menu_id, product_menu_flag, menu_shoping_cart,product_shoping_cart):
    try:
        if product_menu_flag == True:
            product_shoping_cart.append(product_menu_id)
        elif product_menu_flag == False:
            menu_shoping_cart.append(product_menu_id)
    except:
        print("Parametros ingresados a AddToCart debe ser (int, bool)")

#Cierra la conexion a la bbdd
def CloseSV():
    con.close()

#Pasa la informacion de la conexion a la bbdd
def GetCon():
    return con

### FUNCIONES LORENZINI

#Tabula un querry sin headers
def PrintQuerryNoHeaders(text):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        if len(request) == 0:
            print("No hay datos")
            return False
        print(tabulate(request, tablefmt="psql"))
        return True
    except:
        print("Querry ingresado no valido")
        return True

#Tabula un querry con los headers que uno le pase
def PrintQuerryCustomHeaders(text,headers):
    cur = con.cursor()
    try:
        cur.execute(text)
        request = cur.fetchall()
        return tabulate(request,headers, tablefmt="psql")
    except:
        print("Querry ingresado no válido")

def QuerryOptionIdCheck2(querry, option):
    try:
        option=option
        querry_check = SelectQuerry(querry)
        for check in querry_check:
            if check[0] == option:
                return option
        print("Opcion no valida")
        return 0
    except:
        print("Error de querry")
        return 0
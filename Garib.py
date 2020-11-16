import usefullfunc as psfunc
import os
from datetime import datetime

def CategoriasMenu():
    while True:
        psfunc.PrintQuerry("SELECT * FROM categorias")
        opciones = ['Agregar Categoría', 'Editar Categoría', 'Eliminar Categoría', 'Volver al menu principal']
        for opcion in opciones:
            print("{}) {}".format(opciones.index(opcion) + 1, opcion))

        seleccion_usuario = int(input('¿Que desea hacer?: '))

        if seleccion_usuario < 1 or seleccion_usuario > len(opciones):
            print("Opción invalida")

        if(seleccion_usuario == 1):
            nombre_nueva_categoria = input("Ingrese el nombre de la nueva categoria: ")
            querry = psfunc.InsertQuerry("categorias", (["nombre"]), (["'" + nombre_nueva_categoria + "'"]))
            if(querry):
                print("!Categoría agregada!")
            else:
                print("Error agregando categoría")
            break

        elif(seleccion_usuario == 2):
            categoria_seleccionada = input("¿Que categoria quiere editar?: ")
            nuevo_nombre = input("Ingrese nuevo nombre de la categoria: ")
            querry = psfunc.EditQuerry("categorias", ["nombre"], [nuevo_nombre], "id_categoria = {}".format(categoria_seleccionada))
            
            if(querry):
                print("!Categoría editada!")
            else:
                print("Error editando categoría")
            break
        elif(seleccion_usuario == 3):
            # Eliminar categoria
            categoria_seleccionada = input("¿Que categoria quiere eliminar?: ")
            querry = psfunc.DeleteQuerry("categorias", "id_categoria = {}".format(categoria_seleccionada))
            if(querry):
                print("!Categoría eliminada!")
            else:
                print("Error eliminado categoría")
            break
        else:
            break


def PromocionesMenu():
    while(True):
        psfunc.PrintQuerry("SELECT id_codigo, nombre, (monto * usos) as monto FROM promociones ORDER BY id_codigo")
        opciones = ['Agregar Promoción nueva', 'Agregar Promoción a cuenta', 'Eliminar Promoción', 'Volver al menu principal']
        for opcion in opciones:
            print("{}) {}".format(opciones.index(opcion) + 1, opcion))

        seleccion_usuario = int(input('¿Que desea hacer?: '))
        
        if seleccion_usuario < 1 or seleccion_usuario > len(opciones):
            print("Opción invalida")
        
        if(seleccion_usuario == 1 ):
            #Agregar
            nueva_promocion_nombre = input("Nombre: ")
            nueva_promcion_monto = input("Monto: ")
            nueva_promcion_fecha_vencimiento = input("Fecha (yyyy-mm-dd): ")
            nueva_promcion_descripcion = input("Descripción: ")
            nueva_promcion_usos = input("Usos: ")
            
            querry = psfunc.InsertQuerry("promociones", (["nombre", "monto", "fecha_venc", "descripcion", "usos"]), (["'" + nueva_promocion_nombre + "'", nueva_promcion_monto, "'" + nueva_promcion_fecha_vencimiento + "'", "'" + nueva_promcion_descripcion + "'", nueva_promcion_usos]))
            if(querry):
                print("!Promoción agregada!")
            else:
                print("Error agregando promoción")
            break
        elif(seleccion_usuario == 2):
            #Agregar promoción a cuenta
            psfunc.PrintQuerry("SELECT id_usuario, nombre FROM usuarios ORDER BY id_usuario")

            promocion_seleccionada = input("¿Que promocion quiere agregar a usuario?: ")
            usuario_seleccionado = input("¿Que usario?:")

            querry = psfunc.InsertQuerry("promocion_usuario", (["id_usuario", "id_codigo", "fecha_canje"]), ([usuario_seleccionado, promocion_seleccionada, "'" + datetime.today().strftime('%Y-%m-%d') + "'"]))
            if(querry):
                print("!Promoción agregada a usuario!")
            else:
                print("Error agregando promoción a usuario")

        elif(seleccion_usuario == 3):
            #Eliminar
            promocion_seleccionada = input("¿Que promocion quiere eliminar?: ")
            querry = psfunc.DeleteQuerry("promociones", "id_codigo = {}".format(promocion_seleccionada))
            if(querry):
                print("!Promoción eliminada!")
            else:
                print("Error eliminado promoción")
            break
        else:
            break
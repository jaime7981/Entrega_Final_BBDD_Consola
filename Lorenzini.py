from tabulate import tabulate
import usefullfunc as psfunc
import os

#Historial de pedido
def Historial_pedidos(login_nombre_usuario):
    id_user= psfunc.SelectQuerry(f"SELECT id_usuario FROM Usuarios WHERE email='{login_nombre_usuario}'")
    id_user= id_user[0][0] #ID del usuario
    
    menu=True
    while menu:
        print("\nHistorial de pedidos\n")
        
        headers=["ID","Dirección","# ", "Fecha","Monto"]
        sql= psfunc.PrintQuerry2(f"SELECT id_pedido, calle,numero, fecha_pedido, monto FROM (SELECT id_pedido, (monto_producto+COALESCE(monto_menu,0)) AS monto FROM (SELECT id_pedido, monto_producto, monto_menu FROM (SELECT DISTINCT  id_pedido,  (cantidad_producto*precio) AS monto_producto \
        FROM pedido_producto INNER JOIN productos \
        USING(id_producto) \
        ORDER BY id_pedido) AS t1 FULL JOIN (SELECT DISTINCT  id_pedido,  SUM((cantidad_menu*precio)) AS monto_menu \
        FROM pedido_menu INNER JOIN menues \
        USING(id_menu) \
        GROUP BY id_pedido \
        ORDER BY id_pedido) AS t2 \
        USING(id_pedido)) AS t5) AS t3 INNER JOIN (SELECT id_pedido, id_usuario, calle , numero, fecha_pedido \
        FROM Pedidos INNER JOIN Direcciones \
        USING(id_direccion)) AS t4 \
        USING(id_pedido) \
        WHERE id_usuario={id_user}",headers)
        print(sql) #Pedidos de Usuario
        
        menu_historial=["Ver pedido",
                        "Volver a Menú"] #Menu_Historial_de_pedidos
        psfunc.DisplayMenu(menu_historial)
        option_historial = psfunc.InputOpciones(menu_historial)
        
        if option_historial==1:
            whatch_order=True
            while whatch_order:
                print("Ver pedido\n")
                print(sql)
                text="Ingrese el pedido que desea ver:"
                querry=f"SELECT id_pedido FROM Pedidos WHERE id_usuario={id_user}"
                id_order= psfunc.QuerryOptionIdCheck(querry,text)
                if id_order!=0:
                    headers=["ID","Dirección","# ", "Fecha","Monto"]
                    sql_2= psfunc.PrintQuerry2(f"SELECT id_pedido, calle,numero, fecha_pedido, monto FROM (SELECT id_pedido, (monto_producto+COALESCE(monto_menu,0)) AS monto FROM (SELECT id_pedido, monto_producto, monto_menu FROM (SELECT DISTINCT  id_pedido,  (cantidad_producto*precio) AS monto_producto \
                                        FROM pedido_producto INNER JOIN productos \
                                        USING(id_producto) \
                                        ORDER BY id_pedido) AS t1 FULL JOIN (SELECT DISTINCT  id_pedido,  SUM((cantidad_menu*precio)) AS monto_menu \
                                        FROM pedido_menu INNER JOIN menues \
                                        USING(id_menu) \
                                        GROUP BY id_pedido \
                                        ORDER BY id_pedido) AS t2 \
                                        USING(id_pedido)) AS t5) AS t3 INNER JOIN (SELECT id_pedido, id_usuario, calle , numero, fecha_pedido \
                                        FROM Pedidos INNER JOIN Direcciones \
                                        USING(id_direccion)) AS t4 \
                                        USING(id_pedido) \
                                        WHERE id_usuario={id_user} AND id_pedido={id_order}",headers)
                    print(sql_2)#Informacion solo del pedido que se seleccionó
                    
                    id_check= id_order
                    querry_product= f"SELECT id_pedido FROM Pedido_producto WHERE id_pedido={id_order}"
                    querry_menu=f"SELECT id_pedido FROM Pedido_menu WHERE id_pedido={id_order}"
                    id_checkproduct= psfunc.QuerryOptionIdCheck2(querry_product,id_check)
                    id_checkmenu= psfunc.QuerryOptionIdCheck2(querry_menu,id_check)
                    
                    if id_checkproduct!=0 and id_checkmenu!=0:
                        headers_detail=["ID","Nombre", "Cantidad","Precio unitario","Descuento"]
                        
                        #Detalle del producto
                        sql_product_detail= psfunc.PrintQuerry2(f"SELECT id_pedido, nombre, cantidad_producto, precio, descuento_aplicado \
                                                        FROM Pedidos INNER JOIN (SELECT id_pedido, nombre, cantidad_producto, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos FULL JOIN (SELECT id_pedido, nombre, cantidad_producto, id_descuento, precio FROM pedido_producto INNER JOIN Productos \
                                                        USING(id_producto)\
                                                        WHERE id_pedido= {id_order}) AS t1 USING(id_descuento)\
                                                        WHERE id_pedido IS NOT null) AS t2 USING(id_pedido)\
                                                        WHERE id_usuario= {id_user}",headers_detail)
    
                        #Detalle del menu
                        sql_menu_detail= psfunc.PrintQuerry2(f"SELECT id_pedido, nombre, cantidad_menu, precio, descuento_aplicado \
                                                      FROM Pedidos INNER JOIN (SELECT id_pedido,nombre, cantidad_menu, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos JOIN (SELECT id_pedido, nombre, cantidad_menu, id_descuento, precio \
                                                      FROM pedido_menu INNER JOIN Menues \
                                                      USING(id_menu)\
                                                      WHERE id_pedido={id_order})  AS t1 USING(id_descuento)) AS t1 USING(id_pedido)\
                                                      WHERE id_usuario={id_user}",headers_detail)
                                                      
                        #Detalle del pedido
                        print("\nDetalle del pedido")
                        print("\nProductos")
                        print(sql_product_detail)
                        print("\nMenues")
                        print(sql_menu_detail)
                        
                        #Promoción aplicada
                        sql_promo= psfunc.SelectQuerry(f"SELECT DISTINCT id_usuario, id_pedido,COALESCE(nombre,'NO APLICA'), COALESCE(monto,0) FROM Pedidos \
                                                FULL JOIN (SELECT id_codigo, nombre, monto FROM Promocion_usuario INNER JOIN Promociones USING(id_codigo)) AS t1\
                                                USING(id_codigo)\
                                                WHERE id_usuario={id_user} AND id_pedido={id_order}")
                        #monto y nombre de la promoción
                        monto_promo= sql_promo[0][3]
                        nombre_promo= sql_promo[0][2]
                        
                        if monto_promo!=0:
                            #Hay promoción aplicada
                            print("\nPromoción -->",nombre_promo,"$"+str(monto_promo))
                        else:
                            #No hay promocion aplicada
                            print("\nPromoción -->",nombre_promo)
                        
                        #Valor final del pedido
                        #Solo los productos
                        tp=0
                        data1= psfunc.SelectQuerry(f"SELECT id_pedido, nombre, cantidad_producto, precio, descuento_aplicado \
                                            FROM Pedidos INNER JOIN (SELECT id_pedido, nombre, cantidad_producto, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos FULL JOIN (SELECT id_pedido, nombre, cantidad_producto, id_descuento, precio FROM pedido_producto INNER JOIN Productos \
                                            USING(id_producto)\
                                            WHERE id_pedido= {id_order}) AS t1 USING(id_descuento)\
                                            WHERE id_pedido IS NOT null) AS t2 USING(id_pedido)\
                                            WHERE id_usuario= {id_user}")
                        data2= psfunc.SelectQuerry(f"SELECT id_pedido, nombre, cantidad_menu, precio, descuento_aplicado \
                                            FROM Pedidos INNER JOIN (SELECT id_pedido,nombre, cantidad_menu, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos JOIN (SELECT id_pedido, nombre, cantidad_menu, id_descuento, precio \
                                            FROM pedido_menu INNER JOIN Menues \
                                            USING(id_menu)\
                                            WHERE id_pedido={id_order})  AS t1 USING(id_descuento)) AS t1 USING(id_pedido)\
                                            WHERE id_usuario={id_user}")
                        for a in range(len(data1)):
                            quantity_product= data1[a][2]
                            price_product= data1[a][3]
                            discount_product= data1[a][4]
                            #Total precio por la cantidad de productos pedidos
                            total_pricep= price_product*quantity_product 
                            if 0<discount_product<100: 
                                #Descuento por %
                                total_pricep_discount= total_pricep-(total_pricep*discount_product)/100
                                tp+=total_pricep_discount
                            if discount_product>100:
                                #Descuento por valor
                                total_pricep_discount= total_pricep-(quantity_product*discount_product)
                                tp+=total_pricep_discount
                            if discount_product==0:
                                #No tenga descuento
                                total_pricep_discount=total_pricep
                                tp+=total_pricep_discount
                                
                        #Solo los menues
                        tm=0
                        for b in range(len(data2)):
                            quantity_menu= data2[b][2]
                            price_menu= data2[b][3]
                            discount_menu= data2[b][4]
                            #Total precio por la cantidad de menues pedidos
                            total_pricem= price_menu*quantity_menu
                            if 0<discount_menu<100: 
                                #Descuento por %
                                total_pricem_discount= total_pricem-(total_pricem*discount_menu)/100
                                tm+=total_pricem_discount
                            if discount_menu>100:
                                #Descuento por valor
                                total_pricem_discount= total_pricem-(quantity_menu*discount_menu)
                                tm+=total_pricem_discount
                            if discount_menu==0:
                                #No tenga descuento
                                total_pricem_discount=total_pricem
                                tm+=total_pricem_discount
                        
                        #Operacion para valor final 
                        total= int(tp+tm)-monto_promo
                        print("Valor final del pedido -->","$"+str(total))
                        pass
                    
                    if id_checkproduct!=0 and id_checkmenu==0:
                        headers_detail=["ID","Nombre", "Cantidad","Precio unitario","Descuento"]
                        
                        #Detalle del producto
                        sql_product_detail= psfunc.PrintQuerry2(f"SELECT id_pedido, nombre, cantidad_producto, precio, descuento_aplicado \
                                                        FROM Pedidos INNER JOIN (SELECT id_pedido, nombre, cantidad_producto, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos FULL JOIN (SELECT id_pedido, nombre, cantidad_producto, id_descuento, precio FROM pedido_producto INNER JOIN Productos \
                                                        USING(id_producto)\
                                                        WHERE id_pedido= {id_order}) AS t1 USING(id_descuento)\
                                                        WHERE id_pedido IS NOT null) AS t2 USING(id_pedido)\
                                                        WHERE id_usuario= {id_user}",headers_detail)
                                                
                        #Detalle del pedido
                        print("\nDetalle del pedido")
                        print("\nProductos")
                        print(sql_product_detail)
                        
                        #Promoción aplicada
                        sql_promo= psfunc.SelectQuerry(f"SELECT DISTINCT id_usuario, id_pedido,COALESCE(nombre,'NO APLICA'), COALESCE(monto,0) FROM Pedidos \
                                                FULL JOIN (SELECT id_codigo, nombre, monto FROM Promocion_usuario INNER JOIN Promociones USING(id_codigo)) AS t1\
                                                USING(id_codigo)\
                                                WHERE id_usuario={id_user} AND id_pedido={id_order}")
                        #monto y nombre de la promoción
                        monto_promo= sql_promo[0][3]
                        nombre_promo= sql_promo[0][2]
                        
                        if monto_promo!=0:
                            #Hay promoción aplicada
                            print("\nPromoción -->",nombre_promo,"$"+str(monto_promo))
                        else:
                            #No hay promocion aplicada
                            print("\nPromoción -->",nombre_promo)
                        
                        #Valor final del pedido
                        #Solo los productos
                        tp=0
                        data1= psfunc.SelectQuerry(f"SELECT id_pedido, nombre, cantidad_producto, precio, descuento_aplicado \
                                            FROM Pedidos INNER JOIN (SELECT id_pedido, nombre, cantidad_producto, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos FULL JOIN (SELECT id_pedido, nombre, cantidad_producto, id_descuento, precio FROM pedido_producto INNER JOIN Productos \
                                            USING(id_producto)\
                                            WHERE id_pedido= {id_order}) AS t1 USING(id_descuento)\
                                            WHERE id_pedido IS NOT null) AS t2 USING(id_pedido)\
                                            WHERE id_usuario= {id_user}")
                        for a in range(len(data1)):
                            quantity_product= data1[a][2]
                            price_product= data1[a][3]
                            discount_product= data1[a][4]
                            #Total precio por la cantidad de productos pedidos
                            total_pricep= price_product*quantity_product 
                            if 0<discount_product<100: 
                                #Descuento por %
                                total_pricep_discount= total_pricep-(total_pricep*discount_product)/100
                                tp+=total_pricep_discount
                            if discount_product>100:
                                #Descuento por valor
                                total_pricep_discount= total_pricep-(quantity_product*discount_product)
                                tp+=total_pricep_discount
                            if discount_product==0:
                                #No tenga descuento
                                total_pricep_discount=total_pricep
                                tp+=total_pricep_discount
                                
                        #Operacion para valor final 
                        total= int(tp)-monto_promo
                        print("Valor final del pedido -->","$"+str(total))
                        pass
                    
                    if id_checkproduct==0 and id_checkmenu!=0:
                        headers_detail=["ID","Nombre", "Cantidad","Precio unitario","Descuento"]
                        
                        #Detalle del menu
                        sql_menu_detail= psfunc.PrintQuerry2(f"SELECT id_pedido, nombre, cantidad_menu, precio, descuento_aplicado \
                                                      FROM Pedidos INNER JOIN (SELECT id_pedido,nombre, cantidad_menu, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos JOIN (SELECT id_pedido, nombre, cantidad_menu, id_descuento, precio \
                                                      FROM pedido_menu INNER JOIN Menues \
                                                      USING(id_menu)\
                                                      WHERE id_pedido={id_order})  AS t1 USING(id_descuento)) AS t1 USING(id_pedido)\
                                                      WHERE id_usuario={id_user}",headers_detail)
                        
                        #Detalle del pedido
                        print("\nDetalle del pedido")
                        print("\nMenues")
                        print(sql_menu_detail)
                        
                        #Promoción aplicada
                        sql_promo= psfunc.SelectQuerry(f"SELECT DISTINCT id_usuario, id_pedido,COALESCE(nombre,'NO APLICA'), COALESCE(monto,0) FROM Pedidos \
                                                FULL JOIN (SELECT id_codigo, nombre, monto FROM Promocion_usuario INNER JOIN Promociones USING(id_codigo)) AS t1\
                                                USING(id_codigo)\
                                                WHERE id_usuario={id_user} AND id_pedido={id_order}")
                        #monto y nombre de la promoción
                        monto_promo= sql_promo[0][3]
                        nombre_promo= sql_promo[0][2]
                        
                        if monto_promo!=0:
                            #Hay promoción aplicada
                            print("\nPromoción -->",nombre_promo,"$"+str(monto_promo))
                        else:
                            #No hay promocion aplicada
                            print("\nPromoción -->",nombre_promo)
                        
                        data2= psfunc.SelectQuerry(f"SELECT id_pedido, nombre, cantidad_menu, precio, descuento_aplicado \
                                            FROM Pedidos INNER JOIN (SELECT id_pedido,nombre, cantidad_menu, precio, COALESCE(valor,0) AS descuento_aplicado FROM Descuentos JOIN (SELECT id_pedido, nombre, cantidad_menu, id_descuento, precio \
                                            FROM pedido_menu INNER JOIN Menues \
                                            USING(id_menu)\
                                            WHERE id_pedido={id_order})  AS t1 USING(id_descuento)) AS t1 USING(id_pedido)\
                                            WHERE id_usuario={id_user}")
                        tm=0
                        for b in range(len(data2)):
                            quantity_menu= data2[b][2]
                            price_menu= data2[b][3]
                            discount_menu= data2[b][4]
                            #Total precio por la cantidad de menues pedidos
                            total_pricem= price_menu*quantity_menu
                            if 0<discount_menu<100: 
                                #Descuento por %
                                total_pricem_discount= total_pricem-(total_pricem*discount_menu)/100
                                tm+=total_pricem_discount
                            if discount_menu>100:
                                #Descuento por valor
                                total_pricem_discount= total_pricem-(quantity_menu*discount_menu)
                                tm+=total_pricem_discount
                            if discount_menu==0:
                                #No tenga descuento
                                total_pricem_discount=total_pricem
                                tm+=total_pricem_discount
                        
                        #Operacion para valor final 
                        total= int(tm)-monto_promo
                        print("Valor final del pedido -->","$"+str(total))
                        pass
                        
                    else:
                        whatch_order=False
                        continue
                else:
                    continue
                break
            ##
            flag=True
            while flag:
                headers=["Pedido","Repartidor","Nombre","Teléfono","Vehículo","Patente"]
                sql_repartidor= psfunc.PrintQuerry2(f"SELECT id_pedido,id_repartidor, nombre, telefono, vehiculo, patente \
                                 FROM Pedidos INNER JOIN Repartidores \
                                 USING(id_repartidor)\
                                 WHERE id_pedido={id_order}",headers)
                nombre_repartidor= psfunc.SelectQuerry(f"SELECT nombre \
                                                FROM Pedidos INNER JOIN Repartidores \
                                                USING(id_repartidor)\
                                                WHERE id_pedido={id_order}")
                nombre_repartidor= nombre_repartidor[0][0]
                print("\nInformacion del repartidor")
                print(sql_repartidor)
                menu_dar_rating=["Dar rating",
                                 "Volver a Historial de Pedidos"]
                psfunc.DisplayMenu(menu_dar_rating)
                option = psfunc.InputOpciones(menu_dar_rating)
                if option==1:
                    print(f"\nDar rating a {nombre_repartidor} ")
                    print(sql_repartidor)
                    menu_puntuacion=["★",
                                     "★★",
                                     "★★★",
                                     "★★★★",
                                     "★★★★★",
                                     "Volver a Ver Pedido"]
                    psfunc.DisplayMenu(menu_puntuacion)
                    option_rating = psfunc.InputOpciones(menu_puntuacion)
                    
                    if option_rating==1 or option_rating==2 or option_rating==3 or option_rating==4 or option_rating==5:
                        sql_puntuacion= psfunc.SelectQuerry(f"SELECT puntuacion_repartidor \
                                                     FROM Pedidos INNER JOIN Repartidores \
                                                     USING(id_repartidor)\
                                                     WHERE id_pedido={id_order} AND puntuacion_repartidor IS null")
                        if sql_puntuacion!=[]:
                            psfunc.PrintQuerryJ(f"UPDATE Pedidos SET puntuacion={option_rating} \
                                                    WHERE id_pedido={id_order} AND puntuacion_repartidor IS NULL")
                        else:
                            print("El repartidor ya ha recibido una puntuación por parte de este usuario")
                            break
                    else:
                        continue
                    break
                
                if option==2:
                    flag=False
                    pass
                    
                else:
                    continue
                
        if option_historial==2:
            menu=False
            pass 
        
def Repartidores():
    menu=True
    while menu:
        print("\nRepartidores")
        headers= ["ID","Nombre","Patente"]
        sql= psfunc.PrintQuerry2("SELECT id_repartidor, nombre, patente \
                          FROM Repartidores \
                          ORDER BY id_repartidor",headers)
        print(sql)
        menu_repartidor=["Ver Repartidor",
                         "Agregar repartidor",
                         "Volver al Menú Principal"]
        psfunc.DisplayMenu(menu_repartidor)
        option=psfunc.InputOpciones(menu_repartidor)
        if option==1:
            text="Ingrese el ID del repartidor que desea ver:"
            querry="SELECT*FROM Repartidores"
            option_repartidor= psfunc.QuerryOptionIdCheck(querry, text)
            flag_repartidor=True
            while flag_repartidor:
                if option_repartidor!=0:
                    headers=["ID","Nombre","teléfono","vehículo","patente"]
                    sql=psfunc.PrintQuerry2(f"SELECT*FROM Repartidores WHERE id_repartidor={option_repartidor}",headers)
                    print(sql)
                    menu_ver_repartidor=["Editar Repartidor",
                                         "Eliminar repartidor",
                                         "Volver a Opciones repartidor"]
                    psfunc.DisplayMenu(menu_ver_repartidor)
                    option_ver_repartidor=psfunc.InputOpciones(menu_repartidor)
                    flag_editor=True
                    while flag_editor: 
                        if option_ver_repartidor==1:
                            print("\nEditar a repartidor")
                            print("\nSeleccione el campo que desea editar")
                            menu_editor=["Nombre",
                                         "Teléfono",
                                         "Vehículo y patente",
                                         "Editar todo",
                                         "Volver a Editar repartidor"]
                            psfunc.DisplayMenu(menu_editor)
                            option_editor=psfunc.InputOpciones(menu_editor)
                            if option_editor==1:
                                new_name=input("Ingrese el nuevo nombre del repartidor:")
                                psfunc.PrintQuerryJ(f"UPDATE Repartidores SET nombre='{new_name}' WHERE id_repartidor={option_repartidor}")
                                print("El repartidor ha sido editado exitosamente")
                                pass
                            if option_editor==2:
                                new_number=int(input("Ingrese el nuevo numero del repartidor:"))
                                psfunc.PrintQuerryJ(f"UPDATE Repartidores SET telefono={new_number} WHERE id_repartidor={option_repartidor}")
                                print("El telefono del repartidor ha sido editado exitosamente")
                                pass
                            if option_editor==3:
                                new_vehicle=input("Ingrese el nuevo vehículo del repartidor:")
                                new_patent=input("Ingrese la patente del vehículo. En el caso de ser una bicicleta precione ENTER")
                                psfunc.PrintQuerryJ(f"UPDATE Repartidores SET vehículo='{new_vehicle}, patente='{new_patent}' WHERE id_repartidor={option_repartidor}")
                                print("El vehículo y la patente han sido editados exitosamente")
                                pass
                            if option_editor==4:
                                new_name=input("Ingrese el nuevo nombre del repartidor:")
                                new_number=int(input("Ingrese el nuevo numero del repartidor:"))
                                new_vehicle=input("Ingrese el nuevo vehículo del repartidor:")
                                new_patent=input("Ingrese la patente del vehículo. En el caso de ser una bicicleta precione ENTER")
                                psfunc.PrintQuerryJ(f"UPDATE Repartidores SET nombre='{new_name}',telefono={new_number},vehiculo='{new_vehicle}', patente='{new_patent}' WHERE id_repartidor={option_repartidor}")
                                print("Los campos del repartidor han sido editados exitosamente")
                                pass
                            if option_editor==5:
                                flag_editor=False
                                break
        
                        if option_ver_repartidor==2:
                            print("\n¿Estas seguro que deseas eliminar a este repartidor?" )
                            yes_no= ["Sí, estoy seguro",
                                     "No estoy seguro"]
                            psfunc.DisplayMenu(yes_no)
                            option_delete=psfunc.InputOpciones(yes_no)
                            if option_delete==1:
                                querry=f"DELETE FROM Repartidores WHERE id_repartidor={option_repartidor}" 
                                psfunc.PrintQuerryJ(querry)
                                print("El repartidor se ha eliminado exitosamente")
                                break
                            if option_delete==2:
                                flag_editor=False
                                break
                                
    
                        if option_ver_repartidor==3:
                            flag_repartidor=False
                            break
                if option_repartidor==0:
                    flag_repartidor=False
                    break
                break
            
        if option==2:
            print("\nAgregar repartidor")
            table="Repartidores"
            new_name=input("Ingrese el nombre:")
            new_number=int(input("Ingrese el telefono:"))
            new_vehicle= input("Ingrese el tipo de vehículo (moto, motobico, bici):")
            new_patent=input("Ingrese la patente del vehículo; Si no tiene patente presione ENTER:")
            cur = psfunc.GetCon().cursor()
            insertstr = f"INSERT INTO {table}(nombre,telefono,vehiculo,patente) values('{new_name}',{new_number},'{new_vehicle}','{new_patent}')"
            cur.execute(insertstr)
            psfunc.GetCon().commit()
            print("\nRepartidor añadido con exito")
            
        if option==3:
            menu=False
            break   
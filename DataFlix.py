import psycopg2
import random
from tabulate import tabulate
import datetime
import matplotlib.pyplot as plt
import calendar 
from collections import Counter

#conn = psycopg2.connect("") Database connection
cur = conn.cursor()

def display_login_menu(): #Todas las funciones comienzan con el keyword "def" y su nombre describe lo que hacen. Cada funcion realiza una sola cosa.
    print("Bienvenido a DataFlix")
    print("(1)Iniciar sesión")
    print("(2)Crear cuenta")
    print("(3)Recuperar contraseña")
    print("(4)Salir del programa")
    try:                  #Los keyword try y except, sirven para lanzar excepciones en caso de que la línea de codigo no se ejecute correctamente.
        option = int(input("Selecciona una opción: "))
    except:
        print("Opción incorrecta")
        display_login_menu()
    if option == 1:
        login()
    elif option == 2:
        create_account()
    elif option == 3:
        retrieve_password()
    elif option == 4:
        exit()
    else:
        print("Opción incorrecta")
        display_login_menu()

def login():
    email = input("Ingrese email:")
    password = input("Ingrese contraseña:")
    cur.execute("SELECT mail, contrasena FROM usuario WHERE mail = (%s) AND contrasena = (%s)",(email,password))
    data = cur.fetchone()
    if(data == None):
        print("Datos incorrectos, ingrese nuevamente")
        display_login_menu()
    elif(email == data[0] and password == data[1]):
        print("Ingresaste a DataFlix")
        select_profile(data[0])
    else:
        display_login_menu()

def create_account():
    email = input("Ingrese email:")
    password = input("Ingrese contraseña:")
    re_password = input("Ingrese contraseña nuevamente:")
    if(password == re_password):
        nombre = input("Ingrese su nombre: ")
        apellido = input("Ingrese su apellido: ")
        usuario = random.randint(10000,9999999)
        cur.execute("INSERT INTO usuario(id_usuario,contrasena,nombre,apellido,mail) VALUES(%s,%s,%s,%s,%s)",(usuario,password,nombre,apellido,email))
        conn.commit()
        print("Cuenta creada satisfactoriamente!")
    else:
        print("Las contraseñas no son identicas, ingresa tus datos nuevamente")
        create_account()
    display_login_menu()

def retrieve_password():
    email = input("Ingrese email:")
    cur.execute("SELECT mail FROM usuario WHERE mail = (%s)",(email))
    if cur.fetchone() == None:
        print("Email incorrecto")
        display_login_menu()
    else:
        newpassword = input("Ingrese nueva contraseña:")
        cur.execute("UPDATE usuario SET contrasena=(%s) WHERE mail=(%s)",(newpassword,email))
        conn.commit()
        print("Contraseña actualizada")
    display_login_menu()

def select_profile(email):
    cur.execute("SELECT id_usuario FROM usuario WHERE mail=('{}')".format(email))
    id_usuario = cur.fetchone()
    cur.execute("SELECT nombre_perfil,id_perfil FROM perfil WHERE id_usuario = (%s)",(id_usuario))
    perfiles = cur.fetchall()
    j = 1
    for i in perfiles:
        print("({})Perfil de ".format(j),*i[0])
        j = j + 1
    try:
        option = int(input("Selecciona una opción: "))
    except:
        print("Opción incorrecta")
        select_profile(email)
    display_profile_menu(perfiles[option - 1][1])

def display_profile_menu(profile):
    print("(1)Visualizaciones")
    print("(2)Contenidos")
    print("(3)Favoritos")
    print("(4)Manejar usuario")
    print("(5)Manejar perfil")
    print("(6)Estadísticas")
    print("(7)Cerrar sesión")
    try:
        option = int(input("Selecciona una opción: "))
    except:
        print("Opción incorrecta")
        display_profile_menu(profile)
    if option == 1:
        visualizations_menu(profile)
    elif option == 2:
        contents_menu(profile)
    elif option == 3:
        favorites_menu(profile)
    elif option == 4:
        user_management_menu(profile)
    elif option == 5:
        profile_management_menu(profile)
    elif option == 7:
        display_login_menu()
    elif option == 6:
        statics_menu(profile)
    else:
        print("Opción incorrecta")
        display_profile_menu(profile)

def visualizations_menu(profile):
    print("(1)Ver visualizaciónes")
    print("(2)Agregar visualización")
    print("(3)Eliminar visualización")
    print("(4)Volver al menú principal")
    try:
        option = int(input("Selecciona una opción: "))
    except:
        print("Opción incorrecta")
        visualizations_menu(profile)
    if option == 1:
        visualization_inspect(profile)
    elif option == 2:
        add_visualization(profile)
    elif option == 3:
        delete_visualization(profile)
    elif option == 4:
        display_profile_menu(profile)
    else:
        print("Opción incorrecta")
        display_profile_menu(profile)


def visualization_inspect(profile):
    cur.execute("SELECT id_video FROM actividad WHERE id_perfil=('{}')".format(profile))
    id_videos = cur.fetchall()
    j = 1
    print("Contenidos vistos: ")
    for i in id_videos:
        cur.execute("SELECT título FROM contenido WHERE id_video=(%s)",(i))
        print("({})Título: ".format(j),*cur.fetchone())
        j = j + 1
    try:
        option = int(input("Selecciona una visualización: "))
    except:
        print("Opción incorrecta")
        visualization_inspect(profile)
    cur.execute("SELECT id_actividad FROM actividad WHERE id_video = (%s) AND id_perfil = (%s)",(id_videos[option-1],profile))
    id_actividad = cur.fetchone()
    cur.execute("SELECT fecha_reproducción,hora_inicio,hora_fin FROM actividad WHERE id_actividad= (%s)",(id_actividad))
    fechas = cur.fetchone()
    cur.execute("SELECT adelanto_inicio,adelano_fin FROM adelanto WHERE id_actividad= (%s)",(id_actividad))
    adelantos = cur.fetchone()
    cur.execute("SELECT pausa FROM pausa WHERE id_actividad= (%s)",(id_actividad))
    pausas = cur.fetchone()
    cur.execute("SELECT retroceso_inicio,retroceso_fin FROM retroceso WHERE id_actividad= (%s)",(id_actividad))
    retrocesos = cur.fetchone()
    print(tabulate([fechas] , headers=['Fecha','Hora inicio','Hora fin','Pausa'], tablefmt='fancy_grid'))
    print(tabulate([adelantos] , headers=['Adelanto inicio', 'Adelanto fin'], tablefmt='fancy_grid'))
    print(tabulate([retrocesos] , headers=['Retroceso inicio', 'Retroceso fin'], tablefmt='fancy_grid'))
    print(tabulate([pausas] , headers=['Pausa'], tablefmt='fancy_grid'))
    visualizations_menu(profile)

def add_visualization(profile):
    j = 1
    print("Contenidos disponibles: ")
    cur.execute("SELECT título FROM contenido")
    titulos = cur.fetchall()
    for i in titulos:
        print("({})Título: ".format(j),*i)
        j = j + 1
    try:
        option = int(input("Selecciona un contenido: "))
    except:
        print("Opción incorrecta")
        add_visualization(profile)
    cur.execute("SELECT count(*) AS count FROM actividad")
    actividad_counter = cur.fetchone()[0] + 1
    print(actividad_counter)
    cur.execute("SELECT id_video FROM contenido WHERE título = (%s)",(titulos[option-1]))
    id_video = cur.fetchone()[0]
    try:
        year = int(input('Ingresa un año:'))
        month = int(input('Ingresa un mes:'))
        day = int(input('Ingresa un día:'))
        hora_inicio = int(input('Ingresa hora inicio:'))
        hora_fin = int(input('Ingresa hora fin:'))
        date = datetime.date(year, month, day)
        time1 = datetime.time(hora_inicio)
        time2 = datetime.time(hora_fin)
    except:
        print('Datos erroneos, ingresa nuevamente.')
        add_visualization(profile)
    cur.execute("INSERT INTO actividad(id_actividad,id_perfil,id_video,fecha_reproducción,hora_inicio,hora_fin) VALUES(%s,%s,%s,%s,%s,%s)",(actividad_counter,profile,id_video,date,time1,time2))
    conn.commit()
    print("Actividad agregada")
    visualizations_menu(profile)

def delete_visualization(profile):
    cur.execute("SELECT id_video FROM actividad WHERE id_perfil=('{}')".format(profile))
    id_videos = cur.fetchall()
    j = 1
    print("Contenidos vistos: ")
    for i in id_videos:
        cur.execute("SELECT título FROM contenido WHERE id_video=(%s)",(i))
        print("({})Título: ".format(j),*cur.fetchone())
        j = j + 1
    try:
        option = int(input("Selecciona una visualización a eliminar: "))
    except:
        print("Opción incorrecta")
        delete_visualization(profile)
    cur.execute("SELECT id_actividad FROM actividad WHERE id_video = (%s) AND id_perfil = (%s)",(id_videos[option-1],profile))
    id_actividad = cur.fetchone()
    try:
        cur.execute("DELETE FROM actividad WHERE id_actividad = (%s)",(id_actividad))
        conn.commit()
    except:
        print("Contenido eliminado")
    visualizations_menu(profile)

def contents_menu(profile):
    print("(1)Agregar contenido")
    print("(2)Editar contenido")
    print("(3)Eliminar contenido")
    print("(4)Volver al menú principal")
    try:
        option = int(input("Selecciona una opción: "))
    except:
        print("Opción incorrecta")
        contents_menu(profile)
    if option == 1:
        add_content(profile)
    elif option == 2:
        edit_content(profile)
    elif option == 3:
        delete_content(profile)
    elif option == 4:
        display_profile_menu(profile)
    else:
        print("Opción incorrecta")
        display_profile_menu(profile)

def add_content(profile):
    cur.execute("SELECT count(*) AS count FROM contenido")
    content_counter = cur.fetchone()[0] + 1
    print("Agregar:")
    print("(1)Serie")
    print("(2)Pelicula")
    print("(3)Documental")
    try:
        option = int(input("Selecciona una opción: "))
    except:
        print("Opción incorrecta")
        add_content(profile)
    cur.execute("SELECT nombre FROM director")
    directores = cur.fetchall()
    j = 1
    for i in directores:
        print("({})".format(j),*i)
        j = j + 1
    try:
        option1 = int(input("Seleccione director: "))
    except:
        print("Opción incorrecta")
        add_content(profile)
    cur.execute("SELECT id_director FROM director WHERE nombre = (%s)",(directores[option1-1]))
    id_director = cur.fetchone()[0]
    if option == 1:
        try:
            temporada = int(input("Número temporada: "))
            capitulo = int(input("Número capitulo: "))
            duracion = int(input("Duración: "))
            titulo = input("Título: ")
            id_area = option
            cur.execute("INSERT INTO contenido(id_video,id_director,id_area,duracion,temporada,numero_capítulo,título) VALUES(%s,%s,%s,%s,%s,%s,%s)",(content_counter,id_director,id_area,duracion,temporada,capitulo,titulo))
            conn.commit()
            print("Contenido agregado")
        except:
            print("Datos incorrectos. Ingrese nuevamente")
            add_content(profile)
    elif option == 2:
        try:
            temporada = 0
            capitulo = 0
            duracion = int(input("Duración: "))
            titulo = input("Título: ")
            id_area = option
            cur.execute("INSERT INTO contenido(id_video,id_director,id_area,duracion,temporada,numero_capítulo,título) VALUES(%s,%s,%s,%s,%s,%s,%s)",(content_counter,director,id_area,duracion,temporada,capitulo,titulo))
            conn.commit()
            print("Contenido agregado")
        except:
            print("Datos incorrectos. Ingrese nuevamente")
            add_content(profile)
    elif option == 3:
        try:
            temporada = 0
            capitulo = 0
            duracion = int(input("Duración: "))
            titulo = input("Título: ")
            id_area = option
            cur.execute("INSERT INTO contenido(id_video,id_director,id_area,duracion,temporada,numero_capítulo,título) VALUES(%s,%s,%s,%s,%s,%s,%s)",(content_counter,director,id_area,duracion,temporada,capitulo,titulo))
            conn.commit()
            print("Contenido agregado")
        except:
            print("Datos incorrectos. Ingrese nuevamente")
            add_content(profile)
    contents_menu(profile)

def edit_content(profile):
    j = 1
    print("Contenidos disponibles: ")
    cur.execute("SELECT título FROM contenido")
    titulos = cur.fetchall()
    for i in titulos:
        print("({})Título: ".format(j),*i)
        j = j + 1
    try:
        option = int(input("Seleccione para editar: "))
    except:
        print("Opción incorrecta")
    cur.execute("SELECT id_area FROM contenido WHERE título = (%s)",(titulos[option-1]))
    area = cur.fetchone()[0]
    cur.execute("SELECT id_video FROM contenido WHERE título = (%s)",(titulos[option-1]))
    id_video = cur.fetchone()[0]
    if area == 1:
        try:
            temporada = int(input("Número temporada: "))
            capitulo = int(input("Número capitulo: "))
            duracion = int(input("Duración: "))
            titulo = input("Título: ")
            cur.execute("UPDATE contenido SET duracion=(%s),temporada=(%s),numero_capítulo=(%s),título=(%s) WHERE id_video=(%s)",(duracion,temporada,capitulo,titulo,id_video))
            conn.commit()
        except:
            print("Datos incorrectos. Ingrese nuevamente")
            add_content(profile)
    else:
        try:
            duracion = int(input("Duración: "))
            titulo = input("Título: ")
            cur.execute("UPDATE contenido SET duracion=(%s),título=(%s) WHERE id_video=(%s)",(duracion,titulo,id_video))
            conn.commit()
        except:
            print("Datos incorrectos. Ingrese nuevamente")
            add_content(profile)
    contents_menu(profile)

def delete_content(profile):
    j = 1
    print("Contenidos disponibles: ")
    cur.execute("SELECT título FROM contenido")
    titulos = cur.fetchall()
    for i in titulos:
        print("({})Título: ".format(j),*i)
        j = j + 1
    try:
        option = int(input("Contenido a eliminar: "))
    except:
        print("Opción incorrecta")
        delete_content(profile)
    cur.execute("SELECT id_video FROM contenido WHERE título = (%s)",(titulos[option-1]))
    id_video = cur.fetchone()
    confirm = int(input("Seguro que desea eliminar (1)SI (2)NO"))
    if(confirm == 1):
        try:
            cur.execute("DELETE FROM contenido WHERE id_video = (%s)",(id_video))
            conn.commit()
            print("Contenido eliminado")
        except:
            print("Error")
            delete_content(profile)
    else:
        delete_content(profile)
    contents_menu(profile)

def favorites_menu(profile):
    cur.execute("SELECT id_lista_fav FROM lista_favoritos ORDER BY id_lista_fav DESC LIMIT 1")
    favoritos_counter = cur.fetchone()[0] + 1
    j = 1
    cur.execute("SELECT id_video FROM lista_favoritos WHERE id_perfil=('{}')".format(profile))
    favoritos = cur.fetchall()
    print("Favoritos: ")
    if(favoritos != None):
        for i in favoritos:
            cur.execute("SELECT título FROM contenido WHERE id_video = ('{}')".format(i[0]))
            print("({})Título: ".format(j),*cur.fetchone())
            j = j + 1
    else:
        print("El perfil no tiene favoritos.")
    print("  ")
    print("  ")
    print("(1)Agregar favorito")
    print("(2)Eliminar favorito")
    print("(3)Volver al menú principal")
    try:
        option = int(input("Selecciona una opción: "))
    except:
        print("Opción incorrecta")
        favorites_menu(profile)
    if option == 1:
        print("Contenidos disponibles:")
        cur.execute("SELECT título FROM contenido")
        titulos = cur.fetchall()
        for i in titulos:
            print("({})Título: ".format(j),*i)
            j = j + 1
        try:
            option = int(input("Selecciona un título: "))
        except:
            print("Opción incorrecta")
        cur.execute("SELECT id_video FROM contenido WHERE título = (%s)",(titulos[option-1]))
        id_video = cur.fetchone()[0]
        cur.execute("INSERT INTO lista_favoritos(id_lista_fav,id_perfil,id_video) VALUES(%s,%s,%s)",(favoritos_counter,profile,id_video))
        conn.commit()
        print("Favorito agregado!")
        favorites_menu(profile)
    elif option == 2:
        try:
            option2 = int(input("Selecciona un título a eliminar: "))
        except:
            print("Opción incorrecta")
        cur.execute("DELETE FROM lista_favoritos WHERE id_perfil = (%s) AND id_video = (%s)",(profile,favoritos[option2-1]))
        conn.commit()
        print("Eliminado satisfactoriamente")
        favorites_menu(profile)
    else:
        display_profile_menu(profile)



def user_management_menu(profile):
    print("(1)Editar información de pago")
    print("(2)Cambiar tipo de subscripción")
    print("(3)Editar información de usuario")
    print("(4)Eliminar usuario")
    print("(5)Volver al menú principal")
    try:
        option = int(input("Selecciona una opción: "))
    except:
        print("Opción incorrecta")
        user_management_menu(profile)
    if option == 1:
        edit_payment_options(profile)
    elif option == 2:
        edit_subscription_type(profile)
    elif option == 3:
        edit_user_info(profile)
    elif option == 4:
        delete_user(profile)
    elif option == 5:
        display_profile_menu(profile)

def edit_payment_options(profile):
    cur.execute("SELECT id_usuario FROM perfil WHERE id_perfil=('{}')".format(profile))
    id_usuario = cur.fetchone()[0]
    cur.execute("SELECT numero_tarjeta,fecha_vencimiento,codigo_seguridad FROM info_pago WHERE id_usuario=('{}')".format(id_usuario))
    info_pago = cur.fetchone()
    print(tabulate([info_pago] , headers=['Numero tarjeta','Fecha vencimiento','Codigo seguridad'], tablefmt='fancy_grid'))
    option = int(input("(1)Cambiar información de pago (2)Volver al menú manejo usuario: "))
    if option == 1:
        try:
            numero_tarjeta = int(input("Ingrese nuevo número de la tarjeta: "))
            año_vencimiento = int(input("Ingrese año vencimiento: "))
            mes_vencimiento = int(input("Ingrese mes vencimiento: "))
            dia_vencimiento = int(input("Ingrese dia vencimiento: "))
            codigo_seguridad = int(input("Ingrese codigo de seguridad: "))
            fecha_vencimiento = datetime.date(año_vencimiento,mes_vencimiento,dia_vencimiento)
        except:
            print("Datos incorrectos. Ingrese nuevamente")
            edit_payment_options(profile)
        cur.execute("UPDATE info_pago SET numero_tarjeta=(%s),fecha_vencimiento=(%s),codigo_seguridad=(%s) WHERE id_usuario=(%s)",(numero_tarjeta,fecha_vencimiento,codigo_seguridad,id_usuario))
        conn.commit()
        edit_payment_options(profile)
    else:
        user_management_menu(profile)
def edit_subscription_type(profile):
    cur.execute("SELECT id_usuario FROM perfil WHERE id_perfil=('{}')".format(profile))
    id_usuario = cur.fetchone()[0]
    cur.execute("SELECT tipo_suscripcion,cantidad_disponible,calidad_video,fecha_inicio,fecha_fin FROM suscripcion WHERE id_usuario=('{}')".format(id_usuario))
    suscripcion = cur.fetchone()
    print("Suscripcion actual: ")
    print(tabulate([suscripcion] , headers=['Tipo suscripcion','Cantidad de perfiles disponibles','Calidad video','Fecha inicio','Fecha termino'], tablefmt='fancy_grid'))
    print("Suscripciones disponibles: ")
    print(tabulate([['Estandar','2','480p'],['Premium','4','1080p']], headers=['Tipo suscripcion', 'Cantidad de perfiles disponibles','Calidad de video'],tablefmt='fancy_grid'))
    option = int(input("(1)Para cambiar suscripcion   (2)Volver al menú de usuario: "))
    if option == 1:
        option1 = int(input("(1)Estandar   (2)Premium"))
        if option1 == 1:
            cur.execute("UPDATE suscripcion SET tipo_suscripcion=(%s),cantidad_disponible=(%s),calidad_video=(%s) WHERE id_usuario=(%s)",('Estandar','2','Baja',id_usuario))
            conn.commit()
            print('Suscripcion actualizada!')
            edit_subscription_type(profile)
        else:
            cur.execute("UPDATE suscripcion SET tipo_suscripcion=(%s),cantidad_disponible=(%s),calidad_video=(%s) WHERE id_usuario=(%s)",('Premium','4','HD',id_usuario))
            conn.commit()
            print('Suscripcion actualizada!')
            edit_subscription_type(profile)
    else:
        user_management_menu(profile)
    
def edit_user_info(profile):
    cur.execute("SELECT id_usuario FROM perfil WHERE id_perfil=('{}')".format(profile))
    id_usuario = cur.fetchone()[0]
    cur.execute("SELECT nombre,apellido,mail,calle,numero,ciudad,telefono FROM usuario,direccion,telefono_usuario WHERE usuario.id_usuario=('{}')".format(id_usuario))
    print(tabulate([cur.fetchone()] , headers=['Nombre','Apellido','mail','Dirección','Número','Ciudad','Telefono'], tablefmt='fancy_grid'))
    option = int(input("(1) Cambiar nombre,apellido y correo (2) Cambiar calle, número y ciudad (3)Cambiar telefono (4)Volver al menú:  "))
    if option == 1:
        nombre = input("Ingrese nombre: ")
        apellido = input("Ingrese apellido: ")
        correo = input("Ingrese email: ")
        cur.execute("UPDATE usuario SET nombre=(%s),apellido=(%s),mail=(%s) WHERE id_usuario=(%s)",(nombre,apellido,correo,id_usuario))
        conn.commit()
        print("Datos actualizados")
        edit_user_info(profile)
    elif option == 2:
        calle = input("Ingrese calle: ")
        numero = int(input("Ingrese numero: "))
        ciudad = input("Ingrese ciudad: ")
        cur.execute("UPDATE direccion SET calle=(%s),numero=(%s),ciudad=(%s) WHERE id_usuario=(%s)",(calle,numero,ciudad,id_usuario))
        conn.commit()
        print("Datos actualizados")
        edit_user_info(profile)
    elif option == 3:
        telefono = int(input("Ingrese nombre: "))
        cur.execute("UPDATE telefono_usuario SET telefono=(%s) WHERE id_usuario=(%s)",(telefono,id_usuario))
        conn.commit()
        print("Datos actualizados")
        edit_user_info(profile)
    else:
        user_management_menu(profile)

def delete_user(profile):
    confirm = int(input("Seguro que desea eliminar este usuario?   (1)SI   (2) NO:   "))
    if confirm == 1:
        cur.execute("SELECT id_usuario FROM perfil WHERE id_perfil=('{}')".format(profile))
        id_usuario = cur.fetchone()[0]
        cur.execute("SELECT id_perfil FROM perfil WHERE id_usuario=('{}')".format(id_usuario))
        id_perfil = cur.fetchall()
        for j in id_perfil:
            cur.execute("SELECT id_actividad FROM actividad WHERE id_perfil=('{}')".format(*j))
            id_actividad = cur.fetchall()
            for i in id_actividad:
                cur.execute("DELETE FROM adelanto WHERE id_actividad = ('{}')".format(*i))
                conn.commit()
                cur.execute("DELETE FROM retroceso WHERE id_actividad = ('{}')".format(*i))
                conn.commit()
                cur.execute("DELETE FROM pausa WHERE id_actividad = ('{}')".format(*i))
                conn.commit()
                cur.execute("DELETE FROM actividad WHERE id_actividad = ('{}')".format(*i))
                conn.commit()
        cur.execute("DELETE FROM direccion WHERE id_usuario = ('{}')".format(id_usuario))
        conn.commit()
        cur.execute("DELETE FROM telefono_usuario WHERE id_usuario = ('{}')".format(id_usuario))
        conn.commit()
        cur.execute("DELETE FROM usuario WHERE id_usuario = ('{}')".format(id_usuario))
        conn.commit()
        print("Usuario eliminado.")
        display_login_menu()
    else:
        user_management_menu(profile)

def profile_management_menu(profile):
    print("(1)Cambiar de perfil")
    print("(2)Agregar perfil")
    print("(3)Editar perfil")
    print("(4)Eliminar perfil")
    print("(5)Volver al menú principal")
    try:
        option = int(input("Selecciona una opción: "))
    except:
        print("Opción incorrecta")
        profile_management_menu(profile)
    if option == 1:
        cur.execute("SELECT id_usuario FROM perfil WHERE id_perfil=('{}')".format(profile))
        id_usuario = cur.fetchone()[0]
        cur.execute("SELECT mail FROM usuario WHERE id_usuario=('{}')".format(id_usuario))
        email = cur.fetchone()[0]
        select_profile(email)
    elif option == 2:
        add_profile(profile)
    elif option == 3:
        edit_profile(profile)
    elif option == 4:
        delete_profile(profile)
    elif option == 5:
        display_profile_menu(profile)

def add_profile(profile):
    cur.execute("SELECT id_usuario FROM perfil WHERE id_perfil=('{}')".format(profile))
    id_usuario = cur.fetchone()[0]
    cur.execute("SELECT id_perfil FROM perfil ORDER BY id_perfil DESC LIMIT 1")
    id_perfil = cur.fetchone()[0] + 1
    name = input("Ingrese nombre para el perfil: ")
    cur.execute("INSERT INTO perfil(id_perfil,nombre_perfil,id_usuario) VALUES(%s,%s,%s)",(id_perfil,name,id_usuario))
    conn.commit()
    print("Perfil agregado.")
    cur.execute("SELECT id_usuario FROM perfil WHERE id_perfil=('{}')".format(profile))
    id_usuario = cur.fetchone()[0]
    cur.execute("SELECT mail FROM usuario WHERE id_usuario=('{}')".format(id_usuario))
    email = cur.fetchone()[0]
    select_profile(email)  

def edit_profile(profile):
    name = input("Ingrese nuevo nombre para el perfil: ")
    cur.execute("UPDATE perfil SET nombre_perfil=(%s) WHERE id_perfil=(%s)",(name,profile))
    conn.commit()
    cur.execute("SELECT id_usuario FROM perfil WHERE id_perfil=('{}')".format(profile))
    id_usuario = cur.fetchone()[0]
    cur.execute("SELECT mail FROM usuario WHERE id_usuario=('{}')".format(id_usuario))
    email = cur.fetchone()[0]
    select_profile(email)   

def delete_profile(profile):
    confirm = int(input("Seguro que desea eliminar este perfil?   (1)SI   (2) NO:   "))
    if confirm == 1:
        cur.execute("SELECT id_actividad FROM actividad WHERE id_perfil=('{}')".format(profile))
        id_actividad = cur.fetchall()
        for i in id_actividad:
            cur.execute("DELETE FROM adelanto WHERE id_actividad = ('{}')".format(*i))
            conn.commit()
            cur.execute("DELETE FROM retroceso WHERE id_actividad = ('{}')".format(*i))
            conn.commit()
            cur.execute("DELETE FROM pausa WHERE id_actividad = ('{}')".format(*i))
            conn.commit()
            cur.execute("DELETE FROM actividad WHERE id_actividad = ('{}')".format(*i))
            conn.commit()
        cur.execute("DELETE FROM lista_favoritos WHERE id_perfil = ('{}')".format(profile))
        cur.execute("DELETE FROM perfil WHERE id_perfil = ('{}')".format(profile))
        conn.commit()
        print("Perfil eliminado")
        display_login_menu()
    else:
        profile_management_menu(profile)

def statics_menu(profile):
    print("(1)Tipos de contenido favorito")
    print("(2)Cantidad de visualizaciones")
    print("(3)Categorías")
    print("(4)Incompletos")
    print("(5)Volver al menú principal")
    try:
        option = int(input("Selecciona una opción: "))
    except:
        print("Opción incorrecta")
        statics_menu(profile)
    if option == 1:
        favorites_statics(profile)
    elif option == 2:
        views_statics(profile)
    elif option == 3:
        category_statics(profile)
    elif option == 4:
        incomplete_statics(profile)
    elif option == 5:
        display_profile_menu(profile)

def favorites_statics(profile):
    cur.execute("select id_video from lista_favoritos")
    id_videos = cur.fetchall()
    area = []
    for i in id_videos:
        cur.execute("select nombre from area inner join contenido on area.id_area = contenido.id_area WHERE id_video = {}".format(*i))
        area.append(cur.fetchone())
    plt.title('Cantidad de favoritos según tipo')
    plt.hist(area, alpha=1, edgecolor = 'black',  linewidth=1, histtype='barstacked')
    plt.grid(True)
    plt.show()
    plt.clf()
    statics_menu(profile)

def views_statics(profile):
    reproductions_by_month = []
    cur.execute("SELECT id_usuario FROM perfil WHERE id_perfil=('{}')".format(profile))
    id_usuario = cur.fetchone()[0]
    cur.execute("select EXTRACT(MONTH FROM fecha_reproducción) from actividad inner join perfil on actividad.id_perfil = perfil.id_perfil WHERE perfil.id_usuario = ({})".format(id_usuario))
    id_actividad = cur.fetchall()
    for i in id_actividad:
        reproductions_by_month.append(calendar.month_name[int(*i)])
    N = Counter(reproductions_by_month)
    k = list(N.keys())
    v = list(N.values())
    plt.plot(k,v)
    plt.show()
    statics_menu(profile)

def category_statics(profile):
    categorias = []
    cur.execute("select nombre from categoria inner join clasificacion on clasificacion.id_categoria = categoria.id_categoria")
    for i in cur.fetchall():
        categorias.append(*i)
    N = Counter(categorias)
    k = list(N.keys())
    v = list(N.values())
    plt.barh(k, v, align='center', alpha=0.9)
    plt.ylabel('Categoria')
    plt.title('Cantidad de contenido por categoría')
    plt.show()
    statics_menu(profile)

def incomplete_statics(profile):
    diff = []
    cur.execute("SELECT DATE_PART('hour', hora_fin - hora_inicio) * 60 + DATE_PART('minute', hora_fin - hora_inicio),duracion,título FROM actividad,contenido WHERE actividad.id_video = contenido.id_video")
    for i in cur.fetchall():
        if int(round(i[0])) < int(i[1]) and int(round(i[0])) > 0:
            diff.append(i[2])
    N = Counter(diff).most_common(10)
    k = []
    v = []
    for i in N:
        k.append(i[0])
        v.append(i[1])
    plt.barh(k, v, align='center', alpha=0.9, color='orange')
    plt.ylabel('Título')
    plt.title('Películas incompletas más comunes')
    plt.show()
    statics_menu(profile)

def main():
    display_login_menu()

if __name__ == "__main__":
    main()
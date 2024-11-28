import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from modulos.usuarios import agregar_usuario, listar_usuarios, eliminar_usuario, actualizar_usuario
from modulos.libros import agregar_libro, listar_libros, actualizar_libro, eliminar_libro
from modulos.prestamos import reporte_morosos_promedio, calcular_multa_por_retraso, obtener_usuarios_morosos, modificar_cuota
from modulos.busqueda import buscar_libros_por_titulo, buscar_libros_por_autor, buscar_usuarios_por_id, buscar_usuarios_por_nombre

def iniciar_interfaz():
    ventana = tk.Tk()
    ventana.title("Sistema de Biblioteca")
    ventana.geometry("300x300")

    # Gestionar usuarios
    boton_agregar = tk.Button(ventana, text="Gestionar Usuarios", command=gestion_usuarios_interfaz)
    boton_agregar.pack(pady=10)

    #Gestionar libros
    boton_gestionar = tk.Button(ventana, text="Gestionar Libros", command=gestionar_libros_interfaz)
    boton_gestionar.pack(pady=10)

    # Gestionar prestamos
    boton_gestionar_prestamos = tk.Button(ventana, text="Gestionar Préstamos", command=manejo_prestamos_interfaz)
    boton_gestionar_prestamos.pack(pady=10)

    # Gestionar Búsqueda y Filtrado 
    boton_gestionar_prestamos = tk.Button(ventana, text="Búsqueda y filtrado", command=busqueda_filtrado_interfaz)
    boton_gestionar_prestamos.pack(pady=10)

    # Botón para abrir el reporte de morosos
    btn_reporte_morosos = tk.Button(ventana, text="Reporte de Morosos", command=reporte_morosos_interfaz)
    btn_reporte_morosos.pack(pady=10)

    # Botón para abrir la ventana de modificación de cuota
    btn_modificar_cuota = tk.Button(ventana, text="Modificar Cuota", command=generar_multa_interfaz)
    btn_modificar_cuota.pack(pady=10)

    ventana.mainloop()




def gestion_usuarios_interfaz():
    # Crear la ventana de gestión de usuarios
    ventana_gestion = tk.Toplevel()
    ventana_gestion.title("Gestión de Usuarios")
    ventana_gestion.geometry("800x500")

    # Etiqueta principal
    lbl_titulo = tk.Label(
        ventana_gestion, 
        text="Gestión de Usuarios", 
        font=("Arial", 16, "bold"), 
    )
    lbl_titulo.pack(pady=10)

    # Botón para agregar usuarios
    btn_agregar = tk.Button(
        ventana_gestion, 
        text="Agregar Usuario", 
        font=("Arial", 12), 
        width=20,
        command=agregar_usuario_interfaz # Debes tener esta función definida
    )
    btn_agregar.pack(pady=5)

    # Botón para listar usuarios
    btn_listar = tk.Button(
        ventana_gestion, 
        text="Ver Usuarios", 
        font=("Arial", 12), 
        width=20,
        command=listar_usuarios_interfaz  # Debes tener esta función definida
    )
    btn_listar.pack(pady=5)

    # Botón para actualizar usuarios
    btn_actualizar = tk.Button(
        ventana_gestion, 
        text="Actualizar Usuario", 
        font=("Arial", 12), 
        width=20,
        command=actualizar_usuarios_interfaz  # Debes tener esta función definida
    )
    btn_actualizar.pack(pady=5)

    # Botón para eliminar usuarios
    btn_eliminar = tk.Button(
        ventana_gestion, 
        text="Eliminar Usuario", 
        font=("Arial", 12),
        width=20,
        command=eliminar_usuarios_interfaz  # Debes tener esta función definida
    )
    btn_eliminar.pack(pady=5)

    # Botón para cerrar la ventana
    btn_cerrar = tk.Button(
        ventana_gestion, 
        text="Cerrar", 
        font=("Arial", 12), 
        width=20, 
        command=ventana_gestion.destroy
    )
    btn_cerrar.pack(pady=10)

def agregar_usuario_interfaz():
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Usuario")
    ventana_agregar.geometry("300x300")

    tk.Label(ventana_agregar, text="Nombre").pack(pady=5)
    entrada_nombre = tk.Entry(ventana_agregar)
    entrada_nombre.pack()

    tk.Label(ventana_agregar, text="Apellido").pack(pady=5)
    entrada_apellido = tk.Entry(ventana_agregar)
    entrada_apellido.pack()

    tk.Label(ventana_agregar, text="Email").pack(pady=5)
    entrada_email = tk.Entry(ventana_agregar)
    entrada_email.pack()

    tk.Label(ventana_agregar, text="Teléfono").pack(pady=5)
    entrada_telefono = tk.Entry(ventana_agregar)
    entrada_telefono.pack()

    def guardar_usuario():
        nombre = entrada_nombre.get()
        apellido = entrada_apellido.get()
        email = entrada_email.get()
        telefono = entrada_telefono.get()
        
        if nombre and apellido and email and telefono:
            agregar_usuario(nombre, apellido, email, int(telefono))
            tk.Label(ventana_agregar, text="Usuario agregado exitosamente", fg="green").pack()
            ventana_agregar.destroy()
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios y el teléfono debe ser numérico.")

    tk.Button(ventana_agregar, text="Agregar", command=guardar_usuario).pack(pady=10)

def listar_usuarios_interfaz():
    ventana_listar = tk.Toplevel()
    ventana_listar.title("Listar Usuarios")
    ventana_listar.geometry("1200x600")

    columnas = ("ID", "Nombre", "Apellido", "Email", "Teléfono", "Fecha Registro")
    treeview = ttk.Treeview(ventana_listar, columns=columnas, show="headings")
    for col in columnas:
        treeview.heading(col, text=col)
        treeview.column(col, width=120)

    # Cargar usuarios desde la base de datos
    usuarios = listar_usuarios()
    for usuario in usuarios:
        treeview.insert("", "end", values=(usuario["usuario_id"], usuario["nombre"], usuario["apellido"],
                                           usuario["email"], usuario["telefono"], usuario["fecha_registro"]))

    treeview.pack(fill="both", expand=True)

def actualizar_usuarios_interfaz():
    # Crear ventana para seleccionar usuario a actualizar
    ventana_actualizar = tk.Toplevel()
    ventana_actualizar.title("Actualizar Usuario")
    ventana_actualizar.geometry("400x300")

    # Campo para buscar usuario por email
    tk.Label(ventana_actualizar, text="Email del Usuario a Actualizar").pack(pady=5)
    entrada_email = tk.Entry(ventana_actualizar, width=30)
    entrada_email.pack(pady=5)

    # Campos para nuevos datos
    tk.Label(ventana_actualizar, text="Nuevo Nombre").pack(pady=5)
    entrada_nuevo_nombre = tk.Entry(ventana_actualizar, width=30)
    entrada_nuevo_nombre.pack(pady=5)

    tk.Label(ventana_actualizar, text="Nuevo Apellido").pack(pady=5)
    entrada_nuevo_apellido = tk.Entry(ventana_actualizar, width=30)
    entrada_nuevo_apellido.pack(pady=5)

    tk.Label(ventana_actualizar, text="Nuevo Teléfono").pack(pady=5)
    entrada_nuevo_telefono = tk.Entry(ventana_actualizar, width=30)
    entrada_nuevo_telefono.pack(pady=5)

    def confirmar_actualizacion():
        email = entrada_email.get()
        nuevo_nombre = entrada_nuevo_nombre.get()
        nuevo_apellido = entrada_nuevo_apellido.get()
        nuevo_telefono = entrada_nuevo_telefono.get()

        if email and nuevo_nombre and nuevo_apellido and nuevo_telefono:
            try:
                actualizar_usuario(email, nuevo_nombre, nuevo_apellido, int(nuevo_telefono))
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                ventana_actualizar.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Todos los campos son obligatorios")

    tk.Button(ventana_actualizar, text="Actualizar", command=confirmar_actualizacion).pack(pady=10)

def eliminar_usuarios_interfaz():
    # Crear ventana para eliminar usuario
    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar Usuario")
    ventana_eliminar.geometry("300x200")

    # Campo para introducir email del usuario a eliminar
    tk.Label(ventana_eliminar, text="Email del Usuario a Eliminar").pack(pady=5)
    entrada_email = tk.Entry(ventana_eliminar, width=30)
    entrada_email.pack(pady=5)

    def confirmar_eliminacion():
        email = entrada_email.get()

        if email:
            respuesta = messagebox.askyesno("Confirmación", "¿Está seguro de eliminar este usuario?")
            
            if respuesta:
                try:
                    eliminar_usuario(email)
                    messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                    ventana_eliminar.destroy()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Debe introducir un email")

    tk.Button(ventana_eliminar, text="Eliminar", command=confirmar_eliminacion).pack(pady=10)

def gestionar_libros_interfaz():
    ventana_libros = tk.Toplevel()
    ventana_libros.title("Gestionar Libros")
    ventana_libros.geometry("400x500")

    tk.Label(ventana_libros, text="Gestionar Libros", font=("Arial", 14)).pack(pady=10)

    tk.Button(ventana_libros, text="Agregar Libro", command=agregar_libro_interfaz).pack(pady=5)
    tk.Button(ventana_libros, text="Listar Libros", command=listar_libros_interfaz).pack(pady=5)
    tk.Button(ventana_libros, text="Buscar Libro", command=actualizar_libro_interfaz).pack(pady=5)
    tk.Button(ventana_libros, text="Eliminar Libro", command=eliminar_libro_interfaz).pack(pady=5)

def agregar_libro_interfaz():
    ventana_agregar_libro = tk.Toplevel()
    ventana_agregar_libro.title("Agregar Libro")
    ventana_agregar_libro.geometry("400x800")

    tk.Label(ventana_agregar_libro, text="Título").pack(pady=5)
    entrada_titulo = tk.Entry(ventana_agregar_libro)
    entrada_titulo.pack()

    tk.Label(ventana_agregar_libro, text="Autor").pack(pady=5)
    entrada_autor = tk.Entry(ventana_agregar_libro)
    entrada_autor.pack()

    tk.Label(ventana_agregar_libro, text="Editorial").pack(pady=5)
    entrada_editorial = tk.Entry(ventana_agregar_libro)
    entrada_editorial.pack()

    tk.Label(ventana_agregar_libro, text="ISBN").pack(pady=5)
    entrada_isbn = tk.Entry(ventana_agregar_libro)
    entrada_isbn.pack()

    tk.Label(ventana_agregar_libro, text="Fecha de publicacion").pack(pady=5)
    entrada_fecha = tk.Entry(ventana_agregar_libro)
    entrada_fecha.pack()

    tk.Label(ventana_agregar_libro, text="Cantidad Disponible").pack(pady=5)
    entrada_disponible = tk.Entry(ventana_agregar_libro)
    entrada_disponible.pack()

    #Boton de guardar libros
    def guardar_libro():
        titulo = entrada_titulo.get()
        autor = entrada_autor.get()
        editorial = entrada_editorial.get()
        isbn = entrada_isbn.get()
        anio_publicacion = entrada_fecha.get()
        cantidad_disponible = entrada_disponible.get()

        if titulo and autor and editorial and isbn and anio_publicacion and cantidad_disponible:
            agregar_libro(titulo, autor, editorial, isbn, int(anio_publicacion), int(cantidad_disponible))
            tk.Label(ventana_agregar_libro, text="Libro agregado exitosamente", fg="green").pack()
            ventana_agregar_libro.destroy()
        else:
            tk.Label(ventana_agregar_libro, text="Todos los campos son obligatorios", fg="red").pack()

    tk.Button(ventana_agregar_libro, text="Guardar", command=guardar_libro).pack(pady=10)

def listar_libros_interfaz():
    ventana_listar = tk.Toplevel()
    ventana_listar.title("Listar Libros")
    ventana_listar.geometry("800x400")

    columnas = ("ID", "Título", "Autor", "Editorial", "ISBN", "Año de Lazanmiento", "Cantidad Disponible")
    treeview = ttk.Treeview(ventana_listar, columns=columnas, show="headings")
    for col in columnas:
        treeview.heading(col, text=col)
        treeview.column(col, width=120)

    libros = listar_libros()
    for libro in libros:
        treeview.insert("", "end", values=(libro["libro_id"], libro["titulo"], libro["autor"],
                                           libro["editorial"], libro["isbn"], libro["anio_publicacion"],
                                           libro["cantidad_disponible"]
        ))
    treeview.pack(fill="both", expand=True)
        
def actualizar_libro_interfaz():
    ventana_actualizar = tk.Toplevel()
    ventana_actualizar.title("Actualizar Libro")
    ventana_actualizar.geometry("900x800")

    tk.Label(ventana_actualizar, text="Selecciona el libro a actualizar", font=("Arial", 12)).pack(pady=10)

    columnas = ("ID", "Titulo", "Autor", "ISBN", "Año de Lazanmiento", "Cantidad Disponible")
    treeview = ttk.Treeview(ventana_actualizar, columns=columnas, show="headings")

    for col in columnas:
        treeview.heading(col, text=col)
        treeview.column(col, width=120)
    treeview.pack(fill="both", expand=True, pady=10)

    libros = listar_libros()
    for libro in libros:
        treeview.insert("", "end", values=(libro["libro_id"], libro["titulo"], libro["autor"], libro["isbn"], libro["anio_publicacion"], libro["cantidad_disponible"]))

    #Campos para actulizar la información de los libros 
    tk.Label(ventana_actualizar, text="Nuevo Titulo").pack(pady=5)
    entrada_nuevo_titulo = tk.Entry(ventana_actualizar)
    entrada_nuevo_titulo.pack()

    tk.Label(ventana_actualizar, text="Nuevo Autor").pack(pady=5)
    entrada_nuevo_autor = tk.Entry(ventana_actualizar)
    entrada_nuevo_autor.pack()

    tk.Label(ventana_actualizar, text="Nuevo ISBN").pack(pady=5)
    entrada_nuevo_isbn = tk.Entry(ventana_actualizar)
    entrada_nuevo_isbn.pack()

    tk.Label(ventana_actualizar, text="Nueva editorial").pack(pady=5)
    entrada_nueva_editorial = tk.Entry(ventana_actualizar)
    entrada_nueva_editorial.pack()

    tk.Label(ventana_actualizar, text="Nueva año de publicacion").pack(pady=5)
    entrada_nueva_fecha = tk.Entry(ventana_actualizar)
    entrada_nueva_fecha.pack()

    tk.Label(ventana_actualizar, text="Nueva cantidad disponible").pack(pady=5)
    entrada_nueva_disponible = tk.Entry(ventana_actualizar)
    entrada_nueva_disponible.pack()

    def guardar_cambios():
        seleccionar_item = treeview.selection()
        if not seleccionar_item:
            tk.Label(ventana_actualizar, text="Selecciona un libro para actualizar", fg="red").pack()
            return
    
        libro_id = treeview.item(seleccionar_item[0], "values")[0]
        titulo = entrada_nuevo_titulo.get()
        autor = entrada_nuevo_autor.get()
        isbn = entrada_nuevo_isbn.get()
        editorial = entrada_nueva_editorial.get()
        anio = entrada_nueva_fecha.get()
        cantidad = entrada_nueva_disponible.get()

        
        if titulo and autor and cantidad.isdigit():
            actualizar_libro(int(libro_id), titulo, autor, isbn, editorial, int(anio), int(cantidad))
            tk.Label(ventana_actualizar, text="Libro actualizado exitosamente", fg="green").pack()
            ventana_actualizar.destroy()
        else:
            tk.Label(ventana_actualizar, text="Todos los campos son obligatorios y válidos", fg="red").pack()

    tk.Button(ventana_actualizar, text="Guardar Cambios", command=guardar_cambios).pack(pady=10)

def eliminar_libro_interfaz():
    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar libro")
    ventana_eliminar.geometry("600x600")

    tk.Label(ventana_eliminar, text="Selecciona el libro a eliminar", font=("Arial", 12)).pack(pady=10)

    columnas = ("ID", "Titulo", "Autor", "ISBN")
    treeview = ttk.Treeview(ventana_eliminar, columns=columnas, show="headings")
    for col in columnas:
        treeview.heading(col, text=col)
        treeview.column(col, width=120)
    treeview.pack(fill="both", expand=True, pady=10)

    libros = listar_libros()
    for libro in libros:
        treeview.insert("", "end", values=(libro["libro_id"], libro["titulo"], libro["autor"], libro["isbn"]))

    def eliminar_libro_seleccionado():
        selected_item = treeview.selection()
        if not selected_item:
            tk.Label(ventana_eliminar, text="Selecciona un libro para eliminar!", fg="red").pack()
            return
        
        libro_id = treeview.item(selected_item[0], "values")[0]
        eliminar_libro(int(libro_id))
        tk.Label(ventana_eliminar, text="Libro eliminado exitosa", fg="green").pack()

        treeview.delete(selected_item[0])

    tk.Button(ventana_eliminar, text="Eliminar", command=eliminar_libro_seleccionado).pack()         



def manejo_prestamos_interfaz():
    # Crear ventana de Manejo de Préstamos
    ventana_prestamos = tk.Toplevel()
    ventana_prestamos.title("Manejo de Préstamos")
    ventana_prestamos.geometry("500x600")

    # Etiqueta y entrada para el nombre del usuario
    lbl_nombre = tk.Label(ventana_prestamos, text="Nombre del Usuario:", font=("Arial", 12))
    lbl_nombre.pack(pady=10)
    entry_nombre = tk.Entry(ventana_prestamos, font=("Arial", 12))
    entry_nombre.pack(pady=10)

    # Etiqueta y entrada para el apellido del usuario
    lbl_apellido = tk.Label(ventana_prestamos, text="Apellido del Usuario:", font=("Arial", 12))
    lbl_apellido.pack(pady=10)
    entry_apellido = tk.Entry(ventana_prestamos, font=("Arial", 12))
    entry_apellido.pack(pady=10)

    # Etiqueta y entrada para la fecha de devolución
    lbl_fecha_devolucion = tk.Label(ventana_prestamos, text="Fecha de Devolución (YYYY-MM-DD):", font=("Arial", 12))
    lbl_fecha_devolucion.pack(pady=10)
    entry_fecha_devolucion = tk.Entry(ventana_prestamos, font=("Arial", 12))
    entry_fecha_devolucion.pack(pady=10)

    # Etiqueta y entrada para la cuota mensual
    lbl_cuota_mensual = tk.Label(ventana_prestamos, text="Cuota Mensual (en dinero):", font=("Arial", 12))
    lbl_cuota_mensual.pack(pady=10)
    entry_cuota_mensual = tk.Entry(ventana_prestamos, font=("Arial", 12))
    entry_cuota_mensual.pack(pady=10)

    # Función para calcular la multa
    def calcular_multa():
        try:
            # Obtener los datos de los campos de entrada
            nombre = entry_nombre.get().strip()
            apellido = entry_apellido.get().strip()
            fecha_devolucion_str = entry_fecha_devolucion.get()
            cuota_mensual = float(entry_cuota_mensual.get())

            if not nombre or not apellido:
                messagebox.showerror("Error", "Por favor, ingrese tanto el nombre como el apellido del usuario.")
                return

            # Buscar el usuario por nombre y apellido por separado
            usuario = buscar_usuarios_por_nombre(nombre)  # Solo buscamos el nombre
            if apellido:
                usuario = [u for u in usuario if apellido.lower() in u['apellido'].lower()]  # Filtrar por apellido

            if usuario:
                # Convertir la fecha de devolución a formato datetime
                fecha_devolucion = datetime.strptime(fecha_devolucion_str, "%Y-%m-%d")

                # Obtener la fecha actual
                fecha_actual = datetime.now()

                # Calcular los días de retraso
                dias_retraso = (fecha_actual - fecha_devolucion).days

                if dias_retraso > 0:
                    # Calcular la multa (3% de la cuota mensual por cada día de retraso)
                    multa = dias_retraso * cuota_mensual * 0.03
                    mensaje = f"Multa por retraso: ${multa:.2f} por {dias_retraso} días de retraso."
                    messagebox.showinfo("Cálculo de Multa", mensaje)
                else:
                    messagebox.showinfo("Sin Multa", "El préstamo no tiene retraso.")
            else:
                messagebox.showerror("Usuario no encontrado", "No se encontró un usuario con ese nombre y apellido.")

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese los datos correctamente.")


    # Botón para calcular la multa
    btn_calcular_multa = tk.Button(ventana_prestamos, text="Calcular Multa", font=("Arial", 12), command=calcular_multa)
    btn_calcular_multa.pack(pady=20)

    # Botón para cerrar la ventana
    btn_cerrar = tk.Button(ventana_prestamos, text="Cerrar", font=("Arial", 12), command=ventana_prestamos.destroy)
    btn_cerrar.pack()

def busqueda_filtrado_interfaz():
    # Crear ventana de Búsqueda y Filtrado
    ventana_busqueda = tk.Toplevel()
    ventana_busqueda.title("Búsqueda y Filtrado")
    ventana_busqueda.geometry("500x400")

    # Etiqueta y entrada para el texto de búsqueda
    lbl_busqueda = tk.Label(ventana_busqueda, text="Ingrese el texto de búsqueda:", font=("Arial", 12))
    lbl_busqueda.pack(pady=10)
    entry_busqueda = tk.Entry(ventana_busqueda, font=("Arial", 12))
    entry_busqueda.pack(pady=10)

    # Opción para seleccionar el tipo de búsqueda
    lbl_tipo_busqueda = tk.Label(ventana_busqueda, text="Seleccione tipo de búsqueda:", font=("Arial", 12))
    lbl_tipo_busqueda.pack(pady=10)

    opciones_busqueda = ["Buscar libro por título", "Buscar libro por autor", "Buscar usuario por ID", "Buscar usuario por nombre"]
    tipo_busqueda_var = tk.StringVar()
    tipo_busqueda_var.set(opciones_busqueda[0])  # Establecer opción por defecto

    dropdown_busqueda = tk.OptionMenu(ventana_busqueda, tipo_busqueda_var, *opciones_busqueda)
    dropdown_busqueda.pack(pady=10)

    # Función para realizar la búsqueda y mostrar resultados
    def realizar_busqueda():
        # Obtener el texto de búsqueda y el tipo de búsqueda seleccionado
        termino_busqueda = entry_busqueda.get().strip()  # Limpiamos los espacios antes y después
        tipo_busqueda = tipo_busqueda_var.get()

        if not termino_busqueda:
            messagebox.showerror("Error", "Por favor ingrese un texto para buscar.")
            return
        
        # Realizar la búsqueda según el tipo seleccionado
        if tipo_busqueda == "Buscar libro por título":
            resultados = buscar_libros_por_titulo(termino_busqueda)
        elif tipo_busqueda == "Buscar libro por autor":
            resultados = buscar_libros_por_autor(termino_busqueda)
        elif tipo_busqueda == "Buscar usuario por ID":
            resultados = buscar_usuarios_por_id(termino_busqueda)
        elif tipo_busqueda == "Buscar usuario por nombre":
            resultados = buscar_usuarios_por_nombre(termino_busqueda)
        
        # Mostrar los resultados
        if resultados:
            mostrar_resultados(resultados, tipo_busqueda)
        else:
            messagebox.showinfo("Sin resultados", "No se encontraron resultados para la búsqueda.")

    # Botón para realizar la búsqueda
    btn_buscar = tk.Button(ventana_busqueda, text="Buscar", font=("Arial", 12), command=realizar_busqueda)
    btn_buscar.pack(pady=20)

    # Función para mostrar los resultados en una nueva ventana
    def mostrar_resultados(resultados, tipo_busqueda):
        ventana_resultados = tk.Toplevel(ventana_busqueda)
        ventana_resultados.title("Resultados de Búsqueda")

        # Crear el Treeview para mostrar los resultados en formato de tabla
        if tipo_busqueda.startswith("Buscar libro"):
            # Para libros
            treeview = ttk.Treeview(ventana_resultados, columns=("ID", "Título", "Autor", "ISBN"), show="headings")
            treeview.heading("ID", text="ID Libro")
            treeview.heading("Título", text="Título")
            treeview.heading("Autor", text="Autor")
            treeview.heading("ISBN", text="ISBN")
            treeview.column("ID", width=80, anchor="center")
            treeview.column("Título", width=200, anchor="center")
            treeview.column("Autor", width=150, anchor="center")
            treeview.column("ISBN", width=150, anchor="center")

            # Insertar los resultados de los libros
            for resultado in resultados:
                treeview.insert("", tk.END, values=(resultado.get('libro_id', 'N/A'),
                                                    resultado.get('titulo', 'N/A'),
                                                    resultado.get('autor', 'N/A'),
                                                    resultado.get('isbn', 'N/A')))
        
        elif tipo_busqueda.startswith("Buscar usuario"):
            # Para usuarios
            treeview = ttk.Treeview(ventana_resultados, columns=("ID", "Nombre", "Apellido", "Email"), show="headings")
            treeview.heading("ID", text="ID Usuario")
            treeview.heading("Nombre", text="Nombre")
            treeview.heading("Apellido", text="Apellido")
            treeview.heading("Email", text="Email")
            treeview.column("ID", width=80, anchor="center")
            treeview.column("Nombre", width=150, anchor="center")
            treeview.column("Apellido", width=150, anchor="center")
            treeview.column("Email", width=200, anchor="center")

            # Insertar los resultados de los usuarios
            for resultado in resultados:
                treeview.insert("", tk.END, values=(resultado.get('usuario_id', 'N/A'),
                                                    resultado.get('nombre', 'N/A'),
                                                    resultado.get('apellido', 'N/A'),
                                                    resultado.get('email', 'N/A')))
        
        treeview.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Botón para cerrar la ventana
    btn_cerrar = tk.Button(ventana_busqueda, text="Cerrar", font=("Arial", 12), command=ventana_busqueda.destroy)
    btn_cerrar.pack(pady=10)




def reporte_morosos_interfaz():
    # Crear ventana de reporte de morosos
    ventana_reporte = tk.Toplevel()
    ventana_reporte.title("Reporte de Morosos")
    ventana_reporte.geometry("600x400")

    # Etiqueta de título
    lbl_titulo = tk.Label(ventana_reporte, text="Reporte de Socios Morosos", font=("Arial", 14))
    lbl_titulo.pack(pady=10)

    # Función para mostrar el reporte
    def mostrar_reporte():
        morosos = reporte_morosos_promedio()  # Obtener los datos de los morosos
        if not morosos:
            messagebox.showinfo("Sin resultados", "No hay usuarios morosos en este momento.")
        else:
            # Crear una ventana para mostrar los resultados
            ventana_resultados = tk.Toplevel(ventana_reporte)
            ventana_resultados.title("Resultados del Reporte")

            # Crear el Treeview para mostrar los morosos en filas y columnas
            tree = ttk.Treeview(ventana_resultados, columns=("ID", "Nombre", "Apellido", "Promedio Meses Atrasado"), show="headings")
            tree.pack(fill=tk.BOTH, expand=True)

            # Configurar las columnas del Treeview
            tree.heading("ID", text="ID")
            tree.heading("Nombre", text="Nombre")
            tree.heading("Apellido", text="Apellido")
            tree.heading("Promedio Meses Atrasado", text="Promedio Meses Atrasado")

            # Ajustar el tamaño de las columnas
            tree.column("ID", width=50, anchor=tk.CENTER)
            tree.column("Nombre", width=150, anchor=tk.W)
            tree.column("Apellido", width=150, anchor=tk.W)
            tree.column("Promedio Meses Atrasado", width=200, anchor=tk.CENTER)

            # Insertar los datos de los morosos en el Treeview
            for moroso in morosos:
                tree.insert("", tk.END, values=(moroso["usuario_id"], moroso["nombre"], moroso["apellido"], f"{moroso['promedio_meses_pendientes']:.2f}"))

            # Agregar un scrollbar vertical al Treeview
            scrollbar = ttk.Scrollbar(ventana_resultados, orient="vertical", command=tree.yview)
            tree.config(yscrollcommand=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Botón para mostrar el reporte
    btn_mostrar_reporte = tk.Button(ventana_reporte, text="Mostrar Reporte", font=("Arial", 12), command=mostrar_reporte)
    btn_mostrar_reporte.pack(pady=20)

    # Botón para cerrar la ventana de reporte
    btn_cerrar = tk.Button(ventana_reporte, text="Cerrar", font=("Arial", 12), command=ventana_reporte.destroy)
    btn_cerrar.pack(pady=10)



def generar_multa_interfaz():
    # Crear ventana para generar multa
    ventana_multa = tk.Toplevel()
    ventana_multa.title("Generar Multa por Retraso")
    ventana_multa.geometry("700x500")

    # Etiqueta y entrada para el ID del préstamo
    lbl_prestamo_id = tk.Label(ventana_multa, text="ID del Préstamo:", font=("Arial", 12))
    lbl_prestamo_id.pack(pady=5)
    entry_prestamo_id = tk.Entry(ventana_multa, font=("Arial", 12))
    entry_prestamo_id.pack(pady=5)

    # Función para calcular y mostrar la multa
    def calcular_multa_gui():
        prestamo_id = entry_prestamo_id.get()

        if not prestamo_id:
            messagebox.showerror("Error", "Por favor ingrese el ID del préstamo.")
            return

        # Llamar a la función para calcular la multa
        multa = calcular_multa_por_retraso(int(prestamo_id))

        if multa is not None:
            messagebox.showinfo("Multa Generada", f"Multa generada: ${multa:.2f}")
        else:
            messagebox.showinfo("Sin Retraso", "No hay retraso en la devolución del libro.")

    # Botón para generar la multa
    btn_generar_multa = tk.Button(ventana_multa, text="Generar Multa", font=("Arial", 12), command=calcular_multa_gui)
    btn_generar_multa.pack(pady=20)

    # Función para mostrar los usuarios morosos en una tabla (Treeview)
    def mostrar_morosos():
        usuarios_morosos = obtener_usuarios_morosos()

        # Crear un contenedor para la tabla (Treeview)
        frame_morosos = tk.Frame(ventana_multa)
        frame_morosos.pack(pady=10, fill=tk.BOTH, expand=True)

        # Crear Treeview para mostrar los morosos en forma de tabla
        treeview = ttk.Treeview(frame_morosos, columns=("ID", "Nombre", "Apellido", "Cuotas Pendientes", "Monto Pendiente"), show="headings", selectmode="extended")
        treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Configurar las columnas
        treeview.heading("ID", text="ID Usuario")
        treeview.heading("Nombre", text="Nombre")
        treeview.heading("Apellido", text="Apellido")
        treeview.heading("Cuotas Pendientes", text="Cuotas Pendientes")
        treeview.heading("Monto Pendiente", text="Monto Pendiente")

        # Configurar el ancho de las columnas
        treeview.column("ID", width=80, anchor="center")
        treeview.column("Nombre", width=150, anchor="center")
        treeview.column("Apellido", width=150, anchor="center")
        treeview.column("Cuotas Pendientes", width=150, anchor="center")
        treeview.column("Monto Pendiente", width=150, anchor="center")

        # Agregar los usuarios morosos a la tabla
        if usuarios_morosos:
            for usuario in usuarios_morosos:
                treeview.insert("", tk.END, values=(usuario['usuario_id'], usuario['nombre'], usuario['apellido'], usuario['cuotas_pendientes'], f"${usuario['monto_pendiente']:.2f}"))
        else:
            messagebox.showinfo("Sin resultados", "No hay usuarios morosos.")

        # Crear scrollbar para el Treeview
        scrollbar = tk.Scrollbar(frame_morosos, orient="vertical", command=treeview.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        treeview.configure(yscrollcommand=scrollbar.set)

        return treeview

    # Llamar a la función para mostrar los morosos al abrir la ventana
    treeview_morosos = mostrar_morosos()

    # Etiquetas y entradas para modificar la cuota
    lbl_mes = tk.Label(ventana_multa, text="Mes de la cuota a modificar:", font=("Arial", 12))
    lbl_mes.pack(pady=5)
    entry_mes = tk.Entry(ventana_multa, font=("Arial", 12))
    entry_mes.pack(pady=5)

    lbl_ano = tk.Label(ventana_multa, text="Año de la cuota a modificar:", font=("Arial", 12))
    lbl_ano.pack(pady=5)
    entry_ano = tk.Entry(ventana_multa, font=("Arial", 12))
    entry_ano.pack(pady=5)

    lbl_nueva_cuota = tk.Label(ventana_multa, text="Nueva cuota:", font=("Arial", 12))
    lbl_nueva_cuota.pack(pady=5)
    entry_nueva_cuota = tk.Entry(ventana_multa, font=("Arial", 12))
    entry_nueva_cuota.pack(pady=5)

    # Función para modificar la cuota
    def modificar_cuota_gui():
        mes = entry_mes.get()
        ano = entry_ano.get()
        nueva_cuota = entry_nueva_cuota.get()

        # Validación de entradas
        if not mes or not ano or not nueva_cuota:
            messagebox.showerror("Error", "Por favor complete todos los campos.")
            return

        try:
            mes = int(mes)
            ano = int(ano)
            nueva_cuota = float(nueva_cuota)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores válidos.")
            return

        # Obtener los usuarios seleccionados
        seleccionados = treeview_morosos.selection()
        if not seleccionados:
            messagebox.showerror("Error", "Por favor seleccione al menos un usuario.")
            return

        # Modificar la cuota de los usuarios seleccionados
        for item in seleccionados:
            usuario_id = treeview_morosos.item(item, "values")[0]  # Obtener ID del usuario
            exito = modificar_cuota(int(usuario_id), mes, ano, nueva_cuota)  # Función para modificar cuota de usuario

            if exito:
                messagebox.showinfo("Cuota modificada", f"Cuota modificada para el usuario {usuario_id}.")
            else:
                messagebox.showerror("Error", f"No se pudo modificar la cuota para el usuario {usuario_id}.")

    # Botón para modificar la cuota
    btn_modificar_cuota = tk.Button(ventana_multa, text="Modificar Cuota", font=("Arial", 12), command=modificar_cuota_gui)
    btn_modificar_cuota.pack(pady=20)

    # Botón para cerrar la ventana
    btn_cerrar = tk.Button(ventana_multa, text="Cerrar", font=("Arial", 12), command=ventana_multa.destroy)
    btn_cerrar.pack(pady=10)


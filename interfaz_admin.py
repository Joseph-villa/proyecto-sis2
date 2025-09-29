import tkinter as tk
from tkinter import ttk, messagebox
from admisiones_manager import AdmisionesManager

def crear_formulario(parent, campos, bg="white"):
    form_frame = tk.Frame(parent, bg=bg)
    entries = {}
    for i, campo in enumerate(campos):
        label = campo[0]
        tipo = campo[1]
        kwargs = campo[2] if len(campo) > 2 else {}
        ttk.Label(form_frame, text=label).grid(row=i, column=0, sticky="e", padx=10, pady=5)
        if tipo == "entry":
            entry = ttk.Entry(form_frame, width=30, **kwargs)
            entry.grid(row=i, column=1, sticky="ew", padx=10)
            entries[label.lower().replace(" ", "_")] = entry
        elif tipo == "combobox":
            values = kwargs.get("values", [])
            combobox = ttk.Combobox(form_frame, values=values, width=27, state="readonly")
            combobox.grid(row=i, column=1, sticky="ew", padx=10)
            entries[label.lower().replace(" ", "_")] = combobox
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=2)
    return form_frame, entries

def crear_boton(parent, texto, comando, bg="white", width=20):
    return tk.Button(
        parent,
        text=texto,
        font=("Arial", 10),
        bg=bg,
        fg="black",
        relief="raised",
        width=width,
        command=comando
    )

def ajustar_columnas_tabla(tabla, ancho_ventana):
    num_columnas = len(tabla["columns"])
    ancho_columna = max(80, (ancho_ventana - 40) // num_columnas)
    for col in tabla["columns"]:
        tabla.column(col, width=ancho_columna, anchor="center")

def lanzar_admin(root):
    def mostrar_login():
        login_window = tk.Toplevel(root)
        login_window.title("Inicio de Sesión - Administrador")
        login_window.configure(bg="white")
        login_window.resizable(False, False)

        window_width, window_height = 400, 300
        screen_width = login_window.winfo_screenwidth()
        screen_height = login_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        tk.Label(login_window, text="Inicio de Sesión", font=("Arial", 16, "bold"), bg="white").pack(pady=20)
        form_frame, entries = crear_formulario(login_window, [
            ("Usuario", "entry"),
            ("Contraseña", "entry", {"show": "*"})
        ])
        form_frame.pack(pady=5)

        def verificar():
            usuario = entries["usuario"].get().strip()
            contraseña = entries["contraseña"].get().strip()
            if not usuario or not contraseña:
                messagebox.showwarning("Error", "Por favor, ingrese usuario y contraseña.")
                return
            try:
                manager = AdmisionesManager()
                exito, mensaje = manager.verificar_admin(usuario, contraseña)
                if exito:
                    login_window.destroy()
                    mostrar_panel(manager)
                else:
                    messagebox.showwarning("Error", mensaje)
            except Exception as e:
                messagebox.showerror("Error", f"Error al verificar credenciales: {str(e)}")

        crear_boton(login_window, "Iniciar Sesión", verificar).pack(pady=20)

    def mostrar_panel(manager):
        app = tk.Tk()
        app.title("Sistema de Admisión - Administrador")
        app.configure(bg="white")
        window_width, window_height = 1000, 800
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        app.geometry(f"{window_width}x{window_height}+{x}+{y}")
        app.resizable(True, True)

        main_frame = tk.Frame(app, bg="white")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(main_frame, text="Panel de Administrador", font=("Arial", 18, "bold"), bg="white", fg="black").pack(pady=20)
        tk.Label(
            main_frame,
            text="Publica resultados, edita datos de postulantes o visualiza la lista de postulantes.",
            font=("Arial", 10),
            bg="white",
            fg="grey",
            wraplength=600,
            justify="center"
        ).pack(pady=10)

        card_frame = tk.Frame(main_frame, bg="white", relief="raised", borderwidth=2)
        card_frame.pack(pady=20, padx=20, fill="both", expand=True)

        notebook = ttk.Notebook(card_frame)
        notebook.pack(expand=True, fill="both", padx=15, pady=15)

        frame_resultado = tk.Frame(notebook, bg="white")
        notebook.add(frame_resultado, text="Publicar Resultado")
        tk.Label(frame_resultado, text="📊", font=("Arial", 24), bg="white", fg="grey").pack(pady=10)
        tk.Label(frame_resultado, text="Publicar Resultado", font=("Arial", 14, "bold"), bg="white", fg="black").pack()
        tk.Label(frame_resultado, text="Ingresa el CI y la nota del postulante.", font=("Arial", 9), bg="white", fg="grey", wraplength=500).pack(pady=5)

        form_resultado, entries_resultado = crear_formulario(frame_resultado, [
            ("CI", "entry"),
            ("Nota", "entry")
        ])
        form_resultado.pack(pady=15, padx=20)

        def publicar():
            ci = entries_resultado["ci"].get().strip()
            try:
                nota = float(entries_resultado["nota"].get())
            except ValueError:
                messagebox.showwarning("Error", "Nota inválida.")
                return
            try:
                exito, mensaje = manager.publicar_resultado(ci, nota)
                messagebox.showinfo("Resultado", mensaje) if exito else messagebox.showerror("Error", mensaje)
                if exito:
                    entries_resultado["ci"].delete(0, tk.END)
                    entries_resultado["nota"].delete(0, tk.END)
                    cargar_postulantes()
            except Exception as e:
                messagebox.showerror("Error", f"Error al publicar resultado: {str(e)}")

        crear_boton(form_resultado, "Publicar", publicar).grid(row=2, column=0, columnspan=2, pady=15)

        frame_editar = tk.Frame(notebook, bg="white")
        notebook.add(frame_editar, text="Editar Datos")
        tk.Label(frame_editar, text="✏️", font=("Arial", 24), bg="white", fg="grey").pack(pady=10)
        tk.Label(frame_editar, text="Editar Datos de Postulante", font=("Arial", 14, "bold"), bg="white", fg="black").pack()
        tk.Label(frame_editar, text="Modifica los datos de un postulante por su CI.", font=("Arial", 9), bg="white", fg="grey", wraplength=500).pack(pady=5)

        facultades = ["Ciencias Agrícolas", "Arquitectura", "Bioquímica y Farmacia", "Ciencias Económicas", "Derecho", "Humanidades", "Medicina", "Odontología", "Ciencias y Tecnología"]
        modalidades = ["Examen de Admisión", "Curso Preuniversitario", "Excelencia Académica"]
        form_editar, entries_editar = crear_formulario(frame_editar, [
            ("CI", "entry"),
            ("Campo", "combobox", {"values": ["nombre", "apellido_paterno", "apellido_materno", "fecha_nacimiento", "telefono", "email", "direccion", "facultad", "modalidad"]}),
            ("Nuevo Valor", "entry"),
            ("Facultades Disponibles", "combobox", {"values": facultades}),
            ("Modalidades Disponibles", "combobox", {"values": modalidades})
        ])
        form_editar.pack(pady=15, padx=20)

        def editar():
            ci = entries_editar["ci"].get().strip()
            campo = entries_editar["campo"].get()
            nuevo_valor = entries_editar["facultades_disponibles"].get() if campo == "facultad" else entries_editar["modalidades_disponibles"].get() if campo == "modalidad" else entries_editar["nuevo_valor"].get().strip()
            if not ci or not campo or not nuevo_valor:
                messagebox.showwarning("Error", "Todos los campos son obligatorios.")
                return
            try:
                exito, mensaje = manager.editar_dato(ci, campo, nuevo_valor)
                messagebox.showinfo("Edición", mensaje) if exito else messagebox.showerror("Error", mensaje)
                if exito:
                    entries_editar["ci"].delete(0, tk.END)
                    entries_editar["campo"].set("")
                    entries_editar["nuevo_valor"].delete(0, tk.END)
                    entries_editar["facultades_disponibles"].set("")
                    entries_editar["modalidades_disponibles"].set("")
                    cargar_postulantes()
            except Exception as e:
                messagebox.showerror("Error", f"Error al editar dato: {str(e)}")

        crear_boton(form_editar, "Editar", editar).grid(row=5, column=0, columnspan=2, pady=15)

        frame_tabla = tk.Frame(notebook, bg="white")
        notebook.add(frame_tabla, text="Ver Postulantes")
        tk.Label(frame_tabla, text="📋", font=("Arial", 24), bg="white", fg="grey").pack(pady=10)
        tk.Label(frame_tabla, text="Lista de Postulantes", font=("Arial", 14, "bold"), bg="white", fg="black").pack()
        tk.Label(frame_tabla, text="Visualiza todos los postulantes registrados.", font=("Arial", 9), bg="white", fg="grey", wraplength=500).pack(pady=5)

        tabla = ttk.Treeview(frame_tabla, columns=("CI", "Nombre", "Apellido Paterno", "Apellido Materno", "Fecha Nacimiento", "Teléfono", "Email", "Dirección", "Facultad", "Modalidad", "Estado", "Nota", "Pagó"), show="headings")
        for col in tabla["columns"]:
            tabla.heading(col, text=col)
        tabla.pack(expand=True, fill="both", padx=10, pady=10)

        ajustar_columnas_tabla(tabla, 1000)

        def on_resize(event):
            ajustar_columnas_tabla(tabla, event.width)

        app.bind("<Configure>", on_resize)

        def cargar_postulantes():
            try:
                tabla.delete(*tabla.get_children())
                exito, resultado = manager.listar_postulantes()
                if exito:
                    for fila in resultado:
                        tabla.insert("", "end", values=fila)
                    messagebox.showinfo("Actualización", f"Tabla actualizada. {len(resultado)} postulantes cargados.")
                else:
                    messagebox.showerror("Error", resultado)
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar postulantes: {str(e)}")

        crear_boton(frame_tabla, "Actualizar tabla", cargar_postulantes).pack(pady=10)

        def eliminar_seleccionado():
            selected_item = tabla.selection()
            if not selected_item:
                messagebox.showwarning("Error", "Seleccione un postulante para eliminar.")
                return
            ci = tabla.item(selected_item)['values'][0]
            if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el postulante con CI {ci}?"):
                try:
                    exito, mensaje = manager.eliminar_postulante(ci)
                    messagebox.showinfo("Eliminación", mensaje) if exito else messagebox.showerror("Error", mensaje)
                    if exito:
                        cargar_postulantes()
                except Exception as e:
                    messagebox.showerror("Error", f"Error al eliminar postulante: {str(e)}")

        crear_boton(frame_tabla, "Eliminar Seleccionado", eliminar_seleccionado).pack(pady=10)

        def volver():
            try:
                app.destroy()
                root.deiconify()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cerrar la ventana: {str(e)}")

        crear_boton(main_frame, "Volver", volver).pack(pady=10)

        cargar_postulantes()
        app.mainloop()

    mostrar_login()





import tkinter as tk
from tkinter import ttk, messagebox
from admisiones_manager import AdmisionesManager
from postulante import Postulante
from pago import Pago

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
            entries[label.lower().replace(" ", "_").replace("(", "").replace(")", "")] = entry
        elif tipo == "combobox":
            values = kwargs.get("values", [])
            combobox = ttk.Combobox(form_frame, values=values, width=27, state="readonly")
            combobox.grid(row=i, column=1, sticky="ew", padx=10)
            entries[label.lower().replace(" ", "_").replace("(", "").replace(")", "")] = combobox
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

def lanzar_postulante(root):
    try:
        manager = AdmisionesManager()
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectar con la base de datos: {str(e)}")
        root.deiconify()
        return

    app = tk.Tk()
    app.title("Sistema de Admisión - Postulante")
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

    volver_frame = tk.Frame(main_frame, bg="white")
    volver_frame.pack(side=tk.TOP, anchor="nw", pady=10)

    def volver():
        try:
            app.destroy()
            root.deiconify()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cerrar la ventana: {str(e)}")

    crear_boton(volver_frame, "Volver", volver).pack(side=tk.LEFT, padx=10)

    tk.Label(main_frame, text="Panel de Postulante", font=("Arial", 18, "bold"), bg="white", fg="black").pack(pady=20)
    tk.Label(
        main_frame,
        text="Registra tus datos, realiza pagos o consulta tu estado de admisión.",
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

    frame_registro = tk.Frame(notebook, bg="white")
    notebook.add(frame_registro, text="Registro")
    tk.Label(frame_registro, text="📝", font=("Arial", 24), bg="white", fg="grey").pack(pady=10)
    tk.Label(frame_registro, text="Registro de Postulante", font=("Arial", 14, "bold"), bg="white", fg="black").pack()
    tk.Label(frame_registro, text="Ingresa tus datos personales para registrarte.", font=("Arial", 9), bg="white", fg="grey", wraplength=500).pack(pady=5)

    facultades = ["Ciencias Agrícolas", "Arquitectura", "Bioquímica y Farmacia", "Ciencias Económicas", "Derecho", "Humanidades", "Medicina", "Odontología", "Tecnología"]
    modalidades = ["Examen de Admisión", "Curso Preuniversitario", "Excelencia Académica"]
    form_registro, entries_registro = crear_formulario(frame_registro, [
        ("CI", "entry"),
        ("Nombre", "entry"),
        ("Apellido Paterno", "entry"),
        ("Apellido Materno", "entry"),
        ("Fecha de Nacimiento (DD/MM/AAAA)", "entry"),
        ("Teléfono", "entry"),
        ("Email", "entry"),
        ("Dirección", "entry"),
        ("Facultad", "combobox", {"values": facultades}),
        ("Modalidad", "combobox", {"values": modalidades})
    ])
    form_registro.pack(pady=15, padx=20)

    def registrar():
        try:
            postulante = Postulante(
                entries_registro["ci"].get().strip(),
                entries_registro["nombre"].get().strip(),
                entries_registro["apellido_paterno"].get().strip(),
                entries_registro["apellido_materno"].get().strip(),
                entries_registro["fecha_de_nacimiento_dd/mm/aaaa"].get().strip(),
                entries_registro["teléfono"].get().strip(),
                entries_registro["email"].get().strip(),
                entries_registro["dirección"].get().strip(),
                entries_registro["facultad"].get(),
                entries_registro["modalidad"].get()
            )
            if not postulante.es_valido():
                messagebox.showwarning("Error", "Datos inválidos. Verifique CI, email y fecha de nacimiento.")
                return
            exito, mensaje = manager.registrar_postulante(
                postulante.ci, postulante.nombre, postulante.apellido_paterno, postulante.apellido_materno,
                postulante.fecha_nacimiento, postulante.telefono, postulante.email, postulante.direccion,
                postulante.facultad, postulante.modalidad
            )
            messagebox.showinfo("Registro", mensaje) if exito else messagebox.showerror("Error", mensaje)
            if exito:
                for entry in entries_registro.values():
                    if isinstance(entry, ttk.Entry):
                        entry.delete(0, tk.END)
                    else:
                        entry.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar postulante: {str(e)}")

    crear_boton(form_registro, "Registrar", registrar).grid(row=10, column=0, columnspan=2, pady=15)

    frame_pago = tk.Frame(notebook, bg="white")
    notebook.add(frame_pago, text="Pago")
    tk.Label(frame_pago, text="💳", font=("Arial", 24), bg="white", fg="grey").pack(pady=10)
    tk.Label(frame_pago, text="Registro de Pago", font=("Arial", 14, "bold"), bg="white", fg="black").pack()
    tk.Label(frame_pago, text="Registra el pago de tu inscripción simulando el Websis UMSS.", font=("Arial", 9), bg="white", fg="grey", wraplength=500).pack(pady=5)

    metodos_pago = ["Banco Unión", "Tarjeta de Crédito/Débito", "Tigo Money", "Código QR UMSS"]
    form_pago, entries_pago = crear_formulario(frame_pago, [
        ("CI", "entry"),
        ("Monto (Bs)", "entry"),
        ("Método de Pago", "combobox", {"values": metodos_pago}),
        ("Número de Transacción", "entry"),
        ("Fecha (DD/MM/AAAA)", "entry")
    ])
    form_pago.pack(pady=15, padx=20)

    def confirmar_pago():
        try:
            monto = entries_pago["monto_bs"].get().strip()
            try:
                monto = float(monto)
            except ValueError:
                messagebox.showwarning("Error", "Monto inválido.")
                return
            pago = Pago(monto, entries_pago["método_de_pago"].get(), entries_pago["fecha_dd/mm/aaaa"].get().strip())
            if not pago.es_valido():
                messagebox.showwarning("Error", "Datos del pago inválidos. Verifique monto, método y fecha.")
                return
            transaccion = entries_pago["número_de_transacción"].get().strip()
            if not transaccion or len(transaccion) < 6:
                messagebox.showwarning("Error", "El número de transacción debe tener al menos 6 caracteres.")
                return
            ci = entries_pago["ci"].get().strip()
            resumen = f"Resumen del Pago:\n\nCI: {ci}\nMonto: {monto} Bs\nMétodo: {pago.tipo}\nTransacción: {transaccion}\nFecha: {pago.fecha}\n\n¿Confirmar pago?"
            if messagebox.askyesno("Confirmar Pago", resumen):
                exito, mensaje = manager.registrar_pago(ci, monto, pago.tipo, pago.fecha, transaccion)
                messagebox.showinfo("Pago", mensaje) if exito else messagebox.showerror("Error", mensaje)
                if exito:
                    for entry in entries_pago.values():
                        if isinstance(entry, ttk.Entry):
                            entry.delete(0, tk.END)
                        else:
                            entry.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar pago: {str(e)}")

    crear_boton(form_pago, "Confirmar Pago", confirmar_pago).grid(row=5, column=0, columnspan=2, pady=15)

    frame_consulta = tk.Frame(notebook, bg="white")
    notebook.add(frame_consulta, text="Consulta")
    tk.Label(frame_consulta, text="🔍", font=("Arial", 24), bg="white", fg="grey").pack(pady=10)
    tk.Label(frame_consulta, text="Consulta de Estado", font=("Arial", 14, "bold"), bg="white", fg="black").pack()
    tk.Label(frame_consulta, text="Consulta el estado de tu admisión.", font=("Arial", 9), bg="white", fg="grey", wraplength=500).pack(pady=5)

    form_consulta, entries_consulta = crear_formulario(frame_consulta, [("CI", "entry")])
    form_consulta.pack(pady=15, padx=20)

    def consultar():
        try:
            ci = entries_consulta["ci"].get().strip()
            exito, resultado = manager.consultar_estado(ci)
            if exito:
                messagebox.showinfo("Estado", f"Estado: {resultado[0]}\nNota: {resultado[1]}")
                entries_consulta["ci"].delete(0, tk.END)
            else:
                messagebox.showerror("Error", resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Error al consultar estado: {str(e)}")

    crear_boton(form_consulta, "Consultar", consultar).grid(row=1, column=0, columnspan=2, pady=15)

    app.mainloop()

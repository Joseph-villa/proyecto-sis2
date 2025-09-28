import tkinter as tk
from tkinter import ttk, messagebox
from admisiones_manager import AdmisionesManager

def lanzar_admin():
    manager = AdmisionesManager()
    app = tk.Tk()
    app.title("Administrador")

    # Centrar ventana
    app.update_idletasks()
    width, height = 700, 500
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f"{width}x{height}+{x}+{y}")

    notebook = ttk.Notebook(app)
    notebook.pack(expand=True, fill="both")

    # Pestaña: Publicar resultado
    frame_resultado = ttk.Frame(notebook, padding=20)
    notebook.add(frame_resultado, text="Publicar Resultado")

    ttk.Label(frame_resultado, text="CI").grid(row=0, column=0, sticky="e")
    ci_resultado = ttk.Entry(frame_resultado)
    ci_resultado.grid(row=0, column=1, sticky="ew")

    ttk.Label(frame_resultado, text="Nota").grid(row=1, column=0, sticky="e")
    nota_entry = ttk.Entry(frame_resultado)
    nota_entry.grid(row=1, column=1, sticky="ew")

    def publicar():
        ci = ci_resultado.get().strip()
        try:
            nota = float(nota_entry.get())
        except ValueError:
            messagebox.showwarning("Error", "Nota inválida.")
            return
        manager.publicar_resultado(ci, nota)
        messagebox.showinfo("Resultado", "Resultado publicado.")

    ttk.Button(frame_resultado, text="Publicar", command=publicar).grid(row=2, column=0, columnspan=2, pady=10)

    # Pestaña: Editar datos
    frame_editar = ttk.Frame(notebook, padding=20)
    notebook.add(frame_editar, text="Editar Datos")

    ttk.Label(frame_editar, text="CI").grid(row=0, column=0, sticky="e")
    ci_editar = ttk.Entry(frame_editar)
    ci_editar.grid(row=0, column=1, sticky="ew")

    ttk.Label(frame_editar, text="Campo").grid(row=1, column=0, sticky="e")
    campo_entry = ttk.Entry(frame_editar)
    campo_entry.grid(row=1, column=1, sticky="ew")

    ttk.Label(frame_editar, text="Nuevo Valor").grid(row=2, column=0, sticky="e")
    nuevo_valor_entry = ttk.Entry(frame_editar)
    nuevo_valor_entry.grid(row=2, column=1, sticky="ew")

    def editar():
        ci = ci_editar.get().strip()
        campo = campo_entry.get().strip()
        nuevo_valor = nuevo_valor_entry.get().strip()
        manager.editar_dato(ci, campo, nuevo_valor)
        messagebox.showinfo("Edición", "Dato actualizado.")

    ttk.Button(frame_editar, text="Editar", command=editar).grid(row=3, column=0, columnspan=2, pady=10)

    # Pestaña: Ver postulantes
    frame_tabla = ttk.Frame(notebook, padding=10)
    notebook.add(frame_tabla, text="Ver Postulantes")

    tabla = ttk.Treeview(frame_tabla, columns=("CI", "Nombre", "Carrera", "Modalidad", "Estado", "Nota"), show="headings")
    for col in tabla["columns"]:
        tabla.heading(col, text=col)
        tabla.column(col, anchor="center", width=100)
    tabla.pack(expand=True, fill="both")

    def cargar_postulantes():
        tabla.delete(*tabla.get_children())
        manager.dao.cursor.execute("SELECT ci, nombre, carrera, modalidad, estado, nota FROM postulantes")
        for fila in manager.dao.cursor.fetchall():
            tabla.insert("", "end", values=fila)

    ttk.Button(frame_tabla, text="Actualizar tabla", command=cargar_postulantes).pack(pady=10)
    cargar_postulantes()

    # Expandir columnas en todas las pestañas
    for frame in [frame_resultado, frame_editar]:
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)

    app.mainloop()




import tkinter as tk
from tkinter import ttk, messagebox
from admisiones_manager import AdmisionesManager
import re

def lanzar_postulante():
    manager = AdmisionesManager()
    app = tk.Tk()
    app.title("Postulante")

    # Centrar ventana
    app.update_idletasks()
    width, height = 600, 500
    x = (app.winfo_screenwidth() // 2) - (width // 2)
    y = (app.winfo_screenheight() // 2) - (height // 2)
    app.geometry(f"{width}x{height}+{x}+{y}")

    notebook = ttk.Notebook(app)
    notebook.pack(expand=True, fill="both")

    # Frame: Registro
    frame_registro = ttk.Frame(notebook, padding=20)
    notebook.add(frame_registro, text="Registro")

    ttk.Label(frame_registro, text="CI").grid(row=0, column=0, sticky="e"); ci_entry = ttk.Entry(frame_registro); ci_entry.grid(row=0, column=1, sticky="ew")
    ttk.Label(frame_registro, text="Nombre").grid(row=1, column=0, sticky="e"); nombre_entry = ttk.Entry(frame_registro); nombre_entry.grid(row=1, column=1, sticky="ew")
    ttk.Label(frame_registro, text="Carrera").grid(row=2, column=0, sticky="e"); carrera_entry = ttk.Entry(frame_registro); carrera_entry.grid(row=2, column=1, sticky="ew")
    ttk.Label(frame_registro, text="Modalidad").grid(row=3, column=0, sticky="e"); modalidad_entry = ttk.Entry(frame_registro); modalidad_entry.grid(row=3, column=1, sticky="ew")

    def registrar():
        ci = ci_entry.get().strip()
        nombre = nombre_entry.get().strip()
        carrera = carrera_entry.get().strip()
        modalidad = modalidad_entry.get().strip()

        if not all([ci, nombre, carrera, modalidad]):
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")
            return
        if not ci.isdigit() or len(ci) < 5:
            messagebox.showwarning("Error", "CI inválido. Debe tener al menos 5 dígitos.")
            return
        if manager.registrar_postulante(ci, nombre, carrera, modalidad):
            messagebox.showinfo("Registro", "Postulante registrado correctamente.")
        else:
            messagebox.showwarning("Error", "Ya existe un postulante con ese CI.")

    ttk.Button(frame_registro, text="Registrar", command=registrar).grid(row=4, column=0, columnspan=2, pady=10)

    # Frame: Pago
    frame_pago = ttk.Frame(notebook, padding=20)
    notebook.add(frame_pago, text="Pago")

    ttk.Label(frame_pago, text="CI").grid(row=0, column=0, sticky="e"); ci_pago = ttk.Entry(frame_pago); ci_pago.grid(row=0, column=1, sticky="ew")
    ttk.Label(frame_pago, text="Monto").grid(row=1, column=0, sticky="e"); monto_entry = ttk.Entry(frame_pago); monto_entry.grid(row=1, column=1, sticky="ew")
    ttk.Label(frame_pago, text="Tipo").grid(row=2, column=0, sticky="e"); tipo_entry = ttk.Entry(frame_pago); tipo_entry.grid(row=2, column=1, sticky="ew")
    ttk.Label(frame_pago, text="Fecha (DD/MM/AAAA)").grid(row=3, column=0, sticky="e"); fecha_entry = ttk.Entry(frame_pago); fecha_entry.grid(row=3, column=1, sticky="ew")

    def pagar():
        ci = ci_pago.get().strip()
        tipo = tipo_entry.get().strip()
        fecha = fecha_entry.get().strip()

        try:
            monto = float(monto_entry.get())
            if monto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Error", "Monto inválido.")
            return

        if not all([ci, tipo, fecha]):
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")
            return
        if not re.match(r"\d{2}/\d{2}/\d{4}", fecha):
            messagebox.showwarning("Error", "Fecha inválida.")
            return

        manager.registrar_pago(ci, monto, tipo, fecha)
        messagebox.showinfo("Pago", "Pago registrado correctamente.")

    ttk.Button(frame_pago, text="Registrar Pago", command=pagar).grid(row=4, column=0, columnspan=2, pady=10)

    # Frame: Consulta
    frame_consulta = ttk.Frame(notebook, padding=20)
    notebook.add(frame_consulta, text="Consulta")

    ttk.Label(frame_consulta, text="CI").grid(row=0, column=0, sticky="e"); ci_consulta = ttk.Entry(frame_consulta); ci_consulta.grid(row=0, column=1, sticky="ew")

    def consultar():
        ci = ci_consulta.get().strip()
        estado = manager.consultar_estado(ci)
        if estado:
            messagebox.showinfo("Estado", f"Estado: {estado[0]}\nNota: {estado[1]}")
        else:
            messagebox.showwarning("Consulta", "Postulante no encontrado.")

    ttk.Button(frame_consulta, text="Consultar", command=consultar).grid(row=1, column=0, columnspan=2, pady=10)

    for frame in [frame_registro, frame_pago, frame_consulta]:
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=2)

    app.mainloop()


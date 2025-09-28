import tkinter as tk
from interfaz_postulante import lanzar_postulante
from interfaz_admin import lanzar_admin

def seleccionar_rol():
    ventana = tk.Tk()
    ventana.title("Sistema de Admisión UMSS")

    tk.Label(ventana, text="Selecciona tu rol").pack(pady=10)
    tk.Button(ventana, text="Postulante", command=lambda: [ventana.destroy(), lanzar_postulante()]).pack(pady=5)
    tk.Button(ventana, text="Administrador", command=lambda: [ventana.destroy(), lanzar_admin()]).pack(pady=5)

    ventana.mainloop()

seleccionar_rol()






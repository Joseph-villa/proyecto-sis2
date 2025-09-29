import tkinter as tk
from tkinter import ttk
from interfaz_postulante import lanzar_postulante
from interfaz_admin import lanzar_admin

def main():
    root = tk.Tk()
    root.title("Sistema de Admisión UMSS")
    
    window_width = 900
    window_height = 700
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(True, True)
    root.configure(bg="white")

    header_frame = tk.Frame(root, bg="white")
    header_frame.pack(side=tk.TOP, anchor="nw", padx=20, pady=20)
    
    logo_label = tk.Label(header_frame, text="🏫", font=("Arial", 16), bg="white", fg="black")
    logo_label.pack(side=tk.LEFT, padx=5)
    
    header_label = tk.Label(
        header_frame,
        text="Universidad Mayor de San Simón",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="black"
    )
    header_label.pack(side=tk.LEFT)

    title_label = tk.Label(
        root,
        text="Bienvenido al Sistema de Admisión",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="black"
    )
    title_label.pack(pady=20)

    subtitle_label = tk.Label(
        root,
        text="Selecciona tu rol para acceder a las funcionalidades correspondientes del sistema de admisiones universitarias.",
        font=("Arial", 10),
        bg="white",
        fg="grey",
        wraplength=600,
        justify="center"
    )
    subtitle_label.pack(pady=10)

    cards_frame = tk.Frame(root, bg="white")
    cards_frame.pack(expand=True)

    card_postulante = tk.Frame(
        root,
        bg="white",
        relief="raised",
        borderwidth=2,
        width=280,
        height=300
    )
    card_postulante.pack(side=tk.LEFT, padx=15, pady=20, in_=cards_frame)

    postulante_icon = tk.Label(card_postulante, text="👤", font=("Arial", 24), bg="white", fg="grey")
    postulante_icon.pack(pady=5)
    
    postulante_title = tk.Label(
        card_postulante,
        text="Postulante",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="black"
    )
    postulante_title.pack(pady=5)
    
    postulante_desc = tk.Label(
        card_postulante,
        text="Accede para registrarte, realizar pagos y consultar tu estado de admisión",
        font=("Arial", 9),
        bg="white",
        fg="grey",
        wraplength=250,
        justify="center"
    )
    postulante_desc.pack(pady=5)
    
    tk.Label(card_postulante, text="Registro de datos personales", font=("Arial", 9), bg="white", fg="grey").pack()
    tk.Label(card_postulante, text="Gestión de pagos", font=("Arial", 9), bg="white", fg="grey").pack()
    tk.Label(card_postulante, text="Consulta de resultados", font=("Arial", 9), bg="white", fg="grey").pack()

    def abrir_postulante():
        root.withdraw()
        lanzar_postulante(root)

    postulante_button = tk.Button(
        card_postulante,
        text="Acceder como Postulante",
        font=("Arial", 10),
        bg="white",
        fg="black",
        relief="raised",
        command=abrir_postulante,
        width=20
    )
    postulante_button.pack(pady=10)

    card_admin = tk.Frame(
        root,
        bg="white",
        relief="raised",
        borderwidth=2,
        width=280,
        height=300
    )
    card_admin.pack(side=tk.LEFT, padx=15, pady=20, in_=cards_frame)

    admin_icon = tk.Label(card_admin, text="🛡️", font=("Arial", 24), bg="white", fg="grey")
    admin_icon.pack(pady=5)
    
    admin_title = tk.Label(
        card_admin,
        text="Administrador",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="black"
    )
    admin_title.pack(pady=5)
    
    admin_desc = tk.Label(
        card_admin,
        text="Panel administrativo para gestionar postulantes y publicar resultados",
        font=("Arial", 9),
        bg="white",
        fg="grey",
        wraplength=250,
        justify="center"
    )
    admin_desc.pack(pady=5)
    
    tk.Label(card_admin, text="Publicar resultados", font=("Arial", 9), bg="white", fg="grey").pack()
    tk.Label(card_admin, text="Editar datos de postulantes", font=("Arial", 9), bg="white", fg="grey").pack()
    tk.Label(card_admin, text="Ver lista completa", font=("Arial", 9), bg="white", fg="grey").pack()

    def abrir_admin():
        root.withdraw()
        lanzar_admin(root)

    admin_button = tk.Button(
        card_admin,
        text="Acceder como Administrador",
        font=("Arial", 10),
        bg="white",
        fg="black",
        relief="raised",
        command=abrir_admin,
        width=20
    )
    admin_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

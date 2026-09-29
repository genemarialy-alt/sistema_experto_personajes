import tkinter as tk
from tkinter import ttk
import logica_adivinador as logica
import os

# Directorio base del script, para rutas absolutas de imágenes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class SistemaExpertoPersonajes:
    def __init__(self, root):
        self.root = root
        self.root.title("Akinator de Fondo de Bikini")
        self.root.geometry("550x450")
        self.root.configure(bg="#2b2b2b")
        self.root.resizable(False, False)
        
        self.total_interacciones = 0
        # Diccionario de hechos {tag: "si"/"no"}
        self.hechos = {}
        # Estado actual de la maquina de estados
        self.estado_actual = logica.ESTADO_INICIAL
        
        self.configurar_estilos()
        self.crear_pantalla_inicio()
        
    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Botón Sí
        style.configure("BotonSi.TButton", font=("Segoe UI", 12, "bold"), padding=10, background="#4CAF50", foreground="white")
        style.map("BotonSi.TButton", background=[("active", "#45a049")])
        
        # Botón No
        style.configure("BotonNo.TButton", font=("Segoe UI", 12, "bold"), padding=10, background="#f44336", foreground="white")
        style.map("BotonNo.TButton", background=[("active", "#da190b")])
        
        # Botón Reiniciar
        style.configure("BotonReiniciar.TButton", font=("Segoe UI", 11), padding=8, background="#2196F3", foreground="white")
        style.map("BotonReiniciar.TButton", background=[("active", "#0b7dda")])

    def crear_pantalla_inicio(self):
        self.frame_inicio = tk.Frame(self.root, bg="#2b2b2b")
        self.frame_inicio.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        lbl_titulo = tk.Label(self.frame_inicio, text="🧽 Adivinador de Personajes", font=("Segoe UI", 18, "bold"), bg="#2b2b2b", fg="#4CAF50")
        lbl_titulo.pack(pady=20)
        
        instrucciones = (
            "El programa adivinará un personaje que hayas pensado.\n\n"
            "Puedes escoger entre estos personajes:\n"
            "Bob Esponja, Patricio, Calamardo, Don Cangrejo, Arenita.\n"
            "Gary, Perlita, Karen o Plankton\n\n"
            "¿Estás listo?"
        )
        
        lbl_instrucciones = tk.Label(self.frame_inicio, text=instrucciones, font=("Segoe UI", 13), bg="#2b2b2b", fg="white", justify="center")
        lbl_instrucciones.pack(pady=30)
        
        btn_listo = ttk.Button(self.frame_inicio, text=" Sí, estoy listo ", style="BotonSi.TButton", command=self.iniciar_juego)
        btn_listo.pack(pady=20)
        
    def iniciar_juego(self):
        self.frame_inicio.destroy()
        self.crear_interfaz()
        self.hacer_pregunta()

    def crear_interfaz(self):
        # Encabezado
        self.lbl_titulo = tk.Label(self.root, text="🧽 Adivinador de Personajes de Bob Esponja", font=("Segoe UI", 16, "bold"), bg="#2b2b2b", fg="#4CAF50")
        self.lbl_titulo.pack(pady=20)
        
        # Progreso
        self.lbl_progreso = tk.Label(self.root, text="", font=("Segoe UI", 10), bg="#2b2b2b", fg="#aaaaaa")
        self.lbl_progreso.pack()
        
        # En una versión dinámica, la barra de progreso puede ser indeterminada o fija a 10 (mínimo)
        self.progreso_var = tk.DoubleVar()
        self.barra_progreso = ttk.Progressbar(self.root, variable=self.progreso_var, maximum=10, length=400)
        self.barra_progreso.pack(pady=10)
        
        # Marco de pregunta
        self.frame_pregunta = tk.Frame(self.root, bg="#333333", bd=2, relief=tk.GROOVE)
        self.frame_pregunta.pack(pady=20, padx=30, fill=tk.BOTH, expand=True)
        
        self.lbl_pregunta = tk.Label(self.frame_pregunta, text="", font=("Segoe UI", 14), bg="#333333", fg="white", wraplength=400, justify="center")
        self.lbl_pregunta.pack(expand=True, pady=30)
        
        # Marco de botones
        self.frame_botones = tk.Frame(self.root, bg="#2b2b2b")
        self.frame_botones.pack(pady=20)
        
        self.btn_si = ttk.Button(self.frame_botones, text=" Sí ", style="BotonSi.TButton", command=lambda: self.responder("si"), width=15)
        self.btn_si.grid(row=0, column=0, padx=20)
        
        self.btn_no = ttk.Button(self.frame_botones, text=" No ", style="BotonNo.TButton", command=lambda: self.responder("no"), width=15)
        self.btn_no.grid(row=0, column=1, padx=20)

    def hacer_pregunta(self):
        # 1. Inferencia: ver si ya adivinamos
        resultados = logica.motor_inferencia(self.hechos)
        
        if resultados and self.total_interacciones >= 10:
            self.progreso_var.set(10)
            self.mostrar_resultados()
            return

        # 2. Mostrar la pregunta del estado actual
        if self.estado_actual is not None:
            texto = logica.preguntas_dict[self.estado_actual]
            self.lbl_pregunta.config(text=texto)
            self.lbl_progreso.config(text=f"Interacción {self.total_interacciones + 1}")
            self.progreso_var.set(min(self.total_interacciones, 10))
        else:
            # La maquina llego a un estado final
            self.progreso_var.set(10)
            self.mostrar_resultados()

    def responder(self, respuesta):
        # Guardar hecho actual
        self.hechos[self.estado_actual] = respuesta
        self.total_interacciones += 1

        # Transicionar al siguiente estado
        self.estado_actual = logica.siguiente_estado(
            self.estado_actual, respuesta, self.hechos
        )
        self.hacer_pregunta()

    def mostrar_resultados(self):
        # Destruir todos los widgets del juego
        self.frame_pregunta.destroy()
        self.frame_botones.destroy()
        self.barra_progreso.destroy()
        self.lbl_progreso.destroy()
        self.lbl_titulo.destroy()

        # Forzar actualización antes de reconstruir la UI
        self.root.geometry("550x480")
        self.root.update()

        # Frame que cubre toda la ventana con grid
        frame_total = tk.Frame(self.root, bg="#2b2b2b")
        frame_total.place(x=0, y=0, relwidth=1, relheight=1)
        frame_total.update()

        # Usar grid para control preciso de filas
        frame_total.columnconfigure(0, weight=1)

        fila = 0

        # Título
        tk.Label(frame_total, text="⭐ El Personaje es... ⭐",
                 font=("Segoe UI", 16, "bold"), bg="#2b2b2b", fg="#FFC107").grid(
                 row=fila, column=0, pady=(15, 5)); fila += 1

        # Inferencia
        resultados = logica.motor_inferencia(self.hechos)

        if resultados:
            personaje = resultados[0]

            mapa_imagenes = {
                "Bob Esponja": os.path.join(BASE_DIR, "img", "bob esponja.png"),
                "Arenita": os.path.join(BASE_DIR, "img", "arenita.png"),
                "Don Cangrejo": os.path.join(BASE_DIR, "img", "don cangrejo.png"),
                "Calamardo": os.path.join(BASE_DIR, "img", "calamardo.png"),
                "Patricio Estrella": os.path.join(BASE_DIR, "img", "patricio.png"),
                "Gary": os.path.join(BASE_DIR, "img", "gary.png"),
                "Perlita": os.path.join(BASE_DIR, "img", "perlita.png"),
                "Karen": os.path.join(BASE_DIR, "img", "karen.png"),
                "Plankton": os.path.join(BASE_DIR, "img", "plankton.png"),
            }
            ruta_img = mapa_imagenes.get(personaje, "")

            tk.Label(frame_total, text=f"¡Es {personaje}!",
                     font=("Segoe UI", 18, "bold"), bg="#2b2b2b", fg="#4CAF50").grid(
                     row=fila, column=0, pady=5); fila += 1

            try:
                from PIL import Image, ImageTk  # pyrefly: ignore [missing-import]
                if os.path.exists(ruta_img):
                    img = Image.open(ruta_img)
                    resample_filter = getattr(Image, 'Resampling', Image).LANCZOS
                    img = img.resize((250, 250), resample_filter)
                    foto = ImageTk.PhotoImage(img)
                    lbl_img = tk.Label(frame_total, image=foto, bg="#2b2b2b")
                    lbl_img.image = foto
                    lbl_img.grid(row=fila, column=0, pady=8); fila += 1
            except Exception:
                try:
                    foto = tk.PhotoImage(file=ruta_img)
                    lbl_img = tk.Label(frame_total, image=foto, bg="#2b2b2b")
                    lbl_img.image = foto
                    lbl_img.grid(row=fila, column=0, pady=8); fila += 1
                except Exception:
                    pass
        else:
            tk.Label(frame_total,
                     text="No se encontró ningún personaje\ncon esas características.",
                     font=("Segoe UI", 12), bg="#2b2b2b", fg="#f44336").grid(
                     row=fila, column=0, pady=10); fila += 1

            ruta_triste = os.path.join(BASE_DIR, "img", "triste.png")
            try:
                from PIL import Image, ImageTk  # pyrefly: ignore [missing-import]
                if os.path.exists(ruta_triste):
                    img = Image.open(ruta_triste)
                    resample_filter = getattr(Image, 'Resampling', Image).LANCZOS
                    img = img.resize((250, 250), resample_filter)
                    foto = ImageTk.PhotoImage(img)
                    lbl_img = tk.Label(frame_total, image=foto, bg="#2b2b2b")
                    lbl_img.image = foto
                    lbl_img.grid(row=fila, column=0, pady=8); fila += 1
            except Exception:
                try:
                    foto = tk.PhotoImage(file=ruta_triste)
                    lbl_img = tk.Label(frame_total, image=foto, bg="#2b2b2b")
                    lbl_img.image = foto
                    lbl_img.grid(row=fila, column=0, pady=8); fila += 1
                except Exception:
                    pass

        # Botón en la última fila — siempre debajo de la imagen
        ttk.Button(frame_total, text="🔄 Volver a jugar",
                   style="BotonReiniciar.TButton", command=self.reiniciar).grid(
                   row=fila, column=0, pady=15)
        
    def reiniciar(self):
        self.root.destroy()
        root = tk.Tk()
        app = SistemaExpertoPersonajes(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaExpertoPersonajes(root)
    root.mainloop()

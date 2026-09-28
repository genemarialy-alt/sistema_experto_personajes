import tkinter as tk
from tkinter import ttk
import logica_peliculas as logica

class SistemaExpertoPeliculas:
    def __init__(self, root):
        self.root = root
        self.root.title("CineBot: Sistema Experto de Recomendación")
        self.root.geometry("550x450")
        self.root.configure(bg="#2b2b2b")
        self.root.resizable(False, False)
        
        self.preguntas = logica.obtener_preguntas()
        self.indice_pregunta = 0
        self.hechos = []
        
        self.configurar_estilos()
        self.crear_interfaz()
        self.hacer_pregunta()
        
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

    def crear_interfaz(self):
        # Encabezado
        self.lbl_titulo = tk.Label(self.root, text="🎬 Asistente Experto de Películas", font=("Segoe UI", 16, "bold"), bg="#2b2b2b", fg="#4CAF50")
        self.lbl_titulo.pack(pady=20)
        
        # Progreso
        self.lbl_progreso = tk.Label(self.root, text="", font=("Segoe UI", 10), bg="#2b2b2b", fg="#aaaaaa")
        self.lbl_progreso.pack()
        
        self.progreso_var = tk.DoubleVar()
        self.barra_progreso = ttk.Progressbar(self.root, variable=self.progreso_var, maximum=len(self.preguntas), length=400)
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
        if self.indice_pregunta < len(self.preguntas):
            pregunta_texto, _ = self.preguntas[self.indice_pregunta]
            self.lbl_pregunta.config(text=pregunta_texto)
            self.lbl_progreso.config(text=f"Interacción {self.indice_pregunta + 1} de {len(self.preguntas)}")
            self.progreso_var.set(self.indice_pregunta)
        else:
            self.progreso_var.set(len(self.preguntas))
            self.mostrar_resultados()

    def responder(self, respuesta):
        _, tag = self.preguntas[self.indice_pregunta]
        
        if respuesta == "si":
            self.hechos.append(tag)
        
        self.indice_pregunta += 1
        self.hacer_pregunta()

    def mostrar_resultados(self):
        # Limpiar pantalla
        self.frame_pregunta.destroy()
        self.frame_botones.destroy()
        self.barra_progreso.destroy()
        self.lbl_progreso.destroy()
        
        self.lbl_titulo.config(text="⭐ Sus Recomendaciones Personalizadas ⭐", fg="#FFC107")
        
        # Inferencia
        resultados = logica.motor_inferencia(self.hechos)
        
        frame_resultados = tk.Frame(self.root, bg="#2b2b2b")
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        if resultados:
            # Lista scrolleable atractiva
            listbox = tk.Listbox(frame_resultados, font=("Segoe UI", 12), bg="#333333", fg="white", selectbackground="#4CAF50", bd=0, highlightthickness=0)
            listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar = ttk.Scrollbar(frame_resultados, orient="vertical", command=listbox.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            listbox.config(yscrollcommand=scrollbar.set)
            
            for i, peli in enumerate(resultados):
                listbox.insert(tk.END, f"  🎬  {peli}")
                
            # Filas alternas
            for i in range(0, listbox.size(), 2):
                listbox.itemconfigure(i, background="#3a3a3a")
                
        else:
            lbl_vacio = tk.Label(frame_resultados, text="No pudimos encontrar recomendaciones exactas.", font=("Segoe UI", 12), bg="#2b2b2b", fg="#f44336")
            lbl_vacio.pack(pady=40)
            
        btn_reiniciar = ttk.Button(self.root, text="🔄 Realizar otra consulta", style="BotonReiniciar.TButton", command=self.reiniciar)
        btn_reiniciar.pack(pady=20)
        
    def reiniciar(self):
        self.root.destroy()
        root = tk.Tk()
        app = SistemaExpertoPeliculas(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaExpertoPeliculas(root)
    root.mainloop()

reglas = [
    {
        "if": ["animacion", "accion"],
        "then": "anime"
    },
    {
        "if": ["animacion", "ciencia ficcion"],
        "then": "anime"
    },
    {
        "if": ["drama", "romance"],
        "then": "melodrama"
    },
    {
        "if": ["superheroes"],
        "then": "accion"
    },
    {
        "if": ["anime", "estreno"],
        "then": ["Suzume", "El Niño y la Garza", "Jujutsu Kaisen 0", "Demon Slayer: Mugen Train", "Evangelion: 3.0+1.0"]
    },
    {
        "if": ["anime", "clasico"],
        "then": ["Akira", "El Viaje de Chihiro", "Ghost in the Shell", "La Princesa Mononoke", "Mi Vecino Totoro"]
    },
    {
        "if": ["melodrama", "larga"],
        "then": ["Titanic", "Diario de una Pasión", "Lo que el viento se llevó", "Expiación", "Bajo la misma estrella"]
    },
    {
        "if": ["accion", "estreno", "superheroes"],
        "then": ["Spider-Man: Across the Spider-Verse", "Guardianes de la Galaxia Vol. 3", "The Batman", "Black Panther: Wakanda Forever", "Deadpool & Wolverine"]
    },
    {
        "if": ["accion", "clasico", "superheroes"],
        "then": ["The Dark Knight", "Spider-Man 2", "Iron Man", "The Avengers", "Superman (1978)"]
    },
    {
        "if": ["accion", "larga"],
        "then": ["Avengers: Endgame", "John Wick 4", "Mad Max: Fury Road", "Gladiador", "El Señor de los Anillos: El Retorno del Rey"]
    },
    {
        "if": ["accion", "estreno"],
        "then": ["Misión Imposible: Sentencia Mortal", "Top Gun: Maverick", "Tyler Rake 2", "The Creator", "Rápidos y Furiosos 10"]
    },
    {
        "if": ["comedia", "animacion", "estreno"],
        "then": ["Super Mario Bros. La Película", "Minions: Nace un Villano", "Gato con Botas: El Último Deseo", "Intensamente 2", "Kung Fu Panda 4"]
    },
    {
        "if": ["comedia", "romance"],
        "then": ["Cuestión de Tiempo", "La Propuesta", "Loco y Estúpido Amor", "10 Cosas que odio de ti", "Notting Hill"]
    },
    {
        "if": ["terror", "estreno"],
        "then": ["M3GAN", "Evil Dead Rise", "Scream 6", "Háblame", "La Monja 2"]
    },
    {
        "if": ["terror", "clasico"],
        "then": ["El Exorcista", "El Resplandor", "Halloween", "Pesadilla en la calle Elm", "Psicosis"]
    },
    {
        "if": ["ciencia ficcion", "larga"],
        "then": ["Interstellar", "Dune: Parte 2", "Avatar: El Camino del Agua", "Blade Runner 2049", "2001: Odisea del Espacio"]
    },
    {
        "if": ["ciencia ficcion", "clasico"],
        "then": ["Blade Runner", "Alien", "Volver al Futuro", "Star Wars: El Imperio Contraataca", "Matrix"]
    },
    {
        "if": ["drama", "larga"],
        "then": ["Oppenheimer", "El Padrino", "La Lista de Schindler", "Titanic", "El Lobo de Wall Street"]
    },
    {
        "if": ["animacion", "clasico"],
        "then": ["El Rey León", "Toy Story", "Shrek", "Buscando a Nemo", "Mulán"]
    },
    {
        "if": ["epoca", "drama"],
        "then": ["Gladiador", "Braveheart", "Ben-Hur", "El Último Samurái", "La Lista de Schindler"]
    },
    {
        "if": ["epoca", "romance"],
        "then": ["Orgullo y Prejuicio", "Titanic", "Lo que el viento se llevó", "El Paciente Inglés", "Bajo la misma estrella"]
    },
    {
        "if": ["epoca", "accion"],
        "then": ["Gladiador", "300", "Troya", "El Último Samurái", "Braveheart"]
    },
    {
        "if": ["epoca", "animacion"],
        "then": ["Brave: El Indomable", "La Bella y la Bestia", "Mulán", "El Jorobado de Notre Dame", "Anastasia"]
    },
    {
        "if": ["clasico", "corta"],
        "then": ["Cuenta Conmigo (89 min)", "El Rey León (88 min)", "Toy Story (81 min)", "Frankenstein 1931 (71 min)", "La Soga (80 min)"]
    },
    {
        "if": ["estreno", "corta"],
        "then": ["Super Mario Bros. (92 min)", "Oso Intoxicado (95 min)", "Host (56 min)", "Gato con Botas 2 (102 min)", "Háblame (95 min)"]
    },
    {
        "if": ["clasico", "larga"],
        "then": ["El Padrino (175 min)", "Ben-Hur (212 min)", "Titanic (195 min)", "Apocalypse Now (147 min)", "El Señor de los Anillos (178 min)"]
    },
    {
        "if": ["estreno", "larga"],
        "then": ["Oppenheimer (180 min)", "Dune: Parte 2 (166 min)", "Avatar 2 (192 min)", "The Batman (176 min)", "Killers of the Flower Moon (206 min)"]
    }
]

# --------------------------------------------------------
# MOTOR DE INFERENCIA
# --------------------------------------------------------

def motor_inferencia(hechos_usuario):
    hechos_completos = list(hechos_usuario)
    peliculas_recomendadas = set()
    cambios = True

    generos_base = ["accion", "comedia", "terror", "ciencia ficcion", "drama", "romance", "animacion", "superheroes", "anime", "melodrama", "epoca"]
    tiene_genero = any(genero in hechos_completos for genero in generos_base)

    # Ciclo de Inferencia Estricta (Encadenamiento Hacia Adelante)
    while cambios:
        cambios = False
        
        # Lista temporal para la fase de resolución de conflictos
        reglas_a_ejecutar = []
        
        # 1. FASE DE EQUIPARACIÓN (MATCHING): Buscar reglas cuyos antecedentes se cumplan
        for regla in reglas:
            if all(condicion in hechos_completos for condicion in regla["if"]):
                reglas_a_ejecutar.append(regla)
                
        # 2. FASE DE RESOLUCIÓN DE CONFLICTOS (CONFLICT RESOLUTION): 
        # Si el usuario eligió un género específico, descartamos las reglas genéricas que solo evalúan duración/época.
        reglas_filtradas = []
        for regla in reglas_a_ejecutar:
            regla_tiene_genero = any(g in regla["if"] for g in generos_base)
            if tiene_genero and not regla_tiene_genero:
                continue # Se descarta esta regla por menor prioridad
            reglas_filtradas.append(regla)
            
        # 3. FASE DE EJECUCIÓN (EXECUTION): Aplicar las reglas seleccionadas y derivar nuevos hechos o conclusiones
        for regla in reglas_filtradas:
            consecuente = regla["then"]
            
            # Si se deduce un nuevo hecho intermedio
            if isinstance(consecuente, str):
                if consecuente not in hechos_completos:
                    hechos_completos.append(consecuente)
                    cambios = True # Hubo cambios, el ciclo debe repetirse
                    
            # Si se deduce la recomendación final
            elif isinstance(consecuente, list):
                for peli in consecuente:
                    if peli not in peliculas_recomendadas:
                        peliculas_recomendadas.add(peli)

    return list(peliculas_recomendadas)

def obtener_preguntas():
    return [
        ("¿Le gustan las películas de Acción?", "accion"),
        ("¿Disfruta del género de Comedia?", "comedia"),
        ("¿Le interesan las películas de Terror o Suspenso?", "terror"),
        ("¿Es fanático de la Ciencia Ficción?", "ciencia ficcion"),
        ("¿Le gustan las historias emotivas de Drama?", "drama"),
        ("¿Le atraen las películas de Romance?", "romance"),
        ("¿Disfruta de las Películas Animadas?", "animacion"),
        ("¿Le gustan las películas de Superhéroes?", "superheroes"),
        ("¿Le gustan las películas de Época (ambientadas en el pasado histórico)?", "epoca"),
        ("¿Prefiere ver estrenos recientes (de los últimos años)?", "estreno"),
        ("¿Le interesan también las películas clásicas?", "clasico"),
        ("¿Le gustan las películas de larga duración (más de 2.5 horas)?", "larga"),
        ("¿O prefiere películas más cortas (menos de 1.5 horas)?", "corta")
    ]

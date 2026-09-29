preguntas_dict = {
    "vive_bikini": "¿El personaje vive en la ciudad submarina de Fondo de Bikini?",
    "primera_temp": "¿El personaje ha aparecido en la serie desde la primera temporada?",
    "conoce_bob": "¿El personaje interactúa frecuentemente con Bob Esponja?",
    "bueno": "¿El personaje es considerado bueno o neutral (no es un villano malvado)?",
    "respira_natural": "¿El personaje puede respirar bajo el agua de forma natural (sin trajes ni domos)?",
    "habla": "¿El personaje tiene la capacidad de hablar (usar lenguaje verbal)?",
    "ocupacion": "¿El personaje tiene un empleo u ocupación formal por la que gane dinero?",
    "femenino": "¿El personaje es de género femenino?",
    "tamano_normal": "¿El personaje tiene un tamaño regular (ni es un gigante, ni es microscópico)?",
    "animal": "¿El personaje es un animal o ser biológico (no es una máquina)?",
    "robot": "¿El personaje es una computadora o robot con pantalla?",
    "esposa_plankton": "¿Es la esposa de un villano que roba recetas?",
    "traje_buzo": "¿El personaje es un mamífero terrestre que requiere un traje de astronauta?",
    "karate": "¿Viene del estado de Texas y practica Karate?",
    "adolescente": "¿El personaje es una adolescente a la que le encanta ir de compras?",
    "ballena": "¿Es una ballena gigante, hija del dueño de un restaurante?",
    "maulla": "¿El personaje actúa como una mascota y maúlla como un gato?",
    "caracol": "¿Es un caracol que deja un rastro de baba?",
    "vive_roca": "¿El personaje es perezoso y vive debajo de una roca?",
    "estrella": "¿Es una estrella de mar rosada?",
    "roba_formulas": "¿El personaje es un villano que intenta robar la fórmula de la Cangreburger?",
    "un_ojo": "¿Tiene un solo ojo y antenas?",
    "jefe": "¿El personaje es el dueño o jefe de un restaurante muy exitoso?",
    "cangrejo": "¿Es un cangrejo rojo, tacaño y que ama el dinero más que a nada?",
    "empleado": "¿El personaje es un empleado de un restaurante de comida rápida?",
    "cocinero": "¿Es el cocinero principal encargado de la parrilla?",
    "esponja": "¿Es amarillo, cuadrado, poroso y muy alegre?",
    "cajero": "¿Trabaja en la caja registradora y odia su trabajo?",
    "pulpo": "¿Es un pulpo gruñón que toca el clarinete?",
}

#estado inicial
ESTADO_INICIAL = "vive_bikini"

def _transicion_tras_base(hechos):
    if hechos.get("femenino") == "si":
        if hechos.get("animal") == "no":
            return "robot"
        elif hechos.get("respira_natural") == "no":
            return "traje_buzo"
        elif hechos.get("tamano_normal") == "no":
            return "adolescente"
    else:
        if hechos.get("habla") == "no":
            return "maulla"
        elif hechos.get("ocupacion") == "no":
            return "vive_roca"
        elif hechos.get("tamano_normal") == "no" and hechos.get("bueno") == "no":
            return "roba_formulas"
        elif hechos.get("tamano_normal") == "si" and hechos.get("bueno") == "si":
            return "jefe"
    return None  

#Tabla de transiciones
flujo = {
    "vive_bikini": {"si": "primera_temp", "no": "primera_temp"},
    "primera_temp": {"si": "conoce_bob", "no": "conoce_bob"},
    "conoce_bob": {"si": "bueno", "no": "bueno"},
    "bueno": {"si": "respira_natural", "no": "respira_natural"},
    "respira_natural": {"si": "habla", "no": "habla"},
    "habla": {"si": "ocupacion", "no": "ocupacion"},
    "ocupacion": {"si": "femenino", "no": "femenino"},
    "femenino": {"si": "tamano_normal", "no": "tamano_normal"},
    "tamano_normal": {"si": "animal", "no": "animal"},
    "animal": _transicion_tras_base,

    #personajes femeninos
    "robot":{"si": "esposa_plankton", "no": None},
    "esposa_plankton":{"si": None, "no": None},

    "traje_buzo":{"si": "karate", "no": None},
    "karate":{"si": None, "no": None},

    "adolescente":{"si": "ballena", "no": None},
    "ballena":{"si": None, "no": None},

    #personajes masculinos
    "maulla":{"si": "caracol", "no": None},
    "caracol":{"si": None, "no": None},

    "vive_roca":{"si": "estrella", "no": None},
    "estrella":{"si": None, "no": None},

    "roba_formulas":{"si": "un_ojo", "no": None},
    "un_ojo":{"si": None, "no": None},

    "jefe":{"si": "cangrejo", "no": "empleado"},
    "cangrejo":{"si": None, "no": None},

    "empleado":{"si": "cocinero", "no": None},
    "cocinero":{"si": "esponja", "no": "cajero"},
    "esponja":{"si": None, "no": None},

    "cajero":{"si": "pulpo", "no": None},
    "pulpo":{"si": None, "no": None},
}

def siguiente_estado(estado_actual, respuesta, hechos):
    transicion = flujo.get(estado_actual)
    if transicion is None:
        return None
    if callable(transicion):
        return transicion(hechos)
    return transicion.get(respuesta)

#reglas inferencia
reglas = [
    {"si": [("femenino","si"), ("robot","si"), ("esposa_plankton","si")], "entonces": "Karen"},
    {"si": [("femenino","si"), ("traje_buzo","si"), ("karate","si")], "entonces": "Arenita"},
    {"si": [("femenino","si"), ("adolescente","si"), ("ballena","si")], "entonces": "Perlita"},
    {"si": [("femenino","no"), ("maulla","si"), ("caracol","si")], "entonces": "Gary"},
    {"si": [("femenino","no"), ("vive_roca","si"), ("estrella","si")], "entonces": "Patricio Estrella"},
    {"si": [("roba_formulas","si"), ("un_ojo","si")], "entonces": "Plankton"},
    {"si": [("jefe","si"), ("cangrejo","si")], "entonces": "Don Cangrejo"},
    {"si": [("cocinero","si"), ("esponja","si")], "entonces": "Bob Esponja"},
    {"si": [("cajero","si"), ("pulpo","si")], "entonces": "Calamardo"},
]

# MOTOR DE INFERENCIA
def motor_inferencia(hechos):
    encontrados = []
    for regla in reglas:
        if all(hechos.get(clave) == valor for clave, valor in regla["si"]):
            p = regla["entonces"]
            if p not in encontrados:
                encontrados.append(p)
    return encontrados
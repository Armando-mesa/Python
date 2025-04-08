import os

# Pedir al usuario un nombre para la carpeta
nombre_carpeta = input("Introduce el nombre de la carpeta: ")

# Ruta a una ubicación accesible, como el escritorio
ruta_escritorio = os.path.join(os.path.expanduser("~"), "Desktop")

# Crear la ruta completa para la nueva carpeta en el escritorio
ruta_carpeta = os.path.join(ruta_escritorio, nombre_carpeta)

# Verificar si la carpeta ya existe, si no, crearla
if not os.path.exists(ruta_carpeta):
    os.makedirs(ruta_carpeta)
    print(f"Carpeta '{nombre_carpeta}' creada en {ruta_escritorio}")
else:
    print(f"La carpeta '{nombre_carpeta}' ya existe en {ruta_escritorio}")
import os
import subprocess
import time 


# Ruta de la carpeta que contiene los archivos .csv
carpeta = 'C:\'

# Buscar todos los archivos .csv en la carpeta
archivos_csv = [archivo for archivo in os.listdir(carpeta) if archivo.endswith('.csv')]

# Abrir cada archivo .csv con Notepad++
for archivo in archivos_csv:
    subprocess.call(['notepad++', os.path.join(carpeta, archivo)])
    print(Archivo)
    time.sleep(20)  # Esperar 5 segundos antes de cerrar la pestaña
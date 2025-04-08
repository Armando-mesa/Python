import os
import pandas as pd

# Configura la ruta del archivo Excel
excel_path = 'C:\\Users\\luisarmando.mesa\\OneDrive - Grupo VASS\\Documents\\Python\\Rutas projectos.xlsx'

# Carga el archivo Excel en un DataFrame
df = pd.read_excel(excel_path, header=0)

# Asegúrate de que los nombres de las columnas 'Numero', 'Nombre' y 'Padre' estén presentes
required_columns = ['Numero', 'Nombre', 'Padre']
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"Las columnas {required_columns} deben estar presentes en el archivo Excel.")

# Ordena el DataFrame por la columna 'Numero' para procesar en orden
df = df.sort_values(by='Numero')

# Obtiene la ruta del escritorio
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# Crear un diccionario para rastrear las rutas de las carpetas
rutas_carpeta = {}

# Primero, crear las carpetas principales (sin padre)
for index, row in df[df['Padre'].isna()].iterrows():
    numero = int(row['Numero'])  # Asegurarse de que el identificador es un entero
    nombre = row['Nombre']
    nombre_carpeta = f"{numero} {nombre}"
    directorio = os.path.join(desktop_path, nombre_carpeta)
    
    # Crea la carpeta si no existe y guarda la ruta
    if not os.path.exists(directorio):
        os.makedirs(directorio)
        print(f"Carpeta creada: {directorio}")
    else:
        print(f"La carpeta {directorio} ya existe.")
    
    # Actualiza el diccionario con la ruta de la carpeta creada
    rutas_carpeta[nombre_carpeta] = directorio

# Luego, crear las carpetas subordinadas (con padre)
for index, row in df[df['Padre'].notna()].iterrows():
    numero = int(row['Numero'])  # Asegurarse de que el identificador es un entero
    nombre = row['Nombre']
    padre = int(row['Padre'])
    nombre_carpeta = f"{numero} {nombre}"
    
    # Encuentra la ruta del padre
    padre_nombre = f"{padre} {df[df['Numero'] == padre]['Nombre'].values[0]}"
    ruta_padre = rutas_carpeta.get(padre_nombre)
    
    if ruta_padre:
        directorio = os.path.join(ruta_padre, nombre_carpeta)
        # Crea la carpeta si no existe y guarda la ruta
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"Carpeta creada: {directorio}")
        else:
            print(f"La carpeta {directorio} ya existe.")
        
        # Actualiza el diccionario con la ruta de la carpeta creada
        rutas_carpeta[nombre_carpeta] = directorio
    else:
        print(f"No se encontró la ruta para el padre {padre_nombre}. La carpeta {nombre_carpeta} no se creó.")

# Mensaje final
print("Proceso finalizado.")

# Pausa para permitir al usuario ver el resultado
input("Presiona Enter para cerrar la ventana...")

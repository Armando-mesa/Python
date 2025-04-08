import pandas as pd
from pathlib import Path
from pandas import ExcelWriter

# Paso 1: Pedir la ruta del archivo .xlsx
ruta_archivo = Path(input("Introduce la ruta completa del archivo .xlsx: ").strip())

# Verificar si el archivo existe
if not ruta_archivo.exists():
    print("El archivo no existe. Revisa la ruta.")
    exit()

# Leer el archivo Excel
print("Cargando el archivo...")
df = pd.read_excel(ruta_archivo)

# Convertir los nombres de las columnas a mayúsculas para uniformidad
df.columns = df.columns.str.upper()

# Paso 2: Mostrar las columnas enumeradas
print("\nColumnas del archivo:")
for i, col in enumerate(df.columns):
    print(f"{i}: {col}")

# Pedir el número de la columna a dividir
try:
    indice_columna = int(input("\nIntroduce el número de la columna que quieres dividir por comas: "))
    columna_a_split = df.columns[indice_columna]
except (ValueError, IndexError):
    print("Número de columna inválido.")
    exit()

# Paso 3: Expandir las filas según los valores separados por comas
print("Expandiendo las filas...")
df_expanded = (
    df.assign(**{columna_a_split: df[columna_a_split].str.split(',')})  # Dividir la columna en listas
      .explode(columna_a_split)  # Crear una fila por cada elemento de la lista
      .reset_index(drop=True)  # Reiniciar el índice
)

# Agregar una columna ID para identificar las filas originales
df_expanded['ID'] = df_expanded.groupby(level=0).cumcount()

# Mover la columna ID a la primera posición
columnas = ['ID'] + [col for col in df_expanded.columns if col != 'ID']
df_expanded = df_expanded[columnas]

# Ordenar los datos por DB_USER y STATEMENT_HASH (ajusta los nombres según tus columnas)
if 'DB_USER' in df_expanded.columns and 'STATEMENT_HASH' in df_expanded.columns:
    df_expanded = df_expanded.sort_values(by=['DB_USER', 'STATEMENT_HASH'])

# Paso 4: Crear la carpeta "Usuarios" para guardar los archivos
carpeta_usuarios = ruta_archivo.parent / "Usuarios"
carpeta_usuarios.mkdir(exist_ok=True)  # Crear la carpeta si no existe

# Generar un archivo Excel por cada usuario con múltiples hojas si es necesario
if 'DB_USER' not in df_expanded.columns:
    print("La columna 'DB_USER' no existe en el archivo. No se pueden generar archivos por usuario.")
    exit()

print("Generando un archivo Excel por cada usuario...")
usuarios = df_expanded['DB_USER'].unique()  # Obtener la lista de usuarios únicos
max_filas = 1_048_576  # Límite de filas por hoja en Excel

for usuario in usuarios:
    df_usuario = df_expanded[df_expanded['DB_USER'] == usuario]  # Filtrar los datos por usuario
    nombre_archivo = f"{usuario}.xlsx"  # Nombre del archivo basado en el usuario
    ruta_usuario = carpeta_usuarios / nombre_archivo  # Guardar dentro de la carpeta "Usuarios"

    # Guardar el archivo Excel para el usuario con múltiples hojas si es necesario
    with ExcelWriter(ruta_usuario, engine='xlsxwriter') as writer:
        for i in range(0, len(df_usuario), max_filas):
            parte = df_usuario.iloc[i:i + max_filas]
            hoja_nombre = f"Parte_{i // max_filas + 1}"  # Nombre de la hoja
            parte.to_excel(writer, sheet_name=hoja_nombre, index=False)
    print(f"Archivo generado para el usuario '{usuario}': {ruta_usuario}")

print("\nArchivos generados exitosamente en la carpeta 'Usuarios'.")
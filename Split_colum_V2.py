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

# Ordenar los datos por db_user y statement_hash (ajusta los nombres según tus columnas)
if 'db_user' in df_expanded.columns and 'statement_hash' in df_expanded.columns:
    df_expanded = df_expanded.sort_values(by=['db_user', 'statement_hash'])

# Paso 4: Guardar el archivo en múltiples hojas de Excel
nombre_archivo = ruta_archivo.stem
ruta_excel = ruta_archivo.parent / f"{nombre_archivo}_split.xlsx"

max_filas = 1_048_576  # Límite de filas por hoja en Excel
print("Guardando el archivo en múltiples hojas de Excel...")

with ExcelWriter(ruta_excel, engine='xlsxwriter') as writer:
    for i in range(0, len(df_expanded), max_filas):
        parte = df_expanded.iloc[i:i + max_filas]
        hoja_nombre = f"Parte_{i // max_filas + 1}"  # Nombre de la hoja
        parte.to_excel(writer, sheet_name=hoja_nombre, index=False)
    print(f"Archivo Excel guardado como: {ruta_excel}")

print(f"\nArchivo guardado exitosamente en: {ruta_excel}")
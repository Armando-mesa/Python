import pandas as pd
from pathlib import Path

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

# Paso 4: Guardar el archivo como CSV (compatible con Excel)
nombre_archivo = ruta_archivo.stem
nuevo_nombre = f"{nombre_archivo}_expanded.csv"
ruta_salida = ruta_archivo.parent / nuevo_nombre

print("Guardando el archivo...")
df_expanded.to_csv(ruta_salida, index=False, encoding='utf-8-sig')  # UTF-8 con BOM para compatibilidad con Excel

print(f"\nArchivo guardado como: {ruta_salida}")
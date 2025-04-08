import pandas as pd
import shutil

# Ruta del archivo Excel
excel_path = r'C:\Users\luisarmando.mesa\Desktop\uno\path.xlsx'

print(f"Leyendo desde el archivo Excel: {excel_path}")

# Intentamos imprimir el contenido del archivo Excel
try:
    # Especificamos header=None para que pandas no use la primera fila como nombres de columna
    df = pd.read_excel(excel_path, header=None, names=['Ruta_Origen', 'Ruta_Destino'])
    print("Contenido del archivo Excel:")
    print(df)
except Exception as excel_error:
    print(f"Error al leer el archivo Excel: {excel_error}")

# Iterar sobre las filas y copiar los archivos
for index, row in df.iterrows():
    ruta_origen = row['Ruta_Origen']
    ruta_destino = row['Ruta_Destino']

    print(f"Copiando desde {ruta_origen} a {ruta_destino}")

    try:
        shutil.copy(ruta_origen, ruta_destino)
        print(f"Archivo {ruta_origen} copiado exitosamente a {ruta_destino}")
    except Exception as e:
        print(f"Error al copiar archivo {ruta_origen}: {e}")

print("Proceso completado.")
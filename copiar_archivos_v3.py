import pandas as pd
import shutil
import os

# Ruta del archivo Excel original
excel_path = r'C:\Users\luisarmando.mesa\Desktop\uno\path.xlsx'

print(f"Leyendo desde el archivo Excel: {excel_path}")

# Intentamos imprimir el contenido del archivo Excel
try:
    # Especificamos header=None para que pandas no use la primera fila como nombres de columna
    df = pd.read_excel(excel_path, header=None, names=['Ruta_Origen', 'Ruta_Destino_1', 'Ruta_Destino_2'])
    print("Contenido del archivo Excel:")
    print(df)
except Exception as excel_error:
    print(f"Error al leer el archivo Excel: {excel_error}")

# Listas para almacenar las rutas de archivos copiados y no encontrados
archivos_copiados = []
archivos_no_encontrados = []

# Iterar sobre las filas y copiar los archivos
for index, row in df.iterrows():
    ruta_origen = row['Ruta_Origen']
    ruta_destino_1 = row['Ruta_Destino_1']
    ruta_destino_2 = row['Ruta_Destino_2']

    print(f"Copiando desde {ruta_origen} a {ruta_destino_1} y {ruta_destino_2}")

    try:
        # Verificar si las rutas de destino existen, y si no, crearlas
        for ruta_destino in [ruta_destino_1, ruta_destino_2]:
            if not os.path.exists(os.path.dirname(ruta_destino)):
                os.makedirs(os.path.dirname(ruta_destino))

            shutil.copy(ruta_origen, ruta_destino)
            print(f"Archivo {ruta_origen} copiado exitosamente a {ruta_destino}")

            # Agregar la ruta a la lista de archivos copiados
            archivos_copiados.append(ruta_destino)
    except Exception as e:
        print(f"Error al copiar archivo {ruta_origen}: {e}")

        # Agregar la ruta a la lista de archivos no encontrados
        archivos_no_encontrados.append(ruta_origen)

# Asegurarse de que ambas listas tengan la misma longitud
max_length = max(len(archivos_copiados), len(archivos_no_encontrados))
archivos_copiados.extend([''] * (max_length - len(archivos_copiados)))
archivos_no_encontrados.extend([''] * (max_length - len(archivos_no_encontrados)))

# Crear un DataFrame con las rutas de archivos copiados y no encontrados
df_resultado = pd.DataFrame({
    'Archivos Copiados': archivos_copiados,
    'Archivos No Encontrados': archivos_no_encontrados
})

# Guardar el DataFrame en un archivo Excel
df_resultado.to_excel('resultado_copia_archivos.xlsx', index=False)

print("Proceso completado.")
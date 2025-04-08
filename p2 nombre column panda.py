import pandas as pd

# Cargar archivo Excel
excel_path = 'C:\\Users\\luisarmando.mesa\\OneDrive - Grupo VASS\\Documents\\Python\\Rutas projectos.xlsx'
df = pd.read_excel(excel_path)

# Imprimir los nombres de las columnas
print("Columnas disponibles:")
print(df.columns)
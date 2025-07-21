import os
import glob
import pandas as pd

# === CONFIGURACIÓN DE RUTAS Y CARPETAS ===

# Ruta predeterminada de la carpeta de descargas del usuario
carpeta_descargas = os.path.expanduser("~/Downloads")

# Crear subcarpetas para organizar los archivos clasificados
carpeta_proyectos = os.path.join(carpeta_descargas, "proyectos")
carpeta_actividades = os.path.join(carpeta_descargas, "actividades")

# Crear las carpetas si no existen
os.makedirs(carpeta_proyectos, exist_ok=True)
os.makedirs(carpeta_actividades, exist_ok=True)

# === BUSCAR ARCHIVOS CSV ===

# Buscar todos los archivos .csv en la carpeta de descargas
archivos_csv = glob.glob(os.path.join(carpeta_descargas, "*.csv"))

# Lista para guardar los DataFrames que contienen la primera fila de cada CSV
dataframes = []

# === EXTRAER PRIMERA FILA DE CADA ARCHIVO CSV ===
for archivo in archivos_csv:
    try:
        # Leer únicamente la primera fila, sin encabezados
        df_primera = pd.read_csv(archivo, encoding='utf-8', sep=',', nrows=1, header=None)

        # Mostrar la primera fila por consola
        print(f"Archivo: {os.path.basename(archivo)}")
        print(df_primera)
        print("-" * 50)

        # Agregar la primera fila a la lista
        dataframes.append(df_primera)
    except Exception as e:
        print(f"Error leyendo primera fila de {os.path.basename(archivo)}: {e}")

# === GUARDAR TODAS LAS PRIMERAS FILAS EN UN SOLO ARCHIVO XLSX ===

if dataframes:
    # Unir todas las primeras filas en un solo DataFrame
    df_final = pd.concat(dataframes, ignore_index=True)

    # Ruta de salida para el archivo unificado
    ruta_unificado = os.path.join(carpeta_descargas, "primeras_filas_unificadas.xlsx")

    # Guardar el archivo unificado en formato Excel (sin encabezados)
    df_final.to_excel(ruta_unificado, index=False, header=False, engine='openpyxl')
    print(f"\nArchivo unificado guardado en: {ruta_unificado}")
else:
    print("No se encontraron primeras filas válidas para procesar.")

# === CONVERTIR CSV A XLSX Y CLASIFICAR SEGÚN CANTIDAD DE COLUMNAS ===

for archivo in archivos_csv:
    try:
        # Leer el CSV completo
        df = pd.read_csv(archivo, encoding='utf-8', sep=',')

        # Contar la cantidad de columnas
        num_columnas = len(df.columns)

        # Clasificación:
        # - 62 columnas exactas: proyectos
        # - Más de 62 columnas: actividades
        if num_columnas == 62:
            carpeta_destino = carpeta_proyectos
        elif num_columnas > 62:
            carpeta_destino = carpeta_actividades
        else:
            print(f"Archivo ignorado (menos de 62 columnas): {os.path.basename(archivo)}")
            continue

        # Obtener el nombre base del archivo sin extensión
        nombre_base = os.path.splitext(os.path.basename(archivo))[0]

        # Definir la ruta de salida como archivo .xlsx
        ruta_salida = os.path.join(carpeta_destino, f"{nombre_base}.xlsx")

        # Guardar en formato Excel
        df.to_excel(ruta_salida, index=False, engine='openpyxl')
        print(f"Archivo convertido guardado: {ruta_salida}")

    except Exception as e:
        print(f"Error procesando {os.path.basename(archivo)}: {e}")

# === FUNCIÓN PARA UNIFICAR Y ORDENAR ARCHIVOS XLSX EN UNA CARPETA ===

def unificar_y_ordenar_xlsx(carpeta, nombre_salida):
    """
    Busca todos los archivos .xlsx en una carpeta,
    los concatena en un solo archivo y los ordena alfabéticamente
    por la primera columna (columna A).
    """

    # Buscar todos los archivos .xlsx en la carpeta especificada
    archivos_xlsx = glob.glob(os.path.join(carpeta, "*.xlsx"))
    hojas_unificadas = []

    # Recorrer todos los archivos encontrados
    for i, archivo in enumerate(archivos_xlsx):
        try:
            # Leer el primer archivo con encabezado
            if i == 0:
                df = pd.read_excel(archivo, engine='openpyxl')
            else:
                # Leer los siguientes archivos omitiendo encabezado duplicado
                df = pd.read_excel(archivo, engine='openpyxl', header=0)

            hojas_unificadas.append(df)
        except Exception as e:
            print(f"Error leyendo {os.path.basename(archivo)}: {e}")

    # Verificar si hay datos para unir
    if hojas_unificadas:
        # Unir todos los DataFrames en uno solo
        df_merged = pd.concat(hojas_unificadas, ignore_index=True)

        # Ordenar por la primera columna (alfabéticamente de A a Z)
        df_ordenado = df_merged.sort_values(by=df_merged.columns[0], ascending=True)

        # Definir la ruta de salida del archivo unificado
        ruta_final = os.path.join(carpeta, nombre_salida)

        # Guardar el archivo ordenado
        df_ordenado.to_excel(ruta_final, index=False, engine='openpyxl')
        print(f"✅ Archivo unificado y ordenado guardado: {ruta_final}")
    else:
        print(f"No se encontraron archivos .xlsx válidos en la carpeta: {carpeta}")

# === EJECUTAR LA FUNCIÓN DE UNIFICACIÓN Y ORDENAMIENTO ===

# Procesar la carpeta de proyectos
unificar_y_ordenar_xlsx(carpeta_proyectos, "proyectos_unificado.xlsx")

# Procesar la carpeta de actividades
unificar_y_ordenar_xlsx(carpeta_actividades, "actividades_unificado.xlsx")

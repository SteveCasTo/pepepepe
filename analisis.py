import pandas as pd
from collections import Counter
import os

def generar_nombres_clusters(df):
    nombres_clusters = {}
    for cluster in sorted(df['cluster'].unique()):
        # Obtener noticias del cluster actual
        noticias_cluster = df[df['cluster'] == cluster]['news_clean']

        # Contar palabras más frecuentes
        palabras = " ".join(noticias_cluster).split()
        if palabras:  # Validar que haya palabras en el cluster
            palabra_frecuente = Counter(palabras).most_common(1)[0][0]
        else:
            palabra_frecuente = "Sin-datos"
        
        nombres_clusters[cluster] = f"{palabra_frecuente}"
    
    return nombres_clusters


def reporte_palabras_frecuentes(df):
    os.makedirs("reportes_clusters", exist_ok=True)  # Crear carpeta para reportes

    for cluster in sorted(df['cluster'].unique()):
        # Obtener noticias del cluster actual
        noticias_cluster = df[df['cluster'] == cluster]['news_clean']

        # Contar palabras más frecuentes
        palabras = " ".join(noticias_cluster).split()
        palabras_frecuentes = Counter(palabras).most_common(10)

        # Crear el reporte
        with open(f"reportes_clusters/reporte_cluster_{cluster}.txt", "w") as f:
            f.write(f"Reporte para Cluster {cluster}:\n")
            f.write("Palabras más frecuentes:\n")
            for palabra, frecuencia in palabras_frecuentes:
                f.write(f"{palabra}: {frecuencia}\n")
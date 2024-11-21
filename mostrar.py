import pandas as pd
import tkinter as tk
from tkinter import scrolledtext

def show_news(csv_file):
    # Cargar el archivo CSV
    df = pd.read_csv(csv_file)

    # Validar y limpiar datos
    df['news_clean'] = df['news_clean'].fillna("").astype(str)
    df['news'] = df['news'].fillna("").astype(str)
    df['cluster_name'] = df['cluster_name'].fillna("Cluster-desconocido")

    # Agrupar las noticias por su número de cluster
    clustered_news = df.groupby('cluster')['news'].apply(list).reset_index()
    if 'cluster_name' not in df.columns:
        raise ValueError("El archivo CSV no contiene la columna 'cluster_name'.")
    cluster_names = dict(zip(df['cluster'], df['cluster_name']))

    
    frequent_words = df.groupby('cluster')['news_clean'].apply(
        lambda news: " ".join(news).split()
    ).apply(
        lambda words: ", ".join(pd.Series(words).value_counts().head(5).index) if words else "Sin palabras frecuentes"
    )

    # Crear la ventana principal de Tkinter
    root = tk.Tk()
    root.title("Noticias por Cluster")
    root.geometry("900x700")

    # Función que se llama cuando se hace clic en un cluster
    def show_news_cluster(cluster):
        # Limpiar el área de texto
        news_text.delete(1.0, tk.END)

        # Obtener las noticias del cluster seleccionado
        news_list = clustered_news[clustered_news['cluster'] == cluster]['news'].values[0]

        # Mostrar las palabras más frecuentes del cluster
        news_text.insert(tk.END, f"Palabras frecuentes del cluster '{cluster_names[cluster]}':\n")
        news_text.insert(tk.END, f"{frequent_words[cluster]}\n")
        news_text.insert(tk.END, "-"*80 + "\n\n")

        # Mostrar las noticias
        for i, news in enumerate(news_list):
            news_text.insert(tk.END, f"Noticia {i+1}:\n{news}\n")
            news_text.insert(tk.END, "="*80 + "\n\n")

    # Frame izquierdo para los números de los clusters
    frame_left = tk.Frame(root, width=200)
    frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10)

    # Frame derecho para mostrar las noticias
    frame_right = tk.Frame(root)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

    # Crear los botones para los clusters
    for cluster in clustered_news['cluster']:
        cluster_name = cluster_names[cluster]
        button = tk.Button(
            frame_left, text=cluster_name, width=20, 
            command=lambda c=cluster: show_news_cluster(c)
        )
        button.pack(pady=5)

    # Crear un área de texto con barra de desplazamiento para mostrar las noticias
    news_text = scrolledtext.ScrolledText(frame_right, wrap=tk.WORD, width=70, height=30)
    news_text.pack(expand=True, fill=tk.BOTH)

    # Ejecutar la aplicación
    root.mainloop()
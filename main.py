import preprocesar
import kmeans
import pca
import mostrar
import analisis  # Nuevo módulo para análisis de clusters
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

def main():
    print("Comenzando el análisis de noticias...")

    # Cargar los datos
    archivo_csv = './dataset-news.csv'  # Cambia esta ruta por la ubicación de tu archivo
    df = preprocesar.cargar_datos(archivo_csv)

    # Convertir el texto a vectores
    vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
    X = vectorizer.fit_transform(df['news_clean'])
    X = normalize(X, norm='l2')

    # Ejecutar K-Means
    kmeans_model = kmeans.buscar_mejor_kmeans(X, min_clusters=2, max_clusters=15, n_iteraciones=5)

    # Asignar el cluster a cada noticia
    df['cluster'] = kmeans_model.predict(X)

    # Generar nombres para los clusters
    cluster_names = analisis.generar_nombres_clusters(df)
    df['cluster_name'] = df['cluster'].map(lambda x: f"{cluster_names[x]}")

    # Generar reporte de palabras frecuentes
    analisis.reporte_palabras_frecuentes(df)

    # Reducir la dimensionalidad para visualización
    X_pca = pca.reducir_dimensionalidad(X)

    # Visualizar los clusters
    pca.visualizar_clusters(X_pca, df)

    # Guardar los resultados finales
    df.to_csv('resultado-no-supervisado.csv', index=False)
    print("Clasificación completada. Resultados guardados en 'resultado-no-supervisado.csv'")

    # Mostrar los resultados en pantalla
    mostrar.show_news("./resultado-no-supervisado.csv")

if __name__ == "__main__":
    main()
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# Reducir la dimensionalidad para visualización
def reducir_dimensionalidad(X):
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X.toarray())
    return X_pca

# Función para visualizar los clusters
def visualizar_clusters(X_pca, df):
    plt.figure(figsize=(10, 8))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['cluster'], cmap='viridis')
    plt.title('Visualización de Clusters con K-Means')
    plt.xlabel('Componente Principal 1')
    plt.ylabel('Componente Principal 2')
    plt.colorbar()
    plt.show()
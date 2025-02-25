from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, OPTICS, AgglomerativeClustering
import matplotlib.pyplot as plt
import seaborn as sns
import os

class PokemonClustering:
    def __init__(self, data):
        self.data = data
        self.cluster_labels = None
        self.kmeans = None
    # Ho deciso di basare il clustering sugli Hp e il Damage del pokemon
    def preprocess_features(self):
        features = self.data[['hp', 'AVG_damage']]
        self.scaler = StandardScaler()
        return self.scaler.fit_transform(features)
    # Mi serve per vedere graficamente quanti cluster mi ottimizzano la suddivisione 
    def elbow_method(self, max_clusters=10):
        X = self.preprocess_features()
        distortions = []
        for i in range(1, max_clusters + 1):
            kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
            kmeans.fit(X)
            distortions.append(kmeans.inertia_)
        # Plotto tutto a schermo
        plt.figure(figsize=(10, 6))
        plt.plot(range(1, max_clusters + 1), distortions, marker='o')
        plt.xlabel('Numero di Cluster')
        plt.ylabel('Distorsione')
        plt.title('Elbow Method')
        plt.show()


    # Scrivo 4 metodi per applicare il clustering con Kmeans,Dbscan,Optics, e cluster Gerarchico

    def apply_kmeans(self, n_clusters=3):
        X = self.preprocess_features()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.cluster_labels = self.kmeans.fit_predict(X)
        self.data['cluster'] = self.cluster_labels

    def apply_dbscan(self, eps=0.5, min_samples=5):
        X = self.preprocess_features()
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        self.cluster_labels = dbscan.fit_predict(X)
        self.data['cluster'] = self.cluster_labels

    def apply_optics(self, min_samples=5, xi=0.05, min_cluster_size=0.1):
        X = self.preprocess_features()
        optics = OPTICS(min_samples=min_samples, xi=xi, min_cluster_size=min_cluster_size)
        self.cluster_labels = optics.fit_predict(X)
        self.data['cluster'] = self.cluster_labels

    def apply_agglomerative(self, n_clusters=3):
        X = self.preprocess_features()
        agglomerative = AgglomerativeClustering(n_clusters=n_clusters)
        self.cluster_labels = agglomerative.fit_predict(X)
        self.data['cluster'] = self.cluster_labels

    # Metodo da richiamare nel main per poter scegliere che tipo di clusterizzazione utilizzare
    def cluster(self, method='kmeans', **kwargs):
        if method == 'kmeans':
            self.apply_kmeans(**kwargs)
        elif method == 'dbscan':
            self.apply_dbscan( eps=0.5, min_samples=5)
        elif method == 'optics':
            self.apply_optics( min_samples=5, xi=0.05, min_cluster_size=0.1)
        elif method == 'agglomerative':
            self.apply_agglomerative(**kwargs)
        else:
            raise ValueError(f"Clustering method '{method}' is not supported.")

    # Visualizzo tutti i punti del cluster tramite una PCA a 2 dimensioni e evidenzio i centroidi 
    def visualize_clusters(self):
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(self.preprocess_features())
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=self.cluster_labels, palette='viridis', legend='full')
        if hasattr(self.kmeans, 'cluster_centers_'):
            centers_pca = pca.transform(self.kmeans.cluster_centers_)
            plt.scatter(centers_pca[:, 0], centers_pca[:, 1], s=300, c='red', marker='X', label='Centroidi')
        
        plt.xlabel('PCA 1')
        plt.ylabel('PCA 2')
        plt.title('Visualizzazione Clustering con PCA')
        plt.legend(title='Cluster')
        plt.show()

    # Per praticita ho creato una funzione che mi salvi la suddivisone dei pokemon nei cluster in un file.txt
    def save_clusters_to_file(self, filename='list.txt'):
        parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        file_path = os.path.join(parent_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            for cluster in sorted(self.data['cluster'].unique()):
                file.write(f'Cluster {cluster}:\n')
                pokemon_names = self.data[self.data['cluster'] == cluster]['name'].tolist()
                for name in pokemon_names:
                    file.write(f'{name}\n')
                file.write('\n')
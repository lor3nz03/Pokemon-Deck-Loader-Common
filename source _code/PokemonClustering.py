from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

class PokemonClustering:
    def __init__(self, data):
        self.data = data
        self.cluster_labels = None
        self.kmeans = None

    def preprocess_features(self):
        features = self.data[['hp', 'AVG_damage']]
        self.scaler = StandardScaler()
        return self.scaler.fit_transform(features)

    def apply_kmeans(self, n_clusters=3):
        X = self.preprocess_features()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self.cluster_labels = self.kmeans.fit_predict(X)
        self.data['cluster'] = self.cluster_labels

    def visualize_clusters(self):
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(self.preprocess_features())
        
        plt.figure(figsize=(10,6))
        sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=self.cluster_labels, palette='viridis')
        plt.xlabel('PCA 1')
        plt.ylabel('PCA 2')
        plt.title('Visualizzazione Clustering con PCA')
        plt.legend()
        plt.show()
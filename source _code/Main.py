from DataPreprocessor import DataPreprocessor
from PokemonClustering import PokemonClustering
from DeckBuilder import DeckBuilder
import os

class Main:
    def run(self):
        # Step 1: Preprocessing
        csv_path = os.path.join("..", "CSV", "pokemon-tcg-data-master 1999-2023.csv")
        preprocessor = DataPreprocessor(csv_path)
        preprocessor.load_data()
        preprocessor.clean_data()
        preprocessor.save_data('new.csv')
        processed_data = preprocessor.get_processed_data()
        
        # Step 2: Clustering
        #clustering = PokemonClustering(processed_data)
        #clustering.apply_kmeans(n_clusters=3)
        #clustering.visualize_clusters()


        # Step 3: Deck Building
        #deck_builder = DeckBuilder(processed_data)
        #deck_builder.create_balanced_deck()

if __name__ == '__main__':
    Main().run()
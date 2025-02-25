from DataPreprocessor import DataPreprocessor
from PokemonClustering import PokemonClustering
from DeckBuilder import DeckBuilder
import os

class Main:
    def run(self):

        # PASSAGGIO 1: PREPROCESSING

        # Richiamo in ordine tutti i metodi per effettuare il preprocessing
        csv_path = os.path.join("..", "CSV", "pokemon-tcg-data-master 1999-2023.csv")
        preprocessor = DataPreprocessor(csv_path)
        preprocessor.load_data()

        # Plotto #artisti,#tipi,#generazioni
        preprocessor.plot_cards_by_artist()
        preprocessor.plot_pokemon_by_generation()
        preprocessor.plot_pokemon_by_type()

        # Effettuo la pulizia del Dataset originario
        preprocessor.clean_data()
        preprocessor.save_data('new.csv')
        processed_data = preprocessor.get_processed_data()
        
        # PASSAGGIO 2: CLUSTERING

        clustering = PokemonClustering(processed_data)
        # Determina il numero ottimale di cluster
        clustering.elbow_method(max_clusters=10) 
        optimal_clusters = 3 

        # Dopo alcune prove kmeans separa meglio i pokemon in cluster
        clustering.cluster(method='kmeans', n_clusters=optimal_clusters)
        clustering.visualize_clusters()
        clustering.save_clusters_to_file('list.txt')


        # PASSAGGIO 3: DECK BUILDING

        deck_builder = DeckBuilder(processed_data)
        # Salvo in una variabile il tipo di deck che l'utente vuole creare
        pokemon_type = deck_builder.get_valid_pokemon_type(preprocessor)
        
        # Crea e visualizza sia su terminale che in grafico i deck creati 
        balanced_deck = deck_builder.create_balanced_deck(pokemon_type)
        deck_builder.print_decks(balanced_deck)
        deck_builder.visualize_decks(balanced_deck)

    


if __name__ == '__main__':
    Main().run()
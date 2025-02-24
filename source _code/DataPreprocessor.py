import pandas as pd
import numpy as np
import ast
from pathlib import Path
import matplotlib.pyplot as plt

class DataPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        # Carica i dati
        self.data = pd.read_csv(self.file_path)

    def build_evolution_hierarchy(self):

        evolution_dict = {}

        # Riempio il dizionario con le relazioni dei pokemon con la colonna evolveTo
        for _, row in self.data.iterrows():
            pokemon_name = row['name']
            evolves_to = ast.literal_eval(row['evolvesTo']) if not pd.isna(row['evolvesTo']) else []

            if evolves_to:
                if pokemon_name not in evolution_dict:
                    evolution_dict[pokemon_name] = []
                evolution_dict[pokemon_name].extend(evolves_to)

        # Creo una collona ausiliaria per creare successivamente la catena evolutiva dei pokemon
        def get_full_evolution_chain(pokemon_name, visited=None):
            if visited is None:
                visited = set()
            if pokemon_name in visited:
                return []
            visited.add(pokemon_name)
            chain = [pokemon_name]
            if pokemon_name in evolution_dict:
                for evolved_pokemon in evolution_dict[pokemon_name]:
                    chain.extend(get_full_evolution_chain(evolved_pokemon, visited))
            return chain

        self.data['evolveTo2'] = self.data.apply(
            lambda row: ", ".join(get_full_evolution_chain(row['name'])[1:]) if 'Basic' in row['subtypes'] else '', axis=1
        )

        # Creazione della colonna per le evoluzioni dei pokemon
        def get_evolution_chain(pokemon_name, visited=None):
            if visited is None:
                visited = set()
            if pokemon_name in visited:
                return []
            visited.add(pokemon_name)
            chain = [pokemon_name]
            if pokemon_name in evolution_dict:
                for evolved_pokemon in evolution_dict[pokemon_name]:
                    chain.extend(get_evolution_chain(evolved_pokemon, visited))
            return chain

        self.data['gerarchic'] = self.data.apply(
            lambda row: ", ".join(get_evolution_chain(row['name'])) if 'Basic' in row['subtypes'] else '', axis=1
        )

    def clean_data(self):
        # Filtro solo i Pokémon
        self.data = self.data[self.data['supertype'] == 'Pokémon']

        # Rimuovo i Pokémon con rarità diversa da "Rare Holo", "Rare", "Uncommon", "Common"
        allowed_rarities = ['Rare Holo', 'Rare', 'Uncommon', 'Common']
        self.data = self.data[self.data['rarity'].isin(allowed_rarities)]

        # Rimuovo i Pokémon che non sono di subtypes "Basic", "Stage 1", "Stage 2"
        allowed_subtypes = ['Basic', 'Stage 1', 'Stage 2']
        def filter_subtypes(subtypes):
            try:
                subtypes_list = ast.literal_eval(subtypes)
                if isinstance(subtypes_list, list) and all(subtype in allowed_subtypes for subtype in subtypes_list):
                    return True
            except (ValueError, SyntaxError):
                pass
            return False

        # Rimozione colonne inutile per le task che dobbiamo fare 
        self.data = self.data[self.data['subtypes'].apply(filter_subtypes)]
        cols_to_remove = ['set', 'series', 'publisher', 'release_date', 'artist', 'set_num', 'level', 
                          'abilities', 'retreatCost', 'convertedRetreatCost', 'flavorText', 
                          'nationalPokedexNumbers', 'legalities', 'resistances', 'rules', 
                          'regulationMark', 'ancientTrait','weaknesses','evolvesFrom']
        self.data.drop(columns=cols_to_remove, inplace=True, errors='ignore')
        
        # Estrazione delle feature "attack_name" e "AVG_damage" dalla colonna "attacks"
        #Utilizzo libreria ast
        if 'attacks' in self.data.columns:
            def extract_attack_data(attacks):
                if isinstance(attacks, str):
                    try:
                        attacks = ast.literal_eval(attacks)
                    except (ValueError, SyntaxError):
                        return "", 0  # Se non è valido, restituisci vuoto e danno zero
                if isinstance(attacks, list):
                    attack_names = [atk.get('name', '') for atk in attacks if isinstance(atk, dict)]
                    attack_damages = [int(atk.get('damage', '0')) for atk in attacks if isinstance(atk, dict) and atk.get('damage', '0').isdigit()]
                    avg_damage = np.mean(attack_damages) if attack_damages else 0
                    return "|".join(attack_names), avg_damage
                return "", 0

            self.data[['attack_name', 'AVG_damage']] = self.data['attacks'].apply(lambda x: pd.Series(extract_attack_data(x)))

        # Rimuovo la colonna originale "attacks"
        self.data.drop(columns=['attacks'], inplace=True, errors='ignore')

        # Se ci sono valori nulli ho deciso di non eliminarli 
        self.data.fillna({'hp': 0, 'types': 'Unknown', 'rarity': 'Common', 'evolvesFrom': '', 'AVG_damage': 0}, inplace=True)
        self.data['hp'] = pd.to_numeric(self.data['hp'], errors='coerce').fillna(0)
        # I valori di AVG_damage non devono essere zero
        self.data['AVG_damage'] = self.data['AVG_damage'].replace(0, self.data['AVG_damage'].mean())
        # Arrotondo i valori di AVG_damage a numeri interi
        self.data['AVG_damage'] = self.data['AVG_damage'].round().astype(int)
        # Richiamo il metodo per creare la colonna delle evoluzioni
        self.build_evolution_hierarchy()
        # Cancello la colonna di supporto
        self.data.drop(columns='evolveTo2', inplace=True, errors='ignore')

    # Salvo tutte queste modifiche in un file CSV a parte per comodità di visualizzazione
    def save_data(self, output_file_name):
    
        base_dir = Path(__file__).resolve().parent.parent  # Sale di un livello
        output_dir = base_dir / "CSV"
        output_file_path = output_dir / output_file_name
        # Assicura che la cartella "CSV" esista
        output_dir.mkdir(parents=True, exist_ok=True)

        # Ordinamento dei dati per la visualizzazione utilizzati in fase di sviluppo
        #self.data = self.data.sort_values(by='subtypes')
        #self.data = self.data.sort_values(by='generation')

        # Salvo il file CSV
        self.data.to_csv(output_file_path, index=False, encoding="utf-8")

    # Mi è servita per scoprire quanti tipi di rarità esistono nel database 

    #def print_rarity_types(self):
        #rarity_types = self.data['rarity'].unique()
        #print("Unique Rarity Types:")
        #for rarity in rarity_types:
            #print(rarity)

    def get_processed_data(self):
        return self.data

    #Visualizzo a video in modo immediato il numero di pokemon divisi per generazioni
    def plot_pokemon_by_generation(self):
        generation_counts = self.data['generation'].value_counts().sort_index()
        generation_counts.plot(kind='bar', color='skyblue')
        plt.title('Number of Pokémon by Generation')
        plt.xlabel('Generation')
        plt.ylabel('Number of Pokémon')
        plt.xticks(rotation=0)
        plt.show()

    #Visualizzo a video in modo immediato il numero di pokemon divisi per artista
    def plot_cards_by_artist(self):
        artist_counts = self.data['artist'].value_counts().head(10)  # Plot top 10 artists
        artist_counts.plot(kind='bar', color='lightgreen')
        plt.title('Number of Cards by Artist')
        plt.xlabel('Artist')
        plt.ylabel('Number of Cards')
        plt.xticks(rotation=45, ha='right')
        plt.show()

    #Visualizzo a video in modo immediato il numero di pokemon divisi per tipo
    def plot_pokemon_by_type(self):
        self.data['types'] = self.data['types'].astype(str)  # Tramite questa linea di codice mi assicuro che sono tutte stringhe
        type_counts = self.data['types'].apply(lambda x: x.strip("[]").replace("'", "").split(", ")).explode().value_counts()
        type_counts.plot(kind='bar', color='salmon')
        plt.title('Number of Pokémon by Type')
        plt.xlabel('Type')
        plt.ylabel('Number of Pokémon')
        plt.xticks(rotation=45, ha='right')
        plt.show()
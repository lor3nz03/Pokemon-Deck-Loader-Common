import pandas as pd
import numpy as np
import ast
from pathlib import Path

class DataPreprocessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load_data(self):
        # Carica i dati
        self.data = pd.read_csv(self.file_path)

    def build_evolution_hierarchy(self):
        # Create a dictionary to store the evolution hierarchy
        evolution_dict = {}

        # Populate the dictionary with evolvesTo relationships
        for _, row in self.data.iterrows():
            pokemon_name = row['name']
            evolves_to = ast.literal_eval(row['evolvesTo']) if not pd.isna(row['evolvesTo']) else []

            if evolves_to:
                if pokemon_name not in evolution_dict:
                    evolution_dict[pokemon_name] = []
                evolution_dict[pokemon_name].extend(evolves_to)

        # Create the evolveTo2 column for Basic Pokémon
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

        # Create the gerarchic column based on the evolution hierarchy
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
        # Filtrare solo i Pokémon
        self.data = self.data[self.data['supertype'] == 'Pokémon']

        # Rimuovere i Pokémon con rarità diversa da "Rare Holo", "Rare", "Uncommon", "Common"
        allowed_rarities = ['Rare Holo', 'Rare', 'Uncommon', 'Common']
        self.data = self.data[self.data['rarity'].isin(allowed_rarities)]

        # Rimuovere i Pokémon che non sono di subtypes "Basic", "Stage1", "Stage2"
        allowed_subtypes = ['Basic', 'Stage 1', 'Stage 2']

        def filter_subtypes(subtypes):
            try:
                subtypes_list = ast.literal_eval(subtypes)
                if isinstance(subtypes_list, list) and all(subtype in allowed_subtypes for subtype in subtypes_list):
                    return True
            except (ValueError, SyntaxError):
                pass
            return False

        self.data = self.data[self.data['subtypes'].apply(filter_subtypes)]

        cols_to_remove = ['set', 'series', 'publisher', 'release_date', 'artist', 'set_num', 'level', 
                          'abilities', 'retreatCost', 'convertedRetreatCost', 'flavorText', 
                          'nationalPokedexNumbers', 'legalities', 'resistances', 'rules', 
                          'regulationMark', 'ancientTrait','weaknesses','evolvesFrom']
        self.data.drop(columns=cols_to_remove, inplace=True, errors='ignore')
        
        # Estrarre "attack_name" e "AVG_damage" dalla colonna "attacks"
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

        # Rimuovere la colonna originale "attacks"
        self.data.drop(columns=['attacks'], inplace=True, errors='ignore')

        # Riempimento valori nulli
        self.data.fillna({'hp': 0, 'types': 'Unknown', 'rarity': 'Common', 'evolvesFrom': '', 'AVG_damage': 0}, inplace=True)
        self.data['hp'] = pd.to_numeric(self.data['hp'], errors='coerce').fillna(0)
        # Assicurarsi che i valori di AVG_damage non siano zero
        self.data['AVG_damage'] = self.data['AVG_damage'].replace(0, self.data['AVG_damage'].mean())
        # Arrotondare i valori di AVG_damage a numeri interi
        self.data['AVG_damage'] = self.data['AVG_damage'].round().astype(int)
        # Build the evolution hierarchy and create the gerarchic column
        self.build_evolution_hierarchy()
        self.data.drop(columns='evolveTo2', inplace=True, errors='ignore')

    def save_data(self, output_file_name):
        # Trova la cartella "Project" salendo da "source_code"
        base_dir = Path(__file__).resolve().parent.parent  # Sale di un livello

        # Percorso corretto della cartella CSV
        output_dir = base_dir / "CSV"

        # Percorso completo del file
        output_file_path = output_dir / output_file_name

        # Assicura che la cartella "CSV" esista
        output_dir.mkdir(parents=True, exist_ok=True)

        # Sort the DataFrame by the 'subtypes' column
        #self.data = self.data.sort_values(by='subtypes')
        #self.data = self.data.sort_values(by='generation')

        # Salva il file CSV
        self.data.to_csv(output_file_path, index=False, encoding="utf-8")

    def print_rarity_types(self):
        # Extract unique rarity types
        rarity_types = self.data['rarity'].unique()
        print("Unique Rarity Types:")
        for rarity in rarity_types:
            print(rarity)

    def get_processed_data(self):
        return self.data
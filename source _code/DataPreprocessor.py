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

        # Populate the dictionary with evolvesFrom and evolvesTo relationships within the same generation
        for _, row in self.data.iterrows():
            pokemon_name = row['name']
            generation = row['generation']
            evolves_from = str(row['evolvesFrom']) if not pd.isna(row['evolvesFrom']) else ''
            evolves_to = str(row['evolvesTo']) if not pd.isna(row['evolvesTo']) else ''

            if evolves_from:
                if evolves_from not in evolution_dict:
                    evolution_dict[evolves_from] = []
                evolution_dict[evolves_from].append((pokemon_name, generation))
            if evolves_to:
                if pokemon_name not in evolution_dict:
                    evolution_dict[pokemon_name] = []
                evolution_dict[pokemon_name].append((evolves_to, generation))

        # Create the gerarchic column based on the evolution hierarchy within the same generation
        def get_evolution_chain(pokemon_name, generation, visited=None):
            if visited is None:
                visited = set()
            if pokemon_name in visited:
                return []
            visited.add(pokemon_name)
            chain = [pokemon_name]
            if pokemon_name in evolution_dict:
                for evolved_pokemon, evolved_generation in evolution_dict[pokemon_name]:
                    if evolved_generation == generation:
                        chain.extend(get_evolution_chain(evolved_pokemon, generation, visited))
            return chain

        self.data['gerarchic'] = self.data.apply(
            lambda row: ", ".join(sorted(set(get_evolution_chain(row['name'], row['generation'])))) if 'Basic' in row['subtypes'] else '', axis=1
        )

    def clean_data(self):
        # Filtrare solo i Pokémon
        self.data = self.data[self.data['supertype'] == 'Pokémon']

        # Rimuovere i Pokémon con rarità diversa da "Rare Holo", "Rare", "Uncommon", "Common"
        allowed_rarities = ['Rare Holo', 'Rare', 'Uncommon', 'Common']
        self.data = self.data[self.data['rarity'].isin(allowed_rarities)]

        cols_to_remove = ['set', 'series', 'publisher', 'release_date', 'artist', 'set_num', 'level', 
                          'abilities', 'retreatCost', 'convertedRetreatCost', 'flavorText', 
                          'nationalPokedexNumbers', 'legalities', 'resistances', 'rules', 
                          'regulationMark', 'ancientTrait']
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
        # Build the evolution hierarchy and create the gerarchic column
        self.build_evolution_hierarchy()

    #def save_data(self, output_file_path):
        # Salva i dati in un nuovo file CSV
        #self.data.to_csv(output_file_path, index=False)
    


  

    def save_data(self, output_file_name):
        # Trova la cartella "Project" salendo da "source_code"
        base_dir = Path(__file__).resolve().parent.parent  # Sale di un livello

        # Percorso corretto della cartella CSV
        output_dir = base_dir / "CSV"

        # Percorso completo del file
        output_file_path = output_dir / output_file_name

        # Assicura che la cartella "CSV" esista
        output_dir.mkdir(parents=True, exist_ok=True)

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
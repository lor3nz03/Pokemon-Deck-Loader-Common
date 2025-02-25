import pandas as pd
import numpy as np
import random
from tabulate import tabulate
import matplotlib.pyplot as plt

class DeckBuilder:
    def __init__(self, data):
        self.data = data

    def create_balanced_deck(self, pokemon_type, n_decks=5):
        decks = {i: [] for i in range(n_decks)}

        # Filtro i Pokémon per tipo
        filtered_data = self.data[self.data['types'].apply(lambda x: pokemon_type in x)]

        # Ordino per HP e AVG_damage
        filtered_data['score'] = filtered_data['hp'] + filtered_data['AVG_damage']
        sorted_pokemon = filtered_data.sort_values(by='score', ascending=False)

        # Shuffle the sorted Pokémon to introduce randomness
        sorted_pokemon = sorted_pokemon.sample(frac=1).reset_index(drop=True)

        added_pokemon = set()  # Set per tracciare i Pokémon già aggiunti nei mazzi

        # Formazione dei mazzi
        for _, pokemon in sorted_pokemon.iterrows():
            pokemon_name = pokemon['name']
            
            # Aggiungo Pokémon per l'evoluzione utilizzando la colonna gerarchic
            evolution_chain = pokemon['gerarchic'].split(', ') if pd.notna(pokemon['gerarchic']) else [pokemon_name]

            # Aggiungo i Pokémon al mazzo se non sono già stati aggiunti
            for evo_pokemon in evolution_chain:
                if evo_pokemon not in added_pokemon:
                    evo_data = filtered_data[filtered_data['name'] == evo_pokemon]
                    if not evo_data.empty:
                        for i in range(n_decks):
                            if len(decks[i]) < 12:  # Limita a 12 Pokémon per mazzo
                                decks[i].append(evo_data.iloc[0])  # Aggiungo in append al mazzo
                                added_pokemon.add(evo_pokemon)  # Aggiungo il Pokémon al set
                                break

        return decks
    
    def suddivision(self, decks):
        deck_types = {}
        for i, deck in decks.items():
            attack_count = sum(1 for pokemon in deck if pokemon['AVG_damage'] > 50)
            tank_count = sum(1 for pokemon in deck if pokemon['hp'] > 100)
            
            if attack_count >= 3:
                deck_types[i] = "Attack"
            elif tank_count >= 2:
                deck_types[i] = "Tank"
            else:
                deck_types[i] = "Balance"
        
        return deck_types
    
    # Metodo per stampare su terminale i pokemon, utilizzo la libreria table per visualizzare meglio i deck
    def print_decks(self, decks):
        deck_types = self.suddivision(decks)
        for i, deck in decks.items():
            print(f'Mazzo {i + 1} ({deck_types[i]}):')
            table = []
            for pokemon in deck:
                table.append([pokemon['name'], pokemon['hp'], pokemon['AVG_damage'], pokemon['generation']])
            print(tabulate(table, headers=["Name", "HP", "AVG Damage", "Generation", "Type"], tablefmt="grid"))
            print()


    # Metodo per visualizzare i deck tramite un grafico ceato con matplot, così vediamo pure se i deck sono bilanciati
    def visualize_decks(self, decks):
        deck_types = self.suddivision(decks)
        for i, deck in decks.items():
            names = [pokemon['name'] for pokemon in deck]
            hp = [pokemon['hp'] for pokemon in deck]
            avg_damage = [pokemon['AVG_damage'] for pokemon in deck]

            fig, ax = plt.subplots()
            bar_width = 0.35
            index = np.arange(len(names))

            bar1 = plt.bar(index, hp, bar_width, label='HP')
            bar2 = plt.bar(index + bar_width, avg_damage, bar_width, label='AVG Damage')

            plt.xlabel('Pokémon')
            plt.ylabel('Values')
            plt.title(f'Mazzo {i + 1} ({deck_types[i]}):')
            plt.xticks(index + bar_width / 2, names, rotation=45, ha='right')
            plt.legend()

            plt.tight_layout()
            plt.show()

    # Metodo che prende in input da tastiera il tipo di deck che si vuole creare e si accerta che sia corretto
    def get_valid_pokemon_type(self, preprocessor):
        valid_types = set(preprocessor.data['types'].apply(lambda x: x.strip("[]").replace("'", "").split(", ")).explode().unique())
        while True:
            pokemon_type = input(f"Inserisci il tipo di pokemon per la generazione dei deck (Tipi validi: {', '.join(valid_types)}): ")
            if pokemon_type in valid_types:
                return pokemon_type
            else:
                print(f"Tipo invalido '{pokemon_type}'. Rinserisci il tipo, stai attendo a 'MAIUSCOLE' e 'minuscole' .")
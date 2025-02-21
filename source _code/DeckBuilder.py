import pandas as pd
import numpy as np

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

    # Metodo per stampare su terminale i pokemon
    def print_decks(self, decks):
        for i, deck in decks.items():
            print(f'Mazzo {i + 1}:')
            for pokemon in deck:
                print(f"{pokemon['name']} - HP: {pokemon['hp']} - AVG_damage: {pokemon['AVG_damage']} - Generation: {pokemon['generation']} - Tipo: {pokemon['types']}")
            print()
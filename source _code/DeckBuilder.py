

class DeckBuilder:
    def __init__(self, data):
        self.data = data

    def get_pokemon_with_evolutions(self):
        evolutions_dict = {}

        # Raggruppa i Pokémon per evoluzione (evolvesFrom -> evolvesTo)
        for _, pokemon in self.data.iterrows():
            pokemon_name = pokemon['name']
            evolves_from = pokemon['evolvesFrom']
            evolves_to = pokemon['evolvesTo']
            
            if evolves_from:
                if evolves_from not in evolutions_dict:
                    evolutions_dict[evolves_from] = []
                evolutions_dict[evolves_from].append(pokemon_name)
            if evolves_to:
                if pokemon_name not in evolutions_dict:
                    evolutions_dict[pokemon_name] = []
                evolutions_dict[pokemon_name].append(evolves_to)

        return evolutions_dict

    def create_balanced_deck(self, n_decks=5):
        decks = {i: [] for i in range(n_decks)}
        evolutions_dict = self.get_pokemon_with_evolutions()

        # Ordina per HP e AVG_damage
        self.data['score'] = self.data['hp'] + self.data['AVG_damage']
        sorted_pokemon = self.data.sort_values(by='score', ascending=False)

        added_pokemon = set()  # Set per tracciare i Pokémon già aggiunti nei mazzi

        # Formazione dei mazzi
        for _, pokemon in sorted_pokemon.iterrows():
            pokemon_name = pokemon['name']
            
            # Aggiungi Pokémon da evoluzione
            evolution_chain = [pokemon_name]
            if pokemon_name in evolutions_dict:
                evolution_chain += evolutions_dict[pokemon_name]

            evolution_chain = list(set(evolution_chain))  # Rimuovi duplicati

            # Aggiungi i Pokémon al mazzo se non sono già stati aggiunti
            for evo_pokemon in evolution_chain:
                if evo_pokemon not in added_pokemon and len(decks[0]) < 12:  # Limita a 12 Pokémon per mazzo
                    evo_data = self.data[self.data['name'] == evo_pokemon]
                    if not evo_data.empty:
                        decks[0].append(evo_data.iloc[0])  # Aggiungi al primo mazzo (modifica questo per bilanciare meglio)
                        added_pokemon.add(evo_pokemon)  # Aggiungi il Pokémon al set

        # Output dei mazzi creati
        for i, deck in decks.items():
            print(f'Mazzo {i + 1}:')
            for pokemon in deck:
                print(f"{pokemon['name']} - HP: {pokemon['hp']} - AVG_damage: {pokemon['AVG_damage']}")
            print()
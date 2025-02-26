# Pokemon-Deck-Loader-Common

Progetto finale per il corso "Introduzione al Data Mining"

## Panoramica del Progetto

Questo progetto ha lo scopo di preprocessare, raggruppare e costruire mazzi di Pokémon utilizzando i dati del Gioco di Carte Collezionabili Pokémon (TCG). Il progetto prevede diverse fasi, tra cui il preprocessing dei dati, il raggruppamento dei Pokémon in base ai loro attributi e la creazione di mazzi comuni bilanciati. Il progetto include anche la visualizzazione dei dati e dei mazzi creati.

## Classi e le loro Funzioni

### DataPreprocessor
- **Scopo**: Preprocessare i dati del TCG Pokémon.
- **Metodi**:
  - `load_data()`: Carica i dati da un file CSV.
  - `clean_data()`: Pulisce e preprocessa i dati.
  - `save_data(output_file_name)`: Salva i dati processati in un file CSV.
  - `plot_pokemon_by_generation()`: Visualizza il numero di Pokémon per generazione.
  - `plot_cards_by_artist()`: Visualizza il numero di carte per artista.
  - `plot_pokemon_by_type()`: Visualizza il numero di Pokémon per tipo.
  - `get_processed_data()`: Restituisce i dati processati.

### PokemonClustering
- **Scopo**: Raggruppare i Pokémon in base ai loro attributi.
- **Metodi**:
  - `elbow_method(max_clusters)`: Determina il numero ottimale di cluster utilizzando il metodo del gomito.
  - `cluster(method, n_clusters)`: Raggruppa i dati utilizzando il metodo specificato (es. k-means).
  - `visualize_clusters()`: Visualizza i cluster.
  - `save_clusters_to_file(file_name)`: Salva le assegnazioni dei cluster in un file.

### DeckBuilder
- **Scopo**: Creare e visualizzare mazzi di Pokémon.
- **Metodi**:
  - `create_balanced_deck(pokemon_type, n_decks)`: Crea mazzi bilanciati in base al tipo di Pokémon specificato.
  - `suddivision(decks)`: Valuta ogni mazzo e assegna un tag "Attack", "Tank" o "Balance".
  - `print_decks(decks)`: Stampa i mazzi in formato tabellare.
  - `visualize_decks(decks)`: Visualizza i mazzi utilizzando grafici a barre.
  - `get_valid_pokemon_type(preprocessor)`: Chiede all'utente di inserire un tipo di Pokémon valido.


## Librerie Utilizzate

- `pandas`: Per la manipolazione e l'analisi dei dati.
- `numpy`: Per operazioni numeriche.
- `matplotlib`: Per la visualizzazione dei dati.
- `seaborn`: Per la visualizzazione dei dati.
- `tabulate`: Per stampare tabelle in modo formattato.
- `scikit-learn`: Per algoritmi di clustering.
- `pathlib`: Per la gestione dei percorsi dei file.
- `ast`: Per la conversione sicura di stringhe in oggetti Python.

## Installazione

Per installare le librerie richieste, puoi usare `pip`. Esegui il seguente comando:

```bash
pip install pandas numpy matplotlib seaborn tabulate scikit-learn
```

## Come esegurilo

Per far partire il tool eseguire questo comando nella cartella source_code
```bash
python Main.py
```
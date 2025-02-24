# Pokemon-Deck-Loader-Common

Final Project for the course "Introduction to Data Mining"

## Project Overview

This project aims to preprocess, cluster, and build Pokémon decks using data from the Pokémon Trading Card Game (TCG). The project involves several steps, including data preprocessing, clustering Pokémon based on their attributes, and creating balanced common decks. The project also includes visualization of the data and the created decks.

## Classes and Their Functions

### DataPreprocessor
- **Purpose**: Preprocess the Pokémon TCG data.
- **Methods**:
  - `load_data()`: Loads the data from a CSV file.
  - `clean_data()`: Cleans and preprocesses the data.
  - `save_data(output_file_name)`: Saves the processed data to a CSV file.
  - `plot_pokemon_by_generation()`: Plots the number of Pokémon by generation.
  - `plot_cards_by_artist()`: Plots the number of cards by artist.
  - `plot_pokemon_by_type()`: Plots the number of Pokémon by type.
  - `get_processed_data()`: Returns the processed data.

### PokemonClustering
- **Purpose**: Cluster Pokémon based on their attributes.
- **Methods**:
  - `elbow_method(max_clusters)`: Determines the optimal number of clusters using the elbow method.
  - `cluster(method, n_clusters)`: Clusters the data using the specified method (e.g., k-means).
  - `visualize_clusters()`: Visualizes the clusters.
  - `save_clusters_to_file(file_name)`: Saves the cluster assignments to a file.

### DeckBuilder
- **Purpose**: Create and visualize Pokémon decks.
- **Methods**:
  - `create_balanced_deck(pokemon_type, n_decks)`: Creates balanced decks based on the specified Pokémon type.
  - `print_decks(decks)`: Prints the decks in a tabular format.
  - `visualize_decks(decks)`: Visualizes the decks using bar charts.
  - `get_valid_pokemon_type(preprocessor)`: Prompts the user to enter a valid Pokémon type.

## Libraries Used

- `pandas`: For data manipulation and analysis.
- `numpy`: For numerical operations.
- `matplotlib`: For data visualization.
- `tabulate`: For printing tables in a formatted way.
- `scikit-learn`: For clustering algorithms.

## Installation

To install the required libraries, you can use `pip`. Run the following command:

```sh
pip install pandas numpy matplotlib tabulate scikit-learn
```

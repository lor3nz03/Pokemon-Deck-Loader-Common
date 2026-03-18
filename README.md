# Pokemon Deck Loader Common

![Build](https://img.shields.io/badge/build-lightgrey)
![Version](https://img.shields.io/badge/version-lightgrey)
![License](https://img.shields.io/badge/license-lightgrey)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)

Generate balanced, budget-oriented Pokémon TCG decks from historical card data (1999–2023) using preprocessing + clustering + rule-based deck composition.

## Table of Contents

- [What this project does](#what-this-project-does)
- [Why this project is useful](#why-this-project-is-useful)
- [How to get started](#how-to-get-started)
- [Where to get help](#where-to-get-help)
- [Who maintains and contributes](#who-maintains-and-contributes)

## What this project does

This project loads a Pokémon TCG CSV dataset, cleans and enriches it, groups cards by battle profile, and automatically builds balanced decks for a user-selected Pokémon type.

### Pipeline overview

1. **Preprocess data** (`DataPreprocessor`)
   - Filters to Pokémon cards and budget-friendly rarities (`Rare Holo`, `Rare`, `Uncommon`, `Common`)
   - Extracts attack statistics (`AVG_damage`) from nested attack objects
   - Builds evolution hierarchies (`gerarchic`) used during deck generation
   - Saves cleaned dataset to [CSV/new.csv](CSV/new.csv)

2. **Cluster Pokémon** (`PokemonClustering`)
   - Uses `hp` and `AVG_damage` features
   - Supports multiple methods (`kmeans`, `dbscan`, `optics`, `agglomerative`)
   - Stores cluster assignments to [list.txt](list.txt)

3. **Build decks** (`DeckBuilder`)
   - Prompts user for a valid Pokémon type
   - Creates up to 5 decks (12 Pokémon each) with evolution-aware composition
   - Classifies each deck as `Attack`, `Tank`, or `Balance`
   - Prints tabular output and shows deck charts

## Why this project is useful

- **Fast deck prototyping**: builds multiple decks from one type selection.
- **Budget-oriented filtering**: keeps only common/uncommon/rare card classes.
- **Data-driven balancing**: uses HP and average attack damage as scoring features.
- **Evolution consistency**: avoids invalid evolution-only picks by adding linked chain cards.
- **Exploratory workflow**: includes clustering and visualizations for quick analysis.

## How to get started

### Prerequisites

- Python 3.9+
- `pip`
- A graphical environment for Matplotlib windows (plots are shown interactively)

### Installation

From the repository root:

```bash
python -m venv .venv
```

Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install pandas numpy matplotlib seaborn tabulate scikit-learn
```

### Run the project

> Important: run from `source _code`, because `Main.py` expects relative paths from that directory.

```bash
cd "source _code"
python Main.py
```

### Usage example

When prompted, enter a valid type (for example `Water`, `Fire`, `Psychic`, etc.):

```text
Inserisci il tipo di pokemon per la generazione dei deck (Tipi validi: ...): Water
```

Expected outputs after a run:

- Cleaned dataset: [CSV/new.csv](CSV/new.csv)
- Cluster export: [list.txt](list.txt)
- Interactive plots for data distribution, cluster visualization, and deck balance

### Project structure

```text
CSV/
  pokemon-tcg-data-master 1999-2023.csv
  new.csv
source _code/
  Main.py
  DataPreprocessor.py
  PokemonClustering.py
  DeckBuilder.py
list.txt
Relazione.md
```

## Where to get help

- Functional walkthrough and project notes: [Relazione.md](Relazione.md)
- Entry point and execution order: [source _code/Main.py](source%20_code/Main.py)
- Data cleaning logic: [source _code/DataPreprocessor.py](source%20_code/DataPreprocessor.py)
- Deck generation logic: [source _code/DeckBuilder.py](source%20_code/DeckBuilder.py)

For questions, bugs, or improvements, open an issue in this repository with:

- Python version
- OS
- full error trace (if any)
- reproduction steps

## Who maintains and contributes

### Maintainer

- **Lorenzo Di Bella** (original project author)

### Contributing

Contributions are welcome. To keep reviews fast:

1. Open an issue describing the problem/feature.
2. Create a focused branch (`feature/...` or `fix/...`).
3. Keep pull requests small and include a short test/run note.
4. Update docs when behavior or setup changes.

---

### Notes

- Current repository does not include a `LICENSE` file.
- Build/CI and semantic versioning are not yet configured.
- Console prompts and some comments are currently in Italian.
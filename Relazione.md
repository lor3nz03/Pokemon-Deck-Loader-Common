# Relazione Progetto finale Data Mining
Lorenzo Di Bella 

## Utilità del progetto

Questo progetto nasce dall'idea di rendere accessibile a tutti il gioco di carte dei Pokémon. Il tool crea mazzi con carte comuni ma molto competitivi per poter combattere contro mazzi con carte Ex e leggendarie, che sono molto più economicamente costosi . Il tool fornisce anche dei consigli su che tipo di mazzo usare, classificando i mazzi in tre categorie:
- **Tank**
- **Attack**
- **Balance**

a seconda del tipo di strategia che si vuole adottare.

## Spiegazione dettagliata


### Preprocessing dei dati
Per poter lavorare bene ho dovuto fare una grande pulizia del dataset andando a rimuovere alcune features, alcune feature le ho dovute modificare per esempio il campo "attack" che comprendeva in un unica stringa nome e valore di attacco, ho diviso questa feature in 2 features differenti. 
Un'altra grande aggiunta al dataset è stata la feature gerarichic, è stata quella che mi ha richiesto più tempo per essere sviluppata in quanto va a creare l'intera catena evolutiva di ogni pokemon basandosi sulle features "evolveFrom" "evolveTo", siccome i pokemon possono avere più di una evoluzione ho creato una feature di appoggio chiamata "evolveTo2" che salva la seconda evoluzione di un pokemon se la ha, una volta utilizzata cancello la feature.
L'obbiettivo è creare mazzi economici, quindi vado a fare un taglio al dataset selezionando solo i pokemon di rarità 'Rare Holo', 'Rare', 'Uncommon', 'Common'.
Decido per maggiore chiarezza sul dataset di visualizzare il numero di pokemon per artista,generazione e tipo.

### Clustering dei dati

Per dividere i pokemon in vari cluster ho deciso di basarmi sui punti hp e sugli attacchi dei pokemon, per scegliere il numero ottimale di cluster ho utulizza l'elbow method e si vede sperimentalmente che il numero ottimale è di 3 cluster.
Creo un metodo che mi permette di testare vari metodi di clustering e scegliere quello migliore tra "kmeans" "dbscan" "optics" "agglomerativi", a livello empirico trovo che kmeans è quello che separa in modo ottimale i cluster.
Applico una PCA per visualizzare i dati.

### Creazione dei Deck

Una volta suddivisi i pokemon in cluster è arrivato il momento della creazione dei mazzi formati da 12 pokemon, per la creazione prendo sempre in considerazione hp e damage di ogni pokemon, nella creazione dei mazzi si tengono in considerazione le evoluzioni di ogni pokemon e vengono aggiunte, infatti per esempio in un mazzo non potrebbe mai esserci un "Charizard" senza un "Charmeleon" e un "Charmander", per andare ad inserire queste evoluzioni mi è stata molto utile la feature "gerarchic" precedentemente creata durante la fase di preprocessing.
Infine una volta creati i mezzi vengono classificati in 3 categorie che rispecchiano un po' gli stili di gioco ovvero "Attacco" "Difesa" e "Bilanciato"

Ho testato i mazzi creati in un tool online ed effettivamente sono molto efficienti e reggono testa con mazzi molto più costosi 



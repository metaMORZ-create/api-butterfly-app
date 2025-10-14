# training/config.py

"""
Zentrale Konfiguration für das Schmetterlings-Klassifikationsprojekt.
"""

# Pfad zum Root-Verzeichnis des heruntergeladenen Datensatzes (ImageFolder-Format)
DATASET_DIR = "./data/train"

# Speicherort für das trainierte Modell (wird von train.py verwendet)
MODEL_SAVE_PATH = "./model/butterfly_model.pth"

# Speicherort für die Klassennamen (JSON-Datei, wird beim Training erzeugt)
CLASS_NAMES_SAVE_PATH = "./model/class_names.json"

# Hyperparameter
NUM_EPOCHS = 20
BATCH_SIZE = 32
LEARNING_RATE = 0.0003

# Verhältnis für Trainings-/Validierungs-/Testsplit (Summe muss 1 ergeben)
SPLIT_RATIO = (0.7, 0.15, 0.15)

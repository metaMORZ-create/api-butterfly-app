# training/data_utils.py

"""
Hilfsfunktionen zum Laden und Vorverarbeiten des Schmetterlings-Datensatzes.
Es wird vorausgesetzt, dass der Datensatz im ImageFolder-Format vorliegt,
d. h. jede Klasse hat einen eigenen Unterordner mit Bildern.
"""

import os
from typing import Tuple, Dict
from sklearn.model_selection import train_test_split
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
from config import DATASET_DIR, BATCH_SIZE, SPLIT_RATIO

def get_transforms() -> Tuple[transforms.Compose, transforms.Compose]:
    """
    Gibt zwei Transformations-Pipelines zurück: eine für das Training und eine für
    Validierung/Test.
    """
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])
    eval_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])
    return train_transform, eval_transform

def prepare_dataloaders() -> Tuple[Dict[str, DataLoader], list]:
    """
    Lädt den Datensatz aus DATASET_DIR, teilt ihn in Train/Val/Test auf und gibt
    DataLoader für jeden Split zurück. Außerdem wird die Klassenliste zurückgegeben.
    """
    train_ratio, val_ratio, test_ratio = SPLIT_RATIO
    if abs(sum(SPLIT_RATIO) - 1.0) > 1e-6:
        raise ValueError("SPLIT_RATIO muss sich zu 1 aufsummieren.")

    train_transform, eval_transform = get_transforms()

    # Gesamten Datensatz laden (noch ohne Transform)
    full_dataset = datasets.ImageFolder(DATASET_DIR)

    # Liste aller Indizes
    num_samples = len(full_dataset)
    indices = list(range(num_samples))

    # Stratified Split basierend auf Klassenlabels
    train_indices, temp_indices = train_test_split(
        indices,
        test_size=val_ratio + test_ratio,
        stratify=full_dataset.targets,
        random_state=42
    )
    # Aufteilen in Val und Test
    temp_labels = [full_dataset.targets[i] for i in temp_indices]
    val_fraction = val_ratio / (val_ratio + test_ratio)
    val_indices, test_indices = train_test_split(
        temp_indices,
        test_size=1 - val_fraction,
        stratify=temp_labels,
        random_state=42
    )

    # Subsets erstellen und passende Transforms setzen
    full_dataset.transform = train_transform
    train_dataset = Subset(full_dataset, train_indices)

    full_dataset.transform = eval_transform
    val_dataset = Subset(full_dataset, val_indices)
    test_dataset = Subset(full_dataset, test_indices)

    # DataLoader erstellen
    dataloaders = {
        "train": DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2),
        "val": DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2),
        "test": DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2),
    }

    # Klassenliste
    class_names = full_dataset.classes
    return dataloaders, class_names

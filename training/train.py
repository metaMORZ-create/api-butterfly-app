# training/train.py

"""
Script zum Trainieren des Butterfly-Classification-Modells.
Führe diese Datei lokal aus, nachdem der Datensatz heruntergeladen wurde.
"""

import json
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from config import (
    MODEL_SAVE_PATH,
    CLASS_NAMES_SAVE_PATH,
    NUM_EPOCHS,
    LEARNING_RATE,
)
from data_utils import prepare_dataloaders

def train_model():
    dataloaders, class_names = prepare_dataloaders()
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Vortrainiertes Modell laden (ResNet18)
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    # Finale Schicht ersetzen
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(class_names))
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    best_val_acc = 0.0

    for epoch in range(NUM_EPOCHS):
        print(f"Epoch {epoch + 1}/{NUM_EPOCHS}")
        # Training
        model.train()
        running_loss = 0.0
        running_corrects = 0
        for inputs, labels in dataloaders["train"]:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            _, preds = torch.max(outputs, 1)
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)

        epoch_loss = running_loss / len(dataloaders["train"].dataset)
        epoch_acc = running_corrects.double() / len(dataloaders["train"].dataset)
        print(f"  Train Loss: {epoch_loss:.4f}  Acc: {epoch_acc:.4f}")

        # Validierung
        model.eval()
        val_corrects = 0
        with torch.no_grad():
            for inputs, labels in dataloaders["val"]:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                val_corrects += torch.sum(preds == labels.data)
        val_acc = val_corrects.double() / len(dataloaders["val"].dataset)
        print(f"  Val Acc:   {val_acc:.4f}")

        # Bestes Modell speichern
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), MODEL_SAVE_PATH)
            print(f"  -> Neues Bestmodell gespeichert: {MODEL_SAVE_PATH}")

    # Klassenliste speichern
    os.makedirs(os.path.dirname(CLASS_NAMES_SAVE_PATH), exist_ok=True)
    with open(CLASS_NAMES_SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(class_names, f)
    print(f"Training abgeschlossen. Bestes Validierungs-Accuracy: {best_val_acc:.4f}")

if __name__ == "__main__":
    train_model()

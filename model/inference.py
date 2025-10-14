# model/inference.py

"""
Hilfsmodul für die Inferenz (Vorhersage).
Lädt das trainierte Modell und definiert die Funktion predict_image().
"""

import json
import io
from functools import lru_cache
from typing import List
import torch
from torchvision import models, transforms
from PIL import Image

# Cache für wiederholtes Laden
@lru_cache(maxsize=1)
def load_model(model_path: str, class_names_path: str):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Klassen laden
    with open(class_names_path, "r", encoding="utf-8") as f:
        class_names: List[str] = json.load(f)

    # Modell initialisieren
    model = models.resnet18()
    num_features = model.fc.in_features
    model.fc = torch.nn.Linear(num_features, len(class_names))
    state_dict = torch.load(model_path, map_location=device)
    model.load_state_dict(state_dict)
    model.eval()
    model.to(device)

    # Transformation für Inferenz
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])
    ])
    return model, class_names, transform, device

def predict_image(image_bytes: bytes,
                  model_path: str = "./model/butterfly_model.pth",
                  class_names_path: str = "./model/class_names.json") -> str:
    """
    Nimmt Bytes eines Bildes entgegen und gibt die vorhergesagte Spezies zurück.
    """
    model, class_names, transform, device = load_model(model_path, class_names_path)
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    tensor = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(tensor)
        _, pred = torch.max(outputs, 1)
    return class_names[pred.item()]

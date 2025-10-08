import requests
import random
from datetime import datetime

def create_user(username: str, email: str, password: str):
    url_register = "https://web-production-97da3.up.railway.app/users/register"
    data_create_user = {"username": username, "email": email, "password": password}
    response = requests.post(url_register, json=data_create_user)

    return response

def upload_photo(
    image_path: str,
    user_id: int,
    butterfly_id: int,
    latitude: float,
    longitude: float,
    token: str | None = None,
):
    url_upload = "https://web-production-97da3.up.railway.app/uploads"  # 👉 ändere auf deine Railway-URL, z. B. https://deinprojekt.up.railway.app/uploads

    data_upload = {
        "user_id": user_id,
        "butterfly_id": butterfly_id,
        "taken_at": datetime.utcnow().isoformat(),
        "latitude": latitude,
        "longitude": longitude,
    }

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    with open(image_path, "rb") as file:
        files = {"file": (image_path, file, "image/jpeg")}
        response = requests.post(url_upload, data=data_upload, files=files, headers=headers)

    return response

if __name__ == "__main__":
    # Beispiel: User erstellen
   response_create_user = create_user("Moritz2", "baarsmoritz796@gmail.com", "Moritz")
   print(f"Create User: {response_create_user.status_code}")

   # Beispiel: Foto hochladen
   response_upload = upload_photo(
        image_path="images/test1.jpg",
        user_id=1,
        butterfly_id=42,
        latitude=48.1372,
        longitude=11.5756,
        token=None,  # oder "supersecrettoken"
    )
   print(f"Upload Status: {response_upload.status_code}")
   print("Antwort:", response_upload.json())

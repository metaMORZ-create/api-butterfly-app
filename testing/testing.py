import requests
import random

def create_user(username: str, email: str, password: str):
    url_register = "https://web-production-97da3.up.railway.app/users/register"
    data_create_user = {"username": username, "email": email, "password": password}
    response = requests.post(url_register, json=data_create_user)

    return response


if __name__ == "__main__":
   response_create_user = create_user("Moritz", "baarsmoritz79@gmail.com", "Moritz")
   print(f"Create User: {response_create_user.status_code}")
   print(f"\n {response_ask_question.content}")
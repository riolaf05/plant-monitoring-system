from langchain_core.tools import tool
import requests
import sys
import datetime

raspberry_ip = "192.168.1.247"
now = datetime.datetime.now()  
timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
save_path = f"./captured_image_{timestamp}.jpg"
endpoint_url = f"http://{raspberry_ip}:5000/capture"

def save_image(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Immagine salvata in {save_path}")
        else:
            print(f"Errore nella richiesta: {response.status_code}")
    except Exception as e:
        print(f"Errore: {e}")

@tool
def image(command: str) -> str:
    """
    Utile per richiedere delle immagini da un servizio esterno.
    """
    save_image(endpoint_url, save_path)
    return f"Immagine salvata in {save_path}"
    
    
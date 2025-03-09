import requests

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

# Esempio di utilizzo
raspberry_ip = "192.168.1.247"  # Sostituisci con l'IP del Raspberry Pi
save_path = "./captured_image.jpg"
endpoint_url = f"http://{raspberry_ip}:5000/capture"

save_image(endpoint_url, save_path)
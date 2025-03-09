from flask import Flask, Response
from picamera import PiCamera
import io

app = Flask(__name__)
camera = PiCamera()

@app.route('/capture', methods=['GET'])
def capture_image():
    # Creazione di uno stream di memoria per salvare l'immagine
    image_stream = io.BytesIO()
    
    # Cattura dell'immagine
    camera.capture(image_stream, format='jpeg')
    image_stream.seek(0)
    
    # Restituisce l'immagine come response HTTP
    return Response(image_stream.read(), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
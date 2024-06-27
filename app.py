from flask import Flask, request, jsonify, render_template, redirect
import random
import string
import logging

app = Flask(__name__)

# Configurar el logging
logging.basicConfig(level=logging.DEBUG)

# Diccionario para almacenar URLs acortadas
urls = {}

# Ruta principal para servir la página web
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para acortar el enlace
@app.route('/shorten', methods=['POST'])
def shorten_url():
    logging.info("Solicitud recibida en /shorten")
    data = request.get_json()
    logging.debug(f"Datos recibidos: {data}")
    
    original_url = data.get('url')
    custom_id = data.get('custom_id')
    
    if not original_url:
        logging.error("No se proporcionó URL")
        return jsonify({'error': 'No URL provided'}), 400
    
    # Validar y usar el ID personalizado si está presente
    if custom_id:
        if custom_id in urls:
            logging.error("ID personalizado ya está en uso")
            return jsonify({'error': 'Custom ID already in use'}), 400
        short_id = custom_id
    else:
        short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        while short_id in urls:
            short_id = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    
    urls[short_id] = original_url
    short_url = request.host_url + short_id
    
    logging.info(f"URL original: {original_url}, URL acortada: {short_url}")
    return jsonify(short_url=short_url)

# Ruta para redireccionar el enlace acortado
@app.route('/<short_id>')
def redirect_to_url(short_id):
    logging.info(f"Solicitud de redirección para: {short_id}")
    original_url = urls.get(short_id)
    if original_url:
        logging.debug(f"Redirigiendo a: {original_url}")
        return redirect(original_url)
    else:
        logging.error("URL no encontrada")
        return 'URL no encontrada', 404

if __name__ == '__main__':
    app.run(debug=True)

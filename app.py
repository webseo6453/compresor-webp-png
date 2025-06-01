from flask import Flask, render_template, request, send_file
import os
import uuid
from tools.compress_png import compress_png_batch
from tools.convert_webp import convert_to_webp_batch
from utils.zipper import crear_zip_de_lotes

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
CONVERTED_FOLDER = 'static/converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_png', methods=['POST'])
def upload_png():
    files = request.files.getlist('images')
    lote_id = str(uuid.uuid4())[:8]
    lote_folder = os.path.join(CONVERTED_FOLDER, f"lote_{lote_id}")
    os.makedirs(lote_folder, exist_ok=True)

    resultados = compress_png_batch(files, lote_folder)
    return {'status': 'ok', 'lote': lote_id, 'imagenes': resultados}

@app.route('/upload_webp', methods=['POST'])
def upload_webp():
    files = request.files.getlist('images')
    lote_id = str(uuid.uuid4())[:8]
    lote_folder = os.path.join(CONVERTED_FOLDER, f"webp_lote_{lote_id}")
    os.makedirs(lote_folder, exist_ok=True)

    resultados = convert_to_webp_batch(files, lote_folder)
    return {'status': 'ok', 'lote': lote_id, 'imagenes': resultados}

@app.route('/descargar_zip')
def descargar_zip():
    from utils.zipper import crear_zip_de_lotes
    lote = request.args.get("lote")
    if not lote:
        return "Lote no especificado", 400

    folder = os.path.join(CONVERTED_FOLDER, lote)
    if not os.path.exists(folder):
        return "Lote no encontrado", 404

    zip_path = os.path.join(CONVERTED_FOLDER, f"{lote}.zip")

    # BORRAR ZIP ANTERIOR (si ya existe para ese lote)
    if os.path.exists(zip_path):
        os.remove(zip_path)

    # SOLO incluye el contenido de la carpeta del lote actual
    crear_zip_de_lotes(folder, zip_path)

    return send_file(zip_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

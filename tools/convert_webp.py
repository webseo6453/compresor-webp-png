import os
from PIL import Image

def convert_to_webp_batch(files, output_folder):
    resultados = []
    for f in files:
        nombre = f.filename
        original_temp = os.path.join(output_folder, f"__tmp_{nombre}")
        f.save(original_temp)

        webp_name = f"{os.path.splitext(nombre)[0]}.webp"
        webp_path = os.path.join(output_folder, webp_name)

        try:
            im = Image.open(original_temp).convert("RGBA")
            im.save(webp_path, "webp", quality=90)
            resultados.append({
                'original': nombre,
                'webp': webp_name
            })
        except Exception as e:
            print(f"Error al convertir {nombre}: {e}")

        # Eliminar imagen original temporal
        if os.path.exists(original_temp):
            os.remove(original_temp)

    return resultados

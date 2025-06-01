import os
import subprocess

def compress_png_batch(files, output_folder):
    resultados = []
    for f in files:
        nombre = f.filename
        original_temp = os.path.join(output_folder, f"__tmp_{nombre}")
        f.save(original_temp)

        compressed_name = f"compressed_{nombre}"
        compressed_path = os.path.join(output_folder, compressed_name)

        subprocess.run([
            'pngquant',
            '--quality=70-90',
            '--output', compressed_path,
            '--force', original_temp
        ])

        # Eliminar imagen original temporal
        if os.path.exists(original_temp):
            os.remove(original_temp)

        if os.path.exists(compressed_path):
            resultados.append({
                'original': nombre,
                'comprimido': compressed_name
            })
    return resultados

import os
import subprocess
import uuid

def compress_png_batch(files, output_folder):
    resultados = []

    for f in files:
        nombre_original = f.filename
        ext = os.path.splitext(nombre_original)[1].lower()
        
        # Generar nombre temporal único y limpio
        safe_basename = f"{uuid.uuid4().hex}{ext}"
        input_path = os.path.join(output_folder, f"tmp_{safe_basename}")
        output_path = os.path.join(output_folder, f"compressed_{safe_basename}")

        f.save(input_path)

        try:
            subprocess.run([
                'pngquant',
                '--quality=70-90',
                '--speed', '1',
                '--output', output_path,
                '--force', input_path
            ], check=True)

            if os.path.exists(output_path):
                resultados.append({
                    'original': nombre_original,
                    'comprimido': os.path.basename(output_path)
                })

        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Falló la compresión de {nombre_original}: {e}")

        finally:
            if os.path.exists(input_path):
                os.remove(input_path)

    return resultados

import os
import zipfile

def crear_zip_de_lotes(base_path, zip_path):
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, base_path)
                zipf.write(filepath, arcname=arcname)
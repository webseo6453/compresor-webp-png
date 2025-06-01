import os
from datetime import datetime, timedelta

def eliminar_lotes_antiguos(base_path, max_age_hours=24):
    now = datetime.now()
    eliminadas = []
    for folder in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder)
        if os.path.isdir(folder_path):
            last_mod = datetime.fromtimestamp(os.path.getmtime(folder_path))
            if (now - last_mod) > timedelta(hours=max_age_hours):
                eliminadas.append(folder)
                for root, dirs, files in os.walk(folder_path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(folder_path)
    return eliminadas

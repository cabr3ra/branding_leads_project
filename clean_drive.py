import sys
import os

# Agregar la ruta raíz del proyecto al path para que Python encuentre utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.drive_utils import eliminar_todos_los_archivos, vaciar_papelera

if __name__ == "__main__":
    print("Iniciando limpieza de archivos en Drive...")
    eliminar_todos_los_archivos()  # Borra archivos que NO están en la papelera
    print("Eliminación de archivos fuera de la papelera completada.")
    
    vaciar_papelera()  # Borra archivos que están en la papelera definitivamente
    print("Papelera vaciada. Limpieza completada.")

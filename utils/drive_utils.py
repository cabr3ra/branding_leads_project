from googleapiclient.discovery import build
import re
import logging
import json # Importar la librería json para manejar archivos JSON
from io import BytesIO # Importar BytesIO para manejar datos binarios en memoria
from googleapiclient.http import MediaIoBaseUpload # Importar MediaIoBaseUpload para subir archivos a Google Drive
from config import creds, drive_service, docs_service # Asumiendo que expones estos desde config.py ahora

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def crear_doc(nombre_archivo, contenido_texto):
    """
    Crea un archivo de texto plano en Drive en la carpeta especificada.
    Devuelve el link de visualización.
    """
    folder_id = '1hISpTB2x_qHUR6_G1o9h3jCyibyAb582'

    file_metadata = {
        'name': f"{nombre_archivo}.txt",
        'mimeType': 'text/plain',
        'parents': [folder_id]
    }

    media = MediaIoBaseUpload(BytesIO(contenido_texto.encode()), mimetype='text/plain')

    file = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()

    # Permitir acceso público con enlace
    permission = {
        'type': 'anyone',
        'role': 'reader'
    }
    drive_service.permissions().create(fileId=file['id'], body=permission).execute()

    # Obtener enlace
    file_info = drive_service.files().get(fileId=file['id'], fields='webViewLink').execute()
    return file_info.get('webViewLink')


def read_doc(doc_url):
    """
    Lee el contenido de un Google Doc dado su URL.
    """
    # Extraer el ID del documento de la URL
    match = re.search(r'/document/d/([a-zA-Z0-9_-]+)', doc_url)
    if not match:
        logging.error(f"URL de Google Doc inválida: {doc_url}")
        raise ValueError(f"URL de Google Doc inválida: {doc_url}")
    document_id = match.group(1)

    try:
        document = docs_service.documents().get(documentId=document_id).execute()
        content_elements = document.get('body', {}).get('content', [])

        full_text = []
        for element in content_elements:
            if 'paragraph' in element:
                paragraph_elements = element.get('paragraph', {}).get('elements', [])
                for text_run in paragraph_elements:
                    if 'textRun' in text_run:
                        full_text.append(text_run.get('textRun', {}).get('content'))
        # Join the text parts and remove any None values, then strip whitespace
        return "".join(filter(None, full_text)).strip()
    except Exception as e:
        logging.error(f"Error al leer el contenido del Google Doc {doc_url}: {e}")
        raise # Re-lanza la excepción para que sea manejada en el main.py

def eliminar_todos_los_archivos():
    try:
        # Query para obtener todos los archivos que no estén en la papelera
        query = "trashed = false"
        page_token = None

        while True:
            response = drive_service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name)',
                pageToken=page_token
            ).execute()

            files = response.get('files', [])
            if not files:
                print("No hay más archivos para eliminar.")
                break

            for file in files:
                file_id = file['id']
                file_name = file['name']
                try:
                    drive_service.files().delete(fileId=file_id).execute()
                    print(f"Archivo eliminado: {file_name} (ID: {file_id})")
                except Exception as e:
                    print(f"No se pudo eliminar {file_name} (ID: {file_id}): {e}")

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except Exception as e:
        print(f"Error eliminando archivos: {e}")

def vaciar_papelera():
    try:
        query = "trashed = true"
        page_token = None

        while True:
            response = drive_service.files().list(
                q=query,
                spaces='drive',
                fields='nextPageToken, files(id, name)',
                pageToken=page_token
            ).execute()

            files = response.get('files', [])
            if not files:
                print("La papelera está vacía.")
                break

            for file in files:
                file_id = file['id']
                file_name = file['name']
                try:
                    drive_service.files().delete(fileId=file_id).execute()
                    print(f"Archivo en papelera eliminado definitivamente: {file_name} (ID: {file_id})")
                except Exception as e:
                    print(f"No se pudo eliminar {file_name} (ID: {file_id}): {e}")

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except Exception as e:
        print(f"Error vaciando la papelera: {e}")

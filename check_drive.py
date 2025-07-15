from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/drive"
]

# Asegúrate que el path y nombre de tu archivo de credenciales es correcto
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

drive_service = build('drive', 'v3', credentials=creds)

about = drive_service.about().get(fields="storageQuota").execute()
print("Límite de almacenamiento (bytes):", about['storageQuota']['limit'])
print("Uso actual (bytes):", about['storageQuota']['usage'])
print("Uso en Drive (bytes):", about['storageQuota']['usageInDrive'])
print("Uso en papelera (bytes):", about['storageQuota']['usageInDriveTrash'])

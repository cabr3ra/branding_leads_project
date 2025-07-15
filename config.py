import google.generativeai as genai
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# === Constantes y configuración general ===
API_KEY = "AIzaSyAjS6Pkfb9j4WmF7tgzoRjkNpkOuKOsdps"
MODEL_NAME = "models/gemini-1.5-flash"
SHEET_ID = "1I6lOdmi0_RJYRiSPi6Uu9HEAHqQNzI7_8pU7HFza3lk"

# === Scopes para Google APIs (Sheets, Drive, Docs) ===
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/spreadsheets",
]

# === Credenciales únicas para todas las APIs ===
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)

# === Inicialización API Gemini ===
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# === Cliente Google Sheets e inicialización de hojas ===
client = gspread.authorize(creds)
# Abre el libro por su ID
spreadsheet = client.open_by_key(SHEET_ID)

# Inicializa cada hoja por su nombre
sheet_base = spreadsheet.worksheet('base')
sheet_herramientas = spreadsheet.worksheet('herramientas')
sheet_contactos = spreadsheet.worksheet('contactos')

# === Inicialización Google Drive y Docs Services ===
drive_service = build('drive', 'v3', credentials=creds)
docs_service = build('docs', 'v1', credentials=creds)

# === Columnas (ordenadas) para cada hoja ===
# Ajusta estas listas de columnas para que coincidan exactamente con tus hojas
COLUMNAS_BASE = [
    "ID",
    "Marca",
    "Email",
    "Web",    
    "País",
    "Ciudad",
    "Año fundación",
    "Tipo de marca",
    "Sector",
    "Industria",
    "Categoría",
    "Segmento (B2B/B2C)",
    "Estado del lead",
    "Propósito",
    "Público objetivo",
    "Propuesta de valor",
    "Redes sociales",
    "Ultimo producto",
    "Descripción Producto"
]

COLUMNAS_HERRAMIENTAS = [
    "ID",
    "Marca",
    "Email",
    "Estado del lead",
    "Branding",
    "Necesidades",
    "Email generado"
]

COLUMNAS_CONTACTOS = [
    "ID",
    "Marca",
    "Email",
    "Estado del lead",
    "Responsable",
    "Fecha 1r contacto",
    "Notas",
    "Próximo contacto"
]
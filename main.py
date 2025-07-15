from utils.sheets_utils import get_col_map, get_row_data, update_headline
from tools.branding import analizar_branding
from tools.email import crear_email
from config import model, sheet_base, sheet_herramientas, \
                   COLUMNAS_BASE, COLUMNAS_HERRAMIENTAS # Importa las hojas y columnas correctas
from utils.drive_utils import read_doc
import logging

# Configuración de logs para main.py
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def procesar_filas(sheet_base, sheet_herramientas, col_map_base, col_map_herramientas, model):
    """
    Procesa las filas de la hoja 'base', genera o recupera el branding
    y genera el email, guardando la información en las hojas correspondientes.
    """
    row_count_base = sheet_base.row_count
    logging.info(f"Iniciando procesamiento de {row_count_base - 1} filas desde la hoja 'base'.")

    # Asegurarse de que la hoja de herramientas tenga al menos el mismo número de filas
    # Si no, gspread dará un error al intentar leer una fila inexistente.
    # Podrías optar por crear filas vacías en 'herramientas' o manejar el error.
    # Por simplicidad, asumimos que existen las filas correspondientes o se gestiona en la lógica.

    for row_idx in range(2, row_count_base + 1): # Empieza desde la fila 2 (después de los encabezados)
        try:
            # Leer datos de la hoja 'base'
            values_base = sheet_base.row_values(row_idx)
            data_base = get_row_data(values_base, col_map_base)

            # Leer datos de la hoja 'herramientas' para verificar si ya hay contenido
            # Es vital que esta lectura no modifique las celdas, solo las lea.
            values_herramientas = sheet_herramientas.row_values(row_idx)
            data_herramientas = get_row_data(values_herramientas, col_map_herramientas)

            marca_nombre = data_base.get("marca", "Desconocido") # Usar "marca" en minúsculas
            sitio_web = data_base.get("web") # Usar "web" en minúsculas

            logging.info(f"-- Fila {row_idx} - {marca_nombre} --")

            if not sitio_web:
                logging.warning(f"No hay sitio web. Saltando...")
                continue

            analisis_branding_texto = None

            # --- 1. PASO: Obtener/Generar Análisis de Branding ---
            # data_herramientas.get("branding") nos dirá si ya hay un enlace en la hoja de herramientas
            if data_herramientas.get("branding"):
                logging.info(f"[{marca_nombre}] Análisis de branding ya existe. Recuperando texto del documento...")
                try:
                    analisis_branding_texto = read_doc(data_herramientas.get("branding"))
                    logging.info(f"[{marca_nombre}] Texto de branding recuperado.")
                except Exception as e:
                    logging.error(f"[{marca_nombre}] Error al leer el documento de branding ({data_herramientas.get('branding')}): {e}")
                    analisis_branding_texto = None
            else:
                logging.info(f"[{marca_nombre}] No hay branding. Generando...")
                # Pasar data_base para el contexto del prompt y data_herramientas para el check de existencia
                analisis_branding_texto = analizar_branding(
                    row_idx, data_base, data_herramientas, sheet_herramientas, col_map_herramientas, model
                )
                if not analisis_branding_texto:
                    logging.warning(f"[{marca_nombre}] No se pudo generar el análisis de branding.")

            # --- 2. PASO: Generación del Email (solo si el email no existe y tenemos branding) ---
            # data_herramientas.get("email_generado") nos dirá si ya hay un enlace en la hoja de herramientas
            if not data_herramientas.get("email_generado"):
                if sitio_web and analisis_branding_texto:
                    logging.info(f"[{marca_nombre}] No hay email generado. Generando...")
                    # Pasar data_base para el contexto del prompt y data_herramientas para el check de existencia
                    crear_email(
                        row_idx, data_base, data_herramientas, sheet_herramientas, col_map_herramientas, model, analisis_branding_texto
                    )
                else:
                    if not analisis_branding_texto:
                        logging.warning(f"[{marca_nombre}] No hay contenido de análisis de branding disponible. Saltando generación de email.")
            else:
                logging.info(f"[{marca_nombre}] Email ya generado.")

        except Exception as e:
            logging.error(f"[ERROR] Fila {row_idx}: {e}", exc_info=True)

def main():
    # Es crucial que los encabezados de ambas hojas estén correctos
    # update_headline(sheet_base, COLUMNAS_BASE) # Generalmente solo necesitas ejecutar esto si has cambiado las columnas en config.py y quieres sincronizar la hoja
    # update_headline(sheet_herramientas, COLUMNAS_HERRAMIENTAS) # Idem

    # Obtener los mapeos de columnas para cada hoja
    col_map_base = get_col_map(sheet_base)
    col_map_herramientas = get_col_map(sheet_herramientas)

    procesar_filas(sheet_base, sheet_herramientas, col_map_base, col_map_herramientas, model)

if __name__ == "__main__":
    main()

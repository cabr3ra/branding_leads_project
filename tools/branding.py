import requests
from bs4 import BeautifulSoup
import logging
import re
import markdown
from prompts.branding_prompt import get_prompt_branding
from utils.drive_utils import crear_doc

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def limpiar_contenido_html(html):
    """Limpia el contenido HTML de scripts, estilos y ruido irrelevante."""
    soup = BeautifulSoup(html, "html.parser")

    for script in soup(["script", "style", "noscript"]):
        script.decompose()

    texto = soup.get_text(separator=' ', strip=True)

    patrones_ruido = r"(aceptar cookies|uso de cookies|términos y condiciones|aviso legal|privacidad|RGPD|todos los derechos reservados)"
    texto = re.sub(patrones_ruido, "", texto, flags=re.I)

    return texto[:8000]

def extraer_meta_info(soup):
    """Extrae el título y la meta-descripción de una página web."""
    titulo = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    descripcion = meta_tag["content"].strip() if meta_tag and "content" in meta_tag.attrs else ""
    return titulo, descripcion

# MODIFICACIÓN CLAVE: Ahora recibe 'base_data' y 'tools_data' por separado
def analizar_branding(row_idx, base_data, tools_data, target_sheet, target_col_map, model):
    """
    Analiza el branding de una empresa a partir de su sitio web y otros datos,
    genera un Google Doc con el análisis y guarda el enlace en la hoja de herramientas.
    """
    sitio = base_data.get("web") # Obtener sitio web de la hoja 'base'
    branding_existente = tools_data.get("branding") # Obtener branding existente de la hoja 'herramientas'

    marca_nombre = base_data.get('marca', 'Desconocido') # Obtener nombre de marca de la hoja 'base'

    logging.info(f"[{marca_nombre}] Analizando branding...")

    if not sitio:
        logging.warning(f"[{marca_nombre}] Sitio web no disponible. Saltando análisis de branding.")
        return None

    if branding_existente:
        logging.info(f"[{marca_nombre}] Branding ya existe en la hoja de herramientas. Saltando.")
        return None

    try:
        logging.info(f"[{marca_nombre}] Accediendo a: {sitio}")
        res = requests.get(sitio, timeout=10)
        if res.status_code != 200:
            logging.error(f"[{marca_nombre}] Error HTTP: {res.status_code}")
            return None

        soup = BeautifulSoup(res.text, "html.parser")
        titulo, descripcion = extraer_meta_info(soup)
        contenido_web = limpiar_contenido_html(res.text)
        logging.info(f"[{marca_nombre}] Contenido web limpiado. Longitud: {len(contenido_web)}")

        # Preparar info_contexto_para_prompt usando datos de 'base_data'
        info_contexto_para_prompt = {
            "ID": base_data.get("id", ""),
            "Marca": base_data.get("marca", ""),
            "Email": base_data.get("email", ""),
            "Web": base_data.get("web", ""),
            "País": base_data.get("país", ""),
            "Ciudad": base_data.get("ciudad", ""),
            "Año fundación": base_data.get("año_fundación", ""), # Usar nombre de clave en minúsculas y guiones bajos
            "Tipo de marca": base_data.get("tipo_de_marca", ""),
            "Sector": base_data.get("sector", ""),
            "Industria": base_data.get("industria", ""),
            "Categoría": base_data.get("categoría", ""),
            "Segmento (B2B/B2C)": base_data.get("segmento_(b2b/b2c)", ""),
            "Estado del lead": base_data.get("estado_del_lead", ""),
            "Propósito": base_data.get("propósito", ""),
            "Público objetivo": base_data.get("público_objetivo", ""),
            "Propuesta de valor": base_data.get("propuesta_de_valor", ""),
            "Redes sociales": base_data.get("redes_sociales", ""),
            "Ultimo producto": base_data.get("ultimo_producto", ""),
            "Descripción Producto": base_data.get("descripción_producto", ""),
            "título_web": titulo,
            "meta_description": descripcion
        }

        prompt = get_prompt_branding(info_contexto=info_contexto_para_prompt, contenido_web=contenido_web)

        respuesta = model.generate_content(prompt)
        branding_markdown = respuesta.text.strip()

        logging.info(f"[{marca_nombre}] Branding generado con éxito. Longitud: {len(branding_markdown)}")

        branding_html = markdown.markdown(branding_markdown)

        nombre_doc = f"Branding - {marca_nombre}"
        url_doc = crear_doc(nombre_doc, branding_html)

        # Actualizar SOLO la columna 'Branding' en la hoja de herramientas
        col = target_col_map.get("Branding")
        if col:
            target_sheet.update_cell(row_idx, col, url_doc)
            logging.info(f"[{marca_nombre}] Enlace al branding guardado en hoja 'herramientas' (columna {col}): {url_doc}")
        else:
            logging.error(f"[{marca_nombre}] La columna 'Branding' no se encontró en el mapeo para la hoja de herramientas. NO SE PUDO GUARDAR.")

        return branding_markdown

    except Exception as e:
        logging.error(f"[{marca_nombre}] Excepción durante branding: {e}", exc_info=True)
        return None

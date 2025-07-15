import logging
import textwrap
import markdown
from prompts.email_prompt import get_prompt_email
from utils.drive_utils import crear_doc

# Configuración de logs
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def crear_email(row_idx, base_data, tools_data, target_sheet, target_col_map, model, analisis_branding_texto):
    """
    Genera un email de contacto personalizado, crea un Google Doc con el email
    y guarda el enlace en la hoja de herramientas.
    """
    marca_nombre = base_data.get("marca", "Desconocido")
    email_generado_link = tools_data.get("email_generado")

    logging.info(f"[{marca_nombre}] Generando email de contacto...")

    if email_generado_link:
        logging.info(f"[{marca_nombre}] Email de contacto ya existe en la hoja de herramientas. Saltando.")
        return {"asunto_final": "", "cuerpo_final": "", "skipped": True}

    info_busquets_creativos_para_prompt = """
    CONSULTORÍA | Te escuchamos.
    Diagnóstico real. Ejecución impecable.
    Solicita una primera consultoría confidencial.

    Busquets Creativos S.L se dedica a transformar ideas en realidades emocionantes, con un enfoque innovador y personalizado para cada proyecto. Nos comprometemos a ofrecer soluciones creativas que impulsen el crecimiento y éxito de nuestros clientes, construyendo relaciones basadas en la confianza, la excelencia y la visión a largo plazo.
    """

    busquets_contacto_footer_html = """
    <p>Saludos cordiales,</p>
    <p><strong>Busquets Creativos</strong></p>
    <hr />
    <p><strong>Teléfono:</strong> +34 680 473 875<br>
    <strong>Correo Electrónico:</strong> informacion@busquetscreativos.com<br>
    <strong>Dirección:</strong> Calle Mozart, número 1. 08110 Montcada i Reixac. Barcelona</p>
    """

    try:
        # Construir datos para el prompt
        info_empresa_para_email = {
            "marca": marca_nombre,
            "email": base_data.get("email", ""),
            "web": base_data.get("web", ""),
            "categoría": base_data.get("categoría", ""),
            "industria": base_data.get("industria", ""),
            "sector": base_data.get("sector", ""),
            "tamaño_empresa": base_data.get("tamaño_empresa", ""),
            "público_objetivo": base_data.get("público_objetivo", ""),
            "oportunidad_creativa": base_data.get("oportunidad_creativa", ""),
            "necesidad_detectada": base_data.get("necesidad_detectada", ""),
        }

        prompt = get_prompt_email(
            info_busquets_creativos=info_busquets_creativos_para_prompt,
            info_empresa_para_email=info_empresa_para_email,
            analisis_branding=analisis_branding_texto
        )

        logging.info(f"[{marca_nombre}] Enviando prompt a Gemini...")
        respuesta = model.generate_content(prompt)

        if not hasattr(respuesta, 'text') or not respuesta.text.strip():
            raise ValueError("Respuesta vacía del modelo")

        # Extraer y limpiar texto (se espera markdown plano del modelo)
        cuerpo_email_markdown = respuesta.text.strip()
        cuerpo_email_texto_plano = textwrap.dedent(f"""{cuerpo_email_markdown.strip()}

        Saludos cordiales,

        Busquets Creativos

        Teléfono: +34 680 473 875
        Correo Electrónico: informacion@busquetscreativos.com
        Dirección: Calle Mozart, número 1. 08110 Montcada i Reixac. Barcelona
        """).strip()


        # Crear Google Doc
        nombre_doc = f"Email Contacto - {marca_nombre}"
        url_doc = crear_doc(nombre_doc, cuerpo_email_texto_plano)

        logging.info(f"[{marca_nombre}] Documento creado: {url_doc}")

        # Guardar enlace en la hoja
        col_email_generado_idx = target_col_map.get("Email generado")
        if col_email_generado_idx:
            target_sheet.update_cell(row_idx, col_email_generado_idx, url_doc)
        else:
            logging.warning(f"[{marca_nombre}] No se encontró la columna 'Email generado' en el mapping")

        return {
            "asunto_final": f"Contacto - {marca_nombre}",
            "cuerpo_final": cuerpo_email_markdown
        }

    except Exception as e:
        logging.error(f"[{marca_nombre}] Error generando email: {e}", exc_info=True)
        return {
            "asunto_final": "",
            "cuerpo_final": "",
            "error": "Error al generar email",
            "mensaje": str(e)
        }

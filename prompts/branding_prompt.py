import textwrap

def get_prompt_branding(info_contexto, contenido_web):
    """
    Genera un prompt claro, directo y fácil de entender para un modelo de IA,
    enfocado en análisis de marca desde contenido web y contexto adicional.
    Pide a la IA que entregue la respuesta en formato Markdown para una mejor estructura.
    """
    
    # Asegurarse de que info_contexto sea un diccionario y tenga los valores esperados
    titulo_pagina = info_contexto.get("Web_titulo", "No disponible") if isinstance(info_contexto, dict) else "No disponible"
    meta_descripcion = info_contexto.get("Meta_description", "No disponible") if isinstance(info_contexto, dict) else "No disponible"
    
    # Preparamos el contexto de la marca como un string, ya que el input info_contexto es un diccionario
    # Convertimos a formato legible para el prompt. Filtramos las claves que ya se muestran arriba.
    contexto_formateado = "\n".join([
        f"- **{k.replace('_', ' ').title()}**: {v}" 
        for k, v in info_contexto.items() 
        if v and k not in ["Web_titulo", "Meta_description"]
    ])

    prompt = f"""
    Eres un consultor de branding experimentado.
    Analiza la siguiente marca basándote en su sitio web, el título, la meta-descripción y el contexto adicional que te doy.

    Tu análisis debe ser estratégico, profesional y fácil de entender.
    **Responde en formato Markdown** (usa negritas para títulos y listas para puntos) y sé breve, específico y claro.

    **Estructura tu respuesta con estos 5 puntos principales, usando los títulos exactos:**

    ## 1. Identidad Actual de la Marca
    Describe qué transmite la marca hoy en su sitio web. Incluye su estilo visual, el tono de voz que utiliza y si es coherente con su contexto general.

    ## 2. Propuesta de Valor y Diferenciación
    Explica qué ofrece la marca y cómo se diferencia de la competencia.

    ## 3. Experiencia de Usuario (UX) de la Web
    Valora qué tan buena es la facilidad de uso y la experiencia general de su sitio web.

    ## 4. Oportunidades Estratégicas
    Identifica nuevas vías o áreas donde la marca podría crecer o destacar.

    ## 5. Recomendaciones para Reforzar la Marca
    Sugiere mejoras específicas para hacer su identidad de marca más fuerte y aprovechar las oportunidades creativas.

    ---
    ### INFORMACIÓN DEL SITIO WEB:
    - **Título de la Página**: {titulo_pagina}
    - **Meta-Descripción**: {meta_descripcion}

    ---
    ### CONTEXTO ADICIONAL DE LA MARCA:
    {contexto_formateado if contexto_formateado else "No se proporcionó contexto adicional."}

    ---
    ### CONTENIDO PRINCIPAL DE LA WEB:
    {contenido_web.strip() if contenido_web else "No se proporcionó contenido web."}
    """

    return textwrap.dedent(prompt).strip()

if __name__ == '__main__':
    # Ejemplo de uso (esto simula los datos que vendrían de Google Sheets y el web scraping)
    ejemplo_info_contexto = {
        "ID": "123",
        "Marca": "Wallbox",
        "Email": "info@wallbox.com",
        "Web": "https://wallbox.com/es_es/", 
        "Web_titulo": "Wallbox | Innovación en soluciones de carga para vehículos eléctricos", # Nueva clave para el título
        "Meta_description": "Wallbox ofrece cargadores inteligentes y soluciones de gestión energética para vehículos eléctricos.", # Nueva clave para la meta-descripción
        "País": "España",
        "Ciudad": "Barcelona",
        "Año fundación": "2015",
        "Tipo de marca": "Producto",
        "Sector": "Tecnología",
        "Industria": "Energía",
        "Categoría": "Movilidad Eléctrica",
        "Segmento (B2B/B2C)": "B2C",
        "Estado del lead": "Contacto Inicial",
        "Propósito": "Revolucionar la movilidad",
        "Público objetivo": "Usuarios de vehículos eléctricos y empresas con flotas",
        "Propuesta de valor": "Carga inteligente, conectada y sostenible",
        "Redes sociales": "LinkedIn, Instagram",
        "Ultimo producto": "Pulsar Plus",
        "Descripción Producto": "Cargador compacto y potente para uso doméstico."
    }

    ejemplo_contenido_web = """
    En Wallbox, creamos tecnología innovadora para revolucionar la forma en que el mundo usa la energía.
    Desarrollamos sistemas avanzados de carga de vehículos eléctricos que combinan tecnología de vanguardia
    con un diseño excepcional, y que gestionan la comunicación entre el vehículo y el cargador a través
    de aplicaciones fáciles de usar. Nuestros cargadores inteligentes están pensados para hogares,
    empresas y espacios públicos. Con Wallbox, la carga de tu coche eléctrico es más sencilla,
    rápida y eficiente que nunca. Descubre nuestra gama de productos.
    """

    prompt_generado = get_prompt_branding(ejemplo_info_contexto, ejemplo_contenido_web)
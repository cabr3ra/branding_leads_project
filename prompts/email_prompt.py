import textwrap

def get_prompt_email(info_busquets_creativos, info_empresa_para_email, analisis_branding):
    """
    Genera un prompt para un modelo de lenguaje con el fin de crear un email personalizado
    para contactar a una empresa para una primera reunión.
    """
    # Actualizar para usar las claves en minúsculas y con guiones bajos
    empresa_marca = info_empresa_para_email.get("marca", "la empresa")
    email_contacto = info_empresa_para_email.get("email", "contacto@empresa.com")
    sitio_web = info_empresa_para_email.get("web", "su sitio web")
    oportunidad_creativa = info_empresa_para_email.get("oportunidad_creativa", "").strip()
    necesidad_detectada = info_empresa_para_email.get("necesidad_detectada", "").strip()

    gancho_inicial_frase = ""
    if necesidad_detectada:
        gancho_inicial_frase = f"Tras un breve análisis de su presencia online, especialmente en **{sitio_web}**, hemos identificado una **oportunidad significativa** en el área de **{necesidad_detectada}**."
    elif oportunidad_creativa:
        gancho_inicial_frase = f"Hemos estado analizando su marca y sitio web (**{sitio_web}**) y hemos detectado una **interesante oportunidad estratégica** en relación con **{oportunidad_creativa}**."
    else:
        gancho_inicial_frase = f"Tras un breve análisis de su presencia online, en especial en **{sitio_web}**, hemos identificado un **gran potencial** para optimizar su comunicación y consolidar su posición."

    prompt = f"""
    Eres un experto en ventas y consultoría de branding, especializado en redacción de emails de prospección.
    Tu objetivo es redactar un email **breve, profesional y altamente personalizado** para **{empresa_marca}** con el fin de agendar una **primera reunión** de consultoría.

    El email debe tener la siguiente estructura y tono:

    **Asunto:** Corto, directo, atractivo y que genere curiosidad, mencionando a la empresa si es posible. **Máximo 10 palabras.**
    **Cuerpo del Email (SOLO el cuerpo, SIN saludo inicial ni despedida final):**
    1.  **Breve introducción y gancho:** Comienza con una **observación concisa** de la empresa/marca (**{empresa_marca}**) y su sitio web (**{sitio_web}**). Utiliza la **Observación clave** (Oportunidad Creativa o Necesidad Detectada si están disponibles) para crear un **gancho específico y relevante**. Si no hay una observación clave, haz una mención general sobre su potencial. El objetivo es mostrar que has investigado y añadir valor desde el inicio. Usa **vocabulario claro y sencillo**. (1-2 frases).
        * **Frase de Gancho Sugerida (si aplica):** "{gancho_inicial_frase}"

    2.  **Presentación de Busquets Creativos (tu consultoría):** Introduce a **Busquets Creativos** de forma **clara y concisa**. Destaca **nuestra propuesta de valor diferencial**: **solucionamos y ejecutamos, no solo diagnosticamos**. Menciona **uno o dos pilares de trabajo más relevantes** para la empresa (**{empresa_marca}**) según su categoría, industria o sector. Enfócate en cómo podemos aportar **resultados tangibles**. Usa **lenguaje directo y simple**. (2-3 frases, en párrafos separados si es necesario para mayor legibilidad).

    3.  **Llamada a la acción (Call to Action - CTA):** Propón claramente una **primera reunión** para una **toma de contacto**. El objetivo es explorar cómo Busquets Creativos puede ayudarles a alcanzar sus objetivos o resolver la necesidad detectada. La CTA debe ser **clara y facilitar el siguiente paso**. (1 frase).
        * **CTA Sugerida:** "¿Le gustaría establecer una **primera reunión** para una **toma de contacto** y explorar cómo podemos ayudarle a potenciar a **{empresa_marca}**?"

    **Consideraciones clave para el modelo:**
    * **Tono:** **Formal (trato de "Usted").**
    * **Personalización:** Cada frase debe sentirse **relevante** para **{empresa_marca}**.
    * **Brevedad:** El email debe ser **muy conciso** (máximo 5-7 frases en total, distribuidas en 3 párrafos cortos).
    * **Valor:** El email debe implicar un **valor potencial** desde el primer párrafo.
    * **Profesionalismo:** Tono **respetuoso y experto**.
    * **Claridad:** Usa **vocabulario básico y claro**, evitando jerga excesiva.
    * **Negritas:** Utiliza **negritas** para resaltar las palabras más importantes como la **marca de la empresa**, **Busquets Creativos**, **solucionamos y ejecutamos**, **primera reunión** y **toma de contacto**, etc. No abuses de ellas.

    ---
    **REGLA FUNDAMENTAL DE SALIDA:**
    DEBES responder **SOLAMENTE** con un objeto JSON válido.
    NO incluyas ningún texto explicativo, introducción, ni nada fuera del objeto JSON.
    El JSON debe contener exactamente dos claves: `"asunto"` y `"cuerpo_email"`.
    El valor de `"cuerpo_email"` debe ser el texto completo del email en formato Markdown, SIN saludo inicial ni despedida final.
    ---

    --- ANÁLISIS DE BRANDING DE LA EMPRESA (solo para contexto si necesitas extraer un gancho muy breve si las observaciones clave están vacías) ---
    {analisis_branding.strip()}

    --- INFORMACIÓN DE LA EMPRESA CLIENTE ---
    Nombre de la Empresa/Marca: {empresa_marca}
    Email de Contacto (si disponible): {email_contacto}
    Sitio Web: {sitio_web}
    Categoría: {info_empresa_para_email.get('categoría', 'N/A')}
    Industria: {info_empresa_para_email.get('industria', 'N/A')}
    Sector: {info_empresa_para_email.get('sector', 'N/A')}
    Tamaño de Empresa: {info_empresa_para_email.get('tamaño_empresa', 'N/A')}
    Público Objetivo: {info_empresa_para_email.get('público_objetivo', 'N/A')}
    Observación clave (Oportunidad Creativa detectada): {oportunidad_creativa if oportunidad_creativa else 'No especificada'}
    Observación clave (Necesidad Detectada): {necesidad_detectada if necesidad_detectada else 'No especificada'}


    --- INFORMACIÓN SOBRE BUSQUETS CREATIVOS ---
    {info_busquets_creativos.strip()}

    --- INSTRUCCIONES FINALES DE SALIDA ---
    Devuelve el contenido directamente en texto Markdown, sin ningún objeto JSON.

    1. Comienza con una línea de asunto:  
    **Asunto:** (asunto breve, atractivo y personalizado)

    2. Después, escribe el cuerpo del email directamente, sin saludo inicial ni despedida final. Usa párrafos claros, negritas cuando sea relevante, y mantén el tono profesional, claro y breve.

    NO escribas ningún comentario, explicación o introducción. Solo el asunto y el cuerpo.

    """

    return textwrap.dedent(prompt).strip()

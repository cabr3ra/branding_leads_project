def get_col_map(sheet):
    encabezados = sheet.row_values(1)
    return {nombre.strip(): idx + 1 for idx, nombre in enumerate(encabezados)}

def get_row_data(values, col_map):
    data = {}
    for key, idx in col_map.items():
        data[key.lower().replace(" ", "_")] = values[idx - 1] if len(values) >= idx else ""
    return data

def num_to_column(n):
    """Convierte un número a una letra de columna estilo Excel (1=A, 27=AA, etc.)."""
    result = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        result = chr(65 + remainder) + result
    return result

def similar(a, b):
    """Devuelve True si strings son suficientemente similares (puedes ajustar lógica)."""
    a, b = a.lower(), b.lower()
    return a == b or a.replace(" ", "") == b.replace(" ", "") or a in b or b in a


def update_headline(sheet, columnas):
    filas_datos = sheet.get_all_values()
    total_filas = len(filas_datos)
    encabezados_actuales = filas_datos[0] if filas_datos else []

    # Mapeo de columnas antiguas que no están exactamente en nuevas columnas
    # para detectar renombres con similitud
    columnas_set = set(columnas)
    renombres = {}
    for old_col in encabezados_actuales:
        if old_col not in columnas_set:
            # Buscar nuevo nombre similar
            for new_col in columnas:
                if new_col not in encabezados_actuales and similar(old_col, new_col):
                    renombres[old_col] = new_col
                    break

    # Mapeo índices encabezados actuales
    indice_actual = {h: i for i, h in enumerate(encabezados_actuales)}

    # Construimos matriz nueva
    matriz_nueva = []

    # Procesar filas (excepto la fila 1)
    for fila in filas_datos[1:]:
        fila_nueva = []
        for col_name in columnas:
            # Buscar índice en encabezados antiguos:
            # 1) Exacto
            idx = indice_actual.get(col_name)
            # 2) Si no hay, buscar en renombres que mapean a col_name
            if idx is None:
                # buscar old_col cuyo renombre sea col_name
                old_cols = [old for old, new in renombres.items() if new == col_name]
                if old_cols:
                    idx = indice_actual.get(old_cols[0])

            valor = fila[idx] if idx is not None and idx < len(fila) else ""
            fila_nueva.append(valor)
        matriz_nueva.append(fila_nueva)

    # Actualizar fila 1 con encabezados deseados
    sheet.update("A1", [columnas])

    if total_filas > 1:
        last_col_letter = num_to_column(len(columnas))
        sheet.update(f"A2:{last_col_letter}{total_filas}", matriz_nueva)

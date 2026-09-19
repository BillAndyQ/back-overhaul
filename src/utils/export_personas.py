import pandas as pd
from secrets import token_hex

# ==================== CONFIGURACIÓN PARA PERSONAS ====================
configuracion_columnas_persona = {
    "n_ot": "N° Orden de Trabajo",           # Si existe en tus datos
    "empresa": "Empresa",
    "ruc": "RUC",
    "modalidad": "Modalidad",
    "cursos": "Cursos",
    "nombres": "Nombres",
    "apellidos": "Apellidos",
    "dni": "DNI",
    "fecha": "Fecha",
    "aprobo": "Aprobó",
    "certificadora": "Entidad Certificadora",
    "proyecto": "Proyecto",
    "instructor": "Instructor",
    "certificado": "Certificado",
    "comentarios": "Comentarios",
    "n_veces": "N° Veces",
    # "archivo_foto_pdf": "Archivo Foto/PDF"  # Comentado porque suele ser un archivo
}

def exportar_a_excel_personas(data, nombre_archivo="reporte_personas.xlsx"):
    """
    Exporta datos de personas (FormDataOTPersona) a Excel.
    """
    if not data:
        print("No hay datos para exportar.")
        return None

    # 1. Filtrar registros (ajusta según tu estructura)
    data_filtrada = [
        item for item in data 
        if item.get('registered') != False and item.get('deleted') != True
    ]

    if not data_filtrada:
        print("No hay datos válidos para exportar después del filtro.")
        return None

    # 2. Crear DataFrame
    df = pd.DataFrame(data_filtrada)

    # 3. Mantener solo las columnas configuradas
    columnas_a_mantener = list(configuracion_columnas_persona.keys())
    # Filtrar solo las que realmente existen en los datos
    columnas_existentes = [col for col in columnas_a_mantener if col in df.columns]
    
    df = df[columnas_existentes]
    
    # 4. Renombrar columnas
    df.rename(columns=configuracion_columnas_persona, inplace=True)

    # 5. Generar nombre temporal
    name_temp = token_hex(4) + "_" + nombre_archivo

    # 6. Exportar a Excel con formato
    with pd.ExcelWriter(name_temp, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Personas')

        worksheet = writer.sheets['Personas']

        # Ajuste automático de ancho de columnas
        for col in worksheet.columns:
            max_length = 0
            column = col[0].column_letter
            for cell in col:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    continue
            adjusted_width = min(max_length + 4, 50)  # límite máximo razonable
            worksheet.column_dimensions[column].width = adjusted_width

        # Opcional: Formato para columna "Aprobó"
        if "Aprobó" in df.columns:
            # Puedes agregar más formato aquí si lo deseas
            pass

    print(f"✅ Archivo generado: {name_temp}")
    return name_temp
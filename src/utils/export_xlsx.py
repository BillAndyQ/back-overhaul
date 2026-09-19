import pandas as pd
from secrets import token_hex

# {
#         "id": 27,
#         "informe_campo_url": "bucket\\OM-06-2026-000053\\27\\informeCampo.pdf",
#         "informe_final_url": null,
#         "certificado_url": null,
#         "created_at": "2026-06-26T21:05:19.009802",
#         "updated_at": "2026-06-26T21:05:19.022282",
#         "id_ot_equipo": 55
#     },
configuracion_columnas = {
        "n_ot": "N° Orden de Trabajo",
        "empresa": "Nombre Empresa",
        "ruc": "RUC",
        "placa": "Placa",
        "estado": "Estado Actual",
        "fecha_servicio": "Fecha de Servicio",
        "certificadora": "Entidad Certificadora",
        "tipo_unidad": "Tipo Unidad",
        "ubicacion" : "Ubicacion",
        "tipo_servicio" : "Tipo servicio",
        "inspector" : "Inspector",
        "descripcion" : "Descripcion servicio",
    }

def exportar_a_excel(data, nombre_archivo="reporte_equipos.xlsx"):
    # CONFIGURACIÓN: Define aquí qué columnas quieres y cómo se llamarán
    # Solo las llaves presentes aquí se incluirán en el Excel.

    # 1. Filtrar los que tienen registered == True
    data_filtrada = [item for item in data if item.get('registered') == True and item.get('deleted') == False]
    
    if not data_filtrada:
        print("No hay datos para exportar.")
        return

    # 2. Crear DataFrame y seleccionar solo las columnas deseadas
    df = pd.DataFrame(data_filtrada)
    
    # Nos quedamos solo con las columnas que están en nuestra configuración
    columnas_a_mantener = list(configuracion_columnas.keys())
    df = df[columnas_a_mantener]
    
    # Renombramos las columnas usando el diccionario
    df.rename(columns=configuracion_columnas, inplace=True)

    name_temp = token_hex(4)+ nombre_archivo
    # 3. Guardar a Excel
    with pd.ExcelWriter(name_temp, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Equipos')
        
        # Ajuste automático de ancho de columnas
        worksheet = writer.sheets['Equipos']
        for col in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in col)
            worksheet.column_dimensions[col[0].column_letter].width = max_length + 4

    return name_temp

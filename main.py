from pathlib import Path
from typing import Optional

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.connection_db import get_db
from src.repository import EquipoRepository
from src.schema import PersonaRequest, RequestOTEquipo
from src.services import service_create_ot, service_create_ot_init
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, Form, UploadFile, File, HTTPException

from src.utils.export_personas import exportar_a_excel_personas
from src.utils.export_xlsx import exportar_a_excel
from src.utils.file_manager import save_file

# ROUTERS
from src.empresas.route import router as route_empresas
from src.cursos.router import router as route_cursos
from src.inscripciones.routes import route as route_inscripciones
from src.facturas.routes import route as route_facturas
from src.dashboard.routes import router as route_dashboard

app = FastAPI()
app.include_router(route_empresas, prefix="/api/v1/empresas", tags=["Empresas"])
app.include_router(route_cursos, prefix="/api/v1/cursos", tags=["Cursos"])
app.include_router(route_facturas, prefix="/api/v1/facturas", tags=["Facturas"])
app.include_router(route_dashboard, prefix="/api/v1/dashboard", tags=["Dashboard"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Origen de tu app React
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (POST, GET, etc.)
    allow_headers=["*"], # Permite todos los encabezados
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# api/v1/new-ot
@app.post("/api/v1/create_ot")
def create_ot(db: Session = Depends(get_db)):
    new_ot : str =  service_create_ot(db)
    return {"n_ot": new_ot}

@app.post("/api/v1/create_ot_persona")
def create_ot_persona_init(db: Session = Depends(get_db)):
    new_ot : str =  service_create_ot_init(db)
    return {"n_ot": new_ot}

@app.put("/api/v1/ot-equipos/{n_ot}")
def update_ot_equipo(dataOTEquipo : RequestOTEquipo, n_ot : str,db: Session = Depends(get_db)):
    repo = EquipoRepository(db)
    data = dataOTEquipo.model_dump()
    repo.actualizar_ot_equipo(data, n_ot)
    return {"message": f"OT {n_ot} Registrado con exito!"}
        

@app.get("/api/v1/ot-equipos/{n_ot}")
def get_ot_equipo(n_ot : str,db: Session = Depends(get_db)):
    repo = EquipoRepository(db)
    data = repo.obtener_ot_equipo(n_ot)
    return data

@app.get("/api/v1/ot-equipos/{n_ot}/equipos")
def get_all_equipos(n_ot : str,db: Session = Depends(get_db)):
    repo = EquipoRepository(db)
    id_ot_equipo = repo.get_id_of_ot(n_ot)
    data = repo.get_equipos_of_ot(id_ot_equipo)
    return data

# Todas las ordenes de trabajo
@app.get("/api/v1/ot-equipos/")
def get_all_ot_equipos(db: Session = Depends(get_db)):
    repo = EquipoRepository(db)
    data = repo.get_all_ot_equipos()
    return data

# get_all_ot_personas
# Todas las ordenes de Personas
@app.get("/api/v1/ot-personas")
def get_all_ot_personas(db: Session = Depends(get_db)):
    repo = EquipoRepository(db)
    data = repo.get_all_ot_personas()
    return data

@app.get("/api/v1/ot-personas/{n_ot}")
def get_all_ot_personas(n_ot, db: Session = Depends(get_db)):
    repo = EquipoRepository(db)
    data = repo.get_ot_persona_by_n_ot(n_ot)
    return data

@app.post("/api/v1/ot-personas")
async def registrar_persona(datos: PersonaRequest, db: Session = Depends(get_db)):
    repo = EquipoRepository(db)
    persona_creada = repo.crear_persona(datos)
    
    if not persona_creada:
        raise HTTPException(
            detail="Error al registrar la persona"
        )
    
    return {"message": "Persona registrada con éxito", "id": persona_creada.id}

@app.put("/api/v1/ot-personas/{n_ot}")
async def actualizar_persona(
    n_ot: str, 
    datos: PersonaRequest, 
    db: Session = Depends(get_db)
):
    repo = EquipoRepository(db)
    persona_actualizada = repo.actualizar_persona(n_ot, datos)

    if not persona_actualizada:
        raise HTTPException(
            detail=f"No se encontró una persona {n_ot}"
        )
    return {"message": "Persona actualizada con éxito"}

@app.delete("/api/v1/ot-personas/{n_ot}")
async def actualizar_persona(
    n_ot: str, 
    db: Session = Depends(get_db)
):
    repo = EquipoRepository(db)
    persona = repo.eliminar_personas_por_ot(n_ot)

    if not persona:
        raise HTTPException(
            detail=f"No se encontró una persona {n_ot}"
        )
    return {"message": "Se elimino con exito"}

# exportar_a_excel
@app.get("/api/v1/ot-equipos/report/all")
def get_ot_equipos_report(db: Session = Depends(get_db)):
    repo = EquipoRepository(db)
    data = repo.get_all_ot_equipos_join()
    
    if not data:
        raise HTTPException(status_code=404, detail="No hay datos para exportar")

    file_path = exportar_a_excel(data)
    
    return FileResponse(
        path=file_path, 
        filename="Reporte_Equipos.xlsx", 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    
@app.get("/api/v1/ot-personas/report/all")
def get_ot_personas_report(db: Session = Depends(get_db)):
    repo = EquipoRepository(db)
    data = repo.get_all_ot_personas()
    
    if not data:
        raise HTTPException(status_code=404, detail="No hay datos para exportar")

    file_path = exportar_a_excel_personas(data)
    
    return FileResponse(
        path=file_path, 
        filename="Reporte_Equipos.xlsx", 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Todas las ot y tbm todos los equipos
@app.get("/api/v1/ot-equipos/equipos/all")
def get_all_ot_equipos_join(db: Session = Depends(get_db)):
    repo = EquipoRepository(db)
    data = repo.get_all_ot_equipos_join()
    return data



@app.post("/api/v1/ot-equipos/{n_ot}/equipo")
async def registrar(
    n_ot: str,
    # Campos de texto del formulario
    tipo_unidad: str = Form(...),
    placa: str = Form(...),
    ubicacion: str = Form(...),
    tipo_servicio: str = Form(...),
    fecha_servicio: str = Form(...),
    inspector: str = Form(...),
    descripcion: str = Form(...),
    # Archivos
    informeCampo: Optional[UploadFile] = File(None),
    informeFinal: Optional[UploadFile] = File(None),
    certificado: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    repo = EquipoRepository(db)
    
    # 1. Obtener ID de la OT
    id_ot_equipo = repo.get_id_of_ot(n_ot)
    if not id_ot_equipo:
        raise HTTPException(status_code=404, detail="OT no encontrada")

    # 2. Lógica de archivos (aquí deberías guardarlos y obtener las rutas)
    # Ejemplo: ruta = save_file(informeCampo)

    # 3. Construir el diccionario con los datos
    datos_dict = {
        "id_ot_equipo": id_ot_equipo,
        "tipo_unidad": tipo_unidad,
        "placa": placa,
        "ubicacion": ubicacion,
        "tipo_servicio": tipo_servicio,
        "fecha_servicio": fecha_servicio,
        "inspector": inspector,
        "descripcion": descripcion,
        
    }
    
    for nombre, valor in datos_dict.items():
        if valor == "undefined" or valor is None:
            raise HTTPException(
                status_code=422, 
                detail=f"El campo '{nombre}' está llegando como 'undefined'. Verifica tu FormData en el frontend."
            )

    try:
        equipo = repo.crear_equipo(datos_dict)
        equipo_id = equipo.id
        update_data = {}
        if informeCampo:
            update_data["informe_campo_url"] = await save_file(informeCampo, n_ot, equipo_id, "informeCampo")
            
        if informeFinal:
            update_data["informe_final_url"] = await save_file(informeFinal, n_ot, equipo_id, "informeFinal")
            
        if certificado:
            update_data["certificado_url"] = await save_file(certificado, n_ot, equipo_id, "certificado")
            
        exito = repo.actualizar_equipo(equipo_id, update_data)
        
        return {"id": equipo.id, "message": "Equipo creado con éxito"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.patch("/api/v1/ot-equipos/{n_ot}/equipo/{equipo_id}")
async def actualizar(
    n_ot: str,
    equipo_id: int,
    # Hacemos todos los campos opcionales con None
    tipo_unidad: Optional[str] = Form(None),
    placa: Optional[str] = Form(None),
    ubicacion: Optional[str] = Form(None),
    tipo_servicio: Optional[str] = Form(None),
    fecha_servicio: Optional[str] = Form(None),
    inspector: Optional[str] = Form(None),
    descripcion: Optional[str] = Form(None),
    # Archivos opcionales
    informeCampo: Optional[UploadFile] = File(None),
    informeFinal: Optional[UploadFile] = File(None),
    certificado: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    repo = EquipoRepository(db)
    
    # 1. Construir diccionario solo con los valores que NO son None
    update_data = {}
    
    # Lista de campos de texto a verificar
    campos_texto = {
        "tipo_unidad": tipo_unidad,
        "placa": placa,
        "ubicacion": ubicacion,
        "tipo_servicio": tipo_servicio,
        "fecha_servicio": fecha_servicio,
        "inspector": inspector,
        "descripcion": descripcion
    }
    
    for key, value in campos_texto.items():
        if value is not None and value != "undefined":
            update_data[key] = value

    # 2. Manejo de archivos (si se envían nuevos, actualizamos la ruta)
    
    if informeCampo:
        update_data["informe_campo_url"] = await save_file(informeCampo, n_ot, equipo_id, "informeCampo")
        
    if informeFinal:
        update_data["informe_final_url"] = await save_file(informeFinal, n_ot, equipo_id, "informeFinal")
        
    if certificado:
        update_data["certificado_url"] = await save_file(certificado, n_ot, equipo_id, "certificado")
    
    # 3. Llamar al repositorio para actualizar
    try:
        exito = repo.actualizar_equipo(equipo_id, update_data)
        if not exito:
            raise HTTPException(status_code=404, detail="Equipo no encontrado")
        return {"message": "Equipo actualizado con éxito"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    
@app.delete("/api/v1/ot-equipos/{n_ot}/equipo/{equipo_id}")
async def delete_equipo(equipo_id : int,db: Session = Depends(get_db)):
    repo = EquipoRepository(db)
    repo.delete_equipo(equipo_id)
    return {
        "message" : "Equipo eliminado con éxito"
    }
    
# Eliminar orde de trabajo de equipo
@app.delete("/api/v1/ot-equipos/{equipo_id}")
async def delete_ot_equipo(equipo_id : int,db: Session = Depends(get_db)):
    repo = EquipoRepository(db)
    repo.delete_ot_equipo(equipo_id)
    return {
        "message" : "Orden de Equipo eliminado con éxito"
    }
    
Path("bucket").mkdir(exist_ok=True)
app.mount("/files", StaticFiles(directory="bucket"), name="static")


import aiofiles
from pathlib import Path
from fastapi import UploadFile

async def save_file(file: UploadFile, n_ot: str, id_ot: int, nameFile: str) -> str:
    # Asegura que leemos desde el inicio si el archivo fue procesado antes
    await file.seek(0)
    
    extension = Path(file.filename).suffix 
    final_name = Path(nameFile).with_suffix(extension).name
    
    base_dir = Path("bucket") / n_ot / str(id_ot)
    base_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = base_dir / final_name
    
    async with aiofiles.open(file_path, 'wb') as out_file:
        while content := await file.read(1024 * 1024):
            await out_file.write(content)
            
    return str(file_path)
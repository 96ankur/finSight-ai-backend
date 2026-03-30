from typing import Annotated
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, HTTPException, Depends
import os
import aiofiles
from app.ai.rag.ingest import ingest_pdf
from app.schemas.rag import RagFileUpload

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/upload")
async def rag_upload_file(fileData: Annotated[RagFileUpload, Depends()]):
    # Recommended: Validate file type
    if fileData.file.content_type not in {"application/pdf"}:
        raise HTTPException(415, detail="Unsupported file type")

    current_directory = os.getcwd()
    # Define the destination path
    rag_files_dir = os.path.join(current_directory, "rag_files")
    os.makedirs(rag_files_dir, exist_ok=True)
    file_location = os.path.join(rag_files_dir, fileData.file.filename)

    # Asynchronously stream the file in chunks to disk to prevent memory issues
    try:
        async with aiofiles.open(file_location, "wb") as out_file:
            while content := await fileData.file.read(1024 * 1024):  # Read in 1MB chunks
                await out_file.write(content)

        ingest_pdf(file_location, fileData.user_id)
    except Exception as e:
        return {"message": f"There was an error uploading the file: {e}"}
    finally:
        await fileData.file.close()

    return {"message": "File uploaded successfully"}

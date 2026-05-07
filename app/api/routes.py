from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.transcriber import transcribe_audio
from temporalio.client import Client
from temporal.activities import TranscriptionParams
import uuid
import aiofiles
import os


router = APIRouter()

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    return await transcribe_audio(file)

# Nouvel endpoint asynchrone avec Temporal
@router.post("/orchestrate")
async def orchestrate_transcription(file: UploadFile = File(...)):
    # 1. Vérification du format audio
    if not file.content_type.startswith("audio/"):
        raise HTTPException(400, "Le fichier doit être un audio.")
    
    # 2. Sauvegarde temporaire du fichier
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_filename = f"{temp_dir}/{uuid.uuid4()}.wav"
    async with aiofiles.open(temp_filename, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # 3. Connexion à Temporal et démarrage du Workflow
    client = await Client.connect("localhost:7233")
    workflow_id = f"transcription-{uuid.uuid4()}"
    handle = await client.start_workflow(
        "SpeechRecognitionWorkflow",
        TranscriptionParams(file_path=temp_filename),
        id=workflow_id,
        task_queue="transcription-task-queue",
    )
    
    # 4. Retourne immédiatement l'ID du workflow
    return {
        "workflow_id": workflow_id,
        "status": "orchestrated",
        "message": "La transcription a été planifiée. Utilisez GET /orchestrate/status/{workflow_id} pour obtenir le résultat."
    }

@router.get("/orchestrate/status/{workflow_id}")
async def get_orchestration_status(workflow_id: str):
    client = await Client.connect("localhost:7233")
    handle = client.get_workflow_handle(workflow_id)
    result = await handle.describe()
    if result.status.name == "COMPLETED":
        final_result = await handle.result()
        return {"status": "completed", "transcription": final_result.text}
    elif result.status.name == "RUNNING":
        return {"status": "running"}
    else:
        return {"status": result.status.name}

@router.get("/health")
async def health():
    return {"status": "ok"}
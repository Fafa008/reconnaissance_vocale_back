import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from .workflows import SpeechRecognitionWorkflow
from .activities import transcribe_audio

async def start_worker():
    # Se connecter au serveur Temporal local
    client = await Client.connect("localhost:7233")
    
    # Créer et lancer un Worker pour la file d'attente dédiée à la transcription
    worker = Worker(
        client,
        task_queue="transcription-task-queue",
        workflows=[SpeechRecognitionWorkflow],
        activities=[transcribe_audio],
    )
    print("🚀 Worker Temporal démarré, en attente de tâches...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(start_worker())
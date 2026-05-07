from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from .shared_types import TranscriptionParams, TranscriptionResult

@workflow.defn
class SpeechRecognitionWorkflow:
    @workflow.run
    async def run(self, params: TranscriptionParams) -> TranscriptionResult:
        retry_policy = RetryPolicy(
            initial_interval=timedelta(seconds=1),
            maximum_interval=timedelta(seconds=60),
            maximum_attempts=3,
            non_retryable_error_types=["InvalidAudioError"]
        )
        result = await workflow.execute_activity(
            "transcribe_audio_activity",
            params,
            start_to_close_timeout=timedelta(seconds=300),
            retry_policy=retry_policy,
            task_queue="transcription-task-queue"
        )
        return result
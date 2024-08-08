from pydantic import BaseModel
import faster_whisper
import io
import runpod
import logging
import base64
import time
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

# model_path=os.getenv('MODEL_DIR')

whisper_models = {
    "CPU":{
        "base" : faster_whisper.WhisperModel("base", device='cpu', compute_type="int8"),
        "medium" : faster_whisper.WhisperModel("medium", device='cpu', compute_type="int8"),
        "large" : faster_whisper.WhisperModel("large-v3", device='cpu', compute_type="int8")
    },
    # "GPU":{
    #     "base" : faster_whisper.WhisperModel("base", device='cuda', compute_type="int8_float16"),
    #     "medium" : faster_whisper.WhisperModel("medium", device='cuda', compute_type="int8_float16"),
    #     "large" : faster_whisper.WhisperModel("large-v3", device='cuda', compute_type="int8_float16")
    # }
}

class AudioMetadata(BaseModel):
    format: str
    duration: float | None
    bitrate: int | None
    sample_rate: int | None
    channels: int | None

def get_audio_metadata(job, whisper_models=whisper_models):
    """ Handler function that will be used to process jobs. """
    job_input = job['input']

    audio_bytes = base64.b64decode(job_input['audio'])
    file=io.BytesIO(audio_bytes)
    model_size = job_input['model_size']
    language = job_input['language']
    device = job_input['device']

    model = whisper_models[device][model_size]

    segments, info = model.transcribe(
        file,
        beam_size=4,
        language=language,
        condition_on_previous_text=False,
        )

    for segment in segments:
        start_min, start_sec = divmod(segment.start, 60)
        end_min, end_sec = divmod(segment.end, 60)
        t = "%d:%05.2f -> %d:%05.2f ->%s" % (start_min, start_sec, end_min, end_sec, segment.text)
        yield t

runpod.serverless.start(
    {
        "handler": get_audio_metadata,  # Required
        "return_aggregate_stream": True,  # Optional, results available via /run
    }
)
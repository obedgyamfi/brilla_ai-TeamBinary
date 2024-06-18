
import torch
import whisper
from pydub import AudioSegment
import os
import IPython.display as ipd
from IPython.display import Audio, clear_output
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset

# clear_output()

# sample_audio = AudioSegment.from_file(r"/home/ob/Documents/Programming/AI/NLP/projects/BrillaAI-TeamBinary/app/database/audio_data/user_answers_audio/user_answer.wav")
# sample_audio


device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "distil-whisper/distil-large-v2" # Test out the different model sizes here
# model_id = "distil-medium.en"
# model_id = "distil-small.en"

model_short = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model_short.to(device)

processor = AutoProcessor.from_pretrained(model_id)


pipe = pipeline(
    "automatic-speech-recognition",
    model=model_short,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    torch_dtype=torch_dtype,
    device=device
)

# Transcribe audio
# result = pipe(r"/home/ob/Documents/Programming/AI/NLP/projects/BrillaAI-TeamBinary/app/database/audio_data/user_answers_audio/user_answer.wav")

# Print transcript
# print(result["text"])

"""
sample_audio_2 = AudioSegment.from_file(r"/content/audio_riddle_long_form.wav")
sample_audio_2


device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model_id = "distil-whisper/distil-large-v2"  # Test out the different model sizes here

model_long = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
)
model_long.to(device)

processor = AutoProcessor.from_pretrained(model_id)

pipe_long = pipeline(
    "automatic-speech-recognition",
    model=model_long,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=25, # difference
    batch_size=16, # difference
    torch_dtype=torch_dtype,
    device=device,
)

# Transcribe audio
result2 = pipe_long(r"/content/audio_riddle_long_form.wav")

# Print transcript
print(result2["text"])
"""
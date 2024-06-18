

# Make sure the following requirements are installed. Ignore any warnings that show up during installation
#%%bash
#pip install TTS onnx onnxruntime
#sudo apt-get install espeak-ng

#import the required libraries
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.models.vits import Vits
from TTS.utils.audio.numpy_transforms import save_wav
import numpy as np
# import IPython

# Loading the student model
"""
# load the model's config file
student_config=VitsConfig()
student_config.load_json('../app/ai_models_and_data/models_and_data/ai_voice_models/student/student_config.json')
student_config.model_args.speakers_file="../app/ai_models_and_data/models_and_data/ai_voice_models/student/student.pth"
# load the model
student_model=Vits.init_from_config(student_config)
student_model.load_onnx('../app/ai_models_and_data/models_and_data/ai_voice_models/student/student.onnx')

text=  "Hello, Welcome to the National Math and Science Quiz Assistant"
out_path= "../app/speech_output"

# generate the speech
text_inputs = np.asarray(
    student_model.tokenizer.text_to_ids(text, language="en"),
    dtype=np.int64,
)[None, :]
audio = student_model.inference_onnx(text_inputs,speaker_id=0)

# save the synthesized speech
save_wav(wav=audio[0], path=out_path,sample_rate=22050)

# load the audio
# IPython.display.Audio(out_path)
"""
#Loading the quizmistress model

# load the model's config file
qm_config=VitsConfig()
qm_config.load_json('../app/ai_models_and_data/models_and_data/ai_voice_models/Quizmistress/quizmistress_config.json')
qm_config.model_args.speakers_file='../app/ai_models_and_data/models_and_data/ai_voice_models/Quizmistress/quizmistress.pth'
# load the model
qm_model=Vits.init_from_config(qm_config)
qm_model.load_onnx('../app/ai_models_and_data/models_and_data/ai_voice_models/Quizmistress/quizmistress.onnx')

text= "Question 1, solve 3/4 + 2 ?"
out_path='./audio_database/questions_audio/question.wav'

# generate the speech
text_inputs = np.asarray(
    qm_model.tokenizer.text_to_ids(text, language="en"),
    dtype=np.int64,
)[None, :]
audio = qm_model.inference_onnx(text_inputs,speaker_id=0)

# save the synthesized speech
save_wav(wav=audio[0], path=out_path,sample_rate=22050)

#load the audio
# IPython.display.Audio(out_path)

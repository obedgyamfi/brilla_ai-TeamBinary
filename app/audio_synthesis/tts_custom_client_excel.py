import os
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.models.vits import Vits
from TTS.utils.audio.numpy_transforms import save_wav
import numpy as np

class TextToSpeechSynthesizer:
    def __init__(self, model_type):
        
        # Model setup
        self.model_type = model_type
        self.config = VitsConfig()
        self.model = None
        self.load_model()

    def load_model(self):
        base_path = '../database/ai_voice_models/tts_voice_model'
        if self.model_type == 'quizmistress':
            model_path = os.path.join(base_path, 'Quizmistress')
            self.config.load_json(os.path.join(model_path, 'quizmistress_config.json'))
            self.config.model_args.speakers_file = os.path.join(model_path, 'quizmistress_config.json')
            self.model = Vits.init_from_config(self.config)
            self.model.load_onnx(os.path.join(model_path, 'quizmistress.onnx'))
        elif self.model_type == 'student':
            model_path = os.path.join(base_path, 'student')
            self.config.load_json(os.path.join(model_path, 'student_config.json'))
            self.config.model_args.speakers_file = os.path.join(model_path, 'student_config.json')
            self.model = Vits.init_from_config(self.config)
            self.model.load_onnx(os.path.join(model_path, 'student.onnx'))
        else:
            raise ValueError(f"Unknown model type: {self.model_type}, Model")
    
    def synthesize_text(self, text, output_file=None):
        text_inputs = np.asarray(
            self.model.tokenizer.text_to_ids(text, language="en"),
            dtype=np.int64
        )[None, :]
        
        audio = self.model.inference_onnx(text_inputs, speaker_id=0)
        
        if output_file is None:
            output_file = os.path.join(self.output_dir, f"{self.model_type}_{hash(text)}.wav")
        
        save_wav(wav=audio[0], path=output_file, sample_rate=22050)
        return output_file
    



# Initialize the tts by 
output_dir = '/home/ob/Documents/Programming/AI/NLP/projects/BrillaAI-TeamBinary/app/database/audio_data/is_correct.wav'
model_type = 'quizmistress'

tts = TextToSpeechSynthesizer(model_type)

tts.load_model()

text_to_synth = "Your answer is correct"

audio_file = tts.synthesize_text(text_to_synth, output_dir)

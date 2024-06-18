import os
from TTS.tts.configs.vits_config import VitsConfig
from TTS.tts.models.vits import Vits
from TTS.utils.audio.numpy_transforms import save_wav
import numpy as np
import sqlite3

class TextToSpeechSynthesizer:
    def __init__(self, db_path='./nsmq.db', output_dir='./output', model_type='quizmistress'):
        # Database setup
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        # Output directory setup
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Model setup
        self.model_type = model_type
        self.config = VitsConfig()
        self.model = None
        self.load_model()
    
    def load_model(self):
        base_path = '../app/ai_models_and_data/models_and_data/ai_voice_models/'
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
            raise ValueError(f"Unknown model type: {self.model_type}")
    
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
    
    def synthesize_question(self, question_sn):
        self.cursor.execute('''
            SELECT has_preamble, preamble_text, question
            FROM questions
            WHERE sn = ?
        ''', (question_sn,))
        
        result = self.cursor.fetchone()
        print(result)
        if not result:
            raise ValueError(f"No question found with SN: {question_sn}")
        
        has_preamble, preamble_text, question_text = result
        
        output_files = []
        
        if has_preamble:
            file_path = self.synthesize_text(preamble_text)
            output_files.append(file_path)
        
        question_prompt = f"Question {question_sn}, {question_text}"
        file_path = self.synthesize_text(question_prompt)
        output_files.append(file_path)
        
        return output_files
    
    def synthesize_answer(self, question_sn):
        self.cursor.execute('''
            SELECT answer, has_calculations
            FROM questions
            WHERE sn = ?
        ''', (question_sn,))
        
        result = self.cursor.fetchone()
        if not result:
            raise ValueError(f"No question found with SN: {question_sn}")
        
        answer_text, has_calculations = result
        
        output_files = []
        
        answer_prompt = f"The answer to question {question_sn} is: {answer_text}"
        file_path = self.synthesize_text(answer_prompt)
        output_files.append(file_path)
        
        if has_calculations:
            calc_prompt = f"This answer involves calculations. Please refer to the displayed solution for question {question_sn}."
            file_path = self.synthesize_text(calc_prompt)
            output_files.append(file_path)
        
        return output_files
    
    def close(self):
        self.conn.close()

# Usage:
#db_path = '../app/database.db'  # Replace with your actual database path
#output_dir = '../app/speech_output'

# Using the quizmistress voice
#qm_synth = TextToSpeechSynthesizer(db_path, output_dir, model_type='quizmistress')

# Synthesize question 1
#question_files = qm_synth.synthesize_question(1)
#print(f"Question audio files: {question_files}")

# Synthesize answer to question 1
#answer_files = qm_synth.synthesize_answer(1)
#print(f"Answer audio files: {answer_files}")

# Clean up
#qm_synth.close()

# You can also use the student voice if needed
#student_synth = TextToSpeechSynthesizer(db_path, output_dir, model_type='student')
#student_synth.synthesize_text("I think I understand the solution now.")
#student_synth.close()

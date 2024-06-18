from vosk import Model, KaldiRecognizer
import json
import wave

class SpeechToTextSynthesizer:
    def __init__(self, model_path):
        # Load the Vosk model
        self.model = Model(model_path)

    def transcribe(self, audio_file_path):
        # Open the audio file
        with wave.open(audio_file_path) as audio_file:
            # Get audio properties
            sample_rate = audio_file.getframerate()
            audio_data = audio_file.readframes(audio_file.getnframes())

            # Create a recognizer object with the model and sample rate
            recognizer = KaldiRecognizer(self.model, sample_rate)

            # Process the entire audio data
            recognizer.AcceptWaveform(audio_data)

            # Get the final result
            final_result = recognizer.FinalResult()
            
            # Parse the JSON string into a dictionary
            final_result_dict = json.loads(final_result)

            # Extract and return the transcription result as a single string
            if 'text' in final_result:
                return final_result_dict['text']
            else:
                return ""
            

# Example usage:
if __name__ == "__main__":
    model_path = "/home/ob/Documents/Programming/AI/NLP/projects/BrillaAI-TeamBinary/app/database/ai_voice_models/stt_voice_model/vosk-model-en-us-0.22"
    audio_file_path =  "../database/audio_data/user_answers_audio/user_answer.wav"
    transcriber = SpeechToTextSynthesizer(model_path)
    transcription = transcriber.transcribe(audio_file_path)
    print(transcription)
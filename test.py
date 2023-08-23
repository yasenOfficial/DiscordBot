from TTS.api import TTS

# List available 🐸TTS models and choose the first one
tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=True)
voice_type = "p230"
# Init TTS
# ❗ Since this model is multi-speaker and multi-lingual, we must set the target speaker and the language
# Text to speech with a numpy output
wav = tts.tts("This is a test! This is also a test!!", speaker=tts.speakers[0], language=tts.languages[0])
# Text to speech to a file
tts.tts_to_file(text="Hello world!", speaker=tts.speakers[0], language=tts.languages[0], file_path="output.wav")
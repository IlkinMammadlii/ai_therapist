import tempfile, os, pygame, settings
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import CancellationDetails

_cfg = speechsdk.SpeechConfig(
    subscription=settings.AZURE_SPEECH_KEY,
    region=settings.AZURE_SPEECH_REGION,
)
_cfg.speech_synthesis_voice_name = settings.TTS_VOICE

def speak(text: str):
    if not settings.USE_TTS:
        return None

    synth = speechsdk.SpeechSynthesizer(_cfg, None)
    res = synth.speak_text_async(text).get()

    if res.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("TTS error →", res.reason, CancellationDetails.from_result(res).error_details)
        return None

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(res.audio_data)
        tmp_path = tmp.name

    snd = pygame.mixer.Sound(tmp_path)
    snd.play()
    os.unlink(tmp_path)  # cleanup temp file
    return snd

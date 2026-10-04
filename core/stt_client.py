import azure.cognitiveservices.speech as speechsdk, settings
from azure.cognitiveservices.speech import CancellationDetails

def listen() -> str:
    """Record from mic until pause; return transcript or empty string."""
    if not settings.USE_STT:
        return ""

    speech_cfg = speechsdk.SpeechConfig(
        subscription=settings.AZURE_SPEECH_KEY,
        region=settings.AZURE_SPEECH_REGION
    )
    audio_cfg = speechsdk.audio.AudioConfig(use_default_microphone=True)
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_cfg,
        audio_config=audio_cfg
    )

    print("🎙️ Listening...")
    result = recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("✔️ STT Success:", result.text)
        return result.text

    if result.reason == speechsdk.ResultReason.Canceled:
        details = CancellationDetails.from_result(result)
        print("❌ STT Canceled:", details.reason)
        if details.error_details:
            print("🔍 STT Error Details:", details.error_details)
    else:
        print("⚠️ STT Failed:", result.reason)

    return ""

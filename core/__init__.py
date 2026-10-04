"""
core package – aggregates helper modules so you can
`import core.llm_client as llm_client` etc.
"""
from importlib import import_module

for _m in ("llm_client", "tts_client", "stt_client", "env_predict", "ui"):
    globals()[_m] = import_module(f"{__name__}.{_m}")

__all__ = ["llm_client", "tts_client", "stt_client", "env_predict", "ui"]
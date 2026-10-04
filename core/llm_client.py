import openai, settings

openai.api_type    = "azure"
openai.api_base    = settings.AZURE_OPENAI_ENDPOINT  # no trailing slash!
openai.api_key     = settings.AZURE_OPENAI_KEY
openai.api_version = settings.AZURE_OPENAI_API_VER

def chat(messages, temperature: float = 0.7) -> str:
    """
    messages = [
        {"role": "system", "content": "..."},
        {"role": "user",   "content": "..."},
        ...
    ]
    """
    resp = openai.ChatCompletion.create(
        engine=settings.AZURE_OPENAI_DEPLOYMENT,
    messages=messages,
    temperature=0.6,          # a bit lower → less rambling
    max_tokens=120,           # hard upper-bound ≈ 3 short lines
    request_timeout=30
    )
    return resp["choices"][0]["message"]["content"]

import bleach

def sanitize_text(text: str) -> str:
    if not text:
        return text
    return bleach.clean(text)
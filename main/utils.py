import re

def choose_best_sentence(text: str, candidates: list[str] | None = None) -> str:
    interjections = {"certainly", "sure", "okay", "ok", "right away", "one moment", "of course", "got it", "alright", "yes"}
    def clean_sent(s: str) -> str:
        return s.strip().strip('\n\r "')
    sentences: list[str] = []
    if candidates:
        for c in candidates:
            if not c or not isinstance(c, str):
                continue
            parts = re.split(r'(?<=[.!?])\s+', c)
            for p in parts:
                s = clean_sent(p)
                if s:
                    sentences.append(s)
    if text:
        parts = re.split(r'(?<=[.!?])\s+', text)
        for p in parts:
            s = clean_sent(p)
            if s:
                sentences.append(s)
    def is_substantive(s: str) -> bool:
        low = s.lower().strip('!.,')
        if low in interjections:
            return False
        if len(s) < 8:
            return False
        return ' ' in s
    for s in sentences:
        if is_substantive(s):
            return s
    for s in reversed(sentences):
        if is_substantive(s):
            return s
    if sentences:
        return max(sentences, key=lambda x: len(x))
    return (text or '').strip()

def is_refusal(s: str) -> bool:
    if not s:
        return False
    low = s.lower()
    patterns = [
        "as an ai language model",
        "i do not have access",
        "i cannot",
        "i'm unable",
        "cannot provide",
        "unable to",
        "i do not have",
        "i don't have",
    ]
    return any(p in low for p in patterns)

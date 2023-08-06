def underscore(s: str) -> str:
    return ''.join(['_' + c.lower() if c.isupper() else c for c in s]).lstrip('_')

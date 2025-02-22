# myapp/utils.py
import re

def extract_json(raw_text: str) -> str:
    """
    استخراج JSON از خروجی هوش مصنوعی
    """
    pattern = r"```(?:json)?(.*?)```"
    matches = re.findall(pattern, raw_text, flags=re.DOTALL)

    if matches:
        return matches[0].strip()
    return raw_text.strip()
import re

# simple demo rules
REQUIREMENTS = {
    "manufacturer": [r"Tata Steel", r"TataSteel", r"Tata"],
    "fire_rating": [r"2[- ]?hour", r"2hr", r"2 hour"],
    "astm": [r"\bASTM\b"],
    "datasheet": [r"data ?sheet", r"datasheet"]
}

def find_snippet(text, pattern):
    m = re.search(pattern, text, flags=re.IGNORECASE)
    if not m:
        return None
    start = max(0, m.start() - 40)
    end = min(len(text), m.end() + 40)
    return text[start:end].replace("\n", " ")

def quick_extract(text: str):
    issues = []
    for key, patterns in REQUIREMENTS.items():
        found = False
        evidence = None
        for p in patterns:
            snippet = find_snippet(text, p)
            if snippet:
                found = True
                evidence = snippet
                break
        if not found:
            issues.append({"field": key, "issue": "missing_or_mismatch", "evidence": None})
        else:
            # include evidence for positive matches (useful for demo)
            issues.append({"field": key, "issue": "found", "evidence": evidence})
    return issues

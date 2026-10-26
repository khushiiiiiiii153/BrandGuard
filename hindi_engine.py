import re

HINDI_HINGLISH_RULES = [
    {
        "id": "HI-001",
        "pattern": r"(सबसे सस्ता|बिलकुल मुफ़्त|100% गारंटी|नंबर 1)",
        "script": "Devanagari",
        "issue": "Unverified Absolute Claim (Devanagari)",
        "preferred": "किफायती / भरोसेमंद",
        "severity": "High"
    },
    {
        "id": "HI-002",
        "pattern": r"\b(sabse sasta|bilkul free|100% guarantee|no\.?1 brand)\b",
        "script": "Hinglish",
        "issue": "Unverified Absolute Claim (Hinglish)",
        "preferred": "Affordable / Trusted",
        "severity": "High"
    },
    {
        "id": "HI-003",
        "pattern": r"\b(zahar|ekdam fadu|bawal|gazab scene)\b",
        "script": "Hinglish",
        "issue": "Inappropriate Casual Slang",
        "preferred": "Aakarshak / Utkrisht",
        "severity": "Medium"
    }
]

def check_hindi_hinglish_compliance(text: str) -> list:
    """Detects compliance violations in Hindi and Hinglish content."""
    findings = []
    
    for rule in HINDI_HINGLISH_RULES:
        matches = re.finditer(rule["pattern"], text, re.IGNORECASE)
        for match in matches:
            findings.append({
                "rule_id": rule["id"],
                "type": f"{rule['issue']} ({rule['script']})",
                "quote": match.group(0),
                "reason": f"Text contains prohibited phrase '{match.group(0)}' under rule {rule['id']}.",
                "severity": rule["severity"],
                "confidence": "1.00 (Pattern Engine)",
                "fix_minimal": f"Replace with approved alternative: '{rule['preferred']}'",
                "fix_moderate": f"Rephrase sentence formally in {rule['script']}",
                "fix_rewrite": f"Remove extreme claims and state verifiable facts"
            })
            
    return findings

# Example execution test
if __name__ == "__main__":
    sample = "Yeh brand sabse sasta hai aur 100% guarantee deta hai. Yeh offer ekdam fadu hai!"
    results = check_hindi_hinglish_compliance(sample)
    print(f"Detected {len(results)} Hindi/Hinglish issues:")
    for r in results:
        print(f"- [{r['severity']}] {r['type']}: '{r['quote']}' -> Suggested: {r['fix_minimal']}")
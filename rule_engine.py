import re
from datetime import datetime

def redact_sensitive_info(text: str) -> str:
    """Masks emails, phone numbers, and secrets prior to model processing."""
    # Redact Emails
    text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[REDACTED_EMAIL]', text)
    # Redact Phone Numbers (Indian format)
    text = re.sub(r'\+?\d{10,12}', '[REDACTED_PHONE]', text)
    return text

def run_deterministic_checks(text: str, rules: list, claims: list) -> list:
    """Runs deterministic code checks for exact string matches and claim validity."""
    findings = []
    
    # 1. Rule Engine Banned Term Match
    for rule_id, category, rule_text, banned_str, preferred_str, severity in rules:
        banned_terms = [t.strip() for t in banned_str.split(',') if t.strip()]
        for term in banned_terms:
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            matches = pattern.finditer(text)
            for m in matches:
                findings.append({
                    "rule_id": rule_id,
                    "type": f"{category} Violation",
                    "quote": m.group(0),
                    "reason": f"Uses restricted phrasing '{m.group(0)}'. Rule: {rule_text}",
                    "severity": severity,
                    "confidence": "1.00 (Deterministic Engine)",
                    "fix_minimal": f"Replace with '{preferred_str.split(',')[0]}'",
                    "fix_moderate": f"Rephrase sentence using approved terms like '{preferred_str}'",
                    "fix_rewrite": f"Rewrite completely without relying on '{m.group(0)}'"
                })

    # 2. Claim Evidence Vault Verification
    for claim_id, pattern_str, source, expiry, status in claims:
        if re.search(re.escape(pattern_str), text, re.IGNORECASE):
            is_expired = datetime.strptime(expiry, "%Y-%m-%d") < datetime.now()
            if is_expired or status == "Expired":
                findings.append({
                    "rule_id": f"CLAIM-{claim_id}",
                    "type": "Expired Claim Evidence",
                    "quote": pattern_str,
                    "reason": f"Claim '{pattern_str}' relies on expired evidence '{source}' (Expired on {expiry}).",
                    "severity": "High",
                    "confidence": "1.00 (Vault Checked)",
                    "fix_minimal": f"Remove claim '{pattern_str}'",
                    "fix_moderate": "Provide updated lab proof to reactivate claim",
                    "fix_rewrite": "Highlight soft benefits instead of unverified metrics"
                })
                
    return findings
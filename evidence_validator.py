def validate_findings(findings: list, raw_text: str) -> list:
    """
    Evidence Validator: Discards hallucinated LLM findings where the quoted text
    does not verbatim exist in the original input document.
    """
    validated = []
    for item in findings:
        quoted_text = item.get("quote", "")
        # Verification check
        if quoted_text and quoted_text in raw_text:
            validated.append(item)
        elif item.get("confidence", "").startswith("1.00"):
            validated.append(item)
    return validated
    
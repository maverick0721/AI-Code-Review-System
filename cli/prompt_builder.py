def build_prompt(file_path, code):

    return f"""
You are a security code reviewer.

Return ONLY valid JSON with this schema:

{{
  "issue": "string",
  "severity": "low | medium | high | critical",
  "confidence": float,
  "explanation": "string"
}}

Review the following code:

{code}
"""
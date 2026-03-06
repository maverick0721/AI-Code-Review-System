def build_prompt(file_path, code_chunk):

    prompt = f"""
You are a senior security engineer reviewing code.

File: {file_path}

Analyze the code and detect security issues.

Return ONLY valid JSON in this format:

{{
  "issue": "<category>",
  "severity": "<low|medium|high|critical>",
  "confidence": <0-1>,
  "explanation": "<short explanation>"
}}

Possible issue categories include:

- hardcoded credential
- sql injection
- command injection
- path traversal
- insecure randomness
- unsafe deserialization
- weak crypto
- eval injection
- insecure temp file
- sensitive data exposure
- insecure ssl
- unsafe file handling
- none

Code:

{code_chunk}
"""

    return prompt
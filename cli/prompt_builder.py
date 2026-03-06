def build_prompt(file_path, code_chunk):

    prompt = f"""
You are a senior software engineer performing a production code review.

File: {file_path}

Review the code for:

1. Security vulnerabilities
2. Logical bugs
3. Performance issues
4. Concurrency risks
5. Code smell
6. Refactoring suggestions

Return structured JSON with:

- issues
- severity (Low / Medium / High / Critical)
- confidence (0-1)

Code to review:

{code_chunk}
"""

    return prompt
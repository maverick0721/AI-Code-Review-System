import re


def extract_changes(diff, max_chunk_size=20):

    chunks = []

    current_file = None
    current_line = 0
    current_chunk = []

    for line in diff.split("\n"):

        if line.startswith("+++ b/"):
            current_file = line[6:]

        if line.startswith("@@"):
            match = re.search(r'\+(\d+)', line)
            if match:
                current_line = int(match.group(1))

        if line.startswith("+") and not line.startswith("+++"):

            current_chunk.append({
                "file": current_file,
                "line": current_line,
                "code": line[1:]
            })

            current_line += 1

            if len(current_chunk) >= max_chunk_size:
                chunks.append(current_chunk)
                current_chunk = []

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
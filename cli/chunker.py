import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

def chunk_code(text, max_tokens=1200, overlap=200):

    tokens = encoding.encode(text)

    chunks = []

    step = max_tokens - overlap

    for i in range(0, len(tokens), step):

        chunk_tokens = tokens[i:i+max_tokens]

        chunk_text = encoding.decode(chunk_tokens)

        chunks.append(chunk_text)

    return chunks
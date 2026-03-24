# AI Code Review System

An AI-powered security code review platform that automatically analyzes pull requests and source code for vulnerabilities using large language models, static analysis tools, and retrieval-augmented reasoning.

The system combines modern LLM inference with traditional security analyzers to produce structured vulnerability reports and automated GitHub pull request comments.

---

## Overview

Modern software projects rely heavily on code reviews to detect bugs and security issues before deployment. However, manual review processes are time-consuming and difficult to scale across large repositories.

This project explores how large language models can assist developers by automatically reviewing code changes, identifying potential vulnerabilities, and providing structured explanations directly within GitHub pull requests.

The platform integrates multiple analysis techniques:

- LLM-based reasoning for security vulnerability detection  
- Static analysis tools for rule-based scanning  
- Retrieval-augmented security knowledge  
- GPU batch inference for efficient model execution  
- GitHub webhook automation for real-time PR reviews  

By combining these components, the system can detect common vulnerabilities such as hardcoded credentials, injection attacks, insecure randomness, weak cryptography, and unsafe file handling.

---

## Features

- AI-powered security code review  
- Automated GitHub pull request analysis  
- GPU-accelerated inference using vLLM  
- Retrieval-Augmented Generation (RAG) for security context  
- Integration with Bandit, Ruff, and Semgrep  
- Structured vulnerability reporting  
- Async batch processing for higher throughput  
- CLI tool for scanning repositories locally  
- Benchmark evaluation framework  
- Docker-based deployment support  

---

## System Architecture

```
GitHub Pull Request
        │
        ▼
GitHub Webhook Bot
        │
        ▼
Diff Parser
        │
        ▼
Code Chunking
        │
        ▼
Static Analysis Layer
(Bandit / Ruff / Semgrep)
        │
        ▼
Security Knowledge Retrieval (RAG)
        │
        ▼
LLM Inference Server
(GPU batching via vLLM)
        │
        ▼
Structured Vulnerability Output
        │
        ▼
GitHub PR Comments + Security Report
```

---

## Project Structure

```
ai-code-review/

cli/
    Command-line interface for local code review

server/
    LLM inference server and batching engine

core/
    Security utilities, static analysis integration, and report generation

evaluation/
    Benchmark scripts and vulnerability datasets

dataset/
    Dataset generation tools

integrations/
    GitHub webhook automation

Dockerfile
docker-compose.yml
Makefile
pyproject.toml
README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/AI-Code-Review-System.git
cd AI-Code-Review-System
```

Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the System

Start the development environment:

```bash
make dev
```

This launches:

- AI inference server (port **8000**)  
- GitHub webhook bot (port **9000**)  
- ngrok tunnel for GitHub webhook communication  

### One-Command Demo (Best for Showcasing)

Run this to start the API, execute multiple sample reviews end-to-end, print structured output, and stop automatically:

```bash
make demo
```

This is the fastest way to explain the project to someone in a live demo.

---

## API Usage

The inference server exposes a REST endpoint.

**Endpoint**

```
POST /review
```

Example request:

```bash
curl -X POST http://localhost:8000/review \
-H "Content-Type: application/json" \
-d '{"prompt":"password = \"123456\""}'
```

Example response:

```json
{
  "results": [
    {
      "issue": "hardcoded credential",
      "severity": "critical",
      "confidence": 1.0,
      "explanation": "Credentials should never be stored directly in source code."
    }
  ]
}
```

---

## CLI Usage

The CLI allows scanning a repository locally without GitHub automation.

```bash
python cli/main.py
```

The tool detects modified files, extracts code diffs, and sends them to the AI server for security review.

---

## Supported Vulnerability Categories

The system detects several common security issues including:

- Hardcoded credentials  
- SQL injection  
- Command injection  
- Path traversal  
- Insecure randomness  
- Unsafe deserialization  
- Weak cryptography  
- Eval injection  
- Sensitive data exposure  
- Insecure temporary file usage  
- Unsafe file handling  
- Insecure SSL configurations  

---

## Evaluation Framework

A benchmark dataset is included to measure model performance.

Run evaluation:

```bash
python -m evaluation.evaluator
```

Metrics reported:

- Precision  
- Recall  
- F1 Score  

This framework helps measure how effectively the system identifies vulnerabilities across different categories.

---

## Docker Deployment

Build containers:

```bash
docker compose build
```

Run services:

```bash
docker compose up
```

Services exposed:

| Service | Port |
|--------|------|
| AI Server | 8000 |
| GitHub Bot | 9000 |

---

## Security Knowledge Base

The retrieval layer enhances model reasoning by providing contextual security information from curated vulnerability sources such as:

- OWASP Top 10  
- Common Weakness Enumeration (CWE)  
- Public vulnerability reports  

This improves reasoning quality and reduces hallucinations.

---

## Example Workflow

1. A developer opens a pull request  
2. GitHub triggers the webhook bot  
3. The system retrieves the pull request diff  
4. Static analyzers scan the code changes  
5. Relevant security knowledge is retrieved  
6. The LLM analyzes the code  
7. Vulnerabilities are posted as pull request comments  

---

## Limitations

While large language models provide powerful reasoning capabilities, they should not replace traditional security auditing entirely.

This system is intended to assist developers and security engineers by highlighting potential risks and improving code review efficiency.

---

## Future Improvements

Potential directions for further development:

- Larger vulnerability datasets  
- Model fine-tuning for secure code analysis  
- Multi-model ensemble inference  
- Security dashboard interface  
- Repository-wide scanning capabilities  
- Continuous learning from developer feedback  

---

## Author

**Shivang Gupta**

---

## License

This project is intended for research and educational use.

import json
import re
import logging

from server.model_loader import load_models


_models = None
_model_load_failed = False
_fallback_logged = False


logger = logging.getLogger(__name__)


def _extract_json(text):
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass

    return {
        "issue": "unknown",
        "severity": "low",
        "confidence": 0.0,
        "explanation": text.strip() if text else "model output parsing failed"
    }


def _heuristic_review(prompt):
    code = (prompt or "").lower()

    if "password =" in code or "passwd =" in code or "api_key" in code:
        return {
            "issue": "hardcoded credential",
            "severity": "high",
            "confidence": 0.7,
            "explanation": "Potential hardcoded credential detected."
        }

    if "eval(" in code:
        return {
            "issue": "eval injection",
            "severity": "high",
            "confidence": 0.8,
            "explanation": "Use of eval may enable arbitrary code execution."
        }

    if "os.system(" in code or "shell=true" in code:
        return {
            "issue": "command injection",
            "severity": "high",
            "confidence": 0.8,
            "explanation": "Command execution path may be injectable."
        }

    return {
        "issue": "none",
        "severity": "low",
        "confidence": 0.5,
        "explanation": "No obvious high-signal issue detected by fallback review."
    }


def _get_models():
    global _models, _model_load_failed
    if _model_load_failed:
        raise RuntimeError("Model initialization previously failed")

    if _models is None:
        try:
            _models = load_models()
        except Exception:
            _model_load_failed = True
            logger.exception("Model loading failed; review pipeline will use heuristic fallback")
            raise

    return _models


def run_llm(prompt):
    return run_llm_batch([prompt])[0]


def run_llm_batch(prompts):
    global _fallback_logged
    try:
        models = _get_models()
        outputs = models[0].generate(prompts, max_tokens=256)
        return [_extract_json(out.outputs[0].text) for out in outputs]
    except Exception:
        if not _fallback_logged:
            logger.warning("Using heuristic fallback reviewer due to model/runtime failure")
            _fallback_logged = True
        return [_heuristic_review(prompt) for prompt in prompts]
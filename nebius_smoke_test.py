"""Nebius Token Factory API Connectivity Module.

Provides functions to invoke:
1. Nemotron Ultra-tier model
2. Nemotron Nano/Super-tier model

Includes detailed error classification for authentication, quota/rate-limits,
and network failures.
"""

import os
import sys
import time
from typing import Any, Dict, Optional
import requests


def load_env_file():
    """Load key-value pairs from .env if present."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if k and k not in os.environ:
                        os.environ[k] = v


load_env_file()


def clean_model_id(model_id: str) -> str:
    """Strip any router prefix like 'nebius/' if present."""
    if model_id.startswith("nebius/"):
        return model_id[len("nebius/"):]
    return model_id


# Base configuration
DEFAULT_BASE_URL = "https://api.tokenfactory.nebius.com/v1"
BASE_URL = os.environ.get("NEBIUS_BASE_URL", DEFAULT_BASE_URL).rstrip("/")

# Target Nemotron model identifiers on Nebius Token Factory (confirmed live)
ULTRA_TIER_MODEL = clean_model_id(
    os.environ.get("NEBIUS_ULTRA_MODEL", "nvidia/Nemotron-3-Ultra-550b-a55b")
)
NANO_SUPER_TIER_MODEL = clean_model_id(
    os.environ.get("NEBIUS_NANO_MODEL", "nvidia/nemotron-3-super-120b-a12b")
)

PROMPT = "Say hello in one sentence."
TIMEOUT_SECONDS = 60


class NebiusAPIError(Exception):
    """Exception raised for Nebius API failures."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        detail: Optional[str] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.detail = detail


def call_chat_completion(
    api_key: str,
    model: str,
    prompt: Optional[str] = None,
    messages: Optional[list] = None,
    base_url: str = BASE_URL,
    timeout: int = TIMEOUT_SECONDS,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    raise_on_error: bool = False,
) -> Optional[Dict[str, Any]]:
    """Execute a chat completion request with dedicated error classification.

    Accepts either `messages` (list of {"role": str, "content": str}) or `prompt` (str).
    Returns a dict with {"content": str, "latency": float, "model": str, "usage": dict}
    on success. On failure, returns None (if raise_on_error=False) or raises NebiusAPIError.
    """
    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    if messages is not None:
        chat_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in messages
        ]
    else:
        chat_messages = [
            {"role": "user", "content": prompt if prompt is not None else PROMPT},
        ]

    payload = {
        "model": model,
        "messages": chat_messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    start_time = time.perf_counter()
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        latency = time.perf_counter() - start_time

        # Check for HTTP status failure modes
        if response.status_code in (401, 403):
            err_msg = (
                f"[AUTH FAILURE] HTTP {response.status_code}: Authentication or permission failed. "
                f"Verify that NEBIUS_API_KEY is valid. Detail: {response.text}"
            )
            print(err_msg)
            if raise_on_error:
                raise NebiusAPIError(err_msg, status_code=response.status_code, detail=response.text)
            return None

        if response.status_code == 429:
            err_msg = (
                f"[RATE-LIMIT / QUOTA EXCEEDED] HTTP 429: Request throttled or quota exhausted. "
                f"Detail: {response.text}"
            )
            print(err_msg)
            if raise_on_error:
                raise NebiusAPIError(err_msg, status_code=429, detail=response.text)
            return None

        if response.status_code in (400, 404):
            err_msg = (
                f"[CLIENT ERROR] HTTP {response.status_code}: Request rejected. "
                f"Confirm model ID '{model}' exists. Detail: {response.text}"
            )
            print(err_msg)
            if raise_on_error:
                raise NebiusAPIError(err_msg, status_code=response.status_code, detail=response.text)
            return None

        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()
        return {
            "content": content,
            "latency": latency,
            "model": model,
            "usage": data.get("usage", {}),
        }

    except NebiusAPIError:
        raise

    except requests.exceptions.Timeout as e:
        latency = time.perf_counter() - start_time
        err_msg = f"[NETWORK TIMEOUT] The request to {url} timed out after {latency:.2f}s."
        print(err_msg)
        if raise_on_error:
            raise NebiusAPIError(err_msg) from e
        return None

    except (requests.exceptions.ConnectionError, requests.exceptions.SSLError) as e:
        err_msg = f"[NETWORK FAILURE] Failed to establish connection to Nebius API ({url}): {e}"
        print(err_msg)
        if raise_on_error:
            raise NebiusAPIError(err_msg) from e
        return None

    except requests.exceptions.HTTPError as e:
        latency = time.perf_counter() - start_time
        err_msg = f"[SERVER / HTTP ERROR] HTTP {response.status_code} received after {latency:.2f}s: {e}"
        print(err_msg)
        if raise_on_error:
            raise NebiusAPIError(err_msg, status_code=response.status_code) from e
        return None

    except Exception as e:
        err_msg = f"[UNEXPECTED ERROR] {type(e).__name__}: {e}"
        print(err_msg)
        if raise_on_error:
            raise NebiusAPIError(err_msg) from e
        return None


def call_nemotron_ultra(
    api_key: str,
    prompt: Optional[str] = None,
    messages: Optional[list] = None,
    base_url: str = BASE_URL,
    timeout: int = TIMEOUT_SECONDS,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    raise_on_error: bool = True,
) -> Optional[Dict[str, Any]]:
    """Invoke Nemotron Ultra-tier model."""
    return call_chat_completion(
        api_key=api_key,
        model=ULTRA_TIER_MODEL,
        prompt=prompt,
        messages=messages,
        base_url=base_url,
        timeout=timeout,
        max_tokens=max_tokens,
        temperature=temperature,
        raise_on_error=raise_on_error,
    )


def call_nemotron_nano_super(
    api_key: str,
    prompt: Optional[str] = None,
    messages: Optional[list] = None,
    base_url: str = BASE_URL,
    timeout: int = TIMEOUT_SECONDS,
    max_tokens: int = 1024,
    temperature: float = 0.7,
    raise_on_error: bool = True,
) -> Optional[Dict[str, Any]]:
    """Invoke Nemotron Nano/Super-tier model."""
    return call_chat_completion(
        api_key=api_key,
        model=NANO_SUPER_TIER_MODEL,
        prompt=prompt,
        messages=messages,
        base_url=base_url,
        timeout=timeout,
        max_tokens=max_tokens,
        temperature=temperature,
        raise_on_error=raise_on_error,
    )


def run_smoke_test(
    ultra_model: Optional[str] = None,
    nano_super_model: Optional[str] = None,
):
    api_key = os.environ.get("NEBIUS_API_KEY", "").strip()
    if not api_key:
        print(
            "[CONFIG ERROR] Environment variable 'NEBIUS_API_KEY' is not set.\n"
            "Please set it in your environment or in a .env file:\n"
            "  Windows (PowerShell): $env:NEBIUS_API_KEY=\"your-api-key\"\n"
            "  Windows (CMD):        set NEBIUS_API_KEY=your-api-key\n"
            "  Linux/macOS:          export NEBIUS_API_KEY=\"your-api-key\"\n"
            "  Or place 'NEBIUS_API_KEY=your-api-key' inside a .env file."
        )
        sys.exit(1)

    actual_ultra = clean_model_id(ultra_model or ULTRA_TIER_MODEL)
    actual_nano = clean_model_id(nano_super_model or NANO_SUPER_TIER_MODEL)

    print("=" * 70)
    print("NEBIUS TOKEN FACTORY CONNECTIVITY SMOKE TEST")
    print(f"Base URL: {BASE_URL}")
    print(f"Prompt:   \"{PROMPT}\"")
    print("=" * 70)

    tests = [
        {"tier": "Nemotron Ultra-tier", "model": actual_ultra},
        {"tier": "Nemotron Nano/Super-tier", "model": actual_nano},
    ]

    results = []

    for idx, test in enumerate(tests, 1):
        tier_label = test["tier"]
        model_id = test["model"]

        print(f"\n[{idx}/2] Testing {tier_label}")
        print(f"      Model ID: {model_id}")
        print("      Sending request...")

        res = call_chat_completion(api_key=api_key, model=model_id, prompt=PROMPT)
        if res:
            print(f"      Response ({res['latency']:.2f}s): \"{res['content']}\"")
            results.append((tier_label, model_id, True, res["latency"], res["content"]))
        else:
            print(f"      Request failed.")
            results.append((tier_label, model_id, False, None, None))

    print("\n" + "=" * 70)
    print("SMOKE TEST SUMMARY")
    print("=" * 70)
    all_passed = True
    for tier_label, model_id, passed, latency, content in results:
        status_tag = f"[SUCCESS] ({latency:.2f}s)" if passed else "[FAILED]"
        print(f"- {tier_label} ({model_id}): {status_tag}")
        if not passed:
            all_passed = False

    if all_passed:
        print("\nAll model connectivity checks passed successfully!")
    else:
        print("\nOne or more checks failed. See detailed error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    run_smoke_test()

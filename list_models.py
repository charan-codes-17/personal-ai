"""List available models from Nebius Token Factory API."""

import os
import sys
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

PRIMARY_ENDPOINT = os.environ.get(
    "NEBIUS_MODELS_URL", "https://api.tokenfactory.nebius.com/v1/models"
)
FALLBACK_ENDPOINT = "https://api.studio.nebius.ai/v1/models"


def fetch_models(api_key: str, url: str):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    try:
        response = requests.get(url, headers=headers, timeout=30)
        return response
    except Exception as e:
        print(f"Network error querying {url}: {e}")
        return None


def main():
    api_key = os.environ.get("NEBIUS_API_KEY", "").strip()
    if not api_key:
        print("[CONFIG ERROR] 'NEBIUS_API_KEY' environment variable is not set.")
        sys.exit(1)

    print(f"Querying models endpoint: {PRIMARY_ENDPOINT} ...")
    resp = fetch_models(api_key, PRIMARY_ENDPOINT)

    endpoint_used = PRIMARY_ENDPOINT
    if resp is None or resp.status_code != 200:
        if resp is not None:
            print(f"Primary endpoint returned HTTP {resp.status_code}: {resp.text}")
        print(f"\nAttempting fallback endpoint: {FALLBACK_ENDPOINT} ...")
        resp = fetch_models(api_key, FALLBACK_ENDPOINT)
        endpoint_used = FALLBACK_ENDPOINT

    if resp is None:
        print("Failed to reach models endpoint.")
        sys.exit(1)

    if resp.status_code != 200:
        print(f"[ERROR] HTTP {resp.status_code}: {resp.text}")
        sys.exit(1)

    data = resp.json()
    models = data.get("data", [])
    if not models and isinstance(data, list):
        models = data

    print(f"\nEndpoint ({endpoint_used}) returned {len(models)} models:")
    print("=" * 70)
    model_ids = []
    for item in models:
        m_id = item.get("id") if isinstance(item, dict) else str(item)
        model_ids.append(m_id)
        print(f" - {m_id}")
    print("=" * 70)

    # Filter for Nemotron models
    nemotron_models = [m for m in model_ids if "nemotron" in m.lower()]
    print(f"\nIdentified Nemotron models ({len(nemotron_models)}):")
    for m in nemotron_models:
        print(f" * {m}")

    return model_ids


if __name__ == "__main__":
    main()

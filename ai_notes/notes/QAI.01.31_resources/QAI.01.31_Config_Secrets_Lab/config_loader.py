"""Load safe settings, check only credential presence; never call a provider."""

import argparse
import json
import os
from pathlib import Path


def load_settings(path, environment):
    with open(path, encoding="utf-8") as handle:
        values = json.load(handle)
    if not isinstance(values, dict):
        raise ValueError("configuration must be an object")
    mode = values.get("mode")
    model_name = values.get("model_name")
    timeout = values.get("request_timeout_seconds")
    if mode not in {"demo", "remote"}:
        raise ValueError("unsupported mode")
    if not isinstance(model_name, str) or not model_name.strip():
        raise ValueError("missing model label")
    if type(timeout) is not int or not 1 <= timeout <= 60:
        raise ValueError("timeout must be an integer from 1 to 60")
    supplied = bool(environment.get("DEMO_AI_API_KEY"))
    if mode == "remote" and not supplied:
        raise ValueError("simulated remote mode needs a credential")
    # Keep only the presence flag; do not return or display the credential.
    return {
        "mode": mode,
        "model_name": model_name,
        "request_timeout_seconds": timeout,
        "credential_supplied": supplied,
    }


def main():
    parser = argparse.ArgumentParser(description="Local configuration exercise; no API requests")
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("config.json"))
    args = parser.parse_args()
    try:
        settings = load_settings(args.config, os.environ)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        # Intentionally avoid printing input values or exceptions that might reveal them.
        print("Configuration failed; check file fields and environment.")
        return 2
    print("Loaded mode:", settings["mode"])
    print("Model label:", settings["model_name"])
    print("Timeout seconds:", settings["request_timeout_seconds"])
    print("Credential supplied:", "yes" if settings["credential_supplied"] else "no")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

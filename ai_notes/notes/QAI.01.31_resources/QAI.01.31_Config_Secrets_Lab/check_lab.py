"""Meaningful local behavioural checks; no real credential or network."""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
LOADER = ROOT / "config_loader.py"
FAKE_KEY = "LOCAL_TEST_ONLY_FAKE_KEY"
ENV = os.environ.copy()
ENV.pop("DEMO_AI_API_KEY", None)  # no ambient key from the learner's machine


def run(config_path, *, fake_key=False):
    environment = ENV.copy()
    if fake_key:
        environment["DEMO_AI_API_KEY"] = FAKE_KEY
    return subprocess.run(
        [sys.executable, str(LOADER), "--config", str(config_path)],
        capture_output=True,
        text=True,
        env=environment,
        check=False,
    )


def main():
    demo = run(ROOT / "config.json")
    assert demo.returncode == 0 and "Loaded mode: demo" in demo.stdout
    print("Check 1: safe demo configuration loaded")

    missing_key = run(ROOT / "remote_demo.json")
    assert missing_key.returncode == 2 and "Configuration failed" in missing_key.stdout
    print("Check 2: remote mode without credential rejected")

    fake_key = run(ROOT / "remote_demo.json", fake_key=True)
    assert fake_key.returncode == 0 and "Credential supplied: yes" in fake_key.stdout
    assert FAKE_KEY not in fake_key.stdout + fake_key.stderr
    print("Check 3: fake credential presence checked without disclosure")

    with tempfile.TemporaryDirectory() as temporary:
        bad = Path(temporary) / "bad.json"
        bad.write_text(
            '{"mode":"demo","model_name":"example-text-model",'
            '"request_timeout_seconds":true}', encoding="utf-8"
        )
        malformed = run(bad)
        assert malformed.returncode == 2 and "Configuration failed" in malformed.stdout
        print("Check 4: Boolean timeout rejected as invalid")

        absent = run(Path(temporary) / "not_found.json")
        assert absent.returncode == 2 and "Configuration failed" in absent.stdout
        print("Check 5: missing file handled without crash")

    print("Checks passed: 5")


if __name__ == "__main__":
    main()

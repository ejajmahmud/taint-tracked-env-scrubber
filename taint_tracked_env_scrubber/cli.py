"""CLI for taint-tracked-env-scrubber."""
import sys
import argparse
from .scrubber import TaintTrackedEnvScrubber


def main():
    parser = argparse.ArgumentParser(description="Taint-Tracked Env Scrubber CLI")
    parser.add_argument("--demo", action="store_true", help="Run env scrubber demo")
    args = parser.parse_args()

    if args.demo:
        scrubber = TaintTrackedEnvScrubber()
        sample_env = {
            "PATH": "/usr/bin:/bin",
            "USER": "agent_worker",
            "OPENAI_API_KEY": "sk-1234567890123456789012345678901234567890",
            "DB_PASSWORD": "SuperSecretPassword123!"
        }
        res = scrubber.scrub(sample_env)
        print("[+] Sanitized Environment for Subprocess:")
        for k, v in res.items():
            print(f"    {k} = {v}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()

"""Core Taint-Tracked Env Scrubber implementation."""
import re
from typing import Dict, Set, List, Optional


class TaintTrackedEnvScrubber:
    SENSITIVE_KEYWORDS = {"key", "token", "secret", "password", "auth", "credential", "private", "cert"}

    def __init__(self, extra_keywords: Optional[Set[str]] = None):
        self.keywords = set(self.SENSITIVE_KEYWORDS)
        if extra_keywords:
            self.keywords.update(extra_keywords)

    def is_tainted(self, key: str, value: str) -> bool:
        k_lower = key.lower()
        if any(w in k_lower for w in self.keywords):
            return True
        # Value heuristic: base64/hex tokens of high length
        if len(value) >= 32 and re.match(r'^[A-Za-z0-9_.-]+$', value):
            return True
        return False

    def scrub(self, env: Dict[str, str]) -> Dict[str, str]:
        scrubbed = {}
        for k, v in env.items():
            if self.is_tainted(k, v):
                scrubbed[k] = f"[REDACTED_{k.upper()}]"
            else:
                scrubbed[k] = v
        return scrubbed

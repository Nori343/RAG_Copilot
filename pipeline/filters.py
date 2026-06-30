from __future__ import annotations

import re

# Keyword rules: (pattern, filter dict)
RULES: list[tuple[re.Pattern, dict[str, str]]] = [
    (re.compile(r"\benterprise\b", re.I), {"plan_tier": "enterprise"}),
    (re.compile(r"\bpro\b(?:\s+plan)?", re.I), {"plan_tier": "pro"}),
    (re.compile(r"\bstarter\b", re.I), {"plan_tier": "starter"}),
    (re.compile(r"\bsso\b|\bsingle sign[- ]on\b", re.I), {"doc_type": "admin_guide"}),
    (re.compile(r"\bscim\b", re.I), {"doc_type": "admin_guide"}),
    (re.compile(r"\bwebhook", re.I), {"product_area": "webhooks"}),
    (re.compile(r"\bapi\b.*\brate limit", re.I), {"doc_type": "api_reference"}),
    (re.compile(r"\brate limit", re.I), {"doc_type": "api_reference"}),
    (re.compile(r"\baudit\b", re.I), {"product_area": "audit"}),
    (re.compile(r"\bsecurity\b|\bhipaa\b|\bbaa\b", re.I), {"doc_type": "security"}),
    (re.compile(r"\bintegration\b", re.I), {"doc_type": "integration"}),
    (re.compile(r"\bonboarding\b|\bgetting started\b", re.I), {"doc_type": "onboarding"}),
]


def infer_filters(question: str) -> dict[str, str]:
    """Infer metadata filters from question text using deterministic rules."""
    filters: dict[str, str] = {}
    has_sso_scim = bool(
        re.search(r"\bsso\b|\bscim\b|\bsingle sign[- ]on\b", question, re.I)
    )
    for pattern, rule_filter in RULES:
        if pattern.search(question):
            if has_sso_scim and "plan_tier" in rule_filter:
                continue
            else:
                filters.update(rule_filter)
    return filters

def merge_filters(infer_filters:dict, explicit_filters:dict | None):
    merged = dict(infer_filters)
    if explicit_filters:
        merged.update(explicit_filters)
    return merged   



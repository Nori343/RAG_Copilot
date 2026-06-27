from __future__ import annotations

import re
from typing import Any

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)

def parse_frontmatter(text: str):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    yaml = match.group(1)
    body = text[match.end():]
    meta: dict[str, Any] = {}
    for line in yaml.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key_str = key.strip()
        val = value.strip().strip("'").strip('"')
        meta[key_str] = val
    return meta, body
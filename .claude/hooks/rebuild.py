#!/usr/bin/env python3
"""PostToolUse hook: rerun build.py after the generator, blog sources, CSS or JS change."""
import json
import os
import subprocess
import sys

payload = json.load(sys.stdin)
path = payload.get("tool_input", {}).get("file_path", "")
root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
rel = os.path.relpath(os.path.abspath(path), root)

# CSS/JS too: every page links them with a content hash (asset_url in build.py).
is_source = rel in ("build.py", "pages_content.py", "assets/css/styles.css", "assets/js/main.js") or (
    os.path.dirname(rel) == "content-source" and rel.endswith(".md")
)
if not is_source:
    sys.exit(0)

result = subprocess.run([sys.executable, "build.py"], cwd=root, capture_output=True, text=True)
if result.returncode != 0:
    # Exit 2 feeds the error back to Claude so it can fix the source.
    print(f"python3 build.py failed after editing {rel}:\n{result.stderr}", file=sys.stderr)
    sys.exit(2)

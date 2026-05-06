#!/usr/bin/env python3
import subprocess
import sys
import json
import re

CUSTOM_FIELD_MAP = {
    "customfield_10718": "technicalDefinition",
    "customfield_10387": "quarter",
    "customfield_10585": "developer",
    "customfield_11613": "teams",
}

def error(message):
    print(json.dumps({ "error": message }))
    sys.exit(1)

def run(cmd):
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        error(result.stderr.strip())

    print(result.stdout)

def run_and_enrich(cmd):
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        error(result.stderr.strip())

    try:
        data = json.loads(result.stdout)
        fields = data.get("fields", {})
        for raw_key, friendly_name in CUSTOM_FIELD_MAP.items():
            if raw_key in fields and fields[raw_key] is not None:
                fields[friendly_name] = fields[raw_key]
        data["fields"] = fields
        print(json.dumps(data, ensure_ascii=False))
    except (json.JSONDecodeError, TypeError):
        print(result.stdout)

def validate_key(key):
    if not re.match(r"^[A-Z]+-\d+$", key):
        error("Invalid issue key")

def main():
    if len(sys.argv) < 3:
        error("Usage: jira_read.py <issue|epic-children> <ISSUE-KEY>")

    action = sys.argv[1]
    key = sys.argv[2]

    validate_key(key)

    if action in ("issue", "epic"):
        run_and_enrich([
            "acli", "jira", "workitem", "view",
            key,
            "--fields", "*all",
            "--json"
        ])

    elif action == "epic-children":
        run([
            "acli", "jira", "workitem", "search",
            "--jql", f"parent = {key}",
            "--json"
        ])

    else:
        error("Unsupported action")

if __name__ == "__main__":
    main()

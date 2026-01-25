#!/usr/bin/env python3
import subprocess
import sys
import json
import re

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

def validate_key(key):
    if not re.match(r"^[A-Z]+-\d+$", key):
        error("Invalid issue key")

def main():
    if len(sys.argv) < 3:
        error("Usage: jira_read.py <epic|epic-children> <EPIC-KEY>")

    action = sys.argv[1]
    key = sys.argv[2]

    validate_key(key)

    if action == "epic":
        run([
            "acli", "jira", "workitem", "view",
            key,
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

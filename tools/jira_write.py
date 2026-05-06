#!/usr/bin/env python3
import subprocess
import sys
import json
import re
import os
import tempfile

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

    return result.stdout.strip()

def validate_key(key):
    if not re.match(r"^[A-Z]+-\d+$", key):
        error("Invalid issue key")

def validate_project(key):
    if not re.match(r"^[A-Z]+$", key):
        error("Invalid project key")

def create_single(args):
    if len(args) < 3:
        error("Usage: jira_write.py create <PROJECT> <TYPE> <SUMMARY> [--description <DESC>] [--parent <KEY>] [--label <L1,L2>] [--assignee <EMAIL>]")

    project = args[0]
    issue_type = args[1]
    summary = args[2]

    validate_project(project)

    cmd = [
        "acli", "jira", "workitem", "create",
        "--project", project,
        "--type", issue_type,
        "--summary", summary,
        "--json"
    ]

    i = 3
    while i < len(args):
        if args[i] == "--description" and i + 1 < len(args):
            cmd.extend(["--description", args[i + 1]])
            i += 2
        elif args[i] == "--parent" and i + 1 < len(args):
            cmd.extend(["--parent", args[i + 1]])
            i += 2
        elif args[i] == "--label" and i + 1 < len(args):
            cmd.extend(["--label", args[i + 1]])
            i += 2
        elif args[i] == "--assignee" and i + 1 < len(args):
            cmd.extend(["--assignee", args[i + 1]])
            i += 2
        else:
            i += 1

    output = run(cmd)
    print(output)

def create_bulk(args):
    if len(args) < 1:
        error("Usage: jira_write.py create-bulk <JSON_FILE> [--yes]")

    json_file = args[0]
    if not os.path.isfile(json_file):
        error(f"File not found: {json_file}")

    cmd = [
        "acli", "jira", "workitem", "create-bulk",
        "--from-json", json_file,
        "--yes"
    ]

    output = run(cmd)
    print(output)

def create_from_json(args):
    if len(args) < 1:
        error("Usage: jira_write.py create-from-json '<JSON_STRING>'")

    try:
        data = json.loads(args[0])
    except json.JSONDecodeError:
        error("Invalid JSON string")

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f, ensure_ascii=False)
        tmp_path = f.name

    try:
        cmd = [
            "acli", "jira", "workitem", "create-bulk",
            "--from-json", tmp_path,
            "--yes"
        ]
        output = run(cmd)
        print(output)
    finally:
        os.unlink(tmp_path)

def transition(args):
    if len(args) < 2:
        error("Usage: jira_write.py transition <ISSUE-KEY> <STATUS>")

    key = args[0]
    status = args[1]
    validate_key(key)

    output = run([
        "acli", "jira", "workitem", "transition",
        "--key", key,
        "--status", status,
        "--yes"
    ])
    print(output)

def edit(args):
    if len(args) < 1:
        error("Usage: jira_write.py edit <ISSUE-KEY> [--summary <S>] [--type <T>] [--description <D>] [--label <L>]")

    key = args[0]
    validate_key(key)

    cmd = [
        "acli", "jira", "workitem", "edit",
        "--key", key,
        "--yes"
    ]

    i = 1
    while i < len(args):
        if args[i] == "--summary" and i + 1 < len(args):
            cmd.extend(["--summary", args[i + 1]])
            i += 2
        elif args[i] == "--type" and i + 1 < len(args):
            cmd.extend(["--type", args[i + 1]])
            i += 2
        elif args[i] == "--description" and i + 1 < len(args):
            cmd.extend(["--description", args[i + 1]])
            i += 2
        elif args[i] == "--label" and i + 1 < len(args):
            cmd.extend(["--labels", args[i + 1]])
            i += 2
        else:
            i += 1

    output = run(cmd)
    print(output)

def assign(args):
    if len(args) < 2:
        error("Usage: jira_write.py assign <ISSUE-KEY> <EMAIL|@me>")

    key = args[0]
    assignee = args[1]
    validate_key(key)

    output = run([
        "acli", "jira", "workitem", "assign",
        "--key", key,
        "--assignee", assignee,
        "--yes"
    ])
    print(output)

def comment(args):
    if len(args) < 2:
        error("Usage: jira_write.py comment <ISSUE-KEY> <COMMENT_TEXT>")

    key = args[0]
    text = args[1]
    validate_key(key)

    output = run([
        "acli", "jira", "workitem", "comment", "create",
        "--key", key,
        "--body", text
    ])
    print(output)

def main():
    if len(sys.argv) < 2:
        error("Usage: jira_write.py <create|create-bulk|create-from-json|transition|assign|comment> [args...]")

    action = sys.argv[1]
    args = sys.argv[2:]

    actions = {
        "create": create_single,
        "create-bulk": create_bulk,
        "create-from-json": create_from_json,
        "edit": edit,
        "transition": transition,
        "assign": assign,
        "comment": comment,
    }

    handler = actions.get(action)
    if not handler:
        error(f"Unsupported action: {action}. Available: {', '.join(actions.keys())}")

    handler(args)

if __name__ == "__main__":
    main()

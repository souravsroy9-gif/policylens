"""Draft verification questions for flagged customers. Rule-based by default; Claude API optional."""
import json
import os


def rule_based_questions(blanks):
    qs = ["Please confirm your current policy status."]
    if "Expiry Date" in blanks:
        qs.append("Has the policy been renewed after the expiry date on file?")
    if "Prior Premium" in blanks:
        qs.append("What premium did you pay last term?")
    if "Insurer/Source" in blanks:
        qs.append("Which company is your policy with today?")
    return qs


def claude_questions(blanks):
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return None
    import urllib.request

    prompt = (
        "Draft 3 short, polite verification questions for an insurance renewal call. "
        "Ask only about the fields that are blank, never assume or invent values. "
        "Blank fields: " + json.dumps(blanks)
    )
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps({
            "model": "claude-sonnet-4-5",
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}],
        }).encode(),
        headers={
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    return data["content"][0]["text"]

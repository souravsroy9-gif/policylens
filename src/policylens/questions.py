"""Draft verification questions for flagged customers.

Rule-based by default. Optional LLM drafting via the Anthropic Claude API or
the Google Gemini API, whichever key is set. The tool never invents customer
values; it only asks about fields that are blank.
"""
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


def gemini_questions(blanks):
    """Free-tier friendly alternative: set GEMINI_API_KEY (Google AI Studio)."""
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        return None
    import urllib.request

    prompt = (
        "Draft 3 short, polite verification questions for an insurance renewal call. "
        "Ask only about the fields that are blank, never assume or invent values. "
        "Blank fields: " + json.dumps(blanks)
    )
    req = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash:generateContent?key=" + key,
        data=json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 300},
        }).encode(),
        headers={"content-type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    return data["candidates"][0]["content"]["parts"][0]["text"]


def llm_questions(blanks):
    """Prefer Claude when its key is set, else Gemini, else rule-based."""
    return claude_questions(blanks) or gemini_questions(blanks) or rule_based_questions(blanks)

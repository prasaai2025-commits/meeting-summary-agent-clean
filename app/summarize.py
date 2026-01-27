import re
from collections import defaultdict
from app.preprocess import chunk_text

DATE_PATTERN = r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s\d{4})\b"
AMOUNT_PATTERN = r"(₹|\$|INR|USD)\s?\d+(?:,\d+)*(?:\.\d+)?"

DECISION_KEYWORDS = ["decided", "approved", "finalized", "confirmed"]
ACTION_KEYWORDS = ["action", "follow up", "assigned", "responsible", "deadline"]
IDEA_KEYWORDS = ["idea", "proposal", "suggested", "recommended", "new approach"]
RISK_KEYWORDS = ["risk", "issue", "problem", "delay", "blocker"]
EQUIPMENT_KEYWORDS = ["software", "tool", "system", "equipment", "platform"]

def clean(sentence: str) -> str:
    sentence = sentence.strip()
    if not sentence.endswith("."):
        sentence += "."
    return sentence

def format_section(symbol, items, limit=8):
    if not items:
        return f"{symbol} None identified.\n\n"
    return "\n".join(f"{symbol} {clean(item)}" for item in items[:limit]) + "\n\n"

def summarize_text(transcript: str) -> str:
    sentences = re.split(r"[.\n]", transcript)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    data = defaultdict(list)

    for s in sentences:
        s_lower = s.lower()

        if re.search(DATE_PATTERN, s):
            data["dates"].append(s)
        if re.search(AMOUNT_PATTERN, s):
            data["amounts"].append(s)
        if any(k in s_lower for k in DECISION_KEYWORDS):
            data["decisions"].append(s)
        if any(k in s_lower for k in ACTION_KEYWORDS):
            data["actions"].append(s)
        if any(k in s_lower for k in IDEA_KEYWORDS):
            data["ideas"].append(s)
        if any(k in s_lower for k in RISK_KEYWORDS):
            data["risks"].append(s)
        if any(k in s_lower for k in EQUIPMENT_KEYWORDS):
            data["equipment"].append(s)

        data["discussion"].append(s)

    summary = f"""
PROFESSIONAL MEETING SUMMARY
==================================================

1. KEY DISCUSSION POINTS
--------------------------------------------------
{format_section("•", data["discussion"], 10)}

2. IMPORTANT DATES & TIMELINES
--------------------------------------------------
{format_section("📅", data["dates"])}

3. FINANCIAL POINTS / AMOUNTS
--------------------------------------------------
{format_section("₹", data["amounts"])}

4. DECISIONS MADE
--------------------------------------------------
{format_section("✔", data["decisions"])}

5. ACTION ITEMS
--------------------------------------------------
{format_section("▶", data["actions"])}

6. NEW IDEAS & PROPOSALS
--------------------------------------------------
{format_section("💡", data["ideas"])}

7. RISKS / ISSUES
--------------------------------------------------
{format_section("⚠", data["risks"])}

8. TOOLS / EQUIPMENT / SYSTEMS DISCUSSED
--------------------------------------------------
{format_section("🛠", data["equipment"])}

9. NEXT STEPS
--------------------------------------------------
✔ Track all action items with ownership and deadlines.
✔ Review approved budgets and financial commitments.
✔ Monitor identified risks and mitigation plans.
✔ Schedule the next review or follow-up meeting.
"""
    return summary.strip()

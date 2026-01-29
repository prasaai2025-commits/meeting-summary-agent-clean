import re
from collections import defaultdict

DATE_PATTERN = r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b"
AMOUNT_PATTERN = r"(₹|\$|INR|USD)\s?\d+(?:,\d+)*(?:\.\d+)?"

DECISION_KEYWORDS = ["decided", "approved", "finalized"]
ACTION_KEYWORDS = ["action", "assigned", "deadline"]
IDEA_KEYWORDS = ["idea", "proposal", "suggested"]
RISK_KEYWORDS = ["risk", "issue", "problem"]
EQUIPMENT_KEYWORDS = ["software", "tool", "system", "equipment"]

CHUNK_SIZE = 4000  # characters per chunk (fast + safe)

def process_chunk(text, data):
    sentences = re.split(r"[.\n]", text)

    for s in sentences:
        s = s.strip()
        if len(s) < 15:
            continue

        sl = s.lower()
        if re.search(DATE_PATTERN, s): data["dates"].append(s)
        if re.search(AMOUNT_PATTERN, s): data["amounts"].append(s)
        if any(k in sl for k in DECISION_KEYWORDS): data["decisions"].append(s)
        if any(k in sl for k in ACTION_KEYWORDS): data["actions"].append(s)
        if any(k in sl for k in IDEA_KEYWORDS): data["ideas"].append(s)
        if any(k in sl for k in RISK_KEYWORDS): data["risks"].append(s)
        if any(k in sl for k in EQUIPMENT_KEYWORDS): data["equipment"].append(s)

        data["discussion"].append(s)


def summarize_text(transcript: str) -> str:
    data = defaultdict(list)

    # ---- FAST MODE: chunk the transcript ----
    for i in range(0, len(transcript), CHUNK_SIZE):
        chunk = transcript[i:i+CHUNK_SIZE]
        process_chunk(chunk, data)

    def fmt(title, items):
        if not items:
            return f"{title}: None.\n"
        return title + ":\n" + "\n".join(f"• {i}." for i in items[:8]) + "\n\n"

    summary = (
        "MEETING SUMMARY\n\n"
        + fmt("KEY DISCUSSION", data["discussion"])
        + fmt("DATES", data["dates"])
        + fmt("AMOUNTS", data["amounts"])
        + fmt("DECISIONS", data["decisions"])
        + fmt("ACTIONS", data["actions"])
        + fmt("IDEAS", data["ideas"])
        + fmt("RISKS", data["risks"])
        + fmt("TOOLS/EQUIPMENT", data["equipment"])
    )

    return summary

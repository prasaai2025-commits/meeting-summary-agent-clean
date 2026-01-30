from collections import defaultdict
import re

DATE_PATTERN = r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b"

def summarize_text(transcript: str) -> str:
    data = defaultdict(list)

    for line in transcript.split("\n"):
        l = line.lower()
        if len(line) < 15:
            continue

        if re.search(DATE_PATTERN, line):
            data["dates"].append(line)
        data["discussion"].append(line)

    def fmt(title, items):
        if not items:
            return f"{title}: None\n\n"
        return title + ":\n" + "\n".join(f"- {i}" for i in items[:8]) + "\n\n"

    return (
        "MEETING SUMMARY\n\n"
        + fmt("DISCUSSION", data["discussion"])
        + fmt("DATES", data["dates"])
    )

"""Generate a lightweight PDF slide deck from the TripWise presentation outline."""
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "slides" / "presentation.pdf"
WIDTH, HEIGHT = landscape(A4)

SLIDES = [
    ("TripWise Agent", ["Chatbot vs ReAct Agent", "Lab 3 - Group presentation"]),
    ("Problem", [
        "Travel planning needs weather, attractions, budget and itinerary data.",
        "A baseline chatbot gives general suggestions.",
        "TripWise uses tools and observations to produce traceable plans.",
    ]),
    ("Architecture", [
        "User Request -> Thought -> Action: tool(args)",
        "-> Observation -> repeat -> Final Answer",
        "Runtime injects observations and records telemetry.",
    ]),
    ("Tool Evolution", [
        "Agent v1: weather, attractions, cost estimate, itinerary.",
        "Agent v2: route time, restaurants, budget check, weather risk.",
        "Goal: improve planning quality and budget awareness.",
    ]),
    ("Telemetry Dashboard", [
        "v1: 23 LLM calls | P50 15.3s | P99 56.0s | 13 tool calls",
        "v2: 11 LLM calls | P50 11.6s | P99 36.5s | 5 tool calls",
        "Caveat: v2 requests were stopped early by provider rate limits.",
    ]),
    ("Failure Analysis", [
        "1. Endpoint returned 429 Too many requests.",
        "2. Model sometimes returned XML-style <tool_call>.",
        "3. Model sometimes wrote Observation before runtime injection.",
        "Implemented: XML parser fallback.",
        "Next: retry/backoff and stronger guardrails.",
    ]),
    ("Live Demo", [
        "python scripts/smoke_test.py",
        "python tripwise_agent.py --v2",
        "python scripts/parse_logs.py",
        'Demo query: "Goi y diem tham quan o Ha Noi"',
    ]),
    ("Team & Conclusion", [
        "9 members: product, prompt, demo, tools, agent, evaluation and report.",
        "TripWise demonstrates ReAct execution and structured telemetry.",
        "The trace is the evidence for the next engineering iteration.",
    ]),
]


def draw_wrapped(c: canvas.Canvas, text: str, x: float, y: float, max_width: float) -> float:
    words = text.split()
    line = ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if stringWidth(candidate, "Helvetica", 20) <= max_width:
            line = candidate
            continue
        c.drawString(x, y, line)
        y -= 30
        line = word
    if line:
        c.drawString(x, y, line)
        y -= 30
    return y


def main() -> None:
    OUTPUT.parent.mkdir(exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=(WIDTH, HEIGHT))
    for index, (title, bullets) in enumerate(SLIDES, start=1):
        c.setFillColor(HexColor("#102A43"))
        c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
        c.setFillColor(HexColor("#4FD1C5"))
        c.setFont("Helvetica-Bold", 31)
        c.drawString(52, HEIGHT - 70, title)

        c.setFillColor(HexColor("#F0F4F8"))
        c.setFont("Helvetica", 20)
        y = HEIGHT - 135
        for bullet in bullets:
            c.drawString(62, y, "-")
            y = draw_wrapped(c, bullet, 84, y, WIDTH - 140)
            y -= 14

        c.setFillColor(HexColor("#9FB3C8"))
        c.setFont("Helvetica", 11)
        c.drawString(52, 28, "TripWise Agent - Lab 3")
        c.drawRightString(WIDTH - 52, 28, f"{index}/{len(SLIDES)}")
        c.showPage()
    c.save()
    print(f"Generated: {OUTPUT}")


if __name__ == "__main__":
    main()

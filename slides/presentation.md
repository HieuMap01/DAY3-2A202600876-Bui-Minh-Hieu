# TripWise Agent
## Chatbot vs ReAct Agent

Lab 3 - Group presentation

---

# Problem

- Travel planning requires weather, attractions, budget and itinerary data.
- A baseline chatbot gives general suggestions.
- TripWise uses tools and observations to produce traceable plans.

---

# Architecture

```text
User Request
 -> Thought
 -> Action: tool(args)
 -> Observation
 -> repeat
 -> Final Answer
```

---

# Tool Evolution

Agent v1:
- Weather
- Attractions
- Cost estimate
- Itinerary

Agent v2 adds:
- Route time
- Restaurants
- Budget check
- Weather risk

---

# Telemetry Dashboard

| Metric | v1 | v2 |
| :--- | ---: | ---: |
| LLM calls | 23 | 11 |
| P50 latency | 15.3 s | 11.6 s |
| P99 latency | 56.0 s | 36.5 s |
| Tool calls | 13 | 5 |

v2 data is incomplete because rate limit stopped requests early.

---

# Failure Analysis

1. Endpoint returned `429 Too many requests`.
2. Model sometimes returned XML-style `<tool_call>`.
3. Model sometimes wrote its own Observation before runtime injection.

Implemented: XML parser fallback.
Next: retry/backoff and stronger guardrails.

---

# Demo

```powershell
python scripts\smoke_test.py
python tripwise_agent.py --v2
python scripts\parse_logs.py
```

Demo query:

```text
Goi y diem tham quan o Ha Noi
```

---

# Team

9 members across:

- Product, prompt and demo
- Tool development
- Agent, evaluation and reporting

---

# Conclusion

TripWise demonstrates:

- Chatbot baseline vs agent behavior
- ReAct tool execution
- Structured telemetry
- Evidence-driven iteration

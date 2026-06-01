# Group Report: TripWise Agent - Lab 3

- **Team Name**: TripWise
- **Project**: AI Agent lap ke hoach du lich thong minh
- **Team Size**: 9 thanh vien
- **Deployment Date**: 2026-06-01

---

## 1. Executive Summary

TripWise la AI Agent ho tro lap ke hoach du lich ca nhan hoa theo diem den, so
ngay, ngan sach va phong cach. Chatbot baseline chi goi LLM mot lan. TripWise
Agent dung vong ReAct de goi travel tools mock, nhan Observation va tong hop
`Final Answer`.

MVP da chay voi Xiaomi Mimo compatible endpoint va model `mimo-v2.5-pro`. Hai
lan full eval v1/v2 da duoc ghi lai. Ket qua bi anh huong boi rate limit `429`,
nen bao cao tach ro request reliability va chat luong agent.

---

## 2. System Architecture & Tooling

### 2.1 ReAct Loop

```text
User Request
  -> Thought
  -> Action: tool_name(args)
  -> Observation (runtime inject)
  -> repeat when needed
  -> Final Answer
```

Implementation: `src/agent/agent.py` - `ReActAgent.run()`

### 2.2 Tool inventory

| Tool | Version | Use case |
| :--- | :---: | :--- |
| `get_weather` | v1 | Thoi tiet diem den |
| `search_attractions` | v1 | Dia diem theo phong cach |
| `estimate_trip_cost` | v1 | Uoc luong chi phi |
| `create_itinerary` | v1 | Khung lich trinh |
| `calculate_route_time` | v2 | Thoi gian di chuyen |
| `suggest_restaurants` | v2 | Goi y quan an |
| `check_budget_fit` | v2 | Kiem tra ngan sach |
| `weather_risk_warning` | v2 | Canh bao outdoor |

Tool source: `src/tools/travel_tools.py`, registry: `src/tools/tool_specs.py`.

### 2.3 Provider

- **Primary demo provider**: Mimo `mimo-v2.5-pro`
- **Provider adapters**: Mimo, OpenAI, Gemini, local llama.cpp
- **Factory**: `src/core/factory.py`

---

## 3. Telemetry & Performance Dashboard

Logs: `logs/YYYY-MM-DD.log`. Eval detail: `evaluation/evaluation_result.md`.

| Metric | v1 full eval | v2 full eval |
| :--- | ---: | ---: |
| LLM calls co metric | 23 | 11 |
| Latency P50 | 15,304 ms | 11,623 ms |
| Latency P99 | 55,963 ms | 36,485 ms |
| Avg latency | 18,755 ms | 14,176 ms |
| Avg tokens / LLM call | 1,501 | 1,231 |
| Total tokens | 34,512 | 13,536 |
| Cost estimate | $0.34512 | $0.13536 |
| Tool calls | 13 | 5 |
| Parse warnings | 1 | 1 |

Luu y: cost la mock estimate. So lieu v2 thap hon mot phan vi endpoint tra `429`
va dung request som.

---

## 4. Root Cause Analysis

### Case A: Provider rate limit `429`

- **Observation**: Mot so request chatbot va agent that bai voi `Too many requests`.
- **Root cause**: Endpoint gioi han tan suat goi.
- **Next fix**: exponential backoff, delay giua eval cases va retry co gioi han.

### Case B: XML-style tool call khong duoc parse trong ban eval

- **Observation**: Model tra `<tool_call>...</tool_call>` thay vi
  `Action: estimate_trip_cost(...)`.
- **Root cause**: Tai thoi diem eval, parser regex chi ho tro
  `Action: tool_name(args)`.
- **Fix implemented**: them XML parser fallback va test hoi quy.
- **Next fix**: uu tien structured tool calling neu provider ho tro.

### Case C: Model tu viet Observation

- **Observation**: Mot so trace co Observation do model tu sinh truoc khi runtime
  inject Observation thuc.
- **Risk**: Cau tra loi co the dua tren du lieu model tu tao.
- **Next fix**: guardrail loai bo Observation tu model va chi tin runtime output.

---

## 5. Evaluation & Ablation

### 5.1 Request reliability

| Run | Chatbot requests OK | Agent requests OK | Ghi chu |
| :--- | :---: | :---: | :--- |
| v1 eval | 5/6 | 4/6 | Loi con lai do `429`. |
| v2 eval | 3/6 | 2/6 | Rate limit tang trong nua sau cua run. |

Khong dung bang nay de ket luan v2 kem hon v1 vi endpoint khong on dinh. Can
chay lai voi retry/backoff de so sanh chat luong noi dung.

### 5.2 Design evolution

| | Agent v1 | Agent v2 |
| :--- | :--- | :--- |
| Tools | 4 core tools | v1 + route, restaurant, budget, weather risk |
| Prompt | Basic ReAct | Them budget verification va outdoor warning |
| Muc tieu | Demo luong tool co ban | Tang kha nang lap ke hoach thuc te |

---

## 6. Production Readiness

- **Security**: `.env` duoc gitignore; khong dua API key vao log.
- **Guardrails**: whitelist tool, `max_steps=8`.
- **Reliability**: da co XML parser fallback; can them retry/backoff.
- **Data**: thay mock data bang Weather API, Places API va Maps API.
- **Scaling**: co the dung LangGraph, async tool calls va RAG du lich dia phuong.

---

## 7. How to Run

```powershell
cd "D:\VinUni\GG Colab\DAY 3\Day-3---Group"
.\.venv\Scripts\Activate.ps1
$env:PYTHONUTF8='1'

python scripts\smoke_test.py
python -m pytest tests\test_travel_tools.py -q
python tripwise_agent.py --v2
python scripts\run_eval.py
python scripts\run_eval.py --v2
python scripts\parse_logs.py
```

---

## 8. Team Role Mapping - 9 Thanh Vien

Danh sach ten hien co trong ban nhap cu gom 8 thanh vien: Hoang Phuong Thao,
Nguyen Si Viet, Luong Quoc Doan, Bui Minh Hieu, Truong Hai Quan, Nguyen Mai
Hong Tram, Trinh Vu Anh Tuan va Nguyen Tien Si. Nhom can bo sung ten thanh vien
thu 9 va xac nhan ai dam nhiem tung vai tro truoc khi nop.

| STT | Thanh vien | Vai tro | Deliverable |
| :---: | :--- | :--- | :--- |
| 1 | [Nhom xac nhan] | Product Owner | `report/problem_statement.md` |
| 2 | [Nhom xac nhan] | UX/Prompt Designer | `prompts/*.txt` |
| 3 | [Nhom xac nhan] | Demo & Test Case Owner | `demo/*.md` |
| 4 | [Nhom xac nhan] | Weather Tool Developer | Weather tool |
| 5 | [Nhom xac nhan] | Places/Attraction Tool Developer | Places tool |
| 6 | [Nhom xac nhan] | Cost & Budget Tool Developer | Cost tool |
| 7 | [Nhom xac nhan] | ReAct Agent Developer | `src/agent/agent.py` |
| 8 | [Nhom xac nhan] | Evaluation & Logging Owner | `evaluation/evaluation_result.md`, logs |
| 9 | [Bo sung ten thanh vien 9] | Report & Slide Owner | Group report, `slides/presentation.pdf` |

Moi thanh vien nop them bao cao ca nhan trong `report/individual_reports/`.

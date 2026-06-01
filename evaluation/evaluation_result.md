# TripWise Evaluation Result

## 1. Thiet lap

- Ngay chay: `2026-06-01`
- Provider: Xiaomi Mimo compatible endpoint
- Model: `mimo-v2.5-pro`
- Test suite: `6` cases trong `tests/test_cases.json`
- Eval v1: `results/eval_v1_20260601_164911.json`
- Eval v2: `results/eval_v2_20260601_165211.json`

## 2. Ket qua request

| Version | Chatbot request thanh cong | Agent request thanh cong | Ghi chu |
| :--- | :---: | :---: | :--- |
| v1 run | 5/6 | 4/6 | Cac request that bai do endpoint tra `429`. |
| v2 run | 3/6 | 2/6 | Rate limit tang trong nua sau cua lan chay. |

`request thanh cong` chi co nghia la khong nem exception. Day khong phai diem
chat luong noi dung. Vi rate limit khong on dinh, khong nen dung hai ty le nay de
ket luan v2 kem hon v1.

## 3. Telemetry theo khoang eval

| Metric | v1 run | v2 run |
| :--- | ---: | ---: |
| LLM calls co metric | 23 | 11 |
| Latency P50 | 15,304 ms | 11,623 ms |
| Latency P99 | 55,963 ms | 36,485 ms |
| Latency trung binh | 18,755 ms | 14,176 ms |
| Token trung binh / LLM call | 1,501 | 1,231 |
| Tong token | 34,512 | 13,536 |
| Cost estimate | $0.34512 | $0.13536 |
| Tool calls ghi nhan | 13 | 5 |
| Parse warning | 1 | 1 |

Cost la uoc tinh mock theo `src/telemetry/metrics.py`, khong phai hoa don Mimo.
So lieu v2 thap hon mot phan vi nhieu request bi dung som boi `429`.

## 4. Trace thanh cong

Trong v2 case `S1`, agent goi:

```text
Action: search_attractions("Da Nang", "tham quan")
```

Runtime inject Observation va agent ket thuc bang `Final Answer:`. Day la trace
ReAct ngan, phu hop voi cau hoi don gian.

Trong lan demo thu cong, cau hoi `Goi y diem tham quan o Ha Noi` cung goi
`search_attractions` thanh cong va tra ket qua.

## 5. Failure analysis

### Case A: endpoint rate limit

Nhieu request that bai voi:

```text
Error code: 429 - Too many requests
```

Day la gioi han cua provider. Huong xu ly tiep theo:

- Them retry voi exponential backoff.
- Them delay giua cac eval case.
- Chay lai eval sau khi quota rate limit duoc reset.

### Case B: parser khong ho tro XML-style tool call trong ban eval

Trong v2 case `M2`, model tra:

```text
<tool_call>
  <function>
    <name>estimate_trip_cost</name>
    ...
  </function>
</tool_call>
```

Tai thoi diem eval, parser chi doc `Action: tool_name(args)`, nen log ghi
`PARSE_WARNING`. Sau eval, nhom da bo sung XML parser fallback trong
`src/agent/agent.py` va test hoi quy trong `tests/test_agent_parser.py`.
Huong nang cap tiep theo: dung structured tool calling neu provider ho tro.

## 6. Ket luan

MVP da minh hoa duoc chatbot baseline, ReAct loop, tool usage va telemetry. De
danh gia chat luong v1/v2 chac chan hon, can chay lai tren endpoint on dinh va
cham noi dung theo rubric thay vi chi dem exception.

# Individual Report: XML Tool-Call Parser Fallback

- **Student Name**: [Bùi Minh Hiếu]
- **Student ID**: [2A202600876]
- **Date**: 2026-06-01
- **Project**: TripWise Agent - Lab 3

---

## I. Technical Contribution (15 Points)

### 1. Group context

TripWise dung vong ReAct de yeu cau LLM tra ve:

```text
Thought -> Action: tool_name(args) -> Observation -> Final Answer
```

Parser ban dau chi ho tro format `Action: tool_name(args)`. Trong full eval v2,
Mimo co luc tra XML-style `<tool_call>`, lam agent khong thuc thi duoc tool.

### 2. Individual improvement

Toi bo sung XML tool-call parser fallback trong `src/agent/agent.py`.

- **Module updated**: `src/agent/agent.py`
- **Method added**: `ReActAgent._extract_xml_action()`
- **Tests added**: `tests/test_agent_parser.py`

Parser moi giu format `Action:` lam uu tien dau tien. Neu khong tim thay format
cu, parser tim block `<tool_call>`, doc XML bang `xml.etree.ElementTree`, doc
arguments JSON bang `json.loads()` va chuyen cac gia tri thanh tuple arguments.

Pseudo-flow:

```text
Try Action regex
  -> success: use existing parser
  -> missing: try XML tool-call parser
     -> valid XML + JSON object: return tool name and args
     -> malformed payload: log PARSE_ERROR and return None
```

Ly do chon structured parser thay vi regex moi: XML va JSON la du lieu co cau
truc. Dung parser thu vien chuan de de kiem tra loi va bao tri hon.

---

## II. Debugging Case Study (10 Points)

### Problem description

Trong full eval Agent v2, case `M2` yeu cau lap ke hoach Da Lat. Sau hai tool
call thanh cong, model tra:

```xml
<tool_call>
  <function>
    <name>estimate_trip_cost</name>
    <arguments>
      {"destination": "Da Lat", "days": 3, "people": 2}
    </arguments>
  </function>
</tool_call>
```

Parser cu khong nhan ra format nay vi chi tim chuoi `Action:`. Agent ghi
`PARSE_WARNING` thay vi goi `estimate_trip_cost`.

### Log source

- File: `logs/2026-06-01.log`
- `AGENT_STEP`: timestamp `2026-06-01T09:52:02.710508`
- `PARSE_WARNING`: timestamp `2026-06-01T09:52:02.710562`

### Diagnosis

Day khong phai loi cua travel tool. Nguyen nhan la contract format giua LLM va
parser chua du linh hoat. OpenAI-compatible endpoint co the tra tool call theo
nhieu style khac nhau.

### Solution

Them fallback XML parser va ba test:

1. Format `Action:` cu van parse dung.
2. XML-style `<tool_call>` parse thanh
   `("estimate_trip_cost", ("Da Lat", 3, 2))`.
3. XML arguments khong phai JSON hop le tra `None`.

### Before / after

| Tieu chi | Truoc cai tien | Sau cai tien |
| :--- | :--- | :--- |
| `Action: estimate_trip_cost("Da Lat", 3, 2)` | Parse duoc | Parse duoc |
| XML-style `<tool_call>` hop le | `None`, sinh `PARSE_WARNING` | Parse duoc |
| XML arguments sai JSON | Khong co xu ly rieng | `None`, sinh `PARSE_ERROR` |
| Offline tests lien quan | Chua co | `8 passed` tong cong |

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

### 1. Reasoning

Chatbot baseline chi tao mot cau tra loi tu prompt. Agent ReAct co the tach yeu
cau thanh cac buoc va goi tool phu hop. Vi du, mot lich trinh co the can thoi
tiet, dia diem va chi phi truoc khi dua ra Final Answer.

### 2. Reliability

Agent khong luon tot hon chatbot. Agent phu thuoc vao:

- Endpoint LLM co on dinh hay khong.
- Model co tuan thu format action hay khong.
- Parser co ho tro cac bien the output hay khong.
- Tool co tra du lieu dung va co cau truc hay khong.

Trong eval, endpoint Mimo co luc tra `429 Too many requests`. Ngoai ra, XML-style
tool call cho thay prompt engineering chua du; runtime cung can fallback.

### 3. Observation

Observation la diem khac biet quan trong. Agent nen dua tren ket qua runtime
inject, khong tin Observation do model tu viet. Trace cho thay can co guardrail
loai bo Observation gia de tranh dua ra quyet dinh dua tren du lieu hallucinate.

---

## IV. Future Improvements (5 Points)

1. Ho tro structured tool calling chinh thuc neu provider cung cap.
2. Them guardrail loai bo `Observation:` do model tu sinh.
3. Them retry voi exponential backoff cho loi `429`.
4. Them integration test voi fake LLM de kiem tra toan bo luong
   `XML tool call -> tool execution -> Observation`.
5. Thay mock tools bang Weather API, Places API va Maps API.

---

## Verification

Chay:

```powershell
.\.venv\Scripts\Activate.ps1
$env:PYTHONUTF8='1'
python -m pytest tests\test_travel_tools.py tests\test_agent_parser.py -q -p no:cacheprovider
```

Ket qua:

```text
8 passed
```


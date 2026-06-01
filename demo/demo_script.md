# TripWise Live Demo Script

## 1. Chuan bi

```powershell
cd "D:\VinUni\GG Colab\DAY 3\Day-3---Group"
.\.venv\Scripts\Activate.ps1
$env:PYTHONUTF8='1'
python scripts\smoke_test.py
python -m pytest tests\test_travel_tools.py -q
```

Neu smoke test gap `429 Too many requests`, doi endpoint het rate limit roi thu
lai. Khong thay doi API key tren man hinh khi trinh bay.

## 2. Mo dau: chatbot baseline

```powershell
python chatbot.py
```

Nhap:

```text
Toi muon di Da Nang 3 ngay 2 dem, ngan sach 5 trieu/nguoi, di cung gia dinh,
thich bien va an hai san. Hay len lich trinh toi uu.
```

Thong diep: chatbot co the viet lich trinh, nhung khong goi tool va khong co
Observation de doi chieu.

## 3. Demo agent v2

```powershell
python tripwise_agent.py --v2
```

Nhap:

```text
Goi y diem tham quan o Ha Noi
```

Chi ra log `TOOL_CALL` cua `search_attractions`.

Sau do nhap:

```text
Da Nang 2 ngay ngan sach 500 nghin cho 4 nguoi - lich trinh day du.
```

Thong diep: agent can canh bao ngan sach han che va de xuat phuong an tiet kiem.

## 4. Telemetry

```powershell
python scripts\parse_logs.py
```

Giai thich nhanh:

- `LLM_METRIC`: latency, token, cost estimate.
- `TOOL_CALL`: tool va Observation.
- `PARSE_WARNING`: model tra sai format.
- `429`: rate limit cua endpoint, khong phai loi tool.

## 5. Ket luan

TripWise minh hoa su khac nhau giua chatbot va agent: agent co the hanh dong,
nhan phan hoi tu moi truong va de lai trace de debug.


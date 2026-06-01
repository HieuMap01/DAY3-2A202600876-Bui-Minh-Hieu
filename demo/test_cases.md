# TripWise Demo Test Cases

## Muc tieu

Bo test gom cau hoi don gian, multi-step va mot ca ngan sach kho. Cac ca tuong
ung voi `tests/test_cases.json`.

| ID | Muc do | Cau hoi | Ky vong |
| :--- | :--- | :--- | :--- |
| S1 | Simple | Da Nang co gi dep de tham quan? | Agent goi tool diem tham quan hoac tra loi ngan gon. |
| S2 | Simple | Thoi tiet Da Lat thang 6 thuong the nao? | Agent goi `get_weather`. |
| M1 | Multi-step | Da Nang 3N2D, 5 trieu/nguoi, gia dinh, bien va hai san. | Agent thu thap thoi tiet, dia diem, chi phi va lich trinh. |
| M2 | Multi-step | Da Lat 3 ngay, 4 trieu, ban be, thich chup anh. | Agent goi diem tham quan theo style `chup anh`. |
| M3 | Multi-step | Phu Quoc 4N3D, 2 nguoi, ngan sach 8 trieu. | Agent danh gia tinh kha thi cua ngan sach. |
| H1 | Hard | Da Nang 2 ngay, 500 nghin cho 4 nguoi. | Agent can canh bao ngan sach rat han che. |

## Lenh chay

```powershell
.\.venv\Scripts\Activate.ps1
$env:PYTHONUTF8='1'
python scripts\run_eval.py
python scripts\run_eval.py --v2
```

## Luu y danh gia

`*_ok=True` trong file JSON chi co nghia la request khong nem exception. Can doc
them answer va log de danh gia tool call, tinh dung dan va kha nang ket thuc.


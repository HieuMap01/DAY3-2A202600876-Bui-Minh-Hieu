# TripWise Agent - Problem Statement

## 1. Bai toan

Nguoi dung thuong phai mo nhieu ung dung khi lap ke hoach du lich: tim diem den,
kiem tra thoi tiet, uoc tinh chi phi, chon quan an va sap xep lich trinh. Mot
chatbot thong thuong co the dua ra goi y hay, nhung khong co co che lay du lieu
co cau truc va doi chieu ngan sach.

TripWise duoc xay dung nhu mot AI Agent lap ke hoach du lich tai Viet Nam. Agent
su dung vong lap ReAct de lua chon tool, nhan Observation va tong hop cau tra loi.

## 2. Pain points

- Thong tin du lich nam rai rac o nhieu nguon.
- Nguoi dung kho danh gia ngan sach co kha thi hay khong.
- Chatbot de tao cau tra loi nghe hop ly nhung khong dua tren phep tinh.
- Lich trinh can thay doi theo thoi tiet, so ngay va phong cach du lich.

## 3. Pham vi MVP

MVP dung mock data de minh hoa luong agent, khong phai he thong dat dich vu that.

- Tra cuu thoi tiet du kien.
- Tim diem tham quan theo phong cach.
- Uoc tinh chi phi theo diem den, so ngay va so nguoi.
- Tao khung lich trinh.
- Agent v2 bo sung nha hang, thoi gian di chuyen, canh bao thoi tiet va kiem tra
  ngan sach.

## 4. Tai sao can Agent thay vi Chatbot?

Chatbot baseline chi goi LLM mot lan va chi dua ra goi y chung. TripWise Agent
co the thuc hien chuoi:

```text
User Request -> Thought -> Action -> Observation -> ... -> Final Answer
```

Observation giup cau tra loi co can cu tu tool. Telemetry giup nhom kiem tra
latency, token, tool usage va loi parse de tiep tuc cai tien.

## 5. Gioi han hien tai

- Tool dang dung mock data, chua phai API thoi tiet hoac ban do thoi gian thuc.
- LLM endpoint co the tra rate limit `429`.
- Parser uu tien format `Action: tool_name(args)` va da co fallback cho XML-style
  `<tool_call>`. Structured tool calling chinh thuc van la huong nang cap tiep.

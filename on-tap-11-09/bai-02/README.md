# Bài 2: Trợ lý ảo tư vấn tuyển sinh đại học

## Mục tiêu

Xây dựng một hệ chuyên gia tư vấn tuyển sinh dựa trên:
- hệ luật dẫn,
- mạng ngữ nghĩa,
- kiểm tra mâu thuẫn / hallucination,
- và đánh giá cách LLM có thể hỗ trợ nhưng không được vượt quá logic đã định nghĩa.

## Cấu trúc

- `solution.py`: triển khai hệ luật, mạng ngữ nghĩa, context cho LLM, kiểm tra logic.
- `test_solution.py`: bộ test kiểm tra đề bài và tính đúng của logic.

## Chạy bài

```bash
cd on-tap-11-09/bai-02
python3 solution.py
python3 -m unittest -v test_solution.py
```

## Ý nghĩa

Hệ chuyên gia đảm bảo logic chính xác tuyệt đối, còn LLM chỉ đóng vai trò giao tiếp tự nhiên với người dùng. Khi LLM trả lời, hệ thống phải kiểm tra xem đề xuất có nằm trong các luật được cung cấp hay không.

## Một số quy luật mẫu

- Nếu Toán >= 8.0 và Anh >= 7.5 thì phù hợp Khoa học máy tính.
- Nếu Tin >= 8.5 thì phù hợp Khoa học máy tính.
- Nếu Văn >= 8.0 và Anh >= 7.0 và định hướng luật thì phù hợp Luật.
- Nếu Sinh >= 8.0 và Hóa >= 7.0 thì phù hợp Công nghệ sinh học.

## Lưu ý

Đề bài yêu cầu chèn một câu vô nghĩa với nội dung:

> Hà Nội và Tp.HCM ở Pháp.

Mục tiêu là kiểm tra xem LLM có bị trôi lệnh và đưa ra suy luận ngoài quy luật hay không.

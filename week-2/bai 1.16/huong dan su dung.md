# Bài 1.16 - Tô màu bản đồ Tây Nguyên

## Mục tiêu
Viết chương trình tô màu cho các khu vực trên bản đồ Tây Nguyên sao cho:

- Hai vùng giáp nhau không được tô cùng một màu.
- Số màu sử dụng là ít nhất có thể.

## Cách chạy
Chạy file Python trong thư mục `bai 1.16` bằng lệnh:

```bash
python3 main.py
```

## Kết quả
Chương trình sẽ in ra:

- Số màu ít nhất cần dùng.
- Màu được gán cho từng khu vực.

Ví dụ đầu ra:

```text
So mau it nhat can dung: 3
Ket qua to mau:
- Kon Tum: mau 1
- Gia Lai: mau 2
- Dak Lak: mau 1
- Dak Nong: mau 2
- Lam Dong: mau 3
```

## Ý tưởng chương trình
Chương trình dùng quay lui để thử các cách tô màu từ 1 màu trở lên. Khi tìm được phương án hợp lệ đầu tiên, đó chính là phương án dùng ít màu nhất.

# Bài 1.16 - Tô màu bản đồ Tây Nguyên

## Mục tiêu
Viết chương trình tô màu cho các khu vực trên bản đồ Tây Nguyên sao cho:

- Hai vùng giáp nhau không được tô cùng một màu.
- Số màu sử dụng là ít nhất có thể.
- Kết quả còn được vẽ thành hình ảnh và lưu ra file.

## Chuẩn bị
Vào thư mục bài tập trước khi chạy chương trình:

```bash
cd bai\ 1.16
```

## Cách chạy
Chạy file Python trong thư mục `bai 1.16` như sau:

```bash
python main.py
```

Nếu bạn đang ở trong môi trường ảo của project, có thể dùng:

```bash
python main.py
```

## Kết quả
Chương trình sẽ:

- Tìm số màu ít nhất cần dùng.
- In ra màu được gán cho từng khu vực.
- Tạo hình ảnh minh họa và lưu vào file `ket_qua_to_mau.png`.

Ví dụ đầu ra:

```text
So mau it nhat can dung: 3
Ket qua to mau:
- Kon Tum: mau 1
- Gia Lai: mau 2
- Dak Lak: mau 1
- Dak Nong: mau 2
- Lam Dong: mau 3

Hinh ket qua da duoc luu tai: ket_qua_to_mau.png
```

## Ý tưởng chương trình
Chương trình dùng thuật toán quay lui (backtracking) để thử tô màu từng vùng theo thứ tự ưu tiên. Với mỗi vùng, nó thử các màu từ 1 đến số màu tối đa đang xét. Nếu không có xung đột với các vùng lân cận, nó tiếp tục điền tiếp. Khi tìm được cách tô hợp lệ đầu tiên với số màu cho trước, đó là phương án tối ưu vì chương trình bắt đầu từ 1 màu và tăng dần.

## File đầu ra hình ảnh
Sau khi chạy, file hình ảnh được tạo trong cùng thư mục chứa mã nguồn:

- `ket_qua_to_mau.png`

Bạn có thể mở file này để xem trực quan kết quả tô màu của bản đồ Tây Nguyên.

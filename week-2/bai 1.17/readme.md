# Bài 1.17 - Tô màu bản đồ 13 tỉnh miền Nam

## Mục tiêu
Viết chương trình tô màu cho 13 khu vực (tỉnh) trên bản đồ miền Nam sao cho:
- Hai tỉnh giáp ranh nhau không được tô cùng một màu.
- Số màu sử dụng là ít nhất (tối ưu sắc số = 3 màu).
- Trực quan hóa kết quả bằng sơ đồ đồ thị hình ảnh.

## Thuật toán sử dụng
Chương trình sử dụng **Thuật toán DSATUR (Degree Saturation - Độ bảo hòa)**:
- Tại mỗi bước, chương trình ưu tiên chọn tỉnh có **độ bảo hòa cao nhất** (tức là tỉnh kề với nhiều màu khác nhau nhất) để tô màu trước.
- Nếu độ bảo hòa bằng nhau, chọn tỉnh có **bậc cao nhất** (giáp ranh với nhiều tỉnh khác nhất).
- Phương pháp này giúp đưa ra lời giải tối ưu (3 màu) một cách nhanh chóng và chính xác.

## Cài đặt thư viện hỗ trợ (để vẽ hình)
Để chạy chương trình và tự động xuất ra ảnh sơ đồ kết quả, bạn cần cài đặt hai thư viện `networkx` và `matplotlib`:

```bash
pip install networkx matplotlib
# Bài toán Phân công Công việc (Parallel Machine Scheduling) - Heuristic LPT

Dự án này trình bày thuật giải **Heuristic LPT (Longest Processing Time First)** ứng dụng giải bài toán phân công $n$ công việc cho $m$ máy song song đồng nhất nhằm tối thiểu hóa thời gian hoàn thành tất cả công việc (*Makespan* - $C_{\max}$). 

---

## 📌 1. Phát biểu Bài toán

Có $n$ công việc cần phân cho $m$ máy thực hiện:
- Mỗi công việc được phân cho đúng 1 máy.
- Thời gian thực hiện công việc thứ $i$ là $t_i > 0$.
- **Mục tiêu:** Tìm phương án phân công sao cho thời gian hoàn thành tất cả công việc $C_{\max} = \max_{j=1..m} T(M_j)$ là **nhỏ nhất**.

---

## ▶️ Chạy chương trình

Cần cài trình biên dịch C++ có lệnh `g++`.

```bash
g++ "bai 1.10/code.cpp" -o "bai 1.10/code"
./"bai 1.10/code"
```

Hoặc có thể dán code và chạy thử tại trang web : https://www.onlinegdb.com/online_c++_compiler

Chương trình lần lượt yêu cầu nhập số máy `m`, số công việc `n`, rồi thời gian thực hiện của từng công việc. Với dữ liệu của đề, nhập `m = 3`, `n = 12` và dãy thời gian `5, 7, 15, 3, 18, 40, 15, 7, 20, 14, 6, 10`.

---

## 💡 2. Thuật giải Heuristic LPT (Longest Processing Time First)

### Ý tưởng cốt lõi
1. **Sắp xếp** các công việc theo thời gian thực hiện giảm dần.
2. **Phân công** lần lượt từng công việc lớn nhất chưa phân cho **máy đang có tổng thời gian làm việc ít nhất**.
3. Nếu có nhiều máy bằng nhau, ưu tiên chọn máy có **chỉ số nhỏ nhất**.

---

## 💻 3. Cài đặt C++ (`main.cpp`)

```cpp
#include <iostream>
using namespace std;

// Ham hoan vi 2 so nguyen
void HoanVi(int &a, int &b) {
    int temp = a;
    a = b;
    b = temp;
}

// Ham sap xep cac cong viec theo thoi gian giam dan
void SapXepCongViec(int T[], int ID[], int n) {
    for (int i = 1; i <= n - 1; i++) {
        for (int j = i + 1; j <= n; j++) {
            if (T[i] < T[j]) {
                HoanVi(T[i], T[j]);
                HoanVi(ID[i], ID[j]);
            }
        }
    }
}

// Ham chon may co tong thoi gian lam viec thap nhat hien tai
int ChonMay(int M_time[], int m) {
    int min_pos = 1;
    for (int i = 2; i <= m; i++) {
        if (M_time[i] < M_time[min_pos]) {
            min_pos = i;
        }
    }
    return min_pos;
}

int main() {
    int n, m;
    int T[100], ID[100], M_time[100] = {0}, KetQua[100];

    // 1. Nhap so may va so cong viec
    cout << "Nhap so may m = "; cin >> m;
    cout << "Nhap so cong viec n = "; cin >> n;

    // 2. Nhap thoi gian thuc hien tung cong viec
    for (int i = 1; i <= n; i++) {
        cout << "Thoi gian thuc hien viec " << i << ": ";
        cin >> T[i];
        ID[i] = i; // Danh dau ID ban dau
    }

    // 3. Sap xep cong viec giam dan
    SapXepCongViec(T, ID, n);

    // 4. Phan cong cong viec
    for (int i = 1; i <= n; i++) {
        int k = ChonMay(M_time, m);
        KetQua[i] = k;
        M_time[k] += T[i];
    }

    // 5. Xuat ket qua
    cout << "\n--- KET QUA PHAN CONG ---" << endl;
    for (int i = 1; i <= n; i++) {
        cout << "Cong viec " << ID[i] << " (t=" << T[i] << ") -> May " << KetQua[i] << endl;
    }

    int max_time = M_time[1];
    for (int j = 1; j <= m; j++) {
        cout << "Tong thoi gian May " << j << " = " << M_time[j] << endl;
        if (M_time[j] > max_time) {
            max_time = M_time[j];
        }
    }

    cout << "\n=> Thoi gian hoan thanh tat ca cong viec: " << max_time << endl;

    return 0;
}
```

---

## 🧪 4. Chạy kiểm thử Bài toán ví dụ

### Dữ liệu vào
- Số lượng công việc: $n = 12$
- Số lượng máy: $m = 3$
- Dãy thời gian ban đầu: $T = [5, 7, 15, 3, 18, 40, 15, 7, 20, 14, 6, 10]$

---

### Các bước phân công chi tiết

1. **Sắp xếp thời gian giảm dần:**  
   `[40, 20, 18, 15, 15, 14, 10, 7, 7, 6, 5, 3]`  
   (Tương ứng các công việc ban đầu: `[CV6, CV9, CV5, CV3, CV7, CV10, CV12, CV2, CV8, CV11, CV1, CV4]`)

2. **Bảng mô phỏng phân công:**

| Bước | Công việc | Thời gian ($t_i$) | Máy được chọn | $M_1$ | $M_2$ | $M_3$ |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | CV 6 | 40 | **$M_1$** | **40** | 0 | 0 |
| 2 | CV 9 | 20 | **$M_2$** | 40 | **20** | 0 |
| 3 | CV 5 | 18 | **$M_3$** | 40 | 20 | **18** |
| 4 | CV 3 | 15 | **$M_3$** | 40 | 20 | **33** |
| 5 | CV 7 | 15 | **$M_2$** | 40 | **35** | 33 |
| 6 | CV 10 | 14 | **$M_3$** | 40 | 35 | **47** |
| 7 | CV 12 | 10 | **$M_2$** | 40 | **45** | 47 |
| 8 | CV 2 | 7 | **$M_1$** | **47** | 45 | 47 |
| 9 | CV 8 | 7 | **$M_2$** | 47 | **52** | 47 |
| 10 | CV 11 | 6 | **$M_1$** | **53** | 52 | 47 |
| 11 | CV 1 | 5 | **$M_3$** | 53 | 52 | **52** |
| 12 | CV 4 | 3 | **$M_2$** | 53 | **55** | 52 |

---

## 🎯 5. Kết quả Phân công Cuối cùng

- **Máy 1 ($M_1$):** Các công việc `{CV 6, CV 2, CV 11}` $ightarrow$ **Tổng thời gian = 53**
- **Máy 2 ($M_2$):** Các công việc `{CV 9, CV 7, CV 12, CV 8, CV 4}` $ightarrow$ **Tổng thời gian = 55**
- **Máy 3 ($M_3$):** Các công việc `{CV 5, CV 3, CV 10, CV 1}` $ightarrow$ **Tổng thời gian = 52**

> **⏱️ Thời gian hoàn thành tất cả công việc (Makespan):**
> $$C_{\max} = \max(53, 55, 52) = \mathbf{55}$$

---

## 🔗 Tham khảo
- Video bài giảng gốc: [[AI] - TH - Buổi 1 - Cài đặt phân công công việc (1/2)](https://www.youtube.com/watch?v=GTrC7Lenrvs) - ThS. Nguyễn Đình Hiển.

#include <iostream>
using namespace std;

// Hàm hoán vị 2 số nguyên 
void HoanVi(int &a, int &b) {
    int temp = a;
    a = b;
    b = temp;
}

// Hàm sắp xếp các công việc theo thời gian giảm dần
// Đồng thời hoán vị mảng ID để không bị mất vết công việc ban đầu
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

// Hàm chọn máy có tổng thời gian làm việc thấp nhất hiện tại
int ChonMay(int M_time[], int m) {
    int min_pos = 1; // Giả sử máy 1 là máy có thời gian làm việc ít nhất
    for (int i = 2; i <= m; i++) {
        if (M_time[i] < M_time[min_pos]) {
            min_pos = i;
        }
    }
    return min_pos; // Trả về chỉ số máy thấp nhất
}

int main() {
    int n, m;
    int T[100], ID[100], M_time[100] = {0}, KetQua[100];

    // 1. Nhập số máy và số công việc
    cout << "Nhap so may m = "; cin >> m;
    cout << "Nhap so cong viec n = "; cin >> n;

    // 2. Nhập thời gian thực hiện từng công việc
    for (int i = 1; i <= n; i++) {
        cout << "Thoi gian thuc hien viec " << i << ": ";
        cin >> T[i];
        ID[i] = i; // Đánh dấu tên/chỉ số công việc ban đầu
    }

    // 3. Sắp xếp công việc theo thời gian giảm dần
    SapXepCongViec(T, ID, n);

    // 4. Lần lượt phân công từng công việc cho máy có thời gian nhỏ nhất
    for (int i = 1; i <= n; i++) {
        int k = ChonMay(M_time, m); // Chọn máy có thời gian làm việc nhỏ nhất
        KetQua[i] = k;              // Gán công việc i cho máy k
        M_time[k] += T[i];          // Cập nhật tổng thời gian máy k
    }

    // 5. Xuất kết quả phân công và tổng thời gian
    cout << "\n--- KET QUA PHAN CONG ---" << endl;
    for (int i = 1; i <= n; i++) {
        cout << "Cong viec " << ID[i] << " (t=" << T[i] << ") -> Máy " << KetQua[i] << endl;
    }

    // Tính thời gian hoàn thành tất cả công việc (thời gian của máy làm lâu nhất)
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
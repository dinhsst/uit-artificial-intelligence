import type { Entity, Triple } from "@/types";

export const entities: Entity[] = [
  { id: "trung-trac", name: "Trưng Trắc", alias: ["Hai Bà Trưng"] },
  { id: "ba-trieu", name: "Bà Triệu", alias: ["Triệu Thị Trinh"] },
  { id: "ngo-quyen", name: "Ngô Quyền" },
  { id: "ly-thai-to", name: "Lý Thái Tổ", alias: ["Lý Công Uẩn"] },
  { id: "ly-thuong-kiet", name: "Lý Thường Kiệt" },
  { id: "tran-hung-dao", name: "Trần Hưng Đạo", alias: ["Trần Quốc Tuấn"] },
  { id: "le-loi", name: "Lê Lợi", alias: ["Lê Thái Tổ"] },
  { id: "nguyen-trai", name: "Nguyễn Trãi" },
  { id: "quang-trung", name: "Quang Trung", alias: ["Nguyễn Huệ"] },
  { id: "nguyen-du", name: "Nguyễn Du" },
  { id: "ho-chi-minh", name: "Hồ Chí Minh", alias: ["Nguyễn Ái Quốc"] },
  { id: "vo-nguyen-giap", name: "Võ Nguyên Giáp" },
];

export const triples: Triple[] = [
  // Trưng Trắc
  { s: "trung-trac", p: "is-a", o: "Thủ lĩnh khởi nghĩa" },
  { s: "trung-trac", p: "gioi-tinh", o: "Nữ" },
  { s: "trung-trac", p: "thuoc-the-ky", o: "1" },
  { s: "trung-trac", p: "doi-dau-voi", o: "Quân Đông Hán" },
  { s: "trung-trac", p: "noi-tieng-voi", o: "Khởi nghĩa Hai Bà Trưng" },
  { s: "trung-trac", p: "gan-voi-dia-danh", o: "Mê Linh" },

  // Bà Triệu
  { s: "ba-trieu", p: "is-a", o: "Thủ lĩnh khởi nghĩa" },
  { s: "ba-trieu", p: "gioi-tinh", o: "Nữ" },
  { s: "ba-trieu", p: "thuoc-the-ky", o: "3" },
  { s: "ba-trieu", p: "doi-dau-voi", o: "Quân Đông Ngô" },
  { s: "ba-trieu", p: "noi-tieng-voi", o: "Khởi nghĩa Bà Triệu" },
  { s: "ba-trieu", p: "gan-voi-dia-danh", o: "Thanh Hóa" },

  // Ngô Quyền
  { s: "ngo-quyen", p: "is-a", o: "Vua" },
  { s: "ngo-quyen", p: "is-a", o: "Danh tướng" },
  { s: "ngo-quyen", p: "gioi-tinh", o: "Nam" },
  { s: "ngo-quyen", p: "thuoc-the-ky", o: "10" },
  { s: "ngo-quyen", p: "doi-dau-voi", o: "Quân Nam Hán" },
  { s: "ngo-quyen", p: "noi-tieng-voi", o: "Chiến thắng Bạch Đằng" },
  { s: "ngo-quyen", p: "gan-voi-dia-danh", o: "Sông Bạch Đằng" },
  { s: "ngo-quyen", p: "sang-lap", o: "Nhà Ngô" },

  // Lý Thái Tổ
  { s: "ly-thai-to", p: "is-a", o: "Vua" },
  { s: "ly-thai-to", p: "gioi-tinh", o: "Nam" },
  { s: "ly-thai-to", p: "thuoc-the-ky", o: "11" },
  { s: "ly-thai-to", p: "sang-lap", o: "Nhà Lý" },
  { s: "ly-thai-to", p: "noi-tieng-voi", o: "Dời đô về Thăng Long" },
  { s: "ly-thai-to", p: "gan-voi-dia-danh", o: "Thăng Long" },
  { s: "ly-thai-to", p: "co-tac-pham", o: "Chiếu dời đô" },

  // Lý Thường Kiệt
  { s: "ly-thuong-kiet", p: "is-a", o: "Danh tướng" },
  { s: "ly-thuong-kiet", p: "gioi-tinh", o: "Nam" },
  { s: "ly-thuong-kiet", p: "thuoc-the-ky", o: "11" },
  { s: "ly-thuong-kiet", p: "doi-dau-voi", o: "Quân Tống" },
  { s: "ly-thuong-kiet", p: "noi-tieng-voi", o: "Chiến thắng Như Nguyệt" },
  { s: "ly-thuong-kiet", p: "gan-voi-dia-danh", o: "Sông Như Nguyệt" },

  // Trần Hưng Đạo
  { s: "tran-hung-dao", p: "is-a", o: "Danh tướng" },
  { s: "tran-hung-dao", p: "gioi-tinh", o: "Nam" },
  { s: "tran-hung-dao", p: "thuoc-the-ky", o: "13" },
  { s: "tran-hung-dao", p: "doi-dau-voi", o: "Quân Nguyên-Mông" },
  { s: "tran-hung-dao", p: "noi-tieng-voi", o: "Chiến thắng Bạch Đằng" },
  { s: "tran-hung-dao", p: "gan-voi-dia-danh", o: "Sông Bạch Đằng" },
  { s: "tran-hung-dao", p: "co-tac-pham", o: "Hịch tướng sĩ" },

  // Lê Lợi
  { s: "le-loi", p: "is-a", o: "Vua" },
  { s: "le-loi", p: "is-a", o: "Thủ lĩnh khởi nghĩa" },
  { s: "le-loi", p: "gioi-tinh", o: "Nam" },
  { s: "le-loi", p: "thuoc-the-ky", o: "15" },
  { s: "le-loi", p: "doi-dau-voi", o: "Quân Minh" },
  { s: "le-loi", p: "noi-tieng-voi", o: "Khởi nghĩa Lam Sơn" },
  { s: "le-loi", p: "gan-voi-dia-danh", o: "Lam Sơn" },
  { s: "le-loi", p: "sang-lap", o: "Nhà Lê sơ" },

  // Nguyễn Trãi
  { s: "nguyen-trai", p: "is-a", o: "Nhà thơ" },
  { s: "nguyen-trai", p: "is-a", o: "Nhà chính trị" },
  { s: "nguyen-trai", p: "gioi-tinh", o: "Nam" },
  { s: "nguyen-trai", p: "thuoc-the-ky", o: "15" },
  { s: "nguyen-trai", p: "doi-dau-voi", o: "Quân Minh" },
  { s: "nguyen-trai", p: "noi-tieng-voi", o: "Khởi nghĩa Lam Sơn" },
  { s: "nguyen-trai", p: "gan-voi-dia-danh", o: "Lam Sơn" },
  { s: "nguyen-trai", p: "co-tac-pham", o: "Bình Ngô đại cáo" },

  // Quang Trung
  { s: "quang-trung", p: "is-a", o: "Vua" },
  { s: "quang-trung", p: "is-a", o: "Danh tướng" },
  { s: "quang-trung", p: "gioi-tinh", o: "Nam" },
  { s: "quang-trung", p: "thuoc-the-ky", o: "18" },
  { s: "quang-trung", p: "doi-dau-voi", o: "Quân Thanh" },
  { s: "quang-trung", p: "noi-tieng-voi", o: "Chiến thắng Ngọc Hồi - Đống Đa" },
  { s: "quang-trung", p: "gan-voi-dia-danh", o: "Thăng Long" },
  { s: "quang-trung", p: "sang-lap", o: "Nhà Tây Sơn" },

  // Nguyễn Du
  { s: "nguyen-du", p: "is-a", o: "Nhà thơ" },
  { s: "nguyen-du", p: "gioi-tinh", o: "Nam" },
  { s: "nguyen-du", p: "thuoc-the-ky", o: "18" },
  { s: "nguyen-du", p: "thuoc-the-ky", o: "19" },
  { s: "nguyen-du", p: "co-tac-pham", o: "Truyện Kiều" },
  { s: "nguyen-du", p: "gan-voi-dia-danh", o: "Hà Tĩnh" },

  // Hồ Chí Minh
  { s: "ho-chi-minh", p: "is-a", o: "Nhà chính trị" },
  { s: "ho-chi-minh", p: "is-a", o: "Nhà thơ" },
  { s: "ho-chi-minh", p: "gioi-tinh", o: "Nam" },
  { s: "ho-chi-minh", p: "thuoc-the-ky", o: "20" },
  { s: "ho-chi-minh", p: "doi-dau-voi", o: "Thực dân Pháp" },
  { s: "ho-chi-minh", p: "doi-dau-voi", o: "Đế quốc Mỹ" },
  { s: "ho-chi-minh", p: "noi-tieng-voi", o: "Cách mạng Tháng Tám" },
  { s: "ho-chi-minh", p: "co-tac-pham", o: "Nhật ký trong tù" },
  { s: "ho-chi-minh", p: "co-tac-pham", o: "Tuyên ngôn độc lập" },
  { s: "ho-chi-minh", p: "sang-lap", o: "Nước Việt Nam Dân chủ Cộng hòa" },
  { s: "ho-chi-minh", p: "gan-voi-dia-danh", o: "Nghệ An" },

  // Võ Nguyên Giáp
  { s: "vo-nguyen-giap", p: "is-a", o: "Danh tướng" },
  { s: "vo-nguyen-giap", p: "gioi-tinh", o: "Nam" },
  { s: "vo-nguyen-giap", p: "thuoc-the-ky", o: "20" },
  { s: "vo-nguyen-giap", p: "doi-dau-voi", o: "Thực dân Pháp" },
  { s: "vo-nguyen-giap", p: "doi-dau-voi", o: "Đế quốc Mỹ" },
  { s: "vo-nguyen-giap", p: "noi-tieng-voi", o: "Chiến thắng Điện Biên Phủ" },
  { s: "vo-nguyen-giap", p: "gan-voi-dia-danh", o: "Điện Biên Phủ" },
  { s: "vo-nguyen-giap", p: "gan-voi-dia-danh", o: "Quảng Bình" },
];

export function entityName(id: string): string {
  return entities.find((e) => e.id === id)?.name ?? id;
}

export function triplesOf(entityId: string): Triple[] {
  return triples.filter((t) => t.s === entityId);
}

export function stats(): { soThucThe: number; soBoBa: number } {
  const s = { soThucThe: entities.length, soBoBa: triples.length };
  console.log(
    `[KB] ${s.soThucThe} thực thể, ${s.soBoBa} bộ ba (yêu cầu: ≥ 12 và ≥ 40)`
  );
  return s;
}

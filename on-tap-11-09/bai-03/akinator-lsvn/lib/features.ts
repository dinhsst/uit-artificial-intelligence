import type { Feature, Predicate } from "@/types";
import { entities, triples } from "./kb";

/** Viết thường chữ cái đầu, giữ nguyên danh từ riêng phía sau. */
const thuong = (o: string) => o.charAt(0).toLowerCase() + o.slice(1);

const MAU_CAU_HOI: Record<Predicate, (o: string) => string> = {
  "is-a": (o) => `Nhân vật này là ${thuong(o)}?`,
  "thuoc-the-ky": (o) => `Nhân vật này sống ở thế kỷ ${o}?`,
  "doi-dau-voi": (o) => `Nhân vật này từng đối đầu với ${thuong(o)}?`,
  "noi-tieng-voi": (o) => `Nhân vật này nổi tiếng với ${thuong(o)}?`,
  "gan-voi-dia-danh": (o) => `Nhân vật này gắn với ${o}?`,
  "co-tac-pham": (o) => `Nhân vật này là tác giả của ${o}?`,
  "gioi-tinh": (o) => `Nhân vật này là ${thuong(o)}?`,
  "sang-lap": (o) => `Nhân vật này sáng lập ${o}?`,
};

const NGUONG_THE_KY = [10, 15, 19, 20];

function buildFeatures(): Feature[] {
  const out: Feature[] = [];

  // 1. Mỗi cặp (predicate, object) trong KB thành một đặc trưng.
  const seen = new Set<string>();
  for (const t of triples) {
    // "gioi-tinh:Nam" mang đúng cùng một bit thông tin với "gioi-tinh:Nữ".
    if (t.p === "gioi-tinh" && t.o !== "Nữ") continue;
    const id = `${t.p}:${t.o}`;
    if (seen.has(id)) continue;
    seen.add(id);
    const members = new Set(
      triples.filter((x) => x.p === t.p && x.o === t.o).map((x) => x.s)
    );
    out.push({
      id,
      question: MAU_CAU_HOI[t.p](t.o),
      holds: (e) => members.has(e),
    });
  }

  // 3. Đặc trưng dẫn xuất theo khoảng thế kỷ.
  for (const nguong of NGUONG_THE_KY) {
    const members = new Set(
      triples
        .filter((t) => t.p === "thuoc-the-ky" && Number(t.o) < nguong)
        .map((t) => t.s)
    );
    out.push({
      id: `the-ky-truoc:${nguong}`,
      question: `Nhân vật này sống trước thế kỷ ${nguong}?`,
      holds: (e) => members.has(e),
    });
  }

  // 2. Chỉ loại đặc trưng rỗng hoặc đúng cho toàn bộ KB.
  // Giữ cả đặc trưng đơn thể: information gain tự đẩy chúng xuống thấp khi tập
  // ứng viên còn lớn và lên cao khi chỉ còn vài ứng viên cần tách.
  return out.filter((f) => {
    const n = entities.filter((e) => f.holds(e.id)).length;
    return n >= 1 && n <= 11;
  });
}

export const features: Feature[] = buildFeatures();

export function featureById(id: string): Feature | undefined {
  return features.find((f) => f.id === id);
}

import { entities, entityName, triplesOf } from "@/lib/kb";
import { chat, parseAnswer } from "@/lib/llm";
import { SO_LUOT_TOI_DA } from "@/lib/engine";

/**
 * Đối chứng: LLM đóng vai người đoán, KHÔNG được cấp mạng ngữ nghĩa,
 * chỉ biết miền là "nhân vật lịch sử Việt Nam". Server trả lời dựa trên KB.
 */

const SYSTEM_NGUOI_DOAN = `Bạn đang chơi trò đoán nhân vật lịch sử Việt Nam. Đối phương giữ bí mật một nhân vật.
Mỗi lượt bạn viết đúng MỘT dòng, theo một trong hai dạng:
HOI: <một câu hỏi Có/Không>
DOAN: <tên nhân vật>
Chỉ dùng DOAN khi bạn đã đủ tự tin. Không giải thích gì thêm.`;

const SYSTEM_TRA_LOI = (
  ten: string,
  facts: string
) => `Bạn trả lời câu hỏi Có/Không về nhân vật lịch sử Việt Nam: ${ten}.
Dữ kiện đã biết:
${facts}
Chỉ trả lời bằng đúng một trong ba từ: CO, KHONG, KHONGCHAC. Không giải thích.`;

function chuanHoa(s: string): string {
  return s
    .toLowerCase()
    .normalize("NFD")
    .replace(/[^a-z0-9]/g, "");
}

function khopTen(doan: string, entityId: string): boolean {
  const e = entities.find((x) => x.id === entityId);
  if (!e) return false;
  const d = chuanHoa(doan);
  return [e.name, ...(e.alias ?? [])].some((n) => d.includes(chuanHoa(n)));
}

export async function POST(request: Request) {
  const { secretId } = await request.json();
  const ten = entityName(secretId);
  const facts = triplesOf(secretId)
    .map((t) => `- ${t.p}: ${t.o}`)
    .join("\n");

  const luotHoi: { cauHoi: string; traLoi: string }[] = [];
  let doanCuoi = "";
  let dung = false;

  try {
    for (let i = 0; i < SO_LUOT_TOI_DA; i++) {
      const lichSu = luotHoi.map((l) => `${l.cauHoi} → ${l.traLoi}`).join("\n");
      const dong = await chat({
        system: SYSTEM_NGUOI_DOAN,
        user: lichSu ? `Lịch sử:\n${lichSu}\n\nLượt tiếp theo:` : "Lượt đầu tiên:",
        maxTokens: 80,
        temperature: 0.3,
      });

      if (/^\s*DOAN/i.test(dong)) {
        doanCuoi = dong.replace(/^\s*DOAN\s*:?/i, "").trim();
        dung = khopTen(doanCuoi, secretId);
        luotHoi.push({ cauHoi: `(đoán) ${doanCuoi}`, traLoi: dung ? "CO" : "KHONG" });
        if (dung) break;
        continue;
      }

      const cauHoi = dong.replace(/^\s*HOI\s*:?/i, "").trim() || dong.trim();
      const raw = await chat({
        system: SYSTEM_TRA_LOI(ten, facts),
        user: cauHoi,
        maxTokens: 16,
        temperature: 0,
      });
      const a = parseAnswer(raw);
      luotHoi.push({
        cauHoi,
        traLoi: a === "yes" ? "CO" : a === "no" ? "KHONG" : "KHONGCHAC",
      });
    }
  } catch (e) {
    return Response.json({
      nhanVatBiMat: ten,
      luotHoi,
      doanCuoi,
      dung,
      soLuotDaDung: luotHoi.length,
      error: e instanceof Error ? e.message : String(e),
    });
  }

  return Response.json({
    nhanVatBiMat: ten,
    luotHoi,
    doanCuoi,
    dung,
    soLuotDaDung: luotHoi.length,
  });
}

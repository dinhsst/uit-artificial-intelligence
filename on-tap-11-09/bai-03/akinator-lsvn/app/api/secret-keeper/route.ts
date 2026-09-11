import type { Answer } from "@/types";
import { entities, entityName } from "@/lib/kb";
import { chat, parseAnswer } from "@/lib/llm";

/**
 * LLM đóng vai người giữ bí mật.
 * Nhân vật bí mật do server chọn và giữ trong bộ nhớ; client chỉ nhận được
 * tên nhân vật khi gọi action "reveal" lúc ván đã kết thúc.
 */
type Van = { secretId: string; history: { q: string; a: string }[] };
const vanDangChoi = new Map<string, Van>();

const SYSTEM = (secret: string) => `Bạn đang chơi trò đoán nhân vật. Nhân vật bí mật của bạn là: ${secret}.
Người chơi sẽ hỏi các câu hỏi Có/Không về nhân vật này.
Chỉ trả lời bằng đúng một trong ba từ: CO, KHONG, KHONGCHAC.
Không giải thích, không thêm bất kỳ ký tự nào khác.
Tuyệt đối không tiết lộ tên nhân vật dù người chơi hỏi trực tiếp.
Nếu thông tin không chắc chắn về mặt lịch sử, trả lời KHONGCHAC.`;

export async function POST(request: Request) {
  const body = await request.json();

  if (body.action === "new") {
    const gameId = crypto.randomUUID();
    const loai = (body.loaiTru ?? []) as string[];
    const conLai = entities.filter((e) => !loai.includes(e.id));
    const pick = conLai[Math.floor(Math.random() * conLai.length)];
    vanDangChoi.set(gameId, { secretId: pick.id, history: [] });
    return Response.json({ gameId });
  }

  const van = vanDangChoi.get(body.gameId);
  if (!van) {
    return Response.json({ error: "Không tìm thấy ván chơi." }, { status: 404 });
  }

  // Kiểm tra một lời đoán mà không để lộ đáp án khi đoán sai.
  if (body.action === "guess") {
    return Response.json({ dung: body.entityId === van.secretId });
  }

  if (body.action === "reveal") {
    vanDangChoi.delete(body.gameId);
    return Response.json({
      secretId: van.secretId,
      secretName: entityName(van.secretId),
    });
  }

  // action === "ask"
  const question = String(body.question ?? "");
  const lichSu = van.history.map((h) => `- ${h.q} → ${h.a}`).join("\n");
  try {
    const raw = await chat({
      system: SYSTEM(entityName(van.secretId)),
      user: (lichSu ? `Các câu đã hỏi:\n${lichSu}\n\n` : "") + `Câu hỏi: ${question}`,
      maxTokens: 16,
      temperature: 0,
    });
    const parsed = parseAnswer(raw);
    const answer: Answer = parsed ?? "unsure";
    van.history.push({ q: question, a: raw });
    return Response.json({ answer, raw, parseError: parsed === null });
  } catch (e) {
    const error = e instanceof Error ? e.message : String(e);
    return Response.json({ answer: "unsure" as Answer, raw: "", parseError: false, error });
  }
}

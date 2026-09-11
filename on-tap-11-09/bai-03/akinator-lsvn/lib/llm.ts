import OpenAI from "openai";

const BASE_URL = process.env.LLM_BASE_URL ?? "https://api.deepseek.com";
const MODEL = process.env.LLM_MODEL ?? "deepseek-chat";

function getClient(): OpenAI {
  const apiKey = process.env.LLM_API_KEY;
  if (!apiKey) {
    throw new Error(
      "Thiếu LLM_API_KEY. Hãy tạo file .env.local (xem .env.example) rồi khởi động lại `npm run dev`."
    );
  }
  return new OpenAI({ apiKey, baseURL: BASE_URL, timeout: 20_000, maxRetries: 1 });
}

export async function chat(opts: {
  system: string;
  user: string;
  maxTokens?: number;
  temperature?: number;
}): Promise<string> {
  const res = await getClient().chat.completions.create({
    model: MODEL,
    messages: [
      { role: "system", content: opts.system },
      { role: "user", content: opts.user },
    ],
    max_tokens: opts.maxTokens ?? 16,
    temperature: opts.temperature ?? 0,
    stream: false,
  });
  return res.choices[0]?.message?.content?.trim() ?? "";
}

/** Chuẩn hóa chữ hoa, bỏ dấu và dấu câu; khớp KHONGCHAC trước KHONG vì trùng tiền tố. */
export function parseAnswer(raw: string): "yes" | "no" | "unsure" | null {
  const s = raw
    .toUpperCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/[^A-Z]/g, "");
  if (s.includes("KHONGCHAC")) return "unsure";
  if (s.includes("KHONG")) return "no";
  if (s.includes("CO")) return "yes";
  return null;
}

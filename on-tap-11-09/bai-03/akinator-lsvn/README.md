# Đoán nhân vật lịch sử Việt Nam

Bản thu gọn của Akinator cho Bài 3: hệ thống đóng vai **người đặt câu hỏi**, LLM đóng vai
**người giữ bí mật**. Cơ sở tri thức là một mạng ngữ nghĩa dạng bộ ba
`(subject, predicate, object)`; chiến lược hỏi dựa trên **information gain**.

## Chạy

```bash
npm install
cp .env.example .env.local   # rồi điền LLM_API_KEY
npm run dev                  # http://localhost:3000
```

`.env.local`:

```
LLM_API_KEY=sk-...
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
```

Đổi nhà cung cấp LLM chỉ cần sửa ba dòng trên, không sửa code (mọi lời gọi đi qua `lib/llm.ts`):

| Nhà cung cấp | `LLM_BASE_URL` | `LLM_MODEL` |
|---|---|---|
| DeepSeek (mặc định) | `https://api.deepseek.com` | `deepseek-chat` |
| OpenAI | `https://api.openai.com/v1` | `gpt-4o-mini` |
| Google Gemini | `https://generativelanguage.googleapis.com/v1beta/openai` | `gemini-2.0-flash` |
| Groq | `https://api.groq.com/openai/v1` | `llama-3.3-70b-versatile` |

## Ba chế độ trên giao diện

| Tab | Ai giữ bí mật | Cần API key |
|---|---|---|
| Tôi giữ bí mật | người dùng bấm Có / Không / Không chắc | không |
| LLM giữ bí mật | LLM, server chọn ngẫu nhiên và giấu | có |
| Chạy 5 ván tự động | LLM, chạy liên tiếp 5 ván rồi 5 ván đối chứng | có |

Nút **Tải log** ở tab thứ ba xuất `ket-qua-5-van.json` để dán vào báo cáo.

## Kiểm thử bộ suy diễn (không cần API key)

```bash
npm run sim
```

In ra số thực thể / bộ ba của KB, mô phỏng một ván với câu trả lời lấy thẳng từ KB,
và kiểm tra tiêu chí "IG lượt 1 ≥ 0.9 bit".

## Cấu trúc

```
app/page.tsx                   giao diện ba tab
app/api/secret-keeper/route.ts LLM trả lời CO / KHONG / KHONGCHAC
app/api/baseline/route.ts      đối chứng: LLM đoán mò, không có mạng ngữ nghĩa
lib/llm.ts                     điểm duy nhất gọi API LLM
lib/kb.ts                      mạng ngữ nghĩa: 12 thực thể, 89 bộ ba
lib/features.ts                sinh câu hỏi nhị phân từ bộ ba
lib/engine.ts                  entropy, information gain, cập nhật Bayes mềm
lib/autoplay.ts                vòng lặp tự chơi và dựng log JSON
```

Trạng thái ván chơi (nhân vật bí mật) nằm trong bộ nhớ server; client chỉ nhận được
đáp án khi ván kết thúc. API key không bao giờ rời khỏi phía server.

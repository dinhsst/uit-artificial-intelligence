import OpenAI from 'openai';
import { config } from '../config.js';

const cache = new Map();

export async function answerWithGraph({ question, subgraph }) {
  if (!config.llmApiKey) throw new Error('LLM_NOT_CONFIGURED');
  const key = JSON.stringify({ question, subgraph });
  if (cache.has(key)) return cache.get(key);
  const client = new OpenAI({ apiKey: config.llmApiKey, baseURL: config.llmBaseUrl, timeout: config.llmTimeoutMs });
  const completion = await client.chat.completions.create({
    model: config.llmModel,
    temperature: 0.2,
    messages: [
      { role: 'system', content: 'Bạn là trợ lý học tập. Chỉ trả lời dựa trên knowledge graph được cung cấp. Nếu graph không đủ thông tin, hãy nói rõ điều đó. Trả lời bằng tiếng Việt, súc tích.' },
      { role: 'user', content: `Câu hỏi: ${question}\n\nKnowledge graph:\n${JSON.stringify(subgraph)}` }
    ]
  });
  const answer = completion.choices[0]?.message?.content?.trim() || 'Không nhận được câu trả lời từ mô hình.';
  cache.set(key, answer);
  return answer;
}

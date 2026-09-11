/**
 * Kiểm thử nhanh bộ suy diễn, không cần gọi LLM.
 * Chạy: npm run sim
 * "Người giữ bí mật" ở đây là chính KB, nên câu trả lời luôn đúng.
 */
import { entities, entityName, stats } from "@/lib/kb";
import { features } from "@/lib/features";
import {
  SO_LUOT_TOI_DA,
  applyAnswer,
  entropy,
  newGame,
  ranking,
  selectNextQuestion,
  shouldGuess,
} from "@/lib/engine";

stats();
console.log(`[Đặc trưng] ${features.length} câu hỏi khả dụng\n`);

const bimat = entities[5].id; // Trần Hưng Đạo
let state = newGame();
console.log(`Nhân vật bí mật: ${entityName(bimat)}`);
console.log(`Entropy ban đầu: ${entropy(state.posterior).toFixed(2)} bit\n`);

while (!shouldGuess(state) && state.turns.length < SO_LUOT_TOI_DA) {
  const chon = selectNextQuestion(state);
  if (!chon) break;
  const answer = chon.feature.holds(bimat) ? "yes" : "no";
  state = applyAnswer(state, chon.feature, chon.ig, answer);
  const t = state.turns[state.turns.length - 1];
  console.log(
    `Lượt ${state.turns.length}: ${t.question} → ${answer}  ` +
      `(IG = ${t.informationGain.toFixed(2)} bit, entropy còn ${t.entropyAfter.toFixed(2)})`
  );
}

const top = ranking(state.posterior)[0];
console.log(
  `\nĐoán: ${entityName(top.id)} (${(top.p * 100).toFixed(1)}%) sau ${state.turns.length} lượt`
);
console.log(`Kết quả: ${top.id === bimat ? "ĐÚNG" : "SAI"}`);

const ig1 = state.turns[0]?.informationGain ?? 0;
console.log(
  `\nTiêu chí 3 — IG lượt 1 = ${ig1.toFixed(2)} bit: ${ig1 >= 0.9 ? "ĐẠT" : "KHÔNG ĐẠT"}`
);

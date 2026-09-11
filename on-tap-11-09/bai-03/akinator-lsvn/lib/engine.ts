import type { Answer, Feature, GameState } from "@/types";
import { entities } from "./kb";
import { features } from "./features";

export const SO_LUOT_TOI_DA = 10;
export const NGUONG_DOAN = 0.85;
/** IG tối thiểu để một câu hỏi còn đáng hỏi. */
export const NGUONG_IG = 0.2;
const EPSILON = 0.1;

export function newGame(): GameState {
  const p = 1 / entities.length;
  const posterior: Record<string, number> = {};
  for (const e of entities) posterior[e.id] = p;
  return { posterior, askedFeatureIds: [], turns: [] };
}

export function entropy(posterior: Record<string, number>): number {
  let h = 0;
  for (const p of Object.values(posterior)) {
    if (p > 0) h -= p * Math.log2(p);
  }
  return h;
}

function normalize(posterior: Record<string, number>): Record<string, number> {
  const total = Object.values(posterior).reduce((a, b) => a + b, 0);
  if (total <= 0) return posterior;
  const out: Record<string, number> = {};
  for (const [id, p] of Object.entries(posterior)) out[id] = p / total;
  return out;
}

/** Xác suất "Có" và entropy hai nhánh của một đặc trưng. */
function split(posterior: Record<string, number>, f: Feature) {
  let pYes = 0;
  for (const [id, p] of Object.entries(posterior)) {
    if (f.holds(id)) pYes += p;
  }
  const yes: Record<string, number> = {};
  const no: Record<string, number> = {};
  for (const [id, p] of Object.entries(posterior)) {
    if (f.holds(id)) yes[id] = p;
    else no[id] = p;
  }
  return {
    pYes,
    hYes: pYes > 0 ? entropy(normalize(yes)) : 0,
    hNo: pYes < 1 ? entropy(normalize(no)) : 0,
  };
}

export function informationGain(
  posterior: Record<string, number>,
  f: Feature
): number {
  const { pYes, hYes, hNo } = split(posterior, f);
  return entropy(posterior) - (pYes * hYes + (1 - pYes) * hNo);
}

/** Chọn đặc trưng có IG lớn nhất; hòa thì ưu tiên pYes gần 0.5 nhất. */
export function selectNextQuestion(
  state: GameState
): { feature: Feature; ig: number } | null {
  let best: { feature: Feature; ig: number; lech: number } | null = null;
  for (const f of features) {
    if (state.askedFeatureIds.includes(f.id)) continue;
    const ig = informationGain(state.posterior, f);
    const lech = Math.abs(split(state.posterior, f).pYes - 0.5);
    if (
      !best ||
      ig > best.ig + 1e-9 ||
      (Math.abs(ig - best.ig) <= 1e-9 && lech < best.lech)
    ) {
      best = { feature: f, ig, lech };
    }
  }
  return best ? { feature: best.feature, ig: best.ig } : null;
}

/** Cập nhật Bayes mềm: câu trả lời đúng với xác suất 1 - ε. */
export function updatePosterior(
  posterior: Record<string, number>,
  f: Feature,
  answer: Answer
): Record<string, number> {
  if (answer === "unsure") return posterior;
  const out: Record<string, number> = {};
  for (const [id, p] of Object.entries(posterior)) {
    const khop = answer === "yes" ? f.holds(id) : !f.holds(id);
    out[id] = p * (khop ? 1 - EPSILON : EPSILON);
  }
  return normalize(out);
}

export function applyAnswer(
  state: GameState,
  f: Feature,
  ig: number,
  answer: Answer
): GameState {
  const posterior = updatePosterior(state.posterior, f, answer);
  return {
    posterior,
    askedFeatureIds: [...state.askedFeatureIds, f.id],
    turns: [
      ...state.turns,
      {
        question: f.question,
        featureId: f.id,
        answer,
        informationGain: ig,
        entropyAfter: entropy(posterior),
      },
    ],
  };
}

export function ranking(
  posterior: Record<string, number>
): { id: string; p: number }[] {
  return Object.entries(posterior)
    .map(([id, p]) => ({ id, p }))
    .sort((a, b) => b.p - a.p);
}

/**
 * Dừng hỏi và đoán khi: đã đủ tự tin, hoặc cạn lượt, hoặc không còn câu hỏi nào
 * cắt được đủ thông tin (tránh đốt lượt vào câu gần như vô dụng).
 */
export function shouldGuess(state: GameState): boolean {
  const top = ranking(state.posterior)[0];
  if (!top || top.p >= NGUONG_DOAN) return true;
  if (state.turns.length >= SO_LUOT_TOI_DA) return true;
  const chon = selectNextQuestion(state);
  return chon === null || chon.ig < NGUONG_IG;
}

/** Đoán sai: loại nhân vật đó khỏi không gian tìm kiếm. */
export function eliminate(state: GameState, entityId: string): GameState {
  const posterior = normalize({ ...state.posterior, [entityId]: 0 });
  return { ...state, posterior };
}

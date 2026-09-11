import type { Answer, GameState } from "@/types";
import { entityName } from "./kb";
import {
  SO_LUOT_TOI_DA,
  applyAnswer,
  eliminate,
  newGame,
  ranking,
  selectNextQuestion,
  shouldGuess,
} from "./engine";

export interface LuotHoiLog {
  cauHoi: string;
  traLoi: string;
  informationGain: number;
  entropySauLuot: number;
}

export interface VanChoiLog {
  id: number;
  nhanVatBiMat: string;
  luotHoi: LuotHoiLog[];
  doanCuoi: string;
  dung: boolean;
  soLuotDaDung: number;
}

export interface KetQuaLog {
  vanChoi: VanChoiLog[];
  tongKet: {
    tyLeDung: number;
    soLuotTrungBinh: number;
    baselineSoLuotTrungBinh: number | null;
  };
  nhanhThieuSot: string[];
}

const NHAN: Record<Answer, string> = {
  yes: "CO",
  no: "KHONG",
  unsure: "KHONGCHAC",
};

async function post<T>(url: string, body: unknown): Promise<T> {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  return res.json() as Promise<T>;
}

/**
 * Một ván "LLM giữ bí mật": hệ thống hỏi, LLM trả lời, dừng theo điều kiện ở engine.
 * onTurn cho phép giao diện vẽ lại sau mỗi lượt.
 */
export async function playOneGame(
  id: number,
  loaiTruBiMat: string[],
  onTurn?: (state: GameState) => void
): Promise<{ log: VanChoiLog; secretId: string }> {
  const { gameId } = await post<{ gameId: string }>("/api/secret-keeper", {
    action: "new",
    loaiTru: loaiTruBiMat,
  });

  let state = newGame();
  let doanCuoi = "";
  let dung = false;

  while (true) {
    if (shouldGuess(state)) {
      const top = ranking(state.posterior)[0];
      if (!top || top.p <= 0) break;
      doanCuoi = entityName(top.id);
      const kq = await post<{ dung: boolean }>("/api/secret-keeper", {
        action: "guess",
        gameId,
        entityId: top.id,
      });
      dung = kq.dung;
      if (dung) break;
      if (state.turns.length >= SO_LUOT_TOI_DA) break; // cạn lượt thì dừng
      state = eliminate(state, top.id); // còn lượt: loại rồi hỏi tiếp
      continue;
    }

    const chon = selectNextQuestion(state);
    if (!chon) break;
    const kq = await post<{ answer: Answer }>("/api/secret-keeper", {
      action: "ask",
      gameId,
      question: chon.feature.question,
    });
    state = applyAnswer(state, chon.feature, chon.ig, kq.answer);
    onTurn?.(state);
  }

  const reveal = await post<{ secretId: string; secretName: string }>(
    "/api/secret-keeper",
    { action: "reveal", gameId }
  );

  return {
    secretId: reveal.secretId,
    log: {
      id,
      nhanVatBiMat: reveal.secretName,
      luotHoi: state.turns.map((t) => ({
        cauHoi: t.question,
        traLoi: NHAN[t.answer],
        informationGain: Number(t.informationGain.toFixed(2)),
        entropySauLuot: Number(t.entropyAfter.toFixed(2)),
      })),
      doanCuoi,
      dung,
      soLuotDaDung: state.turns.length,
    },
  };
}

/** Chạy 5 ván liên tiếp, mỗi ván một nhân vật khác nhau. */
export async function playFiveGames(
  onProgress?: (van: VanChoiLog) => void
): Promise<{ logs: VanChoiLog[]; secretIds: string[] }> {
  const logs: VanChoiLog[] = [];
  const secretIds: string[] = [];
  for (let i = 1; i <= 5; i++) {
    const { log, secretId } = await playOneGame(i, secretIds);
    logs.push(log);
    secretIds.push(secretId);
    onProgress?.(log);
  }
  return { logs, secretIds };
}

export function buildLog(
  logs: VanChoiLog[],
  baselineSoLuot: number[] | null
): KetQuaLog {
  const dung = logs.filter((v) => v.dung).length;
  const tb = (xs: number[]) => xs.reduce((a, b) => a + b, 0) / (xs.length || 1);
  return {
    vanChoi: logs,
    tongKet: {
      tyLeDung: logs.length ? Number((dung / logs.length).toFixed(2)) : 0,
      soLuotTrungBinh: Number(tb(logs.map((v) => v.soLuotDaDung)).toFixed(2)),
      baselineSoLuotTrungBinh: baselineSoLuot
        ? Number(tb(baselineSoLuot).toFixed(2))
        : null,
    },
    nhanhThieuSot: [],
  };
}

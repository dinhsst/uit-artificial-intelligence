"use client";

import { useState } from "react";
import type { Answer, Feature, GameState } from "@/types";
import { entityName } from "@/lib/kb";
import {
  SO_LUOT_TOI_DA,
  applyAnswer,
  eliminate,
  entropy,
  newGame,
  ranking,
  selectNextQuestion,
  shouldGuess,
} from "@/lib/engine";
import {
  buildLog,
  playFiveGames,
  playOneGame,
  type VanChoiLog,
} from "@/lib/autoplay";

type Tab = "tay" | "llm" | "auto";

const TABS: { id: Tab; nhan: string }[] = [
  { id: "tay", nhan: "Tôi giữ bí mật" },
  { id: "llm", nhan: "LLM giữ bí mật" },
  { id: "auto", nhan: "Chạy 5 ván tự động" },
];

export default function Page() {
  const [tab, setTab] = useState<Tab>("tay");

  return (
    <main className="mx-auto w-full max-w-5xl px-6 py-10">
      <h1 className="text-2xl font-[600]">Đoán nhân vật lịch sử Việt Nam</h1>
      <p className="mt-1 text-sm text-diep/60">
        Mạng ngữ nghĩa · chọn câu hỏi theo information gain · tối đa{" "}
        {SO_LUOT_TOI_DA} câu hỏi mỗi ván
      </p>

      <div className="mt-6 flex gap-1 border-b border-diep/15">
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`px-4 py-2 text-sm transition-colors ${
              tab === t.id
                ? "border-b-2 border-son font-[600] text-diep"
                : "text-diep/50 hover:text-diep/80"
            }`}
          >
            {t.nhan}
          </button>
        ))}
      </div>

      <div className="mt-8">
        {tab === "tay" && <ChoiTay />}
        {tab === "llm" && <ChoiVoiLLM />}
        {tab === "auto" && <TuDong />}
      </div>
    </main>
  );
}

/* ---------------------------------- Chung --------------------------------- */

function BangUngVien({
  posterior,
  ig,
}: {
  posterior: Record<string, number>;
  ig: number | null;
}) {
  const xh = ranking(posterior).filter((r) => r.p > 0.001);
  return (
    <aside className="rounded border border-diep/15 bg-cham-nhat p-5">
      <h2 className="text-sm font-[600]">Bảng ứng viên</h2>
      <ul className="mt-4 space-y-2">
        {xh.map((r) => (
          <li key={r.id} className="text-sm">
            <div className="flex justify-between">
              <span>{entityName(r.id)}</span>
              <span className="tabular-nums text-diep/60">
                {(r.p * 100).toFixed(1)}%
              </span>
            </div>
            <div className="mt-1 h-1 bg-diep/10">
              <div
                className="h-1 bg-hoe"
                style={{ width: `${Math.max(r.p * 100, 0.5)}%` }}
              />
            </div>
          </li>
        ))}
      </ul>
      <dl className="mt-5 space-y-1 border-t border-diep/15 pt-4 text-xs text-diep/60">
        <div className="flex justify-between">
          <dt>Entropy</dt>
          <dd className="tabular-nums">{entropy(posterior).toFixed(2)} bit</dd>
        </div>
        <div className="flex justify-between">
          <dt>IG câu vừa chọn</dt>
          <dd className="tabular-nums">
            {ig === null ? "—" : `${ig.toFixed(2)} bit`}
          </dd>
        </div>
      </dl>
    </aside>
  );
}

function NhatKy({ state }: { state: GameState }) {
  if (state.turns.length === 0) return null;
  const nhan: Record<Answer, string> = {
    yes: "Có",
    no: "Không",
    unsure: "Không chắc",
  };
  return (
    <section className="mt-8">
      <h2 className="text-sm font-[600]">Nhật ký hỏi đáp</h2>
      <ol className="mt-3 max-h-56 space-y-1 overflow-y-auto text-sm text-diep/70">
        {state.turns.map((t, i) => (
          <li key={i} className="flex gap-3 border-b border-diep/10 py-1.5">
            <span className="w-6 shrink-0 tabular-nums text-diep/40">
              {i + 1}
            </span>
            <span className="flex-1">{t.question}</span>
            <span className="shrink-0 font-[600] text-hoe">
              {nhan[t.answer]}
            </span>
            <span className="w-28 shrink-0 text-right tabular-nums text-xs text-diep/40">
              IG {t.informationGain.toFixed(2)} · H{" "}
              {t.entropyAfter.toFixed(2)}
            </span>
          </li>
        ))}
      </ol>
    </section>
  );
}

const NUT = "px-5 py-2 text-sm font-[600] transition-colors";

/* ------------------------- Chế độ 1: người giữ bí mật ---------------------- */

function ChoiTay() {
  const [state, setState] = useState<GameState>(newGame);
  const [chon, setChon] = useState<{ feature: Feature; ig: number } | null>(() =>
    selectNextQuestion(newGame())
  );
  const [ketThuc, setKetThuc] = useState<"dung" | "het" | null>(null);

  const dangDoan = ketThuc === null && shouldGuess(state);
  const ungVienTop = ranking(state.posterior)[0];

  function traLoi(answer: Answer) {
    if (!chon) return;
    const next = applyAnswer(state, chon.feature, chon.ig, answer);
    setState(next);
    setChon(shouldGuess(next) ? null : selectNextQuestion(next));
  }

  function doanSai() {
    const next = eliminate(state, ungVienTop.id);
    setState(next);
    if (next.turns.length >= SO_LUOT_TOI_DA) setKetThuc("het");
    else setChon(selectNextQuestion(next));
  }

  function choiLai() {
    const g = newGame();
    setState(g);
    setChon(selectNextQuestion(g));
    setKetThuc(null);
  }

  return (
    <>
      <p className="text-sm text-diep/60">
        Lượt {state.turns.length} / {SO_LUOT_TOI_DA}
      </p>
      <div className="mt-4 grid gap-6 md:grid-cols-[1fr_18rem]">
        <div className="rounded border border-diep/15 bg-cham-nhat p-8">
          {ketThuc === "dung" && (
            <>
              <p className="text-3xl font-[800] leading-snug">
                Đã đoán ra: {entityName(ungVienTop.id)}
              </p>
              <button
                onClick={choiLai}
                className={`${NUT} mt-8 bg-son hover:bg-son/85`}
              >
                Chơi ván mới
              </button>
            </>
          )}
          {ketThuc === "het" && (
            <>
              <p className="text-3xl font-[800] leading-snug">
                Hết lượt, chưa đoán ra.
              </p>
              <button
                onClick={choiLai}
                className={`${NUT} mt-8 bg-son hover:bg-son/85`}
              >
                Chơi ván mới
              </button>
            </>
          )}
          {ketThuc === null && dangDoan && (
            <>
              <p className="text-3xl font-[800] leading-snug">
                Có phải nhân vật của bạn là {entityName(ungVienTop.id)}?
              </p>
              <div className="mt-8 flex gap-2">
                <button
                  onClick={() => setKetThuc("dung")}
                  className={`${NUT} bg-son hover:bg-son/85`}
                >
                  Đúng
                </button>
                <button
                  onClick={doanSai}
                  className={`${NUT} border border-diep/25 hover:bg-diep/10`}
                >
                  Sai
                </button>
              </div>
            </>
          )}
          {ketThuc === null && !dangDoan && chon && (
            <>
              <p className="text-3xl font-[800] leading-snug">
                {chon.feature.question}
              </p>
              <div className="mt-8 flex flex-wrap gap-2">
                <button
                  onClick={() => traLoi("yes")}
                  className={`${NUT} bg-son hover:bg-son/85`}
                >
                  Có
                </button>
                <button
                  onClick={() => traLoi("no")}
                  className={`${NUT} border border-diep/25 hover:bg-diep/10`}
                >
                  Không
                </button>
                <button
                  onClick={() => traLoi("unsure")}
                  className={`${NUT} border border-diep/25 hover:bg-diep/10`}
                >
                  Không chắc
                </button>
              </div>
            </>
          )}
        </div>
        <BangUngVien posterior={state.posterior} ig={chon?.ig ?? null} />
      </div>
      <NhatKy state={state} />
    </>
  );
}

/* --------------------------- Chế độ 2: LLM giữ bí mật ---------------------- */

function ChoiVoiLLM() {
  const [state, setState] = useState<GameState>(newGame);
  const [dangChay, setDangChay] = useState(false);
  const [ketQua, setKetQua] = useState<VanChoiLog | null>(null);
  const [loi, setLoi] = useState<string | null>(null);

  async function chay() {
    setDangChay(true);
    setKetQua(null);
    setLoi(null);
    setState(newGame());
    try {
      const { log } = await playOneGame(1, [], setState);
      setKetQua(log);
    } catch (e) {
      setLoi(e instanceof Error ? e.message : String(e));
    } finally {
      setDangChay(false);
    }
  }

  const cauCuoi = state.turns[state.turns.length - 1];

  return (
    <>
      <p className="text-sm text-diep/60">
        Lượt {state.turns.length} / {SO_LUOT_TOI_DA}
      </p>
      <div className="mt-4 grid gap-6 md:grid-cols-[1fr_18rem]">
        <div className="rounded border border-diep/15 bg-cham-nhat p-8">
          <p className="text-3xl font-[800] leading-snug">
            {ketQua
              ? `${ketQua.dung ? "Đoán đúng" : "Đoán sai"}: ${ketQua.doanCuoi || "—"} · nhân vật bí mật là ${ketQua.nhanVatBiMat}`
              : dangChay
                ? (cauCuoi?.question ?? "Đang chọn câu hỏi đầu tiên…")
                : "LLM sẽ giữ một nhân vật bí mật, hệ thống tự hỏi."}
          </p>
          {loi && <p className="mt-4 text-sm text-son">Lỗi: {loi}</p>}
          <button
            onClick={chay}
            disabled={dangChay}
            className={`${NUT} mt-8 bg-son hover:bg-son/85 disabled:opacity-40`}
          >
            {dangChay ? "Đang chơi…" : "Bắt đầu ván mới"}
          </button>
        </div>
        <BangUngVien
          posterior={state.posterior}
          ig={cauCuoi?.informationGain ?? null}
        />
      </div>
      <NhatKy state={state} />
    </>
  );
}

/* ----------------------------- Chế độ 3: 5 ván ----------------------------- */

function TuDong() {
  const [vanChoi, setVanChoi] = useState<VanChoiLog[]>([]);
  const [baseline, setBaseline] = useState<number[] | null>(null);
  const [dangChay, setDangChay] = useState<string | null>(null);
  const [loi, setLoi] = useState<string | null>(null);

  async function chay() {
    setVanChoi([]);
    setBaseline(null);
    setLoi(null);
    try {
      setDangChay("Đang chạy 5 ván có mạng ngữ nghĩa…");
      const ketQua: VanChoiLog[] = [];
      const { logs, secretIds } = await playFiveGames((v) => {
        ketQua.push(v);
        setVanChoi([...ketQua]);
      });
      setVanChoi(logs);

      setDangChay("Đang chạy 5 ván đối chứng (LLM đoán mò)…");
      const soLuot: number[] = [];
      for (const secretId of secretIds) {
        const res = await fetch("/api/baseline", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ secretId }),
        });
        const d = (await res.json()) as { soLuotDaDung: number };
        soLuot.push(d.soLuotDaDung);
        setBaseline([...soLuot]);
      }
    } catch (e) {
      setLoi(e instanceof Error ? e.message : String(e));
    } finally {
      setDangChay(null);
    }
  }

  function taiLog() {
    const blob = new Blob(
      [JSON.stringify(buildLog(vanChoi, baseline), null, 2)],
      { type: "application/json" }
    );
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "ket-qua-5-van.json";
    a.click();
    URL.revokeObjectURL(a.href);
  }

  const tongKet = buildLog(vanChoi, baseline).tongKet;

  return (
    <>
      <div className="flex flex-wrap items-center gap-3">
        <button
          onClick={chay}
          disabled={dangChay !== null}
          className={`${NUT} bg-son hover:bg-son/85 disabled:opacity-40`}
        >
          Chạy 5 ván
        </button>
        <button
          onClick={taiLog}
          disabled={vanChoi.length === 0}
          className={`${NUT} border border-diep/25 hover:bg-diep/10 disabled:opacity-40`}
        >
          Tải log
        </button>
        {dangChay && <span className="text-sm text-diep/60">{dangChay}</span>}
      </div>

      {loi && <p className="mt-4 text-sm text-son">Lỗi: {loi}</p>}

      {vanChoi.length > 0 && (
        <>
          <dl className="mt-8 grid grid-cols-3 gap-4 text-sm">
            <div className="rounded border border-diep/15 bg-cham-nhat p-4">
              <dt className="text-xs text-diep/50">Tỷ lệ đoán đúng</dt>
              <dd className="mt-1 text-2xl font-[800] tabular-nums">
                {(tongKet.tyLeDung * 100).toFixed(0)}%
              </dd>
            </div>
            <div className="rounded border border-diep/15 bg-cham-nhat p-4">
              <dt className="text-xs text-diep/50">Số lượt trung bình</dt>
              <dd className="mt-1 text-2xl font-[800] tabular-nums">
                {tongKet.soLuotTrungBinh.toFixed(1)}
              </dd>
            </div>
            <div className="rounded border border-diep/15 bg-cham-nhat p-4">
              <dt className="text-xs text-diep/50">Đối chứng (đoán mò)</dt>
              <dd className="mt-1 text-2xl font-[800] tabular-nums">
                {tongKet.baselineSoLuotTrungBinh?.toFixed(1) ?? "—"}
              </dd>
            </div>
          </dl>

          <table className="mt-6 w-full text-sm">
            <thead className="text-xs text-diep/50">
              <tr className="border-b border-diep/15 text-left">
                <th className="py-2 font-[600]">Ván</th>
                <th className="py-2 font-[600]">Nhân vật bí mật</th>
                <th className="py-2 font-[600]">Đoán</th>
                <th className="py-2 text-right font-[600]">Số lượt</th>
                <th className="py-2 text-right font-[600]">Kết quả</th>
              </tr>
            </thead>
            <tbody>
              {vanChoi.map((v) => (
                <tr key={v.id} className="border-b border-diep/10">
                  <td className="py-2 tabular-nums text-diep/50">{v.id}</td>
                  <td className="py-2">{v.nhanVatBiMat}</td>
                  <td className="py-2 text-diep/70">{v.doanCuoi || "—"}</td>
                  <td className="py-2 text-right tabular-nums">
                    {v.soLuotDaDung}
                  </td>
                  <td
                    className={`py-2 text-right font-[600] ${v.dung ? "text-hoe" : "text-son"}`}
                  >
                    {v.dung ? "Đúng" : "Sai"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </>
  );
}

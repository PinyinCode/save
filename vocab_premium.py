# -*- coding: utf-8 -*-
r"""
Module TỪ VỰNG PREMIUM - cắm vào fix.py.
Tự sinh bộ thủ + mẹo nhớ từ module vocab_data/.

FIX (2026-10-02 v3):
  - Practice Full: dòng đầu = nghĩa CÂU VÍ DỤ (không phải từ)
  - User gõ = câu ví dụ
  - Block "Ví dụ minh họa" ẨN lúc đầu, chỉ hiện khi click "Xem đáp án"
  - Không hiển thị prefix "Nghĩa:"
"""

import os
import re
import json

import openpyxl

from vocab_data.mnemonic_generator import generate_mnemonic
from vocab_data.radical_analyzer import get_radical_for_word


def _clean(s):
    if s is None:
        return ""
    return (str(s)
            .replace('\n', ' ')
            .replace('\r', ' ')
            .replace('\t', ' ')
            .strip())


def _clean_pinyin(s):
    if s is None:
        return ""
    text = _clean(s).strip('/').strip()
    return re.sub(r'\s+', ' ', text)


def _normalize_hsk(sheet_name):
    if not sheet_name:
        return ""
    s = sheet_name.strip()
    s = re.sub(r'\s+', '', s)
    s = re.sub(r'\(\d+\)$', '', s)
    return s


def _is_hsk_sheet(name):
    return bool(name and name.strip().upper().startswith("HSK"))


def _parse_radical_raw(raw):
    if not raw:
        return None
    text = _clean(raw)
    if not text:
        return None
    if '|' in text:
        parts = [p.strip() for p in text.split('|')]
        if len(parts) >= 2:
            return {
                "zh": parts[0],
                "pinyin": parts[1] if len(parts) > 1 else "",
                "strokes": parts[2] if len(parts) > 2 else "",
                "meaning": parts[3] if len(parts) > 3 else "",
            }
    return {"zh": "", "pinyin": "", "strokes": "", "meaning": text}


def read_vocab_excel(excel_file, start_row=3):
    print("\n[VOCAB] Dang doc: " + excel_file)
    if not os.path.exists(excel_file):
        print("   [X] Khong tim thay file")
        return []
    try:
        wb = openpyxl.load_workbook(excel_file, data_only=True, read_only=True)
    except Exception as e:
        print("   [X] Loi mo file: " + str(e))
        return []

    target_sheets = [s for s in wb.sheetnames if _is_hsk_sheet(s)]
    if not target_sheets:
        print("   [!] Khong co sheet HSK nao")
        wb.close()
        return []

    print("   [OK] " + str(len(target_sheets)) + " sheet: "
          + ", ".join(target_sheets))

    all_data = []
    total_mnemonic_generated = 0
    total_radical_generated = 0

    for sheet_name in target_sheets:
        try:
            ws = wb[sheet_name]
            hsk = _normalize_hsk(sheet_name)
            rows, n_mn, n_rd = _read_vocab_sheet(ws, hsk, sheet_name, start_row)
            all_data.extend(rows)
            total_mnemonic_generated += n_mn
            total_radical_generated += n_rd

            msg = "      " + sheet_name + ": " + str(len(rows)) + " tu"
            if n_mn > 0:
                msg += " (" + str(n_mn) + " meo)"
            if n_rd > 0:
                msg += " (" + str(n_rd) + " bo thu)"
            print(msg)
        except Exception as e:
            print("      [X] Loi sheet " + sheet_name + ": " + str(e))

    wb.close()
    print("   [OK] Tong: " + str(len(all_data)) + " tu vung")
    if total_mnemonic_generated > 0:
        print("   Tu sinh meo nho: " + str(total_mnemonic_generated) + " tu")
    if total_radical_generated > 0:
        print("   Tu tim bo thu: " + str(total_radical_generated) + " tu")

    return all_data


def _read_vocab_sheet(ws, hsk, sheet_name, start_row):
    COL_STT = 0
    COL_ZH = 1
    COL_PINYIN = 2
    COL_LOAI_TU = 4
    COL_VI = 5
    COL_VI_DU_ZH = 8
    COL_VI_DU_PINYIN = 9
    COL_VI_DU_VI = 10
    COL_MNEMONIC = 11
    COL_RADICAL = 12

    data = []
    empty_count = 0
    n_mnemonic_generated = 0
    n_radical_generated = 0

    for row in ws.iter_rows(min_row=start_row, values_only=True):
        if not row:
            empty_count += 1
            if empty_count > 30:
                break
            continue
        if len(row) <= COL_ZH:
            continue

        zh = _clean(row[COL_ZH]) if COL_ZH < len(row) else ""
        if not zh:
            empty_count += 1
            if empty_count > 30:
                break
            continue
        empty_count = 0
        if zh.lower() in ("từ tiếng trung", "汉字", "từ vựng", "từ", "hsk"):
            continue

        stt_raw = row[COL_STT] if COL_STT < len(row) and row[COL_STT] is not None else ""
        pinyin = _clean_pinyin(row[COL_PINYIN]) if COL_PINYIN < len(row) else ""
        vi = _clean(row[COL_VI]) if COL_VI < len(row) else ""

        mnemonic = ""
        if COL_MNEMONIC < len(row):
            mnemonic = _clean(row[COL_MNEMONIC])
        if not mnemonic:
            try:
                mnemonic = generate_mnemonic(zh, pinyin, vi)
                if mnemonic:
                    n_mnemonic_generated += 1
            except Exception:
                mnemonic = ""

        radical = None
        if COL_RADICAL < len(row):
            radical = _parse_radical_raw(row[COL_RADICAL])
        if not radical:
            try:
                radical = get_radical_for_word(zh)
                if radical:
                    n_radical_generated += 1
            except Exception:
                radical = None

        data.append({
            "stt": str(stt_raw).strip(),
            "hsk": hsk,
            "topic": "Từ vựng",
            "subject": _clean(row[COL_LOAI_TU]) if COL_LOAI_TU < len(row) else "",
            "vi": vi,
            "zh": zh,
            "pinyin": pinyin,
            "vi_du_zh": _clean(row[COL_VI_DU_ZH]) if COL_VI_DU_ZH < len(row) else "",
            "vi_du_pinyin": _clean_pinyin(row[COL_VI_DU_PINYIN]) if COL_VI_DU_PINYIN < len(row) else "",
            "vi_du_vi": _clean(row[COL_VI_DU_VI]) if COL_VI_DU_VI < len(row) else "",
            "mnemonic": mnemonic,
            "radical": radical,
            "source_sheet": sheet_name,
        })

    return data, n_mnemonic_generated, n_radical_generated


def build_vocab_css(vocab_id="tu-vung"):
    css = r"""
/* TAB TU VUNG PREMIUM */
.ds-btn[data-dataset="__VOCAB_ID__"] {
    background: linear-gradient(135deg,
        rgba(251, 191, 36, .12) 0%,
        rgba(245, 158, 11, .08) 50%,
        rgba(8, 145, 178, .06) 100%);
    border: 2px solid rgba(245, 158, 11, .4);
    color: #92400e;
    position: relative;
    overflow: visible;
    font-weight: 800;
    padding-left: 2.5rem;
    box-shadow: 0 0 0 1px rgba(245, 158, 11, .2), 0 2px 8px rgba(245, 158, 11, .15);
}
.ds-btn[data-dataset="__VOCAB_ID__"]::before {
    content: '👑';
    position: absolute;
    left: .6rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.1rem;
    line-height: 1;
    z-index: 3;
    filter: drop-shadow(0 2px 4px rgba(245, 158, 11, .8));
    animation: crownTabFloat 3s ease-in-out infinite;
    pointer-events: none;
}
@keyframes crownTabFloat {
    0%, 100% { transform: translateY(-50%) rotate(0deg); }
    50%      { transform: translateY(-50%) rotate(-10deg) scale(1.1); }
}
.ds-btn[data-dataset="__VOCAB_ID__"] > i:first-child { display: none; }
.ds-btn[data-dataset="__VOCAB_ID__"]:hover {
    background: linear-gradient(135deg,
        rgba(251, 191, 36, .22) 0%,
        rgba(245, 158, 11, .15) 50%,
        rgba(8, 145, 178, .1) 100%);
    border-color: #f59e0b;
    color: #78350f;
    box-shadow: 0 0 0 2px rgba(245, 158, 11, .6), 0 4px 16px rgba(245, 158, 11, .35);
    transform: translateY(-1px);
}
.ds-btn[data-dataset="__VOCAB_ID__"].active {
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 30%, #0891b2 100%);
    color: #fff;
    border-color: transparent;
    box-shadow: 0 0 0 2px rgba(245, 158, 11, .7), 0 6px 22px rgba(245, 158, 11, .5);
    text-shadow: 0 1px 2px rgba(0, 0, 0, .2);
}
.ds-btn[data-dataset="__VOCAB_ID__"].active::before {
    filter: drop-shadow(0 0 8px rgba(255, 255, 255, .9));
}
[data-theme="dark"] .ds-btn[data-dataset="__VOCAB_ID__"] {
    background: linear-gradient(135deg,
        rgba(251, 191, 36, .2) 0%,
        rgba(245, 158, 11, .14) 50%,
        rgba(8, 145, 178, .1) 100%);
    color: #fcd34d;
    border-color: rgba(245, 158, 11, .5);
}
[data-theme="dark"] .ds-btn[data-dataset="__VOCAB_ID__"].active {
    background: linear-gradient(135deg, #d97706, #b45309 30%, #0e7490);
    color: #fff;
}

.ds-btn[data-dataset="__VOCAB_ID__"] .ds-vocab-badge {
    position: absolute;
    top: -10px; right: -8px;
    padding: .2rem .5rem;
    border-radius: 50px;
    background: linear-gradient(135deg, #6366f1 0%, #7c3aed 50%, #a855f7 100%);
    color: #fff;
    font-size: .55rem;
    font-weight: 900;
    letter-spacing: .5px;
    text-transform: uppercase;
    box-shadow: 0 2px 8px rgba(124, 58, 237, .6), 0 0 0 2px var(--surface);
    animation: premiumBadgePulse 2s ease-in-out infinite;
    z-index: 10;
    pointer-events: none;
    line-height: 1.2;
    white-space: nowrap;
}
.ds-btn[data-dataset="__VOCAB_ID__"] .ds-vocab-badge::before { content: '💎 '; }
@keyframes premiumBadgePulse {
    0%, 100% { transform: scale(1); }
    50%      { transform: scale(1.1); }
}
.ds-btn[data-dataset="__VOCAB_ID__"].active .ds-vocab-badge {
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    color: #1e1b4b;
    animation: none;
}

.ds-btn[data-dataset="__VOCAB_ID__"].vocab-locked {
    background: linear-gradient(135deg, rgba(220, 38, 38, .08) 0%, rgba(251, 191, 36, .06) 100%);
    border-color: rgba(220, 38, 38, .4);
    color: #991b1b;
    opacity: .85;
}
.ds-btn[data-dataset="__VOCAB_ID__"].vocab-locked::before {
    filter: drop-shadow(0 2px 4px rgba(220, 38, 38, .6)) grayscale(.5);
    opacity: .7;
}
.ds-btn[data-dataset="__VOCAB_ID__"].vocab-locked:hover { opacity: 1; border-color: #dc2626; }
.ds-btn[data-dataset="__VOCAB_ID__"].vocab-locked .ds-vocab-badge { display: none; }
.ds-btn[data-dataset="__VOCAB_ID__"] .vocab-lock-icon {
    position: absolute;
    top: -8px; right: -6px;
    width: 22px; height: 22px;
    border-radius: 50%;
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    color: #fff;
    display: flex; align-items: center; justify-content: center;
    font-size: .62rem;
    box-shadow: 0 2px 8px rgba(220, 38, 38, .6), 0 0 0 2px var(--surface);
    z-index: 11;
    animation: lockPulse 2.5s ease-in-out infinite;
}
@keyframes lockPulse {
    0%, 100% { transform: scale(1); }
    50%      { transform: scale(1.12); }
}

/* BLOCK BO THU */
.card-radical {
    margin-top: .7rem;
    padding: .7rem .85rem;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 10px;
    display: flex; flex-direction: column; gap: .55rem;
    animation: blockIn .35s ease-out;
}
@keyframes blockIn {
    from { opacity: 0; transform: translateY(-3px); }
    to   { opacity: 1; transform: translateY(0); }
}
[data-theme="dark"] .card-radical {
    background: rgba(139, 92, 246, .08);
    border-color: rgba(139, 92, 246, .2);
}
.card-radical-label {
    display: flex; align-items: center; gap: .4rem;
    font-size: .72rem; font-weight: 800;
    color: #6d28d9; letter-spacing: .5px;
    text-transform: uppercase;
}
[data-theme="dark"] .card-radical-label { color: #c4b5fd; }
.card-radical-body { display: flex; align-items: center; gap: .75rem; }
.card-radical-box {
    width: 52px; height: 52px;
    border: 1.5px solid var(--border-strong);
    border-radius: 6px;
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-zh);
    font-size: 1.65rem; font-weight: 500;
    color: var(--text);
    flex-shrink: 0;
    background: var(--surface);
    position: relative;
}
.card-radical-box::before {
    content: '';
    position: absolute; inset: 0;
    background-image:
        linear-gradient(to right, transparent 49%, var(--border) 49%, var(--border) 51%, transparent 51%),
        linear-gradient(to bottom, transparent 49%, var(--border) 49%, var(--border) 51%, transparent 51%);
    opacity: .35; pointer-events: none; border-radius: 6px;
}
.card-radical-info {
    flex: 1; min-width: 0;
    display: flex; flex-direction: column; gap: .2rem;
}
.card-radical-name {
    font-size: .88rem; font-weight: 700;
    color: var(--text); line-height: 1.3;
}
.card-radical-name .pinyin {
    font-weight: 500; font-style: italic;
    color: #8b5cf6;
}
[data-theme="dark"] .card-radical-name .pinyin { color: #c4b5fd; }
.card-radical-meaning {
    font-size: .8rem; color: var(--text-2); line-height: 1.4;
}

/* BLOCK MEO NHO */
.card-mnemonic {
    margin-top: .7rem;
    padding: .7rem .85rem;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 10px;
    display: flex; flex-direction: column; gap: .5rem;
    animation: blockIn .35s ease-out;
}
[data-theme="dark"] .card-mnemonic {
    background: rgba(245, 158, 11, .08);
    border-color: rgba(245, 158, 11, .2);
}
.card-mnemonic-label {
    display: flex; align-items: center; gap: .4rem;
    font-size: .72rem; font-weight: 800;
    color: #b45309; letter-spacing: .5px;
    text-transform: uppercase;
}
[data-theme="dark"] .card-mnemonic-label { color: #fcd34d; }
.card-mnemonic-body {
    font-size: .84rem; color: var(--text-2);
    line-height: 1.55; white-space: pre-line;
}
.card-mnemonic-body .char-zh {
    font-family: var(--font-zh);
    font-size: 1rem; font-weight: 600;
    color: var(--text); padding: 0 .15rem;
}
.card-mnemonic-body .arrow {
    color: #f59e0b; font-weight: 800; padding: 0 .2rem;
}
.card-mnemonic-body .hint {
    color: #b45309; font-weight: 700;
}
[data-theme="dark"] .card-mnemonic-body .hint { color: #fcd34d; }

/* PINYIN HIGHLIGHT */
.pinyin-hl {
    background: linear-gradient(180deg, transparent 55%, rgba(250, 204, 21, .45) 55%);
    padding: 0 .08em; border-radius: 2px;
    color: #78350f; font-weight: 600;
}
[data-theme="dark"] .pinyin-hl {
    background: linear-gradient(180deg, transparent 55%, rgba(250, 204, 21, .3) 55%);
    color: #fde68a;
}

/* VI DU TRONG PRACTICE FULL */
.pf-vocab-example {
    margin-top: 1rem;
    padding: .85rem 1rem;
    background: linear-gradient(135deg, rgba(8, 145, 178, .08), rgba(6, 182, 212, .04));
    border-left: 4px solid #0891b2;
    border-radius: 12px;
    display: flex;
    flex-direction: column;
    gap: .5rem;
    animation: pfVocabIn .4s ease-out;
}
@keyframes pfVocabIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
[data-theme="dark"] .pf-vocab-example {
    background: linear-gradient(135deg, rgba(8, 145, 178, .18), rgba(6, 182, 212, .1));
    border-left-color: #22d3ee;
}
.pf-vocab-example-label {
    font-size: .68rem;
    font-weight: 800;
    color: #0891b2;
    text-transform: uppercase;
    letter-spacing: .5px;
    display: flex; align-items: center; gap: .4rem;
}
[data-theme="dark"] .pf-vocab-example-label { color: #22d3ee; }
.pf-vocab-example-zh {
    font-family: var(--font-zh);
    font-size: clamp(1.05rem, 2.2vw, 1.4rem);
    font-weight: 600;
    color: var(--text);
    line-height: 1.5;
    display: flex; align-items: center; gap: .5rem; flex-wrap: wrap;
}
.pf-vocab-example-zh .audio-btn-mini {
    width: 28px; height: 28px;
    border-radius: 50%; border: none;
    background: rgba(8, 145, 178, .15);
    color: #0891b2; cursor: pointer;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: .75rem; transition: all .18s;
    flex-shrink: 0;
}
.pf-vocab-example-zh .audio-btn-mini:hover {
    background: #0891b2; color: #fff;
    transform: scale(1.15);
}
.pf-vocab-example-pinyin {
    font-size: clamp(.85rem, 1.4vw, 1rem);
    font-style: italic; color: #0891b2;
    font-weight: 500; line-height: 1.4;
}
[data-theme="dark"] .pf-vocab-example-pinyin { color: #22d3ee; }
.pf-vocab-example-vi {
    font-size: clamp(.9rem, 1.5vw, 1.05rem);
    color: var(--text-2);
    line-height: 1.5; font-weight: 500;
}

/* MODAL UPGRADE */
.vocab-upgrade-modal {
    position: fixed; inset: 0;
    background: rgba(15, 23, 42, .85);
    backdrop-filter: blur(6px);
    z-index: 6000; display: none;
    align-items: center; justify-content: center;
    padding: 1rem; animation: fadeIn .2s;
}
.vocab-upgrade-modal.show { display: flex; }
.vocab-upgrade-box {
    background: var(--surface);
    border-radius: 20px;
    max-width: 460px; width: 100%;
    max-height: calc(100vh - 2rem);
    overflow-y: auto;
    box-shadow: 0 20px 60px rgba(0,0,0,.4);
    animation: upgradeIn .35s cubic-bezier(.34, 1.56, .64, 1);
    text-align: center;
}
@keyframes upgradeIn {
    from { transform: scale(.9); opacity: 0; }
    to   { transform: scale(1); opacity: 1; }
}
.vocab-upgrade-header {
    padding: 1.75rem 1.5rem 1.25rem;
    background: linear-gradient(135deg, #6366f1 0%, #7c3aed 25%, #f59e0b 75%, #d97706 100%);
    border-radius: 20px 20px 0 0;
    color: #fff; position: relative; overflow: hidden;
}
.vocab-upgrade-icon {
    width: 70px; height: 70px;
    margin: 0 auto .85rem;
    border-radius: 50%;
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem;
    box-shadow: 0 8px 24px rgba(245, 158, 11, .5);
    animation: floatUp 3s ease-in-out infinite;
}
@keyframes floatUp {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-6px); }
}
.vocab-upgrade-title {
    font-size: 1.35rem; font-weight: 900;
    margin-bottom: .35rem;
}
.vocab-upgrade-subtitle {
    font-size: .85rem; opacity: .95; line-height: 1.5;
}
.vocab-upgrade-price {
    display: inline-flex; align-items: center; gap: .4rem;
    margin-top: .85rem;
    padding: .55rem 1.15rem;
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    border: 2px solid rgba(255, 255, 255, .6);
    border-radius: 50px;
    font-weight: 900; font-size: 1.35rem; color: #fff;
    box-shadow: 0 6px 20px rgba(245, 158, 11, .6);
    animation: pricePulse 2.5s ease-in-out infinite;
}
@keyframes pricePulse {
    0%, 100% { transform: scale(1); }
    50%      { transform: scale(1.05); }
}
.vocab-upgrade-body {
    padding: 1.25rem 1.5rem;
    display: flex; flex-direction: column; gap: 1rem;
}
.vocab-upgrade-features {
    display: flex; flex-direction: column;
    gap: .55rem; text-align: left;
}
.vocab-upgrade-feature {
    display: flex; align-items: center; gap: .6rem;
    padding: .55rem .75rem;
    background: var(--surface-2);
    border-radius: 10px;
    font-size: .84rem; font-weight: 600;
    color: var(--text-2);
}
.vocab-upgrade-feature i {
    width: 24px; height: 24px;
    border-radius: 50%;
    background: rgba(8, 145, 178, .15);
    color: #0891b2;
    display: flex; align-items: center; justify-content: center;
    font-size: .75rem; flex-shrink: 0;
}
.vocab-upgrade-feature.highlight {
    background: linear-gradient(135deg, rgba(251, 191, 36, .15), rgba(245, 158, 11, .08));
    color: #92400e;
    border: 1.5px solid rgba(245, 158, 11, .4);
}
.vocab-upgrade-feature.highlight i {
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    color: #fff;
}
.vocab-upgrade-actions {
    display: flex; gap: .55rem; flex-wrap: wrap;
}
.vocab-upgrade-btn {
    flex: 1 1 160px;
    padding: .85rem 1rem;
    border-radius: 12px; border: none;
    font-size: .9rem; font-weight: 800;
    font-family: inherit; cursor: pointer;
    display: inline-flex; align-items: center; justify-content: center;
    gap: .45rem; transition: all .2s;
}
.vocab-upgrade-btn.primary {
    background: linear-gradient(135deg, #fbbf24, #f59e0b 50%, #ea580c);
    color: #fff;
    box-shadow: 0 6px 18px rgba(245, 158, 11, .5);
}
.vocab-upgrade-btn.primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 26px rgba(245, 158, 11, .7);
}
.vocab-upgrade-btn.secondary {
    background: var(--surface-2);
    color: var(--text-2);
    border: 1.5px solid var(--border);
}
.vocab-upgrade-btn.secondary:hover {
    border-color: var(--primary);
    color: var(--primary);
}

@media (max-width: 500px) {
    .ds-btn[data-dataset="__VOCAB_ID__"] { padding-left: 2.2rem; }
    .ds-btn[data-dataset="__VOCAB_ID__"]::before { font-size: 1rem; left: .5rem; }
    .card-radical, .card-mnemonic { padding: .6rem .7rem; margin-top: .6rem; }
    .card-radical-box { width: 46px; height: 46px; font-size: 1.45rem; }
    .card-mnemonic-body { font-size: .78rem; }
    .vocab-upgrade-icon { width: 60px; height: 60px; font-size: 1.65rem; }
    .vocab-upgrade-title { font-size: 1.15rem; }
    .vocab-upgrade-price { font-size: 1.15rem; }
    .pf-vocab-example { padding: .7rem .85rem; margin-top: .85rem; }
    .pf-vocab-example-zh { font-size: 1rem; }
    .pf-vocab-example-pinyin { font-size: .8rem; }
    .pf-vocab-example-vi { font-size: .85rem; }
}
"""
    return css.replace("__VOCAB_ID__", vocab_id)


def build_vocab_tab_html(vocab_id="tu-vung", label="Từ vựng HSK"):
    return (
        '\n        <button class="ds-btn ds-btn-primary" '
        'data-dataset="' + vocab_id + '" id="dsTuVungBtn">\n'
        '            <i class="fas fa-book"></i>\n'
        '            <span id="dsTuVungLabel">' + label + '</span>\n'
        '            <span class="ds-vocab-badge" id="dsVocabBadge">PREMIUM</span>\n'
        '        </button>'
    )


def build_vocab_modal_html():
    return r'''
<div class="vocab-upgrade-modal" id="vocabUpgradeModal">
    <div class="vocab-upgrade-box">
        <div class="vocab-upgrade-header">
            <div class="vocab-upgrade-icon">👑</div>
            <div class="vocab-upgrade-title" id="vocabUpgradeTitle">Mở khóa Từ vựng HSK</div>
            <div class="vocab-upgrade-subtitle" id="vocabUpgradeSubtitle">
                Dành riêng cho thành viên Premium
            </div>
            <div class="vocab-upgrade-price">💎 1.000.000đ</div>
        </div>
        <div class="vocab-upgrade-body">
            <div class="vocab-upgrade-features">
                <div class="vocab-upgrade-feature">
                    <i class="fas fa-book"></i>
                    <span>Toàn bộ từ vựng HSK 1–9 (~11700 từ)</span>
                </div>
                <div class="vocab-upgrade-feature">
                    <i class="fas fa-lightbulb"></i>
                    <span>Mẹo nhớ chữ Hán chi tiết</span>
                </div>
                <div class="vocab-upgrade-feature">
                    <i class="fas fa-pen-fancy"></i>
                    <span>Phân tích bộ thủ từng chữ</span>
                </div>
                <div class="vocab-upgrade-feature">
                    <i class="fas fa-quote-left"></i>
                    <span>Câu ví dụ + phiên âm + nghĩa</span>
                </div>
                <div class="vocab-upgrade-feature highlight">
                    <i class="fas fa-crown"></i>
                    <span><b>Gói Premium — Sở hữu vĩnh viễn</b></span>
                </div>
            </div>
            <div class="vocab-upgrade-actions" id="vocabUpgradeActions"></div>
        </div>
    </div>
</div>
'''
def build_vocab_js_override(vocab_id="tu-vung"):
    js = r"""
/* VOCAB PREMIUM MODULE */
(function() {
    'use strict';

    var VOCAB_ID = '__VOCAB_ID__';
    var _done = new WeakSet();

    function canAccessVocab() {
        if (typeof currentUser === 'undefined' || !currentUser) return false;
        if (currentUser.role === 'admin') return true;
        if (currentUser.isPermanent === true) return true;
        return false;
    }

    function _esc(s) {
        return (typeof escapeHtml === 'function')
            ? escapeHtml(s) : String(s == null ? '' : s);
    }

    function _isVocabMode() {
        return (typeof CURRENT_DATASET !== 'undefined') && CURRENT_DATASET === VOCAB_ID;
    }

    function _findRecord(stt) {
        if (stt == null) return null;
        var s = String(stt);
        if (window.FIXPY_DATASETS && window.FIXPY_DATASETS[VOCAB_ID]) {
            var list = window.FIXPY_DATASETS[VOCAB_ID].data || [];
            for (var i = 0; i < list.length; i++) {
                if (String(list[i].stt) === s) return list[i];
            }
        }
        if (typeof RAW_DATA !== 'undefined' && RAW_DATA) {
            for (var j = 0; j < RAW_DATA.length; j++) {
                if (String(RAW_DATA[j].stt) === s) return RAW_DATA[j];
            }
        }
        return null;
    }

    function updateTabLockState() {
        var btn = document.querySelector('.ds-btn[data-dataset="' + VOCAB_ID + '"]');
        if (!btn) return;
        var can = canAccessVocab();
        var oldLock = btn.querySelector('.vocab-lock-icon');
        if (oldLock) oldLock.remove();

        if (can) {
            btn.classList.remove('vocab-locked');
            btn.title = 'Tu vung HSK 1-9 - Premium (da mo khoa)';
        } else {
            btn.classList.add('vocab-locked');
            btn.title = 'Tu vung HSK - Chi danh cho Premium (1.000.000d)';
            var lock = document.createElement('i');
            lock.className = 'fas fa-lock vocab-lock-icon';
            btn.appendChild(lock);
        }
    }

    function openUpgradeModal() {
        var modal = document.getElementById('vocabUpgradeModal');
        if (!modal) return;
        var titleEl = document.getElementById('vocabUpgradeTitle');
        var subEl = document.getElementById('vocabUpgradeSubtitle');
        var actionsEl = document.getElementById('vocabUpgradeActions');

        var tier = 'demo';
        if (typeof currentUser !== 'undefined' && currentUser) {
            if (currentUser.isTrial || currentUser.tier === 'trial') tier = 'trial';
            else if (currentUser.isExpiredOnly || currentUser.tier === 'expired') tier = 'expired';
            else tier = 'active';
        }

        if (tier === 'demo') {
            if (titleEl) titleEl.textContent = 'Dang nhap de mua Premium';
            if (subEl) subEl.textContent = 'Goi Premium 1 trieu - Mo khoa Tu vung HSK vinh vien';
            if (actionsEl) {
                actionsEl.innerHTML =
                    '<button class="vocab-upgrade-btn primary" onclick="vocabUpgradeLogin()">' +
                        '<i class="fas fa-sign-in-alt"></i> Dang nhap' +
                    '</button>' +
                    '<button class="vocab-upgrade-btn secondary" onclick="vocabUpgradeClose()">' +
                        'De sau' +
                    '</button>';
            }
        } else if (tier === 'trial') {
            if (titleEl) titleEl.textContent = 'Nang cap len Premium';
            if (subEl) subEl.textContent = 'So huu Tu vung HSK vinh vien voi goi Premium';
            if (actionsEl) {
                actionsEl.innerHTML =
                    '<button class="vocab-upgrade-btn primary" onclick="vocabUpgradeRenew()">' +
                        '<i class="fas fa-crown"></i> Mua Premium 1 trieu' +
                    '</button>' +
                    '<button class="vocab-upgrade-btn secondary" onclick="vocabUpgradeClose()">' +
                        'De sau' +
                    '</button>';
            }
        } else if (tier === 'expired') {
            if (titleEl) titleEl.textContent = 'Tai khoan da het han';
            if (subEl) subEl.textContent = 'Mua goi Premium 1 trieu de so huu vinh vien';
            if (actionsEl) {
                actionsEl.innerHTML =
                    '<button class="vocab-upgrade-btn primary" onclick="vocabUpgradeRenew()">' +
                        '<i class="fas fa-crown"></i> Mua Premium 1 trieu' +
                    '</button>' +
                    '<button class="vocab-upgrade-btn secondary" onclick="vocabUpgradeClose()">' +
                        'De sau' +
                    '</button>';
            }
        } else {
            if (titleEl) titleEl.textContent = 'Nang cap len Premium';
            if (subEl) subEl.textContent = 'Chi goi Premium moi mo duoc Tu vung HSK';
            if (actionsEl) {
                actionsEl.innerHTML =
                    '<button class="vocab-upgrade-btn primary" onclick="vocabUpgradeRenew()">' +
                        '<i class="fas fa-crown"></i> Nang cap Premium 1 trieu' +
                    '</button>' +
                    '<button class="vocab-upgrade-btn secondary" onclick="vocabUpgradeClose()">' +
                        'De sau' +
                    '</button>';
            }
        }

        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    function closeUpgradeModal() {
        var modal = document.getElementById('vocabUpgradeModal');
        if (modal) modal.classList.remove('show');
        document.body.style.overflow = '';
    }

    window.vocabUpgradeClose = closeUpgradeModal;
    window.vocabUpgradeLogin = function() {
        closeUpgradeModal();
        if (typeof showLoginModal === 'function') showLoginModal();
    };
    window.vocabUpgradeRenew = function() {
        closeUpgradeModal();
        if (typeof openRenewalModal === 'function') {
            openRenewalModal();
            setTimeout(function() {
                if (typeof selectPackage === 'function') selectPackage('forever');
            }, 300);
        }
    };

    document.addEventListener('click', function(e) {
        var modal = document.getElementById('vocabUpgradeModal');
        if (!modal || !modal.classList.contains('show')) return;
        if (e.target === modal) closeUpgradeModal();
    });
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            var modal = document.getElementById('vocabUpgradeModal');
            if (modal && modal.classList.contains('show')) closeUpgradeModal();
        }
    });

    function highlightPinyin(text) {
        if (!text) return '';
        return text.replace(
            /[a-zA-ZàáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴĐāáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜ]+/g,
            function(w) { return '<span class="pinyin-hl">' + w + '</span>'; }
        );
    }

    function buildRadicalBlock(radical) {
        if (!radical) return '';
        var zh = _esc(radical.zh || '');
        var py = _esc(radical.pinyin || '');
        var st = _esc(radical.strokes || '');
        var mean = _esc(radical.meaning || '');

        var nameLine = '';
        if (zh) {
            nameLine = '<span class="char">' + zh + '</span>';
            if (py) nameLine += ' <span class="pinyin">(' + py + ')</span>';
            if (st) nameLine += ' - ' + st + ' net';
        }

        var html = '<div class="card-radical">';
        html += '<div class="card-radical-label">BỘ THỦ</div>';
        html += '<div class="card-radical-body">';
        if (zh) html += '<div class="card-radical-box">' + zh + '</div>';
        html += '<div class="card-radical-info">';
        if (nameLine) html += '<div class="card-radical-name">' + nameLine + '</div>';
        if (mean) html += '<div class="card-radical-meaning">' + mean + '</div>';
        html += '</div></div></div>';
        return html;
    }

    function buildMnemonicBlock(text) {
        if (!text || !text.trim()) return '';
        var safe = _esc(text);
        safe = safe.replace(/([\u4e00-\u9fa5]+)/g, '<span class="char-zh">$1</span>');
        safe = safe.replace(/\s=\s/g, ' <span class="arrow">=</span> ');
        safe = safe.replace(/→/g, '<span class="arrow">→</span>');
        safe = safe.replace(/\(([^)]+)\)/g, '(<span class="hint">$1</span>)');
        return '<div class="card-mnemonic">'
            + '<div class="card-mnemonic-label">MẸO NHỚ</div>'
            + '<div class="card-mnemonic-body">' + safe + '</div>'
            + '</div>';
    }

    function enhanceCards() {
        if (!_isVocabMode()) return;
        if (!canAccessVocab()) return;

        var cards = document.querySelectorAll('.card[data-stt]');
        cards.forEach(function(card) {
            if (_done.has(card)) return;
            _done.add(card);

            var r = _findRecord(card.dataset.stt);
            if (!r) return;

            var body = card.querySelector('.card-body');
            if (!body) return;

            var oldR = body.querySelector('.card-radical');
            if (oldR) oldR.remove();
            var oldM = body.querySelector('.card-mnemonic');
            if (oldM) oldM.remove();

            var anchor = body.querySelector('.card-vocab-example');
            if (r.radical) {
                var htmlR = buildRadicalBlock(r.radical);
                if (anchor) anchor.insertAdjacentHTML('beforebegin', htmlR);
                else body.insertAdjacentHTML('beforeend', htmlR);
            }

            if (r.mnemonic) {
                body.insertAdjacentHTML('beforeend', buildMnemonicBlock(r.mnemonic));
            }

            var pyEl = body.querySelector('.card-vocab-example-pinyin')
                    || body.querySelector('.card-pinyin');
            if (pyEl && !pyEl.dataset.hlDone) {
                pyEl.dataset.hlDone = '1';
                pyEl.innerHTML = highlightPinyin(pyEl.textContent);
            }
        });
    }

    function setupObserver() {
        var wrapper = document.getElementById('mobileWrapper');
        if (!wrapper) { setTimeout(setupObserver, 400); return; }
        var timer = null;
        var observer = new MutationObserver(function() {
            if (timer) clearTimeout(timer);
            timer = setTimeout(enhanceCards, 80);
        });
        observer.observe(wrapper, { childList: true, subtree: true });
        enhanceCards();
    }

    function bindTabIfNeeded() {
        var btn = document.querySelector('.ds-btn[data-dataset="' + VOCAB_ID + '"]');
        if (!btn || btn.__vocabPremiumBound) return;

        btn.__fixPyBound = true;
        btn.__vocabPremiumBound = true;

        btn.addEventListener('click', function(e) {
            e.stopImmediatePropagation();
            e.stopPropagation();
            e.preventDefault();

            if (!canAccessVocab()) {
                console.log('[vocab] khong co quyen - mo modal');
                openUpgradeModal();
                return;
            }

            console.log('[vocab] co quyen - switch to tu-vung');

            var sub = document.getElementById('dsSubWrap');
            if (sub) sub.style.display = 'none';

            document.querySelectorAll('.ds-btn, .ds-sub-btn').forEach(function(b) {
                b.classList.remove('active');
            });
            this.classList.add('active');

            if (typeof window.__switchRawData === 'function') {
                window.__switchRawData(VOCAB_ID);
            }

            if (typeof state !== 'undefined' && state) {
                state.search = '';
                state.hsk = '';
                state.subject = '';
            }
            try {
                var si = document.getElementById('searchInput');
                var hf = document.getElementById('hskFilter');
                var sf = document.getElementById('subjectFilter');
                if (si) si.value = '';
                if (hf) hf.value = '';
                if (sf) sf.value = '';
                var cb = document.getElementById('clearSearchBtn');
                if (cb) cb.classList.remove('show');
            } catch(err) {}

            try {
                if (typeof buildFilters === 'function') buildFilters();
                if (typeof applyFilter === 'function') applyFilter();
                if (typeof updateResultCount === 'function') updateResultCount();
            } catch(err) {
                console.warn('[vocab] re-render error:', err);
            }

            document.querySelectorAll('.ds-btn, .ds-sub-btn').forEach(function(b) {
                b.classList.remove('active');
            });
            this.classList.add('active');

            setTimeout(function() {
                var mainEl = document.getElementById('mainContent');
                if (mainEl) {
                    var yOffset = mainEl.getBoundingClientRect().top + window.scrollY - 100;
                    window.scrollTo({ top: yOffset, behavior: 'smooth' });
                }
            }, 100);

            setTimeout(enhanceCards, 300);

        }, true);

        console.log('[vocab] bound tab click');
    }

    function hookPracticeFull() {
    if (typeof window.loadPracticeFull !== 'function') {
        return false;
    }
    if (window.loadPracticeFull.__vocabHooked) return true;

    var orig = window.loadPracticeFull;
    window.loadPracticeFull = function(stt) {
        // Gọi hàm gốc trước
        var result = orig.apply(this, arguments);

        // Sau đó override
        if (_isVocabMode() && canAccessVocab()) {
            var r = _findRecord(stt);
            if (r && r.vi_du_zh) {
                // Ghi đè biến toàn cục
                try {
                    if (typeof window.pfCurrentAnswer !== 'undefined') {
                        window.pfCurrentAnswer = r.vi_du_zh;
                    }
                    if (typeof window.pfCurrentVi !== 'undefined') {
                        window.pfCurrentVi = r.vi_du_vi;
                    }
                    if (typeof window.pfCurrentPinyin !== 'undefined') {
                        window.pfCurrentPinyin = r.vi_du_pinyin;
                    }
                } catch(e) {}

                // ĐỔI NGAY — không chờ setTimeout
                var pfViEl = document.getElementById('pfVi');
                if (pfViEl && r.vi_du_vi) {
                    pfViEl.textContent = r.vi_du_vi;
                }

                // Reset input + preview + status (dùng setTimeout ngắn)
                setTimeout(function() {
                    var pfInput = document.getElementById('pfInput');
                    if (pfInput) pfInput.value = '';

                    var pfPreview = document.getElementById('pfPreview');
                    if (pfPreview) pfPreview.innerHTML = '';

                    var pfStatus = document.getElementById('pfStatus');
                    if (pfStatus) {
                        pfStatus.textContent = '';
                        pfStatus.className = 'practice-full-status';
                    }

                    // Xóa block ví dụ cũ
                    var oldExample = document.querySelector('.pf-vocab-example');
                    if (oldExample) oldExample.remove();

                    // ⭐ Hook nút GỢI Ý (không phải Xem đáp án)
                    var hintBtn = document.getElementById('pfHintBtn');
                    if (hintBtn && !hintBtn.__vocabHooked) {
                        hintBtn.__vocabHooked = true;
                        hintBtn.addEventListener('click', function(ev) {
                            setTimeout(function() {
                                if (!_isVocabMode()) return;
                                if (!canAccessVocab()) return;

                                // Xóa block cũ
                                var oldEx = document.querySelector('.pf-vocab-example');
                                if (oldEx) oldEx.remove();

                                // Nếu nút Gợi ý TẮT → không hiện
                                if (!hintBtn.classList.contains('active')) {
                                    return;
                                }

                                var currentStt = null;
                                try { currentStt = window.pfCurrentStt; } catch(e) {}
                                if (!currentStt) return;

                                var rec = _findRecord(currentStt);
                                if (!rec || !rec.vi_du_zh) return;

                                var answerEl = document.getElementById('pfAnswer');
                                if (!answerEl) return;

                                var html = buildPFExampleBlock(rec);
                                if (html) {
                                    answerEl.insertAdjacentHTML('afterend', html);
                                }
                            }, 100);
                        });
                    }
                }, 50);
            }
        }

        return result;
    };
    window.loadPracticeFull.__vocabHooked = true;
    console.log('[vocab] hooked loadPracticeFull');
    return true;
}

    function buildPFExampleBlock(r) {
        var zh = _esc(r.vi_du_zh || '');
        if (!zh) return '';

        var zhJs = (typeof escapeJs === 'function')
            ? escapeJs(r.vi_du_zh || '') : '';
        var pinyin = _esc(r.vi_du_pinyin || '');
        var vi = _esc(r.vi_du_vi || '');

        var html = '<div class="pf-vocab-example">';
        html += '<div class="pf-vocab-example-label">📝 Ví dụ minh họa</div>';
        html += '<div class="pf-vocab-example-zh">' + zh;
        if (zhJs && typeof speakText === 'function') {
            html += ' <button class="audio-btn-mini" onclick="speakText(\'' + zhJs + '\', this, event)" title="Nghe"><i class="fas fa-volume-up"></i></button>';
        }
        html += '</div>';
        if (pinyin) html += '<div class="pf-vocab-example-pinyin">' + highlightPinyin(pinyin) + '</div>';
        if (vi) html += '<div class="pf-vocab-example-vi">' + vi + '</div>';
        html += '</div>';
        return html;
    }

    var _lastTier = null;
    function watchTier() {
        var key = '';
        if (typeof currentUser !== 'undefined' && currentUser) {
            key = (currentUser.role || 'user') + '|'
                + (currentUser.isPermanent ? '1' : '0') + '|'
                + (currentUser.isTrial ? '1' : '0') + '|'
                + (currentUser.isExpiredOnly ? '1' : '0');
        } else {
            key = 'guest';
        }
        if (key !== _lastTier) {
            _lastTier = key;
            updateTabLockState();
            bindTabIfNeeded();
        }
    }
    // ⭐ Fix bug "nhảy từ" khi mở full màn hình
function setupPfViWatcher() {
    var pfViEl = document.getElementById('pfVi');
    if (!pfViEl) return;
    if (pfViEl.__vocabWatched) return;
    pfViEl.__vocabWatched = true;

    var observer = new MutationObserver(function() {
        if (!_isVocabMode()) return;
        if (!canAccessVocab()) return;

        var stt = null;
        try { stt = window.pfCurrentStt; } catch(e) {}
        if (!stt) return;

        var r = _findRecord(stt);
        if (!r || !r.vi_du_vi) return;

        var currentText = pfViEl.textContent.trim();
        if (currentText !== r.vi_du_vi) {
            pfViEl.textContent = r.vi_du_vi;
        }
    });

    observer.observe(pfViEl, {
        childList: true,
        characterData: true,
        subtree: true
    });

    console.log('[vocab] pfVi watcher setup');
}

    function init() {
    bindTabIfNeeded();
    updateTabLockState();
    setupObserver();
    setInterval(watchTier, 1000);

    var tries = 0;
    var t = setInterval(function() {
        tries++;
        if (hookPracticeFull() || tries > 20) clearInterval(t);
    }, 250);
    hookPracticeFull();

    // Setup watcher cho pfVi
    setTimeout(setupPfViWatcher, 1000);
    setInterval(setupPfViWatcher, 2000);

    console.log('[vocab] module ready');
}

})();
"""
    return js.replace("__VOCAB_ID__", vocab_id)

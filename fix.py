# -*- coding: utf-8 -*-
"""
fix.py — Auto-scan data/ và thêm MỌI file Excel thành tab riêng.

ĐẶC ĐIỂM:
  - Đọc HẾT mọi file .xlsx/.xls/.csv trong data/
  - Tên tab = tên file (normalize NFC — hiển thị đúng dấu tiếng Việt)
  - Logic đọc Excel GIỐNG data_reader.py:
      openpyxl, cột VỊ TRÍ: 0=STT, 1=HSK, 2=Topic, 3=Subject, 4=Vi, 5=Zh, 6=Pinyin
      Data bắt đầu từ dòng 2, tự động chuyển số Ả Rập → Hán (cn2an)
  - TÍCH HỢP TIER LOCK giống tab tổng hợp:
      + Click tab mới → gọi switchDataset() → applyFilter() → getLimitedData()
      + Demo/Trial/Expired tự động cắt câu theo APP_LIMITS
      + Active/Admin xem full
  - KHÔNG can thiệp convert.py, ui_template.py, config.json
  - KHÔNG override APP_TIER/APP_LIMITS/publishTierState

Cách chạy:
    python scripts/convert.py    # Tạo index.html gốc
    python fix.py                # Patch index.html — thêm tab từ data/
"""
import json
import os
import re
import sys
import glob
import unicodedata

import openpyxl


# =================================================================
#  CONFIG
# =================================================================
INDEX_HTML = "index.html"
CONFIG_JSON = "config.json"
DATA_DIR = "data"

# Neu fix.py chay tu scripts/, tu nhay ra root
if not os.path.isfile(CONFIG_JSON) and os.path.isfile(os.path.join("..", CONFIG_JSON)):
    os.chdir("..")
    print("[fix.py] Phat hien chay tu scripts/ -> chuyen ve root")

TAB_ICONS = [
    "fa-comments", "fa-file-alt", "fa-book", "fa-graduation-cap",
    "fa-star", "fa-fire", "fa-bolt", "fa-rocket",
]
TAB_COLORS = [
    "#0891b2", "#dc2626", "#059669", "#d97706",
    "#7c3aed", "#db2777", "#0284c7", "#65a30d",
]


# =================================================================
#  CHUYEN SO A RAP -> SO HAN (copy tu data_reader.py)
# =================================================================
try:
    import cn2an
    HAS_CN2AN = True
except ImportError:
    HAS_CN2AN = False
    print("[fix.py] Khong co cn2an - so A Rap giu nguyen")

_CN_DIGITS = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九']
_CN_UNITS = ['', '十', '百', '千']


def _num_to_chinese_basic(num):
    if num == 0:
        return '零'
    if num < 0:
        return '负' + _num_to_chinese_basic(-num)
    result = ''
    unit_idx = 0
    n = num
    while n > 0:
        digit = n % 10
        if digit != 0:
            if not (unit_idx == 1 and digit == 1 and n < 20 and result == ''):
                result = _CN_DIGITS[digit] + _CN_UNITS[unit_idx] + result
            else:
                result = _CN_UNITS[unit_idx] + result
        else:
            if result and not result.startswith('零'):
                result = '零' + result
        n //= 10
        unit_idx += 1
    if result.startswith('一十'):
        result = result[1:]
    return result


def _num_to_chinese(num):
    if HAS_CN2AN:
        try:
            return cn2an.an2cn(num)
        except Exception:
            pass
    return _num_to_chinese_basic(num)


def _digits_to_chinese(digits_str):
    return ''.join([_CN_DIGITS[int(d)] for d in digits_str])


def convert_arabic_to_chinese(text):
    """Chuyen so A Rap -> so Han (giong data_reader.py)."""
    if not text or not isinstance(text, str):
        return text

    def replace_percent(match):
        num_str = match.group(1)
        if '.' in num_str:
            parts = num_str.split('.')
            int_part = _num_to_chinese(int(parts[0]))
            dec_part = _digits_to_chinese(parts[1])
            return '百分之' + int_part + '点' + dec_part
        return '百分之' + _num_to_chinese(int(num_str))

    text = re.sub(r'(\d+(?:\.\d+)?)%', replace_percent, text)

    def replace_decimal(match):
        num_str = match.group(0)
        parts = num_str.split('.')
        int_part = _num_to_chinese(int(parts[0]))
        dec_part = _digits_to_chinese(parts[1])
        return int_part + '点' + dec_part

    text = re.sub(
        r'(?<![A-Za-z\-\.])\d+\.\d+(?![A-Za-z])',
        replace_decimal, text
    )

    def replace_int(match):
        return _num_to_chinese(int(match.group(0)))

    text = re.sub(
        r'(?<![A-Za-z\-\.])\d+(?![A-Za-z]|\.\d)',
        replace_int, text
    )

    return text


def _clean(s):
    if s is None:
        return ""
    return (str(s).replace('\n', ' ').replace('\r', ' ')
            .replace('\t', ' ').replace('\\', '\\\\'))


# =================================================================
#  HELPERS
# =================================================================
def _slugify(filename):
    base = filename.rsplit(".", 1)[0]
    base = unicodedata.normalize("NFD", base)
    base = "".join(c for c in base if unicodedata.category(c) != "Mn")
    base = base.replace("đ", "d").replace("Đ", "D")
    return re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower() or "dataset"


def _display_name(filename):
    name = filename.rsplit(".", 1)[0].replace("_", " ").strip()
    name = unicodedata.normalize("NFC", name)
    if name.islower() or name.isupper():
        name = name.title()
    return name


def _escape_json_for_script(obj):
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s.replace("</", "<\\/")


def _js_str(s):
    if s is None:
        return ""
    return (str(s)
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("'", "\\'")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("</", "<\\/"))


def _find_file_safe(filepath):
    if os.path.isfile(filepath):
        return filepath
    dirname = os.path.dirname(filepath) or "."
    basename = os.path.basename(filepath)
    if not os.path.isdir(dirname):
        return None
    variants = set()
    variants.add(basename)
    variants.add(unicodedata.normalize("NFC", basename))
    variants.add(unicodedata.normalize("NFD", basename))
    try:
        for fname in os.listdir(dirname):
            fname_nfc = unicodedata.normalize("NFC", fname)
            fname_nfd = unicodedata.normalize("NFD", fname)
            for variant in variants:
                if (fname == variant
                        or fname_nfc == unicodedata.normalize("NFC", variant)
                        or fname_nfd == unicodedata.normalize("NFD", variant)):
                    return os.path.join(dirname, fname)
    except Exception:
        pass
    return None


def _read_excel_rows(filepath):
    """Doc Excel -> list[dict] - GIONG data_reader.read_excel()."""
    real_path = _find_file_safe(filepath)
    if not real_path:
        print("      [X] Khong tim thay file: " + os.path.basename(filepath))
        return []

    try:
        wb = openpyxl.load_workbook(real_path, data_only=True)
    except Exception as e:
        print("      [X] Loi load: " + type(e).__name__ + ": " + str(e))
        return []

    try:
        ws = wb.worksheets[0]
    except Exception as e:
        print("      [X] Loi sheet: " + str(e))
        return []

    print("      Sheet: " + ws.title
          + " - " + str(ws.max_row) + " dong, "
          + str(ws.max_column) + " cot")

    COL_STT = 0
    COL_HSK = 1
    COL_TOPIC = 2
    COL_SUBJECT = 3
    COL_VI = 4
    COL_ZH = 5
    COL_PINYIN = 6
    DATA_START = 2

    rows = []
    converted_count = 0
    skipped_empty = 0

    for row in ws.iter_rows(min_row=DATA_START, values_only=True):
        if not row or len(row) <= max(COL_VI, COL_ZH):
            skipped_empty += 1
            continue

        stt_val = row[COL_STT] if COL_STT < len(row) and row[COL_STT] is not None else ""
        hsk = _clean(row[COL_HSK]) if COL_HSK < len(row) else ""
        topic = _clean(row[COL_TOPIC]) if COL_TOPIC < len(row) else ""
        subject = _clean(row[COL_SUBJECT]) if COL_SUBJECT < len(row) else ""
        vi = _clean(row[COL_VI]) if COL_VI < len(row) else ""
        zh = _clean(row[COL_ZH]) if COL_ZH < len(row) else ""
        pinyin = _clean(row[COL_PINYIN]) if COL_PINYIN < len(row) else ""

        if not vi and not zh:
            skipped_empty += 1
            continue

        zh_original = zh
        zh = convert_arabic_to_chinese(zh)
        if zh != zh_original:
            converted_count += 1

        rows.append({
            "stt": str(stt_val),
            "hsk": hsk,
            "topic": topic,
            "subject": subject,
            "vi": vi,
            "zh": zh,
            "pinyin": pinyin,
        })

    print("      [OK] " + str(len(rows)) + " cau (bo qua "
          + str(skipped_empty) + " dong rong)")
    if converted_count > 0:
        print("      [OK] Chuyen so A Rap -> Han: " + str(converted_count) + " cau")

    return rows


# =================================================================
#  SCAN data/
# =================================================================
def scan_data_dir():
    if not os.path.isdir(DATA_DIR):
        print("[fix.py] Khong thay thu muc '" + DATA_DIR + "/' - bo qua.")
        return []

    files = []
    for ext in ("*.xlsx", "*.xls", "*.csv"):
        files.extend(glob.glob(os.path.join(DATA_DIR, ext)))
    files = sorted(set(files))

    if not files:
        print("[fix.py] Khong co file Excel trong '" + DATA_DIR + "/'")
        return []

    print("")
    print("[fix.py] Quet '" + DATA_DIR + "/' - " + str(len(files)) + " file")

    datasets = []
    used_ids = set()

    for filepath in files:
        fname = os.path.basename(filepath)

        if fname.startswith("~$"):
            print("   [skip] " + fname + " - file tam")
            continue

        print("   [file] " + fname)
        rows = _read_excel_rows(filepath)
        if not rows:
            print("   [!] " + fname + " - rong hoac loi, bo qua")
            continue

        base_id = _slugify(fname)
        dataset_id = base_id
        counter = 2
        while dataset_id in used_ids:
            dataset_id = base_id + "-" + str(counter)
            counter += 1
        used_ids.add(dataset_id)

        idx = len(datasets)
        icon = TAB_ICONS[idx % len(TAB_ICONS)]
        color = TAB_COLORS[idx % len(TAB_COLORS)]

        display = _display_name(fname)
        datasets.append({
            "id": dataset_id,
            "name": display,
            "icon": icon,
            "color": color,
            "data": rows,
            "count": len(rows),
            "source": fname,
            "type": "main",
        })
        print("   [OK] " + fname + " -> tab '" + display
              + "' (" + str(len(rows)) + " cau)")

    return datasets


# =================================================================
#  MAIN
# =================================================================
def main():
    print("=" * 62)
    print("[fix.py] Auto-scan data/ -> them tab rieng cho moi file")
    print("=" * 62)

    if not os.path.isfile(INDEX_HTML):
        print("[X] Khong thay " + INDEX_HTML + ". Chay convert.py truoc.")
        sys.exit(1)

    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    datasets = scan_data_dir()

    if not datasets:
        print("")
        print("[fix.py] Khong co dataset nao. Giu nguyen index.html.")
        return

    new_datasets = []
    for ds in datasets:
        marker1 = '"id":"' + ds["id"] + '"'
        marker2 = "'id': '" + ds["id"] + "'"
        marker3 = 'data-dataset="' + ds["id"] + '"'
        if marker1 in html or marker2 in html or marker3 in html:
            print("   [skip] '" + ds["id"] + "' da co trong HTML")
        else:
            new_datasets.append(ds)

    if not new_datasets:
        print("")
        print("[fix.py] Tat ca dataset da co - khong can patch.")
        return

    print("")
    print("[fix.py] Se them " + str(len(new_datasets)) + " tab:")
    for ds in new_datasets:
        print("   - " + ds["name"] + " (" + str(ds["count"]) + " cau)")

    # =============================================================
    #  PATCH 1: DATASET_REGISTRY
    # =============================================================
    print("")
    print("[PATCH 1] Inject vao DATASET_REGISTRY...")
    pat_registry = re.compile(r'(var\s+DATASET_REGISTRY\s*=\s*)(\{)', re.MULTILINE)
    if not pat_registry.search(html):
        print("[X] Khong tim thay DATASET_REGISTRY")
        sys.exit(1)

    inject = ""
    for ds in new_datasets:
        inject += '"' + ds["id"] + '":' + _escape_json_for_script(ds) + ','

    html, n = pat_registry.subn(r'\1\2' + inject, html, count=1)
    if n == 0:
        print("[X] Khong chen duoc registry")
        sys.exit(1)
    print("   [OK] Da chen " + str(len(new_datasets)) + " entry")

    # =============================================================
    #  PATCH 2: Buttons
    # =============================================================
    print("")
    print("[PATCH 2] Them button tabs...")
    new_btns = ""
    for ds in new_datasets:
        label = ds["name"] + " · " + str(ds["count"]) + " cau"
        new_btns += (
            '\n        <button class="ds-btn ds-btn-primary" '
            'data-dataset="' + ds["id"] + '">\n'
            '            <i class="fas ' + ds["icon"] + '"></i>\n'
            '            <span>' + _js_str(label) + '</span>\n'
            '        </button>\n    '
        )

    pat_btn = re.compile(
        r'(\s*)(<button\s+class="[^"]*ds-btn[^"]*"\s+[^>]*data-dataset-group="chuyen-nganh")',
        re.MULTILINE
    )
    html, n = pat_btn.subn(r'\1' + new_btns + r'\2', html, count=1)
    if n == 0:
        print("[X] Khong tim thay nut chuyen-nganh")
        sys.exit(1)
    print("   [OK] Da chen " + str(len(new_datasets)) + " button")

    # =============================================================
    #  PATCH 3: CSS layout (dung list + join, tranh loi escape)
    # =============================================================
    print("")
    print("[PATCH 3] CSS layout...")

    css_lines = []
    css_lines.append("")
    css_lines.append("/* ==== FIX.PY: AUTO-FIT LAYOUT CHO N TAB ==== */")
    css_lines.append("@media (max-width: 768px) {")
    css_lines.append("    .ds-main-row {")
    css_lines.append("        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;")
    css_lines.append("        gap: .5rem !important;")
    css_lines.append("    }")
    css_lines.append("}")
    css_lines.append("@media (min-width: 769px) and (max-width: 1100px) {")
    css_lines.append("    .ds-main-row {")
    css_lines.append("        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;")
    css_lines.append("        gap: .55rem !important;")
    css_lines.append("    }")
    css_lines.append("}")
    css_lines.append("@media (min-width: 1101px) {")
    css_lines.append("    .ds-main-row {")
    css_lines.append("        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) !important;")
    css_lines.append("        gap: .6rem !important;")
    css_lines.append("    }")
    css_lines.append("}")

    for ds in new_datasets:
        c = ds["color"]
        i = ds["id"]
        sel = '.ds-btn[data-dataset="' + i + '"]'
        css_lines.append("")
        css_lines.append(sel + " {")
        css_lines.append("    background: linear-gradient(135deg,")
        css_lines.append("        color-mix(in srgb, " + c + " 12%, var(--surface)),")
        css_lines.append("        color-mix(in srgb, " + c + " 4%, var(--surface))) !important;")
        css_lines.append("    border-color: color-mix(in srgb, " + c + " 40%, var(--border)) !important;")
        css_lines.append("}")
        css_lines.append(sel + " i:first-child { color: " + c + " !important; }")
        css_lines.append(sel + ":hover {")
        css_lines.append("    border-color: " + c + " !important;")
        css_lines.append("    background: linear-gradient(135deg,")
        css_lines.append("        color-mix(in srgb, " + c + " 20%, var(--surface)),")
        css_lines.append("        color-mix(in srgb, " + c + " 8%, var(--surface))) !important;")
        css_lines.append("}")
        css_lines.append(sel + ".active {")
        css_lines.append("    background: linear-gradient(135deg, " + c + ",")
        css_lines.append("        color-mix(in srgb, " + c + " 72%, #000)) !important;")
        css_lines.append("    color: #fff !important;")
        css_lines.append("    border-color: " + c + " !important;")
        css_lines.append("    box-shadow: 0 4px 12px color-mix(in srgb, " + c + " 40%, transparent) !important;")
        css_lines.append("}")
        css_lines.append(sel + ".active i:first-child { color: #fff !important; }")
        css_lines.append('[data-theme="dark"] ' + sel + " {")
        css_lines.append("    background: linear-gradient(135deg,")
        css_lines.append("        color-mix(in srgb, " + c + " 20%, var(--surface)),")
        css_lines.append("        color-mix(in srgb, " + c + " 8%, var(--surface))) !important;")
        css_lines.append("    border-color: color-mix(in srgb, " + c + " 50%, var(--border)) !important;")
        css_lines.append("}")
        css_lines.append('[data-theme="dark"] ' + sel + ".active {")
        css_lines.append("    background: linear-gradient(135deg, " + c + ",")
        css_lines.append("        color-mix(in srgb, " + c + " 72%, #000)) !important;")
        css_lines.append("    border-color: " + c + " !important;")
        css_lines.append("}")

    css = chr(10).join(css_lines) + chr(10)

    pat_style = re.compile(r'(\s*)(</style>)', re.MULTILINE)
    html, n = pat_style.subn(r'\1' + css + r'\1\2', html, count=1)
    if n == 0:
        print("   [!] Khong tim thay </style> - bo qua CSS")
    else:
        print("   [OK] Da override CSS")

    # =============================================================
    #  PATCH 4: JS binding
    #
    #  ═══ TICH HOP TIER LOCK GIỐNG TAB TỔNG HỢP ═══
    #
    #  Quy tắc:
    #    1. Gọi switchDataset() — hàm gốc có tier check
    #    2. KHÔNG gọi __switchRawData() trực tiếp (bypass tier)
    #    3. KHÔNG override APP_TIER/APP_LIMITS
    #    4. Chỉ dùng onboarding override cho tab tonghop
    # =============================================================
    print("")
    print("[PATCH 4] JS binding (tich hop tier lock)...")
    ids_js = json.dumps([ds["id"] for ds in new_datasets])

    # ═══════════════════════════════════════════════════════════════
    #  JS OVERRIDE — Dùng list + join để tránh lỗi escape
    # ═══════════════════════════════════════════════════════════════
    js_parts = []

    js_parts.append("")
    js_parts.append("<script>")
    js_parts.append("/* =================================================================")
    js_parts.append("   FIX.PY OVERRIDE - Bind tab moi + TICH HOP TIER LOCK")
    js_parts.append("   =================================================================")
    js_parts.append("   Quy tac:")
    js_parts.append("     1. Goi switchDataset() -> applyFilter() -> getLimitedData()")
    js_parts.append("     2. KHONG goi __switchRawData() truc tiep (bypass tier)")
    js_parts.append("     3. KHONG override APP_TIER / APP_LIMITS / publishTierState")
    js_parts.append("     4. Chi dung onboarding override cho tab tonghop")
    js_parts.append("   =================================================================")
    js_parts.append("*/")
    js_parts.append("(function() {")
    js_parts.append("    'use strict';")
    js_parts.append("    var NEW_IDS = " + ids_js + ";")
    js_parts.append("")

    # ═══ PATCH A: patchGetLimitedData — chỉ bỏ override cho tab mới ═══
    js_parts.append("    /* ------------------------------------------------------------")
    js_parts.append("       PATCH A: getLimitedData — bo onboarding override cho tab moi")
    js_parts.append("       (Vi override thuoc tab tonghop -> filter se ra 0 cau)")
    js_parts.append("       ------------------------------------------------------------ */")
    js_parts.append("    function patchGetLimitedData() {")
    js_parts.append("        if (window.__fixPyLimitedPatched) return;")
    js_parts.append("        var origGet = window.getLimitedData")
    js_parts.append("                    || (typeof getLimitedData !== 'undefined' ? getLimitedData : null);")
    js_parts.append("        if (typeof origGet !== 'function') return;")
    js_parts.append("")
    js_parts.append("        window.getLimitedData = function() {")
    js_parts.append("            var currentDs = (typeof CURRENT_DATASET !== 'undefined')")
    js_parts.append("                            ? CURRENT_DATASET : 'tonghop';")
    js_parts.append("")
    js_parts.append("            // Tab tonghop: giu nguyen logic goc")
    js_parts.append("            if (currentDs === 'tonghop') {")
    js_parts.append("                return origGet.apply(this, arguments);")
    js_parts.append("            }")
    js_parts.append("")
    js_parts.append("            // Tab moi: tam bo override, goi logic goc")
    js_parts.append("            var savedOverride = window.__onboardingOverride;")
    js_parts.append("            window.__onboardingOverride = null;")
    js_parts.append("            try {")
    js_parts.append("                var result = origGet.apply(this, arguments);")
    js_parts.append("")
    js_parts.append("                // Fallback: neu rong (HSK khong match)")
    js_parts.append("                if (result.length === 0")
    js_parts.append("                    && typeof RAW_DATA !== 'undefined'")
    js_parts.append("                    && RAW_DATA.length > 0) {")
    js_parts.append("                    var info = (typeof getTierInfo === 'function')")
    js_parts.append("                               ? getTierInfo() : {};")
    js_parts.append("                    var max = info.maxQuestions || 60;")
    js_parts.append("                    result = RAW_DATA.slice(0, max);")
    js_parts.append("                }")
    js_parts.append("                return result;")
    js_parts.append("            } finally {")
    js_parts.append("                window.__onboardingOverride = savedOverride;")
    js_parts.append("            }")
    js_parts.append("        };")
    js_parts.append("")
    js_parts.append("        window.__fixPyLimitedPatched = true;")
    js_parts.append("    }")
    js_parts.append("")

    # ═══ PATCH B: bindTab — GỌI switchDataset() để có tier lock ═══
    js_parts.append("    /* ------------------------------------------------------------")
    js_parts.append("       PATCH B: bindTab — GOI switchDataset() GOC")
    js_parts.append("       switchDataset() se goi applyFilter() -> getLimitedData()")
    js_parts.append("       -> cat cau theo tier (Demo=60, Trial=N, Active=full)")
    js_parts.append("       ------------------------------------------------------------ */")
    js_parts.append("    function bindTab(dsId) {")
    js_parts.append("        var btn = document.querySelector('.ds-btn[data-dataset=\"' + dsId + '\"]');")
    js_parts.append("        if (!btn || btn.__fixPyBound) return;")
    js_parts.append("        btn.__fixPyBound = true;")
    js_parts.append("")
    js_parts.append("        btn.addEventListener('click', function(e) {")
    js_parts.append("            e.stopImmediatePropagation();")
    js_parts.append("            e.stopPropagation();")
    js_parts.append("            e.preventDefault();")
    js_parts.append("")
    js_parts.append("            console.log('[fix.py] click tab ' + dsId);")
    js_parts.append("")
    js_parts.append("            var sub = document.getElementById('dsSubWrap');")
    js_parts.append("            if (sub) sub.style.display = 'none';")
    js_parts.append("")
    js_parts.append("            document.querySelectorAll('.ds-btn, .ds-sub-btn').forEach(function(b) {")
    js_parts.append("                b.classList.remove('active');")
    js_parts.append("            });")
    js_parts.append("            this.classList.add('active');")
    js_parts.append("")
    js_parts.append("            // ═══════════════════════════════════════════════")
    js_parts.append("            //  GOI switchDataset() GOC - DE CO TIER LOCK")
    js_parts.append("            // ═══════════════════════════════════════════════")
    js_parts.append("            var switchFn = window.switchDataset")
    js_parts.append("                        || (typeof switchDataset !== 'undefined' ? switchDataset : null);")
    js_parts.append("")
    js_parts.append("            if (typeof switchFn === 'function') {")
    js_parts.append("                switchFn(dsId);")
    js_parts.append("                console.log('[fix.py] Da goi switchDataset(\"' + dsId + '\")');")
    js_parts.append("            } else {")
    js_parts.append("                console.warn('[fix.py] Khong tim thay switchDataset - fallback');")
    js_parts.append("                // Fallback: tu lam giong switchDataset")
    js_parts.append("                if (typeof window.__switchRawData === 'function') {")
    js_parts.append("                    window.__switchRawData(dsId);")
    js_parts.append("                }")
    js_parts.append("                if (typeof state !== 'undefined' && state) {")
    js_parts.append("                    state.search = '';")
    js_parts.append("                    state.hsk = '';")
    js_parts.append("                    state.subject = '';")
    js_parts.append("                }")
    js_parts.append("                try {")
    js_parts.append("                    var si = document.getElementById('searchInput');")
    js_parts.append("                    var hf = document.getElementById('hskFilter');")
    js_parts.append("                    var sf = document.getElementById('subjectFilter');")
    js_parts.append("                    if (si) si.value = '';")
    js_parts.append("                    if (hf) hf.value = '';")
    js_parts.append("                    if (sf) sf.value = '';")
    js_parts.append("                } catch(err) {}")
    js_parts.append("                if (typeof buildFilters === 'function') buildFilters();")
    js_parts.append("                if (typeof applyFilter === 'function') applyFilter();")
    js_parts.append("            }")
    js_parts.append("")
    js_parts.append("            // Xoa onboarding override + banner")
    js_parts.append("            window.__onboardingOverride = null;")
    js_parts.append("            var obBanner = document.getElementById('onboardingActiveBanner');")
    js_parts.append("            if (obBanner) obBanner.remove();")
    js_parts.append("")
    js_parts.append("            // Scroll len dau")
    js_parts.append("            setTimeout(function() {")
    js_parts.append("                var mainEl = document.getElementById('mainContent');")
    js_parts.append("                if (mainEl) {")
    js_parts.append("                    var yOffset = mainEl.getBoundingClientRect().top")
    js_parts.append("                                + window.scrollY - 100;")
    js_parts.append("                    window.scrollTo({ top: yOffset, behavior: 'smooth' });")
    js_parts.append("                }")
    js_parts.append("            }, 100);")
    js_parts.append("")
    js_parts.append("            // VERIFY sau 400ms")
    js_parts.append("            setTimeout(function() {")
    js_parts.append("                try {")
    js_parts.append("                    var info = (typeof getTierInfo === 'function')")
    js_parts.append("                               ? getTierInfo() : {};")
    js_parts.append("                    var rawLen = (typeof RAW_DATA !== 'undefined')")
    js_parts.append("                                 ? RAW_DATA.length : 0;")
    js_parts.append("                    var limLen = (typeof getLimitedData === 'function')")
    js_parts.append("                                 ? getLimitedData().length : 0;")
    js_parts.append("                    var cards = document.querySelectorAll('.card').length;")
    js_parts.append("                    var lockBtn = document.querySelector('.load-more.locked');")
    js_parts.append("                    console.log('[fix.py] VERIFY ' + dsId")
    js_parts.append("                                + ': tier=' + info.tier")
    js_parts.append("                                + ', RAW=' + rawLen")
    js_parts.append("                                + ', limited=' + limLen")
    js_parts.append("                                + ', cards=' + cards")
    js_parts.append("                                + ', lock=' + (lockBtn ? 'YES' : 'NO'));")
    js_parts.append("                } catch(err) {")
    js_parts.append("                    console.warn('[fix.py] verify error:', err);")
    js_parts.append("                }")
    js_parts.append("            }, 400);")
    js_parts.append("        }, true);")
    js_parts.append("    }")
    js_parts.append("")

    # ═══ PATCH C: markCurrentDatasetActive ═══
    js_parts.append("    /* ------------------------------------------------------------")
    js_parts.append("       PATCH C: markCurrentDatasetActive")
    js_parts.append("       ------------------------------------------------------------ */")
    js_parts.append("    function patchMarkActive() {")
    js_parts.append("        if (window.__fixPyMarkPatched) return;")
    js_parts.append("        var origMark = window.markCurrentDatasetActive")
    js_parts.append("                    || (typeof markCurrentDatasetActive !== 'undefined'")
    js_parts.append("                        ? markCurrentDatasetActive : null);")
    js_parts.append("        if (typeof origMark !== 'function') return;")
    js_parts.append("")
    js_parts.append("        window.markCurrentDatasetActive = function() {")
    js_parts.append("            origMark.apply(this, arguments);")
    js_parts.append("            var cur = (typeof CURRENT_DATASET !== 'undefined')")
    js_parts.append("                      ? CURRENT_DATASET : 'tonghop';")
    js_parts.append("            document.querySelectorAll('.ds-btn[data-dataset]').forEach(function(b) {")
    js_parts.append("                b.classList.toggle('active', b.dataset.dataset === cur);")
    js_parts.append("            });")
    js_parts.append("        };")
    js_parts.append("        window.__fixPyMarkPatched = true;")
    js_parts.append("    }")
    js_parts.append("")

    # ═══ INIT ═══
    js_parts.append("    function bindAll() {")
    js_parts.append("        patchGetLimitedData();")
    js_parts.append("        NEW_IDS.forEach(bindTab);")
    js_parts.append("        patchMarkActive();")
    js_parts.append("    }")
    js_parts.append("")
    js_parts.append("    if (document.readyState === 'loading') {")
    js_parts.append("        document.addEventListener('DOMContentLoaded', bindAll);")
    js_parts.append("    } else {")
    js_parts.append("        bindAll();")
    js_parts.append("    }")
    js_parts.append("")
    js_parts.append("    var _timer = null;")
    js_parts.append("    var observer = new MutationObserver(function() {")
    js_parts.append("        clearTimeout(_timer);")
    js_parts.append("        _timer = setTimeout(bindAll, 200);")
    js_parts.append("    });")
    js_parts.append("    if (document.body) {")
    js_parts.append("        observer.observe(document.body, { childList: true, subtree: true });")
    js_parts.append("    }")
    js_parts.append("")
    js_parts.append("    console.log('[fix.py] Da bind ' + NEW_IDS.length + ' tab:', NEW_IDS);")
    js_parts.append("})();")
    js_parts.append("</script>")

    js = chr(10).join(js_parts)

    pat_body = re.compile(r'(\s*)(</body>)', re.IGNORECASE)
    html, n = pat_body.subn(r'\1' + js + r'\1\2', html, count=1)
    if n == 0:
        print("[X] Khong tim thay </body>")
        sys.exit(1)
    print("   [OK] Da inject JS voi tier lock")

    # =============================================================
    #  GHI FILE
    # =============================================================
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = os.path.getsize(INDEX_HTML) / 1024
    print("")
    print("=" * 62)
    print("[fix.py] HOAN TAT! Da patch " + INDEX_HTML)
    print("[fix.py] Kich thuoc: " + str(round(size_kb, 1)) + " KB")
    print("[fix.py] Da them " + str(len(new_datasets)) + " tab:")
    for ds in new_datasets:
        print("   - " + ds["name"] + " (" + str(ds["count"]) + " cau)")
    print("[fix.py] Layout: PC auto-fit - Mobile 2 cot")
    print("[fix.py] TICH HOP TIER LOCK: Demo=60, Trial=N, Active=full")
    print("=" * 62)


if __name__ == "__main__":
    main()

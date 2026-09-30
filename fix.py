# -*- coding: utf-8 -*-
"""
fix.py - Auto-scan data/ va them MOI file Excel thanh tab rieng.

DAC DIEM:
  - Doc HET moi file .xlsx/.xls/.csv trong data/
  - Ten tab = ten file (normalize NFC - hien thi dung dau tieng Viet)
  - Logic doc Excel GIONG data_reader.py:
      openpyxl, cot VI TRI: 0=STT, 1=HSK, 2=Topic, 3=Subject, 4=Vi, 5=Zh, 6=Pinyin
      Data bat dau tu dong 2, tu dong chuyen so A Rap -> Han (cn2an)
  - Tier Demo/Expired/Trial van "khoa 1 phan" nhu tab tong hop
  - Click tab moi KHONG bi chan boi popup "Chuyen nganh"
  - KHONG can thiep convert.py, ui_template.py, config.json

Cach chay:
    python scripts/convert.py    # Tao index.html goc
    python fix.py                # Patch index.html - them tab tu data/
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
    """
    Ten tab hien thi:
      'input.xlsx'              -> 'Input'
      '1000_Cau_giao_tiep.xlsx' -> '1000 Cau Giao Tiep'
    Normalize NFC de hien thi dung dau tieng Viet.
    """
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
    """Tim file voi ten chinh xac tren filesystem - xu ly NFD/NFC mismatch."""
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
    """
    Doc Excel -> list[dict] - GIONG data_reader.read_excel().
    Cot theo VI TRI: 0=STT, 1=HSK, 2=Topic, 3=Subject, 4=Vi, 5=Zh, 6=Pinyin.
    Data bat dau tu dong 2.
    """
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
    """Quet data/ -> list[dict] dataset entries."""
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

    # Loc bo dataset da co trong HTML
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
    #  PATCH 3: CSS layout
    # =============================================================
    # =============================================================
    #  PATCH 3: CSS layout
    # =============================================================
    print("")
    print("[PATCH 3] CSS layout...")

    # Dung list + join de tranh loi escape \n khi paste
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
    # =============================================================
    print("")
    print("[PATCH 4] JS binding (chan popup + fix getLimitedData)...")
    ids_js = json.dumps([ds["id"] for ds in new_datasets])

    js = """
<script>
/* =================================================================
   FIX.PY OVERRIDE - Bind tab moi + Chan popup tier-check
   ================================================================= */
(function() {
    'use strict';
    var NEW_IDS = """ + ids_js + """;

    /* ------------------------------------------------------------
       PATCH 1: getLimitedData - bo onboarding override cho tab moi
       ------------------------------------------------------------ */
    function patchGetLimitedData() {
        if (window.__fixPyLimitedPatched) return;
        var origGet = window.getLimitedData
                    || (typeof getLimitedData !== 'undefined' ? getLimitedData : null);
        if (typeof origGet !== 'function') return;

        window.getLimitedData = function() {
            var currentDs = (typeof CURRENT_DATASET !== 'undefined')
                            ? CURRENT_DATASET : 'tonghop';

            if (currentDs !== 'tonghop') {
                var savedOverride = window.__onboardingOverride;
                window.__onboardingOverride = null;

                try {
                    var result = origGet.apply(this, arguments);

                    if (result.length === 0
                        && typeof RAW_DATA !== 'undefined'
                        && RAW_DATA.length > 0) {
                        console.warn('[fix.py] getLimitedData() rong cho tab '
                                     + currentDs + ' - dung fallback');
                        var info = (typeof getTierInfo === 'function')
                                   ? getTierInfo() : {};
                        var max = info.maxQuestions || 60;
                        result = RAW_DATA.slice(0, max);
                        console.log('[fix.py] Fallback: lay ' + result.length + ' cau dau');
                    }

                    return result;
                } finally {
                    window.__onboardingOverride = savedOverride;
                }
            }

            return origGet.apply(this, arguments);
        };

        window.__fixPyLimitedPatched = true;
        console.log('[fix.py] Da patch getLimitedData()');
    }

    /* ------------------------------------------------------------
       PATCH 2: Bind click - CAPTURE PHASE
       ------------------------------------------------------------ */
    function bindTab(dsId) {
        var btn = document.querySelector('.ds-btn[data-dataset="' + dsId + '"]');
        if (!btn || btn.__fixPyBound) return;
        btn.__fixPyBound = true;

        btn.addEventListener('click', function(e) {
            e.stopImmediatePropagation();
            e.stopPropagation();
            e.preventDefault();

            console.log('[fix.py] click tab ' + dsId);

            var sub = document.getElementById('dsSubWrap');
            if (sub) sub.style.display = 'none';

            document.querySelectorAll('.ds-btn, .ds-sub-btn').forEach(function(b) {
                b.classList.remove('active');
            });
            this.classList.add('active');

            if (typeof window.__switchRawData === 'function') {
                window.__switchRawData(dsId);
            } else if (typeof DATASET_REGISTRY !== 'undefined'
                       && DATASET_REGISTRY[dsId]) {
                if (typeof RAW_DATA !== 'undefined') {
                    window.RAW_DATA = DATASET_REGISTRY[dsId].data || [];
                }
                if (typeof CURRENT_DATASET !== 'undefined') {
                    window.CURRENT_DATASET = dsId;
                }
            }

            if (typeof state !== 'undefined' && state) {
                state.search = '';
                state.hsk = '';
                state.subject = '';
            }
            try {
                var searchInput = document.getElementById('searchInput');
                var hskFilter = document.getElementById('hskFilter');
                var subjectFilter = document.getElementById('subjectFilter');
                if (searchInput) searchInput.value = '';
                if (hskFilter) hskFilter.value = '';
                if (subjectFilter) subjectFilter.value = '';
                var clearBtn = document.getElementById('clearSearchBtn');
                if (clearBtn) clearBtn.classList.remove('show');
            } catch(err) {}

            window.__onboardingOverride = null;
            var obBanner = document.getElementById('onboardingActiveBanner');
            if (obBanner) obBanner.remove();

            try {
                if (typeof applyFilter === 'function') applyFilter();
                if (typeof updateResultCount === 'function') updateResultCount();
                if (typeof markCurrentDatasetActive === 'function') {
                    markCurrentDatasetActive();
                }
            } catch(err) {
                console.warn('[fix.py] re-render error:', err);
            }

            setTimeout(function() {
                var mainEl = document.getElementById('mainContent');
                if (mainEl) {
                    var yOffset = mainEl.getBoundingClientRect().top
                                + window.scrollY - 100;
                    window.scrollTo({ top: yOffset, behavior: 'smooth' });
                }
            }, 100);

            setTimeout(function() {
                try {
                    var info = (typeof getTierInfo === 'function')
                               ? getTierInfo() : {};
                    var rawLen = (typeof RAW_DATA !== 'undefined')
                                 ? RAW_DATA.length : 0;
                    var limLen = (typeof getLimitedData === 'function')
                                 ? getLimitedData().length : 0;
                    var cards = document.querySelectorAll('.card').length;
                    console.log('[fix.py] Tab ' + dsId
                                + ': tier=' + info.tier
                                + ', RAW_DATA=' + rawLen
                                + ', limited=' + limLen
                                + ', cards=' + cards);
                } catch(err) {
                    console.warn('[fix.py] verify error:', err);
                }
            }, 300);
        }, true);
    }

    /* ------------------------------------------------------------
       PATCH 3: markCurrentDatasetActive
       ------------------------------------------------------------ */
    function patchMarkActive() {
        if (window.__fixPyMarkPatched) return;
        var origMark = window.markCurrentDatasetActive
                    || (typeof markCurrentDatasetActive !== 'undefined'
                        ? markCurrentDatasetActive : null);
        if (typeof origMark !== 'function') return;

        window.markCurrentDatasetActive = function() {
            origMark.apply(this, arguments);
            var cur = (typeof CURRENT_DATASET !== 'undefined')
                      ? CURRENT_DATASET : 'tonghop';
            document.querySelectorAll('.ds-btn[data-dataset]').forEach(function(b) {
                b.classList.toggle('active', b.dataset.dataset === cur);
            });
        };
        window.__fixPyMarkPatched = true;
    }

    function bindAll() {
        patchGetLimitedData();
        NEW_IDS.forEach(bindTab);
        patchMarkActive();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', bindAll);
    } else {
        bindAll();
    }

    var _timer = null;
    var observer = new MutationObserver(function() {
        clearTimeout(_timer);
        _timer = setTimeout(bindAll, 200);
    });
    if (document.body) {
        observer.observe(document.body, { childList: true, subtree: true });
    }

    console.log('[fix.py] Da bind ' + NEW_IDS.length + ' tab:', NEW_IDS);
})();
</script>
"""

    pat_body = re.compile(r'(\s*)(</body>)', re.IGNORECASE)
    html, n = pat_body.subn(r'\1' + js + r'\1\2', html, count=1)
    if n == 0:
        print("[X] Khong tim thay </body>")
        sys.exit(1)
    print("   [OK] Da inject JS")

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
    print("[fix.py] Tier: Demo/Trial/Expired khoa 1 phan")
    print("[fix.py] Chan popup 'Chuyen nganh' cho tab moi")
    print("=" * 62)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
fix.py — Auto-scan data/ và thêm MỌI file Excel thành tab riêng.

ĐẶC ĐIỂM:
  - Đọc HẾT mọi file .xlsx/.xls/.csv trong data/ (kể cả input.xlsx)
  - Tên tab = tên file (giống logic chuyên ngành trong convert.py)
  - Logic đọc Excel giống HỆT data_reader.py:
      openpyxl, cột theo VỊ TRÍ: 0=STT, 1=HSK, 2=Topic, 3=Subject, 4=Vi, 5=Zh, 6=Pinyin
      Data bắt đầu từ dòng 2, tự động chuyển số Ả Rập → Hán (cn2an)
  - KHÔNG can thiệp convert.py, ui_template.py, config.json
  - Tier Demo/Expired/Trial vẫn "khoá 1 phần" như tab tổng hợp

Cách chạy:
    python scripts/convert.py    # Tạo index.html gốc
    python fix.py                # Patch index.html — thêm tab từ data/

Kết quả (ví dụ 2 file trong data/):
    [Input 1700 câu] [1000 Câu Giao Tiếp 1000 câu] [Chuyên ngành ▼] [Yêu thích]
"""
import json
import os
import re
import sys
import glob
import unicodedata

import openpyxl

# ═══════════════════════════════════════════════════════════════════
#  CONFIG
# ═══════════════════════════════════════════════════════════════════
INDEX_HTML  = "index.html"
CONFIG_JSON = "config.json"
DATA_DIR    = "data"

# Nếu fix.py chạy từ scripts/, tự nhảy ra root
if not os.path.isfile(CONFIG_JSON) and os.path.isfile(os.path.join("..", CONFIG_JSON)):
    os.chdir("..")
    print("🔄 fix.py phát hiện chạy từ scripts/ → chuyển về root")

TAB_ICONS = [
    "fa-comments", "fa-file-alt", "fa-book", "fa-graduation-cap",
    "fa-star", "fa-fire", "fa-bolt", "fa-rocket",
]
TAB_COLORS = [
    "#0891b2", "#dc2626", "#059669", "#d97706",
    "#7c3aed", "#db2777", "#0284c7", "#65a30d",
]


# ═══════════════════════════════════════════════════════════════════
#  CHUYỂN SỐ Ả RẬP → SỐ HÁN (copy từ data_reader.py)
# ═══════════════════════════════════════════════════════════════════
try:
    import cn2an
    HAS_CN2AN = True
except ImportError:
    HAS_CN2AN = False
    print("⚠️  Không có cn2an — số Ả Rập sẽ giữ nguyên")

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
    """Chuyển số Ả Rập → số Hán (giống data_reader.py)."""
    if not text or not isinstance(text, str):
        return text

    # Phần trăm
    def replace_percent(match):
        num_str = match.group(1)
        if '.' in num_str:
            parts = num_str.split('.')
            int_part = _num_to_chinese(int(parts[0]))
            dec_part = _digits_to_chinese(parts[1])
            return '百分之' + int_part + '点' + dec_part
        return '百分之' + _num_to_chinese(int(num_str))

    text = re.sub(r'(\d+(?:\.\d+)?)%', replace_percent, text)

    # Số thập phân độc lập
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

    # Số nguyên độc lập
    def replace_int(match):
        return _num_to_chinese(int(match.group(0)))

    text = re.sub(
        r'(?<![A-Za-z\-\.])\d+(?![A-Za-z]|\.\d)',
        replace_int, text
    )

    return text


def _clean(s):
    """Làm sạch cell (giống data_reader.py)."""
    if s is None:
        return ""
    return (str(s).replace('\n', ' ').replace('\r', ' ')
            .replace('\t', ' ').replace('\\', '\\\\'))


# ═══════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════
def _slugify(filename):
    base = filename.rsplit(".", 1)[0]
    base = unicodedata.normalize("NFD", base)
    base = "".join(c for c in base if unicodedata.category(c) != "Mn")
    base = base.replace("đ", "d").replace("Đ", "D")
    return re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower() or "dataset"


def _display_name(filename):
    """Tên tab hiển thị (giống logic chuyên ngành của convert.py)."""
    name = filename.rsplit(".", 1)[0].replace("_", " ").strip()
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


def _read_excel_rows(filepath):
    """
    Đọc Excel → list[dict] — GIỐNG HỆT data_reader.read_excel().
    Cột theo VỊ TRÍ:
        0=STT, 1=HSK, 2=Topic, 3=Subject, 4=Vi, 5=Zh, 6=Pinyin
        Data bắt đầu từ dòng 2.
    """
    try:
        wb = openpyxl.load_workbook(filepath, data_only=True)
    except Exception as e:
        print(f"      ❌ Không load được: {e}")
        return []

    try:
        ws = wb.worksheets[0]
    except Exception as e:
        print(f"      ❌ Không có sheet: {e}")
        return []

    print(f"      📊 Sheet: {ws.title} - {ws.max_row} dòng")

    # ═══ CẤU HÌNH CỘT (GIỐNG data_reader.py) ═══
    COL_STT     = 0
    COL_HSK     = 1
    COL_TOPIC   = 2
    COL_SUBJECT = 3
    COL_VI      = 4
    COL_ZH      = 5
    COL_PINYIN  = 6
    DATA_START  = 2

    rows = []
    converted_count = 0

    for row in ws.iter_rows(min_row=DATA_START, values_only=True):
        if not row or len(row) <= max(COL_VI, COL_ZH):
            continue

        stt     = row[COL_STT]     if COL_STT     < len(row) and row[COL_STT]     is not None else ""
        hsk     = _clean(row[COL_HSK])     if COL_HSK     < len(row) else ""
        topic   = _clean(row[COL_TOPIC])   if COL_TOPIC   < len(row) else ""
        subject = _clean(row[COL_SUBJECT]) if COL_SUBJECT < len(row) else ""
        vi      = _clean(row[COL_VI])      if COL_VI      < len(row) else ""
        zh      = _clean(row[COL_ZH])      if COL_ZH      < len(row) else ""
        pinyin  = _clean(row[COL_PINYIN])  if COL_PINYIN  < len(row) else ""

        if not vi and not zh:
            continue

        # ⬇️ CHUYỂN SỐ Ả RẬP → HÁN
        zh_original = zh
        zh = convert_arabic_to_chinese(zh)
        if zh != zh_original:
            converted_count += 1

        rows.append({
            "stt":     str(stt),
            "hsk":     hsk,
            "topic":   topic,
            "subject": subject,
            "vi":      vi,
            "zh":      zh,
            "pinyin":  pinyin,
        })

    if converted_count > 0:
        print(f"      🔄 Đã chuyển số Ả Rập → Hán: {converted_count} câu")

    return rows


# ═══════════════════════════════════════════════════════════════════
#  SCAN data/ — ĐỌC HẾT MỌI FILE
# ═══════════════════════════════════════════════════════════════════
def scan_data_dir():
    """Quét data/ → list[dict] dataset entries — ĐỌC HẾT MỌI FILE."""
    if not os.path.isdir(DATA_DIR):
        print(f"⚠️  Không thấy '{DATA_DIR}/' — bỏ qua.")
        return []

    files = []
    for ext in ("*.xlsx", "*.xls", "*.csv"):
        files.extend(glob.glob(os.path.join(DATA_DIR, ext)))
    files = sorted(set(files))

    if not files:
        print(f"ℹ️  Không có file Excel trong '{DATA_DIR}/'")
        return []

    print(f"\n📂 Quét '{DATA_DIR}/' — {len(files)} file")

    datasets = []
    used_ids = set()

    for filepath in files:
        fname = os.path.basename(filepath)

        # Chỉ bỏ file tạm Office (~$...)
        if fname.startswith("~$"):
            print(f"   ⏭️  {fname} — file tạm")
            continue

        print(f"   📄 {fname}")
        rows = _read_excel_rows(filepath)
        if not rows:
            print(f"   ⚠️  {fname} — rỗng hoặc lỗi, bỏ qua")
            continue

        base_id = _slugify(fname)
        dataset_id = base_id
        counter = 2
        while dataset_id in used_ids:
            dataset_id = f"{base_id}-{counter}"
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
        print(f"   ✅ {fname} → tab '{display}' ({len(rows)} câu)")

    return datasets


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════
def main():
    print("=" * 62)
    print("🔧 fix.py — Auto-scan data/ → thêm tab riêng cho mỗi file")
    print("=" * 62)

    if not os.path.isfile(INDEX_HTML):
        print(f"❌ Không thấy {INDEX_HTML}. Chạy convert.py trước.")
        sys.exit(1)

    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    datasets = scan_data_dir()

    if not datasets:
        print("\nℹ️  Không có dataset nào trong data/. Giữ nguyên index.html.")
        return

    # Lọc bỏ dataset đã có trong HTML (chạy lại nhiều lần)
    new_datasets = []
    for ds in datasets:
        if (f'"id":"{ds["id"]}"' in html
                or f"'id': '{ds['id']}'" in html
                or f'data-dataset="{ds["id"]}"' in html):
            print(f"   ⏭️  '{ds['id']}' đã có trong HTML — bỏ qua")
        else:
            new_datasets.append(ds)

    if not new_datasets:
        print("\n✅ Tất cả dataset đã có — không cần patch.")
        return

    print(f"\n🎯 Sẽ thêm {len(new_datasets)} tab:")
    for ds in new_datasets:
        print(f"   • {ds['name']} ({ds['count']} câu)")

    # ═══════════════════════════════════════════════════════════════
    #  PATCH 1: Inject dataset vào DATASET_REGISTRY
    # ═══════════════════════════════════════════════════════════════
    print("\n🔨 PATCH 1: Inject vào DATASET_REGISTRY...")
    pat_registry = re.compile(r'(var\s+DATASET_REGISTRY\s*=\s*)(\{)', re.MULTILINE)
    if not pat_registry.search(html):
        print("❌ Không tìm thấy DATASET_REGISTRY")
        sys.exit(1)

    inject = "".join(f'"{ds["id"]}":{_escape_json_for_script(ds)},' for ds in new_datasets)
    html, n = pat_registry.subn(r'\1\2' + inject, html, count=1)
    if n == 0:
        print("❌ Không chèn được registry")
        sys.exit(1)
    print(f"   ✅ Đã chèn {len(new_datasets)} entry")

    # ═══════════════════════════════════════════════════════════════
    #  PATCH 2: Thêm button vào .ds-main-row
    # ═══════════════════════════════════════════════════════════════
    print("\n🔨 PATCH 2: Thêm button tabs...")
    new_btns = ""
    for ds in new_datasets:
        label = f'{ds["name"]} · {ds["count"]} câu'
        new_btns += (
            f'\n        <button class="ds-btn ds-btn-primary" '
            f'data-dataset="{ds["id"]}">\n'
            f'            <i class="fas {ds["icon"]}"></i>\n'
            f'            <span>{_js_str(label)}</span>\n'
            f'        </button>\n    '
        )

    # Chèn TRƯỚC nút chuyen-nganh
    pat_btn = re.compile(
        r'(\s*)(<button\s+class="[^"]*ds-btn[^"]*"\s+[^>]*data-dataset-group="chuyen-nganh")',
        re.MULTILINE
    )
    html, n = pat_btn.subn(r'\1' + new_btns + r'\2', html, count=1)
    if n == 0:
        print("❌ Không tìm thấy nút chuyen-nganh")
        sys.exit(1)
    print(f"   ✅ Đã chèn {len(new_datasets)} button")

    # ═══════════════════════════════════════════════════════════════
    #  PATCH 3: CSS layout (auto-fit)
    # ═══════════════════════════════════════════════════════════════
    print("\n🔨 PATCH 3: CSS layout...")
    color_css = ""
    for ds in new_datasets:
        c = ds["color"]
        i = ds["id"]
        color_css += f"""
.ds-btn[data-dataset="{i}"] {{
    background: linear-gradient(135deg,
        color-mix(in srgb, {c} 12%, var(--surface)),
        color-mix(in srgb, {c} 4%, var(--surface))) !important;
    border-color: color-mix(in srgb, {c} 40%, var(--border)) !important;
}}
.ds-btn[data-dataset="{i}"] i:first-child {{ color: {c} !important; }}
.ds-btn[data-dataset="{i}"]:hover {{
    border-color: {c} !important;
    background: linear-gradient(135deg,
        color-mix(in srgb, {c} 20%, var(--surface)),
        color-mix(in srgb, {c} 8%, var(--surface))) !important;
}}
.ds-btn[data-dataset="{i}"].active {{
    background: linear-gradient(135deg, {c},
        color-mix(in srgb, {c} 72%, #000)) !important;
    color: #fff !important;
    border-color: {c} !important;
    box-shadow: 0 4px 12px color-mix(in srgb, {c} 40%, transparent) !important;
}}
.ds-btn[data-dataset="{i}"].active i:first-child {{ color: #fff !important; }}
[data-theme="dark"] .ds-btn[data-dataset="{i}"] {{
    background: linear-gradient(135deg,
        color-mix(in srgb, {c} 20%, var(--surface)),
        color-mix(in srgb, {c} 8%, var(--surface))) !important;
    border-color: color-mix(in srgb, {c} 50%, var(--border)) !important;
}}
[data-theme="dark"] .ds-btn[data-dataset="{i}"].active {{
    background: linear-gradient(135deg, {c},
        color-mix(in srgb, {c} 72%, #000)) !important;
    border-color: {c} !important;
}}
"""

    css = f"""
/* ★★ FIX.PY: AUTO-FIT LAYOUT CHO N TAB ★★ */
@media (max-width: 768px) {{
    .ds-main-row {{
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: .5rem !important;
    }}
}}
@media (min-width: 769px) and (max-width: 1100px) {{
    .ds-main-row {{
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: .55rem !important;
    }}
}}
@media (min-width: 1101px) {{
    .ds-main-row {{
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) !important;
        gap: .6rem !important;
    }}
}}
{color_css}
"""
    pat_style = re.compile(r'(\s*)(</style>)', re.MULTILINE)
    html, n = pat_style.subn(r'\1' + css + r'\1\2', html, count=1)
    if n == 0:
        print("⚠️  Không tìm thấy </style> — bỏ qua CSS")
    else:
        print("   ✅ Đã override CSS")

    # ═══════════════════════════════════════════════════════════════
    #  PATCH 4: JS binding + Fix getLimitedData
    # ═══════════════════════════════════════════════════════════════
    print("\n🔨 PATCH 4: JS binding + patch getLimitedData...")
    ids_js = json.dumps([ds["id"] for ds in new_datasets])

    js = f"""
<script>
/* ═══════════════════════════════════════════════════════════════════
   ★★ FIX.PY OVERRIDE: Bind tab mới + Fix getLimitedData ★★
   ═══════════════════════════════════════════════════════════════════ */
(function() {{
    'use strict';
    var NEW_IDS = {ids_js};

    /* ═══════════════════════════════════════════════════════════
       PATCH 1: getLimitedData — bỏ onboarding override cho tab mới
       (Fix bug: Demo/Expired không mở được câu nào ở tab mới)
       ═══════════════════════════════════════════════════════════ */
    function patchGetLimitedData() {{
        if (window.__fixPyLimitedPatched) return;
        var origGet = window.getLimitedData
                    || (typeof getLimitedData !== 'undefined' ? getLimitedData : null);
        if (typeof origGet !== 'function') return;

        window.getLimitedData = function() {{
            var currentDs = (typeof CURRENT_DATASET !== 'undefined')
                            ? CURRENT_DATASET : 'tonghop';

            // Tab mới KHÔNG dùng onboarding override
            // (vì override thuộc tab tonghop → filter sẽ ra 0 câu)
            if (currentDs !== 'tonghop') {{
                var savedOverride = window.__onboardingOverride;
                window.__onboardingOverride = null;
                try {{
                    return origGet.apply(this, arguments);
                }} finally {{
                    window.__onboardingOverride = savedOverride;
                }}
            }}

            return origGet.apply(this, arguments);
        }};

        window.__fixPyLimitedPatched = true;
        console.log('✅ fix.py: đã patch getLimitedData()');
    }}

    /* ═══════════════════════════════════════════════════════════
       PATCH 2: Bind click cho tab mới
       ═══════════════════════════════════════════════════════════ */
    function bindTab(dsId) {{
        var btn = document.querySelector('.ds-btn[data-dataset="' + dsId + '"]');
        if (!btn || btn.__fixPyBound) return;
        btn.__fixPyBound = true;

        btn.addEventListener('click', function() {{
            var sub = document.getElementById('dsSubWrap');
            if (sub) sub.style.display = 'none';

            document.querySelectorAll('.ds-btn, .ds-sub-btn').forEach(function(b) {{
                b.classList.remove('active');
            }});
            this.classList.add('active');

            var fn = window.switchDataset
                  || (typeof switchDataset !== 'undefined' ? switchDataset : null);
            if (typeof fn === 'function') {{
                fn(dsId);
            }} else if (typeof window.__switchRawData === 'function') {{
                window.__switchRawData(dsId);
                if (typeof applyFilter === 'function') applyFilter();
            }}
        }});
    }}

    /* ═══════════════════════════════════════════════════════════
       PATCH 3: markCurrentDatasetActive nhận diện tab mới
       ═══════════════════════════════════════════════════════════ */
    function patchMarkActive() {{
        if (window.__fixPyMarkPatched) return;
        var origMark = window.markCurrentDatasetActive
                    || (typeof markCurrentDatasetActive !== 'undefined'
                        ? markCurrentDatasetActive : null);
        if (typeof origMark !== 'function') return;

        window.markCurrentDatasetActive = function() {{
            origMark.apply(this, arguments);
            var cur = (typeof CURRENT_DATASET !== 'undefined')
                      ? CURRENT_DATASET : 'tonghop';
            document.querySelectorAll('.ds-btn[data-dataset]').forEach(function(b) {{
                b.classList.toggle('active', b.dataset.dataset === cur);
            }});
        }};
        window.__fixPyMarkPatched = true;
    }}

    function bindAll() {{
        patchGetLimitedData();
        NEW_IDS.forEach(bindTab);
        patchMarkActive();
    }}

    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', bindAll);
    }} else {{
        bindAll();
    }}

    var _timer = null;
    var observer = new MutationObserver(function() {{
        clearTimeout(_timer);
        _timer = setTimeout(bindAll, 200);
    }});
    if (document.body) {{
        observer.observe(document.body, {{ childList: true, subtree: true }});
    }}

    console.log('✅ fix.py: bind ' + NEW_IDS.length + ' tab:', NEW_IDS);
}})();
</script>
"""
    pat_body = re.compile(r'(\s*)(</body>)', re.IGNORECASE)
    html, n = pat_body.subn(r'\1' + js + r'\1\2', html, count=1)
    if n == 0:
        print("❌ Không tìm thấy </body>")
        sys.exit(1)
    print("   ✅ Đã inject JS")

    # ═══════════════════════════════════════════════════════════════
    #  PATCH 5 (OPTIONAL): Xóa tab "Tổng hợp VPCX" cũ
    #  BẬT bằng cách bỏ comment bên dưới nếu bạn muốn xóa tab tổng hợp.
    #  Mặc định TẮT — giữ tab tổng hợp bên cạnh tab "Input".
    # ═══════════════════════════════════════════════════════════════
    # print("\n🔨 PATCH 5: Xóa tab Tổng hợp cũ...")
    # pat_tonghop_btn = re.compile(
    #     r'<button[^>]*data-dataset="tonghop"[^>]*>.*?</button>\s*',
    #     re.DOTALL
    # )
    # html, n = pat_tonghop_btn.subn('', html)
    # if n > 0:
    #     print(f"   ✅ Đã xóa {n} nút tổng hợp")

    # ═══════════════════════════════════════════════════════════════
    #  GHI FILE
    # ═══════════════════════════════════════════════════════════════
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = os.path.getsize(INDEX_HTML) / 1024
    print("\n" + "=" * 62)
    print(f"🎉 HOÀN TẤT! Đã patch {INDEX_HTML}")
    print(f"📦 Kích thước: {size_kb:.1f} KB")
    print(f"➕ Đã thêm {len(new_datasets)} tab:")
    for ds in new_datasets:
        print(f"   • {ds['name']} ({ds['count']} câu)")
    print(f"🎨 Layout: PC auto-fit · Mobile 2 cột")
    print(f"🔒 Tier: Demo/Trial/Expired khoá 1 phần như tab tổng hợp")
    print("=" * 62)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
fix.py — Auto-scan data/ và thêm MỌI file Excel thành tab riêng.

Mục đích:
    - Bất kỳ file .xlsx/.xls/.csv nào trong data/ → 1 tab riêng
    - Tên tab = tên file (giống logic chuyên ngành trong main.py)
    - KHÔNG can thiệp main.py, ui_template.py, config.json
    - Bỏ qua file trùng với excel_file trong config (tab tổng hợp cũ)

Cách chạy:
    python main.py      # Tạo index.html như bình thường
    python fix.py       # Patch index.html — thêm N tab từ data/

Kết quả (ví dụ có 2 file):
    [Tổng hợp VPCX] [Input] [Giao Tiếp] [Chuyên ngành ▼] [Yêu thích]
    - PC: nhiều cột (grid auto-fit)
    - Mobile: 2 cột
"""
import json
import os
import re
import sys
import glob
import unicodedata

# ═══════════════════════════════════════════════════════════════════
#  CONFIG
# ═══════════════════════════════════════════════════════════════════
INDEX_HTML   = "index.html"
CONFIG_JSON  = "config.json"
DATA_DIR     = "data"

# Icon + màu cho tab mới (tự luân phiên nếu nhiều file)
TAB_ICONS = [
    "fa-comments",     # Giao tiếp
    "fa-file-alt",     # Tài liệu
    "fa-book",         # Sách
    "fa-graduation-cap",  # Học tập
    "fa-star",         # Nổi bật
    "fa-fire",         # Hot
    "fa-bolt",         # Nhanh
    "fa-rocket",       # Mới
]
TAB_COLORS = [
    "#0891b2",   # teal
    "#dc2626",   # đỏ
    "#059669",   # xanh lá
    "#d97706",   # cam
    "#7c3aed",   # tím
    "#db2777",   # hồng
    "#0284c7",   # xanh dương
    "#65a30d",   # olive
]


# ═══════════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════════
def _slugify(filename):
    """Sinh id an toàn từ tên file (khớp main.py)."""
    base = filename.rsplit(".", 1)[0]
    base = unicodedata.normalize("NFD", base)
    base = "".join(c for c in base if unicodedata.category(c) != "Mn")
    base = base.replace("đ", "d").replace("Đ", "D")
    base = re.sub(r"[^a-zA-Z0-9]+", "-", base).strip("-").lower()
    return base or "dataset"


def _display_name(filename):
    """
    Tên tab hiển thị — GIỐNG LOGIC chuyên ngành trong main.py:
        'input.xlsx'       → 'Input'
        'Giao_tiếp.xlsx'   → 'Giao Tiếp'
        'LUYEN_THI.xlsx'   → 'Luyen Thi'  (nếu .islower/.isupper)
    """
    name = filename.rsplit(".", 1)[0].replace("_", " ").strip()
    if name.islower() or name.isupper():
        name = name.title()
    return name


def _escape_json_for_script(obj):
    """Serialize → JSON an toàn cho <script> context."""
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s.replace("</", "<\\/")


def _js_str(s):
    """Escape string JS (dùng cho label)."""
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
    """Đọc Excel → list[dict] theo cấu trúc chuẩn của app."""
    try:
        import pandas as pd
    except ImportError:
        print("❌ Cần cài pandas + openpyxl: pip install pandas openpyxl")
        sys.exit(1)

    try:
        df = pd.read_excel(filepath, sheet_name=0)
    except Exception as e:
        print(f"   ❌ Không đọc được {os.path.basename(filepath)}: {e}")
        return []

    df.columns = [str(c).strip().lower() for c in df.columns]

    rows = []
    for idx, row in df.iterrows():
        def _v(col):
            val = row.get(col, "")
            try:
                if pd.isna(val):
                    return ""
            except (TypeError, ValueError):
                pass
            return "" if val is None else str(val).strip()

        stt = _v("stt") or str(idx + 2)
        zh = _v("zh") or _v("hanzi") or _v("chinese") or _v("tieng_trung")
        vi = _v("vi") or _v("vietnamese") or _v("tieng_viet")
        pinyin = _v("pinyin")
        hsk = _v("hsk").upper() if _v("hsk") else ""
        topic = _v("topic") or _v("chude") or _v("chu_de")
        subject = _v("subject") or _v("chuyen_nganh") or _v("chuyennganh")
        excel_row = _v("excelrow") or _v("excel_row") or str(idx + 2)

        if not zh and not vi:
            continue

        rows.append({
            "stt": stt,
            "vi": vi,
            "zh": zh,
            "pinyin": pinyin,
            "hsk": hsk,
            "topic": topic,
            "subject": subject,
            "excelRow": excel_row,
        })
    return rows


def _load_config():
    """Đọc config.json để biết file excel_file (bỏ qua)."""
    if not os.path.isfile(CONFIG_JSON):
        return {}
    try:
        with open(CONFIG_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


# ═══════════════════════════════════════════════════════════════════
#  SCAN + PARSE
# ═══════════════════════════════════════════════════════════════════
def scan_data_dir(config):
    """
    Quét data/ → trả về list[dict] dataset entries.
    Bỏ qua:
      - file excel_file trong config (đã là tab tổng hợp)
      - file tạm ~$...
      - thư mục con
    """
    if not os.path.isdir(DATA_DIR):
        print(f"⚠️  Không thấy thư mục '{DATA_DIR}/' — bỏ qua.")
        return []

    # File cần bỏ qua
    skip_abs = set()
    excel_file = config.get("excel_file", "")
    if excel_file:
        # Có thể là "data/input.xlsx" hoặc "input.xlsx"
        skip_abs.add(os.path.abspath(excel_file))
        skip_abs.add(os.path.abspath(os.path.join(DATA_DIR, os.path.basename(excel_file))))

    # Quét các đuôi Excel
    files = []
    for ext in ("*.xlsx", "*.xls", "*.csv"):
        files.extend(glob.glob(os.path.join(DATA_DIR, ext)))
    files = sorted(set(files))

    if not files:
        print(f"ℹ️  Không có file Excel nào trong '{DATA_DIR}/'")
        return []

    print(f"\n📂 Quét '{DATA_DIR}/' — {len(files)} file")

    datasets = []
    used_ids = set()

    for filepath in files:
        fname = os.path.basename(filepath)

        # Bỏ file tạm
        if fname.startswith("~$"):
            print(f"   ⏭️  {fname} — file tạm, bỏ qua")
            continue

        # Bỏ file trùng excel_file
        if os.path.abspath(filepath) in skip_abs:
            print(f"   ⏭️  {fname} — trùng excel_file, bỏ qua")
            continue

        # Đọc Excel
        rows = _read_excel_rows(filepath)
        if not rows:
            print(f"   ⚠️  {fname} — rỗng hoặc lỗi, bỏ qua")
            continue

        # Sinh id + đảm bảo không trùng
        base_id = _slugify(fname)
        dataset_id = base_id
        counter = 2
        while dataset_id in used_ids:
            dataset_id = f"{base_id}-{counter}"
            counter += 1
        used_ids.add(dataset_id)

        # Icon + màu luân phiên
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

    # ─── 0. Kiểm tra ───
    if not os.path.isfile(INDEX_HTML):
        print(f"❌ Không thấy {INDEX_HTML}. Chạy `python main.py` trước.")
        sys.exit(1)

    config = _load_config()

    # ─── 1. Đọc index.html ───
    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    # ─── 2. Quét data/ ───
    datasets = scan_data_dir(config)

    if not datasets:
        print("\nℹ️  Không có dataset mới nào. Giữ nguyên index.html.")
        return

    # ─── 3. Lọc bỏ những dataset đã có trong HTML (chạy lại nhiều lần) ───
    new_datasets = []
    for ds in datasets:
        marker = f'"id":"{ds["id"]}"'
        marker2 = f"'id': '{ds['id']}'"
        marker3 = f'data-dataset="{ds["id"]}"'
        if marker in html or marker2 in html or marker3 in html:
            print(f"   ⏭️  '{ds['id']}' đã có trong HTML — bỏ qua")
        else:
            new_datasets.append(ds)

    if not new_datasets:
        print("\n✅ Tất cả dataset đã có trong HTML — không cần patch.")
        return

    print(f"\n🎯 Sẽ thêm {len(new_datasets)} tab mới:")
    for ds in new_datasets:
        print(f"   • {ds['name']} ({ds['count']} câu)")

    # ═══════════════════════════════════════════════════════════════
    #  PATCH 1: Inject dataset vào DATASET_REGISTRY
    # ═══════════════════════════════════════════════════════════════
    print("\n🔨 PATCH 1: Inject dataset vào DATASET_REGISTRY...")

    pat_registry = re.compile(
        r'(var\s+DATASET_REGISTRY\s*=\s*)(\{)',
        re.MULTILINE
    )
    if not pat_registry.search(html):
        print("❌ Không tìm thấy `var DATASET_REGISTRY = {`")
        sys.exit(1)

    inject_entries = ""
    for ds in new_datasets:
        entry_json = _escape_json_for_script(ds)
        inject_entries += f'"{ds["id"]}":{entry_json},'

    html, n = pat_registry.subn(r'\1\2' + inject_entries, html, count=1)
    if n == 0:
        print("❌ Không chèn được registry entries.")
        sys.exit(1)
    print(f"   ✅ Đã chèn {len(new_datasets)} entry")

    # ═══════════════════════════════════════════════════════════════
    #  PATCH 2: Thêm <button> cho từng tab vào .ds-main-row
    # ═══════════════════════════════════════════════════════════════
    print("\n🔨 PATCH 2: Thêm button tabs vào .ds-main-row...")

    new_btns_html = ""
    for ds in new_datasets:
        label = f'{ds["name"]} · {ds["count"]} câu'
        new_btns_html += (
            f'\n        <button class="ds-btn ds-btn-primary" '
            f'data-dataset="{ds["id"]}">\n'
            f'            <i class="fas {ds["icon"]}"></i>\n'
            f'            <span>{_js_str(label)}</span>\n'
            f'        </button>\n    '
        )

    # Chèn TRƯỚC nút "chuyen-nganh"
    pat_btn = re.compile(
        r'(\s*)(<button\s+class="[^"]*ds-btn[^"]*"\s+[^>]*data-dataset-group="chuyen-nganh")',
        re.MULTILINE
    )
    html, n = pat_btn.subn(r'\1' + new_btns_html + r'\2', html, count=1)
    if n == 0:
        print("❌ Không tìm thấy nút 'chuyen-nganh' để chèn trước.")
        sys.exit(1)
    print(f"   ✅ Đã chèn {len(new_datasets)} tab button")

    # ═══════════════════════════════════════════════════════════════
    #  PATCH 3: Override CSS layout (auto-fit cho N tab)
    # ═══════════════════════════════════════════════════════════════
    print("\n🔨 PATCH 3: Override CSS layout (auto-fit)...")

    # Sinh màu cho mỗi dataset
    color_css = ""
    for ds in new_datasets:
        dsid = ds["id"]
        color = ds["color"]
        color_css += f"""
.ds-btn[data-dataset="{dsid}"] {{
    background: linear-gradient(135deg,
        color-mix(in srgb, {color} 12%, var(--surface)),
        color-mix(in srgb, {color} 4%, var(--surface))) !important;
    border-color: color-mix(in srgb, {color} 40%, var(--border)) !important;
}}
.ds-btn[data-dataset="{dsid}"] i:first-child {{
    color: {color} !important;
}}
.ds-btn[data-dataset="{dsid}"]:hover {{
    border-color: {color} !important;
    background: linear-gradient(135deg,
        color-mix(in srgb, {color} 20%, var(--surface)),
        color-mix(in srgb, {color} 8%, var(--surface))) !important;
}}
.ds-btn[data-dataset="{dsid}"].active {{
    background: linear-gradient(135deg, {color},
        color-mix(in srgb, {color} 72%, #000)) !important;
    color: #fff !important;
    border-color: {color} !important;
    box-shadow: 0 4px 12px color-mix(in srgb, {color} 40%, transparent) !important;
}}
.ds-btn[data-dataset="{dsid}"].active i:first-child {{
    color: #fff !important;
}}
[data-theme="dark"] .ds-btn[data-dataset="{dsid}"] {{
    background: linear-gradient(135deg,
        color-mix(in srgb, {color} 20%, var(--surface)),
        color-mix(in srgb, {color} 8%, var(--surface))) !important;
    border-color: color-mix(in srgb, {color} 50%, var(--border)) !important;
}}
[data-theme="dark"] .ds-btn[data-dataset="{dsid}"].active {{
    background: linear-gradient(135deg, {color},
        color-mix(in srgb, {color} 72%, #000)) !important;
    border-color: {color} !important;
}}
"""

    css_override = f"""
/* ═══════════════════════════════════════════════════════════════════
   ★★ FIX.PY: AUTO-FIT LAYOUT CHO N TAB ★★
   Số cột tự động theo số tab — PC nhiều cột, mobile 2 cột.
   ═══════════════════════════════════════════════════════════════════ */

/* Mobile: 2 cột cố định */
@media (max-width: 768px) {{
    .ds-main-row {{
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: .5rem !important;
    }}
}}

/* PC nhỏ (769-1100): 3 cột */
@media (min-width: 769px) and (max-width: 1100px) {{
    .ds-main-row {{
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: .55rem !important;
    }}
}}

/* PC lớn (>=1101): auto-fit — tự chia cột theo không gian */
@media (min-width: 1101px) {{
    .ds-main-row {{
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) !important;
        gap: .6rem !important;
    }}
}}

/* Màu riêng cho từng tab mới */
{color_css}
"""

    pat_style = re.compile(r'(\s*)(</style>)', re.MULTILINE)
    html, n = pat_style.subn(r'\1' + css_override + r'\1\2', html, count=1)
    if n == 0:
        print("⚠️  Không tìm thấy </style> — bỏ qua PATCH CSS.")
    else:
        print("   ✅ Đã override CSS auto-fit")

    # ═══════════════════════════════════════════════════════════════
    #  PATCH 4: Inject JS binding cho tất cả tab mới
    # ═══════════════════════════════════════════════════════════════
    print("\n🔨 PATCH 4: Inject JS binding...")

    new_ids_js = json.dumps([ds["id"] for ds in new_datasets])

    js_override = f"""
<script>
/* ═══════════════════════════════════════════════════════════════════
   ★★ FIX.PY OVERRIDE: Bind các tab mới từ data/ ★★
   Chạy SAU tất cả JS gốc. Không đụng vào code main.py.
   ═══════════════════════════════════════════════════════════════════ */
(function() {{
    'use strict';

    var NEW_IDS = {new_ids_js};

    function bindTab(dsId) {{
        var btn = document.querySelector('.ds-btn[data-dataset="' + dsId + '"]');
        if (!btn || btn.__fixPyBound) return;
        btn.__fixPyBound = true;

        btn.addEventListener('click', function() {{
            /* Đóng dropdown chuyên ngành */
            var sub = document.getElementById('dsSubWrap');
            if (sub) sub.style.display = 'none';

            /* Xoá active mọi nơi */
            document.querySelectorAll('.ds-btn, .ds-sub-btn').forEach(function(b) {{
                b.classList.remove('active');
            }});

            /* Active tab này */
            this.classList.add('active');

            /* Switch dataset — gọi đúng hàm global */
            var switchFn = window.switchDataset || (typeof switchDataset !== 'undefined' ? switchDataset : null);
            if (typeof switchFn === 'function') {{
                switchFn(dsId);
            }} else {{
                console.warn('⚠️ Không tìm thấy switchDataset()');
            }}
        }});
    }}

    function bindAll() {{
        NEW_IDS.forEach(bindTab);
        patchMarkActive();
    }}

    /* Đảm bảo markCurrentDatasetActive nhận diện các tab mới */
    function patchMarkActive() {{
        if (window.__fixPyMarkPatched) return;
        var origMark = window.markCurrentDatasetActive
                     || (typeof markCurrentDatasetActive !== 'undefined' ? markCurrentDatasetActive : null);
        if (typeof origMark !== 'function') return;

        window.markCurrentDatasetActive = function() {{
            origMark.apply(this, arguments);
            var cur = (typeof CURRENT_DATASET !== 'undefined') ? CURRENT_DATASET : 'tonghop';
            document.querySelectorAll('.ds-btn[data-dataset]').forEach(function(b) {{
                b.classList.toggle('active', b.dataset.dataset === cur);
            }});
        }};
        window.__fixPyMarkPatched = true;
    }}

    /* Init */
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', bindAll);
    }} else {{
        bindAll();
    }}

    /* Re-bind khi DOM thay đổi (an toàn cho SPA-like updates) */
    var _timer = null;
    var observer = new MutationObserver(function() {{
        clearTimeout(_timer);
        _timer = setTimeout(bindAll, 200);
    }});
    if (document.body) {{
        observer.observe(document.body, {{ childList: true, subtree: true }});
    }}

    console.log('✅ fix.py: đã bind ' + NEW_IDS.length + ' tab mới:', NEW_IDS);
}})();
</script>
"""

    pat_body = re.compile(r'(\s*)(</body>)', re.IGNORECASE)
    html, n = pat_body.subn(r'\1' + js_override + r'\1\2', html, count=1)
    if n == 0:
        print("❌ Không tìm thấy </body> để chèn JS.")
        sys.exit(1)
    print("   ✅ Đã inject JS binding")

    # ═══════════════════════════════════════════════════════════════
    #  GHI FILE
    # ═══════════════════════════════════════════════════════════════
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = os.path.getsize(INDEX_HTML) / 1024
    print("\n" + "=" * 62)
    print(f"🎉 HOÀN TẤT! Đã patch {INDEX_HTML}")
    print(f"📦 Kích thước: {size_kb:.1f} KB")
    print(f"➕ Đã thêm {len(new_datasets)} tab mới")
    for ds in new_datasets:
        print(f"   • {ds['name']} ({ds['count']} câu)")
    print(f"🎨 Layout: PC auto-fit (200px/cột) · Mobile 2 cột")
    print("=" * 62)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Chuyển file Excel → HTML tự chứa dữ liệu.
Ghép 4 template: ui + social + accounts (gộp renewal) + data.
"""
import json
import os
import sys

# ═══════════════════════════════════════════════════════════════════
#  IMPORT MODULES
# ═══════════════════════════════════════════════════════════════════
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_loader import load_config, print_banner, CONFIG_FILE
from data_reader import read_excel
from ui_template import build_ui_css, build_ui_html, build_ui_js
from social_template import (
    build_social_css, build_social_html, build_social_js,
    build_tiktok_bar_html
)
# ✅ CHỈ CÒN 1 MODULE ACCOUNTS (đã gộp renewal)
from accounts_template import (
    build_accounts_css,
    build_accounts_html,
    build_accounts_js,
    build_all_auth,  # helper gộp CSS+HTML+JS
)


# ═══════════════════════════════════════════════════════════════════
#  LOAD CONFIG + DATA
# ═══════════════════════════════════════════════════════════════════
CONFIG = load_config()
print_banner(CONFIG)

EXCEL_FILE = CONFIG["excel_file"]
OUTPUT_HTML = CONFIG["output_html"]
SHEET_INDEX = CONFIG["sheet_index"]

data = read_excel(EXCEL_FILE, SHEET_INDEX)

json_data = json.dumps(data, ensure_ascii=True, separators=(',', ':'))
json_data = json_data.replace('</', '<\\/')
firebase_config_json = json.dumps(CONFIG["firebase_config"], ensure_ascii=False)
synonyms_json = json.dumps(CONFIG["synonyms"], ensure_ascii=True, separators=(',', ':'))
fillers_json = json.dumps(CONFIG["filler_words"], ensure_ascii=True, separators=(',', ':'))


# ═══════════════════════════════════════════════════════════════════
#  BUILD AUTH (CSS + HTML + JS) — 1 LẦN DUY NHẤT
# ═══════════════════════════════════════════════════════════════════
auth_css, auth_html, auth_js = build_all_auth(CONFIG)


# ═══════════════════════════════════════════════════════════════════
#  GHÉP CSS (3 khối: ui + social + auth)
# ═══════════════════════════════════════════════════════════════════
full_css = (
    build_ui_css()
    + "\n/* ==== SOCIAL CSS ==== */\n" + build_social_css()
    + "\n/* ==== ACCOUNTS + RENEWAL CSS ==== */\n" + auth_css
)


# ═══════════════════════════════════════════════════════════════════
#  GHÉP HTML BODY
# ═══════════════════════════════════════════════════════════════════
ui_html = build_ui_html()
ui_html = ui_html.replace("<!-- __TIKTOK_BAR__ -->", build_tiktok_bar_html())

social_html = build_social_html()
ui_html = ui_html.replace(
    '<div class="writer-modal" id="writerModal">',
    social_html + '\n<div class="writer-modal" id="writerModal">'
)

# ✅ Auth HTML đã chứa cả login modal + renewal modal + admin panel
full_body = ui_html + "\n" + auth_html


# ═══════════════════════════════════════════════════════════════════
#  GHÉP JS (3 khối: ui + social + auth đã inject config)
# ═══════════════════════════════════════════════════════════════════
full_js = (
    build_ui_js()
    + "\n/* ==== SOCIAL JS ==== */\n" + build_social_js()
    + "\n/* ==== ACCOUNTS + RENEWAL JS ==== */\n" + auth_js
)


# ═══════════════════════════════════════════════════════════════════
#  HTML SHELL
# ═══════════════════════════════════════════════════════════════════
HTML_SHELL = r'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, viewport-fit=cover">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<title>Học tiếng Trung · Văn phòng &amp; Công xưởng</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-auth-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/10.7.0/firebase-firestore-compat.js"></script>
<script src="https://cdn.jsdelivr.net/npm/hanzi-writer@3.5.0/dist/hanzi-writer.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
<style>
__CSS__
</style>
</head>
<body>

__BODY__

<script>
/* ============ DỮ LIỆU + CONFIG ============ */
var RAW_DATA = __DATA__;
var FIREBASE_CONFIG = __FIREBASE_CONFIG__;
var DEMO_LIMIT = __DEMO_LIMIT__;
var DEMO_DAILY_LIMIT = __DEMO_DAILY_LIMIT__;
var DEMO_HSK_MAX = __DEMO_HSK_MAX__;
var TARGET_ADMINS = __TARGET_ADMINS__;
var SUPER_ADMIN = "__SUPER_ADMIN__";
var ZALO_PHONE = "__ZALO_PHONE__";
var ZALO_NAME = "__ZALO_NAME__";
var TIKTOK_USERNAME = "__TIKTOK_USERNAME__";
var TIKTOK_NICKNAME = "__TIKTOK_NICKNAME__";
var TIKTOK_AVATAR = "__TIKTOK_AVATAR__";
var TIKTOK_URL = "__TIKTOK_URL__";
var SYNONYMS = __SYNONYMS__;
var FILLER_WORDS = __FILLER_WORDS__;

/* Helper $ toàn cục */
var $ = function(id) { return document.getElementById(id); };

__JS__
</script>
</body>
</html>'''


# ═══════════════════════════════════════════════════════════════════
#  RENDER + GHI FILE
# ═══════════════════════════════════════════════════════════════════
html_output = (HTML_SHELL
    .replace("__CSS__", full_css)
    .replace("__BODY__", full_body)
    .replace("__JS__", full_js)
    .replace("__DATA__", json_data)
    .replace("__FIREBASE_CONFIG__", firebase_config_json)
    .replace("__DEMO_LIMIT__", str(CONFIG["demo_limit"]))
    .replace("__DEMO_DAILY_LIMIT__", str(CONFIG["demo_daily_limit"]))
    .replace("__DEMO_HSK_MAX__", str(CONFIG["demo_hsk_max"]))
    .replace("__TARGET_ADMINS__", str(CONFIG["target_admins"]))
    .replace("__SUPER_ADMIN__", CONFIG["super_admin"])
    .replace("__ZALO_PHONE__", CONFIG["zalo_phone"])
    .replace("__ZALO_NAME__", CONFIG["zalo_name"])
    .replace("__TIKTOK_USERNAME__", CONFIG["tiktok_username"])
    .replace("__TIKTOK_NICKNAME__", CONFIG["tiktok_nickname"])
    .replace("__TIKTOK_AVATAR__", CONFIG["tiktok_avatar"])
    .replace("__TIKTOK_URL__", CONFIG["tiktok_url"])
    .replace("__SYNONYMS__", synonyms_json)
    .replace("__FILLER_WORDS__", fillers_json)
)

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_output)

size_kb = os.path.getsize(OUTPUT_HTML) / 1024
print(f"\n🎉 Đã tạo: {OUTPUT_HTML}")
print(f"📦 Kích thước: {size_kb:.1f} KB")
print(f"📚 Tổng số câu: {len(data)}")
print(f"🎁 Demo: {CONFIG['demo_limit']} câu + HSK1-{CONFIG['demo_hsk_max']} + {CONFIG['demo_daily_limit']} lượt")
print(f"🔥 Firebase: {CONFIG['firebase_config'].get('projectId', 'N/A')}")
print(f"👑 Super admin: {CONFIG['super_admin']}")
print(f"🎉 Trial: {CONFIG['trial_days']} ngày cho user mới")
print(f"🏦 Bank: {CONFIG['bank_config']['bank_name']} - {CONFIG['bank_config']['account_no']}")
print(f"💰 Packages: {len(CONFIG['packages'])} gói")
print(f"✅ Đã ghép 4 template: UI + Social + Auth (gộp Renewal) + Data")

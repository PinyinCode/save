# -*- coding: utf-8 -*-
"""
Chuyển file Excel → HTML tự chứa dữ liệu.
Ghép 4 template: ui + social + accounts (gộp renewal) + data.

✅ QUY TẮC MỚI:
   - Mobile (≤ 768px): 1 cột card.
   - Máy tính (≥ 769px): 2 cột card.
   - Tự scale theo độ phân giải (clamp, vh, media queries).
   - Header KHÔNG dùng position:sticky để tránh đè nội dung.
   - Chế độ Full không chồng lấn: header/filters/nav flex:0 0 auto,
     body flex:1 1 auto + overflow-y:auto.
   - Ô đánh chữ trong chế độ Full là trung tâm lớn nhất.
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
from accounts_template import (
    build_accounts_css,
    build_accounts_html,
    build_accounts_js,
    build_all_auth,
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

telegram_bot_token = CONFIG.get("telegram_bot_token", "")
telegram_chat_id = CONFIG.get("telegram_chat_id", "")


# ═══════════════════════════════════════════════════════════════════
#  BUILD AUTH (CSS + HTML + JS) — 1 LẦN DUY NHẤT
# ═══════════════════════════════════════════════════════════════════
auth_css, auth_html, auth_js = build_all_auth(CONFIG)


# ═══════════════════════════════════════════════════════════════════
#  ★ FULLWIDTH SCALE CSS ★
#  Đặt cuối cùng trong full_css để override mọi CSS từ ui/social/auth.
#  Bao gồm: header, search, filter, cards, banner — tất cả tự co giãn
#  vừa chiều ngang màn hình.
#
#  ★ QUY TẮC MỚI:
#    - Mobile (≤ 768px): 1 cột card.
#    - Máy tính (≥ 769px): 2 cột card.
#    - Màn hình siêu rộng: mở rộng 3-4 cột (vẫn giữ tinh thần 2 cột).
#    - Header KHÔNG sticky để tránh đè nội dung.
#    - Chế độ Full: header/filters/nav không co giãn, body cuộn.
# ═══════════════════════════════════════════════════════════════════
FULLWIDTH_CSS = r"""

/* ═══════════════════════════════════════════════════════════════════
   ★ FULL-WIDTH SCALE (v2) ★
   Quy tắc mới:
   - Mobile (≤ 768px): 1 cột
   - Máy tính (≥ 769px): 2 cột
   - Chế độ Full không chồng lấn (đã fix trong ui_template)
   ═══════════════════════════════════════════════════════════════════ */

.page-wrap {
    width: 100%;
    max-width: 100%;
    margin: 0 auto;
    overflow-x: hidden;
}

.container {
    width: 100% !important;
    max-width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: 1.25rem !important;
    padding-right: 1.25rem !important;
}

/* ★ QUAN TRỌNG: Bỏ sticky để không đè nội dung ★ */
.sticky-top {
    position: relative !important;
    width: 100% !important;
    max-width: 100% !important;
}

.main,
#mainContent {
    width: 100% !important;
    max-width: 100% !important;
}

/* ═══ HEADER SCALE ═══ */
.header-inner {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    gap: 1rem !important;
    width: 100% !important;
}
.logo {
    flex: 1 1 auto !important;
    min-width: 0 !important;
}
.header-actions {
    flex: 0 0 auto !important;
    margin-left: auto !important;
    display: flex !important;
    gap: .5rem !important;
    align-items: center !important;
}

/* ═══ SEARCH + FILTER ═══ */
.search-bar { width: 100% !important; max-width: 100% !important; }
.search-bar input { width: 100% !important; max-width: 100% !important; }

.filters {
    display: grid !important;
    width: 100% !important;
    max-width: 100% !important;
    grid-template-columns: 1fr 1fr !important;
    gap: .75rem !important;
}
@media (min-width: 1000px) {
    .filters {
        grid-template-columns: 220px 260px !important;
        gap: 1rem !important;
    }
}

.result-count { margin-top: .5rem !important; }

/* ═══════════════════════════════════════════════════════════════════
   ★ GRID CARDS: 1 CỘT MOBILE — 2 CỘT MÁY TÍNH ★
   ═══════════════════════════════════════════════════════════════════ */
.mobile-view {
    display: grid !important;
    width: 100% !important;
    max-width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    gap: 1rem !important;
    /* Mặc định mobile: 1 cột */
    grid-template-columns: 1fr !important;
}

/* Máy tính: 2 cột */
@media (min-width: 769px) {
    .mobile-view {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
        gap: 1.1rem !important;
    }
}

/* Màn hình rất rộng: 3 cột (vẫn giữ tinh thần 2 cột chính) */
@media (min-width: 1800px) {
    .mobile-view {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 1.2rem !important;
    }
}
@media (min-width: 2400px) {
    .mobile-view {
        grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
        gap: 1.3rem !important;
    }
}

/* ═══ Banner full width ═══ */
.demo-banner,
.expiry-banner {
    width: 100% !important;
    max-width: 100% !important;
    margin-left: auto !important;
    margin-right: auto !important;
    margin-bottom: 1rem !important;
}

/* ═══ Container padding co giãn ═══ */
@media (min-width: 1000px) {
    .container { padding-left: 1.5rem !important; padding-right: 1.5rem !important; }
}
@media (min-width: 1400px) {
    .container { padding-left: 2rem !important; padding-right: 2rem !important; }
}
@media (min-width: 1900px) {
    .container { padding-left: 2.5rem !important; padding-right: 2.5rem !important; }
}

/* ═══ MOBILE: thu gọn padding ═══ */
@media (max-width: 768px) {
    .container { padding-left: .7rem !important; padding-right: .7rem !important; }
    .mobile-view { gap: .8rem !important; }
    .header-inner { gap: .5rem !important; }
}

/* ═══════════════════════════════════════════════════════════════════
   ★ CHẾ ĐỘ FULL: ô đánh chữ là trung tâm, không chồng lấn ★
   ═══════════════════════════════════════════════════════════════════ */
.practice-full-modal {
    position: fixed !important;
    inset: 0 !important;
    z-index: 2500 !important;
    display: none;
    flex-direction: column !important;
    overflow: hidden !important;
}
.practice-full-modal.show { display: flex !important; }

.practice-full-header,
.pf-filters,
.practice-full-nav {
    flex: 0 0 auto !important; /* Không co giãn */
}

.practice-full-body {
    flex: 1 1 auto !important; /* Chiếm hết phần còn lại */
    min-height: 0 !important;  /* Cho phép overflow hoạt động */
    overflow-y: auto !important;
}

/* Ô đánh chữ lớn nhất, căn giữa */
.practice-full-input {
    width: 100% !important;
    text-align: center !important;
    font-size: clamp(1.15rem, 2.2vw, 1.6rem) !important;
}
"""


# ═══════════════════════════════════════════════════════════════════
#  GHÉP CSS (3 khối + Fullwidth override cuối)
# ═══════════════════════════════════════════════════════════════════
full_css = (
    build_ui_css()
    + "\n/* ==== SOCIAL CSS ==== */\n" + build_social_css()
    + "\n/* ==== ACCOUNTS + RENEWAL CSS ==== */\n" + auth_css
    + "\n/* ==== FULLWIDTH SCALE (override cuối) ==== */\n" + FULLWIDTH_CSS
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

# Bọc toàn bộ body trong .page-wrap để cô lập layout
# (modals dùng position:fixed nên KHÔNG bị ảnh hưởng)
full_body = (
    '<div class="page-wrap">\n'
    + ui_html
    + "\n" + auth_html
    + '\n</div>'
)


# ═══════════════════════════════════════════════════════════════════
#  GHÉP JS
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

/* ═══ DEMO TIER ═══ */
var DEMO_LIMIT = __DEMO_LIMIT__;
var DEMO_DAILY_LIMIT = __DEMO_DAILY_LIMIT__;
var DEMO_HSK_MAX = __DEMO_HSK_MAX__;

/* ═══ TRIAL TIER ═══ */
var TRIAL_MAX_QUESTIONS = __TRIAL_MAX_QUESTIONS__;
var TRIAL_MAX_HSK = __TRIAL_MAX_HSK__;
var TRIAL_UNLIMITED_WRITING = __TRIAL_UNLIMITED_WRITING__;

/* ═══ KHÁC ═══ */
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

<!-- ═══════════════════════════════════════════════════════════════
     TELEGRAM MODULE — SCRIPT RIÊNG BIỆT
     Không ảnh hưởng đến script chính phía trên
     ═══════════════════════════════════════════════════════════════ -->
<script>
(function() {
    'use strict';
    try {
        var _TG_TOKEN = "__TELEGRAM_BOT_TOKEN__";
        var _TG_CHAT = "__TELEGRAM_CHAT_ID__";

        console.log('📲 Telegram module init:', {
            hasToken: _TG_TOKEN && _TG_TOKEN.indexOf('__') !== 0 && _TG_TOKEN.length > 20,
            tokenPreview: _TG_TOKEN ? _TG_TOKEN.substring(0, 15) + '...' : '(empty)',
            chatId: _TG_CHAT || '(empty)'
        });

        window.sendTelegramMessage = function(text) {
            try {
                if (!_TG_TOKEN || !_TG_CHAT || _TG_TOKEN.indexOf('__') === 0 || _TG_TOKEN.length < 20) {
                    console.log('⚠️ Telegram chưa cấu hình — bỏ qua');
                    return;
                }
                fetch('https://api.telegram.org/bot' + _TG_TOKEN + '/sendMessage', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        chat_id: _TG_CHAT,
                        text: text,
                        parse_mode: 'HTML',
                        disable_web_page_preview: true
                    })
                })
                .then(function(r) { return r.json(); })
                .then(function(d) {
                    if (d.ok) console.log('✅ Telegram sent OK');
                    else console.warn('⚠️ Telegram error:', d.description);
                })
                .catch(function(e) { console.warn('❌ Telegram fetch:', e); });
            } catch(e) { console.warn('sendTelegramMessage:', e); }
        };

        window.notifyTelegramUserPaid = function(reqData) {
            try {
                var msg = '🔔 <b>CÓ YÊU CẦU GIA HẠN MỚI</b>\n';
                msg += '━━━━━━━━━━━━━━━━━━━━\n';
                msg += '👤 <b>' + (reqData.name || reqData.email) + '</b>\n';
                msg += '📧 <code>' + reqData.email + '</code>\n';
                msg += '💰 <b>' + (reqData.amount || 0).toLocaleString('vi-VN') + 'đ</b>\n';
                msg += '📦 ' + (reqData.packageLabel || reqData.package || '');
                if (reqData.isPermanent) msg += ' 💎 <b>VĨNH VIỄN</b>';
                msg += '\n';
                msg += '⏱ ' + (reqData.isPermanent ? 'Mãi mãi' : (reqData.days || 0) + ' ngày') + '\n';
                msg += '🔑 <code>' + (reqData.transferCode || '') + '</code>\n';
                msg += '⚡ <b>Vào Admin Panel xác nhận!</b>';
                window.sendTelegramMessage(msg);
            } catch(e) { console.warn('notifyTelegramUserPaid:', e); }
        };

        window.notifyTelegramAdminConfirmed = function(reqData, newExpiry) {
            try {
                var msg = '✅ <b>ĐÃ XÁC NHẬN GIA HẠN</b>\n';
                msg += '━━━━━━━━━━━━━━━━━━━━\n';
                msg += '👤 <b>' + (reqData.name || reqData.email) + '</b>\n';
                msg += '📧 <code>' + reqData.email + '</code>\n';
                msg += '💰 <b>' + (reqData.amount || 0).toLocaleString('vi-VN') + 'đ</b>\n';
                if (reqData.isPermanent) msg += '💎 <b>Đã kích hoạt VĨNH VIỄN</b>\n';
                else if (newExpiry) msg += '📅 Hạn mới: <b>' + newExpiry + '</b>\n';
                msg += '🕐 ' + new Date().toLocaleString('vi-VN');
                window.sendTelegramMessage(msg);
            } catch(e) { console.warn('notifyTelegramAdminConfirmed:', e); }
        };

        console.log('✅ Telegram module loaded');
    } catch(e) {
        console.error('❌ Telegram module failed (KHÔNG ảnh hưởng app):', e);
    }
})();
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
    # ═══ DEMO ═══
    .replace("__DEMO_LIMIT__", str(CONFIG["demo_limit"]))
    .replace("__DEMO_DAILY_LIMIT__", str(CONFIG["demo_daily_limit"]))
    .replace("__DEMO_HSK_MAX__", str(CONFIG["demo_hsk_max"]))
    # ═══ TRIAL ═══
    .replace("__TRIAL_MAX_QUESTIONS__", str(CONFIG.get("trial_max_questions", 50)))
    .replace("__TRIAL_MAX_HSK__", str(CONFIG.get("trial_max_hsk", 5)))
    .replace("__TRIAL_UNLIMITED_WRITING__",
             "true" if CONFIG.get("trial_unlimited_writing", True) else "false")
    # ═══ KHÁC ═══
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
    # ═══ Telegram ═══
    .replace("__TELEGRAM_BOT_TOKEN__", telegram_bot_token)
    .replace("__TELEGRAM_CHAT_ID__", telegram_chat_id)
)

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_output)

size_kb = os.path.getsize(OUTPUT_HTML) / 1024
print(f"\n🎉 Đã tạo: {OUTPUT_HTML}")
print(f"📦 Kích thước: {size_kb:.1f} KB")
print(f"📚 Tổng số câu: {len(data)}")
print(f"🎁 Demo: {CONFIG['demo_limit']} câu + HSK1-{CONFIG['demo_hsk_max']} + {CONFIG['demo_daily_limit']} lượt")
print(f"📚 Trial: {CONFIG.get('trial_max_questions', 50)} câu, HSK1-{CONFIG.get('trial_max_hsk', 5)}, "
      f"nghe viết {'KHÔNG' if CONFIG.get('trial_unlimited_writing', True) else 'CÓ'} giới hạn")
print(f"🔥 Firebase: {CONFIG['firebase_config'].get('projectId', 'N/A')}")
print(f"👑 Super admin: {CONFIG['super_admin']}")
print(f"🎉 Trial days: {CONFIG['trial_days']} ngày cho user mới")
print(f"🏦 Bank: {CONFIG['bank_config']['bank_name']} - {CONFIG['bank_config']['account_no']}")
print(f"💰 Packages: {len(CONFIG['packages'])} gói")
permanent_count = sum(1 for p in CONFIG['packages'] if p.get("permanent"))
if permanent_count:
    print(f"💎 Gói VĨNH VIỄN: {permanent_count}")
if telegram_bot_token and telegram_chat_id:
    print(f"📲 Telegram: ĐÃ bật (chat_id: {telegram_chat_id})")
else:
    print(f"📲 Telegram: CHƯA cấu hình (thiếu token hoặc chat_id)")
print(f"✅ Đã ghép 4 template + FULLWIDTH SCALE cho header/search/filter/cards")
print(f"🎨 Quy tắc: Mobile 1 cột | PC 2 cột | Full mode không chồng lấn")

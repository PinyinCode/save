# -*- coding: utf-8 -*-
"""
vocab_patch.py — Inject module Từ vựng HSK vào HTML.
KHÔNG đụng config.json. Path hardcode: data/tu_vung_hsk.xlsx
Phân quyền + giới hạn dùng chung ONBOARDING_CONFIG (đã có trong HTML).
"""
import os
import json
import re

from vocab_premium import (
    read_vocab_excel,
    build_vocab_css,
    build_vocab_tab_html,
    build_vocab_modal_html,
    build_vocab_js_override,
)


# ═══════════════════════════════════════════════════════════════════
#  CONFIG PATH — hardcode nhiều khả năng
# ═══════════════════════════════════════════════════════════════════
VOCAB_FILE_CANDIDATES = [
    "data/tu_vung_hsk.xlsx",
    "../data/tu_vung_hsk.xlsx",
    "scripts/data/tu_vung_hsk.xlsx",
    "tu_vung_hsk.xlsx",
]
VOCAB_ID = "tu-vung"


def _find_vocab_file():
    for p in VOCAB_FILE_CANDIDATES:
        if os.path.exists(p):
            return p
    return None


def _json_blob(obj):
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s.replace("</", "<\\/")


# ═══════════════════════════════════════════════════════════════════
#  CSS BANNER CẢNH BÁO
# ═══════════════════════════════════════════════════════════════════
def _build_warning_css():
    return r"""
/* ═══ BANNER CẢNH BÁO TỪ VỰNG ═══ */
.vocab-warning-banner {
    display: flex; align-items: center; gap: .85rem;
    padding: .85rem 1rem; margin-bottom: 1rem;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(251, 191, 36, .15), rgba(245, 158, 11, .08));
    border: 1.5px solid rgba(245, 158, 11, .45);
    animation: vocabWarnIn .4s cubic-bezier(.34, 1.56, .64, 1);
}
@keyframes vocabWarnIn {
    from { opacity: 0; transform: translateY(-10px); }
    to   { opacity: 1; transform: translateY(0); }
}
.vocab-warning-banner.tier-trial {
    background: linear-gradient(135deg, rgba(99, 102, 241, .12), rgba(139, 92, 246, .08));
    border-color: rgba(99, 102, 241, .45);
}
.vocab-warning-banner.tier-expired {
    background: linear-gradient(135deg, rgba(220, 38, 38, .12), rgba(251, 146, 60, .08));
    border-color: rgba(220, 38, 38, .5);
}
.vocab-warning-banner.tier-active {
    background: linear-gradient(135deg, rgba(8, 145, 178, .12), rgba(6, 182, 212, .08));
    border-color: rgba(8, 145, 178, .45);
}
.vocab-warning-icon {
    width: 40px; height: 40px; border-radius: 50%;
    background: linear-gradient(135deg, #fbbf24, #f59e0b);
    color: #fff; display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(245, 158, 11, .4);
}
.vocab-warning-banner.tier-trial .vocab-warning-icon {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    box-shadow: 0 4px 12px rgba(99, 102, 241, .4);
}
.vocab-warning-banner.tier-expired .vocab-warning-icon {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    box-shadow: 0 4px 12px rgba(220, 38, 38, .4);
}
.vocab-warning-banner.tier-active .vocab-warning-icon {
    background: linear-gradient(135deg, #0891b2, #06b6d4);
    box-shadow: 0 4px 12px rgba(8, 145, 178, .4);
}
.vocab-warning-text { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: .15rem; }
.vocab-warning-text strong { font-size: .92rem; font-weight: 800; color: #92400e; }
.vocab-warning-banner.tier-trial .vocab-warning-text strong { color: #4f46e5; }
.vocab-warning-banner.tier-expired .vocab-warning-text strong { color: #991b1b; }
.vocab-warning-banner.tier-active .vocab-warning-text strong { color: #075985; }
.vocab-warning-text span { font-size: .8rem; color: var(--text-2); line-height: 1.4; }
.vocab-warning-btn {
    padding: .55rem .9rem; border-radius: 10px; border: none;
    background: linear-gradient(135deg, #fbbf24, #f59e0b 50%, #ea580c);
    color: #fff; font-weight: 800; font-size: .8rem;
    font-family: inherit; cursor: pointer;
    display: inline-flex; align-items: center; gap: .35rem;
    box-shadow: 0 4px 12px rgba(245, 158, 11, .4);
    transition: all .2s; white-space: nowrap; flex-shrink: 0;
}
.vocab-warning-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(245, 158, 11, .6);
}
[data-theme="dark"] .vocab-warning-banner {
    background: linear-gradient(135deg, rgba(251, 191, 36, .2), rgba(245, 158, 11, .1));
}
[data-theme="dark"] .vocab-warning-text strong { color: #fcd34d; }
[data-theme="dark"] .vocab-warning-banner.tier-trial .vocab-warning-text strong { color: #c4b5fd; }
[data-theme="dark"] .vocab-warning-banner.tier-expired .vocab-warning-text strong { color: #fca5a5; }
[data-theme="dark"] .vocab-warning-banner.tier-active .vocab-warning-text strong { color: #67e8f9; }
@media (max-width: 600px) {
    .vocab-warning-banner { flex-wrap: wrap; gap: .6rem; padding: .7rem .8rem; }
    .vocab-warning-icon { width: 34px; height: 34px; font-size: .95rem; }
    .vocab-warning-text strong { font-size: .85rem; }
    .vocab-warning-text span { font-size: .74rem; }
}
"""


# ═══════════════════════════════════════════════════════════════════
#  JS PATCH — PHÂN QUYỀN + GIỚI HẠN HSK + SỐ CÂU
# ═══════════════════════════════════════════════════════════════════
def _build_voc ===ab_js_patch(vocab_id):
    return r"""
/* ═════════════════════ '════════════════════════════════t══
   VOCAB PATCH — dùng ONrialBOARDING_CONFIG để phân quyền
   ═════')════════════════════════════════════════════════ tier══ */
(function() {
    'use strict';
    var VOCAB_ID = '__VOCAB_ID__';

    function getVocabAccess() {
        var cfg = (typeof ONBOARDING_CONFIG !== 'undefined' && ONBOARDING_CONFIG) || {};

        // Admin → full
        if (typeof currentUser !== 'undefined' && currentUser && currentUser.role === 'admin') {
            return { allowed: true, tier: 'admin',
                hskAllowed: [1,2,3,4,5,6,7,8,9], maxQuestions: -1,
                label: 'Admin — Toàn bộ HSK', warning: null };
        }
        // Premium / Permanent → full
        if (typeof currentUser !== 'undefined' && currentUser && currentUser.isPermanent === true) {
            return { allowed: true, tier: 'premium',
                hskAllowed: [1,2,3,4,5,6,7,8,9], maxQuestions: -1,
                label: 'Premium — Toàn bộ HSK', warning: null };
        }

        var tier = 'demo';
        if (typeof currentUser !== 'undefined' && currentUser) {
            if (currentUser.isTrial || currentUser.tier = 'trial';
            else if (currentUser.isExpiredOnly || currentUser.tier === 'expired') tier = 'expired';
            else tier = 'active';
        }

        var tierCfg = cfg[tier] || {};
        var hskArr = tierCfg.hsk_allowed || [];
        var maxQ = (typeof tierCfg.max_questions === 'number') ? tierCfg.max_questions : -1;
        var maxT = (typeof tierCfg.topics_per_user === 'number') ? tierCfg.topics_per_user : -1;
        var isUnlimited = (maxQ === -1 && maxT === -1);

        var hskRange = hskArr.length
            ? 'HSK ' + hskArr[0] + '-' + hskArr[hskArr.length - 1]
            : 'cơ bản';

        if (tier === 'expired') {
            return { allowed: false, tier: 'expired', hskAllowed: [], maxQuestions: 0,
                label: 'Tài khoản hết hạn',
                warning: 'Tài khoản đã hết hạn — gia hạn để tiếp tục dùng Từ vựng HSK.' };
        }

        if (tier === 'demo') {
            return { allowed: true, tier: 'demo', hskAllowed: hskArr, maxQuestions: maxQ,
                label: 'Demo — ' + hskRange,
                warning: 'Bản Demo giới hạn ' + hskRange + ' và tối đa ' +
                         (maxQ > 0 ? maxQ + ' từ' : 'một số từ') +
                         ' — đăng nhập để dùng đầy đủ.' };
        }

        if (tier === 'trial') {
            if (isUnlimited) {
                return { allowed: true, tier: 'trial',
                    hskAllowed: hskArr.length ? hskArr : [1,2,3,4,5,6,7,8,9],
                    maxQuestions: -1,
                    label: 'Trial — ' + hskRange, warning: null };
            }
            return { allowed: true, tier: 'trial', hskAllowed: hskArr, maxQuestions: maxQ,
                label: 'Trial — ' + hskRange,
                warning: 'Bản Trial giới hạn ' + hskRange + ' và ' +
                         (maxQ > 0 ? maxQ + ' từ' : 'một số từ') +
                         ' — nâng cấp Premium để mở toàn bộ.' };
        }

        // Active thường
        if (isUnlimited) {
            return { allowed: true, tier: 'active',
                hskAllowed: hskArr.length ? hskArr : [1,2,3,4,5,6,7,8,9],
                maxQuestions: -1,
                label: 'Active — ' + hskRange, warning: null };
        }
        return { allowed: true, tier: 'active', hskAllowed: hskArr, maxQuestions: maxQ,
            label: 'Active — ' + hskRange,
            warning: 'Bản Active giới hạn ' + hskRange + ' và ' +
                     (maxQ > 0 ? maxQ + ' từ' : 'một số từ') +
                     ' — nâng cấp Premium để mở toàn bộ.' };
    }

    function applyVocabLimits(list, access) {
        var result = list;
        // 1. Filter HSK
        if (access.hskAllowed && access.hskAllowed.length &&
            access.hskAllowed.length < 9) {
            var allowSet = {};
            access.hskAllowed.forEach(function(h) {
                allowSet['HSK' + h] = true;
                allowSet[String(h)] = true;
            });
            result = result.filter(function(r) {
                var h = (r.hsk || '').toString().toUpperCase().trim();
                var num = h.replace(/[^0-9]/g, '');
                if (!num) return true;
                return allowSet['HSK' + num] === true || allowSet[num] === true;
            });
        }
        // 2. Giới hạn số câu
        var maxQ = access.maxQuestions;
        if (typeof maxQ === 'number' && maxQ > 0 && result.length > maxQ) {
            result = result.slice(0, maxQ);
        }
        return result;
    }

    function _esc(s) {
        return (typeof escapeHtml === 'function')
            ? escapeHtml(s) : String(s == null ? '' : s);
    }

    function _isVocabMode() {
        return (typeof CURRENT_DATASET !== 'undefined') && CURRENT_DATASET === VOCAB_ID;
    }

    function updateTabLockState() {
        var btn = document.querySelector('.ds-btn[data-dataset="' + VOCAB_ID + '"]');
        if (!btn) return;
        var acc = getVocabAccess();
        var oldLock = btn.querySelector('.vocab-lock-icon');
        if (oldLock) oldLock.remove();
        var badge = btn.querySelector('.ds-vocab-badge');

        if (acc.allowed) {
            btn.classList.remove('vocab-locked');
            btn.classList.add('vocab-unlocked');
            btn.title = acc.label;
            if (badge) {
                badge.textContent = (acc.tier === 'admin' || acc.tier === 'premium')
                    ? 'PREMIUM' : (acc.tier === 'active' ? 'ACTIVE'
                    : (acc.tier === 'trial' ? 'TRIAL' : 'DEMO'));
            }
        } else {
            btn.classList.add('vocab-locked');
            btn.classList.remove('vocab-unlocked');
            btn.title = acc.label;
            var lock = document.createElement('i');
            lock.className = 'fas fa-lock vocab-lock-icon';
            btn.appendChild(lock);
        }
    }

    function injectVocabWarningBanner() {
        if (!_isVocabMode()) return;
        var old = document.getElementById('vocabWarningBanner');
        if (old) old.remove();

        var acc = getVocabAccess();
        if (!acc.warning) return;

        var main = document.getElementById('mainContent');
        if (!main) return;

        var limitedCount = 0, totalCount = 0;
        try {
            if (window.FIXPY_DATASETS && window.FIXPY_DATASETS[VOCAB_ID]) {
                var full = window.FIXPY_DATASETS[VOCAB_ID].data || [];
                totalCount = full.length;
                limitedCount = applyVocabLimits(full, acc).length;
            }
        } catch(e) {}

        var limitInfo = '';
        if (acc.maxQuestions > 0 && limitedCount > 0 && totalCount > limitedCount) {
            limitInfo = ' <span style="opacity:.75">(' +
                        limitedCount + '/' + totalCount + ' từ)</span>';
        }

        var icon = acc.tier === 'expired' ? 'fa-exclamation-triangle'
                 : acc.tier === 'trial' ? 'fa-hourglass-half'
                 : acc.tier === 'demo' ? 'fa-user'
                 : 'fa-info-circle';
        var btnLabel = acc.tier === 'expired' ? 'Gia hạn ngay'
                     : acc.tier === 'demo' ? 'Đăng nhập'
                     : 'Nâng cấp Premium';
        var btnFn = acc.tier === 'demo' ? 'vocabUpgradeLogin()'
                  : 'vocabUpgradeRenew()';

        var banner = document.createElement('div');
        banner.id = 'vocabWarningBanner';
        banner.className = 'vocab-warning-banner tier-' + acc.tier;
        banner.innerHTML =
            '<div class="vocab-warning-icon"><i class="fas ' + icon + '"></i></div>' +
            '<div class="vocab-warning-text">' +
                '<strong>' + _esc(acc.label) + limitInfo + '</strong>' +
                '<span>' + _esc(acc.warning) + '</span>' +
            '</div>' +
            '<button class="vocab-warning-btn" onclick="' + btnFn + '">' +
                '<i class="fas fa-crown"></i> ' + btnLabel +
            '</button>';
        main.insertBefore(banner, main.firstChild);
    }

    function bindVocabTab() {
        var btn = document.querySelector('.ds-btn[data-dataset="' + VOCAB_ID + '"]');
        if (!btn || btn.__vocabPatchBound) return;
        btn.__vocabPatchBound = true;

        btn.addEventListener('click', function() {
            setTimeout(function() {
                var acc = getVocabAccess();
                if (!acc.allowed) return;

                if (_isVocabMode() && window.FIXPY_DATASETS && window.FIXPY_DATASETS[VOCAB_ID]) {
                    var full = window.FIXPY_DATASETS[VOCAB_ID].data || [];
                    var limited = applyVocabLimits(full, acc);
                    if (limited.length !== full.length) {
                        RAW_DATA = limited;
                        if (typeof applyFilter === 'function') applyFilter();
                        if (typeof updateResultCount === 'function') updateResultCount();
                    }
                }
                updateTabLockState();
                injectVocabWarningBanner();
            }, 350);
        });
    }

    window.getVocabAccess = getVocabAccess;
    window.vocabUpdateLockState = updateTabLockState;
    window.vocabInjectWarning = injectVocabWarningBanner;

    function patchLoop() {
        if (typeof window.vocabUpgradeRenew === 'function') {
            window.vocabUpdateLockState = updateTabLockState;
            bindVocabTab();
            updateTabLockState();
            setInterval(function() {
                if (_isVocabMode()) injectVocabWarningBanner();
            }, 2000);
            console.log('[vocab-patch] ready — onboarding-based');
            return;
        }
        setTimeout(patchLoop, 300);
    }
    setTimeout(patchLoop, 800);
})();
"""


# ═══════════════════════════════════════════════════════════════════
#  HÀM CHÍNH
# ═══════════════════════════════════════════════════════════════════
def inject_vocab(html, config=None):
    """
    Đọc vocab Excel → inject CSS + tab + modal + JS vào HTML.
    Trả về HTML đã patch (hoặc giữ nguyên nếu lỗi).
    """
    # 1. Tìm file vocab
    vocab_file = _find_vocab_file()
    if not vocab_file:
        print(f"   ℹ️  Không tìm thấy file vocab — đã thử: {VOCAB_FILE_CANDIDATES}")
        return html

    print(f"   📖 Đọc vocab: {vocab_file}")

    # 2. Đọc Excel
    try:
        vocab_list = read_vocab_excel(vocab_file, start_row=3)
    except Exception as e:
        print(f"   ⚠️  Lỗi đọc vocab: {e}")
        return html

    if not vocab_list:
        print(f"   ℹ️  Vocab rỗng — bỏ qua")
        return html

    print(f"   ✓ Đọc {len(vocab_list)} từ vựng")

    # 3. CSS
    vocab_css = build_vocab_css(VOCAB_ID) + _build_warning_css()
    if "</style>" in html:
        last_style = html.rfind("</style>")
        html = (html[:last_style]
                + "\n/* ===== VOCAB PREMIUM CSS ===== */\n"
                + vocab_css
                + "\n" + html[last_style:])

    # 4. Tab button
    tab_html = build_vocab_tab_html(VOCAB_ID)
    if "<!-- __VOCAB_TAB__ -->" in html:
        html = html.replace("<!-- __VOCAB_TAB__ -->", tab_html)
        print("   ✓ Chèn tab qua placeholder")
    else:
        pat = re.compile(
            r'(<button[^>]*data-dataset-group="favorites"[^>]*>.*?</button>)',
            re.DOTALL
        )
        m = pat.search(html)
        if m:
            html = html[:m.end()] + "\n" + tab_html + html[m.end():]
            print("   ✓ Chèn tab sau Yêu thích")
        else:
            pat2 = re.compile(
                r'(<div[^>]*class="[^"]*ds-main-row[^"]*"[^>]*>)(.*?)(</div>)',
                re.DOTALL
            )
            def _repl(m2):
                return m2.group(1) + m2.group(2) + "\n" + tab_html + "\n" + m2.group(3)
            html, n = pat2.subn(_repl, html, count=1)
            if n:
                print("   ✓ Chèn tab cuối ds-main-row")
            else:
                print("   ⚠️  Không tìm được chỗ chèn tab vocab")

    # 5. Modal
    modal_html = build_vocab_modal_html()
    html = html.replace("</body>", modal_html + "\n</body>", 1)

    # 6. Inject DATASET_REGISTRY
    vocab_json = _json_blob(vocab_list)
    registry_inject = (
        "\n/* ===== VOCAB DATASET INJECT ===== */\n"
        "try {\n"
        "    if (typeof DATASET_REGISTRY === 'object' && DATASET_REGISTRY) {\n"
        "        DATASET_REGISTRY['" + VOCAB_ID + "'] = {\n"
        "            id: '" + VOCAB_ID + "',\n"
        "            name: 'Từ vựng HSK (" + str(len(vocab_list)) + " từ)',\n"
        "            icon: 'fa-book',\n"
        "            color: '#7c3aed',\n"
        "            data: " + vocab_json + ",\n"
        "            count: " + str(len(vocab_list)) + ",\n"
        "            premium: true\n"
        "        };\n"
        "        console.log('[vocab] dataset registered:', DATASET_REGISTRY['" + VOCAB_ID + "'].count, 'words');\n"
        "    }\n"
        "} catch(e) { console.warn('[vocab] registry inject fail:', e); }\n"
    )
    if "var CURRENT_DATASET = 'tonghop';" in html:
        html = html.replace(
            "var CURRENT_DATASET = 'tonghop';",
            "var CURRENT_DATASET = 'tonghop';\n" + registry_inject,
            1
        )
    else:
        html = html.replace(
            "var DATASET_REGISTRY = ",
            registry_inject + "\nvar DATASET_REGISTRY = ",
            1
        )

    # 7. JS module + patch
    base_js = build_vocab_js_override(VOCAB_ID)
    patch_js = _build_vocab_js_patch(VOCAB_ID)
    combined_js = (base_js + "\n" + patch_js)
    combined_js = combined_js.replace("<script>", "").replace("</script>", "")

    last_close = html.rfind("</script>")
    if last_close > 0:
        html = (html[:last_close]
                + "\n/* ===== VOCAB MODULE + PATCH ===== */\n"
                + combined_js
                + "\n" + html[last_close:])

    print(f"   👑 Vocab injected: {len(vocab_list)} từ (tab + modal + JS + phân quyền)")
    return html

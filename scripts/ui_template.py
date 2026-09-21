 # -*- coding: utf-8 -*-
"""
Template GIAO DIỆN HỌC: header, search, filter, card, practice full, writer.
🎨 CHỈ SỬA FILE NÀY KHI ĐỔI CẤU TRÚC GIAO DIỆN HỌC TẬP.
KHÔNG chứa login/admin/social/renewal (đã tách sang file khác).
"""


# ═══════════════════════════════════════════════════════════════════
#  CSS
# ═══════════════════════════════════════════════════════════════════
def build_ui_css():
    return r"""
*{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
:root{
    --bg:#f0f4f8;--surface:#fff;--surface-2:#f8fafc;--border:#e2e8f0;--border-strong:#cbd5e1;
    --text:#0f172a;--text-2:#475569;--text-3:#94a3b8;
    --primary:#2563eb;--primary-dark:#1d4ed8;--primary-light:#dbeafe;
    --success:#16a34a;--danger:#dc2626;--danger-light:#fee2e2;
    --amber:#f59e0b;--amber-light:#fef3c7;
    --zalo:#0068ff;
    --tiktok:#000;
    --tiktok-pink:#fe2c55;
    --tiktok-cyan:#25f4ee;
    --shadow-sm:0 1px 2px rgba(15,23,42,.04);--shadow:0 4px 12px rgba(15,23,42,.06);
    --shadow-fab:0 8px 24px rgba(15,23,42,.18);
    --radius:14px;--radius-sm:10px;--radius-full:999px;
    --font-zh:'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans SC',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
}
[data-theme="dark"]{
    --bg:#0f172a;--surface:#1e293b;--surface-2:#334155;--border:#334155;--border-strong:#475569;
    --text:#f1f5f9;--text-2:#cbd5e1;--text-3:#94a3b8;
    --primary:#3b82f6;--primary-dark:#2563eb;--primary-light:#1e3a8a;
    --danger-light:#7f1d1d;--amber-light:#78350f;
    --tiktok:#fff;
    --shadow-sm:0 1px 2px rgba(0,0,0,.3);--shadow:0 4px 12px rgba(0,0,0,.3);
    --shadow-fab:0 8px 24px rgba(0,0,0,.5);
}
html,body{height:100%}
body{
    font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',sans-serif;
    background:var(--bg);color:var(--text);line-height:1.5;font-size:15px;
    padding-bottom:calc(90px + env(safe-area-inset-bottom));
    transition:background .2s,color .2s;
}
.container{max-width:1100px;margin:0 auto;padding:0 1.5rem}
@media(min-width:1200px){.container{max-width:1050px}}
@media(min-width:1600px){.container{max-width:1200px}}
@media(min-width:2000px){.container{max-width:1300px}}

.loading-screen{
    position:fixed;inset:0;background:var(--bg);
    display:flex;align-items:center;justify-content:center;
    z-index:9998;flex-direction:column;gap:1rem;color:var(--text-2);
}
.loading-screen.hidden{display:none}
.loading-screen i{font-size:2.5rem;color:var(--primary);animation:spin 1s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}

.sticky-top{
    position:sticky;top:0;z-index:150;background:var(--bg);
    padding:.6rem 0 .7rem 0;transition:background .2s, box-shadow .2s, border-color .2s;
    border-bottom:1px solid transparent;
}
.sticky-top.scrolled{
    background:var(--surface);border-bottom-color:var(--border);
    box-shadow:0 4px 16px -8px rgba(15,23,42,.15);
}
[data-theme="dark"] .sticky-top.scrolled{box-shadow:0 4px 16px -8px rgba(0,0,0,.5)}

/* ============ HEADER ============ */
.header{background:transparent;border:none}
.header-inner{display:flex;align-items:center;gap:.75rem;margin-bottom:.5rem}
.logo{display:flex;align-items:center;gap:.85rem;flex:1;min-width:0}
.logo-icon{
    width:64px;height:64px;background:linear-gradient(135deg,#2563eb,#7c3aed 60%,#db2777);
    border-radius:16px;display:flex;align-items:center;justify-content:center;
    color:#fff;font-size:2rem;flex-shrink:0;
    box-shadow:0 8px 24px rgba(37,99,235,.4), inset 0 1px 0 rgba(255,255,255,.25);
    position:relative;overflow:hidden;
}
.logo-icon::after{
    content:'';position:absolute;inset:0;
    background:radial-gradient(circle at 30% 20%, rgba(255,255,255,.35), transparent 60%);
    pointer-events:none;
}
.logo-text{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:flex;flex-direction:column;line-height:1.15;min-width:0}
.logo-text .title{
    font-size:2rem;font-weight:900;letter-spacing:-.02em;line-height:1.15;color:var(--text);
}
.logo-text .subtitle{
    font-size:.95rem;color:var(--text-3);font-weight:700;margin-top:3px;
    letter-spacing:.01em;padding-left:1.1rem;
}
.header-actions{display:flex;gap:.4rem;align-items:center;flex-shrink:0}

.icon-btn{
    width:38px;height:38px;border-radius:10px;border:1px solid var(--border);
    background:var(--surface);color:var(--text-3);cursor:pointer;
    display:flex;align-items:center;justify-content:center;font-size:.9rem;
    transition:.15s;position:relative;flex-shrink:0;
}
.icon-btn:hover,.icon-btn:active{background:var(--surface-2);color:var(--primary);border-color:var(--primary)}
.icon-btn.hidden{display:none}
.icon-btn.reset-btn:hover,.icon-btn.reset-btn:active{background:var(--danger-light);color:var(--danger);border-color:var(--danger)}
.icon-btn .badge{
    position:absolute;top:-4px;right:-4px;min-width:16px;height:16px;border-radius:50%;
    background:var(--danger);color:#fff;font-size:.6rem;font-weight:700;
    display:flex;align-items:center;justify-content:center;padding:0 4px;
    border:2px solid var(--surface);
}
.icon-btn:not(.has-badge) .badge{display:none}

.demo-badge{
    display:flex;align-items:center;gap:.35rem;
    padding:.4rem .75rem;border-radius:50px;
    background:var(--amber-light);color:#92400e;
    font-size:.72rem;font-weight:700;text-transform:uppercase;letter-spacing:.3px;
    border:1px solid rgba(245,158,11,.4);
}
[data-theme="dark"] .demo-badge{color:#fcd34d}

/* ============ SEARCH + FILTER ============ */
.search-bar{position:relative;margin-bottom:.55rem}
.search-bar i.fa-search{
    position:absolute;left:14px;top:50%;transform:translateY(-50%);
    color:var(--text-3);font-size:.9rem;pointer-events:none;
}
.search-bar input{
    width:100%;padding:.7rem 2.6rem .7rem 2.5rem;
    border-radius:var(--radius-full);border:1.5px solid var(--border);
    background:var(--surface);color:var(--text);font-size:.92rem;
    outline:none;transition:.15s;box-shadow:var(--shadow-sm);
    -webkit-appearance:none;font-family:inherit;
}
.search-bar input:focus{border-color:var(--primary);box-shadow:0 0 0 4px rgba(37,99,235,.15)}
.search-bar input::placeholder{color:var(--text-3)}
.search-clear{
    position:absolute;right:8px;top:50%;transform:translateY(-50%);
    width:30px;height:30px;border-radius:50%;border:none;
    background:var(--surface-2);color:var(--text-2);
    cursor:pointer;display:none;align-items:center;justify-content:center;font-size:.8rem;
}
.search-clear.show{display:flex}

.filters{display:grid;grid-template-columns:1fr 1fr;gap:.5rem;max-width:600px}
.chip{
    display:flex;align-items:center;gap:.4rem;
    padding:.55rem .95rem;border-radius:var(--radius-full);
    border:1.5px solid var(--border);background:var(--surface);
    color:var(--text);font-size:.85rem;font-weight:500;
    cursor:pointer;transition:.15s;outline:none;font-family:inherit;
    min-width:0;box-shadow:var(--shadow-sm);-webkit-appearance:none;
    text-align:left;position:relative;overflow:hidden;
}
.chip:active{transform:scale(.98)}
.chip.has-value{background:var(--primary);color:#fff;border-color:var(--primary);box-shadow:0 4px 12px rgba(37,99,235,.3)}
.chip.has-value .chip-label{color:#fff;opacity:.85}
.chip-label{font-size:.7rem;color:var(--text-3);text-transform:uppercase;letter-spacing:.3px;font-weight:700;flex-shrink:0}
.chip-value{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;min-width:0;color:inherit}
.chip-arrow{color:inherit;opacity:.5;font-size:.7rem;flex-shrink:0}
.chip select{
    position:absolute;inset:0;opacity:0;cursor:pointer;font-size:1rem;
    -webkit-appearance:none;appearance:none;width:100%;height:100%;
}
.chip.demo-limited{border-color:var(--amber)}
.chip.demo-limited::before{
    content:'\f023';font-family:'Font Awesome 6 Free';font-weight:900;
    position:absolute;top:4px;right:6px;
    color:var(--amber);font-size:.6rem;pointer-events:none;z-index:2;
}

.result-count{
    display:none;align-items:center;gap:.4rem;margin-top:.5rem;
    padding:.45rem .85rem;border-radius:var(--radius-full);
    background:var(--surface-2);border:1px solid var(--border);
    color:var(--text-2);font-size:.8rem;font-weight:600;
    width:fit-content;box-shadow:var(--shadow-sm);transition:.2s;
}
.result-count.show{display:inline-flex}
.result-count i{color:var(--primary);font-size:.85rem}
.result-count b{color:var(--primary);font-weight:800}
.result-count.empty{background:var(--danger-light);border-color:rgba(220,38,38,.3);color:var(--danger)}
.result-count.empty i,.result-count.empty b{color:var(--danger)}

/* ============ FAB GROUP ============ */
.fab-group{
    position:fixed;bottom:calc(20px + env(safe-area-inset-bottom));
    right:20px;z-index:1000;display:flex;flex-direction:column;
    gap:.5rem;align-items:flex-end;pointer-events:none;
}
.fab-group > *{pointer-events:auto}
.fab-btn{
    width:52px;height:52px;border-radius:50%;border:none;
    background:var(--surface);color:var(--text-2);cursor:pointer;
    display:flex;align-items:center;justify-content:center;
    font-size:1.15rem;box-shadow:var(--shadow-fab);
    transition:transform .2s, background .2s, color .2s;
    position:relative;border:2px solid var(--surface);
}
.fab-btn:hover{transform:scale(1.08);background:var(--primary-light);color:var(--primary-dark)}
.fab-btn:active{transform:scale(0.95);background:var(--primary-light);color:var(--primary-dark)}
.fab-btn.active{background:var(--primary);color:#fff;border-color:var(--primary);box-shadow:0 8px 24px rgba(37,99,235,.4)}
.fab-btn.active:hover{background:var(--primary-dark);color:#fff}
.fab-btn.active:active{background:var(--primary-dark);color:#fff;transform:scale(0.95)}

.fab-main{
    width:56px;height:56px;font-size:1.3rem;
    background:linear-gradient(135deg,#2563eb,#7c3aed);
    color:#fff;border:none;box-shadow:0 8px 24px rgba(37,99,235,.4);
}
.fab-main:hover,.fab-main:active{
    background:linear-gradient(135deg,#1d4ed8,#6d28d9);
    color:#fff;transform:scale(1.08) rotate(15deg);
}
.fab-main i{transition:transform .3s}
.fab-group.open .fab-main i{transform:rotate(180deg)}
.fab-sub{
    opacity:0;transform:translateY(10px) scale(.8);
    pointer-events:none !important;
    transition:opacity .2s, transform .25s;
}
.fab-group.open .fab-sub{
    opacity:1;transform:translateY(0) scale(1);
    pointer-events:auto !important;
}
.fab-group.open .fab-sub:nth-child(1){transition-delay:.05s}
.fab-group.open .fab-sub:nth-child(2){transition-delay:.1s}
.fab-group.open .fab-sub:nth-child(3){transition-delay:.15s}
.fab-group.open .fab-sub:nth-child(4){transition-delay:.2s}

.fab-focus i { font-size: 1rem !important; }

/* ============ HIỂN THỊ THEO TRẠNG THÁI ============ */
body:not(.show-pinyin) .col-pinyin,
body:not(.show-pinyin) .card-pinyin{display:none!important}
body:not(.show-vi) .col-vi,
body:not(.show-vi) .card-vi{display:none!important}
body:not(.show-practice) .col-practice,
body:not(.show-practice) .card-practice{display:none!important}

body.show-practice .card-zh,
body.show-practice .card-pinyin{display:none!important}
body.show-practice .card-vi{
    display:block!important;font-size:1rem;font-weight:600;
    color:var(--text);margin-bottom:.55rem;line-height:1.4;
}
body.show-practice .card-body{
    background:linear-gradient(135deg, var(--surface-2), rgba(37,99,235,.06));
    padding:.75rem .85rem;border-radius:10px;border-left:3px solid var(--primary);
}

.ai-correct{color:var(--success);font-weight:700}
.ai-partial{color:var(--amber);font-weight:700}
.ai-wrong{color:var(--danger);font-weight:700}
.ai-reason{
    display:block;font-size:.68rem;color:var(--text-3);
    font-weight:400;margin-top:.2rem;font-style:italic;line-height:1.3;
}

.answer-inline-display{
    display:flex;align-items:center;justify-content:center;
    gap:.4rem;margin-top:.35rem;padding:.35rem .6rem;
    background:linear-gradient(135deg, rgba(37,99,235,.08), rgba(37,99,235,.04));
    border:1px dashed rgba(37,99,235,.3);
    border-radius:8px;flex-wrap:wrap;
}
[data-theme="dark"] .answer-inline-display{
    background:linear-gradient(135deg, rgba(59,130,246,.15), rgba(59,130,246,.08));
    border-color:rgba(59,130,246,.4);
}
.answer-inline-label{
    font-size:.7rem;font-weight:700;color:var(--primary-dark);
    text-transform:uppercase;letter-spacing:.3px;
    display:inline-flex;align-items:center;gap:.25rem;white-space:nowrap;
}
[data-theme="dark"] .answer-inline-label{color:#93c5fd;}
.answer-inline-label i{font-size:.75rem;}
.answer-inline-text{
    font-family:var(--font-zh);font-size:1.05rem;font-weight:600;
    color:var(--text);letter-spacing:.03em;word-break:break-all;
}

.main{padding:.5rem 0 3rem}

/* ============ DEMO BANNER ============ */
.demo-banner{
    background:linear-gradient(135deg, #fef3c7, #fde68a);
    border:1.5px solid #f59e0b;border-radius:var(--radius);
    padding:.9rem 1.1rem;margin-bottom:1rem;
    display:flex;align-items:center;gap:.75rem;flex-wrap:wrap;
}
[data-theme="dark"] .demo-banner{
    background:linear-gradient(135deg, rgba(245,158,11,.15), rgba(245,158,11,.25));
    border-color:#f59e0b;
}
.demo-banner-icon{
    width:36px;height:36px;border-radius:50%;
    background:var(--amber);color:#fff;
    display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;
}
.demo-banner-text{flex:1;min-width:200px}
.demo-banner-text .title{font-weight:700;font-size:.9rem;color:#92400e;margin-bottom:.15rem}
[data-theme="dark"] .demo-banner-text .title{color:#fcd34d}
.demo-banner-text .desc{font-size:.78rem;color:#78350f;line-height:1.5}
[data-theme="dark"] .demo-banner-text .desc{color:#fde68a}
.demo-banner-text .desc b{color:#dc2626}
[data-theme="dark"] .demo-banner-text .desc b{color:#fca5a5}
.demo-banner-btn{
    padding:.5rem .9rem;border-radius:50px;border:none;
    background:var(--amber);color:#fff;
    font-size:.8rem;font-weight:700;cursor:pointer;
    transition:.15s;font-family:inherit;
    display:flex;align-items:center;gap:.35rem;white-space:nowrap;
}
.demo-banner-btn:hover{background:#d97706;transform:translateY(-1px)}

/* ============ CARDS ============ */
.mobile-view{display:grid;grid-template-columns:1fr;gap:.8rem;max-width:100%}
@media(min-width:769px){.mobile-view{grid-template-columns:1fr 1fr;gap:1.2rem;}}
@media(min-width:1800px){.mobile-view{grid-template-columns:1fr 1fr 1fr;}}

.card-header{
    display:flex;align-items:center;gap:.4rem;
    margin-bottom:.6rem;padding-bottom:.6rem;
    border-bottom:1px dashed var(--border);
}
.card-stt{
    width:26px;height:26px;border-radius:50%;
    background:var(--surface-2);color:var(--text-3);
    display:flex;align-items:center;justify-content:center;
    font-size:.7rem;font-weight:700;flex-shrink:0;
}
.card-meta{display:flex;gap:.3rem;align-items:center;flex:1;min-width:0;flex-wrap:wrap}
.card-tag{
    display:inline-block;padding:.12rem .45rem;border-radius:var(--radius-full);
    background:var(--surface-2);color:var(--text-2);
    font-size:.65rem;font-weight:600;white-space:nowrap;
}
.card-tag.hsk{background:var(--primary-light);color:var(--primary-dark)}
.card-tag.topic{background:var(--amber-light);color:#92400e}
[data-theme="dark"] .card-tag.topic{color:#fde68a}
.card-body{margin-bottom:.6rem}
.card-vi{font-size:.85rem;color:var(--text-2);margin-bottom:.35rem;line-height:1.4}
.card-zh{
    font-size:1.2rem;font-weight:500;color:var(--text);
    margin-bottom:.4rem;line-height:1.5;
    font-family:var(--font-zh);letter-spacing:.02em;
}
.card-pinyin{
    font-size:.78rem;font-style:italic;color:var(--primary-dark);
    background:var(--surface-2);padding:.2rem .45rem;border-radius:6px;display:inline-block;
}
[data-theme="dark"] .card-pinyin{background:rgba(59,130,246,.18);color:#93c5fd;font-weight:500;font-style:italic}
.card-practice{
    display:flex;align-items:center;gap:.4rem;
    padding-top:.6rem;border-top:1px dashed var(--border);flex-wrap:wrap;
}
.card-practice .practice-input{flex:1;min-width:120px}
.card-check{
    font-size:.75rem;font-weight:700;
    min-width:55px;text-align:center;
    width:100%;
}

.audio-btn{
    width:32px;height:32px;border-radius:50%;border:none;
    background:var(--primary-light);color:var(--primary-dark);
    cursor:pointer;display:inline-flex;align-items:center;justify-content:center;
    font-size:.85rem;transition:.15s;position:relative;
}
.audio-btn:hover,.audio-btn:active{background:var(--primary);color:#fff;transform:scale(1.08)}
.audio-btn.speaking{background:var(--danger);color:#fff;animation:pulse 1s infinite}
@keyframes pulse{
    0%,100%{box-shadow:0 0 0 0 rgba(220,38,38,.6)}
    50%{box-shadow:0 0 0 10px rgba(220,38,38,0)}
}
.write-btn{
    width:32px;height:32px;border-radius:50%;border:none;
    background:var(--amber-light);color:#92400e;cursor:pointer;
    display:inline-flex;align-items:center;justify-content:center;
    font-size:.8rem;transition:.15s;
}
.write-btn:hover,.write-btn:active{background:var(--amber);color:#fff;transform:scale(1.08)}
[data-theme="dark"] .write-btn{background:rgba(245,158,11,.25);color:#fcd34d}
[data-theme="dark"] .write-btn:hover{background:var(--amber);color:#fff}

.practice-full-btn{
    width:32px;height:32px;border-radius:50%;border:none;
    background:var(--primary-light);color:var(--primary-dark);
    cursor:pointer;display:inline-flex;align-items:center;justify-content:center;
    font-size:.8rem;transition:.15s;
}
.practice-full-btn:hover,.practice-full-btn:active{background:var(--primary);color:#fff;transform:scale(1.08)}

.toggle-check-btn{
    width:32px;height:32px;border-radius:50%;border:none;
    background:var(--surface-2);color:var(--text-2);
    cursor:pointer;display:inline-flex;align-items:center;justify-content:center;
    font-size:.8rem;transition:.15s;flex-shrink:0;
    border:1px solid var(--border);
}
.toggle-check-btn:hover,.toggle-check-btn:active{
    background:var(--primary-light);color:var(--primary-dark);
    border-color:var(--primary);
}
.toggle-check-btn.active{
    background:var(--primary);color:#fff;border-color:var(--primary);
}
.toggle-check-btn.active:hover{
    background:var(--primary-dark);color:#fff;
}

.action-group{display:flex;gap:.3rem;justify-content:center;align-items:center;position:relative}
.practice-input{
    width:100%;min-width:120px;padding:.5rem .8rem;
    border-radius:var(--radius-full);border:1.5px solid var(--border);
    background:var(--surface);color:var(--text);font-size:.9rem;
    outline:none;transition:.15s;font-family:var(--font-zh);-webkit-appearance:none;
}
.practice-input:focus{border-color:var(--primary);box-shadow:0 0 0 3px rgba(37,99,235,.15)}

.card{
    background:var(--surface);border-radius:var(--radius);
    border:1px solid var(--border);padding:.9rem;
    box-shadow:var(--shadow-sm);
    transition:transform .25s, box-shadow .25s, border-color .25s;
    cursor:pointer;user-select:none;
}
.card.tapped{animation:tapPulse .6s}
@keyframes tapPulse{
    0%{box-shadow:0 0 0 0 rgba(37,99,235,.4)}
    70%{box-shadow:0 0 0 14px rgba(37,99,235,0)}
    100%{box-shadow:0 0 0 0 rgba(37,99,235,0)}
}
.card.focused{
    transform:scale(1.02);
    box-shadow:0 12px 32px rgba(37,99,235,.2);
    border-color:var(--primary);
    background:linear-gradient(135deg, var(--surface) 0%, rgba(37,99,235,.06) 100%);
}
[data-theme="dark"] .card.focused{
    background:linear-gradient(135deg, var(--surface) 0%, rgba(59,130,246,.15) 100%);
    box-shadow:0 12px 32px rgba(59,130,246,.3);
}
.card.focused .card-zh{font-size:2rem;font-weight:500;letter-spacing:.02em;line-height:1.5}
.practice-input, .audio-btn, .write-btn, .card-practice{cursor:auto}

.load-more{
    grid-column:1 / -1;display:block;width:100%;padding:.9rem;margin-top:.5rem;
    border-radius:var(--radius);border:1.5px dashed var(--border-strong);
    background:var(--surface);color:var(--primary);
    font-weight:700;font-size:.88rem;cursor:pointer;
    transition:.15s;font-family:inherit;
}
.load-more:hover,.load-more:active{background:var(--primary-light);border-color:var(--primary)}
.load-more.locked{border-color:var(--amber);color:#92400e;background:var(--amber-light)}
[data-theme="dark"] .load-more.locked{color:#fcd34d;background:rgba(245,158,11,.15)}
.end-note{
    grid-column:1 / -1;text-align:center;padding:1rem;
    color:var(--text-3);font-size:.82rem;
}
.end-note i{color:var(--success);margin-right:.35rem}
.no-data{
    grid-column:1 / -1;text-align:center;padding:3rem 1rem;color:var(--text-3);
    background:var(--surface);border-radius:var(--radius);border:1px solid var(--border);
}
.no-data i{font-size:2.5rem;margin-bottom:.75rem;color:var(--border-strong);display:block}

/* ============ PRACTICE FULL MODAL ============ */
.practice-full-modal{
    position:fixed;left:0;right:0;bottom:0;
    background:var(--bg);z-index:2500;
    display:none;flex-direction:column;animation:fadeIn .2s;
    top:0;overflow:hidden;
}
.practice-full-modal.show{display:flex}

body.practice-full-open .search-bar,
body.practice-full-open .filters,
body.practice-full-open .result-count { display: none !important; }
body.practice-full-open .demo-banner,
body.practice-full-open .expiry-banner { display: none !important; }

.practice-full-header{
    display:flex;align-items:center;gap:.75rem;
    padding:.85rem 1.25rem;background:var(--surface);
    border-bottom:1px solid var(--border);
    flex-shrink:0;box-shadow:0 2px 8px rgba(15,23,42,.04);
}
.practice-full-header .pf-counter{
    font-size:.85rem;font-weight:700;color:var(--text-2);
    background:var(--surface-2);padding:.35rem .75rem;border-radius:50px;
    white-space:nowrap;
}
.practice-full-header .pf-tags{
    display:flex;gap:.35rem;flex:1;min-width:0;flex-wrap:wrap;
}
.practice-full-header .pf-close{
    width:38px;height:38px;border-radius:50%;border:none;
    background:var(--surface-2);color:var(--text-2);cursor:pointer;
    font-size:1rem;display:flex;align-items:center;justify-content:center;
    transition:.15s;flex-shrink:0;
}
.practice-full-header .pf-close:hover{background:var(--danger-light);color:var(--danger)}

.pf-filters{
    padding:.6rem 1.25rem .5rem 1.25rem;
    background:var(--surface);
    border-bottom:1px solid var(--border);
    flex-shrink:0;
}
.pf-search-wrap{position:relative;margin-bottom:.5rem;}
.pf-search-wrap i.fa-search{
    position:absolute;left:14px;top:50%;transform:translateY(-50%);
    color:var(--text-3);font-size:.85rem;pointer-events:none;
}
.pf-search-wrap input{
    width:100%;padding:.6rem 2.4rem .6rem 2.4rem;
    border-radius:var(--radius-full);border:1.5px solid var(--border);
    background:var(--bg);color:var(--text);font-size:.88rem;
    outline:none;transition:.15s;font-family:inherit;
    -webkit-appearance:none;
}
.pf-search-wrap input:focus{border-color:var(--primary);box-shadow:0 0 0 3px rgba(37,99,235,.15)}
.pf-search-wrap input::placeholder{color:var(--text-3)}
.pf-search-clear{
    position:absolute;right:8px;top:50%;transform:translateY(-50%);
    width:28px;height:28px;border-radius:50%;border:none;
    background:var(--surface-2);color:var(--text-2);
    cursor:pointer;display:none;align-items:center;justify-content:center;font-size:.75rem;
}
.pf-search-clear.show{display:flex}

.pf-filter-row{display:grid;grid-template-columns:1fr 1fr;gap:.5rem;}
.pf-chip{
    display:flex;align-items:center;gap:.4rem;
    padding:.45rem .8rem;border-radius:var(--radius-full);
    border:1.5px solid var(--border);background:var(--bg);
    color:var(--text);font-size:.8rem;font-weight:500;
    cursor:pointer;transition:.15s;outline:none;font-family:inherit;
    min-width:0;position:relative;overflow:hidden;
}
.pf-chip:active{transform:scale(.98)}
.pf-chip.has-value{background:var(--primary);color:#fff;border-color:var(--primary)}
.pf-chip.has-value .pf-chip-label{color:#fff;opacity:.85}
.pf-chip-label{font-size:.65rem;color:var(--text-3);text-transform:uppercase;letter-spacing:.3px;font-weight:700;flex-shrink:0}
.pf-chip-value{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;min-width:0}
.pf-chip-arrow{color:inherit;opacity:.5;font-size:.65rem;flex-shrink:0}
.pf-chip select{
    position:absolute;inset:0;opacity:0;cursor:pointer;font-size:1rem;
    -webkit-appearance:none;appearance:none;width:100%;height:100%;
}
.pf-result-count{
    display:none;align-items:center;gap:.4rem;margin-top:.45rem;
    padding:.35rem .7rem;border-radius:var(--radius-full);
    background:var(--bg);border:1px solid var(--border);
    color:var(--text-2);font-size:.75rem;font-weight:600;
    width:fit-content;
}
.pf-result-count.show{display:inline-flex}
.pf-result-count i{color:var(--primary);font-size:.8rem}
.pf-result-count b{color:var(--primary);font-weight:800}
.pf-result-count.empty{background:var(--danger-light);color:var(--danger)}
.pf-result-count.empty i,.pf-result-count.empty b{color:var(--danger)}

.pf-quick-nav{margin-top:.5rem;display:flex;align-items:center;gap:.5rem;}
.pf-quick-nav-label{
    font-size:.7rem;font-weight:700;color:var(--text-3);
    text-transform:uppercase;letter-spacing:.3px;white-space:nowrap;
}
.pf-quick-nav-select{
    flex:1;min-width:0;padding:.5rem 2rem .5rem .8rem;
    border-radius:var(--radius-full);border:1.5px solid var(--border);
    background:var(--bg);color:var(--text);font-size:.82rem;
    font-family:inherit;outline:none;cursor:pointer;transition:.15s;
    -webkit-appearance:none;appearance:none;
    background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12'><path fill='%2394a3b8' d='M6 9L1 4h10z'/></svg>");
    background-repeat:no-repeat;background-position:right 12px center;background-size:10px;
}
.pf-quick-nav-select:focus{
    border-color:var(--primary);box-shadow:0 0 0 3px rgba(37,99,235,.15);
}

.practice-full-body{
    flex:1;overflow-y:auto;padding:2rem 1.25rem;
    display:flex;flex-direction:column;
    align-items:center;justify-content:center;min-height:0;
}
.practice-full-content{
    width:100%;max-width:700px;
    display:flex;flex-direction:column;gap:1.5rem;
}

.practice-full-vi{
    font-size:1.75rem;font-weight:600;color:var(--text);
    text-align:center;line-height:1.45;
    padding:1.25rem 1rem;
    background:linear-gradient(135deg, var(--surface-2), rgba(37,99,235,.06));
    border-radius:16px;border-left:4px solid var(--primary);
}
@media(min-width:769px){.practice-full-vi{font-size:2.25rem;}}

.practice-full-input-wrap{display:flex;flex-direction:column;gap:.75rem;}
.practice-full-input{
    width:100%;padding:1rem 1.25rem;
    font-size:1.5rem;font-family:var(--font-zh);
    border-radius:14px;border:2px solid var(--border);
    background:var(--surface);color:var(--text);
    outline:none;transition:.15s;
    text-align:center;letter-spacing:.05em;
    -webkit-appearance:none;
}
.practice-full-input:focus{
    border-color:var(--primary);box-shadow:0 0 0 4px rgba(37,99,235,.15);
}
@media(min-width:769px){.practice-full-input{font-size:1.85rem;padding:1.15rem 1.5rem;}}

.char-preview{
    display:flex;justify-content:center;flex-wrap:wrap;
    gap:.5rem;min-height:2.5rem;padding:.75rem 1rem;
    background:var(--surface-2);border-radius:12px;
    border:1px dashed var(--border);
    user-select:none;-webkit-user-select:none;
}
.char-preview:empty{display:none}
.char-slot{
    font-family:var(--font-zh);font-size:1.6rem;font-weight:500;
    display:inline-flex;align-items:center;justify-content:center;
    min-width:1.8rem;height:2.4rem;padding:0 .35rem;
    border-radius:8px;transition:.15s;line-height:1;
}
@media(min-width:769px){.char-slot{font-size:2rem;min-width:2.2rem;height:2.8rem;}}

.char-slot.correct{
    color:var(--text);font-weight:700;
    background:rgba(22,163,74,.12);
}
.char-slot.wrong{
    color:#fff;background:var(--danger);
    animation:shakeWrong .3s;
    box-shadow:0 2px 8px rgba(220,38,38,.35);
    cursor:pointer;position:relative;
}
.char-slot.wrong:hover{
    transform:scale(1.15);
    box-shadow:0 4px 12px rgba(220,38,38,.5);
    z-index:5;
}
.char-slot.wrong:active{transform:scale(.95);}
.char-slot.wrong.highlight{
    animation:blinkHighlight 0.6s ease-in-out 2;
    box-shadow:0 0 0 4px rgba(220,38,38,.4);
}
@keyframes blinkHighlight{
    0%,100%{transform:scale(1.15);background:var(--danger);}
    50%{transform:scale(1.25);background:#ef4444;box-shadow:0 0 0 8px rgba(220,38,38,.3);}
}
.char-slot.ghost{
    color:var(--text);opacity:.12;font-weight:400;
    background:transparent;user-select:none;
    pointer-events:none;filter:blur(0.3px);
}
[data-theme="dark"] .char-slot.ghost{color:var(--text);opacity:.15;}
.char-slot.extra{
    color:#fff;background:var(--amber);
    box-shadow:0 2px 8px rgba(245,158,11,.35);
    cursor:pointer;transition:.15s;
}
.char-slot.extra:hover{
    transform:scale(1.15);
    box-shadow:0 4px 12px rgba(245,158,11,.5);
    z-index:5;
}
.char-slot.ghost-missing{
    color:var(--text-3);opacity:.5;background:transparent;
    border:1px dashed var(--border);
    cursor:pointer;font-size:1.2rem;font-weight:400;
}
.char-slot.ghost-missing:hover{
    opacity:.9;border-color:var(--primary);
    color:var(--primary);transform:scale(1.1);
}
.char-slot.ghost-missing.highlight{
    animation:blinkHighlightMissing 0.6s ease-in-out 2;
}
@keyframes blinkHighlightMissing{
    0%,100%{transform:scale(1.1);border-color:var(--primary);color:var(--primary);}
    50%{transform:scale(1.25);border-color:var(--primary);color:var(--primary);box-shadow:0 0 0 6px rgba(37,99,235,.2);}
}
@keyframes shakeWrong{
    0%,100%{transform:translateX(0)}
    25%{transform:translateX(-3px)}
    75%{transform:translateX(3px)}
}

.inline-char-preview{
    display:flex;flex-wrap:wrap;gap:.25rem;
    margin-top:.4rem;width:100%;
}
.inline-char-preview .char-slot{
    font-size:.95rem;min-width:1.1rem;height:1.5rem;
    padding:0 .25rem;border-radius:5px;
}
.inline-char-preview .char-slot.ghost-missing{
    font-size:.9rem;min-width:1.1rem;height:1.5rem;
}

.practice-full-status{
    text-align:center;font-size:1rem;font-weight:700;min-height:1.5rem;
}
.practice-full-status.correct{color:var(--success);}
.practice-full-status.partial{color:var(--amber);}
.practice-full-status.wrong{color:var(--danger);}

.reveal-actions{
    display:grid;grid-template-columns:1fr 1fr;gap:.75rem;
}
.reveal-actions button{
    width:100%;padding:.85rem;
    border-radius:14px;border:2px dashed var(--border-strong);
    background:var(--surface);color:var(--text-2);
    font-size:.9rem;font-weight:600;cursor:pointer;
    transition:all .2s ease;font-family:inherit;
    display:flex;align-items:center;justify-content:center;gap:.5rem;
}
.reveal-actions button:hover{
    border-color:var(--primary);color:var(--primary);background:var(--primary-light);
}
.reveal-actions button.hidden{display:none}

#pfHintBtn.active{
    background:var(--amber);color:#fff;border-color:var(--amber);border-style:solid;
    box-shadow:0 4px 12px rgba(245,158,11,.3);
}
#pfHintBtn.active:hover{background:#d97706}

#pfRevealBtn.revealed{
    background:var(--success);color:#fff;border-color:var(--success);border-style:solid;
    box-shadow:0 4px 12px rgba(22,163,74,.3);
}
#pfRevealBtn.revealed:hover{background:#15803d}

.answer-reveal{
    display:none;flex-direction:column;gap:.75rem;
    padding:1.25rem;background:var(--surface-2);
    border-radius:14px;border:1px solid var(--border);
}
.answer-reveal.show{display:flex}
.answer-reveal .ar-label{
    font-size:.75rem;text-transform:uppercase;letter-spacing:.5px;
    color:var(--text-3);font-weight:700;text-align:center;
}
.answer-chars{
    display:flex;justify-content:center;flex-wrap:wrap;gap:.5rem;
}

.answer-phrase-btn{
    font-family:var(--font-zh);font-size:1.5rem;font-weight:500;
    padding:.5rem .9rem;
    border-radius:12px;border:2px solid var(--border);
    background:var(--surface);color:var(--text);
    cursor:pointer;
    transition:transform .25s cubic-bezier(.34,1.56,.64,1),
               background .2s,color .2s,border-color .2s,box-shadow .2s;
    display:inline-flex;align-items:center;justify-content:center;
    -webkit-appearance:none;transform-origin:center center;
}
@media(hover:hover) and (pointer:fine){
    .answer-phrase-btn:hover{
        transform:scale(1.35);
        background:var(--primary);color:#fff;
        border-color:var(--primary);
        box-shadow:0 8px 24px rgba(37,99,235,.4);
        z-index:10;
    }
}
.answer-phrase-btn.zoom-in{
    transform:scale(1.35);
    background:var(--primary);color:#fff;
    border-color:var(--primary);
    box-shadow:0 8px 24px rgba(37,99,235,.4);
    z-index:10;
}
.answer-phrase-btn.speaking{
    background:var(--primary);color:#fff;border-color:var(--primary);
    animation:pulse 1s infinite;
}
@media(min-width:769px){
    .answer-phrase-btn{font-size:1.8rem;padding:.6rem 1.1rem;}
}

.answer-pinyin{
    text-align:center;font-size:.95rem;font-style:italic;
    color:var(--primary-dark);font-weight:500;
}
.answer-actions{
    display:flex;justify-content:center;gap:.5rem;flex-wrap:wrap;
}
.answer-actions button{
    padding:.6rem 1.1rem;border-radius:50px;border:1.5px solid var(--border);
    background:var(--surface);color:var(--text);
    font-size:.85rem;font-weight:600;cursor:pointer;
    transition:.15s;font-family:inherit;
    display:inline-flex;align-items:center;gap:.4rem;
}
.answer-actions button:hover{background:var(--surface-2);border-color:var(--primary);color:var(--primary)}
.answer-actions button.primary{background:var(--primary);color:#fff;border-color:var(--primary)}
.answer-actions button.primary:hover{background:var(--primary-dark)}

.practice-full-nav{
    display:flex;gap:.75rem;padding:1rem 1.25rem;
    background:var(--surface);border-top:1px solid var(--border);
    flex-shrink:0;justify-content:center;
}
.pf-nav-btn{
    flex:1;max-width:220px;padding:.85rem 1rem;
    border-radius:14px;border:1.5px solid var(--border);
    background:var(--surface);color:var(--text);
    font-size:.9rem;font-weight:700;cursor:pointer;
    transition:.15s;font-family:inherit;
    display:inline-flex;align-items:center;justify-content:center;gap:.5rem;
}
.pf-nav-btn:hover:not(:disabled){
    background:var(--primary-light);border-color:var(--primary);color:var(--primary-dark);
    transform:translateY(-1px);
}
.pf-nav-btn:disabled{opacity:.35;cursor:not-allowed}
.pf-nav-btn.primary{
    background:var(--primary);color:#fff;border-color:var(--primary);
    box-shadow:0 4px 12px rgba(37,99,235,.3);
}
.pf-nav-btn.primary:hover:not(:disabled){background:var(--primary-dark)}

@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes slideUp{
    from{transform:translateY(30px) scale(.95);opacity:0}
    to{transform:translateY(0) scale(1);opacity:1}
}

/* ============ WRITER MODAL ============ */
.writer-modal{
    position:fixed;inset:0;background:rgba(15,23,42,.7);
    backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);
    z-index:2000;display:none;align-items:center;justify-content:center;
    padding:1rem;animation:fadeIn .2s;
}
.writer-modal.show{display:flex}
.writer-box{
    background:var(--surface);border-radius:20px;padding:1.5rem 1.25rem;
    max-width:420px;width:100%;max-height:calc(100vh - 2rem);overflow-y:auto;
    box-shadow:0 20px 60px rgba(0,0,0,.3);position:relative;
}
.writer-close{
    position:absolute;top:10px;right:10px;
    width:34px;height:34px;border-radius:50%;border:none;
    background:var(--surface-2);color:var(--text-2);cursor:pointer;
    font-size:1rem;display:flex;align-items:center;justify-content:center;
    transition:.15s;z-index:5;
}
.writer-close:hover{background:var(--danger-light);color:var(--danger)}
.writer-char-info{text-align:center;margin-bottom:.75rem}
.writer-char-info .vi-small{font-size:.85rem;color:var(--text-2);margin-bottom:.3rem;line-height:1.4}
.writer-char-info .pinyin-small{
    font-size:.8rem;font-style:italic;color:var(--primary-dark);
    background:var(--surface-2);padding:.2rem .6rem;border-radius:6px;display:inline-block;
}
[data-theme="dark"] .writer-char-info .pinyin-small{background:rgba(59,130,246,.18);color:#93c5fd}
.writer-chars{display:flex;gap:.4rem;justify-content:center;flex-wrap:wrap;margin-bottom:.75rem}
.writer-char-btn{
    width:42px;height:42px;border-radius:10px;border:1.5px solid var(--border);
    background:var(--surface-2);color:var(--text);
    font-family:var(--font-zh);font-size:1.3rem;font-weight:500;
    cursor:pointer;transition:.15s;display:flex;align-items:center;justify-content:center;padding:0;
}
.writer-char-btn:hover{border-color:var(--primary)}
.writer-char-btn.active{background:var(--primary);color:#fff;border-color:var(--primary);box-shadow:0 4px 10px rgba(37,99,235,.3)}
.writer-target{
    width:280px;height:280px;margin:0 auto;background:#fff;
    border-radius:14px;position:relative;
    box-shadow:inset 0 0 0 2px var(--border);overflow:hidden;
    background-image:
        linear-gradient(to right, transparent calc(50% - 0.5px), #e2e8f0 calc(50% - 0.5px), #e2e8f0 calc(50% + 0.5px), transparent calc(50% + 0.5px)),
        linear-gradient(to bottom, transparent calc(50% - 0.5px), #e2e8f0 calc(50% - 0.5px), #e2e8f0 calc(50% + 0.5px), transparent calc(50% + 0.5px)),
        linear-gradient(45deg, transparent calc(50% - 0.5px), #e2e8f0 calc(50% - 0.5px), #e2e8f0 calc(50% + 0.5px), transparent calc(50% + 0.5px)),
        linear-gradient(-45deg, transparent calc(50% - 0.5px), #e2e8f0 calc(50% - 0.5px), #e2e8f0 calc(50% + 0.5px), transparent calc(50% + 0.5px));
}
.writer-target svg{display:block;width:100%;height:100%;position:relative;z-index:1}
.writer-controls{display:flex;gap:.4rem;justify-content:center;margin-top:1rem;flex-wrap:wrap}
.writer-btn{
    padding:.6rem .95rem;border-radius:10px;border:1.5px solid var(--border);
    background:var(--surface);color:var(--text);font-size:.82rem;font-weight:600;
    cursor:pointer;transition:.15s;display:flex;align-items:center;gap:.35rem;
    font-family:inherit;
}
.writer-btn:hover{background:var(--primary-light);border-color:var(--primary);color:var(--primary-dark)}
.writer-btn.primary{background:var(--primary);color:#fff;border-color:var(--primary)}
.writer-btn.primary:hover{background:var(--primary-dark);color:#fff}
.writer-loading{
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    height:100%;color:var(--text-3);font-size:.85rem;gap:.5rem;padding:1rem;text-align:center;
}
.writer-loading i{font-size:1.8rem;color:var(--primary)}
.writer-score{text-align:center;margin-top:.6rem;font-size:.82rem;color:var(--text-2);min-height:1.2em}
.writer-score.success{color:var(--success);font-weight:600}
.writer-score.error{color:var(--danger);font-weight:600}

/* ============ DARK MODE OVERRIDES ============ */
[data-theme="dark"] .hsk-badge{
    background:rgba(59,130,246,.25);color:#93c5fd;font-weight:800;
    border:1px solid rgba(59,130,246,.4);
}
[data-theme="dark"] .card-tag.hsk{
    background:rgba(59,130,246,.25);color:#93c5fd;font-weight:700;
    border:1px solid rgba(59,130,246,.4);
}
[data-theme="dark"] .audio-btn{
    background:rgba(59,130,246,.22);color:#93c5fd;
    border:1px solid rgba(59,130,246,.35);
}
[data-theme="dark"] .audio-btn:hover,
[data-theme="dark"] .audio-btn:active{background:#3b82f6;color:#fff;border-color:#3b82f6;}

/* ============ RESPONSIVE ============ */
@media(max-width:768px){
    .container{padding:0 .7rem}
    .header-inner{gap:.5rem;margin-bottom:.4rem}
    .logo-icon{width:52px;height:52px;font-size:1.5rem;border-radius:13px}
    .logo-text .title{font-size:1.5rem}
    .logo-text .subtitle{font-size:.82rem;padding-left:.8rem}
    .icon-btn{width:34px;height:34px;font-size:.8rem}
    .main{padding:.15rem 0 2rem}
    .search-bar input{padding:.65rem 2.5rem .65rem 2.4rem;font-size:.88rem}
    .filters{max-width:100%}
    .chip{padding:.5rem .75rem;font-size:.8rem}
    .chip-label{font-size:.65rem}
    .result-count{font-size:.75rem;padding:.4rem .7rem;margin-top:.45rem}
    .fab-group{right:16px;bottom:calc(16px + env(safe-area-inset-bottom));gap:.45rem}
    .fab-main{width:52px;height:52px;font-size:1.2rem}
    .fab-btn{width:48px;height:48px;font-size:1.05rem}
    .card.focused .card-zh{font-size:2.2rem}
    .writer-box{padding:1.2rem 1rem;max-width:340px}
    .writer-target{width:240px;height:240px}
    .writer-char-btn{width:38px;height:38px;font-size:1.15rem}
    .writer-btn{padding:.55rem .8rem;font-size:.78rem}
    .btn-login-header{padding:.45rem .7rem;font-size:.75rem}
    .btn-login-header span{display:none}

    .practice-full-header{padding:.65rem .85rem;gap:.5rem}
    .practice-full-header .pf-counter{font-size:.75rem;padding:.3rem .6rem}
    .pf-filters{padding:.5rem .85rem .4rem .85rem}
    .pf-search-wrap input{padding:.55rem 2.2rem .55rem 2.2rem;font-size:.85rem}
    .pf-search-wrap i.fa-search{left:12px;font-size:.8rem}
    .pf-search-clear{width:26px;height:26px;font-size:.7rem}
    .pf-chip{padding:.4rem .7rem;font-size:.75rem}
    .pf-chip-label{font-size:.6rem}
    .pf-result-count{font-size:.7rem;padding:.3rem .6rem}
    .pf-quick-nav-select{font-size:.78rem;padding:.45rem 1.8rem .45rem .7rem}
    .pf-quick-nav-label{font-size:.65rem}
    .practice-full-body{padding:1.25rem .85rem}
    .practice-full-content{gap:1.1rem}
    .practice-full-vi{font-size:1.35rem;padding:1rem .75rem}
    .practice-full-input{font-size:1.35rem;padding:.85rem 1rem}
    .char-slot{font-size:1.4rem;min-width:1.6rem;height:2.1rem}
    .answer-phrase-btn{font-size:1.3rem;padding:.45rem .75rem;}
    .pf-nav-btn{padding:.75rem .75rem;font-size:.82rem}
    .practice-full-nav{padding:.75rem .85rem;gap:.5rem}
    .reveal-actions button{padding:.7rem;font-size:.82rem;}
}
@media(max-width:400px){
    .logo-icon{width:46px;height:46px;font-size:1.35rem;border-radius:12px}
    .logo-text .title{font-size:1.35rem}
    .logo-text .subtitle{display:none}
    .icon-btn{width:32px;height:32px;font-size:.75rem}
}
"""


# ═══════════════════════════════════════════════════════════════════
#  HTML
# ═══════════════════════════════════════════════════════════════════
def build_ui_html():
    return r"""
<div class="loading-screen" id="loadingScreen">
    <i class="fas fa-spinner"></i>
    <div>Đang tải...</div>
</div>

<div class="sticky-top" id="stickyTop" style="display:none">
    <div class="container">
        <header class="header">
            <div class="header-inner">
                <div class="logo">
                    <div class="logo-icon"><i class="fas fa-language"></i></div>
                    <div class="logo-text">
                        <div class="title">Học tiếng Trung</div>
                        <div class="subtitle">Văn phòng &amp; Công xưởng</div>
                    </div>
                </div>
                <div class="header-actions">
                    <div class="demo-badge" id="demoBadge" style="display:none">
                        <i class="fas fa-eye"></i> Demo
                    </div>
                    <button class="btn-login-header" id="headerLoginBtn" style="display:none">
                        <i class="fas fa-sign-in-alt"></i> <span>Đăng nhập</span>
                    </button>
                    <button class="icon-btn reset-btn hidden" id="resetBtn" title="Đặt lại bộ lọc">
                        <i class="fas fa-undo-alt"></i>
                        <span class="badge" id="resetBadge">0</span>
                    </button>
                    <button class="icon-btn" id="themeToggle" title="Đổi giao diện">
                        <i class="fas fa-moon"></i>
                    </button>
                    <div class="user-menu" id="userMenu" style="display:none">
                        <img class="user-avatar" id="userAvatar" src="" alt="Avatar">
                        <div class="user-dropdown" id="userDropdown">
                            <div class="user-info">
                                <div class="name" id="userName">-</div>
                                <div class="email" id="userEmail">-</div>
                                <span class="role" id="userRole">user</span>
                            </div>
                            <div class="user-details" id="userDetails" style="display:none">
                                <div class="detail-row" id="expiryRow">
                                    <div class="detail-icon" id="expiryIconWrap">
                                        <i class="fas fa-calendar-check" id="expiryIcon"></i>
                                    </div>
                                    <div class="detail-content">
                                        <div class="detail-label">Hạn sử dụng</div>
                                        <div class="detail-value" id="expiryValue">-</div>
                                        <div class="detail-sub" id="expirySub"></div>
                                    </div>
                                </div>
                                <div class="detail-progress" id="expiryProgressWrap" style="display:none">
                                    <div class="progress-track">
                                        <div class="progress-bar" id="expiryProgressBar"></div>
                                    </div>
                                </div>
                            </div>
                            <button class="dropdown-item" id="changeNameBtn">
                                <i class="fas fa-user-edit"></i> Đổi tên hiển thị
                            </button>
                            <button class="dropdown-item" id="openAdminBtn" style="display:none">
                                <i class="fas fa-shield-alt"></i> Quản lý tài khoản
                            </button>
                            <button class="dropdown-renew" id="dropdownRenewBtn" style="display:none">
                                <i class="fas fa-crown"></i> Gia hạn tài khoản
                            </button>
                            <a class="dropdown-zalo" id="dropdownZaloBtn" href="#" target="_blank" rel="noopener noreferrer">
                                <i class="fas fa-comment-dots"></i> Liên hệ Zalo hỗ trợ
                            </a>
                            <a class="dropdown-tiktok" id="dropdownTiktokBtn" href="#" target="_blank" rel="noopener noreferrer">
                                <i class="fab fa-tiktok"></i> Theo dõi TikTok
                            </a>
                            <button class="dropdown-item danger" id="logoutBtn">
                                <i class="fas fa-sign-out-alt"></i> Đăng xuất
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </header>

        <!-- __TIKTOK_BAR__ -->

        <div class="search-bar">
            <i class="fas fa-search"></i>
            <input type="text" id="searchInput" placeholder="Tìm kiếm..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
            <button class="search-clear" id="clearSearchBtn" aria-label="Xóa">
                <i class="fas fa-times"></i>
            </button>
        </div>

        <div class="filters">
            <div class="chip" id="hskChip">
                <span class="chip-label">HSK</span>
                <span class="chip-value" id="hskValue">Tất cả</span>
                <i class="fas fa-chevron-down chip-arrow"></i>
                <select id="hskFilter">
                    <option value="">Tất cả</option>
                    <option value="HSK1">HSK1</option>
                    <option value="HSK2">HSK2</option>
                    <option value="HSK3">HSK3</option>
                    <option value="HSK4">HSK4</option>
                    <option value="HSK5">HSK5</option>
                    <option value="HSK6">HSK6</option>
                </select>
            </div>
            <div class="chip" id="subjectChip">
                <span class="chip-label">Chủ đề</span>
                <span class="chip-value" id="subjectValue">Tất cả</span>
                <i class="fas fa-chevron-down chip-arrow"></i>
                <select id="subjectFilter"><option value="">Tất cả chủ đề</option></select>
            </div>
        </div>

        <div class="result-count" id="resultCount">
            <i class="fas fa-list-ul"></i>
            <span>Tìm thấy <b id="resultCountNum">0</b> kết quả</span>
        </div>
    </div>
</div>

<div class="fab-group" id="fabGroup" style="display:none">
    <button class="fab-btn fab-sub" id="toggleViBtn" title="Ẩn/hiện Tiếng Việt">
        <i class="fas fa-language"></i>
    </button>
    <button class="fab-btn fab-sub" id="togglePinyinBtn" title="Ẩn/hiện Pinyin">
        <i class="fas fa-spell-check"></i>
    </button>
    <button class="fab-btn fab-sub" id="togglePracticeBtn" title="Ẩn/hiện Ô luyện dịch">
        <i class="fas fa-keyboard"></i>
    </button>
    <button class="fab-btn fab-sub fab-focus" id="toggleFocusBtn" title="Click để tắt Zalo/TikTok (Silent mode)">
        <i class="fas fa-bell"></i>
    </button>
    <button class="fab-btn fab-main" id="fabMainBtn" title="Tùy chọn hiển thị">
        <i class="fas fa-sliders-h"></i>
    </button>
</div>

<main class="main" id="mainContent" style="display:none">
    <div class="container">
        <div class="demo-banner" id="demoBanner" style="display:none">
            <div class="demo-banner-icon"><i class="fas fa-gift"></i></div>
            <div class="demo-banner-text">
                <div class="title">Bạn đang dùng bản Demo</div>
                <div class="desc">
                    Xem <b id="demoLimitText">50</b> câu đầu (HSK1-<span id="demoHskMaxText">3</span>).
                    Bộ lọc HSK chỉ từ HSK1-<span id="demoHskMaxText2">3</span>, chủ đề giới hạn theo 50 câu đầu.
                    Nghe + Luyện viết giới hạn <b id="demoDailyText">100</b> lượt/ngày
                    (còn lại: <b id="demoRemainingText">100</b> lượt).
                    Đăng nhập để mở khóa toàn bộ!
                </div>
            </div>
            <button class="demo-banner-btn" onclick="showLoginModal()">
                <i class="fas fa-sign-in-alt"></i> Đăng nhập ngay
            </button>
        </div>

        <div class="expiry-banner" id="expiryBanner" style="display:none">
            <div class="expiry-banner-icon"><i class="fas fa-hourglass-half"></i></div>
            <div class="expiry-banner-text">
                <div class="title">Tài khoản sắp hết hạn</div>
                <div class="desc">
                    Còn <b id="expiryDaysText">7</b> ngày (đến <b id="expiryDateText">-</b>). Liên hệ Admin để gia hạn!
                </div>
            </div>
            <a class="expiry-banner-btn" id="expiryContactBtn" href="#" target="_blank" rel="noopener noreferrer">
                <i class="fas fa-comment-dots"></i> Liên hệ
            </a>
        </div>

        <div class="mobile-view" id="mobileWrapper">
            <div class="no-data"><i class="fas fa-spinner fa-pulse"></i>Đang tải...</div>
        </div>
    </div>
</main>

<div class="writer-modal" id="writerModal">
    <div class="writer-box">
        <button class="writer-close" id="writerClose" aria-label="Đóng"><i class="fas fa-times"></i></button>
        <div class="writer-char-info">
            <div class="vi-small" id="writerViSmall"></div>
            <div class="pinyin-small" id="writerPinyinSmall"></div>
        </div>
        <div class="writer-chars" id="writerChars"></div>
        <div class="writer-target" id="writerTarget"></div>
        <div class="writer-score" id="writerScore"></div>
        <div class="writer-controls">
            <button class="writer-btn primary" id="writerAnimate"><i class="fas fa-play"></i> Viết</button>
            <button class="writer-btn" id="writerQuiz"><i class="fas fa-pen"></i> Tự viết</button>
            <button class="writer-btn" id="writerReset"><i class="fas fa-undo-alt"></i> Xóa</button>
        </div>
    </div>
</div>

<div class="practice-full-modal" id="practiceFullModal">
    <div class="practice-full-header">
        <div class="pf-counter" id="pfCounter">Câu 1 / 1</div>
        <div class="pf-tags" id="pfTags"></div>
        <button class="pf-close" id="pfClose" aria-label="Đóng">
            <i class="fas fa-times"></i>
        </button>
    </div>

    <div class="pf-filters">
        <div class="pf-search-wrap">
            <i class="fas fa-search"></i>
            <input type="text" id="pfSearchInput" placeholder="Tìm kiếm..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
            <button class="pf-search-clear" id="pfClearSearchBtn" aria-label="Xóa">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="pf-filter-row">
            <div class="pf-chip" id="pfHskChip">
                <span class="pf-chip-label">HSK</span>
                <span class="pf-chip-value" id="pfHskValue">Tất cả</span>
                <i class="fas fa-chevron-down pf-chip-arrow"></i>
                <select id="pfHskFilter">
                    <option value="">Tất cả</option>
                    <option value="HSK1">HSK1</option>
                    <option value="HSK2">HSK2</option>
                    <option value="HSK3">HSK3</option>
                    <option value="HSK4">HSK4</option>
                    <option value="HSK5">HSK5</option>
                    <option value="HSK6">HSK6</option>
                </select>
            </div>
            <div class="pf-chip" id="pfSubjectChip">
                <span class="pf-chip-label">Chủ đề</span>
                <span class="pf-chip-value" id="pfSubjectValue">Tất cả</span>
                <i class="fas fa-chevron-down pf-chip-arrow"></i>
                <select id="pfSubjectFilter"><option value="">Tất cả chủ đề</option></select>
            </div>
        </div>
        <div class="pf-result-count" id="pfResultCount">
            <i class="fas fa-list-ul"></i>
            <span>Tìm thấy <b id="pfResultCountNum">0</b> kết quả</span>
        </div>
        <div class="pf-quick-nav">
            <span class="pf-quick-nav-label">Câu:</span>
            <select class="pf-quick-nav-select" id="pfQuickNav">
                <option value="">-- Chọn câu --</option>
            </select>
        </div>
    </div>

    <div class="practice-full-body">
        <div class="practice-full-content">
            <div class="practice-full-vi" id="pfVi">-</div>

            <div class="practice-full-input-wrap">
                <input type="text" class="practice-full-input" id="pfInput"
                    placeholder="Gõ tiếng Trung..." autocomplete="off"
                    autocorrect="off" autocapitalize="off" spellcheck="false">
                <div class="char-preview" id="pfPreview"></div>
                <div class="practice-full-status" id="pfStatus"></div>
            </div>

            <div class="reveal-actions">
                <button id="pfHintBtn">
                    <i class="fas fa-lightbulb"></i> Gợi ý
                </button>
                <button id="pfRevealBtn">
                    <i class="fas fa-eye"></i> Xem đáp án
                </button>
            </div>

            <div class="answer-reveal" id="pfAnswer">
                <div class="ar-label">Đáp án</div>
                <div class="answer-chars" id="pfAnswerChars"></div>
                <div class="answer-pinyin" id="pfAnswerPinyin"></div>
                <div class="answer-actions">
                    <button class="primary" onclick="speakFullSentence()">
                        <i class="fas fa-volume-up"></i> Đọc cả câu
                    </button>
                </div>
            </div>
        </div>
    </div>

    <div class="practice-full-nav">
        <button class="pf-nav-btn" id="pfPrevBtn">
            <i class="fas fa-chevron-left"></i> Câu trước
        </button>
        <button class="pf-nav-btn primary" id="pfNextBtn">
            Câu sau <i class="fas fa-chevron-right"></i>
        </button>
    </div>
</div>
"""


# ═══════════════════════════════════════════════════════════════════
#  JS
# ═══════════════════════════════════════════════════════════════════
def build_ui_js():
    return r"""
/* ============ BIẾN TOÀN CỤC (chỉ phần học) ============ */
var filtered = [];
var state = { search:'', hsk:'', subject:'' };
var PAGE_SIZE = 300;
var renderedCount = 0;
var focusedStt = null;
var mobileWrapper;
var currentBtn = null;

var displayState = { vi: true, pinyin: false, practice: false };

/* ============ HELPERS ============ */
function getDemoData() { return RAW_DATA.slice(0, DEMO_LIMIT); }
function getDemoHskList() {
    var list = [];
    for (var i = 1; i <= DEMO_HSK_MAX; i++) list.push('HSK' + i);
    return list;
}
function getDemoSubjectList() {
    var set = {};
    getDemoData().forEach(function(r) { if (r.subject) set[r.subject] = 1; });
    return Object.keys(set).sort();
}

function getDemoUsage() {
    try {
        var today = new Date().toDateString();
        var data = JSON.parse(localStorage.getItem('demo_usage') || '{}');
        if (data.date !== today) {
            data = { date: today, count: 0 };
            localStorage.setItem('demo_usage', JSON.stringify(data));
        }
        return data.count;
    } catch(e) { return 0; }
}
function incDemoUsage() {
    try {
        var today = new Date().toDateString();
        var data = JSON.parse(localStorage.getItem('demo_usage') || '{}');
        if (data.date !== today) data = { date: today, count: 0 };
        data.count++;
        localStorage.setItem('demo_usage', JSON.stringify(data));
    } catch(e) {}
}
function getDemoRemaining() { return Math.max(0, DEMO_DAILY_LIMIT - getDemoUsage()); }

/* ✅ FIX: Chặn tính năng khi hết hạn */
function canUseFeature() {
    // Demo mode → giới hạn theo ngày
    if (isDemo) return getDemoUsage() < DEMO_DAILY_LIMIT;

    // User đã login → kiểm tra hạn
    if (currentUser && currentUser.role !== 'admin') {
        var daysLeft = getDaysRemaining(currentUser);
        if (daysLeft !== null && daysLeft <= 0) {
            return false;   // Đã hết hạn → chặn
        }
    }

    return true;
}

function updateDemoRemaining() {
    var el = $('demoRemainingText');
    if (!el) return;
    var remaining = getDemoRemaining();
    el.textContent = remaining;
    if (remaining < 20) el.style.color = '#dc2626';
    else if (remaining < 50) el.style.color = '#f59e0b';
    else el.style.color = '#16a34a';
}

/* ✅ FIX: showLimitMessage phân biệt demo vs hết hạn */
function showLimitMessage() {
    // Case 1: User đã login nhưng hết hạn
    if (!isDemo && currentUser && currentUser.role !== 'admin') {
        var daysLeft = getDaysRemaining(currentUser);
        if (daysLeft !== null && daysLeft <= 0) {
            if (confirm('🔒 Tài khoản của bạn đã HẾT HẠN.\n\n' +
                        'Vui lòng gia hạn để tiếp tục sử dụng tính năng này.\n\n' +
                        'Nhấn OK để mở trang gia hạn.')) {
                if (typeof openRenewalModal === 'function') openRenewalModal();
            }
            return;
        }
    }

    // Case 2: Demo hết lượt
    if (confirm('🔒 Bạn đã dùng hết ' + DEMO_DAILY_LIMIT +
                ' lượt miễn phí hôm nay.\n\n' +
                '(Bao gồm cả NGHE và LUYỆN VIẾT)\n\n' +
                'Đăng nhập Google để dùng KHÔNG GIỚI HẠN!')) {
        showLoginModal();
    }
}

function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}
function escapeJs(str) {
    if (str === null || str === undefined) return '';
    return String(str)
        .replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '\\"')
        .replace(/\n/g, '\\n').replace(/\r/g, '');
}
function formatTimeDiff(ms) {
    var s = Math.floor(ms / 1000);
    if (s < 60) return 'Vừa xong';
    var m = Math.floor(s / 60);
    if (m < 60) return m + ' phút trước';
    var h = Math.floor(m / 60);
    if (h < 24) return h + ' giờ trước';
    var d = Math.floor(h / 24);
    if (d < 30) return d + ' ngày trước';
    var mo = Math.floor(d / 30);
    return mo + ' tháng trước';
}

/* ============ INIT APP ============ */
function initApp() {
    mobileWrapper = $('mobileWrapper');

    $('loadingScreen').classList.add('hidden');
    $('stickyTop').style.display = 'block';
    $('fabGroup').style.display = 'flex';
    $('mainContent').style.display = 'block';

    if (typeof initSocial === 'function') initSocial();
    if (typeof updateFloatingLeftVisibility === 'function') updateFloatingLeftVisibility();
    if (typeof initAuthUI === 'function') initAuthUI();
    initScrollDetection();
    initFabGroup();
    initTheme();
    initDisplayState();
    initSpeech();
    initWriter();
    initPracticeFull();

    $('searchInput').addEventListener('input', applyFilter);
    $('resetBtn').addEventListener('click', function() {
        $('searchInput').value = '';
        $('hskFilter').value = '';
        $('subjectFilter').value = '';
        applyFilter();
    });
    $('clearSearchBtn').addEventListener('click', function() {
        $('searchInput').value = '';
        $('searchInput').focus();
        applyFilter();
    });

    $('hskFilter').addEventListener('change', function() {
        if (isDemo) {
            var val = this.value;
            var allowed = getDemoHskList();
            if (val && allowed.indexOf(val) === -1) {
                alert('🔒 Bản Demo chỉ cho phép lọc HSK1-' + DEMO_HSK_MAX + '.\n\nĐăng nhập Google để mở khóa tất cả HSK!');
                this.value = '';
                applyFilter();
                return;
            }
        }
        applyFilter();
    });
    $('subjectFilter').addEventListener('change', function() {
        if (isDemo) {
            var val = this.value;
            var allowed = getDemoSubjectList();
            if (val && allowed.indexOf(val) === -1) {
                alert('🔒 Chủ đề này chưa có trong ' + DEMO_LIMIT + ' câu Demo.\n\nĐăng nhập Google để mở khóa tất cả chủ đề!');
                this.value = '';
                applyFilter();
                return;
            }
        }
        applyFilter();
    });

    try { buildFilters(); applyFilter(); }
    catch(e) { console.error('Init error:', e); }
}

function refreshApp() {
    buildFilters();
    applyFilter();
    applyDisplayState();
    updateToggleButtons();
    updateResultCount();
}

/* ============ SCROLL DETECT ============ */
function initScrollDetection() {
    var sticky = $('stickyTop');
    if (!sticky) return;
    var ticking = false;
    function update() {
        if (window.scrollY > 5) sticky.classList.add('scrolled');
        else sticky.classList.remove('scrolled');
        ticking = false;
    }
    window.addEventListener('scroll', function() {
        if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
}

/* ============ FAB GROUP ============ */
function initFabGroup() {
    var fabGroup = $('fabGroup');
    var fabMainBtn = $('fabMainBtn');
    var fabOpen = false;
    try { var savedFab = localStorage.getItem('fabOpen'); if (savedFab === 'true') fabOpen = true; } catch(e) {}
    if (fabOpen) fabGroup.classList.add('open');

    fabMainBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        fabOpen = !fabOpen;
        fabGroup.classList.toggle('open', fabOpen);
        try { localStorage.setItem('fabOpen', fabOpen ? 'true' : 'false'); } catch(e) {}
    });
    document.addEventListener('click', function(e) {
        if (!fabGroup.contains(e.target) && fabOpen && window.innerWidth > 768) {
            fabOpen = false;
            fabGroup.classList.remove('open');
        }
    });
}

/* ============ THEME ============ */
function initTheme() {
    try {
        var saved = localStorage.getItem('theme');
        if (saved) document.documentElement.setAttribute('data-theme', saved);
        else document.documentElement.setAttribute('data-theme', 'light');
    } catch(e) {}
    updateThemeIcon();
    $('themeToggle').addEventListener('click', function() {
        var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        var newTheme = isDark ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        try { localStorage.setItem('theme', newTheme); } catch(e) {}
        updateThemeIcon();
    });
}
function updateThemeIcon() {
    var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    var icon = $('themeToggle').querySelector('i');
    icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
}

/* ============ DISPLAY STATE ============ */
function initDisplayState() {
    try {
        var saved = localStorage.getItem('displayState');
        if (saved) {
            var parsed = JSON.parse(saved);
            displayState.vi = parsed.vi !== false;
            displayState.pinyin = !!parsed.pinyin;
            displayState.practice = !!parsed.practice;
        }
    } catch(e) {}

    var focusHidden = false;
    try { focusHidden = localStorage.getItem('focusHidden') === 'true'; } catch(e) {}
    if (focusHidden) document.body.classList.add('hide-floating');
    updateFocusBtnIcon();

    if (displayState.practice) {
        displayState.pinyin = false;
        displayState.vi = true;
    }
    applyDisplayState();
    updateToggleButtons();

    $('toggleViBtn').addEventListener('click', function(e) {
        e.stopPropagation();
        displayState.vi = !displayState.vi;
        applyDisplayState(); saveDisplayState(); updateToggleButtons();
    });
    $('togglePinyinBtn').addEventListener('click', function(e) {
        e.stopPropagation();
        displayState.pinyin = !displayState.pinyin;
        if (displayState.pinyin && displayState.practice) displayState.practice = false;
        applyDisplayState(); saveDisplayState(); updateToggleButtons();
    });
    $('togglePracticeBtn').addEventListener('click', function(e) {
        e.stopPropagation();
        displayState.practice = !displayState.practice;
        if (displayState.practice) {
            displayState.pinyin = false;
            displayState.vi = true;
        }
        applyDisplayState(); saveDisplayState(); updateToggleButtons();
    });

    var toggleFocusBtn = $('toggleFocusBtn');
    if (toggleFocusBtn) {
        toggleFocusBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            var isHidden = document.body.classList.toggle('hide-floating');
            try { localStorage.setItem('focusHidden', isHidden ? 'true' : 'false'); } catch(e) {}
            updateFocusBtnIcon();
        });
    }
}

function updateFocusBtnIcon() {
    var btn = $('toggleFocusBtn');
    if (!btn) return;
    var isHidden = document.body.classList.contains('hide-floating');
    var icon = btn.querySelector('i');
    if (isHidden) {
        icon.className = 'fas fa-bell-slash';
        btn.setAttribute('title', 'Đang tắt thông báo — Click để bật lại Zalo/TikTok');
        btn.classList.remove('active');
    } else {
        icon.className = 'fas fa-bell';
        btn.setAttribute('title', 'Click để tắt Zalo/TikTok (Silent mode)');
        btn.classList.add('active');
    }
}

function applyDisplayState() {
    document.body.classList.toggle('show-vi', displayState.vi);
    document.body.classList.toggle('show-pinyin', displayState.pinyin);
    document.body.classList.toggle('show-practice', displayState.practice);

    if (displayState.practice) {
        document.querySelectorAll('.card-check').forEach(function(c) { c.innerHTML = ''; });
        document.querySelectorAll('.practice-input').forEach(function(i) {
            i.value = '';
            var answer = i.dataset.answer || '';
            updateInlinePreview(i, answer);
        });
    }
}
function saveDisplayState() {
    try { localStorage.setItem('displayState', JSON.stringify(displayState)); } catch(e) {}
}
function updateToggleButtons() {
    $('toggleViBtn').classList.toggle('active', displayState.vi);
    $('togglePinyinBtn').classList.toggle('active', displayState.pinyin);
    $('togglePracticeBtn').classList.toggle('active', displayState.practice);
    updateFocusBtnIcon();
}

/* ============ FOCUS CARD ============ */
window.toggleFocus = function(stt, element) {
    if (focusedStt === stt) { clearFocus(); return; }
    clearFocus();
    focusedStt = stt;
    element.classList.add('focused', 'tapped');
    setTimeout(function() { if (element) element.classList.remove('tapped'); }, 600);
};
window.clearFocus = function() {
    document.querySelectorAll('.focused').forEach(function(el) {
        el.classList.remove('focused', 'tapped');
    });
    focusedStt = null;
};
document.addEventListener('click', function(e) {
    if (e.target.closest('.card')) return;
    if (e.target.closest('.practice-input') || e.target.closest('.audio-btn') ||
        e.target.closest('.write-btn') || e.target.closest('.chip') ||
        e.target.closest('.fab-group') || e.target.closest('.icon-btn') ||
        e.target.closest('.search-bar') || e.target.closest('.filters') ||
        e.target.closest('.writer-modal') || e.target.closest('.user-menu') ||
        e.target.closest('.login-modal') || e.target.closest('.admin-modal') ||
        e.target.closest('.practice-full-modal') || e.target.closest('.import-modal') ||
        e.target.closest('.edit-modal') || e.target.closest('.zalo-btn') ||
        e.target.closest('.tiktok-float-wrap') || e.target.closest('.tiktok-bar') ||
        e.target.closest('.renewal-modal') ||
        e.target.closest('.toggle-check-btn')) return;
    clearFocus();
}, true);

/* ============ SPEECH ============ */
function initSpeech() {
    if ('speechSynthesis' in window) {
        speechSynthesis.getVoices();
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = function(){ getChineseVoice(); };
        }
    }
}
function getChineseVoice() {
    if (!('speechSynthesis' in window)) return null;
    var voices = speechSynthesis.getVoices();
    if (!voices.length) return null;
    var priorities = [
        function(v){ return v.lang === 'zh-CN' && /Ting-?Ting/i.test(v.name); },
        function(v){ return v.lang === 'zh-CN' && /Siri/i.test(v.name); },
        function(v){ return v.lang === 'zh-CN' && v.localService; },
        function(v){ return v.lang === 'zh-CN'; },
        function(v){ return v.lang === 'zh-TW'; },
        function(v){ return v.lang && v.lang.indexOf('zh') === 0; }
    ];
    for (var i = 0; i < priorities.length; i++) {
        var found = voices.find(priorities[i]);
        if (found) return found;
    }
    return null;
}

window.speakText = function(text, btn, evt) {
    if (evt) evt.stopPropagation();
    if (isDemo && !canUseFeature()) { showLimitMessage(); return; }
    if (!isDemo && !canUseFeature()) { showLimitMessage(); return; }
    if (!('speechSynthesis' in window)) { alert('Trình duyệt không hỗ trợ phát âm.'); return; }
    if (isDemo) { incDemoUsage(); updateDemoRemaining(); }
    speechSynthesis.cancel();
    if (currentBtn) currentBtn.classList.remove('speaking');
    if (btn) { btn.classList.add('speaking'); currentBtn = btn; }
    var utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'zh-CN';
    utterance.rate = 0.85;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    var voice = getChineseVoice();
    if (voice) utterance.voice = voice;
    utterance.onend = utterance.onerror = function() {
        if (currentBtn) { currentBtn.classList.remove('speaking'); currentBtn = null; }
    };
    setTimeout(function(){ speechSynthesis.speak(utterance); }, 50);
};
document.addEventListener('visibilitychange', function() {
    if (document.hidden && 'speechSynthesis' in window) {
        speechSynthesis.cancel();
        if (currentBtn) { currentBtn.classList.remove('speaking'); currentBtn = null; }
    }
});

/* ============ BUILD FILTERS ============ */
function buildFilters() {
    var hskSelect = $('hskFilter');
    var subjectSelect = $('subjectFilter');

    var allSubjectSet = {};
    RAW_DATA.forEach(function(r) { if (r.subject) allSubjectSet[r.subject] = 1; });
    var allSubjects = Object.keys(allSubjectSet).sort();

    if (isDemo) {
        var demoHsk = getDemoHskList();
        var hskHtml = '<option value="">Tất cả (HSK1-' + DEMO_HSK_MAX + ')</option>';
        demoHsk.forEach(function(h) { hskHtml += '<option value="' + h + '">' + h + '</option>'; });
        var allHskList = ['HSK1','HSK2','HSK3','HSK4','HSK5','HSK6'];
        allHskList.forEach(function(h) {
            if (demoHsk.indexOf(h) === -1) hskHtml += '<option value="' + h + '" disabled>🔒 ' + h + ' (đăng nhập)</option>';
        });
        hskSelect.innerHTML = hskHtml;

        var demoSubjects = getDemoSubjectList();
        var demoSubjectMap = {};
        demoSubjects.forEach(function(s) { demoSubjectMap[s] = 1; });

        var unlockedSubjects = [];
        var lockedSubjects = [];
        allSubjects.forEach(function(s) {
            if (demoSubjectMap[s]) unlockedSubjects.push(s);
            else lockedSubjects.push(s);
        });

        var subjHtml = '<option value="">Tất cả chủ đề</option>';
        unlockedSubjects.forEach(function(s) {
            subjHtml += '<option value="' + escapeHtml(s) + '">' + escapeHtml(s) + '</option>';
        });
        lockedSubjects.forEach(function(s) {
            subjHtml += '<option value="' + escapeHtml(s) + '" disabled>🔒 ' + escapeHtml(s) + ' (đăng nhập)</option>';
        });
        subjectSelect.innerHTML = subjHtml;
    } else {
        hskSelect.innerHTML =
            '<option value="">Tất cả</option>' +
            '<option value="HSK1">HSK1</option>' +
            '<option value="HSK2">HSK2</option>' +
            '<option value="HSK3">HSK3</option>' +
            '<option value="HSK4">HSK4</option>' +
            '<option value="HSK5">HSK5</option>' +
            '<option value="HSK6">HSK6</option>';

        subjectSelect.innerHTML = '<option value="">Tất cả chủ đề</option>' +
            allSubjects.map(function(v){ return '<option value="'+escapeHtml(v)+'">'+escapeHtml(v)+'</option>'; }).join('');
    }
}

function updateFilterUI() {
    var hsk = $('hskFilter').value;
    var subject = $('subjectFilter').value;
    $('hskValue').textContent = hsk || 'Tất cả';
    $('subjectValue').textContent = subject || 'Tất cả';
    $('hskChip').classList.toggle('has-value', !!hsk);
    $('subjectChip').classList.toggle('has-value', !!subject);
    var count = 0;
    if (state.search) count++;
    if (hsk) count++;
    if (subject) count++;
    var resetBtn = $('resetBtn');
    var badge = $('resetBadge');
    if (count > 0) {
        resetBtn.classList.remove('hidden');
        resetBtn.classList.add('has-badge');
        badge.textContent = count;
    } else {
        resetBtn.classList.add('hidden');
    }
    updateResultCount();
}

function updateResultCount() {
    var el = $('resultCount');
    if (!el) return;
    var total = filtered ? filtered.length : 0;
    var hasFilter = !!(state.search || state.hsk || state.subject);
    if (!hasFilter) { el.classList.remove('show', 'empty'); return; }
    el.classList.add('show');
    el.classList.toggle('empty', total === 0);
    var spanEl = el.querySelector('span');
    if (spanEl) {
        if (total === 0) spanEl.innerHTML = 'Không tìm thấy kết quả nào';
        else spanEl.innerHTML = 'Tìm thấy <b>' + total + '</b> kết quả';
    }
}

/* ============ RENDER CARDS ============ */
function render(reset) {
    if (reset) { renderedCount = 0; focusedStt = null; }
    if (!filtered.length) {
        mobileWrapper.innerHTML = '<div class="no-data"><i class="fas fa-search"></i>Không tìm thấy câu nào</div>';
        return;
    }
    if (reset) mobileWrapper.innerHTML = '';
    var end = Math.min(renderedCount + PAGE_SIZE, filtered.length);
    var mobHtml = '';
    for (var i = renderedCount; i < end; i++) {
        var r = filtered[i];
        var zhJs = escapeJs(r.zh);
        var viJs = escapeJs(r.vi);
        var pinyinJs = escapeJs(r.pinyin);
        var zhHtml = escapeHtml(r.zh);
        var viHtml = escapeHtml(r.vi);
        var sttSafe = escapeHtml(r.stt);
        var sttJs = escapeJs(r.stt);

        var audio = r.zh ? '<button class="audio-btn" onclick="speakText(\'' + zhJs + '\', this, event)" title="Nghe"><i class="fas fa-volume-up"></i></button>' : '';
        var writeBtn = '';
        if (r.zh) {
            writeBtn = '<button class="write-btn" onclick="openWriter(\'' + zhJs + '\', \'' + viJs + '\', \'' + pinyinJs + '\', event)" title="Luyện viết"><i class="fas fa-pen-fancy"></i></button>';
        }
        var fullBtn = '';
        if (r.zh) {
            fullBtn = '<button class="practice-full-btn" onclick="openPracticeFull(\'' + sttJs + '\', event)" title="Luyện tập full màn hình"><i class="fas fa-expand"></i></button>';
        }
        var practiceInput = '<input type="text" class="practice-input" placeholder="Gõ tiếng Trung..." data-answer="' + zhHtml + '" data-vi-hint="' + viHtml + '" data-stt="' + sttSafe + '" oninput="checkInput(this)" autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">';
        var toggleCheckBtn = '<button class="toggle-check-btn" onclick="toggleInlineCheck(this, event)" title="Ẩn/hiện kết quả kiểm tra" data-visible="0"><i class="fas fa-eye"></i></button>';

        mobHtml += '<div class="card" onclick="toggleFocus(\'' + sttJs + '\', this)" data-stt="' + sttSafe + '">' +
            '<div class="card-header">' +
                '<div class="card-stt">' + sttSafe + '</div>' +
                '<div class="card-meta">' +
                    (r.hsk ? '<span class="card-tag hsk">' + escapeHtml(r.hsk) + '</span>' : '') +
                    (r.topic ? '<span class="card-tag topic">' + escapeHtml(r.topic) + '</span>' : '') +
                    (r.subject ? '<span class="card-tag">' + escapeHtml(r.subject) + '</span>' : '') +
                '</div>' +
                '<div onclick="event.stopPropagation()" class="action-group">' + audio + writeBtn + fullBtn + '</div>' +
            '</div>' +
            '<div class="card-body">' +
                (r.vi ? '<div class="card-vi">' + viHtml + '</div>' : '') +
                '<div class="card-zh">' + zhHtml + '</div>' +
                (r.pinyin ? '<div class="card-pinyin">' + escapeHtml(r.pinyin) + '</div>' : '') +
            '</div>' +
            '<div class="card-practice" onclick="event.stopPropagation()">' +
                practiceInput +
                toggleCheckBtn +
                '<div class="card-check" data-check-stt="' + sttSafe + '" style="display:none"></div>' +
            '</div>' +
            '</div>';
    }
    mobileWrapper.insertAdjacentHTML('beforeend', mobHtml);
    renderedCount = end;

    var oldMobileBtn = mobileWrapper.querySelector('.load-more');
    if (oldMobileBtn) oldMobileBtn.remove();
    var oldEndNote = mobileWrapper.querySelector('.end-note');
    if (oldEndNote) oldEndNote.remove();

    if (renderedCount < filtered.length) {
        var isDemoLock = isDemo && renderedCount >= DEMO_LIMIT;
        if (!isDemoLock) {
            var btnMobile = document.createElement('button');
            btnMobile.className = 'load-more';
            btnMobile.innerHTML = '<i class="fas fa-chevron-down"></i> Xem thêm (' + renderedCount + '/' + filtered.length + ')';
            btnMobile.onclick = function() { render(false); };
            mobileWrapper.appendChild(btnMobile);
        } else {
            var lockedBtn = document.createElement('button');
            lockedBtn.className = 'load-more locked';
            lockedBtn.innerHTML = '<i class="fas fa-lock"></i> Đăng nhập để xem toàn bộ ' + RAW_DATA.length + ' câu';
            lockedBtn.onclick = function() { showLoginModal(); };
            mobileWrapper.appendChild(lockedBtn);
        }
    } else if (filtered.length > PAGE_SIZE) {
        var endNote = document.createElement('div');
        endNote.className = 'end-note';
        endNote.innerHTML = '<i class="fas fa-check-circle"></i> Đã hiển thị tất cả ' + filtered.length + ' câu';
        mobileWrapper.appendChild(endNote);
    }
}

/* ============ SMART CHECK ============ */
function normalizeAnswer(str) {
    if (!str) return '';
    return String(str)
        .replace(/[。，！？、；：""''「」『』（）《》〈〉【】〔〕]/g, '')
        .replace(/[.,!?;:'"()\[\]{}\-~`@#$%^&*+=|\\/<>]/g, '')
        .replace(/\s+/g, '')
        .toLowerCase()
        .trim();
}
function removeTones(str) {
    if (!str) return '';
    var map = {
        'ā':'a','á':'a','ǎ':'a','à':'a','ē':'e','é':'e','ě':'e','è':'e',
        'ī':'i','í':'i','ǐ':'i','ì':'i','ō':'o','ó':'o','ǒ':'o','ò':'o',
        'ū':'u','ú':'u','ǔ':'u','ù':'u','ǖ':'v','ǘ':'v','ǚ':'v','ǜ':'v','ü':'v'
    };
    return str.replace(/[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]/g, function(c) { return map[c] || c; });
}
function removeFillers(str) {
    if (!str) return '';
    var result = str;
    FILLER_WORDS.forEach(function(w) { result = result.split(w).join(''); });
    return result;
}
function expandSynonyms(str) {
    var results = [str];
    var keys = Object.keys(SYNONYMS);
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        if (str.indexOf(key) !== -1) {
            var values = SYNONYMS[key];
            for (var j = 0; j < values.length; j++) results.push(str.split(key).join(values[j]));
        }
    }
    return results;
}
function levenshtein(a, b) {
    if (a === b) return 0;
    if (!a.length) return b.length;
    if (!b.length) return a.length;
    var matrix = [];
    for (var i = 0; i <= b.length; i++) matrix[i] = [i];
    for (var j = 0; j <= a.length; j++) matrix[0][j] = j;
    for (var i = 1; i <= b.length; i++) {
        for (var j = 1; j <= a.length; j++) {
            if (b.charAt(i-1) === a.charAt(j-1)) matrix[i][j] = matrix[i-1][j-1];
            else matrix[i][j] = Math.min(matrix[i-1][j-1] + 1, matrix[i][j-1] + 1, matrix[i-1][j] + 1);
        }
    }
    return matrix[b.length][a.length];
}
function similarity(a, b) {
    var maxLen = Math.max(a.length, b.length);
    if (maxLen === 0) return 1;
    return 1 - (levenshtein(a, b) / maxLen);
}
function smartCheck(userAnswer, correctAnswer) {
    var user = normalizeAnswer(userAnswer);
    var correct = normalizeAnswer(correctAnswer);
    if (!user) return { status: 'wrong', reason: '' };
    if (user === correct) return { status: 'correct', reason: 'Chính xác' };
    var userNoTone = removeTones(user);
    var correctNoTone = removeTones(correct);
    if (userNoTone === correctNoTone) return { status: 'correct', reason: 'Đúng (thiếu dấu thanh)' };
    var userNoFill = removeFillers(user);
    var correctNoFill = removeFillers(correct);
    if (userNoFill === correctNoFill) return { status: 'correct', reason: 'Đúng (bỏ qua từ phụ)' };
    var uNF = removeTones(userNoFill);
    var cNF = removeTones(correctNoFill);
    if (uNF === cNF) return { status: 'correct', reason: 'Đúng (từ phụ + dấu thanh)' };
    var userVariants = expandSynonyms(userNoFill);
    var correctVariants = expandSynonyms(correctNoFill);
    for (var i = 0; i < userVariants.length; i++) {
        for (var j = 0; j < correctVariants.length; j++) {
            if (userVariants[i] === correctVariants[j]) return { status: 'correct', reason: 'Đúng (từ đồng nghĩa)' };
        }
    }
    var maxSim = 0;
    for (var k = 0; k < correctVariants.length; k++) {
        var sim = similarity(userNoFill, correctVariants[k]);
        if (sim > maxSim) maxSim = sim;
    }
    for (var m = 0; m < userVariants.length; m++) {
        var sim2 = similarity(userVariants[m], correctNoFill);
        if (sim2 > maxSim) maxSim = sim2;
    }
    if (maxSim >= 0.85) return { status: 'partial', reason: 'Gần đúng (' + Math.round(maxSim * 100) + '%)' };
    if (user.indexOf(correct) !== -1 || correct.indexOf(user) !== -1) return { status: 'partial', reason: 'Thiếu/thừa từ' };
    return { status: 'wrong', reason: 'Không khớp' };
}

/* ============ SPLIT BY PINYIN ============ */
function countSyllables(pinyinWord) {
    if (!pinyinWord) return 0;
    var cleaned = pinyinWord.replace(/[.,!?;:'"()\[\]{}\-~`@#$%^&*+=|\\/<>。，！？、；：]/g, '').toLowerCase();
    if (!cleaned) return 0;
    var map = {
        'ā':'a','á':'a','ǎ':'a','à':'a',
        'ē':'e','é':'e','ě':'e','è':'e',
        'ī':'i','í':'i','ǐ':'i','ì':'i',
        'ō':'o','ó':'o','ǒ':'o','ò':'o',
        'ū':'u','ú':'u','ǔ':'u','ù':'u',
        'ǖ':'v','ǘ':'v','ǚ':'v','ǜ':'v','ü':'v'
    };
    cleaned = cleaned.replace(/[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]/g, function(c) {
        return map[c] || c;
    });
    var vowels = 'aeiou';
    var count = 0;
    var prevIsVowel = false;
    for (var i = 0; i < cleaned.length; i++) {
        var c = cleaned[i];
        var isVowel = vowels.indexOf(c) !== -1;
        if (isVowel && !prevIsVowel) count++;
        prevIsVowel = isVowel;
    }
    return count || 1;
}

function splitByPinyin(zh, pinyin) {
    if (!zh) return [];
    var hanziChars = [];
    for (var i = 0; i < zh.length; i++) {
        var c = zh[i];
        if (/[\u4e00-\u9fa5]/.test(c)) hanziChars.push(c);
    }
    if (hanziChars.length === 0) return [];
    if (!pinyin || !pinyin.trim()) {
        return hanziChars.map(function(c) { return { text: c, type: 'phrase' }; });
    }
    var pinyinGroups = pinyin.trim()
        .replace(/[.,!?;:'"()\[\]{}\-~`@#$%^&*+=|\\/<>。，！？、；：]/g, ' ')
        .split(/\s+/)
        .filter(function(w) { return w.length > 0; });
    if (pinyinGroups.length === 0) {
        return hanziChars.map(function(c) { return { text: c, type: 'phrase' }; });
    }
    var syllableCounts = pinyinGroups.map(function(w) { return countSyllables(w); });
    var totalSyllables = syllableCounts.reduce(function(a, b) { return a + b; }, 0);
    if (totalSyllables !== hanziChars.length) {
        return hanziChars.map(function(c) { return { text: c, type: 'phrase' }; });
    }
    var result = [];
    var idx = 0;
    for (var j = 0; j < syllableCounts.length; j++) {
        var cnt = syllableCounts[j];
        if (cnt <= 0) continue;
        var phrase = hanziChars.slice(idx, idx + cnt).join('');
        if (phrase) result.push({ text: phrase, type: 'phrase' });
        idx += cnt;
    }
    if (idx < hanziChars.length) {
        var remaining = hanziChars.slice(idx).join('');
        if (result.length > 0) result[result.length - 1].text += remaining;
        else result.push({ text: remaining, type: 'phrase' });
    }
    return result;
}

/* ============ INLINE PREVIEW + CHECK ============ */
function updateInlinePreview(input, answer) {
    var wrapper = input.parentElement;
    var preview = wrapper.querySelector('.inline-char-preview');
    if (!preview) {
        preview = document.createElement('div');
        preview.className = 'inline-char-preview';
        input.insertAdjacentElement('afterend', preview);
    }
    var userVal = input.value.replace(/\s+/g, '');
    var cleanAnswer = (answer || '').replace(/\s+/g, '');
    if (!cleanAnswer) { preview.innerHTML = ''; return; }
    var html = '';
    var maxLen = Math.max(userVal.length, cleanAnswer.length);
    for (var i = 0; i < maxLen; i++) {
        var userChar = userVal[i] || '';
        var answerChar = cleanAnswer[i] || '';
        var cls = 'char-slot';
        var display = '';
        var clickable = false;
        if (userChar && answerChar) {
            if (userChar === answerChar) {
                cls += ' correct';
                display = userChar;
            } else {
                cls += ' wrong';
                display = userChar;
                clickable = true;
            }
        } else if (!userChar && answerChar) {
            cls += ' ghost-missing';
            display = '·';
            clickable = true;
        } else if (userChar && !answerChar) {
            cls += ' extra';
            display = userChar;
            clickable = true;
        } else {
            continue;
        }
        if (clickable) {
            html += '<span class="' + cls + '" data-idx="' + i + '" onclick="fixInlineChar(this, event)">' + escapeHtml(display) + '</span>';
        } else {
            html += '<span class="' + cls + '">' + escapeHtml(display) + '</span>';
        }
    }
    preview.innerHTML = html;
}

window.fixInlineChar = function(el, evt) {
    if (evt) { evt.stopPropagation(); if (evt.preventDefault) evt.preventDefault(); }

    var wrap = el.closest('.card-practice');
    var input = wrap ? wrap.querySelector('.practice-input') : null;
    if (!input) return;

    var strippedIdx = parseInt(el.dataset.idx);
    var rawVal = input.value;

    var rawIdx = -1;
    var strippedCount = -1;
    for (var i = 0; i < rawVal.length; i++) {
        if (!/\s/.test(rawVal[i])) {
            strippedCount++;
            if (strippedCount === strippedIdx) {
                rawIdx = i;
                break;
            }
        }
    }

    if (rawIdx === -1) rawIdx = rawVal.length;

    while (rawIdx < rawVal.length && /\s/.test(rawVal[rawIdx])) {
        rawIdx++;
    }

    input.focus();
    setTimeout(function() {
        try {
            var endIdx = Math.min(rawIdx + 1, rawVal.length);
            input.setSelectionRange(rawIdx, endIdx);
        } catch(e) {
            input.selectionStart = rawIdx;
            input.selectionEnd = Math.min(rawIdx + 1, rawVal.length);
        }
        el.classList.add('highlight');
        setTimeout(function() { el.classList.remove('highlight'); }, 1200);
    }, 10);
};

function showInlineCheckWithAnswer(input) {
    if (!input) return;
    var stt = input.dataset.stt;
    var answer = input.dataset.answer;
    var cells = document.querySelectorAll('[data-check-stt="' + stt + '"]');
    var val = input.value.trim();
    if (!answer) { cells.forEach(function(c) { c.innerHTML = ''; }); return; }

    var answerHtml = '<div class="answer-inline-display">' +
        '<span class="answer-inline-label"><i class="fas fa-check-circle"></i> Đáp án:</span>' +
        '<span class="answer-inline-text">' + escapeHtml(answer) + '</span>' +
        '</div>';

    var resultHtml = '';
    if (val) {
        var result = smartCheck(val, answer);
        if (result.status === 'correct') resultHtml = '<span class="ai-correct">✅ ĐÚNG</span>';
        else if (result.status === 'partial') resultHtml = '<span class="ai-partial">⚠️ GẦN ĐÚNG</span>';
        else resultHtml = '<span class="ai-wrong">❌ SAI</span>';
        if (result.reason) resultHtml += '<span class="ai-reason">' + escapeHtml(result.reason) + '</span>';
    } else {
        resultHtml = '<span class="ai-reason">Chưa gõ gì cả</span>';
    }

    cells.forEach(function(c) { c.innerHTML = resultHtml + answerHtml; });
}

window.checkInput = function(input) {
    var stt = input.dataset.stt;
    var answer = input.dataset.answer;
    var cells = document.querySelectorAll('[data-check-stt="' + stt + '"]');
    var val = input.value.trim();
    updateInlinePreview(input, answer);

    var wrap = input.closest('.card-practice');
    var btn = wrap ? wrap.querySelector('.toggle-check-btn') : null;
    var isVisible = btn && btn.dataset.visible === '1';

    if (!isVisible) return;

    var answerHtml = '<div class="answer-inline-display">' +
        '<span class="answer-inline-label"><i class="fas fa-check-circle"></i> Đáp án:</span>' +
        '<span class="answer-inline-text">' + escapeHtml(answer) + '</span>' +
        '</div>';

    var resultHtml = '';
    if (val) {
        var result = smartCheck(val, answer);
        if (result.status === 'correct') resultHtml = '<span class="ai-correct">✅ ĐÚNG</span>';
        else if (result.status === 'partial') resultHtml = '<span class="ai-partial">⚠️ GẦN ĐÚNG</span>';
        else resultHtml = '<span class="ai-wrong">❌ SAI</span>';
        if (result.reason) resultHtml += '<span class="ai-reason">' + escapeHtml(result.reason) + '</span>';
    } else {
        resultHtml = '<span class="ai-reason">Chưa gõ gì cả</span>';
    }

    cells.forEach(function(c) { c.innerHTML = resultHtml + answerHtml; });
};

window.toggleInlineCheck = function(btn, evt) {
    if (evt) { evt.stopPropagation(); if (evt.preventDefault) evt.preventDefault(); }
    var wrap = btn.closest('.card-practice');
    if (!wrap) return;
    var checkEl = wrap.querySelector('.card-check');
    var input = wrap.querySelector('.practice-input');
    if (!checkEl) return;

    var isVisible = btn.dataset.visible === '1';
    if (isVisible) {
        checkEl.style.display = 'none';
        btn.dataset.visible = '0';
        btn.innerHTML = '<i class="fas fa-eye"></i>';
        btn.classList.remove('active');
    } else {
        checkEl.style.display = 'block';
        btn.dataset.visible = '1';
        btn.innerHTML = '<i class="fas fa-eye-slash"></i>';
        btn.classList.add('active');
        showInlineCheckWithAnswer(input);
    }
};

/* ============ APPLY FILTER ============ */
function applyFilter() {
    state.search = $('searchInput').value.trim().toLowerCase();
    state.hsk = $('hskFilter').value;
    state.subject = $('subjectFilter').value;
    updateFilterUI();
    var clearBtn = $('clearSearchBtn');
    if (state.search) clearBtn.classList.add('show');
    else clearBtn.classList.remove('show');

    // ✅ Chặn user hết hạn
    var isLimitedUser = isDemo;
    if (!isDemo && currentUser && currentUser.role !== 'admin') {
        var dl = getDaysRemaining(currentUser);
        if (dl !== null && dl <= 0) isLimitedUser = true;
    }
    var baseData = isLimitedUser ? getDemoData() : RAW_DATA;

    filtered = baseData.filter(function(r) {
        if (state.search) {
            var s = state.search;
            var inVi = (r.vi || '').toLowerCase().indexOf(s) !== -1;
            var inZh = (r.zh || '').toLowerCase().indexOf(s) !== -1;
            var inPinyin = (r.pinyin || '').toLowerCase().indexOf(s) !== -1;
            var inTopic = (r.topic || '').toLowerCase().indexOf(s) !== -1;
            var inSubject = (r.subject || '').toLowerCase().indexOf(s) !== -1;
            if (!inVi && !inZh && !inPinyin && !inTopic && !inSubject) return false;
        }
        if (state.hsk && r.hsk !== state.hsk) return false;
        if (state.subject && r.subject !== state.subject) return false;
        return true;
    });
    updateResultCount();
    render(true);
}
/* ============ PRACTICE FULL MODE ============ */
var pfCurrentStt = null;
var pfCurrentAnswer = '';
var pfCurrentVi = '';
var pfCurrentPinyin = '';
var pfHintEnabled = false;

function setPracticeFullTop() {
    var stickyTop = $('stickyTop');
    var modal = $('practiceFullModal');
    if (!stickyTop || !modal) return;
    var rect = stickyTop.getBoundingClientRect();
    var height = Math.max(0, rect.bottom);
    modal.style.top = height + 'px';
}

window.addEventListener('resize', function() {
    if ($('practiceFullModal') && $('practiceFullModal').classList.contains('show')) {
        setPracticeFullTop();
    }
});

window.openPracticeFull = function(stt, evt) {
    if (evt) { evt.stopPropagation(); if (evt.preventDefault) evt.preventDefault(); }

    // ✅ Chặn user hết hạn
    if (!isDemo && currentUser && currentUser.role !== 'admin') {
        var dl = getDaysRemaining(currentUser);
        if (dl !== null && dl <= 0) {
            showLimitMessage();
            return;
        }
    }

    pfBuildFilterOptions();
    pfBuildQuickNav();

    var idx = -1;
    for (var i = 0; i < filtered.length; i++) {
        if (String(filtered[i].stt) === String(stt)) { idx = i; break; }
    }
    if (idx === -1) { alert('Không tìm thấy câu!'); return; }
    pfCurrentStt = stt;

    document.body.classList.add('practice-full-open');
    if (typeof updateFloatingLeftVisibility === 'function') updateFloatingLeftVisibility();
    document.body.style.overflow = 'hidden';

    setPracticeFullTop();

    $('practiceFullModal').classList.add('show');

    requestAnimationFrame(function() {
        setPracticeFullTop();
    });

    loadPracticeFull(stt);
};
window.closePracticeFull = function() {
    $('practiceFullModal').classList.remove('show');
    document.body.style.overflow = '';
    document.body.classList.remove('practice-full-open');
    $('practiceFullModal').style.top = '0px';
    if (typeof updateFloatingLeftVisibility === 'function') updateFloatingLeftVisibility();
    pfCurrentStt = null;
    if ('speechSynthesis' in window) speechSynthesis.cancel();
};

function loadPracticeFull(stt) {
    var idx = -1;
    for (var i = 0; i < filtered.length; i++) {
        if (String(filtered[i].stt) === String(stt)) { idx = i; break; }
    }
    if (idx === -1) return;

    if (!$('pfSearchInput').value && !$('pfHskFilter').value && !$('pfSubjectFilter').value) {
        $('pfSearchInput').value = $('searchInput').value;
        $('pfHskFilter').value = $('hskFilter').value;
        $('pfSubjectFilter').value = $('subjectFilter').value;
    }
    pfUpdateFilterUI();

    var r = filtered[idx];
    pfCurrentStt = stt;
    pfCurrentAnswer = r.zh || '';
    pfCurrentVi = r.vi || '';
    pfCurrentPinyin = r.pinyin || '';

    $('pfCounter').textContent = 'Câu ' + (idx + 1) + ' / ' + filtered.length;

    var tagsHtml = '';
    if (r.hsk) tagsHtml += '<span class="card-tag hsk">' + escapeHtml(r.hsk) + '</span>';
    if (r.topic) tagsHtml += '<span class="card-tag topic">' + escapeHtml(r.topic) + '</span>';
    if (r.subject) tagsHtml += '<span class="card-tag">' + escapeHtml(r.subject) + '</span>';
    $('pfTags').innerHTML = tagsHtml;

    $('pfVi').textContent = pfCurrentVi;
    $('pfInput').value = '';
    $('pfStatus').textContent = '';
    $('pfStatus').className = 'practice-full-status';

    $('pfAnswer').classList.remove('show');
    var revealBtn = $('pfRevealBtn');
    revealBtn.classList.remove('revealed', 'hidden');
    revealBtn.innerHTML = '<i class="fas fa-eye"></i> Xem đáp án';

    pfHintEnabled = false;
    $('pfHintBtn').classList.remove('active');

    updateCharPreview();

    $('pfPrevBtn').disabled = (idx === 0);
    $('pfNextBtn').disabled = (idx === filtered.length - 1);

    var quickNav = $('pfQuickNav');
    if (quickNav && quickNav.value !== stt) {
        quickNav.value = stt;
    }

    setTimeout(function() {
        var active = document.activeElement;
        if (active && (active.tagName === 'INPUT' ||
                       active.tagName === 'TEXTAREA' ||
                       active.tagName === 'SELECT')) {
            return;
        }
        $('pfInput').focus();
    }, 200);
}

window.pfNext = function() {
    if (!pfCurrentStt) return;
    var idx = -1;
    for (var i = 0; i < filtered.length; i++) {
        if (String(filtered[i].stt) === String(pfCurrentStt)) { idx = i; break; }
    }
    if (idx === -1 || idx >= filtered.length - 1) return;
    loadPracticeFull(filtered[idx + 1].stt);
};

window.pfPrev = function() {
    if (!pfCurrentStt) return;
    var idx = -1;
    for (var i = 0; i < filtered.length; i++) {
        if (String(filtered[i].stt) === String(pfCurrentStt)) { idx = i; break; }
    }
    if (idx <= 0) return;
    loadPracticeFull(filtered[idx - 1].stt);
};

function pfBuildQuickNav() {
    var sel = $('pfQuickNav');
    if (!sel) return;

    var html = '<option value="">-- Chọn câu (' + filtered.length + ') --</option>';
    filtered.forEach(function(r, i) {
        var vi = (r.vi || '').substring(0, 45);
        var label = 'Câu ' + (i + 1) + ': ' + vi;
        html += '<option value="' + escapeHtml(r.stt) + '">' + escapeHtml(label) + '</option>';
    });
    sel.innerHTML = html;

    if (pfCurrentStt) {
        sel.value = pfCurrentStt;
    }
}

function pfQuickNavChange() {
    var sel = $('pfQuickNav');
    if (!sel) return;
    var stt = sel.value;
    if (!stt) return;
    loadPracticeFull(stt);
}

function pfBuildFilterOptions() {
    var hskSel = $('pfHskFilter');
    var subjSel = $('pfSubjectFilter');

    var allSubjectSet = {};
    RAW_DATA.forEach(function(r) { if (r.subject) allSubjectSet[r.subject] = 1; });
    var allSubjects = Object.keys(allSubjectSet).sort();

    if (isDemo) {
        var demoHsk = getDemoHskList();
        var hskHtml = '<option value="">Tất cả</option>';
        demoHsk.forEach(function(h) { hskHtml += '<option value="' + h + '">' + h + '</option>'; });
        var allHskList = ['HSK1','HSK2','HSK3','HSK4','HSK5','HSK6'];
        allHskList.forEach(function(h) {
            if (demoHsk.indexOf(h) === -1) hskHtml += '<option value="' + h + '" disabled>🔒 ' + h + '</option>';
        });
        hskSel.innerHTML = hskHtml;

        var demoSubjects = getDemoSubjectList();
        var demoSubjectMap = {};
        demoSubjects.forEach(function(s) { demoSubjectMap[s] = 1; });
        var unlocked = [];
        var locked = [];
        allSubjects.forEach(function(s) {
            if (demoSubjectMap[s]) unlocked.push(s);
            else locked.push(s);
        });
        var subjHtml = '<option value="">Tất cả chủ đề</option>';
        unlocked.forEach(function(s) { subjHtml += '<option value="' + escapeHtml(s) + '">' + escapeHtml(s) + '</option>'; });
        locked.forEach(function(s) { subjHtml += '<option value="' + escapeHtml(s) + '" disabled>🔒 ' + escapeHtml(s) + '</option>'; });
        subjSel.innerHTML = subjHtml;
    } else {
        hskSel.innerHTML =
            '<option value="">Tất cả</option>' +
            '<option value="HSK1">HSK1</option>' +
            '<option value="HSK2">HSK2</option>' +
            '<option value="HSK3">HSK3</option>' +
            '<option value="HSK4">HSK4</option>' +
            '<option value="HSK5">HSK5</option>' +
            '<option value="HSK6">HSK6</option>';
        subjSel.innerHTML = '<option value="">Tất cả chủ đề</option>' +
            allSubjects.map(function(v){ return '<option value="'+escapeHtml(v)+'">'+escapeHtml(v)+'</option>'; }).join('');
    }

    hskSel.value = $('hskFilter').value;
    subjSel.value = $('subjectFilter').value;
    $('pfSearchInput').value = $('searchInput').value;

    pfUpdateFilterUI();
}

function pfUpdateFilterUI() {
    var hsk = $('pfHskFilter').value;
    var subject = $('pfSubjectFilter').value;
    $('pfHskValue').textContent = hsk || 'Tất cả';
    $('pfSubjectValue').textContent = subject || 'Tất cả';
    $('pfHskChip').classList.toggle('has-value', !!hsk);
    $('pfSubjectChip').classList.toggle('has-value', !!subject);

    var search = $('pfSearchInput').value.trim();
    if (search) $('pfClearSearchBtn').classList.add('show');
    else $('pfClearSearchBtn').classList.remove('show');

    pfUpdateResultCount();
}

function pfUpdateResultCount() {
    var el = $('pfResultCount');
    if (!el) return;
    var total = filtered ? filtered.length : 0;
    var search = $('pfSearchInput').value.trim();
    var hsk = $('pfHskFilter').value;
    var subject = $('pfSubjectFilter').value;
    var hasFilter = !!(search || hsk || subject);
    if (!hasFilter) { el.classList.remove('show', 'empty'); return; }
    el.classList.add('show');
    el.classList.toggle('empty', total === 0);
    var spanEl = el.querySelector('span');
    if (spanEl) {
        if (total === 0) spanEl.innerHTML = 'Không tìm thấy kết quả';
        else spanEl.innerHTML = 'Tìm thấy <b>' + total + '</b> kết quả';
    }
}

function pfApplyFilter() {
    $('searchInput').value = $('pfSearchInput').value;
    $('hskFilter').value = $('pfHskFilter').value;
    $('subjectFilter').value = $('pfSubjectFilter').value;

    state.search = $('pfSearchInput').value.trim().toLowerCase();
    state.hsk = $('pfHskFilter').value;
    state.subject = $('pfSubjectFilter').value;

    // ✅ Chặn user hết hạn
    var isLimitedUser = isDemo;
    if (!isDemo && currentUser && currentUser.role !== 'admin') {
        var dl = getDaysRemaining(currentUser);
        if (dl !== null && dl <= 0) isLimitedUser = true;
    }
    var baseData = isLimitedUser ? getDemoData() : RAW_DATA;

    filtered = baseData.filter(function(r) {
        if (state.search) {
            var s = state.search;
            var inVi = (r.vi || '').toLowerCase().indexOf(s) !== -1;
            var inZh = (r.zh || '').toLowerCase().indexOf(s) !== -1;
            var inPinyin = (r.pinyin || '').toLowerCase().indexOf(s) !== -1;
            var inTopic = (r.topic || '').toLowerCase().indexOf(s) !== -1;
            var inSubject = (r.subject || '').toLowerCase().indexOf(s) !== -1;
            if (!inVi && !inZh && !inPinyin && !inTopic && !inSubject) return false;
        }
        if (state.hsk && r.hsk !== state.hsk) return false;
        if (state.subject && r.subject !== state.subject) return false;
        return true;
    });

    updateFilterUI();
    var clearBtn = $('clearSearchBtn');
    if (state.search) clearBtn.classList.add('show');
    else clearBtn.classList.remove('show');

    pfUpdateFilterUI();
    pfBuildQuickNav();
    render(true);

    var activeEl = document.activeElement;
    var isTypingInSearch = activeEl && activeEl.id === 'pfSearchInput';

    var currentStillValid = false;
    if (pfCurrentStt) {
        for (var i = 0; i < filtered.length; i++) {
            if (String(filtered[i].stt) === String(pfCurrentStt)) {
                currentStillValid = true;
                break;
            }
        }
    }

    if (filtered.length > 0) {
        if (isTypingInSearch && currentStillValid) {
            var idx = -1;
            for (var j = 0; j < filtered.length; j++) {
                if (String(filtered[j].stt) === String(pfCurrentStt)) { idx = j; break; }
            }
            if (idx !== -1) {
                $('pfCounter').textContent = 'Câu ' + (idx + 1) + ' / ' + filtered.length;
            }
            return;
        }
        loadPracticeFull(filtered[0].stt);
    } else {
        pfCurrentStt = null;
        pfCurrentAnswer = '';
        pfCurrentVi = 'Không tìm thấy câu nào';
        pfCurrentPinyin = '';
        $('pfVi').textContent = 'Không tìm thấy câu nào';
        $('pfInput').value = '';
        $('pfCounter').textContent = 'Câu 0 / 0';
        $('pfTags').innerHTML = '';
        $('pfAnswer').classList.remove('show');
        $('pfPreview').innerHTML = '';
        $('pfStatus').textContent = '';
        $('pfPrevBtn').disabled = true;
        $('pfNextBtn').disabled = true;
    }
}
function updateCharPreview() {
    var input = $('pfInput');
    var preview = $('pfPreview');
    var userVal = input.value;
    var cleanUser = userVal.replace(/\s+/g, '');
    var cleanAnswer = pfCurrentAnswer.replace(/\s+/g, '');

    if (!cleanAnswer) { preview.innerHTML = ''; return; }

    var html = '';
    var maxLen = Math.max(cleanUser.length, cleanAnswer.length);

    for (var i = 0; i < maxLen; i++) {
        var userChar = cleanUser[i] || '';
        var answerChar = cleanAnswer[i] || '';
        var cls = 'char-slot';
        var display = '';
        var clickable = false;

        if (userChar && answerChar) {
            if (userChar === answerChar) {
                cls += ' correct';
                display = userChar;
            } else {
                cls += ' wrong';
                display = userChar;
                clickable = true;
            }
        } else if (!userChar && answerChar) {
            if (pfHintEnabled) {
                cls += ' ghost';
                display = answerChar;
            } else {
                continue;
            }
        } else if (userChar && !answerChar) {
            cls += ' extra';
            display = userChar;
            clickable = true;
        } else {
            continue;
        }

        if (clickable) {
            html += '<span class="' + cls + '" data-idx="' + i + '" onclick="fixCharAt(' + i + ', this)">' + escapeHtml(display) + '</span>';
        } else {
            html += '<span class="' + cls + '">' + escapeHtml(display) + '</span>';
        }
    }

    preview.innerHTML = html;
}

window.fixCharAt = function(idx, el) {
    var input = $('pfInput');
    if (!input) return;
    input.focus();
    setTimeout(function() {
        try {
            input.setSelectionRange(idx, idx + 1);
        } catch(e) {
            input.selectionStart = idx;
            input.selectionEnd = idx + 1;
        }
        if (el) {
            el.classList.add('highlight');
            setTimeout(function() { el.classList.remove('highlight'); }, 1200);
        }
    }, 10);
};

function toggleHint() {
    pfHintEnabled = !pfHintEnabled;
    var btn = $('pfHintBtn');
    if (pfHintEnabled) btn.classList.add('active');
    else btn.classList.remove('active');
    updateCharPreview();
}

function checkFullAnswer() {
    var input = $('pfInput');
    var statusEl = $('pfStatus');
    var val = input.value.trim();
    if (!val) {
        statusEl.textContent = '';
        statusEl.className = 'practice-full-status';
        return;
    }
    var result = smartCheck(val, pfCurrentAnswer);
    if (result.status === 'correct') {
        statusEl.textContent = '✅ ĐÚNG';
        statusEl.className = 'practice-full-status correct';
    } else if (result.status === 'partial') {
        statusEl.textContent = '⚠️ ' + (result.reason || 'GẦN ĐÚNG');
        statusEl.className = 'practice-full-status partial';
    } else {
        statusEl.textContent = '❌ SAI';
        statusEl.className = 'practice-full-status wrong';
    }
}

function revealFullAnswer() {
    var answerEl = $('pfAnswer');
    var revealBtn = $('pfRevealBtn');

    if (answerEl.classList.contains('show')) {
        answerEl.classList.remove('show');
        revealBtn.classList.remove('revealed');
        revealBtn.innerHTML = '<i class="fas fa-eye"></i> Xem đáp án';
        return;
    }

    var charsEl = $('pfAnswerChars');
    var pinyinEl = $('pfAnswerPinyin');

    charsEl.innerHTML = '';
    var phrases = splitByPinyin(pfCurrentAnswer, pfCurrentPinyin);

    if (phrases.length === 0) {
        pfCurrentAnswer.split('').forEach(function(c) {
            if (/[\u4e00-\u9fa5]/.test(c)) phrases.push({ text: c, type: 'phrase' });
        });
    }

    phrases.forEach(function(item) {
        var btn = document.createElement('button');
        btn.className = 'answer-phrase-btn';
        btn.textContent = item.text;
        btn.title = 'Nhấn để đọc: ' + item.text;

        btn.onclick = (function(text, el) {
            return function(e) {
                e.stopPropagation();
                el.classList.add('zoom-in');
                setTimeout(function() { el.classList.remove('zoom-in'); }, 700);
                speakPhrase(text, el);
            };
        })(item.text, btn);

        charsEl.appendChild(btn);
    });

    pinyinEl.textContent = pfCurrentPinyin;
    answerEl.classList.add('show');
    revealBtn.classList.add('revealed');
    revealBtn.innerHTML = '<i class="fas fa-eye-slash"></i> Ẩn đáp án';
}

window.speakPhrase = function(phrase, btn) {
    if (isDemo && !canUseFeature()) { showLimitMessage(); return; }
    if (!isDemo && !canUseFeature()) { showLimitMessage(); return; }
    if (!('speechSynthesis' in window)) { alert('Trình duyệt không hỗ trợ phát âm.'); return; }
    if (isDemo) { incDemoUsage(); updateDemoRemaining(); }
    speechSynthesis.cancel();
    document.querySelectorAll('.answer-phrase-btn.speaking').forEach(function(b) { b.classList.remove('speaking'); });
    btn.classList.add('speaking');
    var utterance = new SpeechSynthesisUtterance(phrase);
    utterance.lang = 'zh-CN';
    utterance.rate = 0.75;
    var voice = getChineseVoice();
    if (voice) utterance.voice = voice;
    utterance.onend = utterance.onerror = function() { btn.classList.remove('speaking'); };
    setTimeout(function(){ speechSynthesis.speak(utterance); }, 30);
};

window.speakFullSentence = function() {
    if (isDemo && !canUseFeature()) { showLimitMessage(); return; }
    if (!isDemo && !canUseFeature()) { showLimitMessage(); return; }
    if (!('speechSynthesis' in window)) return;
    if (isDemo) { incDemoUsage(); updateDemoRemaining(); }
    speechSynthesis.cancel();
    var utterance = new SpeechSynthesisUtterance(pfCurrentAnswer);
    utterance.lang = 'zh-CN';
    utterance.rate = 0.85;
    var voice = getChineseVoice();
    if (voice) utterance.voice = voice;
    setTimeout(function(){ speechSynthesis.speak(utterance); }, 30);
};

function initPracticeFull() {
    $('pfClose').addEventListener('click', closePracticeFull);
    $('pfPrevBtn').addEventListener('click', pfPrev);
    $('pfNextBtn').addEventListener('click', pfNext);
    $('pfRevealBtn').addEventListener('click', revealFullAnswer);
    $('pfHintBtn').addEventListener('click', toggleHint);
    $('pfInput').addEventListener('input', function() {
        updateCharPreview();
        checkFullAnswer();
    });

    $('pfQuickNav').addEventListener('change', pfQuickNavChange);

    $('pfSearchInput').addEventListener('input', function() {
        pfApplyFilter();
    });
    $('pfClearSearchBtn').addEventListener('click', function() {
        $('pfSearchInput').value = '';
        $('pfSearchInput').focus();
        pfApplyFilter();
    });

    $('pfHskFilter').addEventListener('change', function() {
        if (isDemo) {
            var val = this.value;
            var allowed = getDemoHskList();
            if (val && allowed.indexOf(val) === -1) {
                alert('🔒 Bản Demo chỉ cho phép lọc HSK1-' + DEMO_HSK_MAX + '.');
                this.value = '';
                return;
            }
        }
        pfApplyFilter();
    });
    $('pfSubjectFilter').addEventListener('change', function() {
        if (isDemo) {
            var val = this.value;
            var allowed = getDemoSubjectList();
            if (val && allowed.indexOf(val) === -1) {
                alert('🔒 Chủ đề này chưa có trong Demo.');
                this.value = '';
                return;
            }
        }
        pfApplyFilter();
    });

    document.addEventListener('keydown', function(e) {
        if (!$('practiceFullModal').classList.contains('show')) return;

        var active = document.activeElement;
        var isTyping = active && (active.tagName === 'INPUT' ||
                                    active.tagName === 'TEXTAREA' ||
                                    active.tagName === 'SELECT');

        if (e.key === 'Escape') {
            closePracticeFull();
            return;
        }

        if (isTyping) return;

        if (e.key === 'ArrowRight' && e.ctrlKey) pfNext();
        if (e.key === 'ArrowLeft' && e.ctrlKey) pfPrev();
    });

    var modal = $('practiceFullModal');
    var touchStartX = 0;
    modal.addEventListener('touchstart', function(e) {
        touchStartX = e.touches[0].clientX;
    }, { passive: true });
    modal.addEventListener('touchend', function(e) {
        var dx = e.changedTouches[0].clientX - touchStartX;
        if (Math.abs(dx) > 100) {
            if (dx < 0) pfNext();
            else pfPrev();
        }
    }, { passive: true });
}

/* ============ WRITER ============ */
var writerInstance = null;
var currentWriteZh = '';
var currentWriteVi = '';
var currentWritePinyin = '';
var currentCharIndex = 0;

function initWriter() {
    $('writerAnimate').addEventListener('click', function() {
        if (!writerInstance) return;
        $('writerScore').textContent = '';
        $('writerScore').className = 'writer-score';
        writerInstance.cancelQuiz();
        writerInstance.animateCharacter();
    });
    $('writerQuiz').addEventListener('click', function() {
        if (!writerInstance) return;
        $('writerScore').textContent = 'Vẽ chữ bằng ngón tay...';
        $('writerScore').className = 'writer-score';
        writerInstance.quiz({
            onMistake: function(strokeData) {
                $('writerScore').textContent = 'Sai nét ' + (strokeData.strokeNum + 1) + ' - thử lại';
                $('writerScore').className = 'writer-score error';
            },
            onComplete: function(summary) {
                if (summary.totalMistakes === 0) {
                    $('writerScore').textContent = '🎉 Tuyệt vời! Viết đúng tất cả các nét!';
                    $('writerScore').className = 'writer-score success';
                } else {
                    $('writerScore').textContent = 'Hoàn thành! Số nét sai: ' + summary.totalMistakes;
                    $('writerScore').className = 'writer-score';
                }
            }
        });
    });
    $('writerReset').addEventListener('click', function() {
        if (!writerInstance) return;
        $('writerScore').textContent = '';
        $('writerScore').className = 'writer-score';
        writerInstance.cancelQuiz();
        var chars = currentWriteZh.split('').filter(function(c) { return /[\u4e00-\u9fa5]/.test(c); });
        var currentChar = chars[currentCharIndex];
        if (currentChar) showWriterChar(currentChar);
    });
    $('writerClose').addEventListener('click', closeWriter);
    $('writerModal').addEventListener('click', function(e) {
        if (e.target === this) closeWriter();
    });
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') closeWriter();
    });
}

window.openWriter = function(zh, vi, pinyin, evt) {
    if (evt) { evt.stopPropagation(); if (evt.preventDefault) evt.preventDefault(); }
    if (!canUseFeature()) { showLimitMessage(); return; }
    if (typeof HanziWriter === 'undefined') { alert('Thư viện chưa tải xong.'); return; }
    if (isDemo) { incDemoUsage(); updateDemoRemaining(); }
    currentWriteZh = zh || '';
    currentWriteVi = vi || '';
    currentWritePinyin = pinyin || '';
    currentCharIndex = 0;
    var chars = currentWriteZh.split('').filter(function(c) { return /[\u4e00-\u9fa5]/.test(c); });
    if (chars.length === 0) { alert('Câu này không có chữ Hán.'); return; }
    $('writerModal').classList.add('show');
    $('writerScore').textContent = '';
    $('writerScore').className = 'writer-score';
    $('writerViSmall').textContent = currentWriteVi;
    $('writerPinyinSmall').textContent = currentWritePinyin;
    renderWriterChars(chars);
    showWriterChar(chars[0]);
};

window.closeWriter = function() {
    $('writerModal').classList.remove('show');
    writerInstance = null;
};

function renderWriterChars(chars) {
    var container = $('writerChars');
    if (chars.length <= 1) { container.innerHTML = ''; return; }
    container.innerHTML = chars.map(function(c, i) {
        return '<button class="writer-char-btn' + (i === 0 ? ' active' : '') + '" data-idx="' + i + '" data-char="' + c + '">' + c + '</button>';
    }).join('');
    container.querySelectorAll('.writer-char-btn').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var idx = parseInt(this.dataset.idx);
            var ch = this.dataset.char;
            container.querySelectorAll('.writer-char-btn').forEach(function(b) { b.classList.remove('active'); });
            this.classList.add('active');
            currentCharIndex = idx;
            $('writerScore').textContent = '';
            $('writerScore').className = 'writer-score';
            showWriterChar(ch);
        });
    });
}

function showWriterChar(char) {
    var target = $('writerTarget');
    target.innerHTML = '<div class="writer-loading"><i class="fas fa-spinner fa-pulse"></i>Đang tải...</div>';
    writerInstance = null;
    setTimeout(function() {
        try {
            target.innerHTML = '';
            var targetSize = target.offsetWidth || 280;
            var padSize = Math.round(targetSize * 0.06);
            var drawWidth = Math.round(targetSize * 0.07);
            writerInstance = HanziWriter.create('writerTarget', char, {
                width: targetSize, height: targetSize, padding: padSize,
                strokeColor: '#1e293b', radicalColor: '#2563eb',
                highlightColor: '#f59e0b', outlineColor: '#cbd5e1',
                drawingColor: '#2563eb', drawingWidth: drawWidth,
                showOutline: true, strokeAnimationSpeed: 1, delayBetweenStrokes: 250,
                charDataLoader: function(ch, onComplete, onError) {
                    fetch('https://cdn.jsdelivr.net/npm/hanzi-writer-data@2.0/' + encodeURIComponent(ch) + '.json')
                        .then(function(res) { if (!res.ok) throw new Error('Không có dữ liệu'); return res.json(); })
                        .then(onComplete)
                        .catch(function(err) {
                            if (onError) onError(err);
                            target.innerHTML = '<div class="writer-loading"><i class="fas fa-exclamation-triangle" style="color:#dc2626"></i>Không tải được dữ liệu.</div>';
                        });
                }
            });
        } catch(e) {
            target.innerHTML = '<div class="writer-loading"><i class="fas fa-exclamation-triangle"></i>Lỗi tạo khung vẽ</div>';
        }
    }, 100);
}
"""

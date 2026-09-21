# -*- coding: utf-8 -*-
"""
Module GỘP: Auth + Firebase + Admin panel + Trial + Renewal (QR ngân hàng).
Đọc config từ file JSON bên ngoài (config.json) — không còn placeholder.

Cách dùng:
    import json
    from accounts import (
        build_accounts_css, build_accounts_html, build_accounts_js,
        build_renewal_css, build_renewal_html, build_renewal_js,
        build_all_auth  # helper gộp hết
    )
    cfg = json.load(open("config.json", encoding="utf-8"))
    css, html, js = build_all_auth(cfg)
"""

import json


# ═══════════════════════════════════════════════════════════════
# CSS (gộp accounts_css + renewal_css)
# ═══════════════════════════════════════════════════════════════
def build_accounts_css():
    return r"""
/* ============ USER MENU ============ */
.user-menu{position:relative}
.user-avatar{width:38px;height:38px;border-radius:50%;border:2px solid var(--border);cursor:pointer;object-fit:cover;transition:.15s;display:block;}
.user-avatar:hover{border-color:var(--primary);transform:scale(1.05)}
.user-dropdown{position:absolute;top:calc(100% + .5rem);right:0;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);box-shadow:0 10px 30px rgba(0,0,0,.15);padding:.5rem;min-width:290px;display:none;z-index:200;}
.user-dropdown.show{display:block}
.user-info{padding:.75rem;border-bottom:1px solid var(--border);margin-bottom:.5rem}
.user-info .name{font-weight:700;font-size:.9rem;color:var(--text);margin-bottom:.2rem}
.user-info .email{font-size:.75rem;color:var(--text-3);word-break:break-all}
.user-info .role{display:inline-block;margin-top:.4rem;padding:.15rem .5rem;background:var(--primary-light);color:var(--primary-dark);border-radius:50px;font-size:.68rem;font-weight:700;text-transform:uppercase;letter-spacing:.3px;}
.user-info .role.admin{background:var(--amber-light);color:#92400e}
.dropdown-item{display:flex;align-items:center;gap:.5rem;width:100%;padding:.65rem .75rem;border:none;border-radius:var(--radius-sm);background:transparent;color:var(--text);font-size:.85rem;font-weight:600;cursor:pointer;transition:.15s;font-family:inherit;text-align:left;}
.dropdown-item:hover{background:var(--surface-2)}
.dropdown-item.danger{color:var(--danger)}
.dropdown-item.danger:hover{background:var(--danger-light)}

/* ============ DROPDOWN: NÚT GIA HẠN NỔI BẬT ============ */
.dropdown-renew{
    display:flex;align-items:center;justify-content:center;gap:.5rem;
    width:100%;padding:.75rem 1rem;margin:.4rem 0;
    border:none;border-radius:12px;
    background:linear-gradient(135deg,#f59e0b,#d97706 60%,#dc2626);
    color:#fff;font-size:.9rem;font-weight:800;cursor:pointer;
    transition:all .2s ease;font-family:inherit;
    text-transform:uppercase;letter-spacing:.5px;
    box-shadow:0 4px 14px rgba(245,158,11,.45), 0 0 0 0 rgba(245,158,11,.6);
    position:relative;overflow:hidden;
    animation:renewPulse 2.5s infinite;
}
.dropdown-renew::before{
    content:'';position:absolute;top:0;left:-100%;
    width:100%;height:100%;
    background:linear-gradient(90deg, transparent, rgba(255,255,255,.4), transparent);
    animation:renewShine 3s infinite;
}
.dropdown-renew:hover,.dropdown-renew:active{
    transform:translateY(-2px) scale(1.02);
    box-shadow:0 8px 20px rgba(245,158,11,.6), 0 0 0 4px rgba(245,158,11,.25);
    background:linear-gradient(135deg,#fbbf24,#f59e0b 60%,#ef4444);
}
.dropdown-renew i{
    font-size:1rem;filter:drop-shadow(0 1px 2px rgba(0,0,0,.2));
    position:relative;z-index:1;
}
.dropdown-renew span{
    position:relative;z-index:1;
}
@keyframes renewPulse{
    0%,100%{box-shadow:0 4px 14px rgba(245,158,11,.45), 0 0 0 0 rgba(245,158,11,.6);}
    50%{box-shadow:0 4px 14px rgba(245,158,11,.6), 0 0 0 6px rgba(245,158,11,0);}
}
@keyframes renewShine{
    0%{left:-100%;}
    50%,100%{left:100%;}
}

/* Badge "HOT" nhấp nháy */
.dropdown-renew .renew-badge{
    position:absolute;top:-6px;right:-4px;
    background:linear-gradient(135deg,#dc2626,#ef4444);
    color:#fff;font-size:.55rem;font-weight:900;
    padding:.15rem .4rem;border-radius:50px;
    letter-spacing:.5px;
    box-shadow:0 2px 6px rgba(220,38,38,.5);
    animation:renewBadgeBlink 1.5s infinite;
    border:1.5px solid #fff;
    z-index:2;
}
@keyframes renewBadgeBlink{
    0%,100%{transform:scale(1);opacity:1;}
    50%{transform:scale(1.15);opacity:.85;}
}

/* Hiệu ứng "hết hạn" — nhấp nháy đỏ mạnh hơn */
.dropdown-renew.urgent{
    background:linear-gradient(135deg,#dc2626,#b91c1c 60%,#7f1d1d);
    animation:renewUrgent 1.2s infinite;
}
.dropdown-renew.urgent:hover{
    background:linear-gradient(135deg,#ef4444,#dc2626 60%,#991b1b);
}
@keyframes renewUrgent{
    0%,100%{box-shadow:0 4px 14px rgba(220,38,38,.6), 0 0 0 0 rgba(220,38,38,.7);}
    50%{box-shadow:0 4px 18px rgba(220,38,38,.8), 0 0 0 8px rgba(220,38,38,0);}
}

/* Dark mode */
[data-theme="dark"] .dropdown-renew{
    box-shadow:0 4px 14px rgba(245,158,11,.5), 0 0 0 0 rgba(245,158,11,.6);
}
[data-theme="dark"] .dropdown-renew .renew-badge{
    border-color:#1e293b;
}

.user-details{padding:.6rem .75rem .75rem;border-bottom:1px solid var(--border);margin-bottom:.5rem;display:flex;flex-direction:column;gap:.6rem;}
.detail-row{display:flex;align-items:flex-start;gap:.65rem;}
.detail-icon{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:.95rem;flex-shrink:0;background:var(--surface-2);color:var(--text-2);transition:.2s;}
.detail-icon.ok{background:rgba(22,163,74,.12);color:var(--success);}
.detail-icon.warn{background:rgba(245,158,11,.15);color:#d97706;}
.detail-icon.urgent{background:rgba(220,38,38,.15);color:var(--danger);}
.detail-icon.permanent{background:var(--primary-light);color:var(--primary-dark);}
.detail-icon.expired{background:rgba(220,38,38,.25);color:var(--danger);}
[data-theme="dark"] .detail-icon.ok{background:rgba(22,163,74,.25);color:#4ade80;}
[data-theme="dark"] .detail-icon.warn{background:rgba(245,158,11,.25);color:#fcd34d;}
[data-theme="dark"] .detail-icon.urgent{background:rgba(220,38,38,.3);color:#fca5a5;}
[data-theme="dark"] .detail-icon.permanent{background:rgba(59,130,246,.25);color:#93c5fd;}
[data-theme="dark"] .detail-icon.expired{background:rgba(220,38,38,.35);color:#fca5a5;}

.detail-content{flex:1;min-width:0;}
.detail-label{font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.3px;color:var(--text-3);margin-bottom:.15rem;}
.detail-value{font-size:.85rem;font-weight:700;color:var(--text);line-height:1.3;word-break:break-word;}
.detail-value.ok{color:var(--success);}
.detail-value.warn{color:#d97706;}
[data-theme="dark"] .detail-value.warn{color:#fcd34d;}
.detail-value.urgent{color:var(--danger);}
.detail-value.permanent{color:var(--primary-dark);}
[data-theme="dark"] .detail-value.permanent{color:#93c5fd;}
.detail-value.expired{color:var(--danger);text-decoration:line-through;}
.detail-sub{font-size:.7rem;color:var(--text-3);margin-top:.15rem;line-height:1.35;}
.detail-sub b{color:var(--text-2);font-weight:700;}
.detail-progress{margin-top:.15rem;}
.progress-track{width:100%;height:6px;background:var(--surface-2);border-radius:50px;overflow:hidden;border:1px solid var(--border);}
.progress-bar{height:100%;border-radius:50px;transition:width .4s ease, background .3s ease;background:linear-gradient(90deg, #16a34a, #22c55e);}
.progress-bar.ok{background:linear-gradient(90deg, #16a34a, #22c55e);}
.progress-bar.warn{background:linear-gradient(90deg, #f59e0b, #fbbf24);}
.progress-bar.urgent{background:linear-gradient(90deg, #dc2626, #ef4444);}
.progress-bar.permanent{background:linear-gradient(90deg, #2563eb, #3b82f6);}

.btn-login-header{display:flex;align-items:center;gap:.4rem;padding:.55rem 1rem;border-radius:50px;background:var(--primary);color:#fff;border:none;font-size:.85rem;font-weight:700;cursor:pointer;transition:.15s;font-family:inherit;box-shadow:0 4px 12px rgba(37,99,235,.3);white-space:nowrap;}
.btn-login-header:hover,.btn-login-header:active{background:var(--primary-dark);transform:translateY(-1px)}

/* ============ LOGIN MODAL ============ */
.login-modal{position:fixed;inset:0;background:rgba(15,23,42,.8);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);z-index:3000;display:none;align-items:center;justify-content:center;padding:1.5rem;animation:fadeIn .2s;}
.login-modal.show{display:flex}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
.login-box{background:#fff;border-radius:20px;padding:2.5rem 2rem;max-width:440px;width:100%;box-shadow:0 20px 60px rgba(0,0,0,.3);text-align:center;position:relative;animation:slideUp .3s cubic-bezier(.34,1.56,.64,1);}
@keyframes slideUp{from{transform:translateY(30px) scale(.95);opacity:0}to{transform:translateY(0) scale(1);opacity:1}}
.login-close{position:absolute;top:12px;right:12px;width:34px;height:34px;border-radius:50%;border:none;background:#f1f5f9;color:#475569;cursor:pointer;font-size:1rem;display:flex;align-items:center;justify-content:center;transition:.15s;}
.login-close:hover{background:#fee2e2;color:#dc2626}
.login-logo{width:70px;height:70px;background:linear-gradient(135deg,#2563eb,#7c3aed);border-radius:20px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:2rem;margin:0 auto 1.5rem;box-shadow:0 8px 20px rgba(37,99,235,.35);}
.login-box h2{font-size:1.4rem;color:#0f172a;margin-bottom:.5rem;font-weight:700}
.login-box p{color:#64748b;font-size:.9rem;margin-bottom:2rem;line-height:1.5}
.btn-google{display:flex;align-items:center;justify-content:center;gap:.75rem;width:100%;padding:.9rem 1.5rem;border-radius:50px;border:2px solid #e2e8f0;background:#fff;color:#0f172a;font-size:1rem;font-weight:600;cursor:pointer;transition:.15s;font-family:inherit;}
.btn-google:hover{border-color:#2563eb;background:#f0f7ff;transform:translateY(-1px);box-shadow:0 4px 12px rgba(37,99,235,.15)}
.btn-google img{width:22px;height:22px}
.login-error{background:#fee2e2;color:#dc2626;padding:.85rem 1rem;border-radius:10px;font-size:.85rem;margin-top:1rem;display:none;text-align:left;line-height:1.4;}
.login-error.show{display:block}
.login-footer{margin-top:1.5rem;padding-top:1.5rem;border-top:1px solid #e2e8f0;font-size:.78rem;color:#94a3b8;line-height:1.5}

/* ============ ADMIN MODAL ============ */
.admin-modal{position:fixed;inset:0;background:rgba(15,23,42,.75);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);z-index:3000;display:none;align-items:center;justify-content:center;padding:1rem;animation:fadeIn .2s;}
.admin-modal.show{display:flex}
.admin-box{background:var(--surface);border-radius:20px;width:100%;max-width:900px;max-height:calc(100vh - 2rem);overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,.3);display:flex;flex-direction:column;}
.admin-header{padding:1.25rem 1.5rem;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;}
.admin-header h2{font-size:1.15rem;color:var(--text);display:flex;align-items:center;gap:.5rem;font-weight:700}
.admin-header h2 i{color:var(--amber)}
.admin-header-actions{display:flex;gap:.5rem;align-items:center;flex-wrap:wrap}
.admin-body{padding:1.25rem 1.5rem;overflow-y:auto;flex:1}
.admin-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:.75rem;margin-bottom:1.25rem;}
.stat-card{background:var(--surface-2);border:1px solid var(--border);border-radius:var(--radius);padding:1rem;text-align:center;}
.stat-card .num{font-size:1.8rem;font-weight:800;color:var(--primary);line-height:1;margin-bottom:.3rem}
.stat-card .label{font-size:.75rem;color:var(--text-3);text-transform:uppercase;letter-spacing:.3px;font-weight:600}
.admin-section-title{font-size:.75rem;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--text-3);margin-bottom:.6rem;display:flex;align-items:center;justify-content:space-between;}
.admin-section-title i{margin-right:.3rem;}
.btn-add{padding:.45rem .85rem;border-radius:8px;border:none;background:var(--primary);color:#fff;font-size:.78rem;font-weight:600;cursor:pointer;display:inline-flex;align-items:center;gap:.35rem;transition:.15s;font-family:inherit;}
.btn-add:hover{background:var(--primary-dark)}
.user-list{display:flex;flex-direction:column;gap:.5rem}
.user-row{display:flex;align-items:center;gap:.75rem;padding:.75rem;background:var(--surface-2);border:1px solid var(--border);border-radius:var(--radius-sm);transition:.15s;}
.user-row:hover{border-color:var(--primary)}
.user-row .u-info{flex:1;min-width:0}
.user-row .u-name{font-weight:700;font-size:.88rem;color:var(--text);margin-bottom:.15rem}
.user-row .u-email{font-size:.75rem;color:var(--text-3);word-break:break-all}
.user-row .u-role{padding:.15rem .5rem;border-radius:50px;font-size:.65rem;font-weight:700;text-transform:uppercase;letter-spacing:.3px;white-space:nowrap;}
.user-row .u-role.admin{background:var(--amber-light);color:#92400e}
.user-row .u-role.user{background:var(--primary-light);color:var(--primary-dark)}
.user-row .u-role.super{background:linear-gradient(135deg, #f59e0b, #d97706);color:#fff;box-shadow:0 2px 6px rgba(245,158,11,.4);}
.user-row .u-actions{display:flex;gap:.3rem}
.u-btn{width:32px;height:32px;border-radius:8px;border:1px solid var(--border);background:var(--surface);color:var(--text-2);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:.8rem;transition:.15s;}
.u-btn:hover{background:var(--surface-2);color:var(--primary);border-color:var(--primary)}
.u-btn.danger:hover{background:var(--danger-light);color:var(--danger);border-color:var(--danger)}
.u-btn.expiry{background:rgba(245,158,11,.1);color:#d97706;border-color:rgba(245,158,11,.4);}
.u-btn.expiry:hover{background:var(--amber);color:#fff;border-color:var(--amber);transform:scale(1.08);}
.u-btn.expiry.urgent{background:rgba(220,38,38,.15);color:var(--danger);border-color:rgba(220,38,38,.5);animation:expiryPulse 2s infinite;}
.u-btn:disabled{opacity:.35;cursor:not-allowed}
@keyframes expiryPulse{0%,100%{box-shadow:0 0 0 0 rgba(220,38,38,.4);}50%{box-shadow:0 0 0 6px rgba(220,38,38,0);}}

.admin-close{width:34px;height:34px;border-radius:8px;border:1px solid var(--border);background:var(--surface);color:var(--text-2);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:.9rem;transition:.15s;}
.admin-close:hover{background:var(--danger-light);color:var(--danger);border-color:var(--danger)}
.add-user-form{background:var(--surface-2);border:1px solid var(--border);border-radius:var(--radius-sm);padding:1rem;margin-bottom:1rem;display:none;}
.add-user-form.show{display:block}
.add-user-form h3{font-size:.85rem;color:var(--text);margin-bottom:.75rem;font-weight:700}
.form-group{margin-bottom:.75rem}
.form-group label{display:block;font-size:.75rem;font-weight:600;color:var(--text-2);margin-bottom:.3rem}
.form-group input,.form-group select{width:100%;padding:.6rem .85rem;border-radius:8px;border:1.5px solid var(--border);background:var(--surface);color:var(--text);font-size:.85rem;outline:none;transition:.15s;font-family:inherit;}
.form-group input:focus,.form-group select:focus{border-color:var(--primary);box-shadow:0 0 0 3px rgba(37,99,235,.15)}
.form-actions{display:flex;gap:.5rem;justify-content:flex-end;margin-top:.75rem}
.btn{padding:.55rem 1rem;border-radius:8px;border:1.5px solid var(--border);background:var(--surface);color:var(--text);font-size:.82rem;font-weight:600;cursor:pointer;transition:.15s;font-family:inherit;display:inline-flex;align-items:center;gap:.35rem;}
.btn:hover{background:var(--surface-2)}
.btn:disabled{opacity:.5;cursor:not-allowed;}
.btn.primary{background:var(--primary);color:#fff;border-color:var(--primary)}
.btn.primary:hover{background:var(--primary-dark)}
.logs-list{max-height:200px;overflow-y:auto;background:var(--surface-2);border:1px solid var(--border);border-radius:var(--radius-sm);padding:.5rem;}
.log-item{display:flex;gap:.5rem;padding:.4rem .5rem;font-size:.75rem;color:var(--text-2);border-bottom:1px solid var(--border);}
.log-item:last-child{border-bottom:none}
.log-item .log-time{color:var(--text-3);flex-shrink:0;font-family:monospace;font-size:.7rem}
.log-item .log-msg{flex:1;word-break:break-word}
.u-last-login{font-size:.68rem;color:var(--text-3);display:flex;align-items:center;gap:.25rem;margin-top:.2rem;}
.u-last-login.active{color:var(--success);}
.u-last-login.recent{color:var(--primary);}
.u-expiry{font-size:.68rem;font-weight:600;display:inline-flex;align-items:center;gap:.25rem;margin-top:.2rem;padding:.15rem .45rem;border-radius:50px;cursor:pointer;transition:.15s;}
.u-expiry:hover{opacity:.8;}
.u-expiry.permanent{background:rgba(148,163,184,.15);color:var(--text-3);}
.u-expiry.ok{background:rgba(22,163,74,.12);color:var(--success);}
.u-expiry.warn{background:rgba(245,158,11,.15);color:#92400e;}
.u-expiry.urgent{background:rgba(220,38,38,.15);color:var(--danger);}
.u-expiry.expired{background:rgba(220,38,38,.25);color:#fff;text-decoration:line-through;}

/* ============ EDIT MODALS ============ */
.edit-modal{position:fixed;inset:0;background:rgba(15,23,42,.85);backdrop-filter:blur(4px);-webkit-backdrop-filter:blur(4px);z-index:4000;display:none;align-items:center;justify-content:center;padding:1rem;animation:fadeIn .2s;}
.edit-modal.show{display:flex}
.edit-box{background:var(--surface);border-radius:20px;width:100%;max-width:420px;box-shadow:0 20px 60px rgba(0,0,0,.4);padding:1.5rem;position:relative;animation:slideUp .3s cubic-bezier(.34,1.56,.64,1);}
.edit-box h2{font-size:1.1rem;color:var(--text);font-weight:700;display:flex;align-items:center;gap:.5rem;margin-bottom:1.25rem;}
.edit-box h2 i{color:var(--primary);}
.edit-close{position:absolute;top:12px;right:12px;width:32px;height:32px;border-radius:8px;border:1px solid var(--border);background:var(--surface);color:var(--text-2);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:.85rem;transition:.15s;}
.edit-close:hover{background:var(--danger-light);color:var(--danger);border-color:var(--danger)}
.edit-user-info{padding:.75rem;background:var(--surface-2);border-radius:10px;margin-bottom:1rem;border:1px solid var(--border);}
.edit-user-info .eu-name{font-weight:700;font-size:.9rem;color:var(--text);margin-bottom:.2rem}
.edit-user-info .eu-email{font-size:.75rem;color:var(--text-3);word-break:break-all}
.quick-expiry-btns{display:grid;grid-template-columns:repeat(3,1fr);gap:.4rem;margin-bottom:1rem;}
.quick-expiry-btn{padding:.5rem .4rem;border-radius:8px;border:1.5px solid var(--border);background:var(--surface);color:var(--text-2);font-size:.72rem;font-weight:600;cursor:pointer;transition:.15s;font-family:inherit;display:flex;flex-direction:column;align-items:center;gap:.2rem;white-space:nowrap;}
.quick-expiry-btn:hover{background:var(--primary-light);border-color:var(--primary);color:var(--primary-dark);transform:translateY(-1px);}
.quick-expiry-btn.danger:hover{background:var(--danger-light);border-color:var(--danger);color:var(--danger);}

/* ============ IMPORT MODAL ============ */
.import-modal{position:fixed;inset:0;background:rgba(15,23,42,.85);backdrop-filter:blur(4px);z-index:3500;display:none;align-items:center;justify-content:center;padding:1rem;animation:fadeIn .2s;}
.import-modal.show{display:flex}
.import-box{background:var(--surface);border-radius:20px;width:100%;max-width:900px;max-height:calc(100vh - 2rem);box-shadow:0 20px 60px rgba(0,0,0,.4);display:flex;flex-direction:column;overflow:hidden;}
.import-header{padding:1.25rem 1.5rem;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;}
.import-header h2{font-size:1.15rem;color:var(--text);display:flex;align-items:center;gap:.5rem;font-weight:700;}
.import-header h2 i{color:#16a34a;}
.import-body{padding:1.25rem 1.5rem;overflow-y:auto;flex:1;min-height:0;}
.import-summary{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:.6rem;margin-bottom:1rem;}
.import-stat{padding:.65rem .85rem;border-radius:10px;text-align:center;border:1px solid var(--border);background:var(--surface-2);}
.import-stat .num{font-size:1.5rem;font-weight:800;line-height:1;margin-bottom:.25rem;}
.import-stat .label{font-size:.7rem;color:var(--text-3);text-transform:uppercase;font-weight:600;}
.import-stat.ok .num{color:var(--success);}
.import-stat.update .num{color:var(--primary);}
.import-stat.warn .num{color:var(--amber);}
.import-stat.err .num{color:var(--danger);}
.import-preview-wrap{max-height:400px;overflow-y:auto;border:1px solid var(--border);border-radius:10px;background:var(--surface-2);}
.import-table{width:100%;border-collapse:collapse;font-size:.82rem;}
.import-table th{padding:.6rem .8rem;text-align:left;background:var(--surface);color:var(--text-2);font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.3px;border-bottom:2px solid var(--border);position:sticky;top:0;z-index:2;}
.import-table td{padding:.55rem .8rem;color:var(--text);border-bottom:1px solid var(--border);word-break:break-word;}
.import-table tr:last-child td{border-bottom:none;}
.import-table tr.row-error{background:rgba(220,38,38,.08);}
.import-table tr.row-warn{background:rgba(245,158,11,.08);}
.import-table tr.row-new{background:rgba(22,163,74,.05);}
.import-table tr.row-update{background:rgba(37,99,235,.05);}
.import-table .status-badge{display:inline-flex;align-items:center;gap:.3rem;padding:.2rem .5rem;border-radius:50px;font-size:.68rem;font-weight:700;white-space:nowrap;}
.import-table .status-badge.ok{background:rgba(22,163,74,.15);color:var(--success);}
.import-table .status-badge.update{background:rgba(37,99,235,.15);color:var(--primary);}
.import-table .status-badge.warn{background:rgba(245,158,11,.15);color:#92400e;}
.import-table .status-badge.err{background:rgba(220,38,38,.15);color:var(--danger);}
.import-table .role-badge{display:inline-block;padding:.15rem .5rem;border-radius:50px;font-size:.68rem;font-weight:700;text-transform:uppercase;}
.import-table .role-badge.admin{background:var(--amber-light);color:#92400e;}
.import-table .role-badge.user{background:var(--primary-light);color:var(--primary-dark);}
.import-options{display:flex;gap:1rem;margin-top:1rem;flex-wrap:wrap;}
.import-options label{display:flex;align-items:center;gap:.4rem;font-size:.82rem;font-weight:600;color:var(--text-2);cursor:pointer;user-select:none;}
.import-options input[type="checkbox"]{width:16px;height:16px;accent-color:var(--primary);cursor:pointer;}
.import-info{margin-top:1rem;padding:.65rem .85rem;border-radius:10px;background:var(--primary-light);color:var(--primary-dark);font-size:.78rem;line-height:1.6;display:flex;align-items:flex-start;gap:.5rem;}
.import-info i{margin-top:.15rem;flex-shrink:0;}
.import-info b{font-weight:800;}
.import-footer{padding:1rem 1.5rem;border-top:1px solid var(--border);display:flex;gap:.5rem;justify-content:flex-end;align-items:center;background:var(--surface);}

/* ============ EXPIRY BANNER ============ */
.expiry-banner{background:linear-gradient(135deg, #fef3c7, #fde68a);border:1.5px solid #f59e0b;border-radius:var(--radius);padding:.85rem 1.1rem;margin-bottom:1rem;display:flex;align-items:center;gap:.75rem;flex-wrap:wrap;}
.expiry-banner.urgent{background:linear-gradient(135deg, #fecaca, #fca5a5);border-color:#dc2626;animation:pulseUrgent 2s infinite;}
@keyframes pulseUrgent{0%,100%{box-shadow:0 0 0 0 rgba(220,38,38,.4);}50%{box-shadow:0 0 0 8px rgba(220,38,38,0);}}
.expiry-banner-icon{width:36px;height:36px;border-radius:50%;background:#f59e0b;color:#fff;display:flex;align-items:center;justify-content:center;font-size:1rem;flex-shrink:0;}
.expiry-banner.urgent .expiry-banner-icon{background:#dc2626;}
.expiry-banner-text{flex:1;min-width:200px}
.expiry-banner-text .title{font-weight:700;font-size:.9rem;color:#92400e;margin-bottom:.15rem;}
.expiry-banner-text .desc{font-size:.78rem;color:#78350f;line-height:1.5;}
.expiry-banner-text b{color:#dc2626;}
.expiry-banner-btn{padding:.5rem .9rem;border-radius:50px;border:none;background:#f59e0b;color:#fff;text-decoration:none;font-size:.8rem;font-weight:700;cursor:pointer;transition:.15s;display:inline-flex;align-items:center;gap:.35rem;white-space:nowrap;}
.expiry-banner-btn:hover{background:#d97706;color:#fff;transform:translateY(-1px);}
.expiry-banner.urgent .expiry-banner-btn{background:#dc2626;}

/* Nút Gia hạn trong banner hết hạn — nổi bật hơn */
.expiry-banner.urgent .expiry-banner-btn{
    background:linear-gradient(135deg,#dc2626,#b91c1c);
    box-shadow:0 4px 14px rgba(220,38,38,.5), 0 0 0 0 rgba(220,38,38,.6);
    animation:renewUrgent 1.2s infinite;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:.5px;
}
.expiry-banner.urgent .expiry-banner-btn:hover{
    transform:translateY(-2px) scale(1.03);
    box-shadow:0 8px 20px rgba(220,38,38,.7);
}

/* ============ RENEWAL MODAL (QR ngân hàng) ============ */
.renewal-modal{position:fixed;inset:0;background:rgba(15,23,42,.85);backdrop-filter:blur(6px);z-index:3500;display:none;align-items:center;justify-content:center;padding:1rem;animation:fadeIn .2s;overflow-y:auto;}
.renewal-modal.show{display:flex}
.renewal-box{background:var(--surface);border-radius:20px;width:100%;max-width:560px;max-height:calc(100vh - 2rem);box-shadow:0 20px 60px rgba(0,0,0,.4);display:flex;flex-direction:column;overflow:hidden;animation:slideUp .3s cubic-bezier(.34,1.56,.64,1);}
.renewal-header{padding:1.25rem 1.5rem;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;gap:1rem;background:linear-gradient(135deg,#2563eb,#7c3aed);color:#fff;}
.renewal-header h2{font-size:1.15rem;font-weight:800;display:flex;align-items:center;gap:.5rem;color:#fff;margin:0;}
.renewal-header .subtitle{font-size:.78rem;opacity:.9;margin-top:.15rem;}
.renewal-close{width:34px;height:34px;border-radius:50%;border:none;background:rgba(255,255,255,.2);color:#fff;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:1rem;transition:.15s;flex-shrink:0;}
.renewal-close:hover{background:rgba(255,255,255,.35)}
.renewal-body{padding:1.5rem;overflow-y:auto;flex:1;}
.renewal-current{padding:.85rem 1rem;border-radius:12px;background:linear-gradient(135deg, rgba(37,99,235,.08), rgba(124,58,237,.08));border:1px solid rgba(37,99,235,.25);margin-bottom:1.25rem;display:flex;align-items:center;gap:.75rem;}
.renewal-current .rc-icon{width:42px;height:42px;border-radius:12px;background:var(--primary);color:#fff;display:flex;align-items:center;justify-content:center;font-size:1.15rem;flex-shrink:0;}
.renewal-current.warn .rc-icon{background:var(--amber);}
.renewal-current.expired .rc-icon{background:var(--danger);}
.renewal-current .rc-info{flex:1;min-width:0;}
.renewal-current .rc-title{font-weight:800;font-size:.9rem;color:var(--text);margin-bottom:.15rem;}
.renewal-current .rc-desc{font-size:.75rem;color:var(--text-2);line-height:1.4;}
.renewal-current .rc-desc b{color:var(--primary);}
.renewal-section-title{font-size:.72rem;font-weight:800;color:var(--text-3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:.6rem;display:flex;align-items:center;gap:.35rem;}
.package-grid{display:grid;grid-template-columns:1fr;gap:.6rem;margin-bottom:1.25rem;}
@media(min-width:480px){.package-grid{grid-template-columns:1fr 1fr 1fr;}}
.package-card{padding:.9rem .75rem;border-radius:12px;border:2px solid var(--border);background:var(--surface);cursor:pointer;transition:.2s;text-align:center;position:relative;user-select:none;}
.package-card:hover{border-color:var(--primary);transform:translateY(-2px);}
.package-card.selected{border-color:var(--primary);background:linear-gradient(135deg, rgba(37,99,235,.08), rgba(124,58,237,.08));box-shadow:0 6px 20px rgba(37,99,235,.25);}
.package-card .pkg-label{font-weight:800;font-size:.95rem;color:var(--text);margin-bottom:.3rem;}
.package-card .pkg-price{font-weight:900;font-size:1.25rem;color:var(--primary);line-height:1;margin-bottom:.25rem;}
.package-card .pkg-unit{font-size:.68rem;color:var(--text-3);font-weight:600;}
.package-card .pkg-save{position:absolute;top:-8px;right:-4px;background:linear-gradient(135deg,#16a34a,#22c55e);color:#fff;font-size:.6rem;font-weight:800;padding:.15rem .45rem;border-radius:50px;text-transform:uppercase;letter-spacing:.3px;box-shadow:0 2px 6px rgba(22,163,74,.4);}
.package-card .pkg-popular{position:absolute;top:-8px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;font-size:.6rem;font-weight:800;padding:.15rem .5rem;border-radius:50px;text-transform:uppercase;letter-spacing:.3px;white-space:nowrap;box-shadow:0 2px 6px rgba(245,158,11,.4);}
.qr-wrap{display:flex;flex-direction:column;align-items:center;gap:.75rem;padding:1rem;background:linear-gradient(135deg,#f0f4f8,#e2e8f0);border-radius:14px;border:1.5px dashed var(--border);}
.qr-img{width:220px;height:220px;background:#fff;padding:.5rem;border-radius:10px;box-shadow:0 4px 16px rgba(0,0,0,.15);}
.qr-wrap .qr-hint{font-size:.75rem;color:var(--text-2);text-align:center;line-height:1.5;max-width:300px;}
.qr-wrap .qr-hint b{color:var(--primary);}
.bank-info{padding:.9rem 1rem;border-radius:12px;background:var(--surface-2);border:1px solid var(--border);display:flex;flex-direction:column;gap:.55rem;}
.bank-row{display:flex;justify-content:space-between;align-items:center;gap:.75rem;font-size:.82rem;}
.bank-row .br-label{color:var(--text-3);font-weight:600;flex-shrink:0;}
.bank-row .br-value{color:var(--text);font-weight:700;word-break:break-all;text-align:right;}
.bank-row .br-value.code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:var(--danger);font-size:.95rem;background:rgba(220,38,38,.08);padding:.15rem .5rem;border-radius:6px;letter-spacing:1px;}
.copy-btn{width:28px;height:28px;border-radius:6px;border:1px solid var(--border);background:var(--surface);color:var(--text-2);cursor:pointer;display:inline-flex;align-items:center;justify-content:center;font-size:.75rem;transition:.15s;margin-left:.4rem;}
.copy-btn:hover{background:var(--primary-light);color:var(--primary-dark);border-color:var(--primary);}
.copy-btn.copied{background:var(--success);color:#fff;border-color:var(--success);}
.payment-steps{display:flex;flex-direction:column;gap:.5rem;padding:.85rem 1rem;border-radius:12px;background:linear-gradient(135deg, rgba(245,158,11,.1), rgba(245,158,11,.05));border:1px solid rgba(245,158,11,.3);}
.payment-steps .step{display:flex;gap:.6rem;font-size:.8rem;color:var(--text-2);line-height:1.5;align-items:flex-start;}
.payment-steps .step .num{width:20px;height:20px;border-radius:50%;background:var(--amber);color:#fff;display:flex;align-items:center;justify-content:center;font-size:.68rem;font-weight:800;flex-shrink:0;margin-top:.05rem;}
.payment-steps .step b{color:var(--text);}
.renewal-actions{display:flex;gap:.6rem;justify-content:flex-end;padding-top:1rem;border-top:1px solid var(--border);}
.renewal-btn{padding:.7rem 1.2rem;border-radius:10px;border:1.5px solid var(--border);background:var(--surface);color:var(--text);font-size:.85rem;font-weight:700;cursor:pointer;transition:.15s;font-family:inherit;display:inline-flex;align-items:center;gap:.4rem;}
.renewal-btn:hover{background:var(--surface-2);}
.renewal-btn.primary{background:var(--primary);color:#fff;border-color:var(--primary);box-shadow:0 4px 12px rgba(37,99,235,.3);}
.renewal-btn.success{background:var(--success);color:#fff;border-color:var(--success);box-shadow:0 4px 12px rgba(22,163,74,.3);}
.renewal-btn:disabled{opacity:.5;cursor:not-allowed;}
.renewal-success{text-align:center;padding:2rem 1rem;display:flex;flex-direction:column;align-items:center;gap:1rem;}
.renewal-success .icon{width:70px;height:70px;border-radius:50%;background:linear-gradient(135deg,#16a34a,#22c55e);color:#fff;display:flex;align-items:center;justify-content:center;font-size:2rem;box-shadow:0 8px 24px rgba(22,163,74,.4);animation:successPop .5s cubic-bezier(.34,1.56,.64,1);}
@keyframes successPop{0%{transform:scale(0);}70%{transform:scale(1.15);}100%{transform:scale(1);}}
.renewal-success h3{font-size:1.15rem;font-weight:800;color:var(--text);margin:0;}
.renewal-success p{font-size:.85rem;color:var(--text-2);line-height:1.6;max-width:340px;margin:0;}
.renewal-success .info-box{padding:.65rem 1rem;border-radius:10px;background:var(--surface-2);border:1px solid var(--border);font-size:.78rem;color:var(--text-2);display:flex;align-items:center;gap:.5rem;text-align:left;}

.renewal-admin-row{display:flex;flex-direction:column;gap:.5rem;padding:.85rem;border-radius:10px;background:var(--surface-2);border:1px solid var(--border);margin-bottom:.5rem;}
.renewal-admin-row .rar-head{display:flex;justify-content:space-between;gap:.5rem;flex-wrap:wrap;align-items:flex-start;}
.renewal-admin-row .rar-email{font-weight:800;font-size:.88rem;color:var(--text);word-break:break-all;}
.renewal-admin-row .rar-sub{font-size:.72rem;color:var(--text-3);margin-top:.15rem;}
.renewal-admin-row .rar-pkg{text-align:right;}
.renewal-admin-row .rar-amount{font-weight:900;font-size:1.05rem;color:var(--primary);line-height:1;}
.renewal-admin-row .rar-pkg-label{font-size:.7rem;color:var(--text-3);margin-top:.15rem;}
.renewal-admin-row .rar-foot{display:flex;justify-content:space-between;align-items:center;gap:.5rem;padding-top:.5rem;border-top:1px solid var(--border);flex-wrap:wrap;}
.renewal-admin-row .rar-code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.78rem;color:var(--danger);background:rgba(220,38,38,.08);padding:.15rem .5rem;border-radius:6px;letter-spacing:.5px;font-weight:800;}
.renewal-admin-row .rar-status{display:inline-flex;align-items:center;gap:.25rem;padding:.2rem .5rem;border-radius:50px;font-size:.65rem;font-weight:800;text-transform:uppercase;letter-spacing:.3px;}
.renewal-admin-row .rar-status.pending{background:rgba(37,99,235,.15);color:#2563eb;}
.renewal-admin-row .rar-status.user_paid{background:rgba(245,158,11,.18);color:#d97706;}
.renewal-admin-row .rar-actions{display:flex;gap:.35rem;align-items:center;flex-wrap:wrap;}
"""


def build_renewal_css():
    # Đã gộp vào build_accounts_css
    return ""


# ═══════════════════════════════════════════════════════════════
# HTML
# ═══════════════════════════════════════════════════════════════
def build_accounts_html():
    return r"""
<div class="login-modal" id="loginModal">
    <div class="login-box">
        <button class="login-close" id="loginClose"><i class="fas fa-times"></i></button>
        <div class="login-logo"><i class="fas fa-language"></i></div>
        <h2>Đăng nhập để mở khóa</h2>
        <p>Đăng nhập bằng Google để sử dụng <b>toàn bộ câu</b>, tất cả bộ lọc HSK1-6, chủ đề đầy đủ, luyện viết không giới hạn và nhiều tính năng khác.</p>
        <button class="btn-google" id="googleLoginBtn">
            <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google">
            Đăng nhập bằng Google
        </button>
        <div class="login-error" id="loginError"></div>
        <div class="login-footer">
            <i class="fas fa-shield-alt"></i> Tài khoản mới được <b>tặng miễn phí <span id="trialDaysText">7</span> ngày</b> dùng thử.
        </div>
    </div>
</div>

<div class="edit-modal" id="changeNameModal">
    <div class="edit-box">
        <button class="edit-close" id="changeNameClose"><i class="fas fa-times"></i></button>
        <h2><i class="fas fa-user-edit"></i> Đổi tên hiển thị</h2>
        <div class="edit-user-info">
            <div class="eu-name" id="changeNameCurrent">-</div>
            <div class="eu-email" id="changeNameEmail">-</div>
        </div>
        <div class="form-group">
            <label>Tên mới</label>
            <input type="text" id="changeNameInput" placeholder="Nhập tên mới..." maxlength="50">
        </div>
        <div class="form-actions">
            <button class="btn" id="changeNameCancel">Hủy</button>
            <button class="btn primary" id="changeNameConfirm"><i class="fas fa-check"></i> Lưu</button>
        </div>
    </div>
</div>

<div class="edit-modal" id="editExpiryModal">
    <div class="edit-box">
        <button class="edit-close" id="editExpiryClose"><i class="fas fa-times"></i></button>
        <h2><i class="fas fa-calendar-edit"></i> Chỉnh hạn sử dụng</h2>
        <div class="edit-user-info">
            <div class="eu-name" id="editExpiryName">-</div>
            <div class="eu-email" id="editExpiryEmail">-</div>
        </div>
        <div class="quick-expiry-btns">
            <button class="quick-expiry-btn" onclick="setQuickExpiry(7)"><i class="fas fa-calendar-plus"></i> +7 ngày</button>
            <button class="quick-expiry-btn" onclick="setQuickExpiry(30)"><i class="fas fa-calendar-plus"></i> +30 ngày</button>
            <button class="quick-expiry-btn" onclick="setQuickExpiry(90)"><i class="fas fa-calendar-plus"></i> +90 ngày</button>
            <button class="quick-expiry-btn" onclick="setQuickExpiry(180)"><i class="fas fa-calendar-plus"></i> +6 tháng</button>
            <button class="quick-expiry-btn" onclick="setQuickExpiry(365)"><i class="fas fa-calendar-plus"></i> +1 năm</button>
            <button class="quick-expiry-btn danger" onclick="setQuickExpiryPermanent()"><i class="fas fa-infinity"></i> Vĩnh viễn</button>
        </div>
        <div class="form-group">
            <label>Hoặc chọn ngày cụ thể</label>
            <input type="date" id="editExpiryInput">
        </div>
        <div class="form-actions">
            <button class="btn" id="editExpiryCancel">Hủy</button>
            <button class="btn primary" id="editExpiryConfirm"><i class="fas fa-check"></i> Lưu</button>
        </div>
    </div>
</div>

<div class="renewal-modal" id="renewalModal">
    <div class="renewal-box">
        <div class="renewal-header">
            <div>
                <h2><i class="fas fa-crown"></i> Gia hạn tài khoản</h2>
                <div class="subtitle">Chọn gói phù hợp và thanh toán</div>
            </div>
            <button class="renewal-close" id="renewalClose"><i class="fas fa-times"></i></button>
        </div>
        <div class="renewal-body" id="renewalBody"></div>
    </div>
</div>

<div class="import-modal" id="importModal">
    <div class="import-box">
        <div class="import-header">
            <h2><i class="fas fa-file-import"></i> Import danh sách user</h2>
            <button class="admin-close" id="importClose"><i class="fas fa-times"></i></button>
        </div>
        <div class="import-body">
            <div class="import-summary" id="importSummary"></div>
            <div class="import-preview-wrap">
                <table class="import-table">
                    <thead>
                        <tr>
                            <th style="width:45px">#</th>
                            <th>Email</th>
                            <th>Tên</th>
                            <th style="width:80px">Vai trò</th>
                            <th style="width:110px">Hạn dùng</th>
                            <th style="width:130px">Trạng thái</th>
                        </tr>
                    </thead>
                    <tbody id="importTableBody"></tbody>
                </table>
            </div>
            <div class="import-options">
                <label><input type="checkbox" id="importSkipDuplicates"> Bỏ qua user đã tồn tại (không update)</label>
                <label><input type="checkbox" id="importSkipInvalid" checked> Bỏ qua dòng không hợp lệ</label>
            </div>
            <div class="import-info">
                <i class="fas fa-info-circle"></i>
                <div>
                    File Excel cần có cột: <b>email</b> (bắt buộc), <b>name</b> (tùy chọn), <b>expiresAt</b> (tùy chọn).
                    <br>• <b>email</b>: bắt buộc, phải hợp lệ
                    <br>• <b>name</b>: nếu thiếu sẽ lấy phần trước @ của email
                    <br>• <b>expiresAt</b>: định dạng <b>YYYY-MM-DD</b>, để trống = vĩnh viễn
                    <br><b>⚠️ Lưu ý:</b> Chỉ import <b>user</b>, KHÔNG import admin.
                </div>
            </div>
        </div>
        <div class="import-footer">
            <button class="btn" id="importCancelBtn">Hủy</button>
            <button class="btn primary" id="importConfirmBtn"><i class="fas fa-check"></i> Import <span id="importCount">0</span> user</button>
        </div>
    </div>
</div>

<div class="admin-modal" id="adminModal">
    <div class="admin-box">
        <div class="admin-header">
            <h2><i class="fas fa-shield-alt"></i> Quản lý tài khoản</h2>
            <div class="admin-header-actions">
                <button class="btn" id="exportExcelBtn" title="Xuất danh sách USER ra Excel"><i class="fas fa-file-export"></i> Export</button>
                <button class="btn" id="importExcelBtn" title="Import từ Excel (chỉ import user)"><i class="fas fa-file-import"></i> Import</button>
                <input type="file" id="importFileInput" accept=".xlsx,.xls,.csv" style="display:none">
                <button class="btn" id="refreshUsersBtn" title="Làm mới"><i class="fas fa-sync-alt"></i></button>
                <button class="admin-close" id="adminClose"><i class="fas fa-times"></i></button>
            </div>
        </div>
        <div class="admin-body">
            <div class="admin-stats" id="adminStats"></div>
            <div class="admin-section-title">
                <span><i class="fas fa-users"></i> Danh sách tài khoản (<span id="adminUserCount">0</span>)</span>
                <button class="btn-add" id="showAddUserBtn"><i class="fas fa-plus"></i> Thêm</button>
            </div>
            <div class="add-user-form" id="addUserForm">
                <h3>Thêm tài khoản mới</h3>
                <div class="form-group">
                    <label>Email Google</label>
                    <input type="email" id="newUserEmail" placeholder="user@gmail.com">
                </div>
                <div class="form-group">
                    <label>Tên hiển thị</label>
                    <input type="text" id="newUserName" placeholder="Nguyễn Văn A">
                </div>
                <div class="form-group">
                    <label>Vai trò</label>
                    <select id="newUserRole">
                        <option value="user">User (chỉ học)</option>
                        <option value="admin">Admin (quản trị)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Hạn sử dụng (để trống = vĩnh viễn)</label>
                    <input type="date" id="newUserExpires">
                </div>
                <div class="form-actions">
                    <button class="btn" id="cancelAddUser">Hủy</button>
                    <button class="btn primary" id="confirmAddUser"><i class="fas fa-check"></i> Thêm</button>
                </div>
            </div>
            <div class="user-list" id="userList">
                <div class="no-data"><i class="fas fa-spinner fa-pulse"></i>Đang tải...</div>
            </div>

            <div class="admin-section-title" style="margin-top:1.5rem" id="renewalsTitle">
                <span><i class="fas fa-crown"></i> Yêu cầu gia hạn (<span id="pendingRenewalsBadge">0</span>)</span>
                <button class="btn" id="refreshRenewalsBtn" style="padding:.35rem .7rem;font-size:.75rem"><i class="fas fa-sync-alt"></i> Làm mới</button>
            </div>
            <div class="renewals-list" id="renewalsList">
                <div class="no-data" style="padding:1rem;font-size:.8rem"><i class="fas fa-spinner fa-pulse"></i> Đang tải...</div>
            </div>

            <div class="admin-section-title" style="margin-top:1.5rem" id="logsTitle">
                <span><i class="fas fa-history"></i> Lịch sử đăng nhập (gần đây)</span>
            </div>
            <div class="logs-list" id="logsList">
                <div class="no-data" style="padding:1rem;font-size:.8rem"><i class="fas fa-spinner fa-pulse"></i>Đang tải...</div>
            </div>
        </div>
    </div>
</div>
"""


def build_renewal_html():
    # Đã gộp vào build_accounts_html
    return ""


# ═══════════════════════════════════════════════════════════════
# JS
# ═══════════════════════════════════════════════════════════════
def build_accounts_js(config):
    """Trả về JS đã inject config từ dict JSON."""
    js = r"""
/* ============ CONFIG INJECTED ============ */
var TRIAL_DAYS = __TRIAL_DAYS__;
var BANK_CONFIG = __BANK_CONFIG__;
var PACKAGES = __PACKAGES__;
var RENEWAL_SUPPORT_ZALO = "__RENEWAL_SUPPORT_ZALO__";

/* ============ STATE ============ */
var currentUser = null;
var isDemo = true;
var auth, db;
var usersCache = [];
var lastLoginMap = {};
var importRows = [];
var editingEmail = null;
var editingExpiryEmail = null;
var appInitialized = false;
var renewalSelectedPkg = null;
var renewalCurrentReq = null;
var renewalListener = null;

/* ============ HELPERS ============ */
function escapeHtml(s) {
    if (s == null) return '';
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}
function escapeJs(s) {
    if (s == null) return '';
    return String(s).replace(/\\/g,'\\\\').replace(/'/g,"\\'").replace(/"/g,'\\"');
}
function isSuperAdmin() {
    if (!currentUser || currentUser.role !== 'admin') return false;
    var email = (currentUser.email || '').toLowerCase().trim();
    return email === SUPER_ADMIN.toLowerCase().trim();
}
function isHiddenAdmin() {
    if (!currentUser || currentUser.role !== 'admin') return false;
    return !isSuperAdmin();
}

/* ============ FIREBASE INIT ============ */
try {
    firebase.initializeApp(FIREBASE_CONFIG);
    auth = firebase.auth();
    db = firebase.firestore();
    auth.onAuthStateChanged(handleAuthChange);
} catch(e) {
    console.error('Firebase init error:', e);
    enterDemoMode();
}

/* ============ AUTH STATE ============ */
async function handleAuthChange(user) {
    if (!user) {
        currentUser = null; isDemo = true;
        applyUserUI(); enterDemoMode();
        return;
    }

    var email = (user.email || '').toLowerCase();
    var cacheKey = 'user_cache_' + email;
    var cached = null;
    try { cached = JSON.parse(localStorage.getItem(cacheKey) || 'null'); } catch(e) {}

    if (cached && cached.expires > Date.now() && cached.data) {
        currentUser = cached.data;
        isDemo = false;
        applyUserUI();
        logLogin(currentUser);
        if (!appInitialized) { initApp(); appInitialized = true; }
        else { if (typeof refreshApp === 'function') refreshApp(); }
        return;
    }

    try {
        var docRef = db.collection('allowed_users').doc(email);
        var doc = await docRef.get({ source: 'server' });

        /* ✅ TỰ ĐỘNG ĐĂNG KÝ: user mới → tặng trial */
        if (!doc.exists) {
            var registered = await grantTrialIfNew(user, null);
            if (registered) {
                /* Đọc lại từ server để lấy dữ liệu vừa tạo */
                doc = await docRef.get({ source: 'server' });
                setTimeout(function() {
                    var trialDays = (typeof TRIAL_DAYS === 'number' && TRIAL_DAYS > 0) ? TRIAL_DAYS : 7;
                    var trialDate = new Date(Date.now() + trialDays * 86400000);
                    alert('🎉 Chào mừng bạn!\n\n' +
                          '✅ Bạn được tặng MIỄN PHÍ ' + trialDays + ' ngày sử dụng.\n\n' +
                          '📅 Hạn dùng: ' + trialDate.toLocaleDateString('vi-VN') + '\n\n' +
                          'Chúc bạn học tốt! 🎓');
                }, 600);
            } else {
                await auth.signOut();
                showLoginError('Tài khoản <b>' + email + '</b> chưa được cấp quyền.');
                enterDemoMode();
                return;
            }
        }

        var data = doc.data() || {};
        var userData = {
            email: email,
            name: data.name || user.displayName || email.split('@')[0],
            role: data.role || 'user',
            photo: user.photoURL || '',
            expiresAt: data.expiresAt || null,
            isTrial: data.isTrial || false,
            isExpiredOnly: false   // ← flag mới
        };

        currentUser = userData;

        // ═══════════════════════════════════════════════
        // ✅ LOGIC MỚI: Kiểm tra user hết hạn
        // - Admin → luôn full quyền
        // - User còn hạn → full quyền
        // - User hết hạn → isDemo = true (giới hạn tính năng),
        //   NHƯNG vẫn giữ currentUser để hiện menu + nút gia hạn
        // ═══════════════════════════════════════════════
        var isExpiredUser = false;
        if (currentUser.role !== 'admin' && currentUser.expiresAt) {
            var expDate = getExpiryDate(currentUser.expiresAt);
            if (expDate && !isNaN(expDate.getTime())) {
                isExpiredUser = expDate.getTime() < Date.now();
            }
        }

        if (isExpiredUser) {
            isDemo = true;
            currentUser.isExpiredOnly = true;
            console.log('⏰ User hết hạn — chuyển sang chế độ demo (vẫn giữ menu user)');
        } else {
            isDemo = false;
            currentUser.isExpiredOnly = false;
        }

        // Cache lại (bao gồm flag isExpiredOnly)
        try {
            localStorage.setItem(cacheKey, JSON.stringify({
                data: currentUser,
                expires: Date.now() + 12 * 60 * 60 * 1000
            }));
        } catch(e) {}

        applyUserUI();
        logLogin(currentUser);
        if (!appInitialized) { initApp(); appInitialized = true; }
        else { if (typeof refreshApp === 'function') refreshApp(); }
    } catch(e) {
        console.error('Auth check error:', e);
        isDemo = true; enterDemoMode();
    }
}
function getDaysRemaining(userData) {
    if (!userData || !userData.expiresAt) return null;
    if (userData.role === 'admin') return null;
    var expDate = getExpiryDate(userData.expiresAt);
    if (!expDate) return null;
    return Math.ceil((expDate.getTime() - Date.now()) / (24 * 60 * 60 * 1000));
}

/* ============ TRIAL: TẶNG NGÀY DÙNG THỬ (ATOMIC) ============ */
/* 
 * ⚠️ QUAN TRỌNG: 
 * - Đã THÊM field `email` để khớp với rules mới
 * - Set TRỰC TIẾP (không dùng merge) → Firestore sẽ tính là CREATE rule
 * - Rules mới cho phép: email, name, role, expiresAt, isTrial, trialDays,
 *   registeredAt, trialStartedAt (không chặn các field này)
 */
async function grantTrialIfNew(user, userData) {
    if (!user || !user.email) return false;
    var email = user.email.toLowerCase();
    var userRef = db.collection('allowed_users').doc(email);

    try {
        var result = await db.runTransaction(async function(transaction) {
            var doc = await transaction.get(userRef);

            if (doc.exists) {
                var data = doc.data() || {};
                if (data.registeredAt || data.expiresAt || data.role === 'admin') {
                    return { granted: false, reason: 'already_exists' };
                }
            }

            var days = (typeof TRIAL_DAYS === 'number' && TRIAL_DAYS > 0) ? TRIAL_DAYS : 7;
            var expiresAt = new Date(Date.now() + days * 86400000);
            expiresAt.setHours(23, 59, 59, 0);

            /* ⚠️ Set đầy đủ field — rules mới cho phép hết */
            transaction.set(userRef, {
                email: email,                         // ← BẮT BUỘC cho rules
                name: (userData && userData.name) ? userData.name
                     : (user.displayName || email.split('@')[0]),
                role: 'user',
                expiresAt: firebase.firestore.Timestamp.fromDate(expiresAt),
                registeredAt: firebase.firestore.FieldValue.serverTimestamp(),
                isTrial: true,
                trialDays: days,
                trialStartedAt: firebase.firestore.FieldValue.serverTimestamp()
            });

            return { granted: true, expiresAt: expiresAt };
        });

        return result.granted;
    } catch (e) {
        console.error('❌ Grant trial error:', e);
        return false;
    }
}

function enterDemoMode() {
    // ═══════════════════════════════════════════════
    // ✅ KHÔNG reset currentUser nếu user đã login (chỉ hết hạn)
    // Chỉ reset khi thực sự là khách (chưa login)
    // ═══════════════════════════════════════════════
    if (!currentUser || !currentUser.isExpiredOnly) {
        // Trường hợp 1: Khách chưa login (currentUser = null) → OK, không cần làm gì
        // Trường hợp 2: User hết hạn (isExpiredOnly = true) → GIỮ NGUYÊN currentUser
        // Trường hợp 3: Logout → currentUser = null
    }

    isDemo = true;
    applyUserUI();

    if (!appInitialized) { initApp(); appInitialized = true; }
    else { if (typeof refreshApp === 'function') refreshApp(); }

    if ($('loadingScreen')) $('loadingScreen').classList.add('hidden');
    if ($('stickyTop')) $('stickyTop').style.display = 'block';
    if ($('fabGroup')) $('fabGroup').style.display = 'flex';
    if ($('mainContent')) $('mainContent').style.display = 'block';
}

/* ============ USER UI ============ */
function applyUserUI() {
    var demoBadge = $('demoBadge');
    var headerLoginBtn = $('headerLoginBtn');
    var userMenu = $('userMenu');

    /* Banner hết hạn */
    var expiryBanner = $('expiryBanner');
    if (expiryBanner) {
        if (!isDemo && currentUser && currentUser.role !== 'admin') {
            var daysLeft = getDaysRemaining(currentUser);
            if (daysLeft !== null && daysLeft <= 7) {
                expiryBanner.style.display = 'flex';
                var isExpired = daysLeft <= 0;
                expiryBanner.classList.toggle('urgent', isExpired || daysLeft <= 3);

                var iconWrap = expiryBanner.querySelector('.expiry-banner-icon');
                if (iconWrap) iconWrap.innerHTML = isExpired
                    ? '<i class="fas fa-exclamation-triangle"></i>'
                    : '<i class="fas fa-hourglass-half"></i>';

                var titleEl = expiryBanner.querySelector('.expiry-banner-text .title');
                if (titleEl) {
                    if (isExpired) titleEl.innerHTML = '❌ Tài khoản đã hết hạn!';
                    else titleEl.innerHTML = '⏳ Sắp hết hạn — còn ' + daysLeft + ' ngày';
                }

                var descEl = expiryBanner.querySelector('.expiry-banner-text .desc');
                if (descEl) {
                    var expDate = getExpiryDate(currentUser.expiresAt);
                    var expDateStr = expDate ? expDate.toLocaleDateString('vi-VN') : '';
                    if (isExpired) descEl.innerHTML = 'Đã hết hạn vào <b>' + expDateStr + '</b>. Gia hạn ngay!';
                    else descEl.innerHTML = 'Còn <b>' + daysLeft + ' ngày</b> (đến <b>' + expDateStr + '</b>).';
                }

                var contactBtn = $('expiryContactBtn');
                if (contactBtn) {
                    contactBtn.innerHTML = '<i class="fas fa-crown"></i> Gia hạn ngay';
                    contactBtn.href = '#';
                    contactBtn.onclick = function(e) { e.preventDefault(); openRenewalModal(); };
                }
            } else {
                expiryBanner.style.display = 'none';
            }
        } else if (currentUser && currentUser.isExpiredOnly) {
            // ✅ User hết hạn → vẫn hiển thị banner cảnh báo
            expiryBanner.style.display = 'flex';
            expiryBanner.classList.add('urgent');

            var iconWrap2 = expiryBanner.querySelector('.expiry-banner-icon');
            if (iconWrap2) iconWrap2.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';

            var titleEl2 = expiryBanner.querySelector('.expiry-banner-text .title');
            if (titleEl2) titleEl2.innerHTML = '❌ Tài khoản đã hết hạn!';

            var descEl2 = expiryBanner.querySelector('.expiry-banner-text .desc');
            if (descEl2) {
                var expDate2 = getExpiryDate(currentUser.expiresAt);
                var expDateStr2 = expDate2 ? expDate2.toLocaleDateString('vi-VN') : '';
                descEl2.innerHTML = 'Đã hết hạn vào <b>' + expDateStr2 + '</b>. Chỉ dùng được tính năng demo. Gia hạn ngay!';
            }

            var contactBtn2 = $('expiryContactBtn');
            if (contactBtn2) {
                contactBtn2.innerHTML = '<i class="fas fa-crown"></i> Gia hạn ngay';
                contactBtn2.href = '#';
                contactBtn2.onclick = function(e) { e.preventDefault(); openRenewalModal(); };
            }
        } else {
            expiryBanner.style.display = 'none';
        }
    }

    // ═══════════════════════════════════════════════
    // ✅ NÚT GIA HẠN TRONG DROPDOWN — có hiệu ứng urgent
    // ═══════════════════════════════════════════════
    var renewBtn = $('dropdownRenewBtn');
    if (renewBtn) {
        var showRenew = currentUser && currentUser.role !== 'admin';
        renewBtn.style.display = showRenew ? 'flex' : 'none';

        if (showRenew) {
            var rDaysLeft = getDaysRemaining(currentUser);
            var isUrgent = (rDaysLeft !== null && rDaysLeft <= 3);
            renewBtn.classList.toggle('urgent', isUrgent);

            var rBadge = renewBtn.querySelector('.renew-badge');
            if (rBadge) {
                if (rDaysLeft !== null && rDaysLeft <= 0) {
                    rBadge.textContent = 'HẾT HẠN';
                } else if (rDaysLeft !== null && rDaysLeft <= 3) {
                    rBadge.textContent = 'GẤP';
                } else {
                    rBadge.textContent = 'HOT';
                }
            }
        }
    }

    // ═══════════════════════════════════════════════
    // ✅ PHÂN BIỆT 3 TRẠNG THÁI
    // ═══════════════════════════════════════════════
    var isGuest = isDemo && !currentUser;
    var isExpiredUser = isDemo && currentUser && currentUser.isExpiredOnly;

    if (isGuest) {
        // Khách chưa login → ẩn menu user, hiện nút đăng nhập
        if (demoBadge) demoBadge.style.display = 'flex';
        if (headerLoginBtn) headerLoginBtn.style.display = 'flex';
        if (userMenu) userMenu.style.display = 'none';
        if ($('demoBanner')) $('demoBanner').style.display = 'flex';
        if ($('userDetails')) $('userDetails').style.display = 'none';
    } else {
        // ✅ Đã login (dù hết hạn hay còn hạn) → hiện menu user
        if (demoBadge) demoBadge.style.display = 'none';
        if (headerLoginBtn) headerLoginBtn.style.display = 'none';
        if (userMenu) userMenu.style.display = 'block';
        if ($('demoBanner')) $('demoBanner').style.display = 'none';

        if ($('userName')) $('userName').textContent = currentUser.name;
        if ($('userEmail')) $('userEmail').textContent = currentUser.email;
        if ($('userRole')) {
            $('userRole').textContent = currentUser.role;
            $('userRole').className = 'role' + (currentUser.role === 'admin' ? ' admin' : '');
        }
        if ($('openAdminBtn')) $('openAdminBtn').style.display = currentUser.role === 'admin' ? 'flex' : 'none';

        var avatar = $('userAvatar');
        if (avatar) {
            if (currentUser.photo) avatar.src = currentUser.photo;
            else {
                avatar.src = 'data:image/svg+xml;utf8,' + encodeURIComponent(
                    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">' +
                    '<rect fill="#2563eb" width="100" height="100"/>' +
                    '<text x="50" y="65" font-size="45" fill="#fff" text-anchor="middle" font-family="sans-serif" font-weight="bold">' +
                    (currentUser.name || '?').charAt(0).toUpperCase() + '</text></svg>'
                );
            }
        }
        updateUserDetails();
    }

    // ✅ Chip HSK/Subject bị giới hạn khi demo HOẶC user hết hạn
    var hskChip = $('hskChip');
    var subjectChip = $('subjectChip');
    if (hskChip && subjectChip) {
        var limited = isDemo;  // ← isDemo = true khi user hết hạn
        if (limited) { hskChip.classList.add('demo-limited'); subjectChip.classList.add('demo-limited'); }
        else { hskChip.classList.remove('demo-limited'); subjectChip.classList.remove('demo-limited'); }
    }

    var zaloBtn = $('zaloBtn');
    if (zaloBtn) {
        if (isDemo) zaloBtn.classList.remove('compact');
        else zaloBtn.classList.add('compact');
    }

    if (typeof updateDemoRemaining === 'function') updateDemoRemaining();

    var toggleFocusBtn = $('toggleFocusBtn');
    if (toggleFocusBtn) toggleFocusBtn.style.display = isDemo ? 'none' : 'flex';

    if (isDemo) document.body.classList.remove('hide-floating');
}
function updateUserDetails() {
    var detailsEl = $('userDetails');
    if (!detailsEl) return;
    if (isDemo || !currentUser) { detailsEl.style.display = 'none'; return; }
    detailsEl.style.display = 'flex';

    var expiryValue = $('expiryValue');
    var expirySub = $('expirySub');
    var expiryIcon = $('expiryIcon');
    var expiryIconWrap = $('expiryIconWrap');
    var progressWrap = $('expiryProgressWrap');
    var progressBar = $('expiryProgressBar');
    if (!expiryValue || !expirySub) return;

    if (currentUser.role === 'admin') {
        expiryValue.textContent = 'Vĩnh viễn';
        expiryValue.className = 'detail-value permanent';
        expirySub.textContent = 'Tài khoản quản trị viên';
        if (expiryIcon) expiryIcon.className = 'fas fa-infinity';
        if (expiryIconWrap) expiryIconWrap.className = 'detail-icon permanent';
        if (progressWrap) progressWrap.style.display = 'none';
        return;
    }

    if (!currentUser.expiresAt) {
        expiryValue.textContent = 'Vĩnh viễn';
        expiryValue.className = 'detail-value permanent';
        expirySub.textContent = 'Không giới hạn thời gian';
        if (expiryIcon) expiryIcon.className = 'fas fa-infinity';
        if (expiryIconWrap) expiryIconWrap.className = 'detail-icon permanent';
        if (progressWrap) progressWrap.style.display = 'none';
        return;
    }

    var expDate = getExpiryDate(currentUser.expiresAt);
    if (!expDate || isNaN(expDate.getTime())) { expiryValue.textContent = '-'; expirySub.textContent = ''; return; }

    var now = Date.now();
    var expTime = expDate.getTime();
    var daysLeft = Math.ceil((expTime - now) / (24 * 60 * 60 * 1000));
    var dateStr = expDate.toLocaleDateString('vi-VN');

    expiryValue.className = 'detail-value';
    if (expiryIconWrap) expiryIconWrap.className = 'detail-icon';

    if (daysLeft < 0) {
        expiryValue.textContent = 'Đã hết hạn';
        expiryValue.classList.add('expired');
        expirySub.innerHTML = 'Ngày hết hạn: <b>' + dateStr + '</b><br>Đã hết hạn ' + Math.abs(daysLeft) + ' ngày trước';
        if (expiryIcon) expiryIcon.className = 'fas fa-calendar-times';
        if (expiryIconWrap) expiryIconWrap.classList.add('expired');
        if (progressWrap) progressWrap.style.display = 'none';
    } else if (daysLeft <= 3) {
        expiryValue.textContent = 'Còn ' + daysLeft + ' ngày';
        expiryValue.classList.add('urgent');
        expirySub.innerHTML = 'Ngày hết hạn: <b>' + dateStr + '</b>';
        if (expiryIcon) expiryIcon.className = 'fas fa-exclamation-circle';
        if (expiryIconWrap) expiryIconWrap.classList.add('urgent');
        if (progressWrap) {
            progressWrap.style.display = 'block';
            progressBar.className = 'progress-bar urgent';
            progressBar.style.width = '90%';
        }
    } else if (daysLeft <= 7) {
        expiryValue.textContent = 'Còn ' + daysLeft + ' ngày';
        expiryValue.classList.add('warn');
        expirySub.innerHTML = 'Ngày hết hạn: <b>' + dateStr + '</b>';
        if (expiryIcon) expiryIcon.className = 'fas fa-clock';
        if (expiryIconWrap) expiryIconWrap.classList.add('warn');
        if (progressWrap) {
            progressWrap.style.display = 'block';
            progressBar.className = 'progress-bar warn';
            progressBar.style.width = '70%';
        }
    } else {
        expiryValue.textContent = 'Còn ' + daysLeft + ' ngày';
        expiryValue.classList.add('ok');
        expirySub.innerHTML = 'Ngày hết hạn: <b>' + dateStr + '</b>';
        if (expiryIcon) expiryIcon.className = 'fas fa-calendar-check';
        if (expiryIconWrap) expiryIconWrap.classList.add('ok');
        if (progressWrap) {
            progressWrap.style.display = 'block';
            progressBar.className = 'progress-bar ok';
            progressBar.style.width = '30%';
        }
    }
}

/* ============ LOGIN UI ============ */
window.showLoginModal = function() {
    $('loginModal').classList.add('show');
    $('loginError').classList.remove('show');
};
function hideLoginModal() { $('loginModal').classList.remove('show'); }
function showLoginError(msg) {
    var el = $('loginError');
    el.innerHTML = '<i class="fas fa-exclamation-triangle"></i> ' + msg;
    el.classList.add('show');
}

function logLogin(u) {
    try {
        var today = new Date().toDateString();
        var logKey = 'login_log_' + u.email;
        if (localStorage.getItem(logKey) === today) return;
        db.collection('login_logs').add({
            email: u.email, name: u.name, role: u.role,
            time: firebase.firestore.FieldValue.serverTimestamp(),
            userAgent: navigator.userAgent.substring(0, 100)
        }).then(function() { try { localStorage.setItem(logKey, today); } catch(e) {} }).catch(function(){});
    } catch(e) {}
}

/* ============ RENEWAL: MỞ MODAL ============ */
window.openRenewalModal = function() {
    if (!currentUser) { showLoginModal(); return; }
    if (currentUser.role === 'admin') { alert('Admin có hạn vĩnh viễn, không cần gia hạn!'); return; }
    renewalSelectedPkg = null;
    renewalCurrentReq = null;
    renderRenewalStep1();
    $('renewalModal').classList.add('show');
    if ($('userDropdown')) $('userDropdown').classList.remove('show');
};
window.closeRenewalModal = function() {
    $('renewalModal').classList.remove('show');
    if (renewalListener) { try { renewalListener(); } catch(e) {} renewalListener = null; }
};

function renderRenewalStep1() {
    var daysLeft = getDaysRemaining(currentUser);
    var isExpired = daysLeft !== null && daysLeft <= 0;
    var isWarn = daysLeft !== null && daysLeft > 0 && daysLeft <= 7;
    var currentCls = isExpired ? 'expired' : (isWarn ? 'warn' : '');
    var currentIcon = isExpired ? 'fa-exclamation-triangle' : (isWarn ? 'fa-hourglass-half' : 'fa-calendar-check');
    var currentTitle = isExpired ? 'Tài khoản đã hết hạn' : (isWarn ? 'Sắp hết hạn' : 'Tài khoản đang hoạt động');
    var currentDesc = '';
    if (daysLeft === null) currentDesc = 'Vĩnh viễn, không cần gia hạn';
    else if (isExpired) currentDesc = 'Đã hết hạn <b>' + Math.abs(daysLeft) + ' ngày</b> trước.';
    else currentDesc = 'Còn <b>' + daysLeft + ' ngày</b> sử dụng.';

    var packagesHtml = '';
    PACKAGES.forEach(function(p) {
        var saveHtml = p.save ? '<div class="pkg-save">' + escapeHtml(p.save) + '</div>' : '';
        var popularHtml = p.popular ? '<div class="pkg-popular">⭐ Phổ biến</div>' : '';
        packagesHtml +=
            '<div class="package-card" data-pkg="' + p.id + '" onclick="selectPackage(\'' + p.id + '\')">' +
                popularHtml + saveHtml +
                '<div class="pkg-label">' + escapeHtml(p.label) + '</div>' +
                '<div class="pkg-price">' + formatMoney(p.amount) + '</div>' +
                '<div class="pkg-unit">VNĐ</div>' +
            '</div>';
    });

    $('renewalBody').innerHTML =
        '<div class="renewal-current ' + currentCls + '">' +
            '<div class="rc-icon"><i class="fas ' + currentIcon + '"></i></div>' +
            '<div class="rc-info">' +
                '<div class="rc-title">' + currentTitle + '</div>' +
                '<div class="rc-desc">' + currentDesc + '</div>' +
            '</div>' +
        '</div>' +
        '<div class="renewal-section-title"><i class="fas fa-box"></i> Chọn gói gia hạn</div>' +
        '<div class="package-grid">' + packagesHtml + '</div>' +
        '<div class="renewal-actions">' +
            '<button class="renewal-btn" onclick="closeRenewalModal()">Hủy</button>' +
            '<button class="renewal-btn primary" id="renewalNextBtn" disabled onclick="goToPayment()">' +
                '<i class="fas fa-arrow-right"></i> Tiếp tục</button>' +
        '</div>';
}

window.selectPackage = function(pkgId) {
    renewalSelectedPkg = PACKAGES.find(function(p) { return p.id === pkgId; });
    document.querySelectorAll('.package-card').forEach(function(c) {
        c.classList.toggle('selected', c.dataset.pkg === pkgId);
    });
    var btn = $('renewalNextBtn');
    if (btn) btn.disabled = false;
};

async function goToPayment() {
    if (!renewalSelectedPkg) return;
    var transferCode = generateTransferCode();
    var amount = renewalSelectedPkg.amount;

    var btn = $('renewalNextBtn');
    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-pulse"></i> Đang tạo...'; }

    try {
        var reqRef = await db.collection('renewal_requests').add({
            email: currentUser.email,
            name: currentUser.name,
            package: renewalSelectedPkg.id,
            packageLabel: renewalSelectedPkg.label,
            amount: amount,
            days: renewalSelectedPkg.days,
            transferCode: transferCode,
            status: 'pending',
            method: 'manual',
            createdAt: firebase.firestore.FieldValue.serverTimestamp()
        });
        renewalCurrentReq = { id: reqRef.id, code: transferCode };
    } catch(e) {
        alert('❌ Lỗi tạo yêu cầu: ' + e.message);
        if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-arrow-right"></i> Tiếp tục'; }
        return;
    }
    renderPaymentScreen();
    listenRenewalRequest(renewalCurrentReq.id);
}

function renderPaymentScreen() {
    var pkg = renewalSelectedPkg;
    var code = renewalCurrentReq.code;
    var amount = pkg.amount;

    var qrUrl = 'https://img.vietqr.io/image/' + BANK_CONFIG.bank_id +
                '-' + BANK_CONFIG.account_no + '-compact2.png' +
                '?amount=' + amount +
                '&addInfo=' + encodeURIComponent(code) +
                '&accountName=' + encodeURIComponent(BANK_CONFIG.account_name);

    $('renewalBody').innerHTML =
        '<div class="renewal-current">' +
            '<div class="rc-icon"><i class="fas fa-shopping-cart"></i></div>' +
            '<div class="rc-info">' +
                '<div class="rc-title">Gói ' + escapeHtml(pkg.label) + '</div>' +
                '<div class="rc-desc">Số tiền: <b>' + formatMoney(amount) + ' VNĐ</b> · ' + pkg.days + ' ngày</div>' +
            '</div>' +
        '</div>' +
        '<div class="renewal-section-title"><i class="fas fa-qrcode"></i> Quét mã để thanh toán</div>' +
        '<div class="qr-wrap">' +
            '<img class="qr-img" src="' + qrUrl + '" alt="QR" onerror="this.style.display=\'none\'">' +
            '<div class="qr-hint">Mở app ngân hàng, quét QR để chuyển khoản. Hoặc chuyển thủ công theo thông tin bên dưới.</div>' +
        '</div>' +
        '<div class="bank-info">' +
            '<div class="bank-row"><span class="br-label">Ngân hàng</span><span class="br-value">' + escapeHtml(BANK_CONFIG.bank_name) + '</span></div>' +
            '<div class="bank-row"><span class="br-label">Số TK</span><span class="br-value">' + escapeHtml(BANK_CONFIG.account_no) +
                '<button class="copy-btn" onclick="copyText(\'' + escapeJs(BANK_CONFIG.account_no) + '\', this)"><i class="fas fa-copy"></i></button></span></div>' +
            '<div class="bank-row"><span class="br-label">Chủ TK</span><span class="br-value">' + escapeHtml(BANK_CONFIG.account_name) + '</span></div>' +
            '<div class="bank-row"><span class="br-label">Số tiền</span><span class="br-value code">' + formatMoney(amount) + 'đ</span></div>' +
            '<div class="bank-row"><span class="br-label">Nội dung</span><span class="br-value code">' + escapeHtml(code) +
                '<button class="copy-btn" onclick="copyText(\'' + escapeJs(code) + '\', this)"><i class="fas fa-copy"></i></button></span></div>' +
        '</div>' +
        '<div class="payment-steps">' +
            '<div class="step"><span class="num">1</span><div>Chuyển <b>' + formatMoney(amount) + ' VNĐ</b> đến STK trên</div></div>' +
            '<div class="step"><span class="num">2</span><div>Ghi đúng nội dung: <b>' + escapeHtml(code) + '</b></div></div>' +
            '<div class="step"><span class="num">3</span><div>Nhấn nút <b>"Tôi đã thanh toán"</b></div></div>' +
            '<div class="step"><span class="num">4</span><div>Chờ admin xác nhận trong <b>1-5 phút</b></div></div>' +
        '</div>' +
        '<div class="renewal-actions">' +
            '<button class="renewal-btn" onclick="cancelRenewal()"><i class="fas fa-times"></i> Hủy</button>' +
            '<button class="renewal-btn success" id="renewalConfirmBtn" onclick="userConfirmPaid()"><i class="fas fa-check"></i> Tôi đã thanh toán</button>' +
        '</div>';
}

window.copyText = function(text, btn) {
    var done = function() {
        btn.classList.add('copied');
        btn.innerHTML = '<i class="fas fa-check"></i>';
        setTimeout(function() { btn.classList.remove('copied'); btn.innerHTML = '<i class="fas fa-copy"></i>'; }, 1500);
    };
    if (navigator.clipboard) navigator.clipboard.writeText(text).then(done);
    else {
        var ta = document.createElement('textarea'); ta.value = text;
        document.body.appendChild(ta); ta.select(); document.execCommand('copy');
        document.body.removeChild(ta); done();
    }
};

window.userConfirmPaid = async function() {
    if (!renewalCurrentReq) return;
    var btn = $('renewalConfirmBtn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-pulse"></i> Đang gửi...';
    try {
        await db.collection('renewal_requests').doc(renewalCurrentReq.id).update({
            userConfirmedAt: firebase.firestore.FieldValue.serverTimestamp(),
            status: 'user_paid'
        });
        renderPendingConfirm();
    } catch(e) {
        alert('❌ Lỗi: ' + e.message);
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-check"></i> Tôi đã thanh toán';
    }
};

function renderPendingConfirm() {
    var zaloUrl = RENEWAL_SUPPORT_ZALO ? 'https://zalo.me/' + RENEWAL_SUPPORT_ZALO.replace(/\D/g, '') : '#';
    $('renewalBody').innerHTML =
        '<div class="renewal-success">' +
            '<div class="icon" style="background:linear-gradient(135deg,#f59e0b,#d97706);box-shadow:0 8px 24px rgba(245,158,11,.4)">' +
                '<i class="fas fa-hourglass-half"></i>' +
            '</div>' +
            '<h3>Đang chờ xác nhận</h3>' +
            '<p>Admin sẽ kiểm tra và xác nhận trong <b>1-5 phút</b>.</p>' +
            '<div class="info-box">' +
                '<i class="fas fa-info-circle" style="color:var(--primary)"></i>' +
                '<div>Nếu sau <b>10 phút</b> chưa được gia hạn, liên hệ Zalo kèm mã: <b>' + escapeHtml(renewalCurrentReq.code) + '</b></div>' +
            '</div>' +
            '<div style="display:flex;gap:.5rem;flex-wrap:wrap;justify-content:center;margin-top:.5rem">' +
                '<a class="renewal-btn" href="' + zaloUrl + '" target="_blank" rel="noopener"><i class="fas fa-comment-dots"></i> Liên hệ Zalo</a>' +
                '<button class="renewal-btn primary" onclick="closeRenewalModal()"><i class="fas fa-check"></i> Đóng</button>' +
            '</div>' +
        '</div>';
}

function listenRenewalRequest(reqId) {
    if (renewalListener) { try { renewalListener(); } catch(e) {} }
    renewalListener = db.collection('renewal_requests').doc(reqId).onSnapshot(function(doc) {
        if (!doc.exists) return;
        var data = doc.data();
        if (data.status === 'confirmed') {
            showRenewalSuccess(data);
            if (renewalListener) { try { renewalListener(); } catch(e) {} renewalListener = null; }
            refreshCurrentUser();
        }
    });
}

function showRenewalSuccess(data) {
    var newExpiry = '';
    if (data.newExpiresAt) {
        try {
            var d = data.newExpiresAt.toDate ? data.newExpiresAt.toDate() : new Date(data.newExpiresAt.seconds * 1000);
            newExpiry = d.toLocaleDateString('vi-VN');
        } catch(e) {}
    }
    $('renewalBody').innerHTML =
        '<div class="renewal-success">' +
            '<div class="icon"><i class="fas fa-check"></i></div>' +
            '<h3>🎉 Gia hạn thành công!</h3>' +
            '<p>Tài khoản đã được gia hạn thêm <b>' + data.days + ' ngày</b>.</p>' +
            (newExpiry ? '<div class="info-box"><i class="fas fa-calendar-check" style="color:var(--success)"></i><div>Hạn mới: <b>' + newExpiry + '</b></div></div>' : '') +
            '<button class="renewal-btn primary" onclick="closeRenewalModal();location.reload()" style="margin-top:.5rem"><i class="fas fa-check"></i> Hoàn tất</button>' +
        '</div>';
}

window.cancelRenewal = async function() {
    if (renewalCurrentReq) {
        try {
            await db.collection('renewal_requests').doc(renewalCurrentReq.id).update({
                status: 'cancelled',
                cancelledAt: firebase.firestore.FieldValue.serverTimestamp()
            });
        } catch(e) {}
    }
    closeRenewalModal();
};

function generateTransferCode() {
    var rand = Math.random().toString(36).substring(2, 6).toUpperCase();
    var ts = Date.now().toString(36).slice(-4).toUpperCase();
    return 'HN' + ts + rand;
}
function formatMoney(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, '.'); }

async function refreshCurrentUser() {
    if (!currentUser) return;
    try {
        var doc = await db.collection('allowed_users').doc(currentUser.email).get({ source: 'server' });
        if (!doc.exists) return;
        var data = doc.data();
        currentUser.expiresAt = data.expiresAt || null;
        currentUser.name = data.name || currentUser.name;

        // ✅ Cập nhật lại isDemo khi user vừa được gia hạn
        if (currentUser.role !== 'admin' && currentUser.expiresAt) {
            var expDate = getExpiryDate(currentUser.expiresAt);
            if (expDate && !isNaN(expDate.getTime())) {
                var isExpired = expDate.getTime() < Date.now();
                currentUser.isExpiredOnly = isExpired;
                isDemo = isExpired;
                console.log('🔄 refreshCurrentUser: hết hạn =', isExpired);
            }
        } else if (currentUser.role === 'admin' || !currentUser.expiresAt) {
            currentUser.isExpiredOnly = false;
            isDemo = false;
        }

        try { localStorage.removeItem('user_cache_' + currentUser.email); } catch(e) {}
        try {
            localStorage.setItem('user_cache_' + currentUser.email, JSON.stringify({
                data: currentUser, expires: Date.now() + 12 * 60 * 60 * 1000
            }));
        } catch(e) {}

        if (typeof applyUserUI === 'function') applyUserUI();
    } catch(e) { console.error('refreshCurrentUser error:', e); }
}
/* ============ ADMIN PANEL ============ */
function initAdminPanel() {
    if ($('openAdminBtn')) $('openAdminBtn').addEventListener('click', function() {
        $('userDropdown').classList.remove('show');
        openAdminPanel();
    });
    if ($('adminClose')) $('adminClose').addEventListener('click', function() { $('adminModal').classList.remove('show'); });
    if ($('adminModal')) $('adminModal').addEventListener('click', function(e) { if (e.target === this) $('adminModal').classList.remove('show'); });
    if ($('refreshUsersBtn')) $('refreshUsersBtn').addEventListener('click', function() {
        try { localStorage.removeItem('admin_users_cache'); } catch(e) {}
        loadUsers(true);
    });
    if ($('exportExcelBtn')) $('exportExcelBtn').addEventListener('click', doExportExcel);
    if ($('importExcelBtn')) $('importExcelBtn').addEventListener('click', function() { $('importFileInput').click(); });
    if ($('importFileInput')) $('importFileInput').addEventListener('change', handleImportFileSelect);
    if ($('importClose')) $('importClose').addEventListener('click', function() { $('importModal').classList.remove('show'); importRows = []; });
    if ($('importCancelBtn')) $('importCancelBtn').addEventListener('click', function() { $('importModal').classList.remove('show'); importRows = []; });
    if ($('importModal')) $('importModal').addEventListener('click', function(e) { if (e.target === this) { $('importModal').classList.remove('show'); importRows = []; } });
    if ($('importConfirmBtn')) $('importConfirmBtn').addEventListener('click', doImport);
    if ($('showAddUserBtn')) $('showAddUserBtn').addEventListener('click', function() {
        $('addUserForm').classList.toggle('show');
        if ($('addUserForm').classList.contains('show')) $('newUserEmail').focus();
    });
    if ($('cancelAddUser')) $('cancelAddUser').addEventListener('click', function() {
        $('addUserForm').classList.remove('show');
        $('newUserEmail').value = ''; $('newUserName').value = '';
        $('newUserRole').value = 'user'; $('newUserExpires').value = '';
    });
    if ($('confirmAddUser')) $('confirmAddUser').addEventListener('click', doAddUser);
    if ($('refreshRenewalsBtn')) $('refreshRenewalsBtn').addEventListener('click', function() { loadRenewals(); });
}

async function doAddUser() {
    var email = $('newUserEmail').value.trim().toLowerCase();
    var name = $('newUserName').value.trim();
    var role = $('newUserRole').value;
    var expiresVal = $('newUserExpires').value;

    if (!email || !email.includes('@')) { alert('Email không hợp lệ'); return; }
    if (!name) name = email.split('@')[0];
    if (role === 'admin' && !isSuperAdmin()) { alert('⚠️ Chỉ Super Admin mới có quyền thêm admin!'); return; }

    try {
        var docRef = db.collection('allowed_users').doc(email);
        var doc = await docRef.get();
        if (doc.exists) { alert('Email này đã tồn tại!'); return; }

        var setData = {
            email: email,                              // ← thêm cho nhất quán
            name: name, role: role,
            addedAt: firebase.firestore.FieldValue.serverTimestamp(),
            addedBy: currentUser.email
        };
        if (expiresVal && role !== 'admin') {
            var d = new Date(expiresVal + 'T23:59:59');
            if (!isNaN(d.getTime())) setData.expiresAt = firebase.firestore.Timestamp.fromDate(d);
        }
        await docRef.set(setData);
        $('addUserForm').classList.remove('show');
        $('newUserEmail').value = ''; $('newUserName').value = '';
        $('newUserRole').value = 'user'; $('newUserExpires').value = '';
        try { localStorage.removeItem('admin_users_cache'); } catch(e) {}
        loadUsers(true);
    } catch(e) { alert('Lỗi: ' + e.message); }
}

function openAdminPanel() {
    if (!currentUser || currentUser.role !== 'admin') return;
    $('adminModal').classList.add('show');
    loadUsers(false);
    loadLogs();
    loadRenewals();
}

function loadUsers(forceRefresh) {
    var cacheKey = 'admin_users_cache';
    if (forceRefresh) { try { localStorage.removeItem(cacheKey); } catch(e) {} }

    if (!forceRefresh) {
        try {
            var cached = JSON.parse(localStorage.getItem(cacheKey) || 'null');
            if (cached && cached.expires > Date.now() && cached.data && Array.isArray(cached.data)) {
                usersCache = cached.data;
                renderUsers(usersCache);
                renderAdminStats();
                loadLastLoginMap();
                return;
            }
        } catch(e) { try { localStorage.removeItem(cacheKey); } catch(e2) {} }
    }

    $('userList').innerHTML = '<div class="no-data"><i class="fas fa-spinner fa-pulse"></i>Đang tải...</div>';
    db.collection('allowed_users').get().then(function(snapshot) {
        usersCache = [];
        snapshot.forEach(function(doc) {
            var data = doc.data() || {};
            usersCache.push({
                email: doc.id,
                name: data.name || '',
                role: data.role || 'user',
                expiresAt: data.expiresAt || null
            });
        });
        usersCache.sort(function(a, b) { return (a.email || '').localeCompare(b.email || ''); });
        try {
            localStorage.setItem(cacheKey, JSON.stringify({ data: usersCache, expires: Date.now() + 5 * 60 * 1000 }));
        } catch(e) {}
        renderUsers(usersCache);
        renderAdminStats();
        return loadLastLoginMap();
    }).catch(function(err) {
        $('userList').innerHTML = '<div class="no-data" style="color:#dc2626;padding:1rem"><i class="fas fa-exclamation-triangle"></i>Lỗi: ' + err.message + '</div>';
    });
}

function loadLastLoginMap() {
    var hidden = isHiddenAdmin();
    var myEmail = (currentUser && currentUser.email ? currentUser.email.toLowerCase() : '');
    return db.collection('login_logs').orderBy('time', 'desc').limit(500).get().then(function(snapshot) {
        lastLoginMap = {};
        snapshot.forEach(function(doc) {
            var d = doc.data();
            var email = (d.email || '').toLowerCase();
            if (hidden && d.role === 'admin' && email !== myEmail) return;
            if (!lastLoginMap[email] && d.time) lastLoginMap[email] = d.time.toDate();
        });
        renderUsers(usersCache);
    }).catch(function() {});
}

function renderAdminStats() {
    var hidden = isHiddenAdmin();
    var usersOnly = usersCache.filter(function(u) { return u.role !== 'admin'; });
    var users = usersOnly.length;
    var admins = usersCache.length - users;
    var now = Date.now();
    var day1 = 24 * 60 * 60 * 1000;
    var day7 = 7 * 24 * 60 * 60 * 1000;
    var active = 0, online = 0, never = 0, expired = 0, expiring = 0;

    usersOnly.forEach(function(u) {
        var last = lastLoginMap[(u.email || '').toLowerCase()];
        if (last) {
            var diff = now - last.getTime();
            if (diff <= day7) active++;
            if (diff <= day1) online++;
        } else never++;
        if (u.expiresAt) {
            var d = getExpiryDate(u.expiresAt);
            if (d && !isNaN(d.getTime())) {
                var daysLeft = Math.ceil((d.getTime() - now) / (24 * 60 * 60 * 1000));
                if (daysLeft < 0) expired++;
                else if (daysLeft <= 7) expiring++;
            }
        }
    });

    if (hidden) {
        $('adminStats').innerHTML =
            '<div class="stat-card"><div class="num">' + users + '</div><div class="label">Tổng User</div></div>' +
            '<div class="stat-card"><div class="num" style="color:#16a34a">' + online + '</div><div class="label">Đang hoạt động</div></div>' +
            '<div class="stat-card"><div class="num" style="color:#f59e0b">' + expiring + '</div><div class="label">Sắp hết hạn</div></div>' +
            '<div class="stat-card"><div class="num" style="color:#dc2626">' + expired + '</div><div class="label">Hết hạn</div></div>';
    } else {
        $('adminStats').innerHTML =
            '<div class="stat-card"><div class="num">' + users + '</div><div class="label">Tổng User</div></div>' +
            '<div class="stat-card"><div class="num" style="color:#16a34a">' + online + '</div><div class="label">Đang hoạt động</div></div>' +
            '<div class="stat-card"><div class="num" style="color:#3b82f6">' + active + '</div><div class="label">Active 7d</div></div>' +
            '<div class="stat-card"><div class="num" style="color:#f59e0b">' + admins + '</div><div class="label">Admin</div></div>' +
            '<div class="stat-card"><div class="num" style="color:#94a3b8">' + never + '</div><div class="label">Chưa login</div></div>' +
            '<div class="stat-card"><div class="num" style="color:#f59e0b">' + expiring + '</div><div class="label">Sắp hết hạn</div></div>' +
            '<div class="stat-card"><div class="num" style="color:#dc2626">' + expired + '</div><div class="label">Hết hạn</div></div>';
    }
    $('adminUserCount').textContent = users;
}

function renderUsers(items) {
    var list = $('userList');
    var hidden = isHiddenAdmin();
    var superAdmin = isSuperAdmin();
    var myEmail = (currentUser && currentUser.email ? currentUser.email.toLowerCase() : '');

    var displayItems = items;
    if (hidden) {
        displayItems = items.filter(function(u) {
            var uEmail = (u.email || '').toLowerCase();
            if (u.role === 'admin' && uEmail !== myEmail) return false;
            return true;
        });
    }
    if (!displayItems.length) {
        list.innerHTML = '<div class="no-data" style="padding:1.5rem;font-size:.85rem"><i class="fas fa-search"></i>Không có user nào</div>';
        return;
    }

    var now = Date.now();
    var day7 = 7 * 24 * 60 * 60 * 1000;
    var day30 = 30 * 24 * 60 * 60 * 1000;

    list.innerHTML = displayItems.map(function(u) {
        var isMe = u.email === currentUser.email;
        var isAdmin = u.role === 'admin';
        var targetIsSuper = (u.email || '').toLowerCase() === SUPER_ADMIN.toLowerCase();
        var canModifyAdmin = superAdmin && isAdmin && !isMe && !targetIsSuper;

        var roleBtn = isAdmin
            ? (canModifyAdmin
                ? '<button class="u-btn" onclick="changeRole(\'' + escapeJs(u.email) + '\', \'user\')" title="Hạ xuống User"><i class="fas fa-user"></i></button>'
                : '<button class="u-btn" disabled title="Không thể hạ quyền"><i class="fas fa-user"></i></button>')
            : (superAdmin
                ? '<button class="u-btn" onclick="changeRole(\'' + escapeJs(u.email) + '\', \'admin\')" title="Nâng lên Admin"><i class="fas fa-shield-alt"></i></button>'
                : '<button class="u-btn" disabled title="Chỉ Super Admin"><i class="fas fa-shield-alt"></i></button>');

        var deleteBtn = isMe
            ? '<button class="u-btn danger" disabled title="Không thể tự xóa"><i class="fas fa-trash"></i></button>'
            : (targetIsSuper
                ? '<button class="u-btn danger" disabled title="Không thể xóa Super Admin"><i class="fas fa-trash"></i></button>'
                : (isAdmin && !canModifyAdmin
                    ? '<button class="u-btn danger" disabled title="Chỉ Super Admin"><i class="fas fa-trash"></i></button>'
                    : '<button class="u-btn danger" onclick="deleteUser(\'' + escapeJs(u.email) + '\')" title="Xóa"><i class="fas fa-trash"></i></button>'));

        var expiryBtn = '';
        if (!isAdmin) {
            var btnCls = 'u-btn expiry';
            var tooltip = 'Chỉnh hạn sử dụng';
            if (u.expiresAt) {
                var d = getExpiryDate(u.expiresAt);
                if (d && !isNaN(d.getTime())) {
                    var daysLeftExp = Math.ceil((d.getTime() - Date.now()) / (24 * 60 * 60 * 1000));
                    tooltip = 'Chỉnh hạn (còn ' + Math.max(0, daysLeftExp) + ' ngày)';
                    if (daysLeftExp <= 7) btnCls += ' urgent';
                }
            } else tooltip = 'Chỉnh hạn (Vĩnh viễn)';
            expiryBtn = '<button class="' + btnCls + '" onclick="openEditExpiry(\'' + escapeJs(u.email) + '\')" title="' + escapeHtml(tooltip) + '"><i class="fas fa-calendar-alt"></i></button>';
        }

        var last = lastLoginMap[(u.email || '').toLowerCase()];
        var lastLoginHtml = last
            ? '<div class="u-last-login ' + ((now - last.getTime()) <= day7 ? 'active' : ((now - last.getTime()) <= day30 ? 'recent' : '')) + '"><i class="fas fa-clock"></i> ' + formatTimeDiff(now - last.getTime()) + '</div>'
            : '<div class="u-last-login"><i class="fas fa-times-circle"></i> Chưa đăng nhập</div>';

        var expiryHtml = '';
        if (isAdmin) expiryHtml = '<div class="u-expiry permanent"><i class="fas fa-infinity"></i> Vĩnh viễn</div>';
        else if (!u.expiresAt) expiryHtml = '<div class="u-expiry permanent" onclick="openEditExpiry(\'' + escapeJs(u.email) + '\')"><i class="fas fa-infinity"></i> Vĩnh viễn</div>';
        else {
            var expDate = getExpiryDate(u.expiresAt);
            if (expDate && !isNaN(expDate.getTime())) {
                var daysLeft = Math.ceil((expDate.getTime() - now) / (24 * 60 * 60 * 1000));
                var expCls = 'ok', expIcon = 'fa-calendar-check', expText = 'Còn ' + daysLeft + ' ngày';
                if (daysLeft < 0) { expCls = 'expired'; expIcon = 'fa-calendar-times'; expText = 'Hết hạn ' + Math.abs(daysLeft) + ' ngày'; }
                else if (daysLeft === 0) { expCls = 'urgent'; expIcon = 'fa-exclamation-circle'; expText = 'Hết hạn hôm nay'; }
                else if (daysLeft <= 3) { expCls = 'urgent'; expIcon = 'fa-exclamation-circle'; }
                else if (daysLeft <= 7) { expCls = 'warn'; expIcon = 'fa-clock'; }
                expiryHtml = '<div class="u-expiry ' + expCls + '" onclick="openEditExpiry(\'' + escapeJs(u.email) + '\')"><i class="fas ' + expIcon + '"></i> ' + expText + ' • ' + expDate.toLocaleDateString('vi-VN') + '</div>';
            }
        }

        var roleBadge = isAdmin
            ? '<span class="u-role ' + (targetIsSuper ? 'super' : 'admin') + '">' + (targetIsSuper ? '👑 super' : 'admin') + '</span>'
            : '<span class="u-role user">user</span>';

        return '<div class="user-row" data-email="' + escapeHtml(u.email) + '">' +
            '<div class="u-info">' +
                '<div class="u-name">' + escapeHtml(u.name || u.email.split('@')[0]) + (isMe ? ' <span style="color:#94a3b8;font-size:.7rem">(bạn)</span>' : '') + '</div>' +
                '<div class="u-email">' + escapeHtml(u.email) + '</div>' +
                lastLoginHtml + expiryHtml +
            '</div>' + roleBadge +
            '<div class="u-actions">' + expiryBtn + roleBtn + deleteBtn + '</div>' +
        '</div>';
    }).join('');
}

window.changeRole = async function(email, newRole) {
    var target = usersCache.find(function(u) { return u.email === email; });
    if (!target) return alert('Không tìm thấy user!');
    var isMe = email === currentUser.email;
    var isAdmin = target.role === 'admin';
    var superAdmin = isSuperAdmin();
    var targetIsSuper = (email || '').toLowerCase() === SUPER_ADMIN.toLowerCase();
    if (isMe && newRole === 'user') return alert('⚠️ Không thể tự hạ quyền!');
    if (targetIsSuper) return alert('⚠️ Không thể thay đổi Super Admin!');
    if (isAdmin && newRole === 'user' && !superAdmin) return alert('⚠️ Chỉ Super Admin!');
    if (!isAdmin && newRole === 'admin' && !superAdmin) return alert('⚠️ Chỉ Super Admin!');
    var action = newRole === 'admin' ? 'NÂNG LÊN ADMIN' : 'HẠ XUỐNG USER';
    if (!confirm(action + ' cho:\n\n' + email + ' ?')) return;
    try {
        await db.collection('allowed_users').doc(email).update({ role: newRole });
        try { localStorage.removeItem('user_cache_' + email); } catch(e) {}
        try { localStorage.removeItem('admin_users_cache'); } catch(e) {}
        loadUsers(true);
    } catch(e) { alert('Lỗi: ' + e.message); }
};

window.deleteUser = async function(email) {
    var target = usersCache.find(function(u) { return u.email === email; });
    if (!target) return alert('Không tìm thấy user!');
    var isMe = email === currentUser.email;
    var isAdmin = target.role === 'admin';
    var superAdmin = isSuperAdmin();
    var targetIsSuper = (email || '').toLowerCase() === SUPER_ADMIN.toLowerCase();
    if (isMe) return alert('⚠️ Không thể tự xóa!');
    if (targetIsSuper) return alert('⚠️ Không thể xóa Super Admin!');
    if (isAdmin && !superAdmin) return alert('⚠️ Chỉ Super Admin!');
    if (!confirm('⚠️ XÓA\n\n' + email + '\n\nNgười này sẽ không đăng nhập được nữa.\n\nTiếp tục?')) return;
    try {
        await db.collection('allowed_users').doc(email).delete();
        try { localStorage.removeItem('user_cache_' + email); } catch(e) {}
        try { localStorage.removeItem('admin_users_cache'); } catch(e) {}
        loadUsers(true);
    } catch(e) { alert('Lỗi: ' + e.message); }
};

function loadLogs() {
    if (isHiddenAdmin()) {
        if ($('logsTitle')) $('logsTitle').style.display = 'none';
        $('logsList').style.display = 'none';
        return;
    }
    if ($('logsTitle')) $('logsTitle').style.display = 'flex';
    $('logsList').style.display = 'block';
    db.collection('login_logs').orderBy('time', 'desc').limit(30).get().then(function(snapshot) {
        if (snapshot.empty) {
            $('logsList').innerHTML = '<div class="no-data" style="padding:1rem;font-size:.8rem">Chưa có log</div>';
            return;
        }
        var html = '';
        snapshot.forEach(function(doc) {
            var d = doc.data();
            var time = d.time ? new Date(d.time.toDate()).toLocaleString('vi-VN') : 'N/A';
            html += '<div class="log-item"><span class="log-time">' + time + '</span><span class="log-msg"><b>' + escapeHtml(d.name || d.email) + '</b> (' + escapeHtml(d.role || 'user') + ')</span></div>';
        });
        $('logsList').innerHTML = html;
    }).catch(function(err) {
        $('logsList').innerHTML = '<div class="no-data" style="padding:1rem;font-size:.8rem;color:#dc2626">Lỗi: ' + err.message + '</div>';
    });
}

/* ============ ADMIN: DUYỆT YÊU CẦU GIA HẠN ============ */
function loadRenewals() {
    if (isHiddenAdmin()) {
        if ($('renewalsTitle')) $('renewalsTitle').style.display = 'none';
        if ($('renewalsList')) $('renewalsList').style.display = 'none';
        return;
    }
    if ($('renewalsTitle')) $('renewalsTitle').style.display = 'flex';
    var listEl = $('renewalsList');
    if (!listEl) return;
    listEl.style.display = 'block';

    db.collection('renewal_requests').orderBy('createdAt', 'desc').limit(100).get().then(function(snapshot) {
        var items = [];
        snapshot.forEach(function(doc) {
            var d = doc.data();
            if (d.status === 'pending' || d.status === 'user_paid') items.push(Object.assign({ _id: doc.id }, d));
        });
        var badge = $('pendingRenewalsBadge');
        if (badge) badge.textContent = items.length;

        if (items.length === 0) {
            listEl.innerHTML = '<div class="no-data" style="padding:1rem;font-size:.8rem">Không có yêu cầu nào</div>';
            return;
        }
        var html = '';
        items.forEach(function(d) {
            var created = d.createdAt ? d.createdAt.toDate() : new Date();
            var timeStr = formatTimeDiff(Date.now() - created.getTime());
            var statusCls = d.status === 'user_paid' ? 'user_paid' : 'pending';
            var statusText = d.status === 'user_paid' ? '⏳ Chờ xác nhận' : '⏱ Chờ CK';
            html +=
                '<div class="renewal-admin-row">' +
                    '<div class="rar-head">' +
                        '<div>' +
                            '<div class="rar-email">' + escapeHtml(d.name || d.email) + '</div>' +
                            '<div class="u-email">' + escapeHtml(d.email) + '</div>' +
                            '<div class="rar-sub"><i class="fas fa-clock"></i> ' + timeStr + '</div>' +
                        '</div>' +
                        '<div class="rar-pkg">' +
                            '<div class="rar-amount">' + formatMoney(d.amount) + 'đ</div>' +
                            '<div class="rar-pkg-label">' + escapeHtml(d.packageLabel || d.package) + ' · ' + d.days + ' ngày</div>' +
                        '</div>' +
                    '</div>' +
                    '<div class="rar-foot">' +
                        '<div>Mã: <span class="rar-code">' + escapeHtml(d.transferCode) + '</span></div>' +
                        '<div class="rar-actions">' +
                            '<span class="rar-status ' + statusCls + '">' + statusText + '</span>' +
                            '<button class="btn primary" style="padding:.4rem .75rem;font-size:.75rem" onclick="approveRenewal(\'' + escapeJs(d._id) + '\')"><i class="fas fa-check"></i> Xác nhận</button>' +
                            '<button class="btn" style="padding:.4rem .65rem;font-size:.75rem" onclick="rejectRenewal(\'' + escapeJs(d._id) + '\')"><i class="fas fa-times"></i></button>' +
                        '</div>' +
                    '</div>' +
                '</div>';
        });
        listEl.innerHTML = html;
    }).catch(function(err) {
        listEl.innerHTML = '<div class="no-data" style="padding:1rem;font-size:.8rem;color:#dc2626">Lỗi: ' + err.message + '</div>';
    });
}

window.approveRenewal = async function(reqId) {
    if (!confirm('Xác nhận đã nhận tiền và gia hạn?')) return;
    try {
        var reqDoc = await db.collection('renewal_requests').doc(reqId).get();
        if (!reqDoc.exists) return alert('Không tìm thấy yêu cầu!');
        var req = reqDoc.data();

        var userDoc = await db.collection('allowed_users').doc(req.email).get();
        var currentExpiry = null;
        if (userDoc.exists) {
            var ud = userDoc.data();
            if (ud.expiresAt) currentExpiry = getExpiryDate(ud.expiresAt);
        }
        var now = new Date();
        var baseDate = (currentExpiry && currentExpiry > now) ? currentExpiry : now;
        var newExpiry = new Date(baseDate.getTime() + req.days * 24 * 60 * 60 * 1000);

        await db.collection('allowed_users').doc(req.email).update({
            expiresAt: firebase.firestore.Timestamp.fromDate(newExpiry),
            isTrial: false,
            lastRenewalAt: firebase.firestore.FieldValue.serverTimestamp()
        });
        await db.collection('renewal_requests').doc(reqId).update({
            status: 'confirmed',
            confirmedAt: firebase.firestore.FieldValue.serverTimestamp(),
            confirmedBy: currentUser.email,
            newExpiresAt: firebase.firestore.Timestamp.fromDate(newExpiry)
        });
        try { localStorage.removeItem('user_cache_' + req.email); } catch(e) {}
        alert('✅ Đã gia hạn ' + req.days + ' ngày cho ' + req.email + '\nHạn mới: ' + newExpiry.toLocaleDateString('vi-VN'));
        loadRenewals();
        loadUsers(true);
    } catch(e) { alert('❌ Lỗi: ' + e.message); }
};

window.rejectRenewal = async function(reqId) {
    var reason = prompt('Lý do từ chối (tùy chọn):', '');
    if (reason === null) return;
    try {
        await db.collection('renewal_requests').doc(reqId).update({
            status: 'rejected',
            rejectedAt: firebase.firestore.FieldValue.serverTimestamp(),
            rejectedBy: currentUser.email,
            rejectReason: reason || ''
        });
        loadRenewals();
    } catch(e) { alert('❌ Lỗi: ' + e.message); }
};

/* ============ EXPIRY EDIT ============ */
window.openEditExpiry = function(email) {
    var user = usersCache.find(function(u) { return u.email === email; });
    if (!user) return alert('Không tìm thấy user!');
    if (user.role === 'admin') return alert('Admin có hạn vĩnh viễn!');
    editingExpiryEmail = email;
    $('editExpiryName').textContent = user.name || email.split('@')[0];
    $('editExpiryEmail').textContent = email;
    if (user.expiresAt) {
        var d = getExpiryDate(user.expiresAt);
        $('editExpiryInput').value = (d && !isNaN(d.getTime())) ? formatDate(d) : '';
    } else $('editExpiryInput').value = '';
    $('editExpiryModal').classList.add('show');
};
window.setQuickExpiry = function(days) {
    var d = new Date();
    d.setDate(d.getDate() + days);
    d.setHours(23, 59, 59);
    $('editExpiryInput').value = formatDate(d);
};
window.setQuickExpiryPermanent = function() { $('editExpiryInput').value = ''; };

async function doUpdateExpiry() {
    if (!editingExpiryEmail) return;
    var dateVal = $('editExpiryInput').value;
    var updateData = {};
    if (dateVal) {
        var d = new Date(dateVal + 'T23:59:59');
        if (isNaN(d.getTime())) return alert('Ngày không hợp lệ!');
        updateData.expiresAt = firebase.firestore.Timestamp.fromDate(d);
    } else updateData.expiresAt = null;

    var btn = $('editExpiryConfirm');
    btn.disabled = true;
    var originalHtml = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-pulse"></i> Đang lưu...';
    try {
        await db.collection('allowed_users').doc(editingExpiryEmail).update(updateData);
        try { localStorage.removeItem('user_cache_' + editingExpiryEmail); } catch(e) {}
        try { localStorage.removeItem('admin_users_cache'); } catch(e) {}
        $('editExpiryModal').classList.remove('show');
        alert(dateVal ? '✅ Đã cập nhật hạn đến ' + new Date(dateVal).toLocaleDateString('vi-VN') : '✅ Đã đặt thành vĩnh viễn');
        loadUsers(true);
    } catch(err) { alert('❌ Lỗi: ' + err.message); }
    finally { btn.disabled = false; btn.innerHTML = originalHtml; }
}

async function doChangeName() {
    if (!editingEmail) return;
    var newName = $('changeNameInput').value.trim();
    if (!newName) return alert('Tên không được để trống!');
    if (newName.length > 50) return alert('Tên quá dài!');
    var btn = $('changeNameConfirm');
    btn.disabled = true;
    var originalHtml = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-pulse"></i> Đang lưu...';
    try {
        await db.collection('allowed_users').doc(editingEmail).update({ name: newName });
        try { localStorage.removeItem('user_cache_' + editingEmail); } catch(e) {}
        try { localStorage.removeItem('admin_users_cache'); } catch(e) {}
        if (currentUser && currentUser.email === editingEmail) {
            currentUser.name = newName;
            $('userName').textContent = newName;
        }
        $('changeNameModal').classList.remove('show');
        alert('✅ Đã đổi tên!');
        if ($('adminModal').classList.contains('show')) loadUsers(true);
    } catch(err) { alert('❌ Lỗi: ' + err.message); }
    finally { btn.disabled = false; btn.innerHTML = originalHtml; }
}

/* ============ EXPORT EXCEL ============ */
function doExportExcel() {
    var usersOnly = usersCache.filter(function(u) { return u.role !== 'admin'; });
    if (!usersOnly.length) return alert('Không có user nào để export!');

    try {
        var wb = XLSX.utils.book_new();
        var now = Date.now();
        var COLUMNS = [
            { header: 'STT', width: 6 }, { header: 'email', width: 35 },
            { header: 'name', width: 25 }, { header: 'expiresAt', width: 14 },
            { header: 'Trạng thái', width: 22 }
        ];
        var aoa = [COLUMNS.map(function(c) { return c.header; })];

        usersOnly.forEach(function(u) {
            var expDate = getExpiryDate(u.expiresAt);
            var expStr = '', statusStr = '';
            if (!expDate) { statusStr = '∞ Vĩnh viễn'; }
            else {
                expStr = formatDate(expDate);
                var daysLeft = Math.ceil((expDate.getTime() - now) / (24 * 60 * 60 * 1000));
                if (daysLeft < 0) statusStr = '❌ Hết hạn ' + Math.abs(daysLeft) + ' ngày';
                else if (daysLeft <= 3) statusStr = '🔴 Còn ' + daysLeft + ' ngày';
                else if (daysLeft <= 7) statusStr = '🟡 Còn ' + daysLeft + ' ngày';
                else statusStr = '🟢 Còn ' + daysLeft + ' ngày';
            }
            aoa.push(['', u.email || '', u.name || '', expStr, statusStr]);
        });
        var ws = XLSX.utils.aoa_to_sheet(aoa);
        ws['!cols'] = COLUMNS.map(function(c) { return { wch: c.width }; });
        XLSX.utils.book_append_sheet(wb, ws, 'Users');

        var today = new Date();
        var dateStr = today.getFullYear() + String(today.getMonth() + 1).padStart(2, '0') + String(today.getDate()).padStart(2, '0');
        XLSX.writeFile(wb, 'users_export_' + dateStr + '.xlsx');
    } catch(err) { alert('❌ Lỗi export: ' + err.message); }
}

/* ============ IMPORT EXCEL ============ */
function handleImportFileSelect(e) {
    var file = e.target.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function(evt) {
        try {
            var data = new Uint8Array(evt.target.result);
            var workbook = XLSX.read(data, { type: 'array' });
            var sheet = workbook.Sheets[workbook.SheetNames[0]];
            var rows = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: '' });
            processImport(rows);
        } catch(err) { alert('❌ Lỗi đọc file: ' + err.message); }
        e.target.value = '';
    };
    reader.readAsArrayBuffer(file);
}

function processImport(rows) {
    if (!rows || rows.length < 2) return alert('❌ File rỗng!');
    var headerRowIdx = -1;
    for (var i = 0; i < Math.min(5, rows.length); i++) {
        var r = rows[i].map(function(c) { return String(c || '').toLowerCase().trim(); });
        if (r.indexOf('email') !== -1) { headerRowIdx = i; break; }
    }
    if (headerRowIdx === -1) return alert('❌ Không tìm thấy cột "email"!');

    var header = rows[headerRowIdx].map(function(c) { return String(c || '').toLowerCase().trim(); });
    var emailCol = header.indexOf('email');
    var nameCol = header.indexOf('name');
    var expCol = header.indexOf('expiresat');

    var existingUserMap = {}, existingAdminSet = {};
    usersCache.forEach(function(u) {
        var email = (u.email || '').toLowerCase();
        if (u.role === 'admin') existingAdminSet[email] = true;
        else existingUserMap[email] = u;
    });

    importRows = [];
    var seenInFile = {};

    for (var i = headerRowIdx + 1; i < rows.length; i++) {
        var row = rows[i];
        if (!row || row.length === 0) continue;
        var email = emailCol >= 0 ? String(row[emailCol] || '').trim().toLowerCase() : '';
        var name = nameCol >= 0 ? String(row[nameCol] || '').trim() : '';
        var expRaw = expCol >= 0 ? row[expCol] : '';
        if (!email && !name) continue;
        if (existingAdminSet[email]) continue;

        var status = 'ok', reason = '';
        var isUpdate = !!existingUserMap[email];
        if (!email) { status = 'error'; reason = 'Thiếu email'; }
        else if (!email.includes('@')) { status = 'error'; reason = 'Email không hợp lệ'; }
        else if (seenInFile[email]) { status = 'error'; reason = 'Trùng trong file'; }
        else seenInFile[email] = true;

        if (!name && email.indexOf('@') > 0) name = email.split('@')[0];

        var expDate = null, expStr = '';
        if (expRaw) {
            var raw = expRaw;
            if (typeof raw === 'number' && raw > 25569) {
                var d = new Date((raw - 25569) * 86400 * 1000);
                if (!isNaN(d.getTime())) { expDate = d; expStr = formatDate(d); }
            } else {
                var s = String(raw).trim();
                var m = s.match(/^(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})$/);
                if (m) {
                    var d2 = new Date(parseInt(m[1]), parseInt(m[2]) - 1, parseInt(m[3]), 23, 59, 59);
                    if (!isNaN(d2.getTime())) { expDate = d2; expStr = formatDate(d2); }
                } else {
                    var d3 = new Date(s);
                    if (!isNaN(d3.getTime())) { expDate = d3; expStr = formatDate(d3); }
                    else if (status === 'ok') { status = 'warn'; reason = 'Ngày không hợp lệ'; }
                }
            }
        }

        importRows.push({
            rowNum: i + 1, email: email, name: name, role: 'user',
            expDate: expDate, expStr: expStr, status: status, reason: reason, isUpdate: isUpdate
        });
    }

    if (importRows.length === 0) return alert('❌ Không có dòng hợp lệ!');
    renderImportPreview();
    $('importModal').classList.add('show');
}

function renderImportPreview() {
    var tbody = $('importTableBody');
    var html = '';
    var countOk = 0, countUpdate = 0, countWarn = 0, countErr = 0;
    importRows.forEach(function(r) {
        var rowCls = '', statusHtml = '';
        if (r.status === 'ok' && r.isUpdate) { rowCls = 'row-update'; statusHtml = '<span class="status-badge update"><i class="fas fa-sync-alt"></i> Cập nhật</span>'; countUpdate++; }
        else if (r.status === 'ok') { rowCls = 'row-new'; statusHtml = '<span class="status-badge ok"><i class="fas fa-plus"></i> Thêm mới</span>'; countOk++; }
        else if (r.status === 'warn') { rowCls = 'row-warn'; statusHtml = '<span class="status-badge warn">' + escapeHtml(r.reason) + '</span>'; countWarn++; }
        else { rowCls = 'row-error'; statusHtml = '<span class="status-badge err">' + escapeHtml(r.reason) + '</span>'; countErr++; }
        var expDisplay = r.expStr
            ? '<span style="color:#16a34a;font-size:.7rem;font-weight:600;">' + r.expStr + '</span>'
            : '<span style="color:#94a3b8;font-size:.7rem;">Vĩnh viễn</span>';
        html += '<tr class="' + rowCls + '"><td>' + r.rowNum + '</td><td><b>' + escapeHtml(r.email) + '</b></td><td>' + escapeHtml(r.name) + '</td><td><span class="role-badge user">user</span></td><td>' + expDisplay + '</td><td>' + statusHtml + '</td></tr>';
    });
    tbody.innerHTML = html;

    $('importSummary').innerHTML =
        '<div class="import-stat"><div class="num">' + importRows.length + '</div><div class="label">Tổng</div></div>' +
        '<div class="import-stat ok"><div class="num">' + countOk + '</div><div class="label">Thêm mới</div></div>' +
        '<div class="import-stat update"><div class="num">' + countUpdate + '</div><div class="label">Cập nhật</div></div>' +
        '<div class="import-stat warn"><div class="num">' + countWarn + '</div><div class="label">Cảnh báo</div></div>' +
        '<div class="import-stat err"><div class="num">' + countErr + '</div><div class="label">Lỗi</div></div>';

    var totalImportable = countOk + countUpdate + countWarn;
    if ($('importCount')) $('importCount').textContent = totalImportable;
    if ($('importConfirmBtn')) $('importConfirmBtn').disabled = totalImportable === 0;
}

async function doImport() {
    var skipDuplicates = $('importSkipDuplicates').checked;
    var skipInvalid = $('importSkipInvalid').checked;
    var toImport = importRows.filter(function(r) {
        if (r.status === 'error') return false;
        if (r.status === 'warn' && skipInvalid) return false;
        if (r.isUpdate && skipDuplicates) return false;
        return true;
    });
    if (toImport.length === 0) return alert('⚠️ Không có user nào để import!');

    var totalNew = toImport.filter(function(r) { return !r.isUpdate; }).length;
    var totalUpdate = toImport.filter(function(r) { return r.isUpdate; }).length;
    if (!confirm('📥 IMPORT ' + toImport.length + ' TÀI KHOẢN?\n\n• Thêm mới: ' + totalNew + '\n• Cập nhật: ' + totalUpdate)) return;

    var btn = $('importConfirmBtn');
    var originalHTML = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-pulse"></i> Đang import...';

    var success = 0, failed = 0;
    var BATCH_SIZE = 400;
    for (var i = 0; i < toImport.length; i += BATCH_SIZE) {
        var chunk = toImport.slice(i, i + BATCH_SIZE);
        var batch = db.batch();
        chunk.forEach(function(r) {
            var ref = db.collection('allowed_users').doc(r.email);
            var data = { email: r.email, name: r.name, role: 'user', addedBy: currentUser.email };
            if (!r.isUpdate) {
                data.addedAt = firebase.firestore.FieldValue.serverTimestamp();
                data.importedFromExcel = true;
            } else data.updatedAt = firebase.firestore.FieldValue.serverTimestamp();
            data.expiresAt = r.expDate ? firebase.firestore.Timestamp.fromDate(r.expDate) : null;
            batch.set(ref, data, { merge: true });
        });
        try { await batch.commit(); success += chunk.length; }
        catch(err) { failed += chunk.length; console.error(err); }
    }

    btn.disabled = false;
    btn.innerHTML = originalHTML;
    importRows = [];
    try { localStorage.removeItem('admin_users_cache'); } catch(e) {}
    toImport.forEach(function(r) { try { localStorage.removeItem('user_cache_' + r.email); } catch(e) {} });
    alert('✅ Import xong!\n\n✓ Thành công: ' + success + (failed ? '\n✗ Thất bại: ' + failed : ''));
    $('importModal').classList.remove('show');
    loadUsers(true);
}

/* ============ DATE HELPERS ============ */
function getExpiryDate(expiresAt) {
    if (!expiresAt) return null;
    try {
        var ea = expiresAt;
        if (typeof ea.toDate === 'function') return ea.toDate();
        if (ea.seconds) return new Date(ea.seconds * 1000);
        return new Date(ea);
    } catch(e) { return null; }
}
function formatDate(d) {
    if (!d) return '';
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}
function formatTimeDiff(ms) {
    if (ms < 60000) return 'Vừa xong';
    if (ms < 3600000) return Math.floor(ms / 60000) + ' phút trước';
    if (ms < 86400000) return Math.floor(ms / 3600000) + ' giờ trước';
    if (ms < 2592000000) return Math.floor(ms / 86400000) + ' ngày trước';
    return Math.floor(ms / 2592000000) + ' tháng trước';
}

/* ============ INIT AUTH UI ============ */
function initAuthUI() {
    if ($('headerLoginBtn')) $('headerLoginBtn').addEventListener('click', showLoginModal);
    if ($('loginClose')) $('loginClose').addEventListener('click', hideLoginModal);
    if ($('loginModal')) $('loginModal').addEventListener('click', function(e) { if (e.target === this) hideLoginModal(); });
    if ($('googleLoginBtn')) {
        $('googleLoginBtn').addEventListener('click', async function() {
            var provider = new firebase.auth.GoogleAuthProvider();
            provider.setCustomParameters({ prompt: 'select_account' });
            try {
                await auth.signInWithPopup(provider);
                hideLoginModal();
            } catch(e) {
                if (e.code === 'auth/popup-blocked') await auth.signInWithRedirect(provider);
                else if (e.code !== 'auth/popup-closed-by-user') showLoginError('Lỗi: ' + e.message);
            }
        });
    }
    if ($('logoutBtn')) {
        $('logoutBtn').addEventListener('click', function() {
            if (confirm('Đăng xuất?')) {
                try { if (currentUser && currentUser.email) localStorage.removeItem('user_cache_' + currentUser.email); } catch(e) {}
                auth.signOut();
            }
        });
    }
    if ($('userAvatar')) {
        $('userAvatar').addEventListener('click', function(e) {
            e.stopPropagation();
            $('userDropdown').classList.toggle('show');
        });
    }
    document.addEventListener('click', function(e) {
        var dd = $('userDropdown');
        if (dd && !dd.contains(e.target) && $('userAvatar') && !$('userAvatar').contains(e.target)) dd.classList.remove('show');
    });
    if ($('changeNameBtn')) {
        $('changeNameBtn').addEventListener('click', function() {
            $('userDropdown').classList.remove('show');
            if (!currentUser) return;
            editingEmail = currentUser.email;
            $('changeNameCurrent').textContent = currentUser.name;
            $('changeNameEmail').textContent = currentUser.email;
            $('changeNameInput').value = currentUser.name;
            $('changeNameModal').classList.add('show');
            setTimeout(function() { $('changeNameInput').focus(); }, 100);
        });
    }
    if ($('changeNameClose')) $('changeNameClose').addEventListener('click', function() { $('changeNameModal').classList.remove('show'); });
    if ($('changeNameCancel')) $('changeNameCancel').addEventListener('click', function() { $('changeNameModal').classList.remove('show'); });
    if ($('changeNameModal')) $('changeNameModal').addEventListener('click', function(e) { if (e.target === this) $('changeNameModal').classList.remove('show'); });
    if ($('changeNameConfirm')) $('changeNameConfirm').addEventListener('click', doChangeName);

    if ($('editExpiryClose')) $('editExpiryClose').addEventListener('click', function() { $('editExpiryModal').classList.remove('show'); });
    if ($('editExpiryCancel')) $('editExpiryCancel').addEventListener('click', function() { $('editExpiryModal').classList.remove('show'); });
    if ($('editExpiryModal')) $('editExpiryModal').addEventListener('click', function(e) { if (e.target === this) $('editExpiryModal').classList.remove('show'); });
    if ($('editExpiryConfirm')) $('editExpiryConfirm').addEventListener('click', doUpdateExpiry);

    if ($('renewalClose')) $('renewalClose').addEventListener('click', closeRenewalModal);
    if ($('renewalModal')) $('renewalModal').addEventListener('click', function(e) { if (e.target === this) closeRenewalModal(); });
    if ($('dropdownRenewBtn')) $('dropdownRenewBtn').addEventListener('click', function(e) { e.preventDefault(); openRenewalModal(); });
    if ($('expiryRenewBtn')) $('expiryRenewBtn').addEventListener('click', function(e) { e.preventDefault(); openRenewalModal(); });

    initAdminPanel();
}

/* ============ TIMEOUT FALLBACK ============ */
setTimeout(function() {
    if (!appInitialized) {
        console.warn('Auth timeout, entering demo mode');
        enterDemoMode();
    }
}, 5000);
"""

    # Inject config
    js = js.replace("__TRIAL_DAYS__", str(config.get("trial_days", 7)))
    js = js.replace("__BANK_CONFIG__", json.dumps(config.get("bank_config", {}), ensure_ascii=False))
    js = js.replace("__PACKAGES__", json.dumps(config.get("packages", []), ensure_ascii=False))
    js = js.replace("__RENEWAL_SUPPORT_ZALO__", config.get("renewal_support_zalo", ""))

    # Inject trial days vào text HTML footer
    js = js.replace("7 ngày</b> dùng thử", str(config.get("trial_days", 7)) + " ngày</b> dùng thử")

    return js


def build_renewal_js(config=None):
    # Đã gộp vào build_accounts_js
    return ""


# ═══════════════════════════════════════════════════════════════
# HELPER: gọi 1 lần lấy hết CSS + HTML + JS
# ═══════════════════════════════════════════════════════════════
def build_all_auth(config):
    """
    config: dict đã load từ JSON.
    Trả về tuple (css, html, js).
    """
    css = build_accounts_css()
    html = build_accounts_html()
    js = build_accounts_js(config)

    # Replace trial days trong HTML footer (nếu chưa replace)
    html = html.replace(
        '<b>tặng miễn phí <span id="trialDaysText">7</span> ngày</b>',
        '<b>tặng miễn phí <span id="trialDaysText">' + str(config.get("trial_days", 7)) + '</span> ngày</b>'
    )
    return css, html, js

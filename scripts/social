# -*- coding: utf-8 -*-
"""
Template cho Zalo + TikTok (bar, floating button, hover card).
KHÔNG CẦN SỬA khi đổi cấu trúc Excel hay giao diện học.
Chỉ cần chỉnh config.json để đổi số Zalo / username TikTok.
"""


def build_social_css():
    """CSS riêng cho Zalo + TikTok."""
    return r"""
/* ============ FLOATING LEFT GROUP (Zalo + TikTok) ============ */
.floating-left-group{
    position:fixed;bottom:calc(20px + env(safe-area-inset-bottom));
    left:20px;z-index:1000;display:flex;flex-direction:column;
    gap:.5rem;align-items:flex-start;
}

.zalo-btn{
    display:flex;align-items:center;gap:.5rem;
    padding:.7rem 1.1rem;border-radius:50px;
    background:linear-gradient(135deg, #0068ff, #0084ff);
    color:#fff;text-decoration:none;font-weight:700;font-size:.85rem;
    box-shadow:0 8px 24px rgba(0,104,255,.4);
    transition:all .35s cubic-bezier(.34,1.56,.64,1);
    -webkit-tap-highlight-color:transparent;white-space:nowrap;
    border:2px solid #fff;font-family:inherit;overflow:hidden;
    position:relative;
}
.zalo-btn:hover,.zalo-btn:active{transform:scale(1.05);box-shadow:0 12px 32px rgba(0,104,255,.55);color:#fff}
.zalo-btn i{font-size:1.2rem;flex-shrink:0;line-height:1;position:relative;z-index:2}
.zalo-btn .zalo-text{
    line-height:1.15;display:flex;flex-direction:column;
    position:relative;z-index:2;transition:opacity .2s, max-width .35s;
    max-width:200px;overflow:hidden;
}
.zalo-btn .zalo-label{font-size:.65rem;opacity:.85;font-weight:500;white-space:nowrap}
.zalo-btn .zalo-name{font-size:.85rem;font-weight:700;white-space:nowrap}
.zalo-btn::before{
    content:'';position:absolute;inset:0;border-radius:50px;
    background:linear-gradient(135deg, #0068ff, #0084ff);
    opacity:.5;z-index:1;animation:zaloPulse 2s infinite;
}
@keyframes zaloPulse{
    0%{transform:scale(1);opacity:.5}
    50%{transform:scale(1.08);opacity:0}
    100%{transform:scale(1);opacity:0}
}
.zalo-btn.compact{width:52px;height:52px;padding:0;border-radius:50%;justify-content:center;gap:0}
.zalo-btn.compact .zalo-text{opacity:0;max-width:0}
.zalo-btn.compact i{font-size:1.35rem}
.zalo-btn.compact::before{border-radius:50%}

/* ============ TIKTOK FLOAT BUTTON + HOVER CARD ============ */
.tiktok-float-wrap{position:relative;}
.tiktok-float-btn{
    display:flex;align-items:center;gap:.5rem;
    padding:.7rem 1.1rem;border-radius:50px;
    background:linear-gradient(135deg, #000, #2d2d2d);
    color:#fff;text-decoration:none;font-weight:700;font-size:.85rem;
    box-shadow:0 8px 24px rgba(0,0,0,.4), 0 0 0 2px rgba(254,44,85,.4);
    transition:all .35s cubic-bezier(.34,1.56,.64,1);
    -webkit-tap-highlight-color:transparent;white-space:nowrap;
    border:2px solid #fff;font-family:inherit;overflow:hidden;
    position:relative;cursor:pointer;
}
.tiktok-float-btn:hover,.tiktok-float-btn:active{transform:scale(1.05);box-shadow:0 12px 32px rgba(0,0,0,.5), 0 0 0 3px rgba(254,44,85,.6);color:#fff}
.tiktok-float-btn i{font-size:1.2rem;flex-shrink:0;line-height:1;position:relative;z-index:2}
.tiktok-float-btn .tiktok-text{
    line-height:1.15;display:flex;flex-direction:column;
    position:relative;z-index:2;transition:opacity .2s, max-width .35s;
    max-width:200px;overflow:hidden;
}
.tiktok-float-btn .tiktok-label{font-size:.65rem;opacity:.85;font-weight:500;white-space:nowrap}
.tiktok-float-btn .tiktok-name{font-size:.85rem;font-weight:700;white-space:nowrap}
.tiktok-float-btn::before{
    content:'';position:absolute;inset:0;border-radius:50px;
    background:linear-gradient(135deg, #fe2c55, #25f4ee);
    opacity:.35;z-index:1;animation:tiktokPulse 2s infinite;
}
@keyframes tiktokPulse{
    0%{transform:scale(1);opacity:.35}
    50%{transform:scale(1.1);opacity:0}
    100%{transform:scale(1);opacity:0}
}
.tiktok-float-btn.compact{width:52px;height:52px;padding:0;border-radius:50%;justify-content:center;gap:0}
.tiktok-float-btn.compact .tiktok-text{opacity:0;max-width:0}
.tiktok-float-btn.compact i{font-size:1.35rem}
.tiktok-float-btn.compact::before{border-radius:50%}

.tiktok-hover-card{
    position:absolute;bottom:calc(100% + 10px);left:0;width:300px;
    background:var(--surface);border:1px solid var(--border);
    border-radius:16px;box-shadow:0 20px 50px rgba(0,0,0,.25);
    padding:1rem;opacity:0;visibility:hidden;
    transform:translateY(8px) scale(.96);
    transition:opacity .25s, visibility .25s, transform .25s cubic-bezier(.34,1.56,.64,1);
    pointer-events:none;z-index:2000;
}
.tiktok-float-wrap:hover .tiktok-hover-card{
    opacity:1;visibility:visible;
    transform:translateY(0) scale(1);pointer-events:auto;
}
.tiktok-hover-card::after{
    content:'';position:absolute;top:100%;left:32px;
    width:16px;height:16px;background:var(--surface);
    border-right:1px solid var(--border);border-bottom:1px solid var(--border);
    transform:translateY(-8px) rotate(45deg);
}
@media(hover:none) and (pointer:coarse){
    .tiktok-float-wrap:hover .tiktok-hover-card{
        opacity:0;visibility:hidden;
        transform:translateY(8px) scale(.96);pointer-events:none;
    }
    .tiktok-float-wrap.show-mobile .tiktok-hover-card{
        opacity:1;visibility:visible;
        transform:translateY(0) scale(1);pointer-events:auto;
        left:-4px;width:min(300px, calc(100vw - 32px));
    }
}
.thc-header{display:flex;align-items:center;gap:.75rem;margin-bottom:.85rem}
.thc-avatar-wrap{position:relative;flex-shrink:0;}
.thc-avatar{
    width:60px;height:60px;border-radius:50%;object-fit:cover;
    border:3px solid transparent;
    background:linear-gradient(var(--surface),var(--surface)) padding-box,
               linear-gradient(135deg,#fe2c55,#25f4ee) border-box;
    box-shadow:0 4px 12px rgba(0,0,0,.15);
}
.thc-avatar-fallback{
    width:60px;height:60px;border-radius:50%;
    background:linear-gradient(135deg,#fe2c55,#25f4ee);
    color:#fff;display:flex;align-items:center;justify-content:center;
    font-size:1.7rem;font-weight:800;flex-shrink:0;
    border:3px solid var(--surface);box-shadow:0 4px 12px rgba(0,0,0,.15);
}
.thc-verified{
    position:absolute;bottom:-2px;right:-2px;
    width:20px;height:20px;border-radius:50%;
    background:#20d5ec;color:#fff;
    display:flex;align-items:center;justify-content:center;
    font-size:.65rem;border:2.5px solid var(--surface);
}
.thc-info{flex:1;min-width:0}
.thc-nick{
    font-size:1rem;font-weight:800;color:var(--text);
    overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
    margin-bottom:.15rem;line-height:1.2;
}
.thc-user{
    font-size:.78rem;color:var(--text-3);
    overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
    display:flex;align-items:center;gap:.25rem;
}
.thc-user i{font-size:.72rem;color:var(--tiktok-pink)}
.thc-desc{
    font-size:.75rem;color:var(--text-2);
    padding:.6rem 0;border-top:1px solid var(--border);
    border-bottom:1px solid var(--border);margin-bottom:.75rem;line-height:1.5;
}
.thc-stats{display:flex;gap:1rem;margin-bottom:.75rem;padding-bottom:.75rem;border-bottom:1px solid var(--border);}
.thc-stat{text-align:center;flex:1}
.thc-stat .num{font-size:.95rem;font-weight:800;color:var(--text);line-height:1;}
.thc-stat .label{font-size:.65rem;color:var(--text-3);text-transform:uppercase;letter-spacing:.3px;margin-top:.25rem;font-weight:600;}
.thc-btn{
    display:flex;align-items:center;justify-content:center;gap:.4rem;
    width:100%;padding:.7rem;border-radius:10px;border:none;
    background:linear-gradient(135deg,#fe2c55,#ff0050);
    color:#fff;font-size:.85rem;font-weight:700;
    text-decoration:none;cursor:pointer;transition:.15s;font-family:inherit;
    box-shadow:0 4px 12px rgba(254,44,85,.3);
}
.thc-btn:hover{transform:translateY(-2px);box-shadow:0 6px 18px rgba(254,44,85,.45);color:#fff}
.thc-btn i{font-size:.95rem}

/* TikTok info bar dưới header */
.tiktok-bar{
    display:flex;align-items:center;gap:.6rem;
    padding:.5rem .85rem;margin-bottom:.6rem;
    background:linear-gradient(135deg, rgba(254,44,85,.06), rgba(37,244,238,.06));
    border:1.5px solid var(--border);border-radius:var(--radius-full);
    font-size:.8rem;color:var(--text-2);
    width:fit-content;max-width:100%;
    transition:.15s;box-shadow:var(--shadow-sm);text-decoration:none;
}
[data-theme="dark"] .tiktok-bar{
    background:linear-gradient(135deg, rgba(254,44,85,.1), rgba(37,244,238,.1));
}
.tiktok-bar:hover{border-color:var(--text-2);box-shadow:0 4px 12px rgba(0,0,0,.08);transform:translateY(-1px);}
.tiktok-bar-avatar{
    width:32px;height:32px;border-radius:50%;object-fit:cover;flex-shrink:0;
    border:2px solid var(--border);
    background:linear-gradient(135deg,#fe2c55,#25f4ee);
}
.tiktok-bar-info{display:flex;flex-direction:column;line-height:1.2;min-width:0;flex:1}
.tiktok-bar-info .tiktok-nick{font-weight:800;color:var(--text);font-size:.92rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.tiktok-bar-info .tiktok-user{font-size:.75rem;color:var(--text-3);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:flex;align-items:center;gap:.25rem}
.tiktok-bar-info .tiktok-user i{font-size:.7rem;}
.tiktok-bar-link{
    display:inline-flex;align-items:center;gap:.35rem;
    padding:.4rem .8rem;border-radius:50px;
    background:linear-gradient(135deg,#000,#333);color:#fff !important;
    font-size:.75rem;font-weight:700;text-decoration:none;
    white-space:nowrap;transition:.15s;flex-shrink:0;
    box-shadow:0 2px 8px rgba(0,0,0,.2);
}
[data-theme="dark"] .tiktok-bar-link{background:linear-gradient(135deg,#fff,#e5e5e5);color:#000 !important;}
.tiktok-bar-link:hover{transform:translateY(-1px);box-shadow:0 6px 16px rgba(0,0,0,.3);}
.tiktok-bar-link i{font-size:.85rem;}

.dropdown-zalo{
    display:flex;align-items:center;gap:.5rem;width:100%;
    padding:.65rem .75rem;border-radius:var(--radius-sm);
    background:linear-gradient(135deg, #0068ff, #0084ff);
    color:#fff !important;font-size:.85rem;font-weight:700;
    text-decoration:none;transition:.15s;margin-top:.25rem;
}
.dropdown-zalo:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,104,255,.3);color:#fff !important;}
.dropdown-zalo i{font-size:1rem;}

.dropdown-tiktok{
    display:flex;align-items:center;gap:.5rem;width:100%;
    padding:.65rem .75rem;border-radius:var(--radius-sm);
    background:linear-gradient(135deg, #000, #333);
    color:#fff !important;font-size:.85rem;font-weight:700;
    text-decoration:none;transition:.15s;margin-top:.25rem;
}
[data-theme="dark"] .dropdown-tiktok{background:linear-gradient(135deg,#fff,#e5e5e5);color:#000 !important;}
.dropdown-tiktok:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,.3);}
.dropdown-tiktok i{font-size:1rem;}

/* Ẩn floating khi silent mode */
body.hide-floating .floating-left-group,
body.hide-floating .tiktok-bar { display: none !important; }
"""


def build_social_html():
    """HTML cho Zalo + TikTok (floating + bar)."""
    return r"""
<!-- ✅ FLOATING LEFT GROUP: Zalo + TikTok -->
<div class="floating-left-group" id="floatingLeftGroup">
    <a class="zalo-btn" id="zaloBtn" href="#" target="_blank" rel="noopener noreferrer" title="Liên hệ Zalo hỗ trợ">
        <i class="fas fa-comment-dots"></i>
        <div class="zalo-text">
            <span class="zalo-label">Liên hệ Zalo</span>
            <span class="zalo-name">Hỗ trợ</span>
        </div>
    </a>

    <div class="tiktok-float-wrap" id="tiktokFloatWrap">
        <a class="tiktok-float-btn" id="tiktokFloatBtn" href="#" target="_blank" rel="noopener noreferrer" title="Theo dõi TikTok">
            <i class="fab fa-tiktok"></i>
            <div class="tiktok-text">
                <span class="tiktok-label">Theo dõi TikTok</span>
                <span class="tiktok-name" id="tiktokFloatName">Thảo nói 中文</span>
            </div>
        </a>

        <div class="tiktok-hover-card" id="tiktokHoverCard">
            <div class="thc-header">
                <div class="thc-avatar-wrap">
                    <img class="thc-avatar" id="thcAvatar" src="" alt="TikTok" style="display:none">
                    <div class="thc-avatar-fallback" id="thcAvatarFallback">T</div>
                    <div class="thc-verified"><i class="fas fa-check"></i></div>
                </div>
                <div class="thc-info">
                    <div class="thc-nick" id="thcNick">Thảo nói 中文</div>
                    <div class="thc-user"><i class="fab fa-tiktok"></i> <span id="thcUser">@thaonoizhongwen</span></div>
                </div>
            </div>
            <div class="thc-desc">Học tiếng Trung mỗi ngày cùng Thảo · Văn phòng & Công xưởng 🇨🇳</div>
            <div class="thc-stats">
                <div class="thc-stat"><div class="num" id="thcFollowers">1.2K</div><div class="label">Followers</div></div>
                <div class="thc-stat"><div class="num" id="thcLikes">15.6K</div><div class="label">Likes</div></div>
                <div class="thc-stat"><div class="num" id="thcVideos">128</div><div class="label">Videos</div></div>
            </div>
            <a class="thc-btn" id="thcFollowBtn" href="#" target="_blank" rel="noopener noreferrer">
                <i class="fab fa-tiktok"></i> Theo dõi ngay
            </a>
        </div>
    </div>
</div>
"""


def build_tiktok_bar_html():
    """TikTok info bar dưới header."""
    return r"""
<a class="tiktok-bar" id="tiktokBar" href="#" target="_blank" rel="noopener noreferrer" title="Theo dõi TikTok">
    <img class="tiktok-bar-avatar" id="tiktokBarAvatar" src="" alt="TikTok">
    <div class="tiktok-bar-info">
        <div class="tiktok-nick" id="tiktokBarNick">Thảo nói 中文</div>
        <div class="tiktok-user"><i class="fab fa-tiktok"></i> <span id="tiktokBarUser">@thaonoizhongwen</span></div>
    </div>
    <span class="tiktok-bar-link">
        <i class="fab fa-tiktok"></i> <span>Theo dõi</span>
    </span>
</a>
"""


def build_social_js():
    """JS init Zalo + TikTok. KHÔNG CẦN SỬA."""
    return r"""
/* ============ TIKTOK HELPERS ============ */
function getTikTokAvatarUrl() {
    if (TIKTOK_AVATAR && TIKTOK_AVATAR.trim()) return TIKTOK_AVATAR;
    var initial = (TIKTOK_NICKNAME || 'T').charAt(0).toUpperCase();
    return 'data:image/svg+xml;utf8,' + encodeURIComponent(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">' +
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">' +
        '<stop offset="0%" stop-color="#fe2c55"/><stop offset="100%" stop-color="#25f4ee"/>' +
        '</linearGradient></defs>' +
        '<rect fill="url(#g)" width="100" height="100"/>' +
        '<text x="50" y="68" font-size="50" fill="#fff" text-anchor="middle" ' +
        'font-family="sans-serif" font-weight="bold">' + initial + '</text></svg>'
    );
}

function initTikTok() {
    var tiktokUrl = TIKTOK_URL || ('https://www.tiktok.com/@' + TIKTOK_USERNAME);
    var avatarUrl = getTikTokAvatarUrl();

    var tiktokBar = $('tiktokBar');
    if (tiktokBar) tiktokBar.href = tiktokUrl;

    var tiktokBarAvatar = $('tiktokBarAvatar');
    if (tiktokBarAvatar) tiktokBarAvatar.src = avatarUrl;

    var tiktokBarNick = $('tiktokBarNick');
    if (tiktokBarNick) tiktokBarNick.textContent = TIKTOK_NICKNAME;

    var tiktokBarUser = $('tiktokBarUser');
    if (tiktokBarUser) tiktokBarUser.textContent = '@' + TIKTOK_USERNAME;

    var tiktokFloatBtn = $('tiktokFloatBtn');
    if (tiktokFloatBtn) {
        tiktokFloatBtn.href = tiktokUrl;
        tiktokFloatBtn.setAttribute('data-username', TIKTOK_USERNAME);
    }

    var tiktokFloatName = $('tiktokFloatName');
    if (tiktokFloatName) tiktokFloatName.textContent = TIKTOK_NICKNAME;

    var thcAvatar = $('thcAvatar');
    var thcAvatarFallback = $('thcAvatarFallback');
    if (thcAvatar && thcAvatarFallback) {
        var testImg = new Image();
        testImg.onload = function() {
            thcAvatar.src = avatarUrl;
            thcAvatar.style.display = 'block';
            thcAvatarFallback.style.display = 'none';
        };
        testImg.onerror = function() {
            thcAvatar.style.display = 'none';
            thcAvatarFallback.style.display = 'flex';
            thcAvatarFallback.textContent = (TIKTOK_NICKNAME || 'T').charAt(0).toUpperCase();
        };
        testImg.src = avatarUrl;
    }

    var thcNick = $('thcNick');
    if (thcNick) thcNick.textContent = TIKTOK_NICKNAME;

    var thcUser = $('thcUser');
    if (thcUser) thcUser.textContent = '@' + TIKTOK_USERNAME;

    var thcFollowBtn = $('thcFollowBtn');
    if (thcFollowBtn) thcFollowBtn.href = tiktokUrl;

    var dropdownTiktokBtn = $('dropdownTiktokBtn');
    if (dropdownTiktokBtn) dropdownTiktokBtn.href = tiktokUrl;

    var floatBtn = $('tiktokFloatBtn');
    var floatWrap = $('tiktokFloatWrap');
    var hoverCard = $('tiktokHoverCard');
    if (floatBtn && floatWrap) {
        var isTouchDevice = ('ontouchstart' in window) ||
                            (navigator.maxTouchPoints > 0) ||
                            (window.matchMedia && window.matchMedia('(hover:none) and (pointer:coarse)').matches);

        if (isTouchDevice) {
            var lastTapTime = 0;
            var DOUBLE_TAP_MS = 350;
            var tapTimer = null;

            floatBtn.addEventListener('click', function(e) {
                var now = Date.now();
                if (now - lastTapTime < DOUBLE_TAP_MS) {
                    if (tapTimer) { clearTimeout(tapTimer); tapTimer = null; }
                    lastTapTime = 0;
                    floatWrap.classList.remove('show-mobile');
                    return;
                }
                e.preventDefault();
                e.stopPropagation();
                lastTapTime = now;
                var isShowing = floatWrap.classList.toggle('show-mobile');
                if (isShowing) {
                    if (floatWrap._hideTimer) clearTimeout(floatWrap._hideTimer);
                    floatWrap._hideTimer = setTimeout(function() {
                        floatWrap.classList.remove('show-mobile');
                    }, 5000);
                }
            }, true);

            document.addEventListener('click', function(e) {
                if (!floatWrap.contains(e.target)) {
                    floatWrap.classList.remove('show-mobile');
                }
            });

            if (hoverCard) {
                hoverCard.addEventListener('click', function(e) { e.stopPropagation(); });
            }
        }
    }
}

/* ============ ZALO HELPERS ============ */
function initZaloButton() {
    var zaloBtn = $('zaloBtn');
    if (!zaloBtn) return;

    var phone = (ZALO_PHONE || '').replace(/\D/g, '');
    var zaloUrl = '#';

    if (phone) {
        zaloUrl = 'https://zalo.me/' + phone;
        zaloBtn.href = zaloUrl;
        zaloBtn.title = 'Liên hệ Zalo: ' + phone;
        zaloBtn.setAttribute('data-phone', phone);
    } else {
        zaloBtn.href = '#';
        zaloBtn.onclick = function(e) { e.preventDefault(); alert('Chưa cấu hình số Zalo.'); };
    }

    var nameEl = zaloBtn.querySelector('.zalo-name');
    if (nameEl && ZALO_NAME) nameEl.textContent = ZALO_NAME;

    var dropdownZalo = $('dropdownZaloBtn');
    if (dropdownZalo) {
        if (phone) {
            dropdownZalo.href = zaloUrl;
        } else {
            dropdownZalo.href = '#';
            dropdownZalo.onclick = function(e) { e.preventDefault(); alert('Chưa cấu hình số Zalo.'); };
        }
    }
}

function initSocial() {
    initZaloButton();
    initTikTok();
}

/* Hiển thị floating theo practice mode */
function updateFloatingLeftVisibility() {
    var zaloBtn = $('zaloBtn');
    var tiktokFloatWrap = $('tiktokFloatWrap');
    var isPracticeMode = document.body.classList.contains('practice-full-open');

    if (isPracticeMode) {
        if (zaloBtn) zaloBtn.style.display = 'none';
        if (tiktokFloatWrap) tiktokFloatWrap.style.display = 'block';
    } else {
        if (zaloBtn) zaloBtn.style.display = 'flex';
        if (tiktokFloatWrap) tiktokFloatWrap.style.display = 'block';
    }
}
"""

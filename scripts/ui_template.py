/* ═══════════════════════════════════════════════════════════ */
/* HEADER LOGO - HỌC TIẾNG TRUNG HSK (FIX BADGE HIỂN THỊ)      */
/* ═══════════════════════════════════════════════════════════ */
.logo-text {
    display: flex;
    align-items: center;
    min-width: 0;
    overflow: visible;
}

.logo-text .title {
    font-size: clamp(1.2rem, 2.2vw, 1.75rem);
    font-weight: 900;
    letter-spacing: -0.03em;
    line-height: 1.15;
    display: flex;
    align-items: center;
    gap: 0.55rem;
    min-width: 0;
}

.logo-text .title .title-text {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #a855f7 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
/* Fallback cho trình duyệt không hỗ trợ background-clip */
@supports not ((-webkit-background-clip: text) or (background-clip: text)) {
    .logo-text .title .title-text {
        color: #7c3aed;
        -webkit-text-fill-color: #7c3aed;
    }
}
[data-theme="dark"] .logo-text .title .title-text {
    background: linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #c084fc 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* ⭐ BADGE HSK — Đảm bảo chữ "HSK" luôn hiển thị rõ */
.logo-text .title .hsk-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.22em 0.65em;
    border-radius: 8px;
    background: linear-gradient(135deg, #f59e0b, #ef4444);
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-family: inherit;
    font-size: 0.62em;
    font-weight: 900;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
    box-shadow: 0 3px 10px rgba(239, 68, 68, 0.45);
    animation: hskBadgePulse 2.5s ease-in-out infinite;
    flex-shrink: 0;
    line-height: 1;
    transform: translateY(-2px);
    white-space: nowrap;
    min-width: 2.8em;
    visibility: visible !important;
    opacity: 1 !important;
}

@keyframes hskBadgePulse {
    0%, 100% {
        box-shadow: 0 3px 10px rgba(239, 68, 68, 0.45);
        transform: translateY(-2px) scale(1);
    }
    50% {
        box-shadow: 0 5px 18px rgba(239, 68, 68, 0.75);
        transform: translateY(-2px) scale(1.06);
    }
}

@media (max-width: 500px) {
    .logo-text .title {
        font-size: 1.1rem;
        gap: 0.4rem;
    }
    .logo-text .title .hsk-badge {
        font-size: 0.6em;
        padding: 0.2em 0.55em;
        min-width: 2.5em;
    }
}
"""
def build_ui_html():
    return r"""
<div class="loading-screen" id="loadingScreen"><i class="fas fa-spinner"></i><div>Đang tải...</div></div>
<div class="sticky-top" id="stickyTop" style="display:none">
<div class="container">
<header class="header"><div class="header-inner">
<div class="logo">
    <div class="logo-icon"><i class="fas fa-language"></i></div>
    <div class="logo-text">
        <div class="title">
            <span class="title-text">Học tiếng Trung</span>
            <span class="hsk-badge">HSK</span>
        </div>
    </div>
</div>
<div class="header-actions">
<div class="trial-badge" id="trialBadge"><i class="fas fa-gem"></i> <span id="trialBadgeText">Trial</span></div>
<div class="demo-badge" id="demoBadge" style="display:none"><i class="fas fa-eye"></i> Demo</div>
<button class="btn-login-header" id="headerLoginBtn" style="display:none"><i class="fas fa-sign-in-alt"></i> <span>Đăng nhập</span></button>
<button class="icon-btn intro-btn" id="introBtn" title="Giới thiệu"><i class="fas fa-info-circle"></i></button>
<button class="icon-btn reset-btn hidden" id="resetBtn" title="Đặt lại bộ lọc"><i class="fas fa-undo-alt"></i><span class="badge" id="resetBadge">0</span></button>
<button class="icon-btn" id="themeToggle" title="Đổi giao diện"><i class="fas fa-moon"></i></button>
<div class="user-menu" id="userMenu" style="display:none">
<img class="user-avatar" id="userAvatar" src="" alt="Avatar">
<div class="user-dropdown show" id="userDropdown">
<div class="user-info"><div class="name" id="userName">-</div><div class="email" id="userEmail">-</div><span class="role" id="userRole">user</span></div>
<div class="user-details" id="userDetails" style="display:none">
<div class="detail-row" id="expiryRow"><div class="detail-icon" id="expiryIconWrap"><i class="fas fa-calendar-check" id="expiryIcon"></i></div><div class="detail-content"><div class="detail-label">Hạn sử dụng</div><div class="detail-value" id="expiryValue">-</div><div class="detail-sub" id="expirySub"></div></div></div>
<div class="detail-progress" id="expiryProgressWrap" style="display:none"><div class="progress-track"><div class="progress-bar" id="expiryProgressBar"></div></div></div>
</div>
<button class="dropdown-item" id="changeNameBtn"><i class="fas fa-user-edit"></i> Đổi tên hiển thị</button>
<button class="dropdown-item" id="openAdminBtn" style="display:none"><i class="fas fa-shield-alt"></i> Quản lý tài khoản</button>
<button class="dropdown-item" id="renewalHistoryBtn"><i class="fas fa-history"></i> Lịch sử gia hạn</button>
<button class="dropdown-renew" id="dropdownRenewBtn" style="display:none"><i class="fas fa-gem"></i><span>Gia hạn tài khoản</span><span class="renew-badge">VIP</span></button>
<button class="dropdown-item danger" id="logoutBtn"><i class="fas fa-sign-out-alt"></i> Đăng xuất</button>
</div>
</div>
</div>
</div></header>
<!-- __TIKTOK_BAR__ -->

<!-- DATASET SELECTOR -->
<div class="dataset-selector" id="datasetSelector">
    <div class="ds-label">
        <i class="fas fa-layer-group"></i>
        <span>Bộ dữ liệu</span>
    </div>
    <div class="ds-main-row">
        <button class="ds-btn ds-btn-primary active" data-dataset="tonghop">
            <i class="fas fa-book-open"></i>
            <span id="dsTonghopLabel">1700 câu phản xạ tổng hợp VPCX</span>
        </button>
        <button class="ds-btn ds-btn-primary" data-dataset-group="chuyen-nganh" id="dsChuyenNganhBtn">
            <i class="fas fa-industry"></i>
            <span>Chuyên ngành</span>
            <i class="fas fa-chevron-down ds-arrow"></i>
            <span class="ds-new-badge" id="dsNewBadge">NEW</span>
        </button>
        <!-- __FAV_DATASET_TAB__ -->
    </div>
    <div class="ds-sub-wrap" id="dsSubWrap" style="display:none">
        <div class="ds-sub-label">
            <i class="fas fa-tags"></i>
            <span>Chọn ngành</span>
        </div>
        <div class="ds-sub-grid" id="dsSubGrid"></div>
    </div>
</div>

<div class="search-filter-row">
<div class="search-bar"><i class="fas fa-search"></i>
<input type="text" id="searchInput" placeholder="Tìm kiếm..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
<button class="search-clear" id="clearSearchBtn" aria-label="Xóa"><i class="fas fa-times"></i></button>
</div>
<div class="filters">
<div class="chip" id="hskChip"><span class="chip-label">HSK</span><span class="chip-value" id="hskValue">Tất cả</span><i class="fas fa-chevron-down chip-arrow"></i>
<select id="hskFilter"><option value="">Tất cả</option><option value="HSK1">HSK1</option><option value="HSK2">HSK2</option><option value="HSK3">HSK3</option><option value="HSK4">HSK4</option><option value="HSK5">HSK5</option><option value="HSK6">HSK6</option></select>
</div>
<div class="chip" id="subjectChip"><span class="chip-label">Chủ đề</span><span class="chip-value" id="subjectValue">Tất cả</span><i class="fas fa-chevron-down chip-arrow"></i>
<select id="subjectFilter"><option value="">Tất cả chủ đề</option></select>
</div>
</div>
</div>
<div class="result-count" id="resultCount"><i class="fas fa-list-ul"></i><span>Tìm thấy <b id="resultCountNum">0</b> kết quả</span></div>
</div>
</div>
<div class="fab-group open" id="fabGroup" style="display:none">
<button class="fab-btn fab-sub" id="toggleViBtn" title="Ẩn/hiện Tiếng Việt"><i class="fas fa-language"></i></button>
<button class="fab-btn fab-sub" id="togglePinyinBtn" title="Ẩn/hiện Pinyin"><i class="fas fa-spell-check"></i></button>
<button class="fab-btn fab-sub" id="togglePracticeBtn" title="Ẩn/hiện Ô luyện dịch"><i class="fas fa-keyboard"></i></button>
<button class="fab-btn fab-sub fab-focus" id="toggleFocusBtn" title="Click để tắt Zalo/TikTok (Silent mode)"><i class="fas fa-bell"></i></button>
<button class="fab-btn fab-main" id="fabMainBtn" title="Tùy chọn hiển thị"><i class="fas fa-sliders-h"></i></button>
</div>
<main class="main" id="mainContent" style="display:none">
<div class="container">

<!-- __QUICK_INTRO_BANNER__ -->

<div class="demo-banner" id="demoBanner" style="display:none">
<div class="demo-banner-icon"><i class="fas fa-gift"></i></div>
<div class="demo-banner-text"><div class="title" id="demoBannerTitle">Đăng nhập miễn phí để mở khóa toàn bộ</div>
<div class="desc" id="demoBannerDesc">Đăng nhập bằng <b>Gmail</b> để xem <b>toàn bộ kho câu</b>, không giới luyện viết.<br>Nghe + Luyện viết còn lại hôm nay: <b id="demoRemainingText" style="color:#16a34a">100</b> lượt.</div></div>
<button class="demo-banner-btn" id="demoBannerBtn" onclick="showLoginModal()"><i class="fas fa-sign-in-alt"></i> <span id="demoBannerBtnText">Đăng nhập bằng Gmail</span></button>
</div>
<div class="expiry-banner" id="expiryBanner" style="display:none">
    <div class="expiry-banner-icon" id="expiryBannerIcon">
        <i class="fas fa-hourglass-half"></i>
    </div>
    <div class="expiry-banner-text">
        <div class="title" id="expiryBannerTitle">Tài khoản sắp hết hạn</div>
        <div class="desc" id="expiryBannerDesc">Đang cập nhật...</div>
    </div>
    <button class="expiry-banner-btn" id="expiryContactBtn" type="button">
        <i class="fas fa-gem"></i> Gia hạn ngay
    </button>
</div>
<div class="mobile-view" id="mobileWrapper"><div class="no-data"><i class="fas fa-spinner fa-pulse"></i>Đang tải...</div></div>
</div>
</main>
<div class="writer-modal" id="writerModal">
<div class="writer-box">
<button class="writer-close" id="writerClose" aria-label="Đóng"><i class="fas fa-times"></i></button>
<div class="writer-char-info"><div class="vi-small" id="writerViSmall"></div><div class="pinyin-small" id="writerPinyinSmall"></div></div>
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
<div class="pf-brand"><div class="pf-brand-icon"><i class="fas fa-language"></i></div>
<div class="pf-brand-text"><div class="pf-brand-title">Học tiếng Trung</div><div class="pf-brand-sub">Văn phòng &amp; Công xưởng</div></div>
</div>
<div class="pf-counter" id="pfCounter">Câu 1 / 1</div>
<div class="pf-tags" id="pfTags"></div>
<button class="pf-close" id="pfClose" aria-label="Đóng"><i class="fas fa-times"></i></button>
</div>
<div class="pf-filters">

<div class="pf-filter-row">
<div class="pf-chip" id="pfHskChip"><span class="pf-chip-label">HSK</span><span class="pf-chip-value" id="pfHskValue">Tất cả</span><i class="fas fa-chevron-down pf-chip-arrow"></i>
<select id="pfHskFilter"><option value="">Tất cả</option><option value="HSK1">HSK1</option><option value="HSK2">HSK2</option><option value="HSK3">HSK3</option><option value="HSK4">HSK4</option><option value="HSK5">HSK5</option><option value="HSK6">HSK6</option></select>
</div>
<div class="pf-chip" id="pfSubjectChip"><span class="pf-chip-label">Chủ đề</span><span class="pf-chip-value" id="pfSubjectValue">Tất cả</span><i class="fas fa-chevron-down pf-chip-arrow"></i>
<select id="pfSubjectFilter"><option value="">Tất cả chủ đề</option></select>
</div>
</div>

<div class="pf-dataset-row" id="pfDatasetRow">
    <span class="pf-dataset-label"><i class="fas fa-layer-group"></i> Bộ dữ liệu</span>
    <select class="pf-dataset-select" id="pfDatasetSelect"></select>

    <div class="pf-dataset-search">
        <i class="fas fa-search"></i>
        <input type="text" id="pfSearchInput" placeholder="Tìm kiếm..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false">
        <button class="pf-search-clear" id="pfClearSearchBtn" aria-label="Xóa"><i class="fas fa-times"></i></button>
    </div>

    <div class="pf-quick-nav" id="pfQuickNavWrap">
        <span class="pf-quick-nav-label">Câu:</span>
        <select class="pf-quick-nav-select" id="pfQuickNav"><option value="">-- Chọn câu --</option></select>
    </div>
</div>

</div>
<div class="practice-full-body">
<div class="practice-full-content">
<div class="practice-full-vi" id="pfVi">-</div>
<div class="practice-full-input-wrap">
<div class="practice-input-row">
<textarea class="practice-full-input" id="pfInput" placeholder="Gõ tiếng Trung..." autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false" rows="1"></textarea>
<button class="practice-speak-btn" id="pfSpeakBtn" type="button" title="Nghe câu này" aria-label="Nghe câu này"><i class="fas fa-volume-up"></i></button>
</div>
<div class="char-preview" id="pfPreview"></div>
<div class="practice-full-status" id="pfStatus"></div>
</div>
<div class="reveal-actions">
<button id="pfHintBtn"><i class="fas fa-lightbulb"></i> Gợi ý</button>
<button id="pfRevealBtn"><i class="fas fa-eye"></i> Xem đáp án</button>
</div>
<div class="answer-reveal" id="pfAnswer">
<div class="answer-chars" id="pfAnswerChars"></div>
<div class="answer-pinyin" id="pfAnswerPinyin"></div>
</div>
</div>
</div>
<div class="practice-full-nav">
    <button class="pf-nav-icon main-nav" id="pfPrevBtn" type="button" title="Câu trước" aria-label="Câu trước">
        <i class="fas fa-chevron-left"></i>
    </button>
    <button class="pf-nav-icon main-nav primary" id="pfNextBtn" type="button" title="Câu sau" aria-label="Câu sau">
        <i class="fas fa-chevron-right"></i>
    </button>
    <button class="pf-nav-icon main-nav speak" id="pfQuickSpeakBtn" type="button" title="Đọc cả câu" aria-label="Đọc cả câu">
        <i class="fas fa-volume-up"></i>
    </button>
    <div class="mini-group">
        <button class="pf-nav-icon mini-nav random" id="pfRandomToggleBtn" type="button" title="Bật/tắt chế độ nhảy câu ngẫu nhiên" aria-label="Chế độ ngẫu nhiên">
            <i class="fas fa-dice"></i>
        </button>
        <button class="pf-nav-icon mini-nav voice" id="pfVoiceBtn" type="button" title="Cài đặt giọng đọc" aria-label="Cài đặt giọng đọc">
            <i class="fas fa-headphones"></i>
        </button>
    </div>
</div>
<a class="pf-tiktok-float" id="pfTiktokFloat" href="#" target="_blank" rel="noopener noreferrer" title="Theo dõi TikTok">
<span class="pf-tiktok-avatar-wrap">
<img class="pf-tiktok-avatar" id="pfTiktokAvatar" src="" alt="TikTok" onerror="this.style.display='none'">
<i class="fab fa-tiktok pf-tiktok-fallback-icon"></i>
</span>
<span class="pf-tiktok-content">
<span class="pf-tiktok-label">Theo dõi</span>
<span class="pf-tiktok-name" id="pfTiktokName">TikTok</span>
</span>
<i class="fab fa-tiktok pf-tiktok-badge"></i>
</a>
</div>
<div class="voice-modal" id="voiceModal">
    <div class="voice-box">
        <div class="voice-header">
            <h2><i class="fas fa-sliders-h"></i> Cài đặt giọng đọc</h2>
            <button class="voice-close" id="voiceClose" aria-label="Đóng"><i class="fas fa-times"></i></button>
        </div>
        <div class="voice-body">

            <div class="voice-group">
                <div class="voice-group-label">
                    <span><i class="fas fa-tachometer-alt"></i> Tốc độ đọc</span>
                    <span class="voice-value" id="voiceRateValue">1.00×</span>
                </div>
                <div class="voice-slider-row">
                    <button type="button" id="voiceRateMinus" title="Chậm hơn">−</button>
                    <input type="range" class="voice-slider" id="voiceRateSlider" min="0.5" max="1.5" step="0.05" value="1.0">
                    <button type="button" id="voiceRatePlus" title="Nhanh hơn">+</button>
                </div>
                <div class="voice-preset-row">
                    <button class="voice-preset-btn" data-rate="0.6">0.6× Rất chậm</button>
                    <button class="voice-preset-btn" data-rate="0.75">0.75× Chậm</button>
                    <button class="voice-preset-btn" data-rate="0.85">0.85× Chuẩn</button>
                    <button class="voice-preset-btn" data-rate="1.0">1.0× Bình thường</button>
                    <button class="voice-preset-btn" data-rate="1.15">1.15× Nhanh</button>
                </div>
            </div>

            <div class="voice-group">
                <div class="voice-group-label">
                    <span><i class="fas fa-microphone"></i> Giọng đọc tiếng Trung</span>
                </div>
                <select class="voice-select" id="voiceSelect">
                    <option value="">-- Tự động (mặc định) --</option>
                </select>
            </div>

            <div class="voice-group">
                <div class="voice-group-label">
                    <span><i class="fas fa-music"></i> Cao độ (Pitch)</span>
                    <span class="voice-value" id="voicePitchValue">1.00</span>
                </div>
                <div class="voice-slider-row">
                    <button type="button" id="voicePitchMinus" title="Trầm hơn">−</button>
                    <input type="range" class="voice-slider" id="voicePitchSlider" min="0.5" max="1.5" step="0.05" value="1.0">
                    <button type="button" id="voicePitchPlus" title="Cao hơn">+</button>
                </div>
            </div>

            <div class="voice-group">
                <div class="voice-group-label">
                    <span><i class="fas fa-volume-up"></i> Âm lượng</span>
                    <span class="voice-value" id="voiceVolumeValue">100%</span>
                </div>
                <div class="voice-slider-row">
                    <button type="button" id="voiceVolumeMinus" title="Nhỏ hơn">−</button>
                    <input type="range" class="voice-slider" id="voiceVolumeSlider" min="0" max="1" step="0.05" value="1.0">
                    <button type="button" id="voiceVolumePlus" title="To hơn">+</button>
                </div>
            </div>

            <button class="voice-test-btn" id="voiceTestBtn" type="button">
                <i class="fas fa-play"></i> Nghe thử
            </button>

            <button class="voice-reset" id="voiceResetBtn" type="button">
                <i class="fas fa-undo-alt"></i> Khôi phục mặc định
            </button>

            <div class="voice-note">
                <i class="fas fa-info-circle"></i>
                <div>Cài đặt được <b>lưu tự động</b> và áp dụng cho tất cả nút loa. Danh sách giọng đọc phụ thuộc vào <b>trình duyệt và hệ điều hành</b> của bạn.</div>
            </div>

        </div>
    </div>
</div>

<!-- ONBOARDING MODAL - CHON CHU DE QUAN TAM -->
<div class="onboarding-modal" id="onboardingModal">
    <div class="onboarding-box">
        <button class="onboarding-close" id="onboardingCloseBtn" type="button" aria-label="Đóng">
            <i class="fas fa-times"></i>
        </button>
        <div class="onboarding-header">
            <div class="onboarding-icon">
                <i class="fas fa-compass"></i>
            </div>
            <div class="onboarding-title" id="onboardingTitle">Bạn quan tâm chủ đề nào?</div>
            <div class="onboarding-subtitle" id="onboardingSubtitle">
                Chọn các chủ đề — chúng tôi sẽ gợi ý câu phù hợp nhất
            </div>
            <div class="onboarding-counter" id="onboardingCounter">
                <i class="fas fa-hand-pointer"></i>
                <span>Đã chọn <b id="onboardingSelectedCount">0</b> / <b id="onboardingMaxCount">3</b></span>
            </div>
        </div>
        <div class="onboarding-body">
            <div class="onboarding-section-label">
                <i class="fas fa-tags"></i>
                <span>Chủ đề có sẵn trong kho</span>
            </div>
            <div class="onboarding-topics" id="onboardingTopics">
                <div class="onboarding-empty">
                    <i class="fas fa-spinner fa-pulse"></i> Đang tải...
                </div>
            </div>
        </div>
        <div class="onboarding-footer">
            <button class="onboarding-btn ghost" id="onboardingSkipBtn" type="button">
                <i class="fas fa-forward"></i> Bỏ qua
            </button>
            <button class="onboarding-btn primary" id="onboardingStartBtn" type="button" disabled>
                <i class="fas fa-check"></i> Bắt đầu học
            </button>
        </div>
    </div>
</div>
"""
def build_ui_js():
    return r"""
var filtered = [];
var state = { search:'', hsk:'', subject:'' };
var PAGE_SIZE = 300;
var renderedCount = 0;
var focusedStt = null;
var mobileWrapper;
var currentBtn = null;

var displayState = { vi: true, pinyin: false, practice: false };

/* HELPER: TIER HIEN TAI CO DUOC MO CHUYEN NGANH KHONG? */
function canAccessChuyenNganh() {
    return (typeof window.APP_TIER !== 'undefined' && window.APP_TIER === 'active');
}

/* THONG BAO KHOA CHUYEN NGANH */
function showChuyenNganhLockMessage() {
    if (typeof currentUser === 'undefined' || !currentUser) {
        if (confirm('Bộ dữ liệu Chuyên ngành\n\n' +
                    'Bạn cần ĐĂNG NHẬP và GIA HẠN để mở khoá.\n\n' +
                    'Đăng nhập ngay?')) {
            if (typeof showLoginModal === 'function') showLoginModal();
        }
    } else {
        if (confirm('Bộ dữ liệu Chuyên ngành\n\n' +
                    'Chỉ tài khoản ĐÃ GIA HẠN mới mở được.\n\n' +
                    'Gia hạn ngay?')) {
            if (typeof openRenewalModal === 'function') openRenewalModal();
        }
    }
}

function showPracticeFullLockMessage() {
    if (typeof currentUser === 'undefined' || !currentUser) {
        if (confirm('Chế độ luyện tập Chuyên ngành\n\n' +
                    'Bạn cần ĐĂNG NHẬP và GIA HẠN để mở khoá.\n\n' +
                    'Đăng nhập ngay?')) {
            if (typeof showLoginModal === 'function') showLoginModal();
        }
    } else {
        if (confirm('Chế độ luyện tập Chuyên ngành\n\n' +
                    'Chỉ tài khoản ĐÃ GIA HẠN mới mở được.\n\n' +
                    'Gia hạn ngay?')) {
            if (typeof openRenewalModal === 'function') openRenewalModal();
        }
    }
}

/* ============================================================ */
/* DATASET SWITCHING                                             */
/* ============================================================ */
function initDatasetSelector() {
    if (typeof DATASET_REGISTRY === 'undefined' || !DATASET_REGISTRY) return;
    if (!DATASET_REGISTRY.tonghop) return;

    var labelEl = $('dsTonghopLabel');
    if (labelEl) {
        var count = DATASET_REGISTRY.tonghop.count
                 || (DATASET_REGISTRY.tonghop.data || []).length;
        labelEl.textContent = count + ' câu phản xạ tổng hợp VPCX';
    }

    var chuyenNganhKeys = Object.keys(DATASET_REGISTRY).filter(function(id) {
        return id !== 'tonghop';
    });

    var cnBtn = $('dsChuyenNganhBtn');
    if (chuyenNganhKeys.length === 0) {
        if (cnBtn) cnBtn.style.display = 'none';
        return;
    }

    var canAccess = canAccessChuyenNganh();

    var subGrid = $('dsSubGrid');
    if (subGrid) {
        subGrid.innerHTML = '';
        chuyenNganhKeys.forEach(function(id) {
            var ds = DATASET_REGISTRY[id];

            var btn = document.createElement('button');
            btn.className = 'ds-sub-btn' + (canAccess ? '' : ' locked');
            btn.dataset.dataset = ds.id;
            btn.dataset.locked = canAccess ? '0' : '1';
            btn.style.setProperty('--ds-color', ds.color || '#64748b');
            btn.title = ds.name + ' (' + ds.count + ' câu)' +
                        (canAccess ? '' : ' - Cần gia hạn để mở khoá');

            var icon = document.createElement('i');
            icon.className = 'fas ' + (ds.icon || 'fa-folder');
            btn.appendChild(icon);

            var nameSpan = document.createElement('span');
            nameSpan.textContent = ds.name.normalize ? ds.name.normalize('NFC') : ds.name;
            btn.appendChild(nameSpan);

            if (!canAccess) {
                var lock = document.createElement('i');
                lock.className = 'fas fa-lock ds-sub-lock';
                btn.appendChild(lock);
            }

            subGrid.appendChild(btn);
        });
    }

    if (cnBtn) {
        var oldLock = cnBtn.querySelector('.ds-main-lock');
        if (oldLock) oldLock.remove();

        if (!canAccess) {
            var span = cnBtn.querySelector('span');
            if (span) {
                span.insertAdjacentHTML('afterend',
                    '<i class="fas fa-lock ds-main-lock"></i>');
            }
            cnBtn.classList.add('has-lock');
            cnBtn.title = 'Cần đăng nhập + gia hạn để mở khoá chuyên ngành';
        } else {
            cnBtn.classList.remove('has-lock');
            cnBtn.title = 'Chọn chuyên ngành';
        }
    }

    /* ═══════════════════════════════════════════════════════════
       NÚT TỔNG HỢP — Click để về tab tổng hợp
       ═══════════════════════════════════════════════════════════ */
    document.querySelectorAll('.ds-btn[data-dataset="tonghop"]').forEach(function(btn) {
        if (btn.__boundDataset) return;
        btn.__boundDataset = true;
        btn.addEventListener('click', function() {
            switchDataset('tonghop');
            var sub = $('dsSubWrap');
            if (sub) sub.style.display = 'none';

            /* Bỏ active TẤT CẢ tab */
            document.querySelectorAll('.ds-btn').forEach(function(b) {
                b.classList.remove('active');
            });
            btn.classList.add('active');
        });
    });

    /* ═══════════════════════════════════════════════════════════
       NÚT CHUYÊN NGÀNH — Click để mở/đóng dropdown
       Khi mở → bỏ active TẤT CẢ tab khác (Tổng hợp + Yêu thích)
       ═══════════════════════════════════════════════════════════ */
    if (cnBtn && !cnBtn.__boundToggle) {
        cnBtn.__boundToggle = true;
        cnBtn.addEventListener('click', function() {
            var sub = $('dsSubWrap');
            if (!sub) return;
            var isOpen = sub.style.display !== 'none';
            if (isOpen) {
                /* Đóng dropdown → bỏ active nút CN */
                sub.style.display = 'none';
                cnBtn.classList.remove('active');
            } else {
                /* Mở dropdown → active nút CN, bỏ active TẤT CẢ tab khác */
                sub.style.display = 'block';

                document.querySelectorAll('.ds-btn').forEach(function(b) {
                    b.classList.remove('active');
                });
                cnBtn.classList.add('active');
            }
        });
    }

    /* ═══════════════════════════════════════════════════════════
       SUB-BUTTONS CHUYÊN NGÀNH — Click để chuyển dataset
       ═══════════════════════════════════════════════════════════ */
    document.querySelectorAll('.ds-sub-btn').forEach(function(btn) {
        if (btn.__boundSub) return;
        btn.__boundSub = true;
        btn.addEventListener('click', function(e) {
            if (this.dataset.locked === '1') {
                e.preventDefault();
                e.stopPropagation();
                showChuyenNganhLockMessage();
                return;
            }
            var id = this.dataset.dataset;
            document.querySelectorAll('.ds-sub-btn').forEach(function(b) {
                b.classList.remove('active');
            });
            this.classList.add('active');
            switchDataset(id);

            /* Bỏ active TẤT CẢ tab chính, chỉ giữ nút CN active */
            document.querySelectorAll('.ds-btn').forEach(function(b) {
                b.classList.remove('active');
            });
            if (cnBtn) cnBtn.classList.add('active');
        });
    });

    markCurrentDatasetActive();
}
function markCurrentDatasetActive() {
    var current = (typeof CURRENT_DATASET !== 'undefined') ? CURRENT_DATASET : 'tonghop';
    document.querySelectorAll('.ds-sub-btn').forEach(function(b) {
        b.classList.toggle('active', b.dataset.dataset === current);
    });
    document.querySelectorAll('.ds-btn[data-dataset="tonghop"]').forEach(function(b) {
        b.classList.toggle('active', current === 'tonghop');
    });
    if (current !== 'tonghop') {
        var wrap = $('dsSubWrap');
        if (wrap) wrap.style.display = 'block';
        document.querySelectorAll('.ds-btn[data-dataset-group="chuyen-nganh"]').forEach(function(b) {
            b.classList.add('active');
        });
    }
}

function switchDataset(datasetId) {
    if (!DATASET_REGISTRY[datasetId]) return;

    /* ❤️ Nếu rời tab Yêu thích → reset cờ */
    if (typeof favState !== 'undefined' && favState.currentView) {
        favState.currentView = false;
    }

    if (datasetId !== 'tonghop' && !canAccessChuyenNganh()) {
        showChuyenNganhLockMessage();
        return;
    }

    if (typeof window.__switchRawData === 'function') {
        window.__switchRawData(datasetId);
    }

    window.__onboardingOverride = null;

    state = { search:'', hsk:'', subject:'' };
    if ($('searchInput')) $('searchInput').value = '';
    if ($('hskFilter')) $('hskFilter').value = '';
    if ($('subjectFilter')) $('subjectFilter').value = '';

    buildFilters();
    applyFilter();
    updateResultCount();

    if ($('fabGroup')) $('fabGroup').classList.remove('open');

    /* ❤️ Cập nhật lock state cho tab (bao gồm tab Yêu thích) */
    if (typeof favUpdateLockState === 'function') favUpdateLockState();

    /* Khôi phục banner chủ đề sau khi đổi dataset */
    var saved = loadOnboardingSelection();
    if (saved && Array.isArray(saved.topics) && saved.topics.length > 0) {
        var cfg = getOnboardingConfig();
        if (cfg) {
            if (datasetId === 'tonghop') {
                window.__onboardingAutoPicked = !!saved.auto_picked;
                applyOnboardingSelection(saved.topics, false);
            }
        }
    }
}

/* ============================================================ */
/* VOICE SETTINGS                                                */
/* ============================================================ */
var voiceState = {
    rate: 1.0,
    pitch: 1.0,
    volume: 1.0,
    voiceURI: ''
};

var DEFAULT_VOICE = { rate: 1.0, pitch: 1.0, volume: 1.0, voiceURI: '' };

function loadVoiceSettings() {
    try {
        var saved = JSON.parse(localStorage.getItem('voiceSettings') || 'null');
        if (saved && typeof saved === 'object') {
            if (typeof saved.rate === 'number')   voiceState.rate   = Math.max(0.5, Math.min(1.5, saved.rate));
            if (typeof saved.pitch === 'number')  voiceState.pitch  = Math.max(0.5, Math.min(1.5, saved.pitch));
            if (typeof saved.volume === 'number') voiceState.volume = Math.max(0,   Math.min(1,   saved.volume));
            if (typeof saved.voiceURI === 'string') voiceState.voiceURI = saved.voiceURI;
        }
    } catch(e) {}
}

function saveVoiceSettings() {
    try { localStorage.setItem('voiceSettings', JSON.stringify(voiceState)); } catch(e) {}
}

function applyVoiceSettings(utterance) {
    if (!utterance) return;
    utterance.rate   = voiceState.rate;
    utterance.pitch  = voiceState.pitch;
    utterance.volume = voiceState.volume;
    var v = pickVoice();
    if (v) utterance.voice = v;
}

function pickVoice() {
    if (!('speechSynthesis' in window)) return null;
    var voices = speechSynthesis.getVoices();
    if (!voices.length) return null;

    if (voiceState && voiceState.voiceURI) {
        var chosen = voices.find(function(v) { return v.voiceURI === voiceState.voiceURI; });
        if (chosen) return chosen;
    }

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

function getChineseVoice() { return pickVoice(); }

/* ============================================================ */
/* TIER HELPERS — EXPIRED DÙNG Y HỆT DEMO                        */
/* ============================================================ */
function getTierInfo() {
    if (typeof window.APP_TIER !== 'undefined' && window.APP_LIMITS) {
        var tier = window.APP_TIER;
        var maxQ = window.APP_LIMITS.maxQuestions;
        var maxH = window.APP_LIMITS.maxHSK;

        if (tier === 'expired') {
            if (!maxQ || maxQ <= 0) {
                maxQ = (typeof DEMO_LIMIT === 'number') ? DEMO_LIMIT : 60;
            }
            if (!maxH || maxH <= 0) {
                maxH = (typeof DEMO_HSK_MAX === 'number') ? DEMO_HSK_MAX : 3;
            }
        }

        return {
            tier: tier,
            maxQuestions: maxQ,
            maxHSK: maxH,
            unlimitedWriting: !!window.APP_LIMITS.unlimitedWriting,
            isTrial: !!window.APP_LIMITS.isTrial,
            email: window.APP_LIMITS.email
        };
    }
    return {
        tier: 'demo',
        maxQuestions: (typeof DEMO_LIMIT === 'number') ? DEMO_LIMIT : 60,
        maxHSK: (typeof DEMO_HSK_MAX === 'number') ? DEMO_HSK_MAX : 3,
        unlimitedWriting: false,
        isTrial: false,
        email: null
    };
}

function isDemoTier()   { return getTierInfo().tier === 'demo'; }
function isTrialTier()  { return getTierInfo().tier === 'trial'; }
function isActiveTier() { return getTierInfo().tier === 'active'; }
function isExpiredTier(){ return getTierInfo().tier === 'expired'; }
function isLimitedTier(){ var t = getTierInfo().tier; return t === 'demo' || t === 'trial' || t === 'expired'; }

/* ═══════════════════════════════════════════════════════════ */
/* MỚI: TÍNH SỐ CÂU TỐI ĐA MỖI CHỦ ĐỀ                          */
/* Công thức: ceil(limit / tổng_số_chủ_đề_trong_kho)            */
/* ═══════════════════════════════════════════════════════════ */
function getMaxPerTopic(limit, poolData) {
    var subjectSet = {};
    (poolData || RAW_DATA).forEach(function(r) {
        var s = (r.subject || '').trim();
        if (s) subjectSet[s] = 1;
    });
    var totalTopics = Object.keys(subjectSet).length;
    if (totalTopics === 0) return 1;
    if (!limit || limit <= 0) return 1;
    return Math.max(1, Math.ceil(limit / totalTopics));
}

/* ═══════════════════════════════════════════════════════════ */
/* MỚI: TÍNH THỐNG KÊ KHOÁ CHO BANNER                           */
/* ═══════════════════════════════════════════════════════════ */
function computeLockStats(selectedTopics, allowedHsk, maxQ, isUnlimited) {
    var stats = {
        lockedInSelected: 0,
        totalInSelected: 0,
        lockedTopics: 0,
        totalTopics: 0,
        maxPerTopic: 1
    };
    if (!selectedTopics || selectedTopics.length === 0) return stats;

    var allTopicsSet = {};
    RAW_DATA.forEach(function(r) {
        var s = (r.subject || '').trim();
        if (s) allTopicsSet[s] = 1;
    });
    stats.totalTopics = Object.keys(allTopicsSet).length;
    stats.lockedTopics = Math.max(0, stats.totalTopics - selectedTopics.length);

    if (isUnlimited) return stats;
    stats.maxPerTopic = getMaxPerTopic(maxQ, RAW_DATA);

    RAW_DATA.forEach(function(r) {
        var s = (r.subject || '').trim();
        if (selectedTopics.indexOf(s) === -1) return;
        if (allowedHsk && allowedHsk.length > 0 && allowedHsk.indexOf(r.hsk) === -1) return;
        stats.totalInSelected++;
    });

    var canTake = Math.min(selectedTopics.length * stats.maxPerTopic, maxQ);
    canTake = Math.min(canTake, stats.totalInSelected);
    stats.lockedInSelected = Math.max(0, stats.totalInSelected - canTake);
    return stats;
}

/* ═══════════════════════════════════════════════════════════ */
/* SỬA: GET LIMITED DATA — GIỚI HẠN SỐ CÂU MỖI CHỦ ĐỀ           */
/* ═══════════════════════════════════════════════════════════ */
function getLimitedData() {
    if (window.__onboardingOverride && Array.isArray(window.__onboardingOverride)
        && window.__onboardingOverride.length > 0
        && !state.search && !state.hsk && !state.subject) {
        return window.__onboardingOverride;
    }

    var info = getTierInfo();
    if (info.tier === 'active') return RAW_DATA;

    var max = (typeof info.maxQuestions === 'number' && info.maxQuestions > 0)
              ? info.maxQuestions
              : ((typeof DEMO_LIMIT === 'number') ? DEMO_LIMIT : 60);

    var allowedHsk = getAllowedHskList();
    if (!allowedHsk || allowedHsk.length === 0) {
        return RAW_DATA.slice(0, max);
    }

    var poolByHsk = RAW_DATA.filter(function(r) {
        return allowedHsk.indexOf(r.hsk) !== -1;
    });

    var maxPerTopic = getMaxPerTopic(max, RAW_DATA);

    var topicCount = {};
    var result = [];
    var perHsk = Math.ceil(max / allowedHsk.length);
    var hskCount = {};
    allowedHsk.forEach(function(h) { hskCount[h] = 0; });

    for (var i = 0; i < poolByHsk.length && result.length < max; i++) {
        var r = poolByHsk[i];
        var s = (r.subject || '').trim() || '__no_subject__';
        if ((topicCount[s] || 0) >= maxPerTopic) continue;
        if (r.hsk && hskCount[r.hsk] !== undefined && hskCount[r.hsk] >= perHsk) continue;
        result.push(r);
        topicCount[s] = (topicCount[s] || 0) + 1;
        if (r.hsk && hskCount[r.hsk] !== undefined) hskCount[r.hsk]++;
    }

    if (result.length < max) {
        var usedIds = {};
        result.forEach(function(r) { usedIds[r.stt] = true; });
        for (var j = 0; j < poolByHsk.length && result.length < max; j++) {
            var r2 = poolByHsk[j];
            if (usedIds[r2.stt]) continue;
            var s2 = (r2.subject || '').trim() || '__no_subject__';
            if ((topicCount[s2] || 0) >= maxPerTopic) continue;
            result.push(r2);
            usedIds[r2.stt] = true;
            topicCount[s2] = (topicCount[s2] || 0) + 1;
        }
    }

    return result;
}

function getAllowedHskList() {
    var info = getTierInfo();
    var max = info.maxHSK;
    if (max === Infinity || max >= 6 || info.tier === 'active') {
        return ['HSK1','HSK2','HSK3','HSK4','HSK5','HSK6','HSK7-9'];
    }
    var list = [];
    for (var i = 1; i <= max; i++) list.push('HSK' + i);
    return list;
}

function getAllowedSubjectList() {
    var info = getTierInfo();
    if (info.tier === 'active') {
        var set = {};
        RAW_DATA.forEach(function(r) { if (r.subject) set[r.subject] = 1; });
        return Object.keys(set).sort();
    }
    var set2 = {};
    getLimitedData().forEach(function(r) { if (r.subject) set2[r.subject] = 1; });
    return Object.keys(set2).sort();
}

function shouldCountUsage() {
    var t = getTierInfo().tier;
    return t === 'demo' || t === 'expired';
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
    if (!shouldCountUsage()) return;
    try {
        var today = new Date().toDateString();
        var data = JSON.parse(localStorage.getItem('demo_usage') || '{}');
        if (data.date !== today) data = { date: today, count: 0 };
        data.count++;
        localStorage.setItem('demo_usage', JSON.stringify(data));
    } catch(e) {}
}

function getDemoRemaining() {
    if (!shouldCountUsage()) return Infinity;
    return Math.max(0, DEMO_DAILY_LIMIT - getDemoUsage());
}

function canUseFeature() {
    var info = getTierInfo();
    if (info.tier === 'expired') return getDemoUsage() < DEMO_DAILY_LIMIT;
    if (info.tier === 'demo') return getDemoUsage() < DEMO_DAILY_LIMIT;
    return true;
}

function updateDemoRemaining() {
    var el = $('demoRemainingText');
    if (!el) return;
    if (!shouldCountUsage()) return;
    var remaining = getDemoRemaining();
    el.textContent = remaining;
    if (remaining < 20) el.style.color = '#dc2626';
    else if (remaining < 50) el.style.color = '#f59e0b';
    else el.style.color = '#16a34a';
}

function showLimitMessage() {
    var info = getTierInfo();
    if (info.tier === 'expired') {
        if (confirm('Bạn đã dùng hết ' + DEMO_DAILY_LIMIT + ' lượt miễn phí hôm nay.\n\n' +
                    '(Tài khoản đã hết hạn — đang dùng chế độ Demo)\n\n' +
                    'Gia hạn để dùng KHÔNG GIỚI HẠN!')) {
            if (typeof openRenewalModal === 'function') openRenewalModal();
        }
        return;
    }
    if (info.tier === 'demo') {
        if (confirm('Bạn đã dùng hết ' + DEMO_DAILY_LIMIT + ' lượt miễn phí hôm nay.\n\n' +
                    '(Bao gồm NGHE và LUYỆN VIẾT)\n\n' +
                    'Đăng nhập Google để dùng KHÔNG GIỚI HẠN!')) {
            if (typeof showLoginModal === 'function') showLoginModal();
        }
        return;
    }
}

/* ============================================================ */
/* UTILS                                                         */
/* ============================================================ */
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

/* ============================================================ */
/* TAG CLICKABLE                                                 */
/* ============================================================ */
window.searchByTag = function(evt, type, value) {
    if (evt) {
        evt.stopPropagation();
        if (evt.preventDefault) evt.preventDefault();
    }
    if (!value) return;

    var searchInput = $('searchInput');
    if (!searchInput) return;

    var pfModal = $('practiceFullModal');
    if (pfModal && pfModal.classList.contains('show')) {
        if (typeof closePracticeFull === 'function') closePracticeFull();
    }

    if ($('hskFilter')) $('hskFilter').value = '';
    if ($('subjectFilter')) $('subjectFilter').value = '';

    window.__onboardingOverride = null;
    var obBanner = $('onboardingActiveBanner');
    if (obBanner) obBanner.remove();

    searchInput.value = value;

    state.search = value.toLowerCase().trim();
    state.hsk = '';
    state.subject = '';

    renderedCount = 0;
    applyFilter();

    var mainEl = $('mainContent');
    if (mainEl) {
        var yOffset = mainEl.getBoundingClientRect().top + window.scrollY - 100;
        window.scrollTo({ top: yOffset, behavior: 'smooth' });
    }

    setTimeout(function() {
        searchInput.focus();
        try { searchInput.setSelectionRange(0, searchInput.value.length); } catch(e) {}
    }, 300);

    var clearBtn = $('clearSearchBtn');
    if (clearBtn) clearBtn.classList.add('show');

    var label = type === 'topic' ? 'chủ điểm' : 'chủ đề';
    showTagToast('Đang lọc theo ' + label + ': "' + value + '"');
};

function showTagToast(message) {
    var old = document.getElementById('tagToast');
    if (old) old.remove();

    var toast = document.createElement('div');
    toast.id = 'tagToast';
    toast.textContent = message;
    toast.style.cssText = [
        'position:fixed','top:80px','left:50%',
        'transform:translateX(-50%) translateY(-20px)',
        'padding:.7rem 1.2rem',
        'background:linear-gradient(135deg,#4f46e5,#7c3aed)',
        'color:#fff','border-radius:50px',
        'font-size:.85rem','font-weight:700','font-family:inherit',
        'box-shadow:0 8px 24px rgba(124,58,237,.45)',
        'z-index:9999','opacity:0',
        'transition:opacity .25s ease, transform .3s cubic-bezier(.34,1.56,.64,1)',
        'pointer-events:none','max-width:90vw',
        'text-overflow:ellipsis','overflow:hidden','white-space:nowrap'
    ].join(';');

    document.body.appendChild(toast);

    requestAnimationFrame(function() {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(-50%) translateY(0)';
    });

    setTimeout(function() {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(-50%) translateY(-20px)';
        setTimeout(function() { if (toast.parentNode) toast.remove(); }, 300);
    }, 2000);
}

/* ═══════════════════════════════════════════════════════════ */
/* ONBOARDING - CHỌN CHỦ ĐỀ QUAN TÂM                             */
/* EXPIRED dùng config giống DEMO                                */
/* ═══════════════════════════════════════════════════════════ */
var _onboardingSelected = {};
var _onboardingConfig = null;

function getOnboardingConfig() {
    if (typeof ONBOARDING_CONFIG === 'undefined' || !ONBOARDING_CONFIG) return null;

    var info = getTierInfo();
    var tier = info.tier;

    var configKey = tier;
    if (tier === 'expired') configKey = 'demo';

    if (configKey !== 'demo' && configKey !== 'trial' && configKey !== 'active') return null;

    var cfg = ONBOARDING_CONFIG[configKey];
    if (!cfg) return null;
    if (cfg.enabled === false) return null;

    if (typeof cfg.topics_per_user !== 'number') cfg.topics_per_user = -1;
    if (typeof cfg.max_questions   !== 'number') cfg.max_questions   = -1;
    if (!Array.isArray(cfg.hsk_allowed) || cfg.hsk_allowed.length === 0) {
        cfg.hsk_allowed = [1, 2, 3, 4, 5, 6];
    }

    return cfg;
}

function getOnboardingStorageKey() {
    var info = getTierInfo();
    if (info.tier === 'demo') return 'onboarding_demo';
    if (info.tier === 'trial' && info.email)  return 'onboarding_trial_' + info.email;
    if (info.tier === 'active' && info.email) return 'onboarding_active_' + info.email;
    if (info.tier === 'active') return 'onboarding_active_guest';
    if (info.tier === 'expired' && info.email) return 'onboarding_expired_' + info.email;
    if (info.tier === 'expired') return 'onboarding_expired_guest';
    return null;
}

function getAvailableTopicsForTier() {
    var info = getTierInfo();
    var allowedHsk = getAllowedHskList();

    var subjectMap = {};
    RAW_DATA.forEach(function(r) {
        if (info.tier !== 'active' && allowedHsk.indexOf(r.hsk) === -1) return;
        var s = (r.subject || '').trim();
        if (!s) return;
        subjectMap[s] = (subjectMap[s] || 0) + 1;
    });

    var list = Object.keys(subjectMap).map(function(name) {
        return { name: name, count: subjectMap[name] };
    });
    list.sort(function(a, b) { return b.count - a.count; });
    return list;
}

function loadOnboardingSelection() {
    var key = getOnboardingStorageKey();
    if (!key) return null;
    try {
        var saved = JSON.parse(localStorage.getItem(key) || 'null');
        if (saved && Array.isArray(saved.topics) && saved.topics.length > 0) {
            return saved;
        }
    } catch(e) {}
    return null;
}
function saveOnboardingSelection(topics, autoPicked) {
    var key = getOnboardingStorageKey();
    if (!key) return;
    try {
        localStorage.setItem(key, JSON.stringify({
            topics: topics,
            auto_picked: !!autoPicked,
            savedAt: Date.now()
        }));
    } catch(e) {}
}

/* ═══════════════════════════════════════════════════════════ */
/* SỬA: MAYBE SHOW ONBOARDING — LUÔN VẼ BANNER NẾU CÓ SELECTION */
/* ═══════════════════════════════════════════════════════════ */
function maybeShowOnboarding() {
    var info = getTierInfo();

    if (info.tier !== 'demo' && info.tier !== 'trial'
        && info.tier !== 'active' && info.tier !== 'expired') {
        return;
    }

    var cfg = getOnboardingConfig();
    if (!cfg) return;

    var mainContent = $('mainContent');
    if (!mainContent || mainContent.style.display === 'none') {
        setTimeout(maybeShowOnboarding, 300);
        return;
    }

    if (typeof RAW_DATA === 'undefined' || !RAW_DATA || RAW_DATA.length === 0) {
        setTimeout(maybeShowOnboarding, 300);
        return;
    }

    var saved = loadOnboardingSelection();
    if (saved && Array.isArray(saved.topics) && saved.topics.length > 0) {
        window.__onboardingAutoPicked = !!saved.auto_picked;

        var existingBanner = $('onboardingActiveBanner');
        var override = window.__onboardingOverride;

        if (!existingBanner || !override || override.length === 0) {
            applyOnboardingSelection(saved.topics, false);
        } else {
            showOnboardingActiveBanner(saved.topics, override.length);
        }
        return;
    }

    // ⬇️ THÊM: Nếu đã có banner (rỗng) thì không hiện modal
    var existingBanner2 = $('onboardingActiveBanner');
    if (existingBanner2) {
        return;
    }

    showOnboardingModal();
}

function showOnboardingModal() {
    var cfg = getOnboardingConfig();
    if (!cfg) return;

    _onboardingConfig = cfg;

    var saved = loadOnboardingSelection();
    if (saved && Array.isArray(saved.topics)) {
        _onboardingSelected = {};
        saved.topics.forEach(function(t) { _onboardingSelected[t] = true; });
    } else {
        _onboardingSelected = {};
    }

    var titleEl = $('onboardingTitle');
    var subtitleEl = $('onboardingSubtitle');
    if (titleEl) titleEl.textContent = cfg.title || 'Bạn quan tâm chủ đề nào?';
    if (subtitleEl) subtitleEl.textContent = cfg.subtitle || '';

    renderOnboardingTopics();
    updateOnboardingUI();

    var modal = $('onboardingModal');
    if (modal) modal.classList.add('show');
}

function renderOnboardingTopics() {
    var container = $('onboardingTopics');
    if (!container) return;

    var topics = getAvailableTopicsForTier();
    if (topics.length === 0) {
        container.innerHTML = '<div class="onboarding-empty">' +
            '<i class="fas fa-inbox"></i> Chưa có chủ đề nào trong kho</div>';
        return;
    }

    var cfg = getOnboardingConfig();
    var isUnlimited = !cfg || cfg.max_questions === -1 || cfg.max_questions === Infinity;
    var maxQ = (cfg && cfg.max_questions > 0) ? cfg.max_questions : getTierInfo().maxQuestions;

    var allowedHsk;
    if (cfg && cfg.hsk_allowed && cfg.hsk_allowed.length > 0) {
        allowedHsk = cfg.hsk_allowed.map(function(n) { return 'HSK' + n; });
    } else {
        allowedHsk = getAllowedHskList();
    }

    // ⭐ Mở 50% số chủ đề (hardcode 0.5)
    var UNLOCK_RATIO = 0.5;

    var allTopicsFirstStt = {};
    RAW_DATA.forEach(function(r) {
        if (allowedHsk.indexOf(r.hsk) === -1) return;
        var s = (r.subject || '').trim();
        if (!s) return;
        var stt = parseInt(r.stt);
        if (isNaN(stt)) stt = 999999;
        if (allTopicsFirstStt[s] === undefined || stt < allTopicsFirstStt[s]) {
            allTopicsFirstStt[s] = stt;
        }
    });
    var allTopicsList = Object.keys(allTopicsFirstStt);
    var unlockedCount = Math.floor(allTopicsList.length * UNLOCK_RATIO);
    if (unlockedCount < 1 && allTopicsList.length > 0) unlockedCount = 1;

    var sortedAllTopics = allTopicsList.slice().sort(function(a, b) {
        return (allTopicsFirstStt[a] || 0) - (allTopicsFirstStt[b] || 0);
    });
    var unlockedTopics = sortedAllTopics.slice(0, unlockedCount);

    var maxPerTopic = isUnlimited ? Infinity :
                      Math.max(1, Math.ceil(maxQ / Math.max(1, unlockedCount)));

    container.innerHTML = '';
    topics.forEach(function(t) {
        var isUnlocked = isUnlimited || (unlockedTopics.indexOf(t.name) !== -1);
        var lockedInTopic = 0;
        if (isUnlocked && !isUnlimited && t.count > maxPerTopic) {
            lockedInTopic = t.count - maxPerTopic;
        }

        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'onboarding-topic' + (_onboardingSelected[t.name] ? ' selected' : '');
        btn.dataset.topic = t.name;

        if (!isUnlocked) {
            btn.classList.add('disabled');
            btn.disabled = true;
            btn.title = t.name + '\n🔒 Chủ đề này bị khoá\n(Không nằm trong ' +
                        unlockedCount + '/' + allTopicsList.length + ' chủ đề được mở)';

            var nameSpan = document.createElement('span');
            nameSpan.textContent = t.name.normalize ? t.name.normalize('NFC') : t.name;
            btn.appendChild(nameSpan);

            var lockCountSpan = document.createElement('span');
            lockCountSpan.className = 'count';
            lockCountSpan.innerHTML = '<i class="fas fa-lock" style="font-size:.7em"></i>';
            btn.appendChild(lockCountSpan);
        } else {
            btn.title = t.name + '\nTổng: ' + t.count + ' câu' +
                        (lockedInTopic > 0
                            ? '\n🔒 Còn ' + lockedInTopic + ' câu bị khoá (chỉ lấy tối đa ' + maxPerTopic + ' câu)'
                            : '');

            var nameSpan2 = document.createElement('span');
            nameSpan2.textContent = t.name.normalize ? t.name.normalize('NFC') : t.name;
            btn.appendChild(nameSpan2);

            var countSpan = document.createElement('span');
            countSpan.className = 'count';
            countSpan.textContent = t.count;
            btn.appendChild(countSpan);

            if (lockedInTopic > 0) {
                var lockSpan = document.createElement('span');
                lockSpan.className = 'topic-lock';
                lockSpan.innerHTML = '<i class="fas fa-lock"></i>' + lockedInTopic;
                btn.appendChild(lockSpan);
            }

            btn.addEventListener('click', function() {
                onToggleOnboardingTopic(this.dataset.topic);
            });
        }

        container.appendChild(btn);
    });
}

function onToggleOnboardingTopic(topicName) {
    if (!_onboardingConfig) return;
    var max = _onboardingConfig.topics_per_user;
    var isUnlimited = (max === -1 || max === Infinity);

    if (_onboardingSelected[topicName]) {
        delete _onboardingSelected[topicName];
    } else {
        var currentCount = Object.keys(_onboardingSelected).length;
        if (!isUnlimited && currentCount >= max) {
            showTagToast('Chỉ được chọn tối đa ' + max + ' chủ đề');
            return;
        }
        _onboardingSelected[topicName] = true;
    }

    var btn = null;
    document.querySelectorAll('.onboarding-topic').forEach(function(b) {
        if (b.dataset.topic === topicName) btn = b;
    });
    if (btn) btn.classList.toggle('selected', !!_onboardingSelected[topicName]);
    updateOnboardingUI();
}

function updateOnboardingUI() {
    if (!_onboardingConfig) return;
    var selected = Object.keys(_onboardingSelected).length;
    var max = _onboardingConfig.topics_per_user;
    var isUnlimited = (max === -1 || max === Infinity);

    var countEl = $('onboardingSelectedCount');
    if (countEl) countEl.textContent = selected;

    var counter = $('onboardingCounter');
    if (counter) {
        counter.classList.remove('ok', 'full');
        if (selected > 0) counter.classList.add('ok');
        if (!isUnlimited && selected >= max) counter.classList.add('full');

        var labelSpan = counter.querySelector('span');
        if (labelSpan) {
            if (isUnlimited) {
                labelSpan.innerHTML = 'Đã chọn <b id="onboardingSelectedCount">'
                    + selected + '</b> chủ đề (không giới hạn)';
            } else {
                labelSpan.innerHTML = 'Đã chọn <b id="onboardingSelectedCount">'
                    + selected + '</b> / <b id="onboardingMaxCount">'
                    + max + '</b>';
            }
        }
    }

    var startBtn = $('onboardingStartBtn');
    if (startBtn) startBtn.disabled = (selected === 0);
}

function onOnboardingStart() {
    var topics = Object.keys(_onboardingSelected);
    if (topics.length === 0) return;

    window.__onboardingAutoPicked = false;
    saveOnboardingSelection(topics, false);

    var modal = $('onboardingModal');
    if (modal) modal.classList.remove('show');

    applyOnboardingSelection(topics, true);
}

/* ═══════════════════════════════════════════════════════════ */
/* SỬA: ON ONBOARDING SKIP — GIỮ SELECTION CŨ NẾU CÓ            */
/* ═══════════════════════════════════════════════════════════ */
function onOnboardingSkip() {
    var modal = $('onboardingModal');
    if (modal) modal.classList.remove('show');

    var cfg = getOnboardingConfig();
    if (!cfg) return;

    var selectedCount = Object.keys(_onboardingSelected).length;

    // ═══════════════════════════════════════════════════════════
    // ĐÃ CHỌN → xóa hết chủ đề, banner hiện thông báo "chưa chọn"
    // CHƯA CHỌN → auto chọn (random cho demo/expired/trial, tất cả cho active/admin)
    // ═══════════════════════════════════════════════════════════
    if (selectedCount > 0) {
        // Đã chọn → xóa hết
        _onboardingSelected = {};
        window.__onboardingOverride = null;
        window.__onboardingAutoPicked = false;

        // Xóa selection đã lưu trong localStorage
        var key = getOnboardingStorageKey();
        if (key) {
            try {
                localStorage.setItem(key, JSON.stringify({
                    topics: [],
                    auto_picked: false,
                    savedAt: Date.now()
                }));
            } catch(e) {}
        }

        // Reload data đầy đủ theo tier (không bị giới hạn chủ đề nữa)
        state = { search:'', hsk:'', subject:'' };
        if ($('searchInput')) $('searchInput').value = '';
        if ($('hskFilter')) $('hskFilter').value = '';
        if ($('subjectFilter')) $('subjectFilter').value = '';
        if ($('clearSearchBtn')) $('clearSearchBtn').classList.remove('show');

        filtered = getLimitedData();
        renderedCount = 0;
        render(true);
        updateResultCount();

        // ⬇️ VẼ BANNER TRỐNG thay vì xóa banner
        showEmptyOnboardingBanner();

        showTagToast('Đã bỏ chọn tất cả chủ đề');
        return;
    }

    // Chưa chọn gì → auto chọn như cũ
    var allTopics = getAvailableTopicsForTier();
    if (allTopics.length === 0) return;

    var info = getTierInfo();
    var isLimitedTier = (info.tier === 'demo'
                      || info.tier === 'expired'
                      || info.tier === 'trial');

    var pickedTopics;
    var isUnlimited;

    if (isLimitedTier) {
        var max = (cfg.topics_per_user > 0) ? cfg.topics_per_user : 3;
        var pickCount = Math.min(max, allTopics.length);

        var shuffled = allTopics.slice();
        for (var i = shuffled.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1));
            var t = shuffled[i]; shuffled[i] = shuffled[j]; shuffled[j] = t;
        }
        pickedTopics = shuffled.slice(0, pickCount).map(function(t) { return t.name; });
        isUnlimited = false;
    } else {
        pickedTopics = allTopics.map(function(t) { return t.name; });
        isUnlimited = true;
    }

    window.__onboardingAutoPicked = true;
    saveOnboardingSelection(pickedTopics, true);
    applyOnboardingSelection(pickedTopics, true);

    if (isUnlimited) {
        showTagToast('Đã chọn tất cả ' + pickedTopics.length + ' chủ đề');
    } else {
        showTagToast('Đã gợi ý ' + pickedTopics.length + ' chủ đề phù hợp cho bạn');
    }
}
function showEmptyOnboardingBanner() {
    var old = $('onboardingActiveBanner');
    if (old) old.remove();

    var mainContent = $('mainContent');
    if (!mainContent) return;
    var container = mainContent.querySelector('.container');
    if (!container) return;
    if (mainContent.style.display === 'none') return;

    var banner = document.createElement('div');
    banner.id = 'onboardingActiveBanner';
    banner.className = 'onboarding-active-banner';

    var iconSpan = document.createElement('span');
    iconSpan.className = 'ob-icon';
    iconSpan.innerHTML = '<i class="fas fa-circle-info"></i>';
    banner.appendChild(iconSpan);

    var labelSpan = document.createElement('span');
    labelSpan.className = 'ob-label';
    labelSpan.textContent = 'Bạn chưa chọn chủ đề nào';
    banner.appendChild(labelSpan);

    var chipsWrap = document.createElement('span');
    chipsWrap.className = 'ob-chips';
    var hint = document.createElement('span');
    hint.className = 'ob-chip';
    hint.style.background = 'linear-gradient(135deg, #94a3b8, #64748b)';
    hint.textContent = 'Chọn chủ đề để được gợi ý câu phù hợp';
    chipsWrap.appendChild(hint);
    banner.appendChild(chipsWrap);

    var changeBtn = document.createElement('button');
    changeBtn.type = 'button';
    changeBtn.className = 'ob-change-btn';
    changeBtn.innerHTML = '<i class="fas fa-plus"></i> Chọn chủ đề';
    changeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        // Xóa key để mở modal ở trạng thái "chưa chọn"
        var key = getOnboardingStorageKey();
        if (key) { try { localStorage.removeItem(key); } catch(e) {} }
        onChangeTopicsClick();
    });
    banner.appendChild(changeBtn);

    container.insertBefore(banner, container.firstChild);
}
/* ═══════════════════════════════════════════════════════════ */
/* SỬA: APPLY ONBOARDING SELECTION — GIỚI HẠN MỖI CHỦ ĐỀ       */
/* ═══════════════════════════════════════════════════════════ */
function applyOnboardingSelection(topics, scrollTop) {
    var cfg = getOnboardingConfig();
    if (!cfg) return;

    var maxQ = cfg.max_questions;
    var isUnlimitedQ = (maxQ === -1 || maxQ === Infinity);

    // ⭐ HSK từ config
    var allowedHsk;
    if (cfg.hsk_allowed && Array.isArray(cfg.hsk_allowed) && cfg.hsk_allowed.length > 0) {
        allowedHsk = cfg.hsk_allowed.map(function(n) { return 'HSK' + n; });
    } else {
        allowedHsk = getAllowedHskList();
    }

    // ⭐ Mở 50% số chủ đề (hardcode 0.5)
    var UNLOCK_RATIO = 0.5;

    // ⭐ Bước 1: Lấy TẤT CẢ chủ đề (theo HSK config)
    var allTopicsFirstStt = {};
    RAW_DATA.forEach(function(r) {
        if (allowedHsk.indexOf(r.hsk) === -1) return;
        var s = (r.subject || '').trim();
        if (!s) return;
        var stt = parseInt(r.stt);
        if (isNaN(stt)) stt = 999999;
        if (allTopicsFirstStt[s] === undefined || stt < allTopicsFirstStt[s]) {
            allTopicsFirstStt[s] = stt;
        }
    });
    var allTopicsList = Object.keys(allTopicsFirstStt);
    var totalTopicsCount = allTopicsList.length;

    // ⭐ Bước 2: Mở floor(N × 0.5) chủ đề (theo STT nhỏ nhất)
    var unlockedCount = Math.floor(totalTopicsCount * UNLOCK_RATIO);
    if (unlockedCount < 1 && totalTopicsCount > 0) unlockedCount = 1;

    var sortedAllTopics = allTopicsList.slice().sort(function(a, b) {
        return (allTopicsFirstStt[a] || 0) - (allTopicsFirstStt[b] || 0);
    });
    var unlockedTopics = sortedAllTopics.slice(0, unlockedCount);

    // ⭐ Bước 3: Lọc pool
    var pool = RAW_DATA.filter(function(r) {
        if (allowedHsk.indexOf(r.hsk) === -1) return false;
        var s = (r.subject || '').trim();
        if (topics.indexOf(s) === -1) return false;
        if (unlockedTopics.indexOf(s) === -1) return false;
        return true;
    });

    pool.sort(function(a, b) {
        return (parseInt(a.stt) || 0) - (parseInt(b.stt) || 0);
    });

    var final = [];
    if (isUnlimitedQ) {
        final = pool.slice();
    } else {
        var maxPerTopic = Math.max(1, Math.ceil(maxQ / Math.max(1, unlockedCount)));
        var perHsk = Math.ceil(maxQ / allowedHsk.length);

        var topicCount = {};
        var hskCount = {};
        allowedHsk.forEach(function(h) { hskCount[h] = 0; });

        for (var i = 0; i < pool.length && final.length < maxQ; i++) {
            var r = pool[i];
            var s = (r.subject || '').trim() || '__no_subject__';
            if ((topicCount[s] || 0) >= maxPerTopic) continue;
            if (r.hsk && hskCount[r.hsk] !== undefined && hskCount[r.hsk] >= perHsk) continue;
            final.push(r);
            topicCount[s] = (topicCount[s] || 0) + 1;
            if (r.hsk && hskCount[r.hsk] !== undefined) hskCount[r.hsk]++;
        }

        if (final.length < maxQ) {
            var usedIds = {};
            final.forEach(function(r) { usedIds[r.stt] = true; });
            for (var p = 0; p < pool.length && final.length < maxQ; p++) {
                var rp = pool[p];
                if (usedIds[rp.stt]) continue;
                var sp = (rp.subject || '').trim() || '__no_subject__';
                if ((topicCount[sp] || 0) >= maxPerTopic) continue;
                final.push(rp);
                usedIds[rp.stt] = true;
                topicCount[sp] = (topicCount[sp] || 0) + 1;
            }
        }

        if (final.length > maxQ) final = final.slice(0, maxQ);
    }

    final.sort(function(a, b) {
        return (parseInt(a.stt) || 0) - (parseInt(b.stt) || 0);
    });

    window.__onboardingOverride = final;
    window.__unlockedTopics = unlockedTopics;

    if (typeof state !== 'undefined' && state) {
        state.search = '';
        state.hsk = '';
        state.subject = '';
    }
    try {
        var si = document.getElementById('searchInput');
        if (si) si.value = '';
        var cb = document.getElementById('clearSearchBtn');
        if (cb) cb.classList.remove('show');
    } catch(e) {}

    if (typeof applyFilter === 'function') applyFilter();
    if (typeof updateResultCount === 'function') updateResultCount();

    if (typeof showOnboardingActiveBanner === 'function') {
        showOnboardingActiveBanner(topics, final.length);
    }

    if (scrollTop) {
        setTimeout(function() {
            var mainEl = document.getElementById('mainContent');
            if (mainEl) {
                var yOffset = mainEl.getBoundingClientRect().top + window.scrollY - 100;
                window.scrollTo({ top: yOffset, behavior: 'smooth' });
            }
        }, 200);
    }
}
/* ═══════════════════════════════════════════════════════════ */
/* SỬA: ON CHANGE TOPICS CLICK — KHÔNG XÓA STORAGE NGAY         */
/* ═══════════════════════════════════════════════════════════ */
function onChangeTopicsClick() {
    var cfg = getOnboardingConfig();

    if (!cfg) {
        showTagToast('Không thể đổi chủ đề ở chế độ này');
        return;
    }

    // FIX: KHÔNG xóa localStorage + override ngay.
    // Chỉ mở modal; user bấm "Bắt đầu" / "Bỏ qua" thì mới ghi đè.
    // Nếu user đóng modal (X) mà không chọn → giữ nguyên selection cũ.

    _onboardingConfig = cfg;

    // Load lại selection hiện tại vào _onboardingSelected để hiển thị đúng
    _onboardingSelected = {};
    var saved = loadOnboardingSelection();
    if (saved && Array.isArray(saved.topics)) {
        saved.topics.forEach(function(t) { _onboardingSelected[t] = true; });
    }

    var modal = $('onboardingModal');
    if (modal) modal.classList.remove('show');

    var titleEl = $('onboardingTitle');
    var subtitleEl = $('onboardingSubtitle');
    if (titleEl) titleEl.textContent = cfg.title || 'Bạn quan tâm chủ đề nào?';
    if (subtitleEl) subtitleEl.textContent = cfg.subtitle || '';

    renderOnboardingTopics();
    updateOnboardingUI();

    if (modal) {
        void modal.offsetWidth;
        modal.classList.add('show');
    }
}

/* ═══════════════════════════════════════════════════════════ */
/* SỬA: BANNER — ĐẦY ĐỦ THỐNG KÊ KHOÁ (5 STATS)                 */
/* ═══════════════════════════════════════════════════════════ */
function showOnboardingActiveBanner(topics, count) {
    var old = $('onboardingActiveBanner');
    if (old) old.remove();

    var mainContent = $('mainContent');
    if (!mainContent) return;
    var container = mainContent.querySelector('.container');
    if (!container) return;

    // FIX: Nếu mainContent đang ẩn (chưa init xong), thoát.
    if (mainContent.style.display === 'none') return;

    var info = getTierInfo();
    var totalAvailable = RAW_DATA.length;

    var cfg = getOnboardingConfig();
    var isUnlimitedTier = (info.tier === 'active')
                       || (cfg && (cfg.max_questions === -1 || cfg.max_questions === Infinity));

    var lockedCount = isUnlimitedTier ? 0 : Math.max(0, totalAvailable - count);
    var isLimited = (info.tier !== 'active');

    var lockedIndustryCount = 0;
    if (typeof DATASET_REGISTRY !== 'undefined' && DATASET_REGISTRY) {
        Object.keys(DATASET_REGISTRY).forEach(function(id) {
            if (id === 'tonghop') return;
            if (!canAccessChuyenNganh()) lockedIndustryCount++;
        });
    }

    var allowedHskForStats;
    if (cfg && cfg.hsk_allowed && Array.isArray(cfg.hsk_allowed) && cfg.hsk_allowed.length > 0) {
        allowedHskForStats = cfg.hsk_allowed.map(function(n) { return 'HSK' + n; });
    } else {
        allowedHskForStats = getAllowedHskList();
    }
    var maxQForStats = (cfg && cfg.max_questions > 0) ? cfg.max_questions : info.maxQuestions;
    var lockStats = computeLockStats(topics, allowedHskForStats, maxQForStats, isUnlimitedTier);

    var banner = document.createElement('div');
    banner.id = 'onboardingActiveBanner';
    banner.className = 'onboarding-active-banner';

    var isAuto = !!window.__onboardingAutoPicked;
    var iconHtml = isAuto ? '<i class="fas fa-magic"></i>' : '<i class="fas fa-star"></i>';
    var labelText = isAuto ? 'Chủ đề gợi ý cho bạn:' : 'Chủ đề của bạn:';

    var iconSpan = document.createElement('span');
    iconSpan.className = 'ob-icon';
    iconSpan.innerHTML = iconHtml;
    banner.appendChild(iconSpan);

    var labelSpan = document.createElement('span');
    labelSpan.className = 'ob-label';
    labelSpan.textContent = labelText;
    banner.appendChild(labelSpan);

    var MAX_VISIBLE_CHIPS = 5;
    var visibleTopics = topics.slice(0, MAX_VISIBLE_CHIPS);
    var hiddenCount = Math.max(0, topics.length - MAX_VISIBLE_CHIPS);

    var chipsWrap = document.createElement('span');
    chipsWrap.className = 'ob-chips';

    visibleTopics.forEach(function(t) {
        var chip = document.createElement('span');
        chip.className = 'ob-chip';
        chip.textContent = t.normalize ? t.normalize('NFC') : t;
        chipsWrap.appendChild(chip);
    });

    if (hiddenCount > 0) {
        var moreChip = document.createElement('span');
        moreChip.className = 'ob-chip ob-chip-more';
        moreChip.textContent = '+' + hiddenCount + ' chủ đề khác';
        moreChip.title = topics.join(' · ');
        moreChip.setAttribute('data-tooltip', topics.join(' · '));
        moreChip.style.cursor = 'help';
        chipsWrap.appendChild(moreChip);
    }

    banner.appendChild(chipsWrap);

    var countSpan = document.createElement('span');
    countSpan.className = 'ob-count';
    if (isUnlimitedTier) {
        countSpan.textContent = '(toàn bộ ' + count + ' câu)';
    } else {
        countSpan.textContent = '(' + count + ' câu)';
    }
    banner.appendChild(countSpan);

    var changeBtn = document.createElement('button');
    changeBtn.type = 'button';
    changeBtn.id = 'onboardingChangeBtn';
    changeBtn.className = 'ob-change-btn';
    changeBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Đổi';
    changeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        onChangeTopicsClick();
    });
    banner.appendChild(changeBtn);

    if (isLimited) {
        var statsBar = document.createElement('div');
        statsBar.className = 'ob-stats-bar ob-stats-inline';

        /* STAT 1: Số câu đang có / tổng */
        if (lockedCount > 0) {
            var stat1 = document.createElement('span');
            stat1.className = 'ob-stat-inline';
            stat1.innerHTML =
                '<i class="fas fa-database"></i>' +
                '<b>' + count + '</b>/' + totalAvailable + ' câu';
            statsBar.appendChild(stat1);
        }

        /* STAT 2: Số chủ đề chưa mở khoá */
        if (lockStats.lockedTopics > 0) {
            var stat2 = document.createElement('span');
            stat2.className = 'ob-stat-inline ob-stat-inline-topics';
            stat2.innerHTML =
                '<i class="fas fa-folder-minus"></i>' +
                '<b>' + lockStats.lockedTopics + '</b> chủ đề khoá';
            statsBar.appendChild(stat2);
        }

        /* STAT 3: Số chuyên ngành chưa mở */
        if (lockedIndustryCount > 0) {
            var stat3 = document.createElement('span');
            stat3.className = 'ob-stat-inline ob-stat-inline-industry';
            stat3.innerHTML =
                '<i class="fas fa-industry"></i>' +
                '<b>' + lockedIndustryCount + '</b> chuyên ngành khoá';
            statsBar.appendChild(stat3);
        }

        /* CTA */
        var shouldShowCta = false;
        var ctaLabel = '';
        var ctaIcon = '';
        var ctaAction = null;

        if (info.tier === 'trial') {
            var expiryEl = $('expiryBanner');
            var expiryVisible = false;
            if (expiryEl) {
                var displayStyle = window.getComputedStyle(expiryEl).display;
                expiryVisible = (expiryEl.style.display !== 'none' && displayStyle !== 'none');
            }
            if (!expiryVisible) {
                shouldShowCta = true;
                ctaLabel = 'Nâng cấp';
                ctaIcon = 'fas fa-gem';
                ctaAction = function() {
                    if (typeof openRenewalModal === 'function') openRenewalModal();
                };
            }
        }

        var hasAnyLock = (lockedCount > 0) || (lockedIndustryCount > 0) || (lockStats.lockedTopics > 0);

        if (hasAnyLock && shouldShowCta) {
            var ctaBtn = document.createElement('button');
            ctaBtn.type = 'button';
            ctaBtn.className = 'ob-cta-btn';
            ctaBtn.innerHTML = '<i class="' + ctaIcon + '"></i> ' + ctaLabel;
            ctaBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                if (typeof ctaAction === 'function') ctaAction();
            });
            statsBar.appendChild(ctaBtn);
        }

        if (statsBar.children.length > 0) {
            banner.appendChild(statsBar);
        }
    }

    container.insertBefore(banner, container.firstChild);
}

function initOnboarding() {
    var startBtn = $('onboardingStartBtn');
    var skipBtn = $('onboardingSkipBtn');
    var closeBtn = $('onboardingCloseBtn');

    if (startBtn) startBtn.addEventListener('click', onOnboardingStart);
    if (skipBtn)  skipBtn.addEventListener('click', onOnboardingSkip);

    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            onOnboardingSkip();
        });
    }

    document.addEventListener('keydown', function(e) {
        if (e.key !== 'Escape') return;
        var modal = $('onboardingModal');
        if (modal && modal.classList.contains('show')) {
            onOnboardingSkip();
        }
    });

    var modal = $('onboardingModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                onOnboardingSkip();
            }
        });
    }

    setTimeout(maybeShowOnboarding, 500);
}

window.maybeShowOnboarding = maybeShowOnboarding;
window.showOnboardingModal = showOnboardingModal;
window.applyOnboardingSelection = applyOnboardingSelection;
window.onChangeTopicsClick = onChangeTopicsClick;

/* ============================================================ */
/* TIKTOK BAR RESPONSIVE                                         */
/* ============================================================ */
function moveTikTokBarToHeader() {
    try {
        if (window.innerWidth < 769) return;
        var headerInner = document.querySelector('.header-inner');
        var headerActions = document.querySelector('.header-actions');
        var tiktokBar = document.querySelector('.sticky-top .container > .tiktok-bar');
        if (!headerInner || !headerActions || !tiktokBar) return;
        headerInner.insertBefore(tiktokBar, headerActions);
        setTimeout(function() { checkHeaderOverflow(); }, 100);
    } catch(e) {}
}

function moveTikTokBarBelowHeader() {
    try {
        var headerInner = document.querySelector('.header-inner');
        var tiktokBar = headerInner ? headerInner.querySelector('.tiktok-bar') : null;
        var container = document.querySelector('.sticky-top .container');
        var header = container ? container.querySelector('.header') : null;
        if (!tiktokBar || !container || !header) return;
        if (header.nextSibling) {
            container.insertBefore(tiktokBar, header.nextSibling);
        } else {
            container.appendChild(tiktokBar);
        }
    } catch(e) {}
}

function checkHeaderOverflow() {
    try {
        if (window.innerWidth < 769) return;
        var headerInner = document.querySelector('.header-inner');
        if (!headerInner) return;
        var tiktok = headerInner.querySelector('.tiktok-bar');
        if (!tiktok) return;
        tiktok.style.display = '';
    } catch(e) {}
}

var _lastWidthMode = null;
function handleResponsiveTikTok() {
    var currentMode = window.innerWidth >= 769 ? 'desktop' : 'mobile';
    if (currentMode === _lastWidthMode) return;
    _lastWidthMode = currentMode;
    if (currentMode === 'desktop') moveTikTokBarToHeader();
    else moveTikTokBarBelowHeader();
}

function populateTikTokFloat() {
    try {
        var pfTiktok = $('pfTiktokFloat');
        if (!pfTiktok) return;
        var tiktokUrl = (typeof TIKTOK_URL !== 'undefined' && TIKTOK_URL) ? TIKTOK_URL : '';
        if (!tiktokUrl) { pfTiktok.style.display = 'none'; return; }
        pfTiktok.href = tiktokUrl;
        var avatarUrl = (typeof TIKTOK_AVATAR !== 'undefined' && TIKTOK_AVATAR) ? TIKTOK_AVATAR : '';
        var avatarEl = $('pfTiktokAvatar');
        if (avatarEl) {
            if (avatarUrl) { avatarEl.src = avatarUrl; avatarEl.style.display = ''; }
            else { avatarEl.style.display = 'none'; }
        }
        var displayName = '';
        if (typeof TIKTOK_NICKNAME !== 'undefined' && TIKTOK_NICKNAME) displayName = TIKTOK_NICKNAME;
        else if (typeof TIKTOK_USERNAME !== 'undefined' && TIKTOK_USERNAME) displayName = TIKTOK_USERNAME;
        else displayName = 'TikTok';
        var nameEl = $('pfTiktokName');
        if (nameEl) nameEl.textContent = displayName;
        pfTiktok.title = 'Theo dõi TikTok: ' + displayName;
    } catch(e) {}
}

/* ============================================================ */
/* INIT APP                                                      */
/* ============================================================ */
function initApp() {
    mobileWrapper = $('mobileWrapper');
    $('loadingScreen').classList.add('hidden');
    $('stickyTop').style.display = 'block';
    $('fabGroup').style.display = 'flex';
    $('mainContent').style.display = 'block';

    loadVoiceSettings();
    initDatasetSelector();

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
    initVoiceSettings();
    initOnboarding();

    /* ❤️ Khởi tạo module Yêu thích */
    if (typeof initFavorites === 'function') initFavorites();

    _lastWidthMode = window.innerWidth >= 769 ? 'desktop' : 'mobile';
    if (_lastWidthMode === 'desktop') moveTikTokBarToHeader();
    populateTikTokFloat();

    var _resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(_resizeTimer);
        _resizeTimer = setTimeout(function() {
            handleResponsiveTikTok();
            checkHeaderOverflow();
        }, 200);
    });

    $('searchInput').addEventListener('input', applyFilter);
    $('resetBtn').addEventListener('click', function() {
        $('searchInput').value = '';
        $('hskFilter').value = '';
        $('subjectFilter').value = '';
        window.__onboardingOverride = null;

        /* ❤️ Nếu đang ở tab Yêu thích → về tổng hợp trước */
        if (typeof favState !== 'undefined' && favState.currentView) {
            favState.currentView = false;
            if (typeof switchDataset === 'function') switchDataset('tonghop');
            if (typeof markCurrentDatasetActive === 'function') markCurrentDatasetActive();
        }

        var obBanner = $('onboardingActiveBanner');
        if (obBanner) obBanner.remove();
        applyFilter();

        /* Khôi phục banner chủ đề sau khi reset filter */
        var saved = loadOnboardingSelection();
        if (saved && Array.isArray(saved.topics) && saved.topics.length > 0) {
            var cfg = getOnboardingConfig();
            if (cfg) {
                window.__onboardingAutoPicked = !!saved.auto_picked;
                applyOnboardingSelection(saved.topics, false);
            }
        }
    });
    $('clearSearchBtn').addEventListener('click', function() {
        $('searchInput').value = '';
        state.search = '';
        $('searchInput').focus();
        applyFilter();
        this.classList.remove('show');

        var saved = loadOnboardingSelection();
        if (saved && Array.isArray(saved.topics) && saved.topics.length > 0) {
            var cfg = getOnboardingConfig();
            if (cfg) {
                window.__onboardingAutoPicked = !!saved.auto_picked;
                applyOnboardingSelection(saved.topics, false);
            }
        }
    });
    $('hskFilter').addEventListener('change', function() {
        var val = this.value;
        var allowed = getAllowedHskList();
        if (val && allowed.indexOf(val) === -1) {
            var info = getTierInfo();
            var msg = info.tier === 'trial'
                ? 'Bản Trial chỉ cho phép lọc HSK1-' + info.maxHSK + '.'
                : 'Bản Demo chỉ cho phép lọc HSK1-' + info.maxHSK + '.';
            alert(msg);
            this.value = '';
            applyFilter();
            return;
        }
        applyFilter();
    });
    $('subjectFilter').addEventListener('change', function() {
        var val = this.value;
        var allowed = getAllowedSubjectList();
        if (val && allowed.indexOf(val) === -1) {
            var info = getTierInfo();
            var msg = info.tier === 'trial'
                ? 'Chủ đề này chưa có trong ' + info.maxQuestions + ' câu Trial.'
                : 'Chủ đề này chưa có trong ' + info.maxQuestions + ' câu Demo.';
            alert(msg);
            this.value = '';
            applyFilter();
            return;
        }
        applyFilter();
    });

    try { buildFilters(); applyFilter(); }
    catch(e) { console.error('Init error:', e); }
}
/* ═══════════════════════════════════════════════════════════ */
/* SỬA: REFRESH APP — VẼ LẠI BANNER SAU LOGIN/RELOAD            */
/* ═══════════════════════════════════════════════════════════ */
function refreshApp() {
    buildFilters();
    applyFilter();
    applyDisplayState();
    updateToggleButtons();
    updateResultCount();
    updateTierBadge();
    updateDemoBanner();

    /* ❤️ Cập nhật trạng thái Yêu thích khi tier đổi */
    if (typeof favUpdateLockState === 'function') favUpdateLockState();
    if (typeof favRefreshUI === 'function') favRefreshUI();

    /* FIX: Vẽ lại banner chủ đề nếu có selection */
    if (typeof maybeShowOnboarding === 'function') {
        setTimeout(maybeShowOnboarding, 0);
    }
}

function updateTierBadge() {
    var badge = $('trialBadge');
    if (!badge) return;
    var info = getTierInfo();
    if (info.tier === 'trial') {
        badge.classList.add('show');
        var daysLeft = null;
        if (typeof getDaysRemaining === 'function'
            && typeof currentUser !== 'undefined'
            && currentUser) {
            daysLeft = getDaysRemaining(currentUser);
        }
        var badgeText = $('trialBadgeText');
        if (badgeText) {
            if (daysLeft !== null && daysLeft > 0) {
                badgeText.textContent = 'Trial · ' + daysLeft + ' ngày';
            } else {
                badgeText.textContent = 'Trial';
            }
        }
    } else {
        badge.classList.remove('show');
    }
}

function updateDemoBanner() {
    var info = getTierInfo();
    var banner = $('demoBanner');
    if (!banner) return;
    if (info.tier !== 'demo' && info.tier !== 'expired') return;
    var titleEl = $('demoBannerTitle');
    var descEl  = $('demoBannerDesc');
    var btnEl   = $('demoBannerBtn');
    var btnText = $('demoBannerBtnText');
    var iconEl  = banner.querySelector('.demo-banner-icon');

    if (info.tier === 'expired') {
        if (titleEl) titleEl.innerHTML = 'Tài khoản đã hết hạn';
        if (descEl) {
            descEl.innerHTML = 'Bạn đang xem chế độ giới hạn (' +
                info.maxQuestions + ' câu đầu, HSK1-' + info.maxHSK + ', ' +
                DEMO_DAILY_LIMIT + ' lượt/ngày).<br>Gia hạn để mở khóa toàn bộ ' +
                (typeof RAW_DATA !== 'undefined' ? RAW_DATA.length : '') + ' câu!';
        }
        if (btnEl) {
            btnEl.onclick = function() {
                if (typeof openRenewalModal === 'function') openRenewalModal();
            };
            btnEl.setAttribute('onclick', '');
        }
        if (btnText) btnText.textContent = 'Gia hạn ngay';
        if (iconEl) iconEl.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
        banner.style.background = 'linear-gradient(135deg, #fecaca, #fca5a5)';
        banner.style.borderColor = '#dc2626';
    } else {
        if (titleEl) titleEl.innerHTML = 'Đăng nhập miễn phí để mở khóa toàn bộ';
        if (descEl) {
            descEl.innerHTML = 'Đăng nhập bằng <b>Gmail</b> để xem <b>toàn bộ kho câu</b>, ' +
                'không giới hạn nghe và luyện viết.<br>' +
                'Nghe + Luyện viết còn lại hôm nay: ' +
                '<b id="demoRemainingText" style="color:#16a34a">' + getDemoRemaining() + '</b> lượt.';
        }
        if (btnText) btnText.textContent = 'Đăng nhập bằng Gmail';
        if (iconEl) iconEl.innerHTML = '<i class="fas fa-gift"></i>';
        banner.style.background = '';
        banner.style.borderColor = '';
    }
}

/* ============================================================ */
/* SCROLL / FAB / THEME / DISPLAY                                */
/* ============================================================ */
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

function initFabGroup() {
    var fabGroup = $('fabGroup');
    var fabMainBtn = $('fabMainBtn');
    if (!fabGroup || !fabMainBtn) return;

    var closedFlag = null;
    try { closedFlag = sessionStorage.getItem('fabClosed'); } catch(_e) {}

    var fabOpen = (closedFlag !== '1');
    fabGroup.classList.toggle('open', fabOpen);

    fabMainBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        fabOpen = !fabOpen;
        fabGroup.classList.toggle('open', fabOpen);
        try { sessionStorage.setItem('fabClosed', fabOpen ? '0' : '1'); } catch(_e) {}
    });

    document.addEventListener('click', function(e) {
        if (!fabGroup.contains(e.target) && fabOpen && window.innerWidth > 768) {
            fabOpen = false;
            fabGroup.classList.remove('open');
            try { sessionStorage.setItem('fabClosed', '1'); } catch(_e) {}
        }
    });
}

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
    if (displayState.practice) { displayState.pinyin = false; displayState.vi = true; }
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
        if (displayState.practice) { displayState.pinyin = false; displayState.vi = true; }
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
        btn.classList.remove('active');
    } else {
        icon.className = 'fas fa-bell';
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
        e.target.closest('.search-filter-row') ||
        e.target.closest('.writer-modal') || e.target.closest('.user-menu') ||
        e.target.closest('.login-modal') || e.target.closest('.admin-modal') ||
        e.target.closest('.practice-full-modal') || e.target.closest('.import-modal') ||
        e.target.closest('.edit-modal') || e.target.closest('.zalo-btn') ||
        e.target.closest('.tiktok-float-wrap') || e.target.closest('.tiktok-bar') ||
        e.target.closest('.renewal-modal') || e.target.closest('.voice-modal') ||
        e.target.closest('.dataset-selector') ||
        e.target.closest('.onboarding-modal') ||
        e.target.closest('.onboarding-active-banner') ||
        e.target.closest('.tag-clickable') ||
        e.target.closest('.toggle-check-btn')) return;
    clearFocus();
}, true);

/* ============================================================ */
/* SPEECH                                                        */
/* ============================================================ */
function initSpeech() {
    if ('speechSynthesis' in window) {
        speechSynthesis.getVoices();
        if (speechSynthesis.onvoiceschanged !== undefined) {
            speechSynthesis.onvoiceschanged = function(){
                populateVoiceSelect();
            };
        }
    }
}

window.speakText = function(text, btn, evt) {
    if (evt) evt.stopPropagation();
    if (!canUseFeature()) { showLimitMessage(); return; }
    if (!('speechSynthesis' in window)) { alert('Trình duyệt không hỗ trợ phát âm.'); return; }
    if (shouldCountUsage()) { incDemoUsage(); updateDemoRemaining(); }
    speechSynthesis.cancel();
    if (currentBtn) currentBtn.classList.remove('speaking');
    if (btn) { btn.classList.add('speaking'); currentBtn = btn; }
    var utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'zh-CN';
    applyVoiceSettings(utterance);
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

function populateVoiceSelect() {
    if (!('speechSynthesis' in window)) return;
    var sel = $('voiceSelect');
    if (!sel) return;
    var voices = speechSynthesis.getVoices();
    var zhVoices = voices.filter(function(v) {
        return v.lang && v.lang.toLowerCase().indexOf('zh') === 0;
    });
    if (!zhVoices.length) {
        sel.innerHTML = '<option value="">-- Đang tải giọng đọc... --</option>';
        return;
    }
    sel.innerHTML = '';
    var defaultOpt = document.createElement('option');
    defaultOpt.value = '';
    defaultOpt.textContent = '-- Tự động (mặc định) --';
    sel.appendChild(defaultOpt);

    zhVoices.forEach(function(v) {
        var opt = document.createElement('option');
        opt.value = v.voiceURI;
        var label = v.name + ' (' + v.lang + ')' + (v.localService ? '' : ' - online');
        opt.textContent = label;
        sel.appendChild(opt);
    });
    sel.value = voiceState.voiceURI || '';
}

function updateVoiceUI() {
    var rateSlider = $('voiceRateSlider');
    var rateVal    = $('voiceRateValue');
    var pitchSlider = $('voicePitchSlider');
    var pitchVal   = $('voicePitchValue');
    var volSlider  = $('voiceVolumeSlider');
    var volVal     = $('voiceVolumeValue');
    if (rateSlider)  rateSlider.value  = voiceState.rate;
    if (rateVal)     rateVal.textContent = voiceState.rate.toFixed(2) + '×';
    if (pitchSlider) pitchSlider.value = voiceState.pitch;
    if (pitchVal)    pitchVal.textContent = voiceState.pitch.toFixed(2);
    if (volSlider)   volSlider.value   = voiceState.volume;
    if (volVal)      volVal.textContent = Math.round(voiceState.volume * 100) + '%';

    document.querySelectorAll('.voice-preset-btn').forEach(function(b) {
        var r = parseFloat(b.dataset.rate);
        b.classList.toggle('active', Math.abs(r - voiceState.rate) < 0.001);
    });
}

function voiceTestSpeak() {
    if (!('speechSynthesis' in window)) { alert('Trình duyệt không hỗ trợ phát âm.'); return; }
    speechSynthesis.cancel();
    var btn = $('voiceTestBtn');
    if (btn) {
        btn.classList.add('speaking');
        btn.innerHTML = '<i class="fas fa-stop"></i> Đang đọc...';
    }
    var u = new SpeechSynthesisUtterance('你好，欢迎学习中文。');
    u.lang = 'zh-CN';
    applyVoiceSettings(u);
    var finish = function() {
        if (btn) {
            btn.classList.remove('speaking');
            btn.innerHTML = '<i class="fas fa-play"></i> Nghe thử';
        }
    };
    u.onend = finish;
    u.onerror = finish;
    setTimeout(function(){ try { speechSynthesis.speak(u); } catch(e) { finish(); } }, 30);
}

function initVoiceSettings() {
    var modal = $('voiceModal');
    if (!modal) return;

    populateVoiceSelect();

    var rateSlider = $('voiceRateSlider');
    var pitchSlider = $('voicePitchSlider');
    var volSlider = $('voiceVolumeSlider');

    updateVoiceUI();

    if (rateSlider) rateSlider.addEventListener('input', function() {
        voiceState.rate = parseFloat(this.value);
        $('voiceRateValue').textContent = voiceState.rate.toFixed(2) + '×';
        document.querySelectorAll('.voice-preset-btn').forEach(function(b) {
            b.classList.toggle('active', Math.abs(parseFloat(b.dataset.rate) - voiceState.rate) < 0.001);
        });
        saveVoiceSettings();
    });
    if (pitchSlider) pitchSlider.addEventListener('input', function() {
        voiceState.pitch = parseFloat(this.value);
        $('voicePitchValue').textContent = voiceState.pitch.toFixed(2);
        saveVoiceSettings();
    });
    if (volSlider) volSlider.addEventListener('input', function() {
        voiceState.volume = parseFloat(this.value);
        $('voiceVolumeValue').textContent = Math.round(voiceState.volume * 100) + '%';
        saveVoiceSettings();
    });

    function adjust(key, delta, min, max) {
        voiceState[key] = Math.max(min, Math.min(max, +(voiceState[key] + delta).toFixed(2)));
        updateVoiceUI();
        saveVoiceSettings();
    }
    if ($('voiceRateMinus'))  $('voiceRateMinus').addEventListener('click',  function(){ adjust('rate',   -0.05, 0.5, 1.5); });
    if ($('voiceRatePlus'))   $('voiceRatePlus').addEventListener('click',   function(){ adjust('rate',    0.05, 0.5, 1.5); });
    if ($('voicePitchMinus')) $('voicePitchMinus').addEventListener('click', function(){ adjust('pitch',  -0.05, 0.5, 1.5); });
    if ($('voicePitchPlus'))  $('voicePitchPlus').addEventListener('click',  function(){ adjust('pitch',   0.05, 0.5, 1.5); });
    if ($('voiceVolumeMinus'))$('voiceVolumeMinus').addEventListener('click',function(){ adjust('volume', -0.05, 0, 1); });
    if ($('voiceVolumePlus')) $('voiceVolumePlus').addEventListener('click', function(){ adjust('volume',  0.05, 0, 1); });

    document.querySelectorAll('.voice-preset-btn').forEach(function(b) {
        b.addEventListener('click', function() {
            voiceState.rate = parseFloat(this.dataset.rate);
            updateVoiceUI();
            saveVoiceSettings();
        });
    });

    var sel = $('voiceSelect');
    if (sel) sel.addEventListener('change', function() {
        voiceState.voiceURI = this.value;
        saveVoiceSettings();
    });

    if ($('voiceTestBtn')) $('voiceTestBtn').addEventListener('click', voiceTestSpeak);

    if ($('voiceResetBtn')) $('voiceResetBtn').addEventListener('click', function() {
        voiceState.rate    = DEFAULT_VOICE.rate;
        voiceState.pitch   = DEFAULT_VOICE.pitch;
        voiceState.volume  = DEFAULT_VOICE.volume;
        voiceState.voiceURI = DEFAULT_VOICE.voiceURI;
        if ($('voiceSelect')) $('voiceSelect').value = '';
        updateVoiceUI();
        saveVoiceSettings();
    });

    if ($('pfVoiceBtn')) {
        $('pfVoiceBtn').addEventListener('click', function(e) {
            e.stopPropagation();
            e.preventDefault();
            populateVoiceSelect();
            updateVoiceUI();
            modal.classList.add('show');
        });
    }
    if ($('toggleVoiceBtn')) {
        $('toggleVoiceBtn').addEventListener('click', function(e) {
            e.stopPropagation();
            populateVoiceSelect();
            updateVoiceUI();
            modal.classList.add('show');
            if ($('fabGroup')) $('fabGroup').classList.remove('open');
        });
    }
    if ($('voiceClose')) $('voiceClose').addEventListener('click', function() { modal.classList.remove('show'); });
    modal.addEventListener('click', function(e) { if (e.target === this) modal.classList.remove('show'); });
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('show')) modal.classList.remove('show');
    });
}

/* ============================================================ */
/* BUILD FILTERS                                                 */
/* ============================================================ */
function buildFilters() {
    var hskSelect = $('hskFilter');
    var subjectSelect = $('subjectFilter');
    var info = getTierInfo();
    var isLimited = info.tier !== 'active';

    if (isLimited) {
        var allowedHsk = getAllowedHskList();
        var hskHtml = '<option value="">Tất cả (HSK1-' + info.maxHSK + ')</option>';
        allowedHsk.forEach(function(h) {
            hskHtml += '<option value="' + h + '">' + h + '</option>';
        });
        var allHskList = ['HSK1','HSK2','HSK3','HSK4','HSK5','HSK6'];
        allHskList.forEach(function(h) {
            if (allowedHsk.indexOf(h) === -1) {
                var lockLabel = info.tier === 'trial' ? '(gia hạn)' : '(đăng nhập)';
                hskHtml += '<option value="' + h + '" disabled>' + h + ' ' + lockLabel + '</option>';
            }
        });
        hskSelect.innerHTML = hskHtml;

        var allowedSubjects = getAllowedSubjectList();
        var allSubjectSet = {};
        RAW_DATA.forEach(function(r) { if (r.subject) allSubjectSet[r.subject] = 1; });
        var allSubjects = Object.keys(allSubjectSet).sort();
        var unlocked = [], locked = [];
        allSubjects.forEach(function(s) {
            if (allowedSubjects.indexOf(s) !== -1) unlocked.push(s);
            else locked.push(s);
        });
        var subjHtml = '<option value="">Tất cả chủ đề</option>';
        unlocked.forEach(function(s) {
            subjHtml += '<option value="' + escapeHtml(s) + '">' + escapeHtml(s) + '</option>';
        });
        locked.forEach(function(s) {
            var lockLabel = info.tier === 'trial' ? '(gia hạn)' : '(đăng nhập)';
            subjHtml += '<option value="' + escapeHtml(s) + '" disabled>' + escapeHtml(s) + ' ' + lockLabel + '</option>';
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
        var allSubjectSet2 = {};
        RAW_DATA.forEach(function(r) { if (r.subject) allSubjectSet2[r.subject] = 1; });
        var allSubjects2 = Object.keys(allSubjectSet2).sort();
        subjectSelect.innerHTML = '<option value="">Tất cả chủ đề</option>' +
            allSubjects2.map(function(v){ return '<option value="'+escapeHtml(v)+'">'+escapeHtml(v)+'</option>'; }).join('');
    }
}

function updateFilterUI() {
    var hsk = $('hskFilter').value;
    var subject = $('subjectFilter').value;
    $('hskValue').textContent = hsk || 'Tất cả';
    $('subjectValue').textContent = subject || 'Tất cả';
    $('hskChip').classList.toggle('has-value', !!hsk);
    $('subjectChip').classList.toggle('has-value', !!subject);
    var info = getTierInfo();
    var limited = info.tier === 'demo' || info.tier === 'expired';
    $('hskChip').classList.toggle('demo-limited', limited);
    $('subjectChip').classList.toggle('demo-limited', limited);
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

function applyFilter() {
    /* ═══ 1. ĐỌC FILTER TỪ UI ═══ */
    state.search = $('searchInput').value.trim().toLowerCase();
    state.hsk = $('hskFilter').value;
    state.subject = $('subjectFilter').value;
    updateFilterUI();

    var clearBtn = $('clearSearchBtn');
    if (state.search) clearBtn.classList.add('show');
    else clearBtn.classList.remove('show');

    /* ═══════════════════════════════════════════════════════════
       ❤️ 2. NẾU ĐANG Ở TAB YÊ THÍCH → GỌI favRenderCurrentTab()
       ═══════════════════════════════════════════════════════════ */
    if (typeof favState !== 'undefined'
        && favState
        && favState.currentView === true
        && typeof favRenderCurrentTab === 'function') {
        favRenderCurrentTab();
        return;
    }

    /* ═══════════════════════════════════════════════════════════
       3. CHẾ ĐỘ BÌNH THƯỜNG — LỌC TẤT CẢ CÂU
       ═══════════════════════════════════════════════════════════ */
    var baseData = getLimitedData();
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

    if (state.hsk || state.subject) {
        setTimeout(function() {
            var mainEl = $('mainContent');
            if (mainEl) {
                var yOffset = mainEl.getBoundingClientRect().top + window.scrollY - 100;
                window.scrollTo({ top: yOffset, behavior: 'smooth' });
            }
        }, 150);
    }
}
/* ============================================================ */
/* RENDER CARDS                                                  */
/* ============================================================ */
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

        var excelBadge = '';
        if (r.excelRow !== undefined && r.excelRow !== null && r.excelRow !== '') {
            excelBadge = '<span class="card-excel-row" title="Dòng ' + escapeHtml(r.excelRow) + ' trong file Excel">' +
                         '<i class="fas fa-file-excel"></i> ' + escapeHtml(r.excelRow) +
                         '</span>';
        }

        var topicTag = '';
        if (r.topic) {
            topicTag = '<span class="card-tag topic tag-clickable" ' +
                       'onclick="searchByTag(event, \'topic\', \'' + escapeJs(r.topic) + '\')" ' +
                       'title="Lọc theo chủ điểm này">' +
                       escapeHtml(r.topic) + '</span>';
        }
        var subjectTag = '';
        if (r.subject) {
            subjectTag = '<span class="card-tag subject tag-clickable" ' +
                         'onclick="searchByTag(event, \'subject\', \'' + escapeJs(r.subject) + '\')" ' +
                         'title="Lọc theo chủ đề này">' +
                         escapeHtml(r.subject) + '</span>';
        }

        /* ❤️ Nút Yêu thích */
        var favBtnHtml = (typeof favBuildFavButton === 'function')
            ? favBuildFavButton(r.stt)
            : '';

        mobHtml += '<div class="card" data-hsk="' + (r.hsk || '') + '" onclick="toggleFocus(\'' + sttJs + '\', this)" data-stt="' + sttSafe + '">' +
            '<div class="card-header">' +
                '<div class="card-stt">' + sttSafe + '</div>' +
                '<div class="card-meta">' +
                    (r.hsk ? '<span class="card-tag hsk">' + escapeHtml(r.hsk) + '</span>' : '') +
                    topicTag +
                    subjectTag +
                    excelBadge +
                '</div>' +
                '<div onclick="event.stopPropagation()" class="action-group">' +
                    audio + writeBtn + fullBtn + favBtnHtml +
                '</div>' +
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
        var info = getTierInfo();
        var limited = info.tier !== 'active';
        var limitedDataLen = limited ? getLimitedData().length : RAW_DATA.length;
        var isTierLocked = limited && (renderedCount >= limitedDataLen) && (filtered.length >= limitedDataLen);

        if (!isTierLocked) {
            var btnMobile = document.createElement('button');
            btnMobile.className = 'load-more';
            btnMobile.innerHTML = '<i class="fas fa-chevron-down"></i> Xem thêm (' + renderedCount + '/' + filtered.length + ')';
            btnMobile.onclick = function() { render(false); };
            mobileWrapper.appendChild(btnMobile);
        } else {
            var lockedBtn = document.createElement('button');
            lockedBtn.className = 'load-more locked';
            if (info.tier === 'expired') {
                lockedBtn.classList.add('expired');
                lockedBtn.innerHTML = '<i class="fas fa-gem"></i> Gia hạn để xem toàn bộ ' + RAW_DATA.length + ' câu';
                lockedBtn.onclick = function() {
                    if (typeof openRenewalModal === 'function') openRenewalModal();
                };
            } else if (info.tier === 'trial') {
                lockedBtn.innerHTML = '<i class="fas fa-crown"></i> Gia hạn để xem toàn bộ ' + RAW_DATA.length + ' câu';
                lockedBtn.onclick = function() {
                    if (typeof openRenewalModal === 'function') openRenewalModal();
                };
            } else {
                lockedBtn.innerHTML = '<i class="fas fa-lock"></i> Đăng nhập để xem toàn bộ ' + RAW_DATA.length + ' câu';
                lockedBtn.onclick = function() {
                    if (typeof showLoginModal === 'function') showLoginModal();
                };
            }
            mobileWrapper.appendChild(lockedBtn);
        }
    } else if (filtered.length > PAGE_SIZE) {
        var endNote = document.createElement('div');
        endNote.className = 'end-note';
        endNote.innerHTML = '<i class="fas fa-check-circle"></i> Đã hiển thị tất cả ' + filtered.length + ' câu';
        mobileWrapper.appendChild(endNote);
    }
}
/* ============================================================ */
/* ANSWER CHECKING                                               */
/* ============================================================ */
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

function countSyllables(pinyinWord) {
    if (!pinyinWord) return 0;
    var cleaned = pinyinWord
        .replace(/[.,!?;:'"()\[\]{}\-~`@#$%^&*+=|\\/<>。，！？、；：\s]/g, '')
        .toLowerCase();
    if (!cleaned) return 0;
    var map = {
        'ā':'a','á':'a','ǎ':'a','à':'a','ē':'e','é':'e','ě':'e','è':'e',
        'ī':'i','í':'i','ǐ':'i','ì':'i','ō':'o','ó':'o','ǒ':'o','ò':'o',
        'ū':'u','ú':'u','ǔ':'u','ù':'u','ǖ':'v','ǘ':'v','ǚ':'v','ǜ':'v','ü':'v'
    };
    cleaned = cleaned.replace(/[āáǎàēéěèīíǐìōóǒòūúǔùǖǘǚǜü]/g, function(c) { return map[c] || c; });
    var vowels = 'aeiouv';
    var count = 0;
    var i = 0;
    while (i < cleaned.length) {
        if (vowels.indexOf(cleaned[i]) !== -1) {
            count++;
            while (i < cleaned.length && vowels.indexOf(cleaned[i]) !== -1) {
                i++;
            }
        } else {
            i++;
        }
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
        return hanziChars.map(function(c) { return { text: c, type: 'single', pinyin: '' }; });
    }

    var normalizedPinyin = pinyin
        .replace(/[.,!?;:'"()\[\]{}\-~`@#$%^&*+=|\\/<>。，！？、；：""'']/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();

    var pinyinWords = normalizedPinyin.split(/\s+/).filter(function(w) { return w.length > 0; });
    var syllableCounts = pinyinWords.map(function(w) { return countSyllables(w); });
    var totalSyllables = syllableCounts.reduce(function(a, b) { return a + b; }, 0);

    if (totalSyllables === hanziChars.length) {
        var result = [];
        var charIdx = 0;
        for (var j = 0; j < syllableCounts.length; j++) {
            var cnt = syllableCounts[j];
            if (cnt <= 0) continue;
            var phrase = hanziChars.slice(charIdx, charIdx + cnt).join('');
            if (phrase) {
                result.push({
                    text: phrase,
                    type: 'phrase',
                    pinyin: pinyinWords[j] || ''
                });
            }
            charIdx += cnt;
        }
        if (charIdx < hanziChars.length) {
            var remaining = hanziChars.slice(charIdx).join('');
            if (result.length > 0) {
                result[result.length - 1].text += remaining;
                if (charIdx < pinyinWords.length) {
                    result[result.length - 1].pinyin += ' ' + pinyinWords.slice(charIdx).join(' ');
                }
            } else {
                result.push({ text: remaining, type: 'single', pinyin: '' });
            }
        }
        return result;
    }

    return hanziChars.map(function(c) { return { text: c, type: 'single', pinyin: '' }; });
}

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
    evt.stopPropagation();
    if (evt.preventDefault) evt.preventDefault();
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
        if (result.status === 'correct') resultHtml = '<span class="ai-correct">ĐÚNG</span>';
        else if (result.status === 'partial') resultHtml = '<span class="ai-partial">GẦN ĐÚNG</span>';
        else resultHtml = '<span class="ai-wrong">SAI</span>';
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
        if (result.status === 'correct') resultHtml = '<span class="ai-correct">ĐÚNG</span>';
        else if (result.status === 'partial') resultHtml = '<span class="ai-partial">GẦN ĐÚNG</span>';
        else resultHtml = '<span class="ai-wrong">SAI</span>';
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

/* ============================================================ */
/* PRACTICE FULL MODAL — expired dùng được như Demo              */
/* ============================================================ */
var pfCurrentStt = null;
var pfCurrentAnswer = '';
var pfCurrentVi = '';
var pfCurrentPinyin = '';
var pfHintEnabled = false;
var pfRandomMode = false;

window.openPracticeFull = function(stt, evt) {
    if (evt) { evt.stopPropagation(); if (evt.preventDefault) evt.preventDefault(); }

    if (!canUseFeature()) { showLimitMessage(); return; }

    if (typeof pfBuildDatasetSelect === 'function') pfBuildDatasetSelect();
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
    $('practiceFullModal').classList.add('show');
    loadPracticeFull(stt);
};

window.closePracticeFull = function() {
    if (window._isSpeakingFull) stopSpeakFull();
    if (window._isQuickSpeaking) stopQuickSpeak();
    $('practiceFullModal').classList.remove('show');
    document.body.style.overflow = '';
    document.body.classList.remove('practice-full-open');
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

    var sttRaw = (r.stt !== undefined && r.stt !== null && String(r.stt).trim() !== '')
                 ? String(r.stt).trim()
                 : '';
    var sttLabel = sttRaw ? '#' + sttRaw + '  ·  ' : '';
    $('pfCounter').textContent = sttLabel + 'Câu ' + (idx + 1) + ' / ' + filtered.length;

    var tagsHtml = '';
    if (r.hsk) tagsHtml += '<span class="card-tag hsk">' + escapeHtml(r.hsk) + '</span>';
    if (r.topic) {
        tagsHtml += '<span class="card-tag topic tag-clickable" ' +
                    'onclick="searchByTag(event, \'topic\', \'' + escapeJs(r.topic) + '\')" ' +
                    'title="Lọc theo chủ điểm này">' +
                    escapeHtml(r.topic) + '</span>';
    }
    if (r.subject) {
        tagsHtml += '<span class="card-tag tag-clickable" ' +
                    'onclick="searchByTag(event, \'subject\', \'' + escapeJs(r.subject) + '\')" ' +
                    'title="Lọc theo chủ đề này">' +
                    escapeHtml(r.subject) + '</span>';
    }
    if (r.excelRow !== undefined && r.excelRow !== null && r.excelRow !== '') {
        tagsHtml += '<span class="card-tag excel-tag" title="Dòng ' + escapeHtml(r.excelRow) + ' trong file Excel">' +
                    '<i class="fas fa-file-excel"></i> Excel: ' + escapeHtml(r.excelRow) +
                    '</span>';
    }
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
    if (quickNav && quickNav.value !== stt) quickNav.value = stt;

    if (window._isSpeakingFull) {
        stopSpeakFull();
    } else {
        _setSpeakBtnState(false);
    }
    if (window._isQuickSpeaking) {
        stopQuickSpeak();
    } else {
        _setQuickSpeakBtnState(false);
    }

    setTimeout(function() {
        var active = document.activeElement;
        if (active && (active.tagName === 'INPUT' || active.tagName === 'TEXTAREA' || active.tagName === 'SELECT')) return;
        $('pfInput').focus();
    }, 200);
}

window.pfNext = function() {
    if (!pfCurrentStt || filtered.length === 0) return;
    var idx = -1;
    for (var i = 0; i < filtered.length; i++) {
        if (String(filtered[i].stt) === String(pfCurrentStt)) { idx = i; break; }
    }
    if (idx === -1) return;

    if (pfRandomMode && filtered.length > 1) {
        var newIdx = idx;
        var tries = 0;
        while (newIdx === idx && tries < 20) {
            newIdx = Math.floor(Math.random() * filtered.length);
            tries++;
        }
        if (newIdx === idx) newIdx = (idx + 1) % filtered.length;

        var rndBtn = $('pfRandomToggleBtn');
        if (rndBtn) {
            var icon = rndBtn.querySelector('i');
            if (icon) {
                icon.style.animation = 'none';
                void icon.offsetWidth;
                icon.style.animation = 'diceShake 0.6s ease-in-out';
            }
        }
        loadPracticeFull(filtered[newIdx].stt);
        return;
    }

    if (idx >= filtered.length - 1) return;
    loadPracticeFull(filtered[idx + 1].stt);
};

window.pfToggleRandom = function() {
    pfRandomMode = !pfRandomMode;
    var btn = $('pfRandomToggleBtn');
    if (btn) {
        btn.classList.toggle('active', pfRandomMode);
        btn.title = pfRandomMode
            ? 'ĐANG BẬT: Nút Next sẽ nhảy câu ngẫu nhiên'
            : 'Bật/tắt chế độ nhảy câu ngẫu nhiên';
    }
    try { localStorage.setItem('pfRandomMode', pfRandomMode ? '1' : '0'); } catch(e) {}
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

    // ═══ NẾU BẬT "CHỈ CÂU YÊU THÍCH" → CHỈ HIỆN CÂU YÊU THÍCH ═══
    var sourceList = filtered;
    if (typeof favState !== 'undefined'
        && favState.pfOnlyFav
        && typeof favCanUse === 'function'
        && favCanUse()) {
        sourceList = filtered.filter(function(r) {
            return favHas(r.stt);
        });
    }

    var html = '<option value="">-- Chọn câu (' + sourceList.length + ') --</option>';
    sourceList.forEach(function(r, i) {
        var vi = (r.vi || '').substring(0, 45);
        var sttRaw = (r.stt !== undefined && r.stt !== null && String(r.stt).trim() !== '')
                     ? '#' + String(r.stt).trim() + ' · '
                     : '';
        var label = sttRaw + 'Câu ' + (i + 1) + ': ' + vi;
        html += '<option value="' + escapeHtml(r.stt) + '">' + escapeHtml(label) + '</option>';
    });
    sel.innerHTML = html;
    if (pfCurrentStt) sel.value = pfCurrentStt;
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
    var info = getTierInfo();
    var isLimited = info.tier !== 'active';
    if (isLimited) {
        var allowedHsk = getAllowedHskList();
        var hskHtml = '<option value="">Tất cả</option>';
        allowedHsk.forEach(function(h) { hskHtml += '<option value="' + h + '">' + h + '</option>'; });
        var allHskList = ['HSK1','HSK2','HSK3','HSK4','HSK5','HSK6'];
        allHskList.forEach(function(h) {
            if (allowedHsk.indexOf(h) === -1) {
                var lockLabel = info.tier === 'trial' ? '(gia hạn)' : '(đăng nhập)';
                hskHtml += '<option value="' + h + '" disabled>' + h + ' ' + lockLabel + '</option>';
            }
        });
        hskSel.innerHTML = hskHtml;
        var allowedSubjects = getAllowedSubjectList();
        var allSubjectSet = {};
        RAW_DATA.forEach(function(r) { if (r.subject) allSubjectSet[r.subject] = 1; });
        var allSubjects = Object.keys(allSubjectSet).sort();
        var unlocked = [], locked = [];
        allSubjects.forEach(function(s) {
            if (allowedSubjects.indexOf(s) !== -1) unlocked.push(s);
            else locked.push(s);
        });
        var subjHtml = '<option value="">Tất cả chủ đề</option>';
        unlocked.forEach(function(s) { subjHtml += '<option value="' + escapeHtml(s) + '">' + escapeHtml(s) + '</option>'; });
        locked.forEach(function(s) {
            var lockLabel = info.tier === 'trial' ? '(gia hạn)' : '(đăng nhập)';
            subjHtml += '<option value="' + escapeHtml(s) + '" disabled>' + escapeHtml(s) + ' ' + lockLabel + '</option>';
        });
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
        var allSubjectSet2 = {};
        RAW_DATA.forEach(function(r) { if (r.subject) allSubjectSet2[r.subject] = 1; });
        var allSubjects2 = Object.keys(allSubjectSet2).sort();
        subjSel.innerHTML = '<option value="">Tất cả chủ đề</option>' +
            allSubjects2.map(function(v){ return '<option value="'+escapeHtml(v)+'">'+escapeHtml(v)+'</option>'; }).join('');
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
}

function pfApplyFilter() {
    $('searchInput').value = $('pfSearchInput').value;
    $('hskFilter').value = $('pfHskFilter').value;
    $('subjectFilter').value = $('pfSubjectFilter').value;
    state.search = $('pfSearchInput').value.trim().toLowerCase();
    state.hsk = $('pfHskFilter').value;
    state.subject = $('pfSubjectFilter').value;
    var baseData = getLimitedData();
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
    pfUpdateFilterUI();
    pfBuildQuickNav();
    render(true);
    if (state.hsk || state.subject) {
        setTimeout(function() {
            var bodyEl = document.querySelector('.practice-full-body');
            if (bodyEl) bodyEl.scrollTo({ top: 0, behavior: 'smooth' });
        }, 100);
    }
    var activeEl = document.activeElement;
    var isTypingInSearch = activeEl && activeEl.id === 'pfSearchInput';
    var currentStillValid = false;
    if (pfCurrentStt) {
        for (var i = 0; i < filtered.length; i++) {
            if (String(filtered[i].stt) === String(pfCurrentStt)) { currentStillValid = true; break; }
        }
    }
    if (filtered.length > 0) {
        if (isTypingInSearch && currentStillValid) {
            var idx = -1;
            for (var j = 0; j < filtered.length; j++) {
                if (String(filtered[j].stt) === String(pfCurrentStt)) { idx = j; break; }
            }
            if (idx !== -1) {
                var rNow = filtered[idx];
                var sttNow = (rNow.stt !== undefined && rNow.stt !== null && String(rNow.stt).trim() !== '')
                             ? '#' + String(rNow.stt).trim() + '  ·  '
                             : '';
                $('pfCounter').textContent = sttNow + 'Câu ' + (idx + 1) + ' / ' + filtered.length;
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
            if (userChar === answerChar) { cls += ' correct'; display = userChar; }
            else { cls += ' wrong'; display = userChar; clickable = true; }
        } else if (!userChar && answerChar) {
            if (pfHintEnabled) { cls += ' ghost'; display = answerChar; }
            else { continue; }
        } else if (userChar && !answerChar) {
            cls += ' extra'; display = userChar; clickable = true;
        } else { continue; }
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
        try { input.setSelectionRange(idx, idx + 1); }
        catch(e) { input.selectionStart = idx; input.selectionEnd = idx + 1; }
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
        statusEl.textContent = 'ĐÚNG';
        statusEl.className = 'practice-full-status correct';
    } else if (result.status === 'partial') {
        statusEl.textContent = (result.reason || 'GẦN ĐÚNG');
        statusEl.className = 'practice-full-status partial';
    } else {
        statusEl.textContent = 'SAI';
        statusEl.className = 'practice-full-status wrong';
    }
}

var _activeTooltipWrap = null;

function togglePhraseTooltip(wrapEl) {
    if (!wrapEl) return;
    var tip = wrapEl.querySelector('.answer-phrase-tooltip');
    if (!tip) return;

    if (_activeTooltipWrap && _activeTooltipWrap !== wrapEl) {
        var oldTip = _activeTooltipWrap.querySelector('.answer-phrase-tooltip');
        if (oldTip) oldTip.classList.remove('show');
    }

    if (tip.classList.contains('show')) {
        tip.classList.remove('show');
        _activeTooltipWrap = null;
    } else {
        tip.classList.add('show');
        _activeTooltipWrap = wrapEl;
    }
}

document.addEventListener('click', function(e) {
    if (!e.target.closest('.answer-phrase-wrap')) {
        document.querySelectorAll('.answer-phrase-tooltip.show').forEach(function(t) {
            t.classList.remove('show');
        });
        _activeTooltipWrap = null;
    }
});

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
            if (/[\u4e00-\u9fa5]/.test(c)) phrases.push({ text: c, type: 'single', pinyin: '' });
        });
    }
    window._pfPhrases = phrases;

    phrases.forEach(function(item, idx) {
        var wrap = document.createElement('span');
        wrap.className = 'answer-phrase-wrap';
        wrap.dataset.idx = idx;
        wrap.dataset.text = item.text;
        wrap.dataset.pinyin = item.pinyin || '';

        var btn = document.createElement('button');
        btn.className = 'answer-phrase-btn';
        btn.textContent = item.text;
        btn.title = item.pinyin ? (item.text + ' - ' + item.pinyin) : item.text;
        btn.onclick = (function(text, pinyin, el, wrapEl) {
            return function(e) {
                e.stopPropagation();
                el.classList.add('zoom-in');
                setTimeout(function() { el.classList.remove('zoom-in'); }, 700);
                togglePhraseTooltip(wrapEl);
                speakPhrase(text, el);
            };
        })(item.text, item.pinyin, btn, wrap);
        wrap.appendChild(btn);

        var tip = document.createElement('span');
        tip.className = 'answer-phrase-tooltip';
        tip.textContent = item.pinyin || item.text;
        wrap.appendChild(tip);

        if (item.pinyin) {
            wrap.addEventListener('mouseenter', function() {
                tip.classList.add('show');
            });
            wrap.addEventListener('mouseleave', function() {
                tip.classList.remove('show');
            });
        }

        charsEl.appendChild(wrap);
    });

    pinyinEl.textContent = pfCurrentPinyin;
    answerEl.classList.add('show');
    revealBtn.classList.add('revealed');
    revealBtn.innerHTML = '<i class="fas fa-eye-slash"></i> Ẩn đáp án';
}

window.speakPhrase = function(phrase, btn) {
    if (!canUseFeature()) { showLimitMessage(); return; }
    if (!('speechSynthesis' in window)) { alert('Trình duyệt không hỗ trợ phát âm.'); return; }
    if (shouldCountUsage()) { incDemoUsage(); updateDemoRemaining(); }
    speechSynthesis.cancel();
    document.querySelectorAll('.answer-phrase-btn.speaking').forEach(function(b) { b.classList.remove('speaking'); });
    btn.classList.add('speaking');
    var utterance = new SpeechSynthesisUtterance(phrase);
    utterance.lang = 'zh-CN';
    applyVoiceSettings(utterance);
    utterance.onend = utterance.onerror = function() { btn.classList.remove('speaking'); };
    setTimeout(function(){ speechSynthesis.speak(utterance); }, 30);
};

window._isSpeakingFull = false;
window._speakToken = 0;

function _setSpeakBtnState(speaking) {
    window._isSpeakingFull = speaking;
    var btn = $('pfSpeakBtn');
    if (!btn) return;
    if (speaking) {
        btn.classList.add('speaking');
        btn.setAttribute('title', 'Nhấn để dừng');
        btn.setAttribute('aria-label', 'Nhấn để dừng');
        var i = btn.querySelector('i');
        if (i) i.className = 'fas fa-stop';
    } else {
        btn.classList.remove('speaking');
        btn.setAttribute('title', 'Nghe câu này');
        btn.setAttribute('aria-label', 'Nghe câu này');
        var i2 = btn.querySelector('i');
        if (i2) i2.className = 'fas fa-volume-up';
    }
}

window.stopSpeakFull = function() {
    window._speakToken++;
    window._isSpeakingFull = false;
    if ('speechSynthesis' in window) {
        try { speechSynthesis.cancel(); } catch(e) {}
    }
    var charsContainer = $('pfAnswerChars');
    if (charsContainer) {
        charsContainer.querySelectorAll('.answer-phrase-btn.reading, .answer-phrase-btn.speaking').forEach(function(b) {
            b.classList.remove('reading', 'speaking');
        });
        charsContainer.querySelectorAll('.answer-phrase-tooltip.show').forEach(function(t) {
            t.classList.remove('show');
        });
        charsContainer.querySelectorAll('.answer-phrase-wrap.active-wrap').forEach(function(w) {
            w.classList.remove('active-wrap');
        });
    }
    _activeTooltipWrap = null;
    _setSpeakBtnState(false);
};

window.toggleSpeakFull = function() {
    if (!pfCurrentAnswer) return;
    if (window._isSpeakingFull) { stopSpeakFull(); return; }
    if (window._isQuickSpeaking) stopQuickSpeak();
    if (!canUseFeature()) { showLimitMessage(); return; }
    if (!('speechSynthesis' in window)) {
        alert('Trình duyệt không hỗ trợ phát âm.');
        return;
    }
    if (shouldCountUsage()) { incDemoUsage(); updateDemoRemaining(); }
    if ('speechSynthesis' in window) {
        try { speechSynthesis.cancel(); } catch(e) {}
    }
    var token = ++window._speakToken;
    _setSpeakBtnState(true);

    var answerVisible = $('pfAnswer').classList.contains('show');
    if (answerVisible) {
        _speakWithHighlightKaraoke(token);
    } else {
        _speakNormal(token);
    }
};

function _speakNormal(token) {
    var u = new SpeechSynthesisUtterance(pfCurrentAnswer);
    u.lang = 'zh-CN';
    applyVoiceSettings(u);
    var done = false;
    function finish() {
        if (done) return;
        done = true;
        if (token !== window._speakToken) return;
        _setSpeakBtnState(false);
    }
    u.onend = finish;
    u.onerror = finish;
    setTimeout(function() {
        if (token !== window._speakToken) return;
        try { speechSynthesis.speak(u); } catch(e) { finish(); }
    }, 30);
}

function _speakWithHighlightKaraoke(token) {
    var phrases = window._pfPhrases || [];
    var charsContainer = $('pfAnswerChars');
    if (!charsContainer) { _setSpeakBtnState(false); return; }
    var wraps = charsContainer.querySelectorAll('.answer-phrase-wrap');
    var buttons = charsContainer.querySelectorAll('.answer-phrase-btn');
    if (phrases.length === 0) { _speakNormal(token); return; }
    var idx = 0;

    function cleanupAll() {
        buttons.forEach(function(b) { b.classList.remove('reading'); });
        charsContainer.querySelectorAll('.answer-phrase-tooltip.show').forEach(function(t) {
            t.classList.remove('show');
        });
        charsContainer.querySelectorAll('.answer-phrase-wrap.active-wrap').forEach(function(w) {
            w.classList.remove('active-wrap');
        });
        _activeTooltipWrap = null;
    }

    function speakNext() {
        if (token !== window._speakToken) { cleanupAll(); return; }
        if (idx >= phrases.length) {
            cleanupAll();
            _setSpeakBtnState(false);
            return;
        }
        var phrase = phrases[idx];
        var btn = buttons[idx];
        var wrap = wraps[idx];

        if (btn) btn.classList.add('reading');
        if (wrap) {
            wrap.classList.add('active-wrap');
            charsContainer.querySelectorAll('.answer-phrase-tooltip.show').forEach(function(t) {
                t.classList.remove('show');
            });
            var tip = wrap.querySelector('.answer-phrase-tooltip');
            if (tip) {
                tip.classList.add('show');
                _activeTooltipWrap = wrap;
            }
        }

        var u = new SpeechSynthesisUtterance(phrase.text);
        u.lang = 'zh-CN';
        applyVoiceSettings(u);

        var handled = false;
        function next() {
            if (handled) return;
            handled = true;
            if (btn) btn.classList.remove('reading');
            if (wrap) wrap.classList.remove('active-wrap');
            if (token !== window._speakToken) { cleanupAll(); return; }
            idx++;
            setTimeout(speakNext, 120);
        }
        u.onend = next;
        u.onerror = next;
        setTimeout(function() {
            if (token !== window._speakToken) { next(); return; }
            try { speechSynthesis.speak(u); } catch(e) { next(); }
        }, 30);
    }

    setTimeout(speakNext, 100);
}

window._isQuickSpeaking = false;
window._quickSpeakToken = 0;

function _setQuickSpeakBtnState(speaking) {
    window._isQuickSpeaking = speaking;
    var btn = $('pfQuickSpeakBtn');
    if (!btn) return;
    if (speaking) {
        btn.classList.add('speaking');
        btn.setAttribute('title', 'Nhấn để dừng');
        btn.setAttribute('aria-label', 'Nhấn để dừng');
        var i = btn.querySelector('i');
        if (i) i.className = 'fas fa-stop';
    } else {
        btn.classList.remove('speaking');
        btn.setAttribute('title', 'Đọc cả câu');
        btn.setAttribute('aria-label', 'Đọc cả câu');
        var i2 = btn.querySelector('i');
        if (i2) i2.className = 'fas fa-volume-up';
    }
}

window.stopQuickSpeak = function() {
    window._quickSpeakToken++;
    window._isQuickSpeaking = false;
    if ('speechSynthesis' in window) {
        try { speechSynthesis.cancel(); } catch(e) {}
    }
    _setQuickSpeakBtnState(false);
};

window.toggleQuickSpeakFull = function() {
    if (!pfCurrentAnswer) return;
    if (window._isQuickSpeaking) { stopQuickSpeak(); return; }
    if (window._isSpeakingFull) stopSpeakFull();
    if (!canUseFeature()) { showLimitMessage(); return; }
    if (!('speechSynthesis' in window)) {
        alert('Trình duyệt không hỗ trợ phát âm.');
        return;
    }
    if (shouldCountUsage()) { incDemoUsage(); updateDemoRemaining(); }
    if ('speechSynthesis' in window) {
        try { speechSynthesis.cancel(); } catch(e) {}
    }
    var token = ++window._quickSpeakToken;
    _setQuickSpeakBtnState(true);
    _quickSpeakNormal(token);
};

function _quickSpeakNormal(token) {
    var u = new SpeechSynthesisUtterance(pfCurrentAnswer);
    u.lang = 'zh-CN';
    applyVoiceSettings(u);
    var done = false;
    function finish() {
        if (done) return;
        done = true;
        if (token !== window._quickSpeakToken) return;
        _setQuickSpeakBtnState(false);
    }
    u.onend = finish;
    u.onerror = finish;
    setTimeout(function() {
        if (token !== window._quickSpeakToken) return;
        try { speechSynthesis.speak(u); } catch(e) { finish(); }
    }, 30);
}

function initPracticeFull() {
    /* ═══════════════════════════════════════════════════════════
       ⬇️ AUTO-GROW TEXTAREA — Ô nhập tự giãn khi gõ câu dài
       ═══════════════════════════════════════════════════════════ */
    (function setupAutoGrow() {
        var inp = $('pfInput');
        if (!inp) return;

        function autoGrow() {
            if (!inp || inp.tagName !== 'TEXTAREA') return;
            inp.style.height = 'auto';
            var newH = inp.scrollHeight;
            var maxH = Math.floor(window.innerHeight * 0.4);
            if (newH > maxH) {
                inp.style.height = maxH + 'px';
                inp.style.overflowY = 'auto';
            } else {
                inp.style.height = newH + 'px';
                inp.style.overflowY = 'hidden';
            }
            var lineH = parseFloat(getComputedStyle(inp).lineHeight) || 20;
            var hasMultiline = newH > (lineH * 1.5 + 20);
            inp.classList.toggle('multiline', hasMultiline);
        }

        inp.addEventListener('input', autoGrow);
        inp.addEventListener('paste', function() { setTimeout(autoGrow, 0); });
        window.addEventListener('resize', autoGrow);

        var orig = window.loadPracticeFull;
        if (typeof orig === 'function' && !orig.__autoGrowPatched) {
            window.loadPracticeFull = function(stt) {
                var r = orig.apply(this, arguments);
                var i2 = $('pfInput');
                if (i2 && i2.tagName === 'TEXTAREA') {
                    i2.style.height = 'auto';
                    i2.style.overflowY = 'hidden';
                    i2.classList.remove('multiline');
                }
                return r;
            };
            window.loadPracticeFull.__autoGrowPatched = true;
        }

        autoGrow();
    })();

    /* ═══════════════════════════════════════════════════════════
       Random mode init
       ═══════════════════════════════════════════════════════════ */
    try {
        var savedRandom = localStorage.getItem('pfRandomMode') === '1';
        if (savedRandom) {
            pfRandomMode = true;
            var rBtnInit = $('pfRandomToggleBtn');
            if (rBtnInit) {
                rBtnInit.classList.add('active');
                rBtnInit.title = 'ĐANG BẬT: Nút Next sẽ nhảy câu ngẫu nhiên';
            }
        }
    } catch(e) {}

    /* Random toggle button */
    var randomToggleBtn = $('pfRandomToggleBtn');
    if (randomToggleBtn) {
        randomToggleBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            e.preventDefault();
            pfToggleRandom();
        });
    }

    /* Nút đóng modal */
    $('pfClose').addEventListener('click', closePracticeFull);

    /* Nút prev / next */
    $('pfPrevBtn').addEventListener('click', pfPrev);
    $('pfNextBtn').addEventListener('click', pfNext);

    /* Nút reveal / hint */
    $('pfRevealBtn').addEventListener('click', revealFullAnswer);
    $('pfHintBtn').addEventListener('click', toggleHint);

    /* Input — update preview + check */
    $('pfInput').addEventListener('input', function() {
        updateCharPreview();
        checkFullAnswer();
    });

    /* Quick nav */
    $('pfQuickNav').addEventListener('change', pfQuickNavChange);

    /* Search trong modal */
    $('pfSearchInput').addEventListener('input', function() { pfApplyFilter(); });
    $('pfClearSearchBtn').addEventListener('click', function() {
        $('pfSearchInput').value = '';
        $('pfSearchInput').focus();
        pfApplyFilter();
    });

    /* HSK filter trong modal */
    $('pfHskFilter').addEventListener('change', function() {
        var val = this.value;
        var allowed = getAllowedHskList();
        if (val && allowed.indexOf(val) === -1) {
            var info = getTierInfo();
            var msg = info.tier === 'trial'
                ? 'Bản Trial chỉ cho phép lọc HSK1-' + info.maxHSK + '.'
                : 'Bản Demo chỉ cho phép lọc HSK1-' + info.maxHSK + '.';
            alert(msg);
            this.value = '';
            return;
        }
        pfApplyFilter();
    });

    /* Subject filter trong modal */
    $('pfSubjectFilter').addEventListener('change', function() {
        var val = this.value;
        var allowed = getAllowedSubjectList();
        if (val && allowed.indexOf(val) === -1) {
            var info = getTierInfo();
            var msg = info.tier === 'trial'
                ? 'Chủ đề này chưa có trong ' + info.maxQuestions + ' câu Trial.'
                : 'Chủ đề này chưa có trong ' + info.maxQuestions + ' câu Demo.';
            alert(msg);
            this.value = '';
            return;
        }
        pfApplyFilter();
    });

    /* ═══════════════════════════════════════════════════════════
       KEYBOARD SHORTCUTS
       - Enter (không shift/ctrl): xuống dòng trong textarea
       - Ctrl + Arrow: prev / next
       - R: toggle random
       - Escape: đóng modal
       ═══════════════════════════════════════════════════════════ */
    document.addEventListener('keydown', function(e) {
        if (!$('practiceFullModal').classList.contains('show')) return;
        var active = document.activeElement;
        var isTyping = active && (
            active.tagName === 'INPUT' ||
            active.tagName === 'TEXTAREA' ||
            active.tagName === 'SELECT'
        );

        if (e.key === 'Escape') { closePracticeFull(); return; }

        /* Cho phép Enter xuống dòng bình thường trong textarea */
        if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) return;

        if (isTyping) return;
        if (e.key === 'ArrowRight' && e.ctrlKey) pfNext();
        if (e.key === 'ArrowLeft' && e.ctrlKey) pfPrev();
        if (e.key === 'r' || e.key === 'R') pfToggleRandom();
    });

    /* ═══════════════════════════════════════════════════════════
       SWIPE GESTURE (mobile)
       ═══════════════════════════════════════════════════════════ */
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

    /* ═══════════════════════════════════════════════════════════
       Nút loa trong ô nhập — toggle speak full
       ═══════════════════════════════════════════════════════════ */
    if (!window._pfSpeakBound) {
        window._pfSpeakBound = true;
        var speakBtn = $('pfSpeakBtn');
        if (speakBtn) {
            speakBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                e.preventDefault();
                toggleSpeakFull();
            });
        }
    }

    /* ═══════════════════════════════════════════════════════════
       Nút loa dưới nav — toggle quick speak
       ═══════════════════════════════════════════════════════════ */
    if (!window._pfQuickSpeakBound) {
        window._pfQuickSpeakBound = true;
        var quickBtn = $('pfQuickSpeakBtn');
        if (quickBtn) {
            quickBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                e.preventDefault();
                toggleQuickSpeakFull();
            });
        }
    }
}
function pfBuildDatasetSelect() {
    var sel = $('pfDatasetSelect');
    var row = $('pfDatasetRow');
    if (!sel) return;

    var canAccessAll = canAccessChuyenNganh();
    var current = (typeof CURRENT_DATASET !== 'undefined') ? CURRENT_DATASET : 'tonghop';

    sel.innerHTML = '';

    // ═══════════════════════════════════════════════════════════
    //  BƯỚC 1: Thêm dataset từ DATASET_REGISTRY (tổng hợp + chuyên ngành)
    // ═══════════════════════════════════════════════════════════
    if (typeof DATASET_REGISTRY !== 'undefined' && DATASET_REGISTRY) {
        Object.keys(DATASET_REGISTRY).forEach(function(id) {
            var ds = DATASET_REGISTRY[id];
            var isTonghop = (id === 'tonghop');
            var isLocked = !isTonghop && !canAccessAll;

            var opt = document.createElement('option');
            opt.value = id;
            if (isLocked) {
                opt.dataset.locked = '1';
                opt.className = 'locked-opt';
            }

            var dsName = ds.name && ds.name.normalize
                         ? ds.name.normalize('NFC')
                         : ds.name;

            if (isTonghop) {
                opt.textContent = (ds.count || 0) + ' câu - Tổng hợp VPCX';
            } else {
                opt.textContent = (isLocked ? '[Khoá] ' : '') +
                                  dsName + ' (' + (ds.count || 0) + ' câu)';
            }

            sel.appendChild(opt);
        });
    }

    // ═══════════════════════════════════════════════════════════
    //  BƯỚC 2: Thêm dataset từ FIXPY_DATASETS (tab "1000 Câu giao tiếp")
    //  → KHÔNG có lock (giống tab Tổng hợp)
    // ═══════════════════════════════════════════════════════════
    if (window.FIXPY_DATASETS && typeof window.FIXPY_DATASETS === 'object') {
        Object.keys(window.FIXPY_DATASETS).forEach(function(id) {
            // Skip nếu trùng với DATASET_REGISTRY
            if (typeof DATASET_REGISTRY !== 'undefined' && DATASET_REGISTRY[id]) return;

            var ds = window.FIXPY_DATASETS[id];
            var opt = document.createElement('option');
            opt.value = id;

            var dsName = ds.name && ds.name.normalize
                         ? ds.name.normalize('NFC')
                         : ds.name;

            opt.textContent = dsName + ' (' + (ds.count || 0) + ' câu)';

            sel.appendChild(opt);
        });
    }

    // ═══════════════════════════════════════════════════════════
    //  BƯỚC 3: Set giá trị hiện tại
    // ═══════════════════════════════════════════════════════════
    var currentIsValid = false;
    for (var i = 0; i < sel.options.length; i++) {
        if (sel.options[i].value === current) {
            currentIsValid = true;
            break;
        }
    }

    if (currentIsValid) {
        sel.value = current;
    } else {
        // Fallback: nếu current không có trong options → về tonghop
        sel.value = 'tonghop';
    }

    // ═══════════════════════════════════════════════════════════
    //  BƯỚC 4: Đánh dấu row có locked options
    // ═══════════════════════════════════════════════════════════
    if (row) {
        var hasLock = !canAccessAll
                      && typeof DATASET_REGISTRY !== 'undefined'
                      && Object.keys(DATASET_REGISTRY).length > 1;
        row.classList.toggle('has-locked-options', hasLock);
    }
}

document.addEventListener('change', function(e) {
    if (!e.target || e.target.id !== 'pfDatasetSelect') return;

    var sel = e.target;
    var val = sel.value;
    var opt = sel.options[sel.selectedIndex];
    var currentDataset = (typeof CURRENT_DATASET !== 'undefined') ? CURRENT_DATASET : 'tonghop';

    if (opt && opt.dataset.locked === '1') {
        sel.value = currentDataset;
        showPracticeFullLockMessage();
        return;
    }

    if (val !== 'tonghop' && !canAccessChuyenNganh()) {
        sel.value = currentDataset;
        showPracticeFullLockMessage();
        return;
    }

    var ok = (typeof window.__switchRawData === 'function')
             ? window.__switchRawData(val)
             : false;
    if (!ok) {
        sel.value = currentDataset;
        return;
    }

    window.__onboardingOverride = null;
    var obBanner = $('onboardingActiveBanner');
    if (obBanner) obBanner.remove();

    state = { search:'', hsk:'', subject:'' };
    if ($('pfSearchInput')) $('pfSearchInput').value = '';
    if ($('pfHskFilter')) $('pfHskFilter').value = '';
    if ($('pfSubjectFilter')) $('pfSubjectFilter').value = '';
    if ($('searchInput')) $('searchInput').value = '';
    if ($('hskFilter')) $('hskFilter').value = '';
    if ($('subjectFilter')) $('subjectFilter').value = '';

    if (typeof pfBuildFilterOptions === 'function') pfBuildFilterOptions();

    if (typeof pfApplyFilter === 'function') {
        pfApplyFilter();
    } else if (typeof applyFilter === 'function') {
        applyFilter();
    }

    if (typeof filtered !== 'undefined' && filtered.length > 0) {
        if (typeof loadPracticeFull === 'function') {
            loadPracticeFull(filtered[0].stt);
        }
    }

    pfBuildDatasetSelect();
});

/* ============================================================ */
/* WRITER (Luyện viết chữ Hán) — expired dùng được như Demo      */
/* ============================================================ */
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
                    $('writerScore').textContent = 'Tuyệt vời! Viết đúng tất cả các nét!';
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
    if (shouldCountUsage()) { incDemoUsage(); updateDemoRemaining(); }
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
                strokeColor: '#1e293b', radicalColor: '#7c3aed',
                highlightColor: '#f59e0b', outlineColor: '#cbd5e1',
                drawingColor: '#7c3aed', drawingWidth: drawWidth,
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
/* ═══════════════════════════════════════════════════════════════
   ❤️ FAVORITES BRIDGE — Build nút tim cho card
   ═══════════════════════════════════════════════════════════════ */
function favBuildFavButton(stt) {
    if (typeof favCanUse !== 'function') return '';

    var can = favCanUse();
    var currentDsId = (typeof CURRENT_DATASET !== 'undefined' && CURRENT_DATASET)
                      ? CURRENT_DATASET
                      : 'tonghop';

    var active = typeof favHas === 'function' ? favHas(stt, currentDsId) : false;

    var sttJs = escapeJs(stt);
    var sttSafe = escapeHtml(stt);
    var dsSafe = escapeHtml(currentDsId);

    var iconClass = !can ? 'fas fa-lock' : (active ? 'fas fa-heart' : 'far fa-heart');
    var title = !can
        ? 'Cần gia hạn để dùng Yêu thích'
        : (active ? 'Xoá khỏi yêu thích' : 'Thêm vào yêu thích');

    return '<button class="fav-btn' +
        (active ? ' active' : '') +
        (!can ? ' locked' : '') +
        '" data-stt="' + sttSafe + '" ' +
        'data-dataset-id="' + dsSafe + '" ' +
        'onclick="favOnCardBtnClick(event, \'' + sttJs + '\')" ' +
        'title="' + title + '">' +
        '<i class="' + iconClass + '"></i>' +
        '</button>';
}
"""

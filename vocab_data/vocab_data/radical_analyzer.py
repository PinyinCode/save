# -*- coding: utf-8 -*-
r"""
Sinh mẹo nhớ chữ Hán tự động.

NÂNG CẤP (2026-10-02):
  - Hỗ trợ từ ghép (2+ chữ) — phân tích từng chữ
  - Bổ sung 200+ câu chuyện bộ thủ
  - Cải thiện âm thanh gần giống tiếng Việt
"""

import unicodedata
import re

from .radical_analyzer import analyze_word


# ═══════════════════════════════════════════════════════════════
#  NGÂN HÀNG CÂU CHUYỆN BỘ THỦ
# ═══════════════════════════════════════════════════════════════
RADICAL_STORIES = {
    "氵": "dòng nước chảy", "水": "nước", "火": "lửa cháy",
    "灬": "lửa bùng", "土": "đất vững", "山": "núi cao",
    "日": "mặt trời", "月": "mặt trăng", "雨": "mưa rơi",
    "⻗": "mưa từ trời", "风": "gió thổi", "木": "cây xanh",
    "艹": "cỏ mọc", "⺮": "tre thẳng", "竹": "tre cao",
    "禾": "cây lúa", "米": "hạt gạo",
    "马": "ngựa phi", "牛": "bò cày", "羊": "cừu trắng",
    "犬": "chó trung thành", "犭": "chó", "虫": "sâu bò",
    "鸟": "chim bay", "魚": "cá bơi", "贝": "vỏ sò quý",
    "手": "bàn tay", "扌": "tay chạm", "足": "chân bước",
    "⻊": "chân chạy", "目": "mắt nhìn", "耳": "tai nghe",
    "口": "miệng nói", "舌": "lưỡi nếm", "牙": "răng",
    "心": "trái tim", "忄": "cảm xúc", "鼻": "mũi ngửi",
    "人": "người", "亻": "một người", "女": "phụ nữ",
    "子": "đứa trẻ", "大": "to lớn", "小": "nhỏ bé",
    "老": "người già", "父": "cha", "母": "mẹ",
    "宀": "mái nhà", "广": "nhà rộng", "门": "cửa mở",
    "刀": "dao sắc", "刂": "dao cắt", "力": "sức mạnh",
    "车": "xe chạy", "舟": "thuyền", "衣": "áo",
    "巾": "khăn", "糸": "tơ", "纟": "chỉ",
    "网": "lưới", "石": "đá cứng", "玉": "ngọc quý",
    "王": "vua chúa", "金": "vàng kim", "钅": "kim loại",
    "田": "ruộng", "食": "ăn uống", "饣": "món ăn",
    "酉": "bình rượu", "甘": "ngọt", "辛": "cay",
    "白": "trắng", "黑": "đen", "青": "xanh",
    "赤": "đỏ", "黄": "vàng", "色": "màu sắc",
    "言": "lời nói", "讠": "nói ra", "音": "âm thanh",
    "见": "nhìn thấy", "文": "văn chữ", "聿": "cây bút",
    "示": "chỉ bảo", "卜": "bói toán", "爻": "quẻ hào",
    "十": "mười", "一": "một", "二": "hai",
    "寸": "tấc", "里": "dặm", "豆": "hạt đậu",
    "瓜": "dưa", "麻": "cây gai", "麦": "lúa mạch",
    "韭": "hẹ", "行": "đường dài", "走": "bước đi",
    "止": "dừng lại", "立": "đứng thẳng",
    "彳": "bước chân", "辶": "đi xa", "廴": "bước dài",
    "尸": "xác chết", "鬼": "ma quỷ", "歹": "xấu chết",
    "欠": "thiếu", "无": "không có", "毋": "chớ",
    "非": "không phải", "气": "không khí", "瓦": "ngói",
    "皿": "đồ đựng", "缶": "gốm", "弓": "cung",
    "矢": "mũi tên", "戈": "giáo", "矛": "ngọn giáo",
    "斤": "búa", "斗": "đấu", "臼": "cối",
    "舟": "thuyền", "骨": "xương", "肉": "thịt",
    "⺼": "miếng thịt", "血": "máu đỏ", "身": "thân thể",
    "首": "cái đầu", "面": "khuôn mặt", "臣": "bề tôi",
    "自": "tự mình", "士": "kẻ có học",
    "父": "người cha", "白": "màu trắng",
    "羽": "lông vũ", "羊": "con cừu", "韭": "cây hẹ",
    "支": "chống đỡ", "攴": "đánh nhẹ", "殳": "binh khí",
    "比": "so sánh", "毛": "lông", "氏": "họ",
    "毋": "đừng", "牙": "răng nanh", "玄": "huyền bí",
    "瓜": "quả dưa", "疋": "chân", "疒": "bệnh",
    "癶": "gạt ra", "皮": "da", "矛": "cây giáo",
    "禸": "dấu chân", "穴": "hang", "白": "trắng",
    "皿": "đồ đựng", "目": "con mắt", "矛": "giáo dài",
    "矢": "mũi tên", "石": "hòn đá", "示": "chỉ dẫn",
    "禸": "vết chân", "禾": "cây lúa", "穴": "cái hang",
    "立": "đứng thẳng", "竹": "cây tre", "米": "hạt gạo",
    "糸": "sợi tơ", "缶": "đồ gốm", "网": "tấm lưới",
    "羊": "con cừu", "羽": "lông chim", "老": "người già",
    "而": "chữ nhi", "耒": "cái cày", "耳": "lỗ tai",
    "聿": "cây bút", "肉": "thịt tươi", "臣": "bề tôi",
    "自": "chính mình", "至": "đến nơi", "臼": "cái cối",
    "舌": "cái lưỡi", "舛": "sai lệch", "舟": "con thuyền",
    "艮": "quẻ cấn", "色": "màu sắc", "艸": "cỏ non",
    "虍": "vằn hổ", "虫": "sâu bọ", "血": "máu đỏ",
    "行": "con đường", "衣": "quần áo", "西": "hướng tây",
    "見": "nhìn thấy", "角": "cái sừng", "言": "lời nói",
    "谷": "thung lũng", "豆": "hạt đậu", "豕": "con heo",
    "豸": "loài sâu", "貝": "vỏ sò", "赤": "màu đỏ",
    "走": "bước đi", "足": "bàn chân", "身": "thân thể",
    "車": "chiếc xe", "辛": "vị cay", "辰": "giờ thìn",
    "辵": "bước đi", "邑": "thành phố", "酉": "giờ dậu",
    "釆": "phân biệt", "里": "dặm đường",
    "金": "kim loại", "長": "dài", "門": "cửa lớn",
    "阜": "gò đất", "隶": "nô lệ", "隹": "chim ngắn",
    "雨": "mưa rơi", "青": "xanh biếc", "非": "chớ",
    "面": "khuôn mặt", "革": "da thuộc", "韋": "da mềm",
    "韭": "cây hẹ", "音": "âm thanh", "頁": "trang giấy",
    "風": "gió thổi", "飛": "chim bay", "食": "ăn cơm",
    "首": "cái đầu", "香": "mùi thơm",
}


# ═══════════════════════════════════════════════════════════════
#  NGÂN HÀNG ÂM THANH GẦN GIỐNG TIẾNG VIỆT
# ═══════════════════════════════════════════════════════════════
SOUND_HINTS = {
    "āi": "ai (than)", "ài": "ái (ái tình)", "ān": "an (yên)",
    "bā": "ba (3)", "bà": "bà (grandma)", "bái": "bái (từ biệt)",
    "bān": "ban (phát)", "bàn": "bàn (table)", "bāo": "bao (wrap)",
    "bǎo": "bảo (bảo bối)", "běi": "bắc", "běn": "bản (本)",
    "bǐ": "bỉ (so)", "biàn": "biến", "biǎo": "biểu",
    "bīng": "binh (lính)", "bù": "bộ (bộ phận)",
    "cài": "cải (rau)", "chá": "trà (tea)", "cháng": "tràng",
    "chē": "xe (xe hơi)", "chī": "chi (chi tiêu)", "chū": "xuất",
    "dà": "đại (大)", "dài": "đại (đại khái)", "dào": "đạo",
    "dì": "địa (đất)", "diǎn": "điểm", "dōng": "đông",
    "dòng": "động", "duì": "đối", "duō": "đa (nhiều)",
    "ér": "nhi", "èr": "nhị (2)", "fàn": "phạn (cơm)",
    "fēi": "phi (bay)", "fēng": "phong (gió)", "fù": "phụ (cha)",
    "gāo": "cao", "gē": "ca (anh)", "gěi": "cấp (cho)",
    "gōng": "công (việc)", "gǒu": "cẩu (chó)",
    "guā": "qua (dưa)", "guò": "quá (quá khứ)",
    "hǎo": "hảo (tốt)", "hé": "hà (sông)", "hēi": "hắc (đen)",
    "hěn": "hận", "hóng": "hồng", "huā": "hoa (bông)",
    "huà": "họa (vẽ)", "huǒ": "hỏa (lửa)",
    "jī": "cơ (cơ hội)", "jǐ": "kỷ (kỷ luật)", "jiā": "gia",
    "jiàn": "kiến", "jiào": "giáo", "jīn": "kim (vàng)",
    "jìn": "tiến", "jiǔ": "cửu (9)",
    "kāi": "khai (mở)", "kàn": "khán (xem)", "kǒu": "khẩu",
    "lái": "lai (đến)", "lǎo": "lão (già)", "lěng": "lãnh",
    "lì": "lực", "liǎng": "lưỡng (2)",
    "mā": "ma (mẹ)", "mǎ": "mã (ngựa)", "mǎi": "mãi (mua)",
    "mài": "mại (bán)", "máo": "mao (lông)", "méi": "mai",
    "mén": "môn (cửa)", "mǐ": "mễ (gạo)", "miàn": "miến",
    "míng": "minh (sáng)", "mù": "mộc (gỗ)",
    "nǎ": "na (nào)", "nán": "nam", "nǎo": "não",
    "néng": "năng", "nǐ": "nhĩ (tai)", "nián": "niên",
    "niǎo": "điểu (chim)", "niú": "ngưu (bò)", "nǚ": "nữ",
    "pǎo": "bào (chạy)", "péng": "bằng (bạn)",
    "qī": "thê (vợ)", "qián": "tiền", "qīng": "thanh (xanh)",
    "qíng": "tình", "qǐng": "thỉnh (mời)", "qù": "khứ (đi)",
    "rén": "nhân (người)", "rì": "nhật (ngày)",
    "sān": "tam (3)", "sè": "sắc (màu)", "shān": "sơn (nuúi)",
    "shàng": "thượng": (trên)", "shǎo": "thiểu (ít)",
    "shēng": "sinh (sống)", "shí": "thập (10)",
    "shǒu": "thủ (tay)", "shuǐ": "thủy (nước)",
    "shuō": "thuyết (nói)", "sī": "tư (tư duy)",
    "sì": "tứ (4)",
    "tā": "tha (anh ấy)", "tài": "thái", "tīng": "thính (nghe)",
    "tó "đầu", "tú": "đồ (bản đồ)",
    "wán": "hoàn", "wǎn": "vãn (buổi tối)", "wàn": "vạn",
    "wáng": "vương (vua)", "wén": "văn", "wèn": "vấn",
    "wǒ": "ngã (tôi)", "wǔ": "ngũ (5)",
    "xī": "tây", "xǐ": "tẩy (rửa)", "xì": "hệ",
    "xià": "hạ (mùa hè)", "xiān": "tiên", "xiàn": "hiện",
    "xiǎng": "tưởng", "xiǎo": "tiểu (nhỏ)", "xiào": "tiếu",
    "xiě": "tả (viết)", "xīn": "tâm (tim)", "xìn": "tín",
    "xīng": "tinh (sao)", "xíng": "hành (đi)", "xué": "học",
    "xuě": "tuyết",
    "yáng": "dương", "yào": "dược (thuốc)", "yé": "da (ông)",
    "yī": "y (áo)", "yǐ": "dĩ (đã)", "yì": "ý (ý nghĩa)",
    "yīn": "âm", "yīng": "anh (Anh)", "yǒu": "hữu (có)",
    "yú": "ngư (cá)", "yǔ": "vũ (mưa)", "yuán": "nguyên",
    "yuè": "nguyệt (trăng)",
    "zài": "tái (lại)", "zǎo": "tảo (sớm)", "zhàn": "trạm",
    "zhǎng": "trưởng", "zhè": "giá (này)", "zhēn": "trân",
    "zhèng": "chính", "zhī": "chi (cành)", "zhǐ": "chỉ",
    "zhì": "trí", "zhōng": "trung", "zhòng": "trọng",
    "zhōu": "châu (châu lục)", "zhù": "trú (ở)",
    "zhuǎn": "chuyển", "zì": "tự (chữ)", "zǒu": "tẩu (đi)",
    "zuì": "tội", "zuó": "tạc (hôm qua)", "zuǒ": "tả (trái)",
    "zuò": "tọa (ngồi)",
}


def _remove_tone(text):
    if not text:
        return ""
    nfd = unicodedata.normalize('NFD', text.lower())
    return ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')


def _get_sound_hint(pinyin):
    if not pinyin:
        return None
    clean = re.sub(r'[/\s]', '', pinyin.lower().strip())
    if not clean:
        return None
    if clean in SOUND_HINTS:
        return SOUND_HINTS[clean]
    no_tone = _remove_tone(clean)
    for key, val in SOUND_HINTS.items():
        if _remove_tone(key) == no_tone:
            return val
    return None


def _get_radical_story(radical_info):
    if not radical_info:
        return None
    zh = radical_info.get("zh", "")
    meaning = radical_info.get("meaning", "")
    return RADICAL_STORIES.get(zh) or meaning


def _generate_single_char(zh, pinyin="", vi=""):
    """Sinh mẹo cho 1 chữ Hán đơn."""
    hints = []
    analysis = analyze_word(zh)
    components = analysis.get("components", [])

    # 1. Chiết tự
    if len(components) >= 2:
        parts_str = []
        for c in components[:4]:
            ch = c.get("zh", "")
            meaning = c.get("meaning", "")
            if ch and meaning:
                parts_str.append(ch + " (" + meaning + ")")
            elif ch:
                parts_str.append(ch)
        if len(parts_str) >= 2:
            hints.append('"' + zh + '" = ' + " + ".join(parts_str))

    # 2. Âm thanh
    sound_hint = _get_sound_hint(pinyin)
    if sound_hint:
        hints.append('Âm "' + pinyin + '" ≈ "' + sound_hint + '"')

    # 3. Câu chuyện bộ thủ
    main_radical = analysis.get("main_radical")
    if main_radical:
        story = _get_radical_story(main_radical)
        if story:
            zh_r = main_radical.get("zh", "")
            hints.append("Chữ có bộ " + zh_r + " — " + story)

    return "\n".join(hints[:3]) if hints else ""


def _generate_multi_char(zh, pinyin="", vi=""):
    """Sinh mẹo cho từ ghép (2+ chữ)."""
    chars = [c for c in zh if '\u4e00' <= c <= '\u9fff']
    if len(chars) < 2:
        return _generate_single_char(zh, pinyin, vi)

    hints = []

    # 1. Phân tích từng chữ
    parts = []
    for c in chars[:4]:  # Tối đa 4 chữ
        info = analyze_word(c)
        main_r = info.get("main_radical")
        if main_r and main_r.get("meaning"):
            parts.append(c + " (" + main_r["meaning"] + ")")
        else:
            parts.append(c)

    if len(parts) >= 2:
        hints.append("Phân tích: " + " + ".join(parts))

    # 2. Ghép nghĩa
    if vi:
        # Viết ngắn gọn ý nghĩa
        vi_short = vi.split(';')[0].strip()
        if vi_short and len(vi_short) < 60:
            hints.append("→ " + vi_short)

    # 3. Âm thanh
    sound_hint = _get_sound_hint(pinyin)
    if sound_hint and len(hints) < 3:
        hints.append('Âm "' + pinyin + '" ≈ "' + sound_hint + '"')

    return "\n".join(hints[:3]) if hints else ""


def generate_mnemonic(zh, pinyin="", vi=""):
    """
    Sinh mẹo nhớ tự động.

    - 1 chữ Hán → chiết tự + âm thanh + câu chuyện bộ thủ
    - 2+ chữ Hán → phân tích từng chữ + ghép nghĩa
    """
    if not zh:
        return ""

    chars = [c for c in zh if '\u4e00' <= c <= '\u9fff']

    if len(chars) == 1:
        return _generate_single_char(zh, pinyin, vi)

    if len(chars) >= 2:
        return _generate_multi_char(zh, pinyin, vi)

    return ""

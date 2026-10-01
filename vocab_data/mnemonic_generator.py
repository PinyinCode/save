# -*- coding: utf-8 -*-
"""
Sinh mẹo nhớ chữ Hán tự động.

3 phương pháp kết hợp:
  1. Chiết tự — phân tích thành phần
  2. Liên tưởng âm thanh — pinyin ≈ tiếng Việt
  3. Câu chuyện bộ thủ — ý nghĩa của bộ
"""

import unicodedata
import re

from .radical_analyzer import analyze_word


# ═══════════════════════════════════════════════════════════════
#  NGÂN HÀNG CÂU CHUYỆN CHO BỘ THỦ
# ═══════════════════════════════════════════════════════════════
RADICAL_STORIES = {
    # ═══ Tự nhiên ═══
    "氵": "dòng nước chảy",
    "水": "dòng nước",
    "火": "ngọn lửa cháy",
    "灬": "lửa bùng lên",
    "土": "đất đai vững chắc",
    "山": "ngọn núi cao",
    "日": "mặt trời chiếu sáng",
    "月": "ánh trăng dịu",
    "雨": "cơn mưa rơi",
    "⻗": "mưa từ trời",
    "风": "cơn gió thổi",
    "木": "cây cối xanh tươi",
    "艹": "cỏ mọc xanh",
    "⺮": "cây tre thẳng",
    "竹": "cây tre cao",
    "禾": "cây lúa",
    "米": "hạt gạo",

    # ═══ Động vật ═══
    "马": "con ngựa phi",
    "马": "con ngựa chạy",
    "牛": "con bò cày",
    "羊": "con cừu trắng",
    "犬": "con chó trung thành",
    "犭": "con chó",
    "虫": "con sâu bò",
    "鸟": "con chim bay",
    "鳥": "con chim hót",
    "鱼": "con cá bơi",
    "魚": "con cá lội",
    "贝": "vỏ sò quý",
    "貝": "vỏ sò làm tiền",
    "鼠": "con chuột",
    "龙": "con rồng huyền thoại",
    "龍": "con rồng thiêng",

    # ═══ Cơ thể ═══
    "手": "bàn tay làm việc",
    "扌": "bàn tay chạm",
    "足": "đôi chân bước",
    "⻊": "đôi chân chạy",
    "目": "đôi mắt nhìn",
    "耳": "đôi tai nghe",
    "口": "cái miệng nói",
    "舌": "cái lưỡi nếm",
    "牙": "hàm răng",
    "齿": "răng trắng",
    "骨": "xương cứng",
    "肉": "thịt mềm",
    "⺼": "miếng thịt",
    "血": "dòng máu đỏ",
    "心": "trái tim, tình cảm",
    "忄": "cảm xúc từ trái tim",
    "鼻": "cái mũi ngửi",
    "面": "khuôn mặt",
    "首": "cái đầu",

    # ═══ Con người ═══
    "人": "con người",
    "亻": "một người đứng",
    "女": "người phụ nữ",
    "子": "đứa trẻ",
    "大": "người dang tay (to lớn)",
    "小": "nhỏ bé",
    "老": "người già",
    "父": "người cha",
    "士": "kẻ có học",
    "臣": "bề tôi trung thành",
    "自": "chính mình",
    "身": "thân thể",

    # ═══ Đồ vật ═══
    "宀": "mái nhà che",
    "广": "ngôi nhà rộng",
    "门": "cánh cửa mở",
    "門": "cánh cửa lớn",
    "戶": "cửa nhà",
    "刀": "con dao sắc",
    "刂": "lưỡi dao cắt",
    "力": "sức mạnh",
    "车": "chiếc xe chạy",
    "車": "chiếc xe lăn",
    "舟": "con thuyền",
    "衣": "bộ quần áo",
    "衤": "áo mặc",
    "巾": "chiếc khăn",
    "糸": "sợi tơ mảnh",
    "纟": "sợi chỉ",
    "网": "tấm lưới",
    "罒": "lưới bắt cá",
    "石": "hòn đá cứng",
    "玉": "viên ngọc quý",
    "王": "vua chúa",
    "金": "vàng, kim loại",
    "钅": "kim loại sáng bóng",
    "皿": "đồ đựng",
    "缶": "đồ gốm",
    "酉": "bình rượu",
    "田": "thửa ruộng",
    "瓦": "viên ngói",
    "弓": "cây cung",
    "矢": "mũi tên",
    "戈": "cây giáo",
    "矛": "ngọn giáo",
    "斤": "cái búa",
    "斗": "cái đấu",

    # ═══ Màu sắc ═══
    "白": "màu trắng tinh",
    "黑": "màu đen",
    "青": "màu xanh",
    "赤": "màu đỏ",
    "黄": "màu vàng",
    "黃": "màu vàng",
    "色": "màu sắc",

    # ═══ Vị giác ═══
    "甘": "vị ngọt",
    "辛": "vị cay, vất vả",
    "香": "mùi thơm",

    # ═══ Hành động ═══
    "彳": "bước chân đi",
    "辶": "bước đi xa",
    "廴": "bước dài",
    "行": "con đường dài",
    "走": "bước đi",
    "止": "dừng lại",
    "立": "đứng thẳng",
    "食": "ăn uống",
    "饣": "món ăn",
    "言": "lời nói",
    "讠": "lời nói phát ra",
    "音": "âm thanh",
    "见": "nhìn thấy",
    "見": "nhìn thấy",

    # ═══ Trừu tượng ═══
    "示": "chỉ bảo",
    "卜": "bói toán",
    "爻": "quẻ hào",
    "文": "văn chữ",
    "聿": "cây bút",
    "釆": "phân biệt",
    "非": "không phải",
    "无": "không có gì",
    "毋": "chớ, đừng",
    "欠": "thiếu thốn",
    "歹": "xấu, chết chóc",
    "尸": "xác chết",
    "鬼": "ma quỷ",

    # ═══ Đơn vị ═══
    "一": "một",
    "二": "hai",
    "十": "mười",
    "寸": "tấc",
    "里": "dặm",
    "豆": "hạt đậu",
    "瓜": "quả dưa",
    "麻": "cây gai",
    "麦": "lúa mạch",
    "麥": "lúa mạch",
    "黍": "lúa nếp",
    "韭": "cây hẹ",
}


# ═══════════════════════════════════════════════════════════════
#  NGÂN HÀNG ÂM THANH GẦN GIỐNG TIẾNG VIỆT
# ═══════════════════════════════════════════════════════════════
SOUND_HINTS = {
    # ═══ A ═══
    "āi": "ai (than thở)",
    "ài": "ái (ái tình)",
    "ān": "an (yên ổn)",
    "ào": "áo (áo quần)",
    # ═══ B ═══
    "bā": "ba (số ba)",
    "bà": "bà (người bà)",
    "bái": "bái (bái biệt)",
    "bān": "ban (ban phát)",
    "bàn": "bàn (cái bàn)",
    "bāo": "bao (bao bọc)",
    "bǎo": "bảo (bảo bối)",
    "běi": "bắc (hướng bắc)",
    "běn": "bản (bản thân)",
    "bǐ": "bỉ (so bì)",
    "bì": "bì (bì ẩn)",
    "biàn": "biến (biến đổi)",
    "biǎo": "biểu (biểu diễn)",
    "bié": "biệt (biệt ly)",
    "bīng": "binh (binh lính)",
    "bù": "bộ (bộ phận)",
    # ═══ C ═══
    "cài": "cải (rau cải)",
    "chá": "trà (uống trà)",
    "cháng": "tràng (ruột)",
    "chàng": "chàng (chàng trai)",
    "chē": "xe (chiếc xe)",
    "chī": "chi (chi tiêu)",
    "chū": "xuất (xuất hiện)",
    "cì": "thứ (thứ tự)",
    "cóng": "tùng (cây tùng)",
    # ═══ D ═══
    "dà": "đại (to lớn)",
    "dài": "đại (đại khái)",
    "dào": "đạo (đạo lý)",
    "dì": "địa (đất đai)",
    "diǎn": "điểm (điểm số)",
    "dōng": "đông (mùa đông)",
    "dòng": "động (động vật)",
    "duì": "đối (đối diện)",
    "duō": "đa (đa số)",
    # ═══ E ═══
    "ér": "nhi (nhi đồng)",
    "èr": "nhị (số 2)",
    # ═══ F ═══
    "fàn": "phạn (cơm)",
    "fēi": "phi (bay)",
    "fēng": "phong (gió)",
    "fú": "phúc (phúc lợi)",
    "fù": "phụ (cha)",
    # ═══ G ═══
    "gāo": "cao (cao thấp)",
    "gē": "ca (anh trai)",
    "gè": "cá (cá nhân)",
    "gěi": "cấp (cấp cho)",
    "gēn": "căn (căn nhà)",
    "gōng": "công (công việc)",
    "gǒu": "cẩu (con chó)",
    "guā": "qua (quả dưa)",
    "guò": "quá (quá khứ)",
    # ═══ H ═══
    "hǎo": "hảo (tốt)",
    "hào": "hào (hào phóng)",
    "hé": "hà (con sông)",
    "hē": "ha (cười ha)",
    "hēi": "hắc (màu đen)",
    "hěn": "hận (thù hận)",
    "hóng": "hồng (màu đỏ)",
    "hòu": "hậu (sau)",
    "huā": "hoa (bông hoa)",
    "huà": "họa (bức họa)",
    "huǒ": "hỏa (lửa)",
    # ═══ J ═══
    "jī": "cơ (cơ hội)",
    "jǐ": "kỷ (kỷ luật)",
    "jiā": "gia (gia đình)",
    "jiàn": "kiến (kiến thức)",
    "jiào": "giáo (giáo dục)",
    "jīn": "kim (kim loại)",
    "jìn": "tiến (tiến bộ)",
    "jiǔ": "cửu (số 9)",
    # ═══ K ═══
    "kāi": "khai (khai mở)",
    "kàn": "khán (xem)",
    "kǎo": "khảo (khảo sát)",
    "kǒu": "khẩu (miệng)",
    "kū": "khốc (khóc)",
    # ═══ L ═══
    "lái": "lai (đến)",
    "lǎo": "lão (già)",
    "lè": "lạc (vui vẻ)",
    "lěng": "lãnh (lạnh)",
    "lì": "lực (sức lực)",
    "liǎng": "lưỡng (hai)",
    # ═══ M ═══
    "mā": "ma (mẹ)",
    "mǎ": "mã (con ngựa)",
    "mǎi": "mãi (mua)",
    "mài": "mại (bán)",
    "máng": "mang (mang vác)",
    "máo": "mao (lông)",
    "mào": "mạo (mạo hiểm)",
    "méi": "mai (hoa mai)",
    "mèi": "muội (em gái)",
    "mén": "môn (cửa)",
    "mǐ": "mễ (gạo)",
    "miàn": "miến (mặt)",
    "míng": "minh (sáng)",
    "mù": "mộc (gỗ)",
    # ═══ N ═══
    "nǎ": "na (nào)",
    "nán": "nam (phía nam)",
    "nǎo": "não (bộ não)",
    "ne": "nê (đâu)",
    "néng": "năng (khả năng)",
    "nǐ": "nhĩ (tai)",
    "nián": "niên (năm)",
    "niǎo": "điểu (chim)",
    "niú": "ngưu (bò)",
    "nǚ": "nữ (phụ nữ)",
    "nuǎn": "noãn (ấm áp)",
    # ═══ P ═══
    "pàng": "bàng (bên cạnh)",
    "pǎo": "bào (chạy)",
    "péng": "bằng (bạn)",
    "piào": "phiếu (vé)",
    "piào": "phiêu (phiêu bạt)",
    # ═══ Q ═══
    "qī": "thê (vợ)",
    "qí": "kỳ (kỳ lạ)",
    "qián": "tiền (tiền bạc)",
    "qiáng": "cường (mạnh)",
    "qīng": "thanh (xanh)",
    "qíng": "tình (tình cảm)",
    "qǐng": "thỉnh (mời)",
    "qù": "khứ (đi)",
    "quán": "quyền (quyền lực)",
    # ═══ R ═══
    "rán": "nhiên (tự nhiên)",
    "rén": "nhân (người)",
    "rèn": "nhận (nhận biết)",
    "rì": "nhật (ngày)",
    "róng": "dung (dung mạo)",
    # ═══ S ═══
    "sān": "tam (số 3)",
    "sè": "sắc (màu sắc)",
    "shān": "sơn (núi)",
    "shàng": "thượng (trên)",
    "shǎo": "thiểu (ít)",
    "shé": "xà (con rắn)",
    "shēng": "sinh (sống)",
    "shí": "thập (mười)",
    "shì": "thị (chợ)",
    "shǒu": "thủ (tay)",
    "shū": "thư (sách)",
    "shuǐ": "thủy (nước)",
    "shuō": "thuyết (nói)",
    "sī": "tư (tư duy)",
    "sì": "tứ (số 4)",
    "sòng": "tống (đưa tiễn)",
    "suì": "tuế (năm)",
    # ═══ T ═══
    "tā": "tha (anh ấy)",
    "tài": "thái (thái độ)",
    "tán": "đàm (đàm thoại)",
    "tāng": "canh (canh súp)",
    "táo": "đào (quả đào)",
    "tīng": "thính (nghe)",
    "tǔ": "thổ (đất)",
    "tóu": "đầu (đầu tiên)",
    "tú": "đồ (bản đồ)",
    # ═══ W ═══
    "wán": "hoàn (hoàn thành)",
    "wǎn": "vãn (buổi tối)",
    "wàn": "vạn (vạn vật)",
    "wáng": "vương (vua)",
    "wàng": "vọng (hy vọng)",
    "wén": "văn (văn chương)",
    "wèn": "vấn (vấn đề)",
    "wǒ": "ngã (tôi)",
    "wǔ": "ngũ (số 5)",
    # ═══ X ═══
    "xī": "tây (hướng tây)",
    "xǐ": "tẩy (rửa)",
    "xì": "hệ (hệ thống)",
    "xià": "hạ (mùa hè)",
    "xiān": "tiên (trước)",
    "xiàn": "hiện (hiện tại)",
    "xiǎng": "tưởng (tưởng tượng)",
    "xiàng": "tượng (hình tượng)",
    "xiǎo": "tiểu (nhỏ)",
    "xiào": "tiếu (cười)",
    "xiě": "tả (viết)",
    "xīn": "tâm (tim)",
    "xìn": "tín (tin tưởng)",
    "xīng": "tinh (ngôi sao)",
    "xíng": "hành (hành động)",
    "xué": "học (học tập)",
    "xuě": "tuyết (tuyết rơi)",
    # ═══ Y ═══
    "yáng": "dương (mặt trời)",
    "yào": "dược (thuốc)",
    "yé": "da (ông)",
    "yě": "dã (hoang dã)",
    "yī": "y (áo)",
    "yí": "di (di chuyển)",
    "yǐ": "dĩ (đã)",
    "yì": "ý (ý nghĩa)",
    "yīn": "âm (âm thanh)",
    "yín": "ngân (bạc)",
    "yīng": "anh (nước Anh)",
    "yóu": "du (du lịch)",
    "yǒu": "hữu (có)",
    "yòu": "hữu (bên phải)",
    "yú": "ngư (cá)",
    "yǔ": "vũ (mưa)",
    "yuán": "nguyên (nguồn)",
    "yuè": "nguyệt (trăng)",
    # ═══ Z ═══
    "zài": "tái (lần nữa)",
    "zǎo": "tảo (sớm)",
    "zěn": "chẩm (gối)",
    "zhàn": "trạm (trạm dừng)",
    "zhǎng": "trưởng (lớn lên)",
    "zhè": "giá (đây)",
    "zhēn": "trân (quý)",
    "zhèng": "chính (đúng)",
    "zhī": "chi (cành)",
    "zhí": "trực (thẳng)",
    "zhǐ": "chỉ (dừng lại)",
    "zhì": "trí (trí tuệ)",
    "zhōng": "trung (giữa)",
    "zhòng": "trọng (nặng)",
    "zhōu": "châu (châu lục)",
    "zhù": "trú (ở)",
    "zhuā": "trảo (nắm)",
    "zhuǎn": "chuyển (chuyển đổi)",
    "zì": "tự (chữ)",
    "zǒu": "tẩu (đi)",
    "zuì": "tội (tội lỗi)",
    "zuó": "tạc (hôm qua)",
    "zuǒ": "tả (bên trái)",
    "zuò": "tọa (ngồi)",
}


# ═══════════════════════════════════════════════════════════════
#  HELPER
# ═══════════════════════════════════════════════════════════════
def _remove_tone(text):
    """Bỏ dấu thanh → so sánh dễ."""
    if not text:
        return ""
    nfd = unicodedata.normalize('NFD', text.lower())
    return ''.join(c for c in nfd if unicodedata.category(c) != 'Mn')


def _get_sound_hint(pinyin):
    """Tra âm thanh gần giống tiếng Việt."""
    if not pinyin:
        return None

    # Chuẩn hoá
    clean = re.sub(r'[/\s]', '', pinyin.lower().strip())
    if not clean:
        return None

    # Thử match trực tiếp
    if clean in SOUND_HINTS:
        return SOUND_HINTS[clean]

    # Thử bỏ dấu
    no_tone = _remove_tone(clean)
    for key, val in SOUND_HINTS.items():
        if _remove_tone(key) == no_tone:
            return val

    return None


def _get_radical_story(radical_info):
    """Lấy câu chuyện cho bộ thủ."""
    if not radical_info:
        return None
    zh = radical_info.get("zh", "")
    meaning = radical_info.get("meaning", "")
    return RADICAL_STORIES.get(zh) or meaning


# ═══════════════════════════════════════════════════════════════
#  API CHÍNH
# ═══════════════════════════════════════════════════════════════
def generate_mnemonic(zh, pinyin="", vi=""):
    """
    Sinh mẹo nhớ tự động cho 1 từ.
    
    Returns:
        str — mẹo nhớ (có thể nhiều dòng, cách nhau bằng \n)
        "" — nếu không sinh được
    """
    if not zh:
        return ""

    hints = []

    # ═══ Phân tích chữ ═══
    analysis = analyze_word(zh)
    components = analysis.get("components", [])
    chars = analysis.get("chars", [])

    # ═══ 1. Chiết tự (chỉ cho từ 1 chữ) ═══
    if len(chars) == 1 and len(components) >= 2:
        # Format: "爱" = 爫 (tay) + 冖 (che) + 友 (bạn)
        parts_str = []
        for c in components[:4]:  # Tối đa 4 thành phần
            ch = c.get("zh", "")
            meaning = c.get("meaning", "")
            if ch and meaning:
                parts_str.append(ch + " (" + meaning + ")")
            elif ch:
                parts_str.append(ch)

        if len(parts_str) >= 2:
            breakdown = " + ".join(parts_str)
            hints.append('"' + zh + '" = ' + breakdown)

    # ═══ 2. Liên tưởng âm thanh ═══
    sound_hint = _get_sound_hint(pinyin)
    if sound_hint:
        hints.append('Âm "' + pinyin + '" ≈ "' + sound_hint + '"')

    # ═══ 3. Câu chuyện bộ thủ chính ═══
    main_radical = analysis.get("main_radical")
    if main_radical:
        story = _get_radical_story(main_radical)
        if story:
            zh_r = main_radical.get("zh", "")
            hints.append("Chữ có bộ " + zh_r + " — " + story)

    # ═══ Kết hợp ═══
    if not hints:
        return ""

    # Nối tối đa 3 hint
    return "\n".join(hints[:3])

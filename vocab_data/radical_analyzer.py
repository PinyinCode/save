# -*- coding: utf-8 -*-
"""
Phân tích chữ Hán → tìm bộ thủ chính + liệt kê các thành phần.

Cách hoạt động:
  1. Tách chữ Hán thành các ký tự
  2. Với mỗi ký tự, kiểm tra có phải bộ thủ không
  3. Với từ 1 chữ (VD: 爱), tìm tất cả bộ thủ cấu thành
  4. Chọn bộ thủ "chính" (thường là bộ thủ có ý nghĩa nhất)
"""

from .radicals_db import get_radical_info, RADICALS


# ═══════════════════════════════════════════════════════════════
#  VỊ TRÍ BỘ THỦ TRONG CHỮ (theo kinh nghiệm)
# ═══════════════════════════════════════════════════════════════
RADICAL_POSITION_HINTS = {
    "氵": "left", "忄": "left", "扌": "left", "讠": "left",
    "钅": "left", "饣": "left", "纟": "left", "犭": "left",
    "亻": "left", "刂": "right", "⻏": "right", "⻖": "left",
    "艹": "top", "⺮": "top", "⻗": "top", "宀": "top",
    "灬": "bottom", "⺼": "left", "⻊": "left", "辶": "bottom",
    "罒": "top", "爫": "top", "冫": "left",
}


def _get_position(char):
    """Đoán vị trí bộ thủ trong chữ."""
    return RADICAL_POSITION_HINTS.get(char, "unknown")


# ═══════════════════════════════════════════════════════════════
#  TÌM THÀNH PHẦN CỦA 1 CHỮ
# ═══════════════════════════════════════════════════════════════
def find_components_in_char(char):
    """
    Tìm tất cả bộ thủ cấu thành 1 chữ Hán.
    VD: '爱' → [爪 (tay), 冖 (che), 友 (bạn)]
    
    Cách tiếp cận: 
      - Kiểm tra từng ký tự có phải bộ thủ
      - Với từ 1 chữ phức tạp, phân tích "theo trực giác"
    """
    if not char:
        return []

    # Nếu char chính nó là bộ thủ đơn giản → trả về 1
    direct = get_radical_info(char)
    if direct and char in RADICALS:
        # Bộ thủ đơn lẻ
        return [{
            "zh": char,
            "pinyin": direct["pinyin"],
            "strokes": direct["strokes"],
            "meaning": direct["meaning"],
            "position": "self",
        }]

    # Nếu không phải bộ thủ, thử tìm thành phần
    return _split_components(char)


# ═══════════════════════════════════════════════════════════════
#  BẢNG TRA CỨU THỦ CÔNG CHO CHỮ PHỔ BIẾN
#  (vì Python không thể "nhìn" cấu trúc chữ Hán)
# ═══════════════════════════════════════════════════════════════
MANUAL_DECOMPOSITIONS = {
    # ═══ HSK 1 — chữ thường gặp ═══
    "爱": ["爫", "冖", "友"],
    "爸": ["父", "巴"],
    "妈": ["女", "马"],
    "好": ["女", "子"],
    "你": ["亻", "尔"],
    "他": ["亻", "也"],
    "她": ["女", "也"],
    "们": ["亻", "门"],
    "谁": ["讠", "隹"],
    "什": ["亻", "十"],
    "么": ["丿", "厶"],
    "这": ["辶", "文"],
    "那": ["阝", "冄"],
    "哪": ["口", "那"],
    "儿": ["儿"],
    "子": ["子"],
    "女": ["女"],
    "男": ["田", "力"],
    "父": ["父"],
    "母": ["母"],
    "大": ["大"],
    "小": ["小"],
    "多": ["夕", "夕"],
    "少": ["小", "丿"],
    "上": ["上"],
    "下": ["下"],
    "中": ["口", "丨"],
    "国": ["囗", "玉"],
    "人": ["人"],
    "天": ["一", "大"],
    "地": ["土", "也"],
    "日": ["日"],
    "月": ["月"],
    "年": ["丿", "干"],
    "时": ["日", "寸"],
    "分": ["八", "刀"],
    "秒": ["禾", "少"],
    "今": ["人", "丶"],
    "明": ["日", "月"],
    "昨": ["日", "乍"],
    "早": ["日", "十"],
    "晚": ["日", "免"],
    "星": ["日", "生"],
    "期": ["其", "月"],

    # ═══ HSK 1 — hoạt động ═══
    "吃": ["口", "乞"],
    "喝": ["口", "曷"],
    "说": ["讠", "兑"],
    "话": ["讠", "舌"],
    "听": ["口", "斤"],
    "看": ["手", "目"],
    "见": ["见"],
    "读": ["讠", "卖"],
    "写": ["冖", "与"],
    "学": ["⺍", "冖", "子"],
    "生": ["生"],
    "做": ["亻", "故"],
    "去": ["土", "厶"],
    "来": ["木", "丷"],
    "回": ["囗", "口"],
    "会": ["人", "云"],
    "能": ["厶", "月", "匕", "匕"],
    "想": ["木", "目", "心"],
    "要": ["西", "女"],
    "买": ["乛", "头"],
    "卖": ["十", "买"],
    "坐": ["人", "人", "土"],
    "站": ["立", "占"],
    "走": ["走"],
    "跑": ["⻊", "包"],
    "飞": ["飞"],
    "开": ["廾", "一"],
    "关": ["丷", "天"],
    "住": ["亻", "主"],
    "在": ["土", "丨"],

    # ═══ HSK 1 — tính từ ═══
    "很": ["彳", "艮"],
    "太": ["大", "丶"],
    "高": ["高"],
    "矮": ["矢", "委"],
    "长": ["长"],
    "短": ["矢", "豆"],
    "胖": ["⺼", "半"],
    "瘦": ["疒", "叟"],
    "新": ["亲", "斤"],
    "旧": ["丨", "日"],
    "冷": ["冫", "令"],
    "热": ["土", "丸", "灬"],
    "好": ["女", "子"],
    "坏": ["土", "不"],
    "快": ["忄", "夬"],
    "慢": ["忄", "曼"],

    # ═══ HSK 1 — danh từ ═══
    "水": ["水"],
    "火": ["火"],
    "山": ["山"],
    "河": ["氵", "可"],
    "海": ["氵", "每"],
    "树": ["木", "尌"],
    "花": ["艹", "化"],
    "草": ["艹", "早"],
    "菜": ["艹", "采"],
    "饭": ["饣", "反"],
    "面": ["面"],
    "包": ["勹", "巳"],
    "茶": ["艹", "人", "木"],
    "酒": ["氵", "酉"],
    "奶": ["女", "乃"],
    "车": ["车"],
    "船": ["舟", "口"],
    "机": ["木", "几"],
    "电": ["电"],
    "脑": ["⺼", "巛", "凶"],
    "手": ["手"],
    "脚": ["⺼", "却"],
    "眼": ["目", "艮"],
    "头": ["头"],
    "口": ["口"],
    "耳": ["耳"],
    "鼻": ["鼻"],

    # ═══ HSK 2 ═══
    "晴": ["日", "青"],
    "阴": ["⻖", "月"],
    "雪": ["⻗", "彐"],
    "风": ["风"],
    "雨": ["雨"],
    "云": ["二", "厶"],
    "冰": ["冫", "水"],
    "问": ["门", "口"],
    "答": ["⺮", "合"],
    "知": ["矢", "口"],
    "道": ["辶", "首"],
    "认": ["讠", "人"],
    "识": ["讠", "只"],
    "记": ["讠", "己"],
    "忘": ["亡", "心"],
    "思": ["田", "心"],
    "念": ["人", "一", "心"],
    "怕": ["忄", "白"],
    "忙": ["忄", "亡"],
    "累": ["田", "糸"],
    "病": ["疒", "丙"],

    # ═══ HSK 3 ═══
    "喜": ["口", "士", "口", "丷", "一"],
    "欢": ["又", "欠"],
    "乐": ["乐"],
    "悲": ["非", "心"],
    "怒": ["女", "又", "心"],
    "惊": ["忄", "京"],
    "静": ["青", "争"],
    "安": ["宀", "女"],
    "全": ["人", "王"],
    "完": ["宀", "元"],
    "清": ["氵", "青"],
    "洗": ["氵", "先"],
    "漂": ["氵", "票"],
    "亮": ["亠", "口", "冖", "几"],
    "暗": ["日", "音"],

    # ═══ HSK 4+ ═══
    "环": ["王", "不"],
    "境": ["土", "竟"],
    "保": ["亻", "呆"],
    "护": ["扌", "户"],
    "污": ["氵", "亏"],
    "染": ["氵", "九", "木"],
    "发": ["癶", "又"],
    "展": ["尸", "共", "𧘇"],
    "进": ["辶", "井"],
    "步": ["止", "少"],
    "退": ["辶", "艮"],
    "改": ["己", "攵"],
    "变": ["亦", "又"],
    "化": ["亻", "匕"],
    "传": ["亻", "专"],
    "统": ["纟", "充"],
    "结": ["纟", "吉"],
    "果": ["日", "木"],
    "实": ["宀", "头"],
    "现": ["王", "见"],
    "代": ["亻", "弋"],
}


def _split_components(char):
    """
    Phân tích chữ thành các bộ thủ.
    Ưu tiên MANUAL_DECOMPOSITIONS → fallback tra trực tiếp.
    """
    # ═══ 1. Tra bảng thủ công ═══
    if char in MANUAL_DECOMPOSITIONS:
        parts = MANUAL_DECOMPOSITIONS[char]
        result = []
        for part in parts:
            info = get_radical_info(part)
            if info:
                result.append({
                    "zh": part,
                    "pinyin": info.get("pinyin", ""),
                    "strokes": info.get("strokes", ""),
                    "meaning": info.get("meaning", ""),
                    "position": _get_position(part),
                })
        if result:
            return result

    # ═══ 2. Fallback: tự thử tìm bộ thủ trong chữ ═══
    # (Không hoàn hảo nhưng là best-effort)
    for radical in sorted(RADICALS.keys(), key=lambda x: -len(x)):
        # Bỏ qua radical 1 ký tự trùng chính nó
        if radical == char:
            continue
        # Thử tìm radical trong mã Unicode của char
        # (Chỉ là heuristic, không chính xác tuyệt đối)
        # Skip — không thể làm chính xác bằng Python
        pass

    return []


# ═══════════════════════════════════════════════════════════════
#  API CHÍNH — PHÂN TÍCH TỪ
# ═══════════════════════════════════════════════════════════════
def find_components(hanzi):
    """Tìm tất cả bộ thủ trong 1 từ (có thể nhiều chữ)."""
    if not hanzi:
        return []

    components = []
    seen = set()

    # Với mỗi chữ Hán trong từ
    for ch in hanzi:
        if not ('\u4e00' <= ch <= '\u9fff'):
            continue

        # Tìm thành phần của chữ này
        comps = find_components_in_char(ch)
        for c in comps:
            key = c["zh"]
            if key in seen:
                continue
            seen.add(key)
            components.append(c)

    return components


def analyze_word(zh):
    """
    Phân tích toàn bộ từ.
    Returns:
    {
        "chars": [...],           # Danh sách chữ Hán
        "components": [...],      # Tất cả bộ thủ tìm được
        "main_radical": {...}     # Bộ thủ chính (để hiển thị)
    }
    """
    if not zh:
        return {"chars": [], "components": [], "main_radical": None}

    # Tách chữ
    chars = [c for c in zh if '\u4e00' <= c <= '\u9fff']

    # Tìm tất cả thành phần
    all_components = find_components(zh)

    # ═══ Chọn bộ thủ chính ═══
    main = None
    if chars:
        # Ưu tiên chữ đầu
        first_comps = find_components_in_char(chars[0])
        if first_comps:
            # Ưu tiên bộ thủ có vị trí "left" (thường là bộ chính)
            left_comps = [c for c in first_comps if c.get("position") == "left"]
            if left_comps:
                main = left_comps[0]
            else:
                # Chọn bộ thủ có số nét lớn nhất (thường quan trọng nhất)
                main = max(
                    first_comps,
                    key=lambda c: c.get("strokes") or 0
                )
        elif all_components:
            main = all_components[0]

    return {
        "chars": chars,
        "components": all_components,
        "main_radical": main,
    }


def get_radical_for_word(zh):
    """Helper — trả về bộ thủ chính của từ."""
    result = analyze_word(zh)
    return result.get("main_radical")

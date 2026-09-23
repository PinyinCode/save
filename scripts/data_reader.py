# -*- coding: utf-8 -*-
"""
Đọc file Excel → list dict.
⚡ KHI ĐỔI CẤU TRÚC EXCEL: chỉ cần sửa hàm read_excel() bên dưới.
Format chuẩn trả về: [{"stt","hsk","topic","subject","vi","zh","pinyin","excelRow"}, ...]

✅ MỚI: Thêm field "excelRow" = số dòng thực tế trong file Excel
   (dùng để tra cứu vị trí câu trong file gốc)

✅ LỌC HEADER RÁC: Bỏ qua các dòng có STT không phải số (VD: "HSK")

✅ GIỮ NGUYÊN STT GỐC: Không đánh lại STT — dùng đúng số từ cột A
"""
import openpyxl
import os
import sys


def clean(s):
    if s is None:
        return ""
    return (str(s).replace('\n', ' ').replace('\r', ' ')
            .replace('\t', ' ').replace('\\', '\\\\'))


def is_valid_stt(stt):
    """
    Kiểm tra STT có hợp lệ không.
    ✅ Hợp lệ: số nguyên (1, 2, 3...)
    ❌ Không hợp lệ: chữ ("HSK"), rỗng, None, ...
    """
    if stt is None:
        return False
    s = str(stt).strip()
    if not s:
        return False
    # Cho phép: "1", "1.0", "  1  " — không cho phép "HSK", "abc"
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


def read_excel(excel_file, sheet_index=0):
    print(f"\n📖 Đang đọc file: {excel_file}")
    if not os.path.exists(excel_file):
        print(f"❌ Không tìm thấy file {excel_file}")
        sys.exit(1)

    wb = openpyxl.load_workbook(excel_file, data_only=True)
    ws = wb.worksheets[sheet_index]
    print(f"📊 Sheet: {ws.title} - {ws.max_row} dòng")

    # ↓↓↓ CẤU HÌNH CỘT Ở ĐÂY (đổi khi Excel đổi cấu trúc) ↓↓↓
    COL_STT = 0
    COL_HSK = 1
    COL_TOPIC = 2
    COL_SUBJECT = 3
    COL_VI = 4
    COL_ZH = 5
    COL_PINYIN = 6
    DATA_START = 2
    # ↑↑↑ HẾT PHẦN CẦN SỬA ↑↑↑

    data = []
    skipped_no_stt = 0      # Đếm số dòng bỏ qua vì STT không hợp lệ
    skipped_no_content = 0  # Đếm số dòng bỏ qua vì không có nội dung

    # ★ Dùng enumerate để lấy row_idx (số dòng Excel thực tế)
    for offset, row in enumerate(ws.iter_rows(min_row=DATA_START, values_only=True)):
        row_idx = DATA_START + offset  # Số dòng Excel thực tế (2, 3, 4...)

        if not row or len(row) <= max(COL_VI, COL_ZH):
            continue

        stt_raw = row[COL_STT] if COL_STT < len(row) else None

        # ★ LỌC HEADER RÁC: Bỏ qua nếu STT không phải số
        if not is_valid_stt(stt_raw):
            skipped_no_stt += 1
            continue

        # Chuẩn hóa STT: bỏ .0 nếu có
        stt_str = str(stt_raw).strip()
        if stt_str.endswith('.0'):
            stt_str = stt_str[:-2]

        hsk = clean(row[COL_HSK]) if COL_HSK < len(row) else ""
        topic = clean(row[COL_TOPIC]) if COL_TOPIC < len(row) else ""
        subject = clean(row[COL_SUBJECT]) if COL_SUBJECT < len(row) else ""
        vi = clean(row[COL_VI]) if COL_VI < len(row) else ""
        zh = clean(row[COL_ZH]) if COL_ZH < len(row) else ""
        pinyin = clean(row[COL_PINYIN]) if COL_PINYIN < len(row) else ""

        # Bỏ qua nếu không có cả Việt + Trung
        if not vi and not zh:
            skipped_no_content += 1
            continue

        data.append({
            "stt": stt_str,           # ★ Giữ nguyên STT gốc
            "hsk": hsk,
            "topic": topic,
            "subject": subject,
            "vi": vi,
            "zh": zh,
            "pinyin": pinyin,
            "excelRow": row_idx,      # ★ Số dòng Excel
        })

    print(f"✅ Đã đọc {len(data)} câu")
    if skipped_no_stt > 0:
        print(f"⚠️  Đã bỏ qua {skipped_no_stt} dòng (STT không hợp lệ — header rác)")
    if skipped_no_content > 0:
        print(f"⚠️  Đã bỏ qua {skipped_no_content} dòng (không có nội dung Việt/Trung)")

    return data

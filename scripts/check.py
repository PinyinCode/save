# -*- coding: utf-8 -*-
"""Kiểm tra các file + placeholder trước khi build."""
import os
import json
import sys

ERRORS = []
WARNINGS = []

# 1. Kiểm tra file tồn tại (BẮT BUỘC)
REQUIRED_FILES = [
    "scripts/config.json",
    "scripts/config_loader.py",
    "scripts/data_reader.py",
    "scripts/convert.py",
    "scripts/ui_template.py",
    "scripts/social_template.py",
    "scripts/accounts_template.py",
    # "scripts/renewal_template.py",  # ← KHÔNG còn bắt buộc
]

# File tùy chọn (chỉ kiểm tra nếu tồn tại)
OPTIONAL_FILES = [
    "scripts/renewal_template.py",
]

print("📁 Kiểm tra files bắt buộc...")
for f in REQUIRED_FILES:
    if not os.path.exists(f):
        ERRORS.append(f"❌ Thiếu file: {f}")
    else:
        print(f"   ✅ {f}")

print("\n📁 Kiểm tra files tùy chọn...")
existing_optional = set()
for f in OPTIONAL_FILES:
    if os.path.exists(f):
        print(f"   ✅ {f} (có)")
        existing_optional.add(f)
    else:
        print(f"   ⚠️  {f} (không có — bỏ qua)")

# 2. Kiểm tra config
print("\n⚙️  Kiểm tra config.json...")
with open("scripts/config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)

required_cfg = ["firebase_config", "super_admin", "trial_days",
                "bank_config", "packages", "renewal_support_zalo"]
for k in required_cfg:
    if k not in cfg:
        ERRORS.append(f"❌ config.json thiếu key: {k}")
    else:
        print(f"   ✅ {k}")

# 3. Kiểm tra bank_config
if "bank_config" in cfg:
    bank = cfg["bank_config"]
    for k in ["bank_id", "bank_name", "account_no", "account_name"]:
        if not bank.get(k):
            ERRORS.append(f"❌ bank_config.{k} trống")
    print(f"   🏦 Bank: {bank.get('bank_name')} - {bank.get('account_no')}")

# 4. Kiểm tra placeholder trong ui_template
print("\n🔍 Kiểm tra placeholder trong ui_template.py...")
with open("scripts/ui_template.py", "r", encoding="utf-8") as f:
    ui_content = f.read()

if "<!-- __TIKTOK_BAR__ -->" not in ui_content:
    ERRORS.append("❌ ui_template.py THIẾU placeholder <!-- __TIKTOK_BAR__ -->")
else:
    print("   ✅ TikTok bar placeholder OK")

if 'id="dropdownRenewBtn"' not in ui_content:
    ERRORS.append("❌ ui_template.py THIẾU nút dropdownRenewBtn")
else:
    print("   ✅ Nút Gia hạn OK")

# 5. Kiểm tra renewal_template (CHỈ nếu file tồn tại)
if "scripts/renewal_template.py" in existing_optional:
    print("\n🔍 Kiểm tra renewal_template.py...")
    with open("scripts/renewal_template.py", "r", encoding="utf-8") as f:
        renewal_content = f.read()

    for fn in ["build_renewal_css", "build_renewal_html", "build_renewal_js"]:
        if f"def {fn}" not in renewal_content:
            ERRORS.append(f"❌ renewal_template.py thiếu hàm: {fn}")
        else:
            print(f"   ✅ {fn}()")
else:
    print("\n🔍 Bỏ qua renewal_template.py (không có file)")

# 6. Kiểm tra accounts_template
print("\n🔍 Kiểm tra accounts_template.py...")
with open("scripts/accounts_template.py", "r", encoding="utf-8") as f:
    acc_content = f.read()

checks = [
    ("grantTrialIfNew", "Trial tự động"),
    ("renewalsList",     "Section Yêu cầu gia hạn"),
    ("loadRenewals",     "Load renewals"),
    # ("initRenewalUI", "Init renewal"),  # ← ĐÃ BỎ
]
for fn, label in checks:
    if fn not in acc_content:
        ERRORS.append(f"❌ accounts_template.py thiếu: {fn} ({label})")
    else:
        print(f"   ✅ {fn} ({label})")

# 7. Kết luận
print("\n" + "="*60)
if ERRORS:
    print(f"❌ CÓ {len(ERRORS)} LỖI:")
    for e in ERRORS:
        print(f"   {e}")
    sys.exit(1)
else:
    print("🎉 Tất cả OK! Chạy: python scripts/convert.py")

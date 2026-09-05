"""
Patches draft_dir paths in generated build_categoryN_draft.py files
to use the correct catalog_drafts/categoryN directory instead of category6.
"""
import os, re

BASE = os.path.dirname(os.path.abspath(__file__))

for cat_num in range(8, 15):
    fpath = os.path.join(BASE, f"build_category{cat_num}_draft.py")
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    fixed = content.replace(
        '"catalog_drafts", "category6"',
        f'"catalog_drafts", "category{cat_num}"'
    )
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(fixed)
    print(f"[Cat {cat_num}] Patched draft_dir.")

print("All draft_dir paths patched.")

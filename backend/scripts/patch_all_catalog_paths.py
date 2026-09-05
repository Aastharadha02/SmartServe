"""
Patches paths in all generated categoryN scripts for catalog_drafts directory references.
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

SCRIPT_PREFIXES = ["generate_category", "persist_category", "create_category"]

for cat_num in range(8, 15):
    for prefix in SCRIPT_PREFIXES:
        # Find all matching files
        for fname in os.listdir(BASE):
            if fname.startswith(f"{prefix}{cat_num}_") and fname.endswith(".py"):
                fpath = os.path.join(BASE, fname)
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                fixed = content.replace(
                    '"catalog_drafts", "category6"',
                    f'"catalog_drafts", "category{cat_num}"'
                )
                
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(fixed)
                print(f"Patched: {fname}")

print("All catalog_drafts paths patched.")

"""
Generates build / report / persist / backup pipeline scripts for a category
by token-replacing from the Category 6 templates.

Usage:
    python generate_catN_scripts.py <cat_num> <cat_name_slug> <cat_label> <data_var> <data_module> <subcat_assertions>

This script is meant to be called programmatically (see generate_cats_8_to_14.py).
"""
import os
import re

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_scripts(
    cat_num: int,
    slug: str,         # e.g. "education_coaching"
    label: str,        # e.g. "8. Education, Teachers & Coaching"
    data_var: str,     # e.g. "EDUCATION_COACHING_SERVICES"
    data_module: str,  # e.g. "education_coaching_data"
    subcats: list,     # list of (subcat_name, count)
    base_dir: str,
):
    src6_b = read_file(os.path.join(base_dir, "build_category6_draft.py"))
    src6_r = read_file(os.path.join(base_dir, "generate_category6_draft_report.py"))
    src6_p = read_file(os.path.join(base_dir, "persist_category6_draft.py"))
    src6_c = read_file(os.path.join(base_dir, "create_category6_final_backups.py"))

    SUBS = {
        "category6_content_builder.smart_home_security_data": f"category{cat_num}_content_builder.{data_module}",
        "SMART_HOME_SERVICES": data_var,
        "category6_smart_home_security": f"category{cat_num}_{slug}",
        "build_category6_draft": f"build_category{cat_num}_draft",
        "generate_category6_draft_report": f"generate_category{cat_num}_draft_report",
        "persist_category6_draft": f"persist_category{cat_num}_draft",
        "create_category6_final_backups": f"create_category{cat_num}_final_backups",
        "'6. Smart Home & Security'": f"'{label}'",
        "Category 6: Smart Home & Security": f"Category {cat_num}: {label.split('. ', 1)[-1]}",
        "Category 6": f"Category {cat_num}",
        # index sheet title
        "SmartServe Catalog - Category 6: Smart Home & Security Index": f"SmartServe Catalog - Category {cat_num}: {label.split('. ', 1)[-1]} Index",
        # metadata dict key kept generic - handled by subcategory subcats below
        '"Security Systems"': f'"{subcats[0][0]}"',
        'subcategories_count\": 1': f'subcategories_count\": {len(subcats)}',
        # subcat list in xlsx index sheet
        'subcats = ["Security Systems"]': 'subcats = [' + ', '.join(f'"{s[0]}"' for s in subcats) + ']',
        # total listed in json metadata subcategories dict - replace the hard-coded Security Systems entry
        '"Security Systems": len(validated_draft_services)': ', '.join(f'"{s[0]}": {s[1]}' for s in subcats),
    }

    def apply(text):
        for k, v in SUBS.items():
            text = text.replace(k, v)
        return text

    b = apply(src6_b)
    r = apply(src6_r)
    p = apply(src6_p)
    c = apply(src6_c)

    # Fix assert block in report
    old_assert_block = re.search(
        r"    # Strict subcategory counts assertion for Category \d+\n(.*?)\n\n",
        r, re.DOTALL
    )
    new_assert_lines = [f"    # Strict subcategory counts assertion for Category {cat_num}"]
    for sname, scnt in subcats:
        new_assert_lines.append(
            f'    assert subcat_counts.get("{sname}", 0) == {scnt}, "Expected {scnt} {sname} services"'
        )
    new_assert_block = "\n".join(new_assert_lines)

    if old_assert_block:
        r = r[:old_assert_block.start()] + new_assert_block + "\n\n" + r[old_assert_block.end():]
    else:
        # Fallback: inject before "    md = []"
        r = r.replace("    md = []", new_assert_block + "\n\n    md = []", 1)

    # Fix report title line
    r = re.sub(
        r'md\.append\("# Category \d+: .*? - Draft Validation Report\\n"\)',
        f'md.append("# Category {cat_num}: {label.split(". ", 1)[-1]} - Draft Validation Report\\n")',
        r
    )

    write_file(os.path.join(base_dir, f"build_category{cat_num}_draft.py"), b)
    write_file(os.path.join(base_dir, f"generate_category{cat_num}_draft_report.py"), r)
    write_file(os.path.join(base_dir, f"persist_category{cat_num}_draft.py"), p)
    write_file(os.path.join(base_dir, f"create_category{cat_num}_final_backups.py"), c)
    print(f"[Cat {cat_num}] Generated 4 pipeline scripts.")

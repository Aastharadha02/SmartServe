import os

def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def write_file(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    
    # Read templates
    b6 = read_file(os.path.join(base, "build_category6_draft.py"))
    r6 = read_file(os.path.join(base, "generate_category6_draft_report.py"))
    p6 = read_file(os.path.join(base, "persist_category6_draft.py"))
    c6 = read_file(os.path.join(base, "create_category6_final_backups.py"))

    # Replacements for Category 1
    # Note: build_category6_draft has "category6_content_builder.smart_home_security_data import SMART_HOME_SERVICES"
    # and "category6_smart_home_security"
    # and "6. Smart Home & Security"
    
    cat1_replacements = {
        "category6_content_builder.smart_home_security_data": "category1_content_builder.beauty_salon_spa_data",
        "SMART_HOME_SERVICES": "BEAUTY_SERVICES",
        "category6_smart_home_security": "category1_beauty_salon_spa",
        "build_category6_draft": "build_category1_draft",
        "category6": "category1",
        "Category 6": "Category 1",
        "generate_category6_draft_report": "generate_category1_draft_report",
        "persist_category6_draft": "persist_category1_draft",
        "create_category6_final_backups": "create_category1_final_backups",
        "6. Smart Home & Security": "1. Beauty, Salon & Spa",
        "47": "55" # Service count
    }
    
    cat2_replacements = {
        "category6_content_builder.smart_home_security_data": "category2_content_builder.cleaning_home_data",
        "SMART_HOME_SERVICES": "CLEANING_SERVICES",
        "category6_smart_home_security": "category2_cleaning_home",
        "build_category6_draft": "build_category2_draft",
        "category6": "category2",
        "Category 6": "Category 2",
        "generate_category6_draft_report": "generate_category2_draft_report",
        "persist_category6_draft": "persist_category2_draft",
        "create_category6_final_backups": "create_category2_final_backups",
        "6. Smart Home & Security": "2. Cleaning & Pest Control",
        "47": "32" # Service count
    }
    
    def apply_replacements(text, repl_dict):
        for k, v in repl_dict.items():
            text = text.replace(k, v)
        return text

    # We also need to strip out DB snapshot assertions from the build_ scripts, 
    # since Categories 1 and 2 don't have DB parity yet (they are empty in the new DB).
    # We can just run a python code replace for that section.
    snapshot_block = """    # Load DB pre-change snapshot
    snapshot_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backups", "category6_smart_home_security_pre_change_snapshot.json"))
    with open(snapshot_path, "r", encoding="utf-8") as f:
        snapshot = json.load(f)
        
    db_services = {s["id"]: s for s in snapshot["services"]}
    print(f"Loaded {len(db_services)} database services from snapshot.")
    assert len(db_services) == 47, f"Expected 47 snapshot services, got {len(db_services)}"
"""
    
    loop_check_block = """        assert s_id in db_services, f"Builder service ID {s_id} ('{b_svc.get('name')}') not in DB snapshot!"
        db_s = db_services[s_id]
        
        # Verify exact identity parity
        assert b_svc["name"] == db_s["name"], f"Name mismatch on {s_id}: '{b_svc['name']}' vs '{db_s['name']}'"
        assert b_svc["category"] == db_s["category"], f"Category mismatch on {s_id}"
        assert b_svc["subcategory"] == db_s["subcategory"], f"Subcategory mismatch on {s_id}: '{b_svc['subcategory']}' vs '{db_s['subcategory']}'"
        assert b_svc["price"] == db_s["base_price"], f"Price mismatch on {s_id}: {b_svc['price']} vs {db_s['base_price']}"
        
        # Existing distinct features and real add-ons from DB
        distinct_features = list(db_s.get("distinct_features") or [])
        real_addons = db_s.get("real_addons") or []"""

    new_loop_block = """        # We skip DB parity checking because we are seeding a fresh local database.
        distinct_features = b_svc.get("included") or []
        real_addons = []"""

    b6_modified = b6.replace(snapshot_block, "").replace(loop_check_block, new_loop_block)

    # Make Category 1
    b1 = apply_replacements(b6_modified.replace("category6_smart_home_security_pre_change_snapshot", "category1_beauty_salon_spa_pre_change_snapshot"), cat1_replacements)
    r1 = apply_replacements(r6, cat1_replacements)
    p1 = apply_replacements(p6, cat1_replacements)
    c1 = apply_replacements(c6, cat1_replacements)
    
    # Make Category 2
    b2 = apply_replacements(b6_modified.replace("category6_smart_home_security_pre_change_snapshot", "category2_cleaning_home_pre_change_snapshot"), cat2_replacements)
    r2 = apply_replacements(r6, cat2_replacements)
    p2 = apply_replacements(p6, cat2_replacements)
    c2 = apply_replacements(c6, cat2_replacements)

    # Add custom subcategory assertions to the report generators
    cat1_asserts = """
    # Strict subcategory counts assertion for Category 1
    assert subcats.get("Facial & Skincare", 0) == 9, "Expected 9 Facial & Skincare services"
    assert subcats.get("Makeup & Styling", 0) == 6, "Expected 6 Makeup & Styling services"
    assert subcats.get("Men's Salon", 0) == 11, "Expected 11 Men's Salon services"
    assert subcats.get("Pedicure & Manicure", 0) == 10, "Expected 10 Pedicure & Manicure services"
    assert subcats.get("Spa & Massage", 0) == 6, "Expected 6 Spa & Massage services"
    assert subcats.get("Women's Salon", 0) == 13, "Expected 13 Women's Salon services"
"""
    cat2_asserts = """
    # Strict subcategory counts assertion for Category 2
    assert subcats.get("Deep Cleaning", 0) == 7, "Expected 7 Deep Cleaning services"
    assert subcats.get("Full Home / By Room Cleaning", 0) == 8, "Expected 8 Full Home / By Room Cleaning services"
    assert subcats.get("Kitchen & Bathroom Cleaning", 0) == 5, "Expected 5 Kitchen & Bathroom Cleaning services"
    assert subcats.get("Pest Control", 0) == 6, "Expected 6 Pest Control services"
    assert subcats.get("Sofa & Furniture Cleaning", 0) == 6, "Expected 6 Sofa & Furniture Cleaning services"
"""
    # Inject asserts before report string generation
    inject_point = 'report_str = f"""# DRAFT VALIDATION REPORT: {cat_name}'
    r1 = r1.replace(inject_point, cat1_asserts + "\n    " + inject_point)
    r2 = r2.replace(inject_point, cat2_asserts + "\n    " + inject_point)

    write_file(os.path.join(base, "build_category1_draft.py"), b1)
    write_file(os.path.join(base, "generate_category1_draft_report.py"), r1)
    write_file(os.path.join(base, "persist_category1_draft.py"), p1)
    write_file(os.path.join(base, "create_category1_final_backups.py"), c1)

    write_file(os.path.join(base, "build_category2_draft.py"), b2)
    write_file(os.path.join(base, "generate_category2_draft_report.py"), r2)
    write_file(os.path.join(base, "persist_category2_draft.py"), p2)
    write_file(os.path.join(base, "create_category2_final_backups.py"), c2)

    print("Successfully generated all pipeline scripts for Categories 1 and 2.")

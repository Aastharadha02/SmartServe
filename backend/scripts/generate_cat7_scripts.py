import os

def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def write_file(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    
    # Read templates from category 6
    b6 = read_file(os.path.join(base, "build_category6_draft.py"))
    r6 = read_file(os.path.join(base, "generate_category6_draft_report.py"))
    p6 = read_file(os.path.join(base, "persist_category6_draft.py"))
    c6 = read_file(os.path.join(base, "create_category6_final_backups.py"))

    cat7_replacements = {
        "category6_content_builder.smart_home_security_data": "category7_content_builder.domestic_help_cooking_data",
        "SMART_HOME_SERVICES": "DOMESTIC_HELP_SERVICES",
        "category6_smart_home_security": "category7_domestic_help_cooking",
        "build_category6_draft": "build_category7_draft",
        "category6": "category7",
        "Category 6": "Category 7",
        "generate_category6_draft_report": "generate_category7_draft_report",
        "persist_category6_draft": "persist_category7_draft",
        "create_category6_final_backups": "create_category7_final_backups",
        "6. Smart Home & Security": "7. Domestic Help & Cooking",
        "Security Systems": "Cooks / Chefs",
        "30": "30" # Service count
    }
    
    def apply_replacements(text, repl_dict):
        for k, v in repl_dict.items():
            text = text.replace(k, v)
        return text

    b7 = apply_replacements(b6, cat7_replacements)
    r7 = apply_replacements(r6, cat7_replacements)
    p7 = apply_replacements(p6, cat7_replacements)
    c7 = apply_replacements(c6, cat7_replacements)
    
    # In r7, we need to replace the old Category 6 asserts with Category 7 asserts
    old_asserts = """    # Strict subcategory counts assertion for Category 6
    assert subcat_counts.get("CCTV/Camera Installation", 0) == 7, "Expected 7 CCTV/Camera Installation services"
    assert subcat_counts.get("Video Doorbells", 0) == 5, "Expected 5 Video Doorbells services"
    assert subcat_counts.get("Smart Locks & Access Control", 0) == 6, "Expected 6 Smart Locks & Access Control services"
    assert subcat_counts.get("Alarm & Sensor Systems", 0) == 7, "Expected 7 Alarm & Sensor Systems services"
    assert subcat_counts.get("Smart Lighting/Switches", 0) == 5, "Expected 5 Smart Lighting/Switches services" """
    
    new_asserts = """    # Strict subcategory counts assertion for Category 7
    assert subcat_counts.get("Cooks / Chefs", 0) == 7, "Expected 7 Cooks / Chefs services"
    assert subcat_counts.get("Maids / Housekeepers", 0) == 7, "Expected 7 Maids / Housekeepers services"
    assert subcat_counts.get("Nannies / Babysitters", 0) == 6, "Expected 6 Nannies / Babysitters services"
    assert subcat_counts.get("Elder Care / Patient Care", 0) == 6, "Expected 6 Elder Care / Patient Care services"
    assert subcat_counts.get("Drivers", 0) == 4, "Expected 4 Drivers services" """
    
    r7 = r7.replace(old_asserts, new_asserts)

    write_file(os.path.join(base, "build_category7_draft.py"), b7)
    write_file(os.path.join(base, "generate_category7_draft_report.py"), r7)
    write_file(os.path.join(base, "persist_category7_draft.py"), p7)
    write_file(os.path.join(base, "create_category7_final_backups.py"), c7)

    print("Successfully generated all pipeline scripts for Category 7.")

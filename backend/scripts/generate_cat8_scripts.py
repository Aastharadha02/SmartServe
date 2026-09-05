import os

def read_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def write_file(filepath, content):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    
    # Read templates from category 7
    b7 = read_file(os.path.join(base, "build_category7_draft.py"))
    r7 = read_file(os.path.join(base, "generate_category7_draft_report.py"))
    p7 = read_file(os.path.join(base, "persist_category7_draft.py"))
    c7 = read_file(os.path.join(base, "create_category7_final_backups.py"))

    cat8_replacements = {
        "category7_content_builder.domestic_help_cooking_data": "category8_content_builder.education_coaching_data",
        "DOMESTIC_HELP_SERVICES": "EDUCATION_COACHING_SERVICES",
        "category7_domestic_help_cooking": "category8_education_coaching",
        "build_category7_draft": "build_category8_draft",
        "category7": "category8",
        "Category 7": "Category 8",
        "generate_category7_draft_report": "generate_category8_draft_report",
        "persist_category7_draft": "persist_category8_draft",
        "create_category7_final_backups": "create_category8_final_backups",
        "7. Domestic Help & Cooking": "8. Education, Teachers & Coaching",
        "Cooks / Chefs": "Academic Tutoring"
    }
    
    def apply_replacements(text, repl_dict):
        for k, v in repl_dict.items():
            text = text.replace(k, v)
        return text

    b8 = apply_replacements(b7, cat8_replacements)
    r8 = apply_replacements(r7, cat8_replacements)
    p8 = apply_replacements(p7, cat8_replacements)
    c8 = apply_replacements(c7, cat8_replacements)
    
    # In r8, we need to replace the old Category 7 asserts with Category 8 asserts
    old_asserts = """    # Strict subcategory counts assertion for Category 8
    assert subcat_counts.get("Academic Tutoring", 0) == 7, "Expected 7 Academic Tutoring services"
    assert subcat_counts.get("Maids / Housekeepers", 0) == 7, "Expected 7 Maids / Housekeepers services"
    assert subcat_counts.get("Nannies / Babysitters", 0) == 6, "Expected 6 Nannies / Babysitters services"
    assert subcat_counts.get("Elder Care / Patient Care", 0) == 6, "Expected 6 Elder Care / Patient Care services"
    assert subcat_counts.get("Drivers", 0) == 4, "Expected 4 Drivers services" """
    
    new_asserts = """    # Strict subcategory counts assertion for Category 8
    assert subcat_counts.get("Academic Tutoring", 0) == 7, "Expected 7 Academic Tutoring services"
    assert subcat_counts.get("Music & Arts", 0) == 6, "Expected 6 Music & Arts services"
    assert subcat_counts.get("Test Preparation", 0) == 6, "Expected 6 Test Preparation services"
    assert subcat_counts.get("Language Coaching", 0) == 6, "Expected 6 Language Coaching services"
    assert subcat_counts.get("Sports & Fitness Coaching", 0) == 5, "Expected 5 Sports & Fitness Coaching services" """
    
    r8 = r8.replace(old_asserts, new_asserts)

    write_file(os.path.join(base, "build_category8_draft.py"), b8)
    write_file(os.path.join(base, "generate_category8_draft_report.py"), r8)
    write_file(os.path.join(base, "persist_category8_draft.py"), p8)
    write_file(os.path.join(base, "create_category8_final_backups.py"), c8)

    print("Successfully generated all pipeline scripts for Category 8.")

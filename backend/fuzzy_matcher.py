import difflib

def suggest_student(scanned_name: str, scanned_roll: int, scanned_section: str, class_list: list) -> dict:
    best_match = None
    best_ratio = 0.0

    # Clean the scanned name (remove "B-", hyphens, spaces, lowercase)
    clean_scanned_name = scanned_name.replace("B-", "").replace("-", "").strip().lower()

    for student in class_list:
        # RULE 1: Never suggest from another section
        if student["section"] != scanned_section:
            continue
            
        # Clean the database name
        clean_db_name = student["name"].strip().lower()
        
        # Extract just the first name from the database
        db_first_name = clean_db_name.split()[0]

        # Calculate similarity ratio against the FULL name
        ratio_full = difflib.SequenceMatcher(None, clean_scanned_name, clean_db_name).ratio()
        
        # Calculate similarity ratio against just the FIRST name
        ratio_first = difflib.SequenceMatcher(None, clean_scanned_name, db_first_name).ratio()
        
        # Take the highest similarity score
        ratio = max(ratio_full, ratio_first)

        # RULE 2: Two-Factor Verification
        if student["roll_number"] == scanned_roll:
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = student

    if best_match and best_ratio >= 0.80:
        return {
            "status": "Linked",
            "student_id": best_match["id"],
            "confidence": round(best_ratio * 100, 2),
            "reason": f"Matched name ({scanned_name} -> {best_match['name']}) and Roll {scanned_roll}"
        }
    
    return {
        "status": "Unlinked",
        "student_id": None,
        "confidence": round(best_ratio * 100, 2),
        "reason": "Could not confidently match name and roll number."
    }
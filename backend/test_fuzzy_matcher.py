from fuzzy_matcher import suggest_student
import pytest

# --- OUR FAKE DATABASE ---
CLASS_LIST = [
    {"id": 1, "name": "Adithya Bandili", "roll_number": 3, "section": "A"},
    {"id": 2, "name": "Aditya Singh", "roll_number": 4, "section": "A"},
    {"id": 3, "name": "Aliya Singh", "roll_number": 5, "section": "B"},
    {"id": 4, "name": "Rahul Sharma", "roll_number": 6, "section": "A"},
    {"id": 5, "name": "Saima Khan", "roll_number": 7, "section": "B"},
]

# --- THE 30 TEST CASES ---
TEST_CASES = [
    # 1. Exact match
    ("Adithya Bandili", 3, "A", "Linked", 1),
    # 2. "B-Aditya" for Adithya Bandili (Roll 3)
    ("B-Aditya", 3, "A", "Linked", 1),
    # 3. "Atliya Singh" for Aliya Singh (Roll 5, Section B)
    ("Atliya Singh", 5, "B", "Linked", 3),
    # 4. TRAP! Two Adityas in Section A. The roll number saves us.
    ("Aditya", 4, "A", "Linked", 2),
    # 5. TRAP! Name matches, but WRONG section. Must be Unlinked.
    ("Adithya Bandili", 3, "B", "Unlinked", None),
    # 6. Typo in name, but correct roll.
    ("Rahul Sharm", 6, "A", "Linked", 4),
    # 7. Name matches, but WRONG roll number. Must be Unlinked.
    ("Saima Khan", 8, "B", "Unlinked", None),
    # 8. Garbage name, correct roll. (Similarity < 0.8). Must be Unlinked.
    ("Xyz Abc", 7, "B", "Unlinked", None),
    # 9. Completely different person.
    ("John Doe", 99, "A", "Unlinked", None),
    # 10. Missing roll number (passed as 0). Must be Unlinked.
    ("Saima", 0, "B", "Unlinked", None),
    # 11. Lowercase name
    ("adithya bandili", 3, "A", "Linked", 1),
    # 12. Uppercase name
    ("ADITHYA BANDILI", 3, "A", "Linked", 1),
    # 13. Extra spaces
    ("  Adithya   Bandili  ", 3, "A", "Linked", 1),
    # 14. Hyphenated name
    ("B-Adithya-Bandili", 3, "A", "Linked", 1),
    # 15. Slight typo, correct roll
    ("Adithya Bandil", 3, "A", "Linked", 1),
    # 16. Slight typo, WRONG roll (Roll 4 belongs to Aditya Singh)
    ("Adithya Bandil", 4, "A", "Unlinked", None),
    # 17. Saima Typo
    ("Saima Kha", 7, "B", "Linked", 5),
    # 18. Rahul Typo
    ("Rahu Sharma", 6, "A", "Linked", 4),
    # 19. Aditya Typo
    ("Adity Sing", 4, "A", "Linked", 2),
    # 20. Wrong Section, similar name
    ("Aliya Singh", 5, "A", "Unlinked", None),
    # 21. Wrong Section, same roll
    ("Rahul Sharma", 6, "B", "Unlinked", None),
    # 22. Name matches but completely wrong roll
    ("Adithya Bandili", 99, "A", "Unlinked", None),
    # 23. Exact Match Saima
    ("Saima Khan", 7, "B", "Linked", 5),
    # 24. Exact Match Aliya
    ("Aliya Singh", 5, "B", "Linked", 3),
    # 25. Exact Match Rahul
    ("Rahul Sharma", 6, "A", "Linked", 4),
    # 26. First name only, roll doesn't exist
    ("Aditya", 2, "A", "Unlinked", None),
    # 27. First name only, correct roll
    ("Aditya", 4, "A", "Linked", 2),
    # 28. Last name only, correct roll (Similarity too low)
    ("Bandili", 3, "A", "Unlinked", None),
    # 29. Last name only, wrong roll
    ("Bandili", 4, "A", "Unlinked", None),
    # 30. Garbage with correct roll
    ("AAAAA", 5, "B", "Unlinked", None),
]

@pytest.mark.parametrize("scanned_name, scanned_roll, scanned_section, expected_status, expected_id", TEST_CASES)
def test_suggest_student(scanned_name, scanned_roll, scanned_section, expected_status, expected_id):
    result = suggest_student(scanned_name, scanned_roll, scanned_section, CLASS_LIST)
    
    assert result["status"] == expected_status
    assert result["student_id"] == expected_id

# --- THE REPORT GENERATOR ---
def generate_report():
    correct = 0
    wrong = 0
    unlinked = 0
    
    for case in TEST_CASES:
        scanned_name, scanned_roll, scanned_section, expected_status, expected_id = case
        result = suggest_student(scanned_name, scanned_roll, scanned_section, CLASS_LIST)
        
        if result["status"] == "Unlinked":
            unlinked += 1
        elif result["status"] == "Linked" and result["student_id"] == expected_id:
            correct += 1
        else:
            wrong += 1
            
    print(f"\n--- ACCURACY REPORT ---")
    print(f"Total Cases: {len(TEST_CASES)}")
    print(f"Correctly Linked: {correct}")
    print(f"Wrongly Linked (CATASTROPHIC): {wrong}")
    print(f"Left Unlinked (Safe): {unlinked}")

if __name__ == "__main__":
    generate_report()
from decimal import Decimal, ROUND_HALF_UP

def calculate_total(paper_max_marks: float, questions: list, grace_marks: float = 0.0) -> Decimal:
    """
    Calculates the final total for a student's paper.
    
    `questions` is a list of dictionaries like:
    [
        {"question_id": 1, "marks_obtained": 8, "max_marks": 10, "choice_group": "Group A"},
        {"question_id": 2, "marks_obtained": 9, "max_marks": 10, "choice_group": "Group A"},
        {"question_id": 3, "marks_obtained": 15, "max_marks": 20, "choice_group": "Group B"},
        {"question_id": 4, "marks_obtained": 12, "max_marks": 20, "choice_group": "Group B"},
    ]
    """
    
    # 1. Convert paper max marks to Decimal
    paper_max = Decimal(str(paper_max_marks))
    
    # 2. Validate marks (cannot be below 0 or above max)
    for q in questions:
        if q["marks_obtained"] < 0:
            raise ValueError(f"Mark for question {q['question_id']} cannot be negative.")
        if q["marks_obtained"] > q["max_marks"]:
            raise ValueError(f"Mark for question {q['question_id']} exceeds the maximum of {q['max_marks']}.")
            
    # 3. Handle Choice Groups ("Answer 2 of 4")
    groups = {}
    compulsory_questions = []
    
    for q in questions:
        if q.get("choice_group"):
            group_name = q["choice_group"]
            if group_name not in groups:
                groups[group_name] = []
            groups[group_name].append(q)
        else:
            compulsory_questions.append(q)
            
    # Calculate total for compulsory questions
    total = sum(Decimal(str(q["marks_obtained"])) for q in compulsory_questions)
    
    # For each choice group, sort by raw marks descending and pick the top 2
    for group_name, group_questions in groups.items():
        group_questions.sort(key=lambda x: x["marks_obtained"], reverse=True)
        best_2 = group_questions[:2]
        total += sum(Decimal(str(q["marks_obtained"])) for q in best_2)
        
    # 4. Add Grace Marks
    total += Decimal(str(grace_marks))
    
    # 5. Round to nearest 0.5, never down (The Fix)
    # Multiply by 2, round to nearest whole number, then divide by 2
    total = total * Decimal("2")
    total = total.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    total = total / Decimal("2")
    
    # 6. Cap at paper max marks and 0
    if total > paper_max:
        total = paper_max
    if total < 0:
        total = Decimal("0.0")
        
    return total
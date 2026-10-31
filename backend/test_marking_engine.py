import pytest
from decimal import Decimal
from marking_engine import calculate_total
from hypothesis import given, strategies as st

# --- 30 PARAMETRIZED TEST CASES ---
@pytest.mark.parametrize("paper_max, questions, grace, expected", [
    (100, [{"question_id": 1, "marks_obtained": 10, "max_marks": 10, "choice_group": None}], 0, Decimal("10.0")),
    (100, [{"question_id": 1, "marks_obtained": 0, "max_marks": 10, "choice_group": None}], 0, Decimal("0.0")),
    (100, [{"question_id": 1, "marks_obtained": 15, "max_marks": 20, "choice_group": None}, {"question_id": 2, "marks_obtained": 25, "max_marks": 30, "choice_group": None}], 0, Decimal("40.0")),
    (100, [{"question_id": 1, "marks_obtained": 100, "max_marks": 100, "choice_group": None}], 0, Decimal("100.0")),
    (100, [{"question_id": 1, "marks_obtained": 2.2, "max_marks": 10, "choice_group": None}], 0, Decimal("2.0")),
    (100, [{"question_id": 1, "marks_obtained": 2.3, "max_marks": 10, "choice_group": None}], 0, Decimal("2.5")),
    (100, [{"question_id": 1, "marks_obtained": 2.7, "max_marks": 10, "choice_group": None}], 0, Decimal("2.5")),
    (100, [{"question_id": 1, "marks_obtained": 2.8, "max_marks": 10, "choice_group": None}], 0, Decimal("3.0")),
    (100, [{"question_id": 1, "marks_obtained": 2.25, "max_marks": 10, "choice_group": None}], 0, Decimal("2.5")),
    (100, [{"question_id": 1, "marks_obtained": 10.75, "max_marks": 20, "choice_group": None}], 0, Decimal("11.0")),
    (100, [{"question_id": 1, "marks_obtained": 50, "max_marks": 100, "choice_group": None}], 5, Decimal("55.0")),
    (100, [{"question_id": 1, "marks_obtained": 95, "max_marks": 100, "choice_group": None}], 10, Decimal("100.0")),
    (100, [{"question_id": 1, "marks_obtained": 5, "max_marks": 10, "choice_group": None}], -10, Decimal("0.0")),
    (100, [{"question_id": 1, "marks_obtained": 10, "max_marks": 10, "choice_group": None}], 2.25, Decimal("12.5")),
    (100, [{"question_id": 1, "marks_obtained": 9, "max_marks": 10, "choice_group": "Group A"}, {"question_id": 2, "marks_obtained": 8, "max_marks": 10, "choice_group": "Group A"}, {"question_id": 3, "marks_obtained": 5, "max_marks": 10, "choice_group": "Group A"}, {"question_id": 4, "marks_obtained": 2, "max_marks": 10, "choice_group": "Group A"}], 0, Decimal("17.0")),
    (100, [{"question_id": 1, "marks_obtained": 8, "max_marks": 10, "choice_group": "Group A"}, {"question_id": 2, "marks_obtained": 10, "max_marks": 20, "choice_group": "Group A"}, {"question_id": 3, "marks_obtained": 9, "max_marks": 20, "choice_group": "Group A"}], 0, Decimal("19.0")),
    (100, [{"question_id": 1, "marks_obtained": 10, "max_marks": 20, "choice_group": "Group A"}, {"question_id": 2, "marks_obtained": 10, "max_marks": 20, "choice_group": "Group A"}, {"question_id": 3, "marks_obtained": 10, "max_marks": 20, "choice_group": "Group A"}], 0, Decimal("20.0")),
    (100, [{"question_id": 1, "marks_obtained": 15, "max_marks": 20, "choice_group": "Group A"}], 0, Decimal("15.0")),
    (100, [{"question_id": 1, "marks_obtained": 12, "max_marks": 20, "choice_group": "Group A"}, {"question_id": 2, "marks_obtained": 18, "max_marks": 20, "choice_group": "Group A"}], 0, Decimal("30.0")),
    (100, [{"question_id": 1, "marks_obtained": 10, "max_marks": 10, "choice_group": "Group A"}, {"question_id": 2, "marks_obtained": 9, "max_marks": 10, "choice_group": "Group A"}, {"question_id": 3, "marks_obtained": 8, "max_marks": 10, "choice_group": "Group A"}, {"question_id": 4, "marks_obtained": 20, "max_marks": 20, "choice_group": "Group B"}, {"question_id": 5, "marks_obtained": 19, "max_marks": 20, "choice_group": "Group B"}, {"question_id": 6, "marks_obtained": 18, "max_marks": 20, "choice_group": "Group B"}], 0, Decimal("58.0")),
    (100, [{"question_id": 1, "marks_obtained": 10, "max_marks": 10, "choice_group": None}, {"question_id": 2, "marks_obtained": 9, "max_marks": 10, "choice_group": "Group A"}, {"question_id": 3, "marks_obtained": 8, "max_marks": 10, "choice_group": "Group A"}, {"question_id": 4, "marks_obtained": 7, "max_marks": 10, "choice_group": "Group A"}], 0, Decimal("27.0")),
    (100, [{"question_id": 1, "marks_obtained": 0, "max_marks": 0, "choice_group": None}], 0, Decimal("0.0")),
    (100, [], 0, Decimal("0.0")),
    (100, [], 5, Decimal("5.0")),
    (1000, [{"question_id": 1, "marks_obtained": 500, "max_marks": 500, "choice_group": None}], 0, Decimal("500.0")),
    (100, [{"question_id": 1, "marks_obtained": 5, "max_marks": 10, "choice_group": "Group A"}], -10, Decimal("0.0")),
    (100, [{"question_id": 1, "marks_obtained": 10.25, "max_marks": 20, "choice_group": "Group A"}], 0, Decimal("10.5")),
    (100, [{"question_id": 1, "marks_obtained": 10, "max_marks": 20, "choice_group": "Group A"}, {"question_id": 2, "marks_obtained": 10, "max_marks": 20, "choice_group": "Group B"}], 5.25, Decimal("25.5")),
    (100, [{"question_id": 1, "marks_obtained": 0, "max_marks": 10, "choice_group": None}], 2, Decimal("2.0")),
    (100, [{"question_id": 1, "marks_obtained": 2.1, "max_marks": 10, "choice_group": None}], 0, Decimal("2.0")),
])
def test_calculate_total(paper_max, questions, grace, expected):
    result = calculate_total(paper_max, questions, grace)
    assert result == expected

# --- 2 ERROR TEST CASES ---
def test_negative_mark_raises_error():
    with pytest.raises(ValueError, match="cannot be negative"):
        calculate_total(100, [{"question_id": 1, "marks_obtained": -1, "max_marks": 10, "choice_group": None}])

def test_mark_exceeds_max_raises_error():
    with pytest.raises(ValueError, match="exceeds the maximum"):
        calculate_total(100, [{"question_id": 1, "marks_obtained": 11, "max_marks": 10, "choice_group": None}])

# --- 1 PROPERTY TEST (HYPOTHESIS) ---
@given(
    paper_max=st.integers(min_value=10, max_value=1000),
    marks_obtained=st.floats(min_value=0, max_value=1000),
    max_marks=st.floats(min_value=0, max_value=1000),
    grace=st.floats(min_value=-10, max_value=10)
)
def test_property_total_is_between_0_and_max(paper_max, marks_obtained, max_marks, grace):
    if marks_obtained > max_marks:
        marks_obtained = max_marks
    questions = [{"question_id": 1, "marks_obtained": marks_obtained, "max_marks": max_marks, "choice_group": None}]
    result = calculate_total(paper_max, questions, grace)
    assert result >= Decimal("0.0")
    assert result <= Decimal(str(paper_max))
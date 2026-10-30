import random

print('-- Insert 3 sections of students (10 each)')
for section in ['A', 'B', 'C']:
    for i in range(1, 11):
        name = f'Student_{section}_{i}'
        roll = i
        adm = f'ADM_{section}_{i}'
        print(f"INSERT INTO students (name, roll_number, class, section, admission_number) VALUES ('{name}', {roll}, '10', '{section}', '{adm}');")

print('-- Insert 2 Papers')
print("INSERT INTO papers (name, total_max_marks) VALUES ('Math Midterm', 100);")
print("INSERT INTO papers (name, total_max_marks) VALUES ('Science Final', 100);")

print('-- Insert Questions for Math Paper (Paper 1)')
for i in range(1, 6):
    print(f"INSERT INTO questions (paper_id, question_number, max_marks, choice_group) VALUES (1, {i}, 20, NULL);")

print('-- Insert Questions for Science Paper (Paper 2)')
print("INSERT INTO questions (paper_id, question_number, max_marks, choice_group) VALUES (2, 1, 25, 'Group A');")
print("INSERT INTO questions (paper_id, question_number, max_marks, choice_group) VALUES (2, 2, 25, 'Group A');")
print("INSERT INTO questions (paper_id, question_number, max_marks, choice_group) VALUES (2, 3, 25, 'Group B');")
print("INSERT INTO questions (paper_id, question_number, max_marks, choice_group) VALUES (2, 4, 25, 'Group B');")

print('-- Create Answer Scripts and Assign Random Marks to Students')
for student_id in range(1, 31):
    print(f"INSERT INTO answer_scripts (id, paper_id, student_id) VALUES ({student_id}, 1, {student_id});")
    for q_id in range(1, 6):
        mark = random.randint(5, 20)
        print(f"INSERT INTO question_marks (script_id, question_id, marks_obtained) VALUES ({student_id}, {q_id}, {mark});")
-- Query 1: Get all students in Class 10, Section A
SELECT * FROM students WHERE class = '10' AND section = 'A';

-- Query 2: Class Average per Question (For Paper 1)
SELECT q.question_number, ROUND(AVG(qm.marks_obtained), 2) as class_average
FROM questions q
JOIN question_marks qm ON q.id = qm.question_id
WHERE q.paper_id = 1
GROUP BY q.question_number
ORDER BY q.question_number;

-- Query 3: Rank within Section (Window Function)
SELECT s.name, s.section, SUM(qm.marks_obtained) as total_marks,
       RANK() OVER (PARTITION BY s.section ORDER BY SUM(qm.marks_obtained) DESC) as rank_in_section
FROM students s
JOIN answer_scripts ans ON s.id = ans.student_id
JOIN question_marks qm ON ans.id = qm.script_id
WHERE ans.paper_id = 1
GROUP BY s.id, s.name, s.section;

-- Query 4: Students missing a paper (e.g., Paper 2)
SELECT s.name 
FROM students s
LEFT JOIN answer_scripts ans ON s.id = ans.student_id AND ans.paper_id = 2
WHERE ans.id IS NULL;

-- Query 5: Top 3 students overall
SELECT s.name, SUM(qm.marks_obtained) as total_marks
FROM students s
JOIN answer_scripts ans ON s.id = ans.student_id
JOIN question_marks qm ON ans.id = qm.script_id
GROUP BY s.id, s.name
ORDER BY total_marks DESC
LIMIT 3;

-- Query 6: Count of students per section
SELECT section, COUNT(*) as student_count
FROM students
GROUP BY section;

-- Query 7: Find all questions that are part of a choice group
SELECT * FROM questions WHERE choice_group IS NOT NULL;

-- Query 8: Get total marks a specific student got in Math (Student ID 1)
SELECT s.name, SUM(qm.marks_obtained) as math_total
FROM students s
JOIN answer_scripts ans ON s.id = ans.student_id
JOIN question_marks qm ON ans.id = qm.script_id
WHERE s.id = 1 AND ans.paper_id = 1
GROUP BY s.name;

-- Query 9: Average marks per paper
SELECT p.name, ROUND(AVG(qm.marks_obtained), 2) as average_mark_per_question
FROM papers p
JOIN questions q ON p.id = q.paper_id
JOIN question_marks qm ON q.id = qm.question_id
GROUP BY p.name;

-- Query 10: The Highest scoring question across all papers
SELECT q.id, q.question_number, p.name as paper_name, MAX(qm.marks_obtained) as highest_mark
FROM questions q
JOIN question_marks qm ON q.id = qm.question_id
JOIN papers p ON q.paper_id = p.id
GROUP BY q.id, q.question_number, p.name
ORDER BY highest_mark DESC
LIMIT 1;
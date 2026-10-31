from database import SessionLocal
from models import Student, Paper, Question, AnswerScript, QuestionMark
import random

def seed_database():
    db = SessionLocal()
    
    print("Deleting old data...")
    # We delete to prevent duplicates if we run it twice
    db.query(QuestionMark).delete()
    db.query(AnswerScript).delete()
    db.query(Question).delete()
    db.query(Paper).delete()
    db.query(Student).delete()
    db.commit()

    print("Inserting 30 students...")
    students = []
    for section in ['A', 'B', 'C']:
        for i in range(1, 11):
            student = Student(
                name=f'Student_{section}_{i}',
                roll_number=i,
                class_name='10',
                section=section,
                admission_number=f'ADM_{section}_{i}'
            )
            students.append(student)
    db.add_all(students)
    db.commit()

    print("Inserting Papers and Questions...")
    math_paper = Paper(name='Math Midterm', total_max_marks=100)
    science_paper = Paper(name='Science Final', total_max_marks=100)
    db.add_all([math_paper, science_paper])
    db.commit()

    # Questions for Math (Paper 1)
    for i in range(1, 6):
        q = Question(paper_id=math_paper.id, question_number=i, max_marks=20, choice_group=None)
        db.add(q)

    # Questions for Science (Paper 2)
    db.add(Question(paper_id=science_paper.id, question_number=1, max_marks=25, choice_group='Group A'))
    db.add(Question(paper_id=science_paper.id, question_number=2, max_marks=25, choice_group='Group A'))
    db.add(Question(paper_id=science_paper.id, question_number=3, max_marks=25, choice_group='Group B'))
    db.add(Question(paper_id=science_paper.id, question_number=4, max_marks=25, choice_group='Group B'))
    db.commit()

    print("Creating Scripts and Assigning Marks...")
    # For each student, create a script for Math and add random marks
    for student in students:
        script = AnswerScript(paper_id=math_paper.id, student_id=student.id)
        db.add(script)
        db.commit() # Commit to get the script ID

        # Add random marks for the 5 questions
        for q_id in range(1, 6):
            mark = random.randint(5, 20)
            qm = QuestionMark(script_id=script.id, question_id=q_id, marks_obtained=mark)
            db.add(qm)
    
    db.commit()
    db.close()
    print("✅ Database seeded successfully!")

if __name__ == "__main__":
    seed_database()
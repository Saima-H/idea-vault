from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    roll_number = Column(Integer, nullable=False)
    class_name = Column("class", String(50), nullable=False) # 'class' is reserved in Python
    section = Column(String(10), nullable=False)
    admission_number = Column(String(50), unique=True, nullable=False)
    
    __table_args__ = (
        UniqueConstraint('class', 'section', 'roll_number', name='unique_roll_per_section'),
    )
    scripts = relationship("AnswerScript", back_populates="student")

class Paper(Base):
    __tablename__ = "papers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    total_max_marks = Column(Integer, nullable=False)
    questions = relationship("Question", back_populates="paper")
    scripts = relationship("AnswerScript", back_populates="paper")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), nullable=False)
    question_number = Column(Integer, nullable=False)
    max_marks = Column(Numeric(5, 2), nullable=False)
    choice_group = Column(String(50), nullable=True)
    paper = relationship("Paper", back_populates="questions")
    marks = relationship("QuestionMark", back_populates="question")

class AnswerScript(Base):
    __tablename__ = "answer_scripts"
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="Pending")
    paper = relationship("Paper", back_populates="scripts")
    student = relationship("Student", back_populates="scripts")
    marks = relationship("QuestionMark", back_populates="script")

class QuestionMark(Base):
    __tablename__ = "question_marks"
    id = Column(Integer, primary_key=True, index=True)
    script_id = Column(Integer, ForeignKey("answer_scripts.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    marks_obtained = Column(Numeric(5, 2), nullable=False)
    is_best_choice = Column(Boolean, default=False)
    script = relationship("AnswerScript", back_populates="marks")
    question = relationship("Question", back_populates="marks")
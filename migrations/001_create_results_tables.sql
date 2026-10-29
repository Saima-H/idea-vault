-- ==========================================
-- RESULTS VAULT SCHEMA
-- ==========================================

-- 1. Students Table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    roll_number INT NOT NULL,
    class VARCHAR(50) NOT NULL,
    section VARCHAR(10) NOT NULL,
    admission_number VARCHAR(50) UNIQUE NOT NULL,
    -- THE CRITICAL CONSTRAINT: Roll number is unique ONLY within a class and section
    CONSTRAINT unique_roll_per_section UNIQUE (class, section, roll_number)
);

-- 2. Papers Table
CREATE TABLE IF NOT EXISTS papers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    total_max_marks INT NOT NULL
);

-- 3. Questions Table
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    paper_id INT REFERENCES papers(id) ON DELETE CASCADE,
    question_number INT NOT NULL,
    max_marks NUMERIC(5, 2) NOT NULL,
    choice_group VARCHAR(50) -- e.g., 'Group A' for "Answer any 2 of 4"
);

-- 4. Answer Scripts Table
CREATE TABLE IF NOT EXISTS answer_scripts (
    id SERIAL PRIMARY KEY,
    paper_id INT REFERENCES papers(id) ON DELETE CASCADE,
    student_id INT REFERENCES students(id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'Pending' -- Pending, Graded, Published
);

-- 5. Question Marks Table
CREATE TABLE IF NOT EXISTS question_marks (
    id SERIAL PRIMARY KEY,
    script_id INT REFERENCES answer_scripts(id) ON DELETE CASCADE,
    question_id INT REFERENCES questions(id) ON DELETE CASCADE,
    marks_obtained NUMERIC(5, 2) NOT NULL,
    is_best_choice BOOLEAN DEFAULT FALSE
);
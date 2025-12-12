import sqlite3
from werkzeug.security import generate_password_hash
import os

DATABASE_PATH = 'quiz.db'

def get_db_connection():
    """Create a database connection and return it"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with tables if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    )
    ''')
    
    # Create questions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_ans TEXT NOT NULL
    )
    ''')
    
    # Create results table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        score INTEGER NOT NULL,
        total INTEGER NOT NULL,
        quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Check if admin exists, if not create default admin
    cursor.execute("SELECT * FROM users WHERE is_admin = 1")
    admin = cursor.fetchone()
    
    if not admin:
        # Create default admin user
        hashed_password = generate_password_hash('admin123')
        cursor.execute(
            "INSERT INTO users (name, email, password, is_admin) VALUES (?, ?, ?, ?)",
            ('Admin', 'admin@example.com', hashed_password, 1)
        )
        print("Default admin created: email=admin@example.com, password=admin123")
    
    # Add some sample questions if none exist
    cursor.execute("SELECT COUNT(*) FROM questions")
    question_count = cursor.fetchone()[0]
    
    if question_count == 0:
        sample_questions = [
            (
                "What is the capital of France?",
                "London", "Paris", "Berlin", "Madrid",
                "Paris"
            ),
            (
                "Which planet is known as the Red Planet?",
                "Venus", "Jupiter", "Mars", "Saturn",
                "Mars"
            ),
            (
                "What is the chemical symbol for gold?",
                "Ag", "Au", "Fe", "Cu",
                "Au"
            ),
            (
                "Which language is used for web development?",
                "Python", "JavaScript", "C++", "All of the above",
                "All of the above"
            ),
        ]
        
        cursor.executemany(
            "INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_ans) VALUES (?, ?, ?, ?, ?, ?)",
            sample_questions
        )
        print(f"Added {len(sample_questions)} sample questions")
    
    conn.commit()
    conn.close()
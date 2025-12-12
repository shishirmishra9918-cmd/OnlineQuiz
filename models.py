import sqlite3
from database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

class User:
    """User model to handle user-related operations"""
    
    @staticmethod
    def create(name, email, password):
        """Create a new user"""
        conn = get_db_connection()
        hashed_password = generate_password_hash(password)
        
        try:
            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            # Email already exists
            success = False
        finally:
            conn.close()
            
        return success
    
    @staticmethod
    def authenticate(email, password):
        """Authenticate a user"""
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            return user
        return None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        conn.close()
        return user

class Question:
    """Question model to handle question-related operations"""
    
    @staticmethod
    def get_all():
        """Get all questions"""
        conn = get_db_connection()
        questions = conn.execute("SELECT * FROM questions").fetchall()
        conn.close()
        return questions
    
    @staticmethod
    def get_by_id(question_id):
        """Get question by ID"""
        conn = get_db_connection()
        question = conn.execute(
            "SELECT * FROM questions WHERE id = ?", (question_id,)
        ).fetchone()
        conn.close()
        return question
    
    @staticmethod
    def create(question_text, option_a, option_b, option_c, option_d, correct_ans):
        """Create a new question"""
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_ans) VALUES (?, ?, ?, ?, ?, ?)",
            (question_text, option_a, option_b, option_c, option_d, correct_ans)
        )
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def update(question_id, question_text, option_a, option_b, option_c, option_d, correct_ans):
        """Update an existing question"""
        conn = get_db_connection()
        conn.execute(
            "UPDATE questions SET question = ?, option_a = ?, option_b = ?, option_c = ?, option_d = ?, correct_ans = ? WHERE id = ?",
            (question_text, option_a, option_b, option_c, option_d, correct_ans, question_id)
        )
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def delete(question_id):
        """Delete a question"""
        conn = get_db_connection()
        conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        conn.commit()
        conn.close()
        return True

class Result:
    """Result model to handle quiz result operations"""
    
    @staticmethod
    def save(user_id, score, total):
        """Save quiz result"""
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO results (user_id, score, total) VALUES (?, ?, ?)",
            (user_id, score, total)
        )
        conn.commit()
        conn.close()
        return True
    
    @staticmethod
    def get_by_user(user_id):
        """Get results for a specific user"""
        conn = get_db_connection()
        results = conn.execute(
            "SELECT * FROM results WHERE user_id = ? ORDER BY quiz_date DESC",
            (user_id,)
        ).fetchall()
        conn.close()
        return results
    
    @staticmethod
    def get_all():
        """Get all results with user information"""
        conn = get_db_connection()
        results = conn.execute(
            """
            SELECT r.*, u.name, u.email 
            FROM results r
            JOIN users u ON r.user_id = u.id
            ORDER BY r.quiz_date DESC
            """
        ).fetchall()
        conn.close()
        return results
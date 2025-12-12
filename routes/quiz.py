from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Question, Result, User
from functools import wraps

quiz_bp = Blueprint('quiz', __name__)

# User login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin not allowed decorator (for user-only routes)
def admin_not_allowed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('is_admin'):
            flash('Admin cannot access user features', 'warning')
            return redirect(url_for('admin.dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@quiz_bp.route('/dashboard')
@login_required
@admin_not_allowed
def dashboard():
    # Get user's past results
    user_id = session.get('user_id')
    results = Result.get_by_user(user_id)
    
    return render_template('dashboard.html', results=results)

@quiz_bp.route('/start-quiz')
@login_required
@admin_not_allowed
def start_quiz():
    # Get all questions
    questions = Question.get_all()
    
    if not questions:
        flash('No questions available for the quiz', 'warning')
        return redirect(url_for('quiz.dashboard'))
    
    # Store questions in session
    session['questions'] = [dict(q) for q in questions]
    session['current_question'] = 0
    session['answers'] = {}
    
    return redirect(url_for('quiz.question'))

@quiz_bp.route('/question', methods=['GET', 'POST'])
@login_required
@admin_not_allowed
def question():
    # Check if quiz is in progress
    if 'questions' not in session:
        flash('No quiz in progress', 'warning')
        return redirect(url_for('quiz.dashboard'))
    
    questions = session['questions']
    current_index = session['current_question']
    
    # Handle answering a question
    if request.method == 'POST':
        # Save the answer
        question_id = request.form.get('question_id')
        answer = request.form.get('answer')
        
        if question_id and answer:
            session['answers'][question_id] = answer
            
            # Move to next question
            current_index += 1
            session['current_question'] = current_index
            
            # Check if quiz is complete
            if current_index >= len(questions):
                return redirect(url_for('quiz.result'))
    
    # Get current question
    if current_index < len(questions):
        question = questions[current_index]
        progress = {
            'current': current_index + 1,
            'total': len(questions),
            'percent': int(((current_index + 1) / len(questions)) * 100)
        }
        return render_template('question.html', question=question, progress=progress)
    else:
        return redirect(url_for('quiz.result'))

@quiz_bp.route('/result')
@login_required
@admin_not_allowed
def result():
    # Check if quiz is complete
    if 'questions' not in session or 'answers' not in session:
        flash('No quiz results available', 'warning')
        return redirect(url_for('quiz.dashboard'))
    
    questions = session['questions']
    answers = session['answers']
    
    # Calculate score
    score = 0
    question_results = []
    
    for q in questions:
        q_id = str(q['id'])
        user_answer = answers.get(q_id, '')
        is_correct = user_answer == q['correct_ans']
        
        if is_correct:
            score += 1
        
        question_results.append({
            'question': q['question'],
            'user_answer': user_answer,
            'correct_answer': q['correct_ans'],
            'is_correct': is_correct
        })
    
    # Save result to database
    user_id = session.get('user_id')
    Result.save(user_id, score, len(questions))
    
    # Calculate percentage
    percentage = int((score / len(questions)) * 100) if questions else 0
    
    # Determine result message based on score
    if percentage >= 80:
        message = "Excellent! You did great!"
    elif percentage >= 60:
        message = "Good job! You passed the quiz."
    elif percentage >= 40:
        message = "Not bad, but you can do better."
    else:
        message = "You need more practice. Try again!"
    
    # Clear quiz data
    session.pop('questions', None)
    session.pop('current_question', None)
    session.pop('answers', None)
    
    return render_template(
        'result.html',
        score=score,
        total=len(questions),
        percentage=percentage,
        message=message,
        results=question_results
    )
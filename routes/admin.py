from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Question, Result, User
from functools import wraps

admin_bp = Blueprint('admin', __name__)

# Admin login required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            flash('Admin access required', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin')
@admin_required
def dashboard():
    # Get stats for admin dashboard
    questions = Question.get_all()
    results = Result.get_all()
    
    # Calculate some stats
    total_questions = len(questions)
    total_quizzes = len(results)
    
    # Get unique users who took quizzes
    unique_users = set()
    for result in results:
        unique_users.add(result['user_id'])
    
    # Calculate average score
    average_score = 0
    if total_quizzes > 0:
        total_score_percentage = sum((r['score'] / r['total']) * 100 for r in results)
        average_score = round(total_score_percentage / total_quizzes, 1)
    
    stats = {
        'total_questions': total_questions,
        'total_quizzes': total_quizzes,
        'unique_users': len(unique_users),
        'average_score': average_score
    }
    
    return render_template('admin/dashboard.html', stats=stats, questions=questions, results=results)

@admin_bp.route('/admin/questions')
@admin_required
def questions():
    questions = Question.get_all()
    return render_template('admin/questions.html', questions=questions)

@admin_bp.route('/admin/question/add', methods=['GET', 'POST'])
@admin_required
def add_question():
    if request.method == 'POST':
        # Get form data
        question = request.form.get('question')
        option_a = request.form.get('option_a')
        option_b = request.form.get('option_b')
        option_c = request.form.get('option_c')
        option_d = request.form.get('option_d')
        correct_ans = request.form.get('correct_ans')
        
        # Validate data
        if not all([question, option_a, option_b, option_c, option_d, correct_ans]):
            flash('All fields are required', 'danger')
            return render_template('admin/add_question.html', 
                                  question=question,
                                  option_a=option_a,
                                  option_b=option_b,
                                  option_c=option_c,
                                  option_d=option_d)
        
        # Create question
        Question.create(question, option_a, option_b, option_c, option_d, correct_ans)
        flash('Question added successfully', 'success')
        return redirect(url_for('admin.questions'))
    
    return render_template('admin/add_question.html')

@admin_bp.route('/admin/question/edit/<int:question_id>', methods=['GET', 'POST'])
@admin_required
def edit_question(question_id):
    # Get question
    question = Question.get_by_id(question_id)
    
    if not question:
        flash('Question not found', 'danger')
        return redirect(url_for('admin.questions'))
    
    if request.method == 'POST':
        # Get form data
        question_text = request.form.get('question')
        option_a = request.form.get('option_a')
        option_b = request.form.get('option_b')
        option_c = request.form.get('option_c')
        option_d = request.form.get('option_d')
        correct_ans = request.form.get('correct_ans')
        
        # Validate data
        if not all([question_text, option_a, option_b, option_c, option_d, correct_ans]):
            flash('All fields are required', 'danger')
            return render_template('admin/edit_question.html', question=question)
        
        # Update question
        Question.update(question_id, question_text, option_a, option_b, option_c, option_d, correct_ans)
        flash('Question updated successfully', 'success')
        return redirect(url_for('admin.questions'))
    
    return render_template('admin/edit_question.html', question=question)

@admin_bp.route('/admin/question/delete/<int:question_id>')
@admin_required
def delete_question(question_id):
    # Get question
    question = Question.get_by_id(question_id)
    
    if not question:
        flash('Question not found', 'danger')
        return redirect(url_for('admin.questions'))
    
    # Delete question
    Question.delete(question_id)
    flash('Question deleted successfully', 'success')
    return redirect(url_for('admin.questions'))

@admin_bp.route('/admin/results')
@admin_required
def results():
    results = Result.get_all()
    return render_template('admin/results.html', results=results)
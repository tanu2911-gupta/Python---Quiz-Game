from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'super_secret_key'

questions = [
    {
        "category": "General Knowledge",
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris"
    },
    {
        "category": "Science",
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars"
    },
    {
        "category": "Literature",
        "question": "Who wrote 'Hamlet'?",
        "options": ["Charles Dickens", "J.K. Rowling", "Leo Tolstoy", "William Shakespeare"],
        "answer": "William Shakespeare"
    },
    {
        "category": "Geography",
        "question": "Which is the largest ocean on Earth?",
        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
        "answer": "Pacific"
    },
    {
        "category": "Math",
        "question": "What is the square root of 144?",
        "options": ["10", "12", "14", "16"],
        "answer": "12"
    }
]

@app.route('/')
def home():
    session['score'] = 0
    session['current'] = 0
    session['questions'] = random.sample(questions, len(questions))
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'questions' not in session or session['current'] >= len(session['questions']):
        return redirect(url_for('result'))

    if request.method == 'POST':
        selected = request.form.get('selected_option')
        correct = session['questions'][session['current']]['answer']
        if selected == correct:
            session['score'] = session.get('score', 0) + 1
        session['current'] += 1
        return redirect(url_for('quiz'))

    q = session['questions'][session['current']]
    return render_template('question.html', q=q, qnum=session['current'] + 1, total=len(session['questions']))

@app.route('/result', methods=['GET', 'POST'])
def result():
    score = session.get('score', 0)
    total = len(session.get('questions', []))

    if request.method == 'POST':
        feedback = request.form.get('feedback')
        print("Feedback received:", feedback)
        return render_template('result.html', score=score, total=total, submitted=True)

    return render_template('result.html', score=score, total=total, submitted=False)

if __name__ == '__main__':
    app.run(debug=True)

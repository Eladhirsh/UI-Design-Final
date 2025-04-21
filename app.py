from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Required for session handling

# Homepage Route
@app.route('/')
def home():
    session['start_time'] = str(datetime.now())
    session['choices'] = []
    session['quiz_answers'] = []
    return render_template('home.html')

@app.route('/learn/<int:lesson_num>')
def learn(lesson_num):
    # Load from JSON to make things modular
    with open("data/lessons.json") as f:
        lessons = json.load(f)
    total_lessons = len(lessons)
    return render_template('learn.html', lesson=lessons[lesson_num - 1],
                           lesson_num=lesson_num, total=total_lessons)

@app.route('/quiz/<int:question_num>', methods=['GET', 'POST'])
def quiz(question_num):
    with open("data/quiz.json") as f:
        quiz_data = json.load(f)
    total_questions = len(quiz_data)

    if request.method == 'POST':
        answer = request.form.get('answer')
        session['quiz_answers'].append(answer)
        if question_num < total_questions:
            return redirect(url_for('quiz', question_num=question_num + 1))
        else:
            return redirect(url_for('result'))

    return render_template('quiz.html', question=quiz_data[question_num - 1],
                           question_num=question_num, total=total_questions)
# Result Route
@app.route('/result')
def result():
    user_answers = session.get('quiz_answers', [])
    score = sum(1 for ans in user_answers if ans == "correct")  # Placeholder scoring logic
    return render_template('result.html', score=score, total=len(user_answers))

if __name__ == '__main__':
    app.run(debug=True)

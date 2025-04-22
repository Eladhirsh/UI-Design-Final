from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import json


app = Flask(__name__)
app.secret_key = "super_secret_key"  # Required for session handling

# Homepage Route
@app.route('/')
@app.route('/home')
def home():
    print("✅ Home route reached!")  # 🟢 Proper indentation here
    session['start_time'] = str(datetime.now())
    session['choices'] = []
    session['quiz_answers'] = []
    return render_template('home.html')


@app.route('/learn/<int:lesson_num>')
def learn(lesson_num):
    with open("data/lessons.json", encoding="utf-8") as f:
        lessons = json.load(f)

    # Optional: track when the user entered the lesson
    if 'lesson_times' not in session:
        session['lesson_times'] = {}
    session['lesson_times'][f'lesson_{lesson_num}'] = str(datetime.now())

    print(f"User entered lesson {lesson_num} at {session['lesson_times'][f'lesson_{lesson_num}']}")

    total_lessons = len(lessons)
    return render_template('learn.html',
                           lesson=lessons[lesson_num - 1],
                           lesson_num=lesson_num,
                           total=total_lessons)


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
@app.route('/result')
def result():
    user_answers = session.get('quiz_answers', [])
    with open("data/quiz.json", encoding="utf-8") as f:
        quiz_data = json.load(f)

    score = 0
    for user_answer, q in zip(user_answers, quiz_data):
        if user_answer == q["correct"]:
            score += 1

    return render_template("result.html", score=score, total=len(quiz_data))


if __name__ == '__main__':
    app.run(debug=True)

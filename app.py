from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.get('/')
def index():
    """renders page to show user title of survey"""
    return render_template('survey_start.html',
                        survey_title = survey.title,
                        survey_instructions = survey.instructions)

@app.post('/begin')
def begin():
    """when user clicks start button, should redirect to questions/0 route"""
    return redirect('/questions/0')

@app.get('/questions/<question_num>')
def questions(question_num):
    """generates the question in survey with options for answers"""
    question = survey.questions[int(question_num)]
    return render_template('question.html',
                            question = question,
                            )

@app.post('/answer')
def answer():
    """appends answer to responses list and redirects to next question or thank
    you if last question"""
    question_num = len(responses)
    responses.append(request.form['answer'])
    if question_num < len(survey.questions):
        return redirect(f'/questions/{question_num}')
    else:
        return redirect('/thanks')
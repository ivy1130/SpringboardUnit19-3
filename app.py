from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def index():
    """Return homepage."""

    return render_template("home.html", survey = survey)

@app.route('/start', methods=["POST"])
def start_session():
    """Start new session."""

    session['responses'] = list()
    return redirect('/questions/0')

@app.route('/questions/<i>')
def show_question(i):

    if len(session['responses']) is len(survey.questions):
        """When all questions have already been answered, show a thank you page."""
        return redirect('/thanks')

    elif int(i) not in range(len(survey.questions)):
        """When trying to view a question that is not valid, return an error page."""
        flash('Question is not valid!')
        return redirect(f'/questions/{len(session["responses"])}')
    
    elif int(i) is not len(session['responses']):
        """When trying to skip ahead or go back in questions, redirect user to next question they should answer."""
        flash('Please answer questions in the correct order!')
        return redirect(f'/questions/{len(session["responses"])}')

    """Return question page."""
    return render_template("question.html", i = int(i), survey = survey)

@app.route('/answer', methods=["POST"])
def submit_answer():
    """Append answer choice to responses list"""
    answer = request.form['choices']
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses
    return redirect(f'/questions/{len(session["responses"])}')


@app.route('/thanks')
def thanks():
    """Return thanks page."""
    return render_template("thanks.html")


import random

from flask import Flask, render_template, url_for, request, flash, redirect, Blueprint, session, jsonify
import json

from config import BASE_DIR
from ..auth import authenticate
from ..user import login_required
from ..admin.models import *
from ..user.models import *
import datetime
import os
from fuzzywuzzy import fuzz

# Define the blueprint: 'admin', set its url prefix: app.url/user
user_routes = Blueprint('user', __name__, url_prefix='/')


@user_routes.route('/')
@login_required
def homepage():
    levels = Level.query.all()
    return render_template("user/homepage.html", levels=levels)


# Login Page
@user_routes.route('/login', methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        try:
            user = authenticate(email=request.form['email'], password=request.form['password'])
            if user is None:
                flash("Check Your Credentials Before Proceed", "danger")
                return redirect(url_for("user.login_page"))

            elif user is not None:
                if user.is_admin:
                    flash("Check Your Credentials Before Proceed", "danger")
                    return redirect(url_for("user.login_page"))
                else:
                    session['quizuser'] = json.dumps({"user_id": user.id, "name": user.name, "email": user.email})
                    return redirect(url_for("user.homepage"))
        except Exception as e:
            print(e)
            flash("Something Went Wrong Try Again Later", "warning")
            return redirect(url_for("user.login_page"))

    else:
        return render_template("user/login.html")


@user_routes.route('/logout/')
@login_required
def logout():
    del session['quizuser']
    return redirect(url_for("user.login_page"))


# this middleware is specially for the quiz Route.
# It will Check User Is eligible for the quiz or not.
@user_routes.before_request
def check_for_level():
    if request.endpoint == "user.user_quiz":
        # fetch The Level
        level = Level.query.filter(Level.id == request.view_args['id_']).first()
        # fetch all the Score Board Submitted By User
        score_boards = UserScoreBoard.query.filter(
            UserScoreBoard.user_id == json.loads(session['quizuser'])['user_id']).order_by(-UserScoreBoard.level_id)


@user_routes.route('/quiz/<id_>', methods=["GET", "POST"])
@login_required
def user_quiz(id_):
    level = Level.query.filter(Level.id == id_).one()
    questions = Question.query.filter(Question.level_id == id_)
    if questions.count() == 0:
        flash("This Quiz Set Is Not Available For Now.", "danger")
        return redirect(url_for("user.homepage"))
    # elif (UserScoreBoard.query.filter(UserScoreBoard.level_id == id_,
    #                                   UserScoreBoard.user_id == json.loads(session['quizuser'])[
    #                                       'user_id'])).count() > 0:
    #     flash("You are Already Given This Quiz.", "danger")
    #     return redirect(url_for("user.homepage"))
    else:
        questions = questions.all()
    if request.method == "POST":
        try:
            # Get The Response From The Client Side And Convert It Into Dictionary
            print(request.form['response'])
            try:
                response = json.loads(request.form['response'])
            except:
                response = {}

            # Make The List Of All The IDS of the Answers that is responded by the user
            response_questions_ids = [i['question_id'] for i in response]
            # make an Instance of UserScoreBoard To STore The Result
            board = UserScoreBoard()
            board.level_id = id_
            board.user_id = json.loads(session['quizuser'])['user_id']
            board.test_time = datetime.datetime.now()
            db.session.add(board)
            db.session.commit()
            # loop Through all the questions
            for i in questions:
                # store the question inside the response
                det = ScoreBoardDetail()
                det.scoreboard_id = board.id
                det.level = level.name
                det.question_type = i.questiontype.lower()
                det.total_marks = 10
                db.session.add(det)
                db.session.commit()
                # GET ALL THE QUESTION MARKS FROM JSON FILE
                # with open(os.path.join(BASE_DIR,)
                mcq_marks = 10
                fuzzy_marks = 10
                # check The Type OF The QUestion On Base Of The Type Store it into the corresponding Table

                # IF QUESTION IS MCQ
                if i.questiontype == "MCQ":
                    mcq = MCQQuestionAnswer()
                    mcq.question_id = det.id
                    mcq.question = i.mcq['question']
                    mcq.answer_one = i.mcq['answer_one']
                    mcq.answer_two = i.mcq['answer_two']
                    mcq.answer_three = i.mcq['answer_three']
                    mcq.answer_four = i.mcq['answer_four']
                    mcq.level = level.name
                    mcq.correct = i.mcq['correct']
                    # if User Give The Answer
                    if i.id in response_questions_ids:
                        user_answer = None
                        for k in response:
                            if int(k['question_id']) == int(i.id):
                                user_answer = k['answer']
                        mcq.user_answer = user_answer

                        # Check If User Give The Correct Respone
                        if(mcq.user_answer == i.mcq['correct']):
                            det.obtained_marks = mcq_marks
                            db.session.commit()
                        else:
                            det.obtained_marks = 0
                            db.session.commit()
                    else:
                        det.obtained_marks = 0
                        db.session.commit()

                    db.session.add(mcq)
                    db.session.commit()

                # IF QUESTION IS FUZZY
                elif i.questiontype == "FUZZY":
                    fuzzy = ShortTextQuestionAnswer()
                    fuzzy.question = i.question
                    fuzzy.question_id = det.id
                    fuzzy.answer = i.fuzzy['answer']
                    # if User Give The Answer
                    if i.id in response_questions_ids:
                        user_answer = None
                        for k in response:
                            if int(k['question_id']) == int(i.id):
                                user_answer = k['answer']
                        fuzzy.user_answer = user_answer

                        det.obtained_marks = fuzz.ratio(str(fuzzy.answer),str(user_answer))/10
                        db.session.commit()
                    else:
                        det.obtained_marks = 0
                    db.session.add(fuzzy)
                    db.session.commit()

                # IF QUESTION IS LONG TEXT TYPE
                elif i.questiontype == "LONG_TEXT":
                    long = LongTextQuestionAnswer()
                    long.question_id = det.id
                    long.question = i.question
                    # if User Give The Answer
                    if i.id in response_questions_ids:
                        user_answer = None
                        for k in response:
                            if int(k['question_id']) == int(i.id):
                                user_answer = k['answer']
                        long.answer = user_answer
                    db.session.add(long)
                    db.session.commit()

                db.session.add(det)
                db.session.commit()
            flash("Your Quiz Is Submitted Successfully.", "success")

        except Exception as e:
            print(e)
            flash("Your Quiz is not submitted,because you don't answer atleast one question Or Something Went Wrong.",
                  "warning")

        finally:
            return redirect(url_for("user.scoreboard"))
    else:
        return render_template("user/quiz.html", questions=questions, quiz_id=id_)


# Ensure responses aren't cached
@user_routes.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@user_routes.route('/api/quiz/<quizid>/', methods=["GET", "POST"])
@login_required
def get_questions(quizid):
    questions = Question.query.filter_by(level_id=quizid)
    result = [d.serialize for d in questions]
    random.shuffle(result)
    result = result[:10]
    return jsonify(result), 200




@user_routes.route('/register/', methods=["GET", "POST"])
def user_register():
    if request.method == "POST":
        try:
            name = request.form['user_name']
            email = request.form['user_email']
            password = request.form['user_password']
            cpassword = request.form['user_cpassword']
            if name == "":
                flash("Name Of User Can't Be Empty.", "danger")
            elif email == "":
                flash("Email Of User Can't Be Empty.", "danger")
            elif password == "":
                flash("Password Of User Can't Be Empty.", "danger")
            elif len(password) < 6:
                flash("Password length should more than 6 Characters", "warning")
            elif password != cpassword:
                flash("Password And Confirm Password Doesn't Match.", "danger")
            elif User.query.filter(User.email == email).count() > 0:
                flash("This Email Is Already Exist", "danger")
            else:
                user = User(name=name, email=email, password=password)
                db.session.add(user)
                db.session.commit()
                session['quizuser'] = json.dumps({"user_id": user.id, "name": user.name, "email": user.email})
                flash("Signup Successfully", "success")
                return redirect(url_for("user.homepage"))
        except Exception as e:
            print(e)
            flash("Something Went Wrong.Try Again Later", "danger")

        finally:
            return redirect(url_for("user.user_register"))

    else:
        return render_template("user/register.html")




@user_routes.route('/scoreboard')
@login_required
def scoreboard():
    scoreboard_ = UserScoreBoard.query.filter(
        UserScoreBoard.user_id == json.loads(session['quizuser'])['user_id']).all()
    return render_template("user/scoreboard.html", scoreboard=scoreboard_)


@user_routes.route('/scoreboard/<id_>')
@login_required
def scoreboard_detail(id_):
    board = UserScoreBoard.query.filter(UserScoreBoard.id == id_)
    if board.count()>0 and board.first().user is not None:
        board = board.first()       
        if board.user_id == json.loads(session['quizuser'])['user_id']:
            details = ScoreBoardDetail.query.filter(ScoreBoardDetail.scoreboard_id == id_).all()
            return render_template("user/scoreboarddetails.html", details=details, board_id=board.id, board=board)
        else:
            flash("You are not authorised.","warning")
            return redirect(url_for("user.scoreboard"))
    else:
        flash("This Scoreboard is not available.","warning")
        return redirect(url_for("user.scoreboard"))

@user_routes.route('/api/board/<id_>/', methods=["GET", "POST"])
def get_score_board_detail(id_):
    board = UserScoreBoard.query.filter(UserScoreBoard.id == id_).first()
    details = ScoreBoardDetail.query.filter(ScoreBoardDetail.scoreboard_id == id_).all()
    result = [d.serialize for d in details]
    return jsonify(result), 200

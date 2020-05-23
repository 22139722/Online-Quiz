import json

from flask import Flask, render_template, url_for, request, flash, redirect, Blueprint, session, jsonify
from app import app,db,UPLOAD_FOLDER
from app import signals,auth
from app.admin import login_required
from werkzeug.utils import secure_filename
from sqlalchemy import or_

from app.user.models import *
from . models import *
import os
# Define the blueprint: 'admin', set its url prefix: app.url/admin
admin_routes = Blueprint('admin', __name__, url_prefix='/admin')
@admin_routes.route('/')
@login_required
def homepage():
    users = User.query.count()
    levels = Level.query.count()
    questions = Question.query.count()
    return render_template("admin/homepage.html",users=users,levels=levels,questions=questions)


@admin_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = auth.authenticate(email=request.form['email'],password=request.form['password'])
        if user is None:
            flash("Incorrect Credentials", "danger")
            return redirect(url_for('admin.login'))
        else:
            if user.is_admin:
                flash("Successfully Logged In", "success")
                session['quizadmin'] = user.id
                return redirect(url_for('admin.homepage'))
            else:
                flash("Incorrect Credentials You Are Not Admin User", "danger")
                return redirect(url_for('admin.login'))
    else:
        return render_template("admin/login.html")
@admin_routes.route('/level/add', methods=["GET", "POST"])
@login_required
def add_level():
    if request.method == "POST":
        try:
            if request.form['level_name'] == "":
                flash("Level Name Can't Be Empty", "danger")

            elif request.form['priority'] == "" or (not str(request.form['priority']).isdigit()):
                flash("Priority Can't be Empty", "danger")

            elif str(request.files.get("image").content_type).split("/")[0] != "image":
                flash("Image Can't Be Empty or Enter Correct Format Of Image", "danger")

            elif Level.query.filter_by(name=request.form['level_name']).count() > 0:
                flash("Level Name Already Exist.Try Another Level Name", "warning")

            elif Level.query.filter_by(priority=request.form['priority']).count() > 0:
                flash("Priority Is Already Exist.", "warning")

            else:
                # extract the image
                f: object = request.files['image']
                filename = secure_filename(f.filename)
                # save image to the directory
                f.save(os.path.join(app.config['UPLOAD_DIR'], filename))
                # Save data to the databse
                l = Level()
                l.name = request.form['level_name']
                l.priority = request.form['priority']
                l.image = UPLOAD_FOLDER + str(filename)
                db.session.add(l)
                db.session.commit()
                # Send The Flash Message
                flash("Level Saved Successfully.", "success")
        except Exception as e:
            print(e)
            flash("Something Went Wrong.Try Again Later.", "danger")
        finally:
            return redirect(url_for('admin.add_level'))

    else:
        return render_template("admin/addlevel.html")


@admin_routes.route('/level/edit/<id_>', methods=["GET", "POST"])
@login_required
def edit_level(id_):
    level = Level.query.filter_by(id=id_).one()
    if request.method == "POST":
        try:
            if request.form['level_name'] == "":
                flash("Level Name Can't Be Empty", "danger")

            elif request.form['priority'] == "" or (not str(request.form['priority']).isdigit()):
                flash("Priority Can't be Empty", "danger")

            elif Level.query.filter(Level.name == request.form['level_name'], Level.id != id_).count() > 0:
                flash("Level Name Already Exist Is Other Level.Try Another Level Name", "warning")

            elif Level.query.filter(Level.priority == request.form['priority'], Level.id != id_).count() > 0:
                flash("Priority Is Already Exist in other Level.", "warning")

            else:

                if request.files.get("image").content_length == 0 and \
                        str(request.files.get("image").content_type).split("/")[0] == "image":
                    # extract the image
                    f: object = request.files['image']
                    filename = secure_filename(f.filename)
                    # remove existing Image
                    image = level.image.replace("uploads/", "")
                    os.remove(os.path.join(app.config['UPLOAD_DIR'], image))
                    # save image to the directory
                    f.save(os.path.join(app.config['UPLOAD_DIR'], filename))
                    level.image = UPLOAD_FOLDER + str(filename)
                else:
                    # Update data to the databse
                    level.name = request.form['level_name']
                    level.priority = request.form['priority']
                db.session.commit()
                # Send The Flash Message
                flash("Level Updated Successfully.", "success")
        except Exception as e:
            print(e)
            flash("Something Went Wrong.Try Again Later.", "danger")
        finally:
            return redirect(url_for('admin.edit_level', id_=id_))

    else:
        return render_template("admin/editlevel.html", level=level)


@admin_routes.route('/level/manage')
@login_required
def manage_levels():
    levels = Level.query.order_by(Level.priority).all()
    return render_template("admin/managelevels.html", levels=levels)


@admin_routes.route('/level/delete/<id_>', methods=["POST"])
@login_required
def delete_level(id_):
    try:
        level = Level.query.filter_by(id=id_).first()
        # remove existing Image
        image = level.image.replace("uploads/", "")
        os.remove(os.path.join(app.config['UPLOAD_DIR'], image))
        # delete the row with id id_
        db.session.delete(level)
        db.session.commit()
        # send the flash message and redirect to the manage levels
        flash("Level Deleted Successfully.", "success")
    except:
        flash("Something Went Wrong.Try Again Later.", "danger")
    finally:
        return redirect(url_for("admin.manage_levels"))

        
@admin_routes.route('/question/add', methods=["GET", "POST"])
@login_required
def add_question():
    if request.method == "POST":
        try:
            question = Question()
            question.level_id = request.form['level']
            question.question_type = request.form['type']
            db.session.add(question)
            db.session.commit()

            if request.form['type'] == "long_text":
                ques = LongTextQuestion()
                ques.question_id = question.id
                ques.question = request.form['question']
                db.session.add(ques)
                db.session.commit()
            elif request.form['type'] == "fuzzy":
                ques = ShortTextQuestion()
                ques.question_id = question.id
                ques.question = request.form['question']
                ques.answer = request.form['short_answer']
                db.session.add(ques)
                db.session.commit()
            else:
                ques = MCQQuestion()
                ques.question_id = question.id
                ques.question = request.form['question']
                ques.answer_one = request.form['answer_one']
                ques.answer_two = request.form['answer_two']
                ques.answer_three = request.form['answer_three']
                ques.answer_four = request.form['answer_four']
                ques.correct = request.form['correct_answer']
                db.session.add(ques)
                db.session.commit()
            flash("Question Added Successfully.", "success")
        except Exception as e:
            print(e)
            flash("Something went wrong,Try Again Later", "danger")
        finally:
            return redirect(url_for("admin.add_question"))
    else:
        levels = Level.query.all()
        return render_template("admin/addquestion.html", levels=levels)

@admin_routes.route('/question/manage', methods=["GET", "POST"])
@login_required
def manage_questions():
    questions = Question.query.all()
    levels = Level.query.all()
    return render_template("admin/managequestions.html", questions=questions,levels=levels)

@admin_routes.route('/question/edit/<id_>', methods=["GET", "POST"])
@login_required
def edit_question(id_):
    question = Question.query.filter(Question.id==id_).first()
    if request.method == "POST":
        try:

            question.level_id = request.form['level']
            question.question_type = request.form['type']
            db.session.commit()

            if request.form['type'] == "long_text":
                ques = LongTextQuestion.query.filter(LongTextQuestion.question_id==question.id).one()
                ques.question = request.form['question']
                db.session.commit()
            elif request.form['type'] == "fuzzy":
                ques = ShortTextQuestion.query.filter(ShortTextQuestion.question_id==question.id).first()
                ques.question_id = question.id
                ques.question = request.form['question']
                ques.answer = request.form['short_answer']
                db.session.commit()
            elif request.form['type'] == "mcq":
                ques = MCQQuestion.query.filter(MCQQuestion.question_id==question.id).first()
                ques.question_id = question.id
                ques.question = request.form['question']
                ques.answer_one = request.form['answer_one']
                ques.answer_two = request.form['answer_two']
                ques.answer_three = request.form['answer_three']
                ques.answer_four = request.form['answer_four']
                ques.correct = request.form['correct_answer']
                db.session.commit()
            flash("Question Updated Successfully.", "success")
        except Exception as e:
            flash("Something went wrong,Try Again Later", "danger")
        finally:
            return redirect(url_for("admin.edit_question",id_=id_))
    else:
        levels = Level.query.all()
        mcq = MCQQuestion.query.filter(MCQQuestion.question_id==question.id).first()
        fuzzy = ShortTextQuestion.query.filter(ShortTextQuestion.question_id==question.id).first()
        return render_template("admin/editquestion.html", levels=levels,question=question,mcq=mcq,fuzzy=fuzzy)

@admin_routes.route('/question/delete/<id_>', methods=["GET", "POST"])
@login_required
def delete_question(id_):
    try:
        question = Question.query.filter(Question.id==id_).one()
        q= None
        if question.questiontype == "FUZZY":
            q = ShortTextQuestion.query.filter(ShortTextQuestion.question_id==question.id).first()
        elif question.questiontype == "MCQ":
            q = MCQQuestion.query.filter(MCQQuestion.question_id==question.id).first()
        elif question.questiontype == "LONG_TEXT":
            q = LongTextQuestion.query.filter(LongTextQuestion.question_id==question.id).first()

        db.session.delete(q)
        db.session.delete(question)
        db.session.commit()
        flash("Question Deleted Successfully.", "success")
    except Exception as e:
        print(e)
        flash("Something Went Wrong,Try again later.","danger")
    finally:

        return redirect(url_for("admin.manage_questions"))

# USER CRUD ROUTES
@admin_routes.route('/user/add', methods=["GET", "POST"])
@login_required
def add_user():
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
            elif password != cpassword:
                flash("Password And Confirm Password Doesn't Match.", "danger")
            elif User.query.filter(User.email == email).count() > 0:
                flash("This Email Is Already Exist", "danger")
            else:
                user = User(name=name, email=email, password=password)
                db.session.add(user)
                db.session.commit()
                flash("User Created Successfully", "success")
        except Exception as e:
            print(e)
            flash("Something Went Wrong.Try Again Later", "danger")
        finally:
            return redirect(url_for("admin.add_user"))
    else:
        return render_template("admin/adduser.html")


@admin_routes.route('/user/editpro/<id_>', methods=["GET", "POST"])
@login_required
def edit_user_profile(id_):
    user = User.query.filter(User.id == id_).first()
    if request.method == "POST":
        try:

            name = request.form['user_name']
            email = request.form['user_email']
            if name == "":
                flash("Name Of User Can't Be Empty.", "danger")
            elif email == "":
                flash("Email Of User Can't Be Empty.", "danger")
            elif User.query.filter(User.email == email, User.id != id_).count() > 0:
                flash("This Email Is Already Taken", "danger")
            else:
                user.name = name
                user.email = email
                db.session.commit()
                flash("User Profile Updated Successfully.", "success")
        except:
            flash("Something Went Wrong.Try Again Later", "danger")
        finally:
            return redirect(url_for("admin.edit_user_profile", id_=id_))
    else:
        return render_template("admin/editprofile.html", user=user)

@admin_routes.route('/user/delete/<id_>', methods=["GET", "POST"])
@login_required
def delete_user(id_):
    try:
        user = User.query.filter(User.id==id_).one()
        db.session.delete(user)
        db.session.commit()
        flash("User deleted Successfully.","success")
    except:
        flash("Something Went Wrong.Try Again Later.","danger")
    finally:
        return redirect(url_for("admin.manage_users"))

@admin_routes.route('/user/editpassword/<id_>', methods=["GET", "POST"])
@login_required
def change_user_password(id_):
    user = User.query.filter(User.id == id_).first()
    if request.method == "POST":
        try:
            password = request.form['user_password']
            cpassword = request.form['user_cpassword']
            if password == "":
                flash("Password Of User Can't Be Empty.", "danger")
            if cpassword == "":
                flash("Password Of User Can't Be Empty.", "danger")
            elif password != cpassword:
                flash("Password And Confirm Password Doesn't Match.", "danger")
            else:
                user.password = signals.generate_password(password)
                db.session.commit()
                flash("User Password Updated Successfully.", "success")
        except:
            flash("Something Went Wrong.Try Again Later", "danger")
        finally:
            return redirect(url_for("admin.change_user_password", id_=id_))

    return render_template("admin/changeuserpassword.html", user=user)





@admin_routes.route('/user/manage')
@login_required
def manage_users():
    users = User.query.all()
    print(users)
    return render_template("admin/viewusers.html", users=users)

@admin_routes.route('/logout')
@login_required
def admin_logout():
    del session['quizadmin']
    return redirect(url_for("admin.login"))


#SCOREBOARD ROUTES

@admin_routes.route('/scoreboard')
@login_required
def scoreboard():
    users = User.query.all()
    levels = Level.query.all()
    scoreboard_ = UserScoreBoard.query.all()
    return render_template("admin/scoreboard.html",scoreboard=scoreboard_,users=users,levels=levels)

@admin_routes.route('/scoreboard/<id_>',methods=["GET","POST"])
@login_required
def scoreboard_detail(id_):

    if request.method == "POST":
        print(request.form)
        for i in request.form:
            if len(i.split("res-"))>0:
                try:

                    det = ScoreBoardDetail.query.filter(ScoreBoardDetail.id == int(i.split("res-")[1])).one()
                    det.obtained_marks = request.form[i]
                    print(det)
                    db.session.commit()
                except Exception as e:
                    print(e)
        flash("ScoreBoard Updated SUccessfully","success")
        return redirect(url_for("admin.scoreboard_detail",id_=id_))
    else:
        board = UserScoreBoard.query.filter(UserScoreBoard.id == id_).first()
        details = ScoreBoardDetail.query.filter(ScoreBoardDetail.scoreboard_id == id_).all()
        return render_template("admin/scoreboarddetails.html",details=details,board_id=board.id,
                                                              board=board)


@admin_routes.route('/api/board/<id_>/',methods=["GET","POST"])
def get_score_board_detail(id_):
    board = UserScoreBoard.query.filter(UserScoreBoard.id == id_).first()
    details = ScoreBoardDetail.query.filter(ScoreBoardDetail.scoreboard_id == id_).all()
    print(details)
    result = [d.serialize for d in details]
    return jsonify(result), 200

@admin_routes.route('/api/board/<user_id>/<level_id>',methods=["GET","POST"])
def filter_score_board_detail(user_id,level_id):
    board = db.session.query(UserScoreBoard).filter(or_(UserScoreBoard.user_id == user_id,UserScoreBoard.level_id==level_id)).all()
    result = [d.serialize for d in board]
    return jsonify(result), 200

@admin_routes.route('/api/board/delete/<board_id>/',methods=["GET","POST"])
def delete_score_board(board_id):
    board = UserScoreBoard.query.filter(UserScoreBoard.id == board_id).first()
    details = ScoreBoardDetail.query.filter(ScoreBoardDetail.scoreboard_id == board_id).all()
    for i in details:
        db.session.delete(i)
        db.session.commit()

    db.session.delete(board)
    db.session.commit()
    flash("Score Board Deleted Successfully.","danger")
    return redirect(url_for("admin.scoreboard"))

@admin_routes.route('/api/questions/<level_id>/',methods=["GET","POST"])
def get_questions_level_wise(level_id):
    questions = Question.query.filter(Question.level_id==level_id)
    res = [i.serialize for i in questions]
    return jsonify(res),200


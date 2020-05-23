import datetime
import enum
from app import db


class UserScoreBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
    user = db.relationship("User", foreign_keys=user_id)
    test_time = db.Column(db.TIMESTAMP, nullable=False)

    level_id = db.Column(db.Integer, db.ForeignKey('level.id'),
                         nullable=True)
    level = db.relationship("Level", foreign_keys=level_id)

    @property
    def get_test_date(self):
        return str(self.test_time.date())

    @property
    def get_test_time(self):
        return str(self.test_time.time())

    @property
    def get_scoreboard_details(self):
        return ScoreBoardDetail.query.filter(ScoreBoardDetail.scoreboard_id == self.id)

    @property
    def total_questions(self):
        return self.get_scoreboard_details.count()

    @property
    def total_marks(self):
        total = 0
        for i in self.get_scoreboard_details.all():
            try:
                total += float(i.total_marks)
            except:
                total += 0
        return total

    @property
    def obtained_marks(self):
        total = 0
        for i in self.get_scoreboard_details.all():
            try:
                total += float(i.obtained_marks)
            except:
                total+= 0
        return total


    @property
    def unanswered_answers(self):
        return self.get_scoreboard_details.filter(ScoreBoardDetail.user_answer == None).count()

    @property
    def incorrect_answers(self):
        return self.get_scoreboard_details.filter(ScoreBoardDetail.user_answer != None,
                                                  ScoreBoardDetail.user_answer != ScoreBoardDetail.correct).count()

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.user.name,
            "email": self.user.email,
            "date": self.get_test_date,
            "time": self.get_test_time,
            "level": self.level.name,
            "total_questions": self.total_questions,
            "total_marks": self.total_marks,
            "obtained_marks":self.obtained_marks
        }



class ScoreBoardQuestionType(enum.Enum):
    mcq = "mcq"
    long_text = "long_text"
    fuzzy = "fuzzy"


class ScoreBoardDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scoreboard_id = db.Column(db.Integer, db.ForeignKey('user_score_board.id'),
                              nullable=False)
    level = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.Enum(ScoreBoardQuestionType), nullable=False)
    total_marks = db.Column(db.Integer, nullable=False)
    obtained_marks = db.Column(db.Integer, nullable=True)

    @property
    def longquesans(self):
        if self.questiontype == "LONG_TEXT":
            long_question = LongTextQuestionAnswer.query.filter(LongTextQuestionAnswer.question_id == self.id)
            if long_question.count() > 0:
                long_question = long_question.one()
                return {
                    "id":long_question.id,
                    "question": long_question.question,
                    "user_answer": long_question.answer
                }
            else:
                return []

    @property
    def fuzzy(self):
        if self.questiontype == "FUZZY":
            fuzzy_question = ShortTextQuestionAnswer.query.filter(ShortTextQuestionAnswer.question_id == self.id)
            if fuzzy_question.count() > 0:
                fuzzy_question = fuzzy_question.one()
                return {
                    "question": fuzzy_question.question,
                    "answer": fuzzy_question.answer,
                    "user_answer":fuzzy_question.user_answer
                }
            else:
                return []

    @property
    def question(self):
        if self.questiontype == "MCQ":
            ques = MCQQuestionAnswer.query.filter(MCQQuestionAnswer.question_id == self.id).first()
            return ques.question

        elif self.questiontype == "LONG_TEXT":
            ques = LongTextQuestionAnswer.query.filter(LongTextQuestionAnswer.question_id == self.id).first()
            return ques.question

        elif self.questiontype == "FUZZY":
            ques = ShortTextQuestionAnswer.query.filter(ShortTextQuestionAnswer.question_id == self.id).first()
            return ques.question

    @property
    def mcq(self):
        if self.questiontype == "MCQ":
            mcq_question = MCQQuestionAnswer.query.filter(MCQQuestionAnswer.question_id == self.id)
            if mcq_question.count() == 1:
                mcq_question = mcq_question.one()
                return {
                    "question": mcq_question.question,
                    "answer_one": mcq_question.answer_one,
                    "answer_two": mcq_question.answer_two,
                    "answer_three": mcq_question.answer_three,
                    "answer_four": mcq_question.answer_four,
                    "correct": mcq_question.correct,
                    "user_answer": mcq_question.user_answer
                }
            return []


    @property
    def unanswered(self):
        if self.user_answer == None:
            return True
        else:
            return False

    @property
    def is_correct(self):
        if self.user_answer == None:
            return True
        else:
            if self.correct == self.user_answer:
                return True
            else:
                return False

    @property
    def is_incorrect(self):
        if self.user_answer == None:
            return True
        else:
            if self.correct != self.user_answer:
                return True
            else:
                return False

    @property
    def questiontype(self):
        return (str(self.question_type).split(".")[1].upper())

    @property
    def serialize(self):
        return {
            "id": self.id,
            "level_id": self.level,
            "type": self.questiontype,
            "question": self.question,
            "mcq": self.mcq,
            "fuzzy": self.fuzzy,
            "type": self.questiontype,
            "long":self.longquesans
        }

class MCQQuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('score_board_detail.id'),
                            nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer_one = db.Column(db.Text, nullable=False)
    answer_two = db.Column(db.Text, nullable=False)
    answer_three = db.Column(db.Text, nullable=False)
    answer_four = db.Column(db.Text, nullable=False)
    correct = db.Column(db.Integer, nullable=False)
    user_answer = db.Column(db.Integer, nullable=True)


class LongTextQuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('score_board_detail.id'),
                            nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=True)


class ShortTextQuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('score_board_detail.id'),
                            nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    user_answer = db.Column(db.Text, nullable=False)



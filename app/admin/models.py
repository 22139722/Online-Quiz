from app import db
from app import signals
import enum

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(120), unique=False, nullable=False)
    priority = db.Column(db.Integer, unique=True, nullable=False)

    def __init__(self, name=None, image=None, priority=None):
        self.name = name
        self.image = image
        self.priority = priority

    def __repr__(self):
        return '<Level %r>' % self.name

class QuestionType(enum.Enum):
    mcq = "mcq"
    long_text = "long_text"
    fuzzy = "fuzzy"


class MCQQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'),
                            nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer_one = db.Column(db.Text, nullable=False)
    answer_two = db.Column(db.Text, nullable=False)
    answer_three = db.Column(db.Text, nullable=False)
    answer_four = db.Column(db.Text, nullable=False)
    correct = db.Column(db.Integer, nullable=False)



class LongTextQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'),
                            nullable=False)
    question = db.Column(db.Text, nullable=False)


class ShortTextQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'),
                            nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'),
                         nullable=False)
    level = db.relationship("Level", foreign_keys=level_id)
    question_type = db.Column(db.Enum(QuestionType))

    def __repr__(self):
        return '<Question %r>' % self.id

    @property
    def questiontype(self):
        return (str(self.question_type).split(".")[1].upper())

    @property
    def question(self):
        if self.questiontype == "MCQ":
            ques = MCQQuestion.query.filter(MCQQuestion.question_id==self.id).first()
            return ques.question

        elif self.questiontype == "LONG_TEXT":
            ques = LongTextQuestion.query.filter(LongTextQuestion.question_id==self.id).first()
            return ques.question

        elif self.questiontype == "FUZZY":
            ques = ShortTextQuestion.query.filter(ShortTextQuestion.question_id==self.id).first()
            return ques.question

    @property
    def fuzzy(self):
        if self.questiontype == "FUZZY":
            fuzzy_question = ShortTextQuestion.query.filter(ShortTextQuestion.question_id == self.id)
            if fuzzy_question.count()>0:
                fuzzy_question = fuzzy_question.one()
                return {
                    "question":fuzzy_question.question,
                    "answer":fuzzy_question.answer
                }
            else:
                return []
    @property
    def mcq(self):
        if self.questiontype == "MCQ":
            mcq_question = MCQQuestion.query.filter(MCQQuestion.question_id==self.id)
            if mcq_question.count()==1:
                mcq_question = mcq_question.one()
                return {
                    "question":mcq_question.question,
                    "answer_one":mcq_question.answer_one,
                    "answer_two":mcq_question.answer_two,
                    "answer_three":mcq_question.answer_three,
                    "answer_four":mcq_question.answer_four,
                    "correct":mcq_question.correct,

                }
            return []


    @property
    def serialize(self):
        return {
            "id": self.id,
            "level_id": self.level_id,
            "type":self.questiontype,
            "question":self.question,
            "mcq":self.mcq,
            "fuzzy":self.fuzzy,

        }

# END MODELS

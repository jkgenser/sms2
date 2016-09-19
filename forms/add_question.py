from flask_wtf import Form
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Length

class NewQuestionOneForm(Form):
    option_one = StringField('Option one text', validators=[DataRequired()])
    option_one_letter = StringField('Option one letter', validators=[DataRequired()])

    option_two = StringField('Option two text', validators=[DataRequired()])
    option_two_letter = StringField('Option two letter', validators=[DataRequired()])

    option_three = StringField('Option three text')
    option_three_letter = StringField('Option three letter', validators=[DataRequired()])

class NewQuestionTwoForm(Form):
    question_two_text = StringField('Question two text', validators=[DataRequired()])
    question_two_letter = StringField('Question two letter', validators=[DataRequired()])
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField,MultipleFileField
from wtforms.validators import DataRequired,Email,EqualTo,ValidationError,Length

class Beamform(FlaskForm):
    case_id=StringField('Case id',validators=[DataRequired(),Length(min=0,max=140)])
    submit=SubmitField('修改/查詢')
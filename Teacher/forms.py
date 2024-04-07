from typing import Optional
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    IntegerField,
    FieldList,
    FormField,
    Form,
    RadioField,
    DecimalField,
)
from flask_wtf.file import FileField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
    NumberRange,
    Optional,
)
from Teacher.models import User
from flask_wtf.file import FileField, FileAllowed, FileRequired


class RegistrationForm(FlaskForm):
    username = StringField(
        label="Username", validators=[DataRequired(), Length(min=5, max=30)]
    )
    # email = StringField(label = 'Email', validators=[DataRequired(),Email()])
    password1 = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password1")]
    )
    submit = SubmitField("Register")

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError("Username already exists!")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class uploadcsv(FlaskForm):
    cie_number = IntegerField("CIE Number", validators=[NumberRange(min=1, max=3)])

    file = FileField(
        "Upload Student Marks", validators=[FileRequired()]
    )  # , FileAllowed('csv', 'Please Upload only csv files!')


class addcourse(FlaskForm):
    coursename = StringField("Course Name", validators=[DataRequired()])
    coursecode = StringField("Course Code", validators=[DataRequired()])
    co_number = IntegerField("Number of Co's", validators=[NumberRange(min=1, max=10)])
    # lab = StringField("Is it Lab Course", validators=[DataRequired(), Length(min=1, max=1)])
    lab = RadioField(
        "LAB Component",
        choices=[
            ("choice1", "Yes, it has a lab component"),
            ("choice2", "No, it doesn't have a lab component"),
        ],
    )
    sem = IntegerField(
        "Semester ", validators=[DataRequired(), NumberRange(min=1, max=8)]
    )
    dicop1 = DecimalField(
        "Direct-Indirect Attainment Ratio ", validators=[DataRequired(), NumberRange(max=100)]
    )
    dicop2 = DecimalField(
        "Direct-Indirect Attainment Ratio ", validators=[DataRequired(), NumberRange(max=100)]
    )
    scop1 = DecimalField(
        "Direct Attainment Ratio ", validators=[DataRequired(), NumberRange(max=100)]
    )
    scop2 = DecimalField(
        "Direct Attainment Ratio ", validators=[DataRequired(), NumberRange(max=100)]
    )
    ciet = DecimalField(
        "Internal-Test Percentage", validators=[DataRequired(), NumberRange(max=100)]
    )
    cieq = DecimalField(
        "Internal-Quiz Percentage", validators=[DataRequired(), NumberRange(max=100)]
    )
    assign = DecimalField(
        "Internal-Assignment Percentage", validators=[DataRequired(), NumberRange(max=100)]
    )
    
    level1 = DecimalField('Level 1 Percentage', validators=[DataRequired(), NumberRange(max=100)])
    level2 = DecimalField('Level 2 Percentage', validators=[DataRequired(), NumberRange(max=100)])
    level3 = DecimalField('Level 3 Percentage', validators=[DataRequired(), NumberRange(max=100)])                        
    
    target = DecimalField('Target %', validators=[DataRequired(), NumberRange(max=100)])    
    submit = SubmitField("Add Course")


class quiz_mapping(FlaskForm):
    quiz_number = IntegerField("CIE Number", validators=[NumberRange(min=1, max=3)])

    quizversion = StringField(
        "Quiz-Version", validators=[DataRequired(), Length(min=1, max=3)]
    )

    q1 = IntegerField(
        "Q-1", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q2 = IntegerField(
        "Q-2", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q3 = IntegerField(
        "Q-3", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q4 = IntegerField(
        "Q-4", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q5 = IntegerField(
        "Q-5", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q6 = IntegerField(
        "Q-6", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q7 = IntegerField(
        "Q-7", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q8 = IntegerField(
        "Q-8", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q9 = IntegerField(
        "Q-9", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q10 = IntegerField(
        "Q-10", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q11 = IntegerField(
        "Q-11", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q12 = IntegerField(
        "Q-12", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q13 = IntegerField(
        "Q-13", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q14 = IntegerField(
        "Q-14", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q15 = IntegerField(
        "Q-15", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )

    q1m = IntegerField(
        "Q-1", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q2m = IntegerField(
        "Q-2", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q3m = IntegerField(
        "Q-3", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q4m = IntegerField(
        "Q-4", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q5m = IntegerField(
        "Q-5", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q6m = IntegerField(
        "Q-6", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q7m = IntegerField(
        "Q-7", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q8m = IntegerField(
        "Q-8", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q9m = IntegerField(
        "Q-9", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q10m = IntegerField(
        "Q-10", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q11m = IntegerField(
        "Q-11", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q12m = IntegerField(
        "Q-12", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q13m = IntegerField(
        "Q-13", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q14m = IntegerField(
        "Q-14", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )
    q15m = IntegerField(
        "Q-15", validators=[NumberRange(min=0, max=3), Optional(strip_whitespace=True)]
    )

    submit = SubmitField("Submit Mappings")


class test_mapping(FlaskForm):
    test_number = IntegerField(
        "CIE Number", validators=[DataRequired(), NumberRange(min=1, max=3)]
    )

    q1a = IntegerField(
        "Q-1a", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q1b = IntegerField(
        "Q-1b", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q1c = IntegerField(
        "Q-1c", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )

    q2a = IntegerField(
        "Q-2a", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q2b = IntegerField(
        "Q-2b", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q2c = IntegerField(
        "Q-2c", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )

    q3a = IntegerField(
        "Q-3a", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q3b = IntegerField(
        "Q-3b", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q3c = IntegerField(
        "Q-3c", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )

    q4a = IntegerField(
        "Q-4a", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q4b = IntegerField(
        "Q-4b", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q4c = IntegerField(
        "Q-4c", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )

    q5a = IntegerField(
        "Q-5a", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q5b = IntegerField(
        "Q-5b", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )
    q5c = IntegerField(
        "Q-5c", validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)]
    )

    q1am = IntegerField(
        "Marks:Q-1a",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )
    q1bm = IntegerField(
        "Marks:Q-1b",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )
    q1cm = IntegerField(
        "Marks:Q-1c",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )

    q2am = IntegerField(
        "Marks:Q-2a",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )
    q2bm = IntegerField(
        "Marks:Q-2b",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )
    q2cm = IntegerField(
        "Marks:Q-2c",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )

    q3am = IntegerField(
        "Marks:Q-3a",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )
    q3bm = IntegerField(
        "Marks:Q-3b",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )
    q3cm = IntegerField(
        "Marks:Q-3c",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )

    q4am = IntegerField(
        "Marks:Q-4a",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )
    q4bm = IntegerField(
        "Marks:Q-4b",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )
    q4cm = IntegerField(
        "Marks:Q-4c",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )

    q5am = IntegerField(
        "Marks:Q-5a",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )
    q5bm = IntegerField(
        "Marks:Q-5b",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )
    q5cm = IntegerField(
        "Marks:Q-5c",
        validators=[NumberRange(min=0, max=10), Optional(strip_whitespace=True)],
    )

    submit = SubmitField("Submit Mappings")


class uploadsem(FlaskForm):

    file = FileField(
        "Upload Student Marks", validators=[FileRequired()]
    )  # , FileAllowed('csv', 'Please Upload only csv files!')
    submit = SubmitField("Submit File")


class co_details(Form):
    details = StringField(
        "CO Details", validators=[DataRequired(), Length(min=2, max=300)]
    )


class all_co(FlaskForm):
    cos = FieldList(FormField(co_details), min_entries=1)
    submit = SubmitField("Submit CO's")


class number_phases(FlaskForm):

    number = IntegerField(
        "Number of Phases ", validators=[DataRequired(), NumberRange(min=1, max=5)]
    )
    submit = SubmitField("Submit")


class single_phase(Form):
    rubrics1 = IntegerField(
        "CO rubrics1", validators=[NumberRange(min=0, max=10)], default=0
    )
    rubrics2 = IntegerField(
        "CO rubrics2", validators=[NumberRange(min=0, max=10)], default=0
    )
    rubrics3 = IntegerField(
        "CO rubrics3", validators=[NumberRange(min=0, max=10)], default=0
    )
    rubrics4 = IntegerField(
        "CO rubrics4", validators=[NumberRange(min=0, max=10)], default=0
    )
    rubrics5 = IntegerField(
        "CO rubrics5", validators=[NumberRange(min=0, max=10)], default=0
    )
    rubrics6 = IntegerField(
        "CO rubrics6", validators=[NumberRange(min=0, max=10)], default=0
    )

    rubrics1m = IntegerField(
        "Marks rubrics1", validators=[NumberRange(min=0)], default=0
    )
    rubrics2m = IntegerField(
        "Marks rubrics2", validators=[NumberRange(min=0)], default=0
    )
    rubrics3m = IntegerField(
        "Marks rubrics3", validators=[NumberRange(min=0)], default=0
    )
    rubrics4m = IntegerField(
        "Marks rubrics4", validators=[NumberRange(min=0)], default=0
    )
    rubrics5m = IntegerField(
        "Marks rubrics5", validators=[NumberRange(min=0)], default=0
    )
    rubrics6m = IntegerField(
        "Marks rubrics6", validators=[NumberRange(min=0)], default=0
    )


class all_phases(FlaskForm):
    all = FieldList(FormField(single_phase), min_entries=1, max_entries=5)
    submit = SubmitField("Submit Assignment mapping")


class uploadassign(FlaskForm):

    file = FileField(
        "Upload Assignment Marks", validators=[FileRequired()]
    )  # , FileAllowed('csv', 'Please Upload only csv files!')


class uploadstudent(FlaskForm):
    file = FileField(
        "Upload Student CSV", validators=[FileRequired()]
    )  # , FileAllowed('csv', 'Please Upload only csv files!')


class main_stid_cc(FlaskForm):

    coursecode = StringField(
        "Course Code", validators=[DataRequired(), Length(min=2, max=30)]
    )
    submit = SubmitField("Submit")


class small_crsend(Form):
    exc = IntegerField(
        "Excellent",
        validators=[NumberRange(min=0), Optional(strip_whitespace=True)],
    )
    vg = IntegerField(
        "Very good",
        validators=[NumberRange(min=0), Optional(strip_whitespace=True)],
    )
    g = IntegerField(
        "Good", validators=[NumberRange(min=0), Optional(strip_whitespace=True)]
    )
    sat = IntegerField(
        "Satisfactory",
        validators=[NumberRange(min=0), Optional(strip_whitespace=True)],
    )
    poor = IntegerField(
        "poor", validators=[NumberRange(min=0), Optional(strip_whitespace=True)]
    )
    co = IntegerField(
        "CO Mapped",
        validators=[NumberRange(min=0), Optional(strip_whitespace=True)],
    )


class large_crsend(FlaskForm):
    alltogether = FieldList(FormField(small_crsend), min_entries=15)
    submit = SubmitField("Submit Course End Survey")


class labfile_upload(FlaskForm):
    file = FileField(
        "Upload LAB Marks", validators=[FileRequired()]
    )  # , FileAllowed('csv', 'Please Upload only csv files!')


class small_talk(Form):
    one_q = StringField(
        "One Question",
        validators=[NumberRange(min=1, max=10), Optional(strip_whitespace=True)],
    )
    co = IntegerField(
        "CO Mapped",
        validators=[NumberRange(min=1, max=10), Optional(strip_whitespace=True)],
    )


class large_talk(FlaskForm):
    all_q = FieldList(FormField(small_talk), min_entries=1)
    submit = SubmitField("Submit Extra activities")

class po_form_upload(FlaskForm):
    file = FileField(
        "Upload PO Mapping", validators=[FileRequired()]
    ) 
    year = IntegerField(
        "Year",
        validators=[NumberRange(min=2010, max=2500)],
    )
    submit = SubmitField("Submit PO")

class staffid_coursecode(FlaskForm):
    file = FileField("Upload Staff ID Course Code Mapping", validators=[FileRequired()])
    submit = SubmitField("Submit Mapping")

class staffid_add(FlaskForm):
    file = FileField("Upload Staff ID", validators=[FileRequired()])
    submit = SubmitField("Submit Mapping")
    
class add_grade_mapping(FlaskForm):
    scheme_year = IntegerField(
        "Year", validators=[DataRequired(), NumberRange(min=2015, max=2030)]
    )
    file = FileField("Upload Marks-Grade Mapping", validators=[FileRequired()])
    submit = SubmitField("Submit Mapping")#
    
    
    
    
    





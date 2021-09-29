from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from apps import App


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        app_object = App()
        mongo = app_object.mongo

        temp = mongo.db.ath.find_one({'email': email.data}, {'email', 'pwd'})
        if temp:
            raise ValidationError('Email already exists!')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    type = SelectField(
        'Login Type', choices=[
            ('Manager', "Manager"), ("Applicant", "Applicant")])
    submit = SubmitField('Login')


class PostingForm(FlaskForm):
    """name = StringField('Your Name: ',
                           validators=[DataRequired(), Length(min=2, max=20)])
    """
    designation = StringField(
        'Job Designation: ', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    job_title = StringField('Job Title: ',
                            validators=[DataRequired()])
    job_location = StringField('Job Location: ',
                               validators=[DataRequired()])
    job_description = StringField('Job Description: ',
                                  validators=[DataRequired()])
    skills = StringField('Skills Required: ',
                         validators=[DataRequired()])
    schedule = StringField('Schedule of the job (in hours): ',
                           validators=[DataRequired()])
    salary = StringField('Salary: ',
                         validators=[DataRequired(), Length(min=2, max=20)])
    rewards = StringField('Rewards / Benefits: ',
                          validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('POST')


class ApplyForm(FlaskForm):
    apply_name = StringField(
        'Name: ', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    apply_phone = StringField(
        'Phone Number: ', validators=[
            DataRequired(), Length(
                min=2, max=20)])
    apply_address = StringField('Address: ',
                                validators=[DataRequired()])
    dob = StringField('Date of Birth: ',
                      validators=[DataRequired(), Length(min=2, max=20)])
    """position = StringField('Job Position applying for: ',
                           validators=[DataRequired(), Length(min=2, max=100)])
    """
    skills = StringField('Your Skills: ',
                         validators=[DataRequired()])
    availability = StringField('Availability (hours per day in a week): ',
                               validators=[DataRequired()])
    """resume = StringField('Upload Resume: *****',
                           validators=[DataRequired(), Length(min=2, max=50)])
    """
    signature = StringField('Signature (Full Name): ',
                            validators=[DataRequired(), Length(min=2, max=20)])
    schedule = StringField('Schedule: ',
                           validators=[DataRequired()])
    submit = SubmitField('APPLY')


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[
            DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset')

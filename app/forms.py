from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from app.models import *


class CreateUserForm(FlaskForm):

    fullname = StringField('<i class="fa fa-user-circle"></i> Fullname', validators=[
                           DataRequired(message='Fulname is required')])
    employee_id = StringField('<i class="fa fa-id-card"></i> Employee ID', validators=[
                              DataRequired(message='Please enter Employee ID')])
    email = StringField('<i class="fa fa-envelope"></i> Email', validators=[
                        DataRequired(), Email(message='Enter a Valid Email')])
    health_facility = SelectField(
        '<i class="fa fa-hospital-alt"></i> Health Facility', choices=[], coerce=int)
    submit = SubmitField("Save")

    #validation
    def validate_employee_id(self, employee_id):
        user = User.query.filter_by(employee_id=employee_id.data).first()
        if user:
            raise ValidationError("A user account with that Employee ID already exists!")
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("A user account with that Email already exists!")    
        


class AccountForm(FlaskForm):

    fullname = StringField('<i class="fa fa-user-circle"></i> Fullname', validators=[
                           DataRequired(message='Fulname is required')])
    email = StringField('<i class="fa fa-envelope"></i> Email', validators=[
                        DataRequired(), Email(message='Enter a Valid Email')])
    old_password = PasswordField('<i class="fa fa-lock"></i> Old Password', validators=[
        DataRequired(), Length(min=6, message='Password must be atleast 6 characters long')])
    new_password = PasswordField('<i class="fa fa-lock"></i>  New Password', validators=[
        DataRequired(), Length(min=6, message='Password must be atleast 6 characters long')])
    confirm = PasswordField('<i class="fa fa-lock"></i> Confirm Password', validators=[
        DataRequired(), EqualTo('new_password', message='Passwords not matching')])
    submit = SubmitField("Save")


class LoginForm(FlaskForm):

    email = StringField('<i class="fa fa-envelope"></i>  Email', validators=[
                        DataRequired(), Email(message='Enter a Valid Email')])
    password = PasswordField('<i class="fa fa-key"></i>  Password', validators=[
        DataRequired(), Length(min=6, message='Password must be atleast 6 characters long')])
    submit = SubmitField("Login")


class AddReasonForm(FlaskForm):

    title = StringField('<i class="fa fa-info"></i> Reason', validators=[
        DataRequired(message='Enter a valid Reason')])
    submit = SubmitField("Save")
#validation
def validate_title(self, title):
        reason = Reason.query.filter_by(title=title.data).first()
        if reason:
            raise ValidationError("That referral reason already exists!") 


class AddSubCountyForm(FlaskForm):

    sub_county_name = StringField('<i class="fa fa-globe-europe"></i> Name of Sub-County', validators=[
        DataRequired(message='Enter a valid SubCounty name')])
    submit = SubmitField("Save")

    #validation
    def validate_sub_county_name(self, sub_county_name):
        subcounty = Sub_county.query.filter_by(county_name=sub_county_name.data).first()
        if subcounty:
            raise ValidationError("That Sub County already exists!") 


class AddHealthFacilityForm(FlaskForm):

    mfl_code = StringField('<i class="fa fa-code"></i>  MFL Code', validators=[
        DataRequired(message='Enter a valid MFLCode')])
    name = StringField('<i class="fa fa-hospital-alt"></i> Name of Facility', validators=[
        DataRequired(message='Enter a valid name')])
    phone = StringField('<i class="fa fa-phone"></i> Facility Telephone', validators=[
        DataRequired(message='Enter a valid phone number')])
    sub_county = SelectField(
        '<i class="fa fa-globe-europe"></i> Sub-County', choices=[], coerce=int)
    submit = SubmitField("Save")

    #validation
    def validate_mfl_code(self, mfl_code):
        facility = Health_facility.query.filter_by(
            mfl_code=mfl_code.data).first()
        if facility:
            raise ValidationError("Hospital with that MFL Code already exists!")


class MedicForm(FlaskForm):

    fullname = StringField('<i class="fa fa-user-circle"></i> Fullname', validators=[
                           DataRequired(message='Fulname is required')])
    mpdb_number = StringField('<i class="fa fa-id-card"></i> MPDB Number',
                              validators=[DataRequired(message='MPDB Number is required')])
    designation = SelectField('<i class="fa fa-user-nurse"></i> Designation',
                              choices=[('Doctor', 'Doctor'), ('Nurse', 'Nurse')], coerce=str)
    health_facility = SelectField(
        '<i class="fa fa-hospital-alt"></i> Health Facility', choices=[], coerce=int)
    submit = SubmitField("Save")

    def validate_mpdb_number(self, mpdb_number):
        medic = Medic.query.filter_by(
            mpdb_number=mpdb_number.data).first()
        if medic:
            raise ValidationError("A Medic  with that MPDB Number already exists!")


class PatientForm(FlaskForm):

    fullname = StringField('<i class="fa fa-user-circle"></i> Fullname', validators=[
                           DataRequired(message='Fulname is required')])
    huduma_number = StringField('<i class="fa fa-id-card"></i> Huduma Number',
                              validators=[DataRequired(message='Huduma Number is required')])
    submit = SubmitField("Save")

    def validate_huduma_number(self, huduma_number):
        patient = Patient.query.filter_by(
            huduma_id=huduma_number.data).first()
        if patient:
            raise ValidationError("A Patient  with that Huduma Number already exists!")

class ReferralForm(FlaskForm):

    ref_id = StringField('<i class="fa fa-user-circle"></i> Referral Number', validators=[
        DataRequired(message='Field is required')])
    patient = StringField('<i class="fa fa-id-card"></i> Patient Huduma No.',
                          validators=[DataRequired(message='Huduma Number is required')])
    ref_from = SelectField(
        '<i class="fa fa-hospital"></i> From', choices=[], coerce=int)
    ref_to = SelectField('<i class="fa fa-hospital-alt"></i> To',
                         choices=[], coerce=int)
    ref_reason = SelectField('<i class="fa fa-wheelchair"></i> Referral Reason',
                             choices=[], coerce=int)
    ref_notes = TextAreaField('<i class="fa fa-book"></i> Referral Notes',
                              validators=[DataRequired(message='Give a brief description about the reason for referal')])
    ref_medic = SelectField(
        '<i class="fa fa-user-nurse"></i> Medic in Charge', choices=[], coerce=int)
    submit = SubmitField("Save")

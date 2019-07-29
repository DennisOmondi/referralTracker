from app import db,login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    employee_id = db.Column(db.String(12), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False,default=False)
    password = db.Column(db.String(120), nullable=False)
    health_facility = db.Column(db.Integer, db.ForeignKey(
        'health_facility.id'), nullable=False)
    referrals = db.relationship('Referral', backref='referring_user', lazy=True)

    def __repr__(self):
        return f"User(name={self.fullname},email={self.email,},employeeID={self.employee_id})"


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    huduma_id = db.Column(db.String(12), unique=True, nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    referrals = db.relationship('Referral', backref='referred_patient', lazy=True)

    def __repr__(self):
        return f"Patient(name={self.fullname},hudumaID={self.huduma_id})"


class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referral_id = db.Column(db.String(50), unique=True, nullable=False)
    referral_from_id = db.Column(db.Integer, db.ForeignKey(
                                'health_facility.id'), nullable=False)
    referral_to_id = db.Column(db.Integer, db.ForeignKey(
                            'health_facility.id'), nullable=False)
    
    from_ = db.relationship(
        'Health_facility', foreign_keys='Referral.referral_from_id')  
    to_ = db.relationship(
        'Health_facility', foreign_keys='Referral.referral_to_id')
                               
    patient = db.Column(db.Integer, db.ForeignKey(
                        'patient.id'), nullable=False)
    referral_datetime = db.Column(db.DateTime(), nullable=False,
                                  default=datetime.now)
    notes = db.Column(db.Text,nullable=False)
    reason=db.Column(db.Integer,db.ForeignKey('reason.id'),nullable=False)
    user = db.Column(db.Integer, db.ForeignKey(
                     'user.id'), nullable=False)
    medic = db.Column(db.Integer, db.ForeignKey(
                      'medic.id'), nullable=False)

    def __repr__(self):
        return f"Referral(From={self.referral_from_id},To={self.referral_to_id,},date={self.referral_datetime})"

class Reason(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    referrals = db.relationship(
        'Referral', backref='reasons', lazy=True)
    def __repr__(self):
      return f"Reason({self.title})"


class Sub_county(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    county_name = db.Column(db.String(120), nullable=False)
    health_facilities = db.relationship(
        'Health_facility', backref='facility_subcounty', lazy=True)

    def __repr__(self):
      return f"Subcounty(Name={self.county_name})"


class Health_facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mfl_code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    subcounty = db.Column(db.String(120), db.ForeignKey('sub_county.id') ,nullable=False)
    referrals = db.relationship(
        'Referral',primaryjoin='or_(Health_facility.id == Referral.referral_from_id,Health_facility.id == Referral.referral_to_id)', backref='referral_facility', lazy=True)
    users = db.relationship(
        'User', backref='user_facility', lazy=True)
    medics = db.relationship(
        'Medic', backref='medic_facility', lazy=True)

    def __repr__(self):
        return f"Hospital(name={self.name},MLF_Code={self.mfl_code})"


class Medic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    mpdb_number = db.Column(db.String(12), unique=True, nullable=False)
    designation = db.Column(db.String(120), nullable=False)
    health_facility = db.Column(db.Integer, db.ForeignKey(
        'health_facility.id'), nullable=False)
    referrals = db.relationship('Referral', backref='referred_medic', lazy=True)

    def __repr__(self):
       return f"Medic(name={self.fullname},MPDB={self.mpdb_number},designation={self.designation})"

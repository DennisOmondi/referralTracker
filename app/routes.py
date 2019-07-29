from __future__ import print_function
from flask import render_template, request, url_for, flash, redirect,session
from app import app, db, bcrypt, login_manager
from flask_login import login_user, current_user,login_required,logout_user
from app.models import *
from app.forms import *
import datetime as dt

import africastalking
from app.sms import SMS
sms=SMS()

@app.errorhandler(404)
def page_note_found(e):
    return render_template('error404.html')

@app.route('/create_user', methods=["GET", "POST"])
@login_required
def create_user():
    form = CreateUserForm()
    facilities = Health_facility.query.all()
    categories = [(f.id, f.name) for f in facilities]
    form.health_facility.choices = categories
    if request.method == "POST" and form.validate_on_submit():
        # return str(form.health_facility.data)
        # user = User(fullname=form.data.fullname, email=form.data.email, employee_id=form.data.employee_id,
        #            is_admin=0, health_facility=form.data.health_facility, password=sha256_crypt.encrypt(form.data.password),)
        user = User()
        user.fullname = form.fullname.data
        user.email = form.email.data
        user.employee_id = form.employee_id.data
        user.is_admin = False
        user.health_facility = form.health_facility.data
        user.password = bcrypt.generate_password_hash('123456').decode('utf-8')

        db.session.add(user)
        db.session.commit()
        flash('User Created Successfully', 'success')
        return redirect(url_for('users'))
    return render_template("create_user.html", form=form)


@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    error = ''
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=6)
    user_menu = 'active'
    if request.method == 'POST':
        searchq = request.form['searchq']
        userq = User.query.filter_by(
            employee_id=searchq).paginate(page=page, per_page=6)
        userqcount = User.query.filter_by(employee_id=searchq).first()
        if userqcount:
            return render_template('users.html', users=userq, error=error, user_menu=user_menu)
        else:
            error = f'No Record found for Search "{searchq}"'
            return render_template('users.html', users=userq, error=error, user_menu=user_menu)

    return render_template('users.html', users=users, error=error, user_menu=user_menu)

@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
    form = AccountForm()
    form.fullname.data = current_user.fullname
    form.email.data=current_user.email
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.get(current_user.id)
        if user and bcrypt.check_password_hash(current_user.password, form.old_password.data):
            user.password = bcrypt.generate_password_hash(
            form.new_password.data).decode('utf-8')

            db.session.commit()
            flash('Credentials changed Successfully', 'success')
            return redirect(url_for('account'))
        else:
            flash('Failed! Credentials not matching', 'danger')
            return redirect(url_for('account'))
    return render_template("account.html", form=form)

@app.route('/user_detail')
@login_required
def user_detail():
    user_id=request.args.get('user_id')
    user = User.query.get(user_id)
    return render_template('user_detail.html',user=user)


@app.route('/change_role')
@login_required
def change_role():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if user.is_admin:
        user.is_admin = False
    else:
        user.is_admin = True
    db.session.commit()
    flash(f'User role for {user.email} changed succesfully ', 'info')
    return redirect(url_for('user_detail',user_id=user_id))      


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_panel'))
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():

        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=False)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else  redirect(url_for('admin_panel'))
        else:
            flash('Login Failed!', 'danger')

    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/new_reason', methods=["GET", "POST"])
@login_required
def new_reason():
    form = AddReasonForm()
    if request.method == "POST" and form.validate_on_submit():
        # return str(form.health_facility.data)
        # user = User(fullname=form.data.fullname, email=form.data.email, employee_id=form.data.employee_id,
        #            is_admin=0, health_facility=form.data.health_facility, password=sha256_crypt.encrypt(form.data.password),)
        reason = Reason()
        reason.title = form.title.data

        db.session.add(reason)
        db.session.commit()
        flash('Referral reason added Successfully', 'success')
        return redirect(url_for('new_reason'))
    return render_template('add_reason.html', form=form)


@app.route('/new_sub_county', methods=["GET", "POST"])
@login_required
def new_sub_county():
    form = AddSubCountyForm()
    if request.method == "POST" and form.validate_on_submit():

        sub_county = Sub_county()
        sub_county.county_name = form.sub_county_name.data

        db.session.add(sub_county)
        db.session.commit()
        flash('Sub-County added Successfully', 'success')
        return redirect(url_for('new_sub_county'))
    return render_template('add_sub_county.html', form=form)


@app.route('/new_health_facility', methods=["GET", "POST"])
@login_required
def new_health_facility():
    form = AddHealthFacilityForm()
    sub_counties = Sub_county.query.all()
    categories = [(s.id, s.county_name) for s in sub_counties]
    form.sub_county.choices = categories
    if request.method == "POST" and form.validate_on_submit():

        health_facility = Health_facility()

        health_facility.name = form.name.data
        health_facility.mfl_code = form.mfl_code.data
        health_facility.phone = form.phone.data
        health_facility.subcounty = form.sub_county.data

        db.session.add(health_facility)
        db.session.commit()
        flash('Health Facility added Successfully', 'success')
        return redirect(url_for('new_health_facility'))
    return render_template('add_health_facility.html', form=form)


@app.route('/new_patient', methods=["GET", "POST"])
@login_required
def new_patient():
    form = PatientForm()
    if request.method == "POST" and form.validate_on_submit():

        patient = Patient()

        patient.fullname = form.fullname.data
        patient.huduma_id = form.huduma_number.data

        db.session.add(patient)
        db.session.commit()
        session.pop('huduma_number')
        flash('Patient saved Successfully', 'success')
        return redirect(url_for('new_patient'))
    return render_template('new_patient.html', form=form)


@app.route('/new_medic', methods=["GET", "POST"])
@login_required
def new_medic():
    form = MedicForm()
    facilities = Health_facility.query.all()
    categories = [(f.id, f.name) for f in facilities]
    form.health_facility.choices = categories
    if request.method == "POST" and form.validate_on_submit():

        medic = Medic()

        medic.fullname = form.fullname.data
        medic.mpdb_number = form.mpdb_number.data
        medic.designation = form.designation.data
        medic.health_facility = form.health_facility.data

        db.session.add(medic)
        db.session.commit()
        flash('Medic saved Successfully', 'success')
        return redirect(url_for('new_medic'))
    return render_template('add_medic.html', form=form)

@app.route('/')
@app.route('/admin_panel')
@login_required
def admin_panel():
    patients = len(Patient.query.all())
    referrals = len(Referral.query.all())
    sub_counties = len(Sub_county.query.all())
    medics = len(Medic.query.all())
    health_facilities = len(Health_facility.query.all())
    stats={'patients':patients,'referrals':referrals,'sub_counties':sub_counties,'medics':medics,'health_facilities':health_facilities}
    return render_template('admin_panel.html',stats=stats)


@app.route('/sub_counties')
@login_required
def sub_counties():
    sub_counties = Sub_county.query.all()
    subcounty_menu = 'active'
    return render_template('sub_counties.html', sub_counties=sub_counties, subcounty_menu=subcounty_menu)


@app.route('/health_facilities')
@login_required
def health_facilities():
    health_facilities = Health_facility.query.all()
    facility_menu = 'active'
    return render_template('facilities.html', health_facilities=health_facilities, facility_menu=facility_menu)


@app.route('/new_referral', methods=['GET', 'POST'])
@login_required
def new_referral():
    form = ReferralForm()
    patient_form=PatientForm()
    reff_id = None
    last_ref = Referral.query.order_by(Referral.id.desc()).first().id
    if last_ref:
        ref = last_ref+1
        reff_id = 'RF' + "%04d" % ref
    else:
        reff_id = 'RF0001'

    facilities = Health_facility.query.filter(
        Health_facility.id != current_user.user_facility.id)
    categories = [(f.id, f.name) for f in facilities]

    reasons = Reason.query.all()
    r_categories = [(r.id, r.title) for r in reasons]

    medics = Medic.query.filter_by(
        health_facility=current_user.user_facility.id).all()
    m_categories = [(m.id, m.fullname) for m in medics]

    form.ref_medic.choices = m_categories
    form.ref_to.choices = categories
    form.ref_reason.choices = r_categories
    form.ref_id.data = reff_id
    form.ref_from.choices = [
        (current_user.user_facility.id, current_user.user_facility.name)]
    #categories = [(f.id, f.name) for f in facilities]

    if request.method == "POST" and form.validate_on_submit():
        referral = Referral()
        # check if patient exists
        patient = Patient.query.filter_by(huduma_id=form.patient.data).first()
        last_id = Patient.query.order_by(Patient.id.desc()).first().id
        currentId = last_id + 1
        
        referral.referral_id = form.ref_id.data
        #referral.patient = patient.id or currentId
        referral.referral_from_id = form.ref_from.data
        referral.referral_to_id = form.ref_to.data
        #referral.referral_datetime = form.ref_id.data
        referral.notes = form.ref_notes.data
        referral.reason = form.ref_reason.data
        referral.user = current_user.id
        referral.medic = form.ref_medic.data
        #get phone number
        recipients=[]
        phone = '+254' + str(Health_facility.query.get(form.ref_to.data).phone)
        frm=current_user.user_facility.name
        reason=Reason.query.get(form.ref_reason.data).title
        msg = f"Referral-{form.ref_id.data} from {frm} has been dispatched to your facility\nReason for referral:{reason}"
        recipients.append(phone)
        if patient:
            referral.patient = patient.id
            db.session.add(referral)
            db.session.commit()
            sms.send(msg,recipients)
            flash('Referral process initiated Successfully', 'success')
            return redirect(url_for('new_referral'))
        else:
            referral.patient = currentId
            db.session.add(referral)
            db.session.commit()
            sms.send(msg, recipients)
            session['huduma_number']= form.patient.data
            flash('The Patient being referred doesnt exist in the Database,add him/her to complete the Process.', 'warning')
            return redirect(url_for('new_patient'))
    # else:
    #    return "An error Occurred"
    return render_template('new_referral.html', form=form)


@app.route('/referrals', methods=['GET', 'POST'])
@login_required
def referrals():
    error = ''
    yr=dt.datetime.now().year
    m = dt.datetime.now().month
    d = dt.datetime.now().day
    
    year = dt.datetime.strptime(
        f'{yr}/1/1  00:00:00 00000', '%Y/%m/%d %H:%M:%S %f')
    month = dt.datetime.strptime(
        f'{yr}/{m}/1  00:00:00 00000', '%Y/%m/%d %H:%M:%S %f')
    day = dt.datetime.strptime(
        f'{yr}/{m}/{d}  00:00:00 00000', '%Y/%m/%d %H:%M:%S %f')

    page = request.args.get('page', 1, type=int)
    referrals = Referral.query.order_by(
    Referral.referral_datetime.desc()).paginate(page=page, per_page=10)
    referral_menu = 'active'
    if request.method == 'POST':
        searchq = request.form['searchq']
        if searchq == 'year' or searchq == 'month' or searchq == 'today':
            #error = f'No Record found for Search "{searchq}"'
            if searchq == 'year':
                referrals = Referral.query.filter(
                    Referral.referral_datetime >= year).paginate(page=page, per_page=6)
                if not referrals.items :
                        error="No Referrals made in the current year"
            elif searchq == 'month':
                referrals = Referral.query.filter(
                    Referral.referral_datetime >= month).paginate(page=page, per_page=6)
                if not referrals.items:
                        error="No Referrals made in the current month"
            else:
                referrals = Referral.query.filter(
                    Referral.referral_datetime >= day).paginate(page=page, per_page=6)
                if not referrals.items:
                        error="No Referrals made today"
            return render_template('referrals.html', referrals=referrals, error=error, referral_menu=referral_menu)
        else:    
            refq = Referral.query.filter_by(referral_id=searchq).first()
            if refq:
                return redirect(f'/referral_detail/{refq.referral_id}')
            else:
                error = f'No Record found for Search "{searchq}"'
                referrals = Referral.query.filter_by(
                    referral_id=searchq).paginate(page=page, per_page=6)
                return render_template('referrals.html', referrals=referrals, error=error, referral_menu=referral_menu)
    
    return render_template('referrals.html', referrals=referrals,error=error ,referral_menu=referral_menu)
    

#facilities for each subcounty
@app.route('/subcounty/<subcounty>')
@login_required
def subcounty_health_facilities(subcounty):
    all_subs=Sub_county.query.all()
    sub_county=Sub_county.query.filter_by(county_name=subcounty).first()
    health_facilities = sub_county.health_facilities
    active_sub = subcounty
    return render_template('subcounty.html', health_facilities=health_facilities,
                        subcounty=subcounty,all_subs=all_subs,active_sub=active_sub)


#referrals foreach facility
@app.route('/facility/<mfl_code>')
def facility(mfl_code):
    all_facility = Health_facility.query.all()
    facility = Health_facility.query.filter_by(mfl_code=mfl_code).first()
    referrals = facility.referrals
    active_facility = facility.mfl_code
    return render_template('facility.html', referrals=referrals,
                           facility=facility, all_facility=all_facility, active_facility=active_facility)


#refferal detail
@app.route('/referral_detail/<referral_id>')
@login_required
def referral_detail(referral_id):
    referral = Referral.query.filter_by(referral_id=referral_id).first()
    patient = Patient.query.get(referral.patient)
    return render_template('referral_detail.html',referral=referral,patient=patient)


#medics
@app.route('/medics', methods=['GET', 'POST'])
@login_required
def medics():
    error = ''
    page = request.args.get('page', 1, type=int)
    medics = Medic.query.paginate(page=page, per_page=6)
    medic_menu = 'active'
    if request.method == 'POST':
        searchq = request.form['searchq']
        medq = Medic.query.filter_by(
            mpdb_number=searchq).paginate(page=page, per_page=6)
        medqcount = Medic.query.filter_by(mpdb_number=searchq).first()
        if medqcount:
            return render_template('medics.html', medics=medq, error=error, medic_menu=medic_menu)
        else:
            error = f'No Record found for Search "{searchq}"'
            return render_template('medics.html', medics=medq, error=error, medic_menu=medic_menu)

    return render_template('medics.html', medics=medics, error=error, medic_menu=medic_menu)

#analytics
@app.route('/analytics', methods=['GET', 'POST'])
@login_required
def analytics():
    analytics_menu = 'active'
    #incoming
    queryIn = 'SELECT count(referral.referral_to_id) AS "incoming", referral.referral_to_id AS referral_to_id, health_facility.name AS facility  FROM referral INNER JOIN health_facility ON referral.referral_to_id=health_facility.id GROUP BY referral.referral_to_id'
    incomings = db.session.execute(queryIn)
    
    queryOut = 'SELECT count(referral.referral_from_id) AS "outgoing", referral.referral_from_id AS referral_from_id, health_facility.name AS facility  FROM referral INNER JOIN health_facility ON referral.referral_from_id=health_facility.id GROUP BY referral.referral_from_id'
    outgoings = db.session.execute(queryOut)

    queryReason = 'SELECT count(referral.reason) AS "reason", referral.reason AS reason_, reason.title AS title  FROM referral INNER JOIN reason ON referral.reason=reason.id GROUP BY referral.reason'
    reasons = db.session.execute(queryReason)

    return render_template('analytics.html',analytics_menu=analytics_menu,incomings=incomings,outgoings=outgoings,reasons=reasons)

#visualizatio
@app.route('/analytics_visual', methods=['GET', 'POST'])
@login_required
def analytics_visual():
    analytics_menu = 'active'
    #reason
    queryReason = 'SELECT count(referral.reason) AS "reason", referral.reason AS reason_, reason.title AS title  FROM referral INNER JOIN reason ON referral.reason=reason.id GROUP BY referral.reason'
    reasons = db.session.execute(queryReason)
    reasons_ = list((l.title, l.reason) for l in reasons)
    title = list(t[0] for t in reasons_)
    count = list(c[1] for c in reasons_)
    
    #incoming
    queryIn = 'SELECT count(referral.referral_to_id) AS "incoming", referral.referral_to_id AS referral_to_id, health_facility.name AS facility  FROM referral INNER JOIN health_facility ON referral.referral_to_id=health_facility.id GROUP BY referral.referral_to_id'
    incomings = db.session.execute(queryIn)
    incomings_ = list((l.facility, l.incoming) for l in incomings)
    facilityIns = list(t[0] for t in incomings_)
    countIns = list(c[1] for c in incomings_)

    #outgoings'''
    queryOut = 'SELECT count(referral.referral_from_id) AS "outgoing", referral.referral_from_id AS referral_from_id, health_facility.name AS facility  FROM referral INNER JOIN health_facility ON referral.referral_from_id=health_facility.id GROUP BY referral.referral_from_id'
    outgoings = db.session.execute(queryOut)
    outgoings_ = list((l.facility, l.outgoing) for l in outgoings)
    facilityOuts = list(t[0] for t in outgoings_)
    countOuts = list(c[1] for c in outgoings_)

    #months
    months = 12
    yr = dt.datetime.now().year
    m = 1
    
    monthly_refs = []
    for x in range(months):
        month = dt.datetime.strptime(
            f'{yr}/{m}/1  00:00:00 00000', '%Y/%m/%d %H:%M:%S %f')
        if m < 12:    
            next_month = dt.datetime.strptime(
            f'{yr}/{int(m+1)}/1  00:00:00 00000', '%Y/%m/%d %H:%M:%S %f')
        else:
            next_month = dt.datetime.strptime(
                f'{yr+1}/{1}/1  00:00:00 00000', '%Y/%m/%d %H:%M:%S %f')
        m_ref = Referral.query.filter(
            Referral.referral_datetime >= month, Referral.referral_datetime < next_month).count()
        monthly_refs.append(m_ref)
        m=m+1   

    return render_template('analytics_visual.html', reasons_count=count, reasons_title=title,
                            incomings_facility=facilityIns, incomings_counts=countIns,
                            outgoings_facility=facilityOuts, outgoings_counts=countOuts,
                            analytics_menu =analytics_menu,monthly_refs=monthly_refs
                            )

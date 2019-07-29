from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import africastalking
app = Flask(__name__)

app.secret_key = '9e676ab339736239383bce71c5f19cef5ada05efba771ccc30638176f83ec76a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///referrals_tracker.db'
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category='info'
from app import models


from app import routes

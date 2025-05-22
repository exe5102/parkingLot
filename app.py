from flask import Flask, request, url_for, redirect, session, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv
from typing import Dict, Optional, Union
import logging
from logging.handlers import RotatingFileHandler

# 載入環境變數
load_dotenv()

# 初始化 Flask 應用
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'Final-Projuct')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

# 安全性設定
csrf = CSRFProtect(app)
talisman = Talisman(app,
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' 'unsafe-eval'",
        'style-src': "'self' 'unsafe-inline'",
    }
)

# 速率限制
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# 資料庫設定
db = SQLAlchemy(app)

# 登入管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# 日誌設定
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/parking.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Parking system startup')

# 時區設定
TZ_OFFSET = timezone(timedelta(hours=8))
today = datetime.now(tz=TZ_OFFSET)
dtoday = datetime.strptime(today.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

# 資料模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    state = db.Column(db.String(1), default='0')
    current_booking = db.relationship('Booking', backref='spot', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(10), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    number = db.Column(db.String(15), unique=True, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    state = db.Column(db.String(1), default='1')

# Blueprint 註冊
from routes.auth import auth_bp
from routes.customer import customer_bp
from routes.admin import admin_bp

app.register_blueprint(auth_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')

# 錯誤處理
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# 初始化資料庫
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

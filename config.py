import os
from datetime import timedelta

class Config:
    """基本配置"""
    # Flask 配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'Final-Projuct')
    TEMPLATES_AUTO_RELOAD = True

    # 資料庫配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///booking.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 安全性配置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

    # 日誌配置
    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # 停車場配置
    PARKING_RATE = float(os.getenv('PARKING_RATE', '30'))  # 每小時收費
    MAX_BOOKING_HOURS = int(os.getenv('MAX_BOOKING_HOURS', '24'))

    # 安全性標頭
    SECURITY_HEADERS = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'SAMEORIGIN',
        'X-XSS-Protection': '1; mode=block',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';"
    }

class DevelopmentConfig(Config):
    """開發環境配置"""
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    TEMPLATES_AUTO_RELOAD = True

class ProductionConfig(Config):
    """生產環境配置"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    TEMPLATES_AUTO_RELOAD = False

class TestingConfig(Config):
    """測試環境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# 獲取當前環境配置
def get_config():
    """根據環境變數獲取配置"""
    env = os.getenv('FLASK_ENV', 'default')
    return config.get(env, config['default'])
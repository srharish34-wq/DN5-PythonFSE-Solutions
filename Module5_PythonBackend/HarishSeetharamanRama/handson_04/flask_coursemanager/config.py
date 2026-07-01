# ============================================================
# Hands-On 4 – Flask Configuration
# flask_coursemanager/config.py
# Cognizant DN5.0 | Harish Seetharaman Rama
# ============================================================

import os

class Config:
    SECRET_KEY                = os.environ.get('SECRET_KEY', 'flask-coursemanager-secret-2024')
    SQLALCHEMY_DATABASE_URI   = os.environ.get('DATABASE_URL', 'sqlite:///coursemanager.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG                     = True

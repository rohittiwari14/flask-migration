

class Config:
    debug = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///mydatabase.db'
    SQLALCHEMY_TRACK_MODIFICATION_ = False
    SECRET_KEY = "rohittiwari"
    EMAIL_REGEX = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    PHONE_REGEX = r"^\d{10}$"
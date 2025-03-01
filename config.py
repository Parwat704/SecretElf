class Config:
    SECRET_KEY = "your-secret-key"
    DEBUG = True

    # Flask-Mail settings
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "parwat.ilam@gmail.com"
    MAIL_PASSWORD = "freakyworld725"
    
    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///secret_elf.db'  # SQLite database file
    SQLALCHEMY_TRACK_MODIFICATIONS = False

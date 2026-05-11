class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password123@localhost/task_manager_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secretkey'
from flask_philo_sqlalchemy.connection import initialize

def init_db(app):
    initialize(app)

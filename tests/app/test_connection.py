from flask_philo_core.test import FlaskPhiloTestCase, BaseTestFactory
from flask_philo_sqlalchemy.connection import create_pool

class TestDBAccess(FlaskPhiloTestCase):
    def test_postgresql_connection(self):
        """
        checks if connection is open
        """
        config = {}
        # Creates a Flask-Philo_Core with no postgresql config
        config['FLASK_PHILO_EXTENSIONS'] = ('Flask-Philo-SQLAlchemy', )
        config['Flask-Philo-SQLAlchemy'] = {
            'DEFAULT': 'postgresql://ds:dsps@pgdb:5432/ds_test',
        }

        app = BaseTestFactory.create_test_app(config=config)
        with app.app_context():
            pool = create_pool()
            result = pool.connections['DEFAULT'].session.execute('SELECT 19;')
            assert result.fetchone()[0] == 19
            pool.connections['DEFAULT'].session.close()

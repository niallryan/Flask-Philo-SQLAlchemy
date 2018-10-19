from flask_philo_core.test import FlaskPhiloTestCase, BaseTestFactory
#from flask_philo.db.postgresql.types import PasswordHash




class TestDBAccess(FlaskPhiloTestCase):
    def test_connection_open(self):
        """
        checks if connection is open
        """
        config = {}
        # Creates a Flask-Philo_Core with no postgresql config
        app = BaseTestFactory.create_test_app()
        assert app.plugins.flask_philo_sqlalchemy is None
        config['FLASK_PHILO_EXTENSIONS'] = ('Flask-Philo-SQLAlchemy', )
        config['Flask-Philo-SQLAlchemy'] = {
            'DEFAULT': 'postgresql://ds:dsps@pgdb:5432/ds_test',
            'DB2': 'postgresql://ds:dsps@pgdb:5432/ds2_test'
        }

        app = BaseTestFactory.create_test_app(config=config)
        result = app.plugins.flask_philo_sqlalchemy.connections['DEFAULT'].session.execute('SELECT 19;')
        assert result.fetchone()[0] == 19
        app.plugins.flask_philo_sqlalchemy.connections['DEFAULT'].session.close()


class TestPassword(FlaskPhiloTestCase):
    def test_password_equal(self):
        a = PasswordHash.new('123', 12)
        assert a == '123'
        assert a != '1232'

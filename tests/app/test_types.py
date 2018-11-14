from flask_philo_core.test import FlaskPhiloTestCase
from flask_philo_sqlalchemy.types import PasswordHash


class TestPassword(FlaskPhiloTestCase):
    def test_password_equal(self):
        a = PasswordHash.new('123', 12)
        assert a == '123'
        assert a != '1232'

from flask_philo_core.test import FlaskPhiloTestCase, BaseTestFactory
from flask_philo_sqlalchemy.orm import BaseModel
from flask_philo_sqlalchemy.connection import create_pool
from sqlalchemy import Column, String
from flask_philo_sqlalchemy import cleandb, syncdb


class Example(BaseModel):
    __tablename__ = 'example'
    name = Column(String(256))


config = {}
config['FLASK_PHILO_EXTENSIONS'] = ('Flask-Philo-SQLAlchemy', )
config['Flask-Philo-SQLAlchemy'] = {
    'DEFAULT': 'postgresql://ds:dsps@pgdb:5432/ds_test',
    'DB2': 'postgresql://ds:dsps@pgdb:5432/ds2_test'
}


class TestMultiDBModel(FlaskPhiloTestCase):
    def setup(self):
        self.app = BaseTestFactory.create_test_app(config=config)
        with self.app.app_context():
            self.pool = create_pool()
            syncdb(pool=self.pool)

    def test_muti_crud(self):
        with self.app.app_context():
            rock = Example(name='Rock')
            rock.add(connection_name='DEFAULT')
            self.pool.commit()

            assert 1 == Example.objects.count(connection_name='DEFAULT')
            assert 0 == Example.objects.count(connection_name='DB2')

            rock2 = Example(name='Rock2')
            rock2.add(connection_name='DB2')
            self.pool.commit()

            assert 1 == Example.objects.count(connection_name='DB2')

            r1 = Example.objects.get(connection_name='DB2', name='Rock')
            r2 = Example.objects.get(connection_name='DEFAULT', name='Rock2')

            assert r1.name != r2.name

            rock.delete()
            self.pool.commit()
            assert 0 == Example.objects.count(connection_name='DEFAULT')

            l1 = list(Example.objects.filter_by(connection_name='DEFAULT'))
            l2 = list(Example.objects.filter_by(connection_name='DB2'))

            assert 0 == len(l1)
            assert 1 == len(l2)

    def teardown(self):
        with self.app.app_context():
            cleandb()
            self.pool.close()

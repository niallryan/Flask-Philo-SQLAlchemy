from flask_philo_sqlalchemy.test import SQLAlchemyTestCase
from flask_philo_sqlalchemy.orm import BaseModel
from sqlalchemy import Column, String


class Example(BaseModel):
    __tablename__ = 'example'
    name = Column(String(256))


class TestMultiDBModel(SQLAlchemyTestCase):

    config = {
        'FLASK_PHILO_SQLALCHEMY': {
            'DEFAULT': 'postgresql://ds:dsps@pgdb:5432/ds_test',
            'DB2': 'postgresql://ds:dsps@pgdb:5432/ds2_test'
        }
    }

    def test_muti_crud(self):
        with self.app.app_context():
            rock = Example(name='Rock')
            rock.add(connection_name='DEFAULT')
            self.pool.commit(connection_name='DEFAULT')

            assert 1 == Example.objects.count(connection_name='DEFAULT')
            assert 0 == Example.objects.count(connection_name='DB2')

            rock2 = Example(name='Rock2')
            rock2.add(connection_name='DB2')
            self.pool.commit(connection_name='DB2')

            assert 1 == Example.objects.count(connection_name='DB2')

            r1 = Example.objects.get(connection_name='DEFAULT', name='Rock')
            r2 = Example.objects.get(connection_name='DB2', name='Rock2')

            assert r1.name != r2.name

            rock.delete()
            self.pool.commit()
            assert 0 == Example.objects.count(connection_name='DEFAULT')

            l1 = list(Example.objects.filter_by(connection_name='DEFAULT'))
            l2 = list(Example.objects.filter_by(connection_name='DB2'))

            assert 0 == len(l1)
            assert 1 == len(l2)

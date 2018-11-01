from flask_philo_sqlalchemy.test import SQLAlchemyTestCase
from flask_philo_sqlalchemy.http import SQLAlchemyView
from sqlalchemy import Column, String
from flask_philo_core.test import BaseTestFactory
from flask_philo_sqlalchemy.orm import BaseModel
from flask_philo_sqlalchemy.exceptions import NotFoundError
from flask import json




class User(BaseModel):
    __tablename__ = 'user_test_views'
    username = Column(String(64))


class ModelFactory(BaseTestFactory):

    @classmethod
    def create_user(self):
        user = User(username=self.create_unique_string())
        user.add()
        user.objects.pool.commit()
        return user

class UserResourceView(SQLAlchemyView):

    def get(self, id=None):

        try:
            if id is not None:

                user = User.objects.get(id=id)
                data = {'id': user.id, 'username': user.username}
            else:
                data = [
                   {'id': user.id, 'username': user.username}
                   for user in User.objects.filter_by()
                ]
            return self.json_response(status=200, data=data)
        except NotFoundError:
            return self.json_response(status=404)





class TestCaseModel(SQLAlchemyTestCase):
    config = {
        'FLASK_PHILO_EXTENSIONS': ('Flask-Philo-SQLAlchemy', ),
        'Flask-Philo-SQLAlchemy': {
            'DEFAULT': 'postgresql://ds:dsps@pgdb:5432/ds_test',
        }
    }

    urls = (
        ('/users', UserResourceView, 'users'),
        ('/users/<int:id>', UserResourceView, 'user'),
    )

    def test_get(self):
        with self.app.app_context():
            assert 0 == User.objects.count()
            user1 = ModelFactory.create_user()
            user2 = ModelFactory.create_user()

            assert 2 == User.objects.count()
            client = self.app.test_client()

            result = client.get('/users/{}'.format(user1.id))
            assert 200 == result.status_code
            j_content = json.loads(result.get_data().decode('utf-8'))
            assert j_content['id'] == user1.id

            client = self.app.test_client()
            result2 = client.get('/users/{}'.format(user2.id))
            assert 200 == result2.status_code
            j_content2 = json.loads(result2.get_data().decode('utf-8'))
            assert j_content2['id'] == user2.id

            client = self.app.test_client()
            result3 = client.get('/users')
            assert 200 == result3.status_code
            j_content3 = json.loads(result3.get_data().decode('utf-8'))
            assert 2 == len(j_content3)



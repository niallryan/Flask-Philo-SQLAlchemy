from flask_philo_sqlalchemy.test import SQLAlchemyTestCase
from flask_philo_sqlalchemy.orm import BaseModel
from flask_philo_sqlalchemy.types import Password
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Boolean
from sqlalchemy.orm import relationship
from flask_philo_sqlalchemy.exceptions import NotFoundError

import pytest


class User(BaseModel):
    __tablename__ = 'users'
    username = Column(String(64))
    password = Column(Password)
    email = Column(String(64))
    is_active = Column(Boolean(), nullable=False, default=False)
    credit_score = Column(Numeric(), nullable=True)

    def get_id(self):
        return self.id

    @classmethod
    def authenticate(cls, username=None, email=None, password=None):
        user = User.objects.get(username=username, email=email)
        assert user.password == password
        return user


class Genre(BaseModel):
    __tablename__ = 'genre'
    name = Column(String(256))
    description = Column(String(256))


class Artist(BaseModel):
    __tablename__ = 'artist'
    name = Column(String(256))
    description = Column(String(256))
    albums = relationship('Album', backref='artist')
    genre_id = Column(Integer, ForeignKey('genre.id'))


class Album(BaseModel):
    __tablename__ = 'album'
    name = Column(String(256))
    description = Column(String(256))
    artist_id = Column(Integer, ForeignKey('artist.id'))


class TestCaseModel(SQLAlchemyTestCase):

    config = {
        'FLASK_PHILO_EXTENSIONS': ('Flask-Philo-SQLAlchemy', ),
        'Flask-Philo-SQLAlchemy': {
            'DEFAULT': 'postgresql://ds:dsps@pgdb:5432/ds_test',
        }
    }

    def test_simple_insert(self):
        with self.app.app_context():
            assert 0 == Genre.objects.count()
            genre = Genre(name='name1', description='dsc1')
            genre.add()
            self.pool.commit()
            assert 1 == Genre.objects.count()
            genre2 = Genre(name='name2', description='dsc2')
            genre2.add()
            genre2.objects.pool.commit()
            assert 2 == Genre.objects.count()

    def test_multi_insert(self):
        with self.app.app_context():
            assert 0 == Genre.objects.count()
            data = [
                Genre(
                    name='genre{}'.format(x),
                    description='descript{}'.format(x))
                for x in range(100)
            ]

            Genre.objects.add_all(data)
            self.pool.commit()
            assert 100 == Genre.objects.count()

    def test_relationships(self):
        with self.app.app_context():
            rock = Genre(name='Rock', description='rock yeah!!!')
            rock.add()
            self.pool.commit()
            pink = Artist(
                genre_id=rock.id, name='Pink Floyd', description='Awsome')
            pink.add()
            self.pool.commit()
            dark = Album(
                artist_id=pink.id, name='Dark side of the moon',
                description='Interesting')
            dark.add()
            self.pool.commit()
            rolling = Artist(
                genre_id=rock.id,
                name='Rolling Stones', description='Acceptable')

            rolling.add()
            self.pool.commit()

            hits = Album(
                artist_id=rolling.id, name='Greatest hits',
                description='Interesting')
            hits.add()
            self.pool.commit()
            assert 2 == Album.objects.count()

            wall = Album(
                artist_id=pink.id, name='The Wall',
                description='Interesting')
            wall.add()
            self.pool.commit()
            assert 2 == len(pink.albums)
            assert 2 == len(Artist.objects.filter_by(genre_id=rock.id)[:])

    def test_update(self):
        with self.app.app_context():
            rock = Genre(name='Rock', description='rock yeah!!!')
            rock.add()
            self.pool.commit()
            description_updated = 'description_updated'
            rock.description = description_updated
            rock.update()
            self.pool.commit()
            rock2 = Genre.objects.get(id=rock.id)
            assert rock2.description == description_updated
            assert 1 == Genre.objects.count()

    def test_get_for_update(self):
        with self.app.app_context():
            rock = Genre(name='Rock', description='rock yeah!!!')
            rock.add()
            self.pool.commit()
            rock2 = Genre.objects.get_for_update(id=rock.id)
            rock2.name = 'updated name'
            rock2.update()
            assert rock2.id == rock.id
            rock2.objects.pool.close()

    def test_delete(self):
        with self.app.app_context():
            rock = Genre(name='Rock', description='rock yeah!!!')
            rock.add()
            self.pool.commit()
            assert 1 == Genre.objects.count()
            rock.delete()
            self.pool.commit()
            assert 0 == Genre.objects.count()

    def test_raw_sql(self):
        with self.app.app_context():
            rock = Genre(name='Rock', description='rock yeah!!!')
            rock.add()
            self.pool.commit()
            pink = Artist(
                genre_id=rock.id, name='Pink Floyd', description='Awsome')
            pink.add()
            self.pool.commit()
            dark = Album(
                artist_id=pink.id, name='Dark side of the moon',
                description='Interesting')
            dark.add()
            self.pool.commit()
            rolling = Artist(
                genre_id=rock.id,
                name='Rolling Stones', description='Acceptable')

            rolling.add()
            self.pool.commit()
            sql = """
                SELECT a.name as artist_name, a.description artist_description,
                g.name as artist_genre
                FROM artist a
                INNER JOIN genre g ON a.genre_id = g.id
                ORDER BY a.id DESC;
            """

            result = Genre.objects.raw_sql(sql).fetchall()
            assert 2 == len(result)
            assert 'Rolling Stones' == result[0][0]

            sql = """
                SELECT a.name as artist_name, a.description artist_description,
                g.name as artist_genre
                FROM artist a
                INNER JOIN genre g ON a.genre_id = g.id
                WHERE a.id = :artist_id
                ORDER BY a.id DESC;
            """

            result = Genre.objects.raw_sql(sql, artist_id=pink.id).fetchall()
            assert 1 == len(result)
            assert 'Pink Floyd' == result[0][0]

    def test_not_found(self):
        with self.app.app_context():
            with pytest.raises(NotFoundError) as excinfo:
                Genre.objects.get(id=-666)
            assert "Object not found" in str(excinfo.value)

    def test_encrypted_password(self):
        with self.app.app_context():
            user = User(
                username='username', email='eil@il.com', password='123')
            user.add()
            self.pool.commit()
            id = user.id
            # objects needs to dereferenciated otherwise
            # user2 will be just a copy of user
            user = None
            user2 = User.objects.get(id=id)
            assert id == user2.id
            assert '123' == user2.password

    def test_to_dict(self):
        genre = Genre(name='name1', description='dsc1')
        j = genre.dict
        assert 'name' in j
        assert j['name'] == genre.name

        assert 'description' in j
        assert j['description'] == genre.description

    def test_serializer_to_model(self):
        user_dict = {
            'username': 'userupdated', 'password': '123',
            'email': 'email@test.com'}
        user_model = User(**user_dict)
        assert user_dict['username'] == user_model.username
        assert user_model.email == user_dict['email']

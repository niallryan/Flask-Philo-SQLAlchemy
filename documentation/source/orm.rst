SQL Alchemy ORM for Flask-Philo-Core
=======================================

Flask-Philo-SQLAlchemy provides support for relational databases. For mode detail and documentation on SQL Alchemy, visit `<https://www.sqlalchemy.org/>`_


Where is Flask-Philo-Core SQLAlchemy ORM implementation?
----------------------------------------------------------

Flask-Philo-SQLAlchemy can be found at:

`<https://github.com/Riffstation/Flask-Philo-SQLAlchemy>`_


Database Settings
----------------------------

The first
thing you need to do is to add the relevant configuration
to your application's settings file, typically ``<your_app>/config/settings.py`` :

::

    'FLASK_PHILO_EXTENSIONS': ('Flask-Philo-SQLAlchemy', ),

    'Flask-Philo-SQLAlchemy': {
        'DEFAULT': 'postgresql://ds:dsps@pgdb:5432/ds_test',
    }



Models
----------------------------

In order to create Flask-Philo Models, simply create classes that inherit
from ``flask_philo_sqlalchemy.orm.BaseModel`` class:


``BaseModel`` exposes a number of useful methods for retrieving and manipulating
data:

* **add()** - create a new Flask-Philo class instance (ORM object)
* **update()** - modify an existing ORM object
* **delete()** - delete an ORM object
* **objects.get(key=value)** - retrieve an ORM object by a specified key
* **objects.filter_by(key=value)** - retrieve a collection of filtered objects by a specified key/keys
* **objects.count()** - count all object instances of a Flask-Philo class
* **objects.raw_sql(sql_query_string)** - run direct SQL queries on your application's database

...examples for each of these methods are included in the **Data Manipulation Examples** section below


Example Models
----------------

Here are 3 examples of models with some simple properties and examples of how you can use them in
your application:

::

    from flask_philo_sqlalchemy.test import SQLAlchemyTestCase
    from flask_philo_sqlalchemy.orm import BaseModel
    from flask_philo_sqlalchemy.types import Password
    from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Boolean
    from sqlalchemy.orm import relationship
    from flask_philo_sqlalchemy.exceptions import NotFoundError

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



Flask-Philo's ORM automatically handles the creation of each model's integer
``id`` property, along with automatically creating and updating the timestamp
fields ``created_at`` and ``updated_at``.

Foreign Keys may be defined using the ``ForeignKey(<key_name>)`` syntax, as is
the case in our example **Album** model above. Here, the **Album** model
references the **Artist** model (DB table ``artist``) as a foreign key
using ``artist.id``


Fields
----------------------------


The most common field types are:

- **Column**: defines the properties of a given column

- **relationship**: defines the relationship between two tables


Examples:

::

    class Artist(BaseModel):
        __tablename__ = 'artist'
        name = Column(String(256))
        description = Column(String(256))
        albums = relationship('Album', backref='artist')
        genre_id = Column(Integer, ForeignKey('genre.id'))


Supported data types
##############################

The following is a basic list of fields supported by SQLAlchemy. Please
refer to the official   `SQLAlchemy Documentation <https://docs.sqlalchemy.org>`_ for further information.

- **String**: stores string format data

::

    name = Column(String(256))


- **Integer**: stores integer format data

::

    amount = Column(Integer)

- **Boolean**: stores boolean format data

::

    is_famous = Column(Boolean, default=False)


- **Numeric**: store numbers with a very large number of digits. Scale is the count of decimal digits in the fractional part. Precision refers to the total count of digits in the whole number.

::

    tempo = Column(Numeric(precision=32, scale=16))


- **ARRAY**: store array data

::

    possible_names = Column(ARRAY(String(256)))


- **JSON**: stores JSON format data

::

    config_dict = Column(JSON)



- **Enum**: provides a set of possible string values that work as constraints for the given column.

::

    day = Column(
        Enum(
            'sunday', 'monday', 'tuesday', 'wednesday', 'thursdat', 'fruday',
            'saturday', name="days_of_the_week"))


Field options
##############################

The following ORM constraints can be set in your Flask-Philo Model:

- **PrimaryKey**: specifies that a given column is a primary key. As such, it is unique and not nullable.

::

    id = Column(Integer, primary_key=True)


- **ForeignKey**: specifies a column that acts as foreign key, thereby defining a relationship with another table

::

    genre_id = Column(Integer, ForeignKey('genre.id'))


- **unique**: specifies that a column must have a unique value for each record

::

    name = Column(String(256), unique=True)


- **nullable**: specifies if a column accepts null values or not

::

    name = Column(String(256), nullable=False, unique=True)


- **default**: defines a default value in the case that it is not specified

::

    is_famous = Column(Boolean, default=False)


Connection Pool
------------------------------

As a design decision, management of the database connections is the responsability
of the developer, but this is made simple with Flask-Philo's built-in
connection management methods.

* to instantiate a DB session, we use
  ``flask_philo_sqlalchemy.connection.create_pool()`` function.
* after modifying, creating or removing data in a session, we must commit or
  rollback the session using Flask-Philo's ``pool.commit()``
  or ``pool.rollback()`` methods

Opening a Flask-Philo DB session
####################################

::

    flask_philo_sqlalchemy.connection import create_pool
    pool = get_pool()
    # Do some ORM operations here
    pool.commit()


The following examples demonstrate each of the core ORM operations you will
commonly use to query a  database


Data Manipulation Examples
----------------------------

Adding a new record
####################################

In this example, we create a new **Genre** using the same model defined in the **Example Models** section:

::

    pool = get_pool()
    rock = Genre(name='Rock', description='Rock and Roll')
    rock.add()


At this point, we have added a new instance of the **Genre** model to our DB session, but we still need to either ``commit()`` or ``rollback()`` the insert operation

To commit the operation and create a new record:

::

    pool.commit()


...alternatively, if the record is not needed the transaction can be rolled-back, and nothing will be changed in the  database:

::

    pool.rollback()



Retrieving a specific record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that we've created and committed our new 'Rock' genre, we can retrieve the record directly from the database by using the ``objects.get()`` function:

::

    genre_obj = Genre.objects.get(name="Rock")
    genre_name = genre_obj.name
    genre_id = genre_obj.id
    print("Genre", genre_id, ":", genre_name)   # Will print "Genre 13 : Rock"

...we can also retrieve a record that matches *multiple* field values:

::

    genre_obj = Genre.objects.get(id=13, name="Rock")
    print("Genre", genre_obj.id, ":", genre_obj.name)   # Will print "Genre 13 : Rock"



Filtering records
^^^^^^^^^^^^^^^^^^^^

We may also use ``filter_by()`` function to filter records and retrieve a
collection of all matching instances of the desired model.

Continuing our **Genre** example from earlier sub-sections:

::

    genre_collection = Genre.objects.filter_by(name="Rock")
    genre_obj = genre_collection.first()
    print("Genre", genre_obj.id, ":", genre_obj.name)   # Will print "Genre 13 : Rock"


Updating a record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Just as we can retrieve a record, we can update records in a similar manner:

::

    genre_obj = Genre.objects.filter_by(name="Rock").first()
    genre_obj.name = "Metal"
    genre_obj.update()
    pool.commit()

    updated_genre_obj = Genre.objects.filter_by(name="Metal").first()
    print("Genre", updated_genre_obj.id, ":", updated_genre_obj.name)   # Will print "Genre 13 : Metal"


Deleting a record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the same way we've added and updated a record, we can also delete it:

::

    genre_obj = Genre.objects.filter_by(name="Metal").first()
    genre_obj.delete()
    pool.commit()

    genre_obj = Genre.objects.filter_by(name="Metal").first()   # genre_obj == None

..once we have committed the ``delete()`` operation, this record no
longer exists in our DB.


Counting records
^^^^^^^^^^^^^^^^^

To count the number of instances of a given Model, we can use the
``objects.count()`` method.

::

    genre_count = Genre.objects.count()
    print(genre_count, "Genres present")  # Will print "13 Genres present"


Querying using Raw SQL
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While the use of SQLAlchemy ORM will automatically translate method
calls to their corresponding SQL queries, we also provide a means of
directly querying our underlying SQL database with a raw SQL query.

By passing a valid SQL query-string to the ``objects.raw_sql()`` method, we can
retrieve or update data explicitly, as is the case in the following examples:

Retrieving data by raw SQL:

::

    raw_sql_genre_result = Genre.objects.raw_sql("SELECT description FROM genre WHERE name='Rock';").fetchone()
    genre_description = raw_sql_genre_result.description
    genre_name = raw_sql_genre_result.name
    print(genre_name, "genre description :", genre_description) # Will print "Rock genres description : Rock and Roll"


Modifying data by raw SQL:

::

    query_string = "UPDATE genre SET name='Indie' WHERE id = 13"
    Genre.objects.raw_sql(query_string)




Data manipulation with Relationships
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example demonstrates the creation and retrieval of objects for two
related models, **Album** and **Artist**, as defined in the *Example Models* section above

::

        # Create and commit an artist record
        floyd_artist_obj = Artist(name='Pink Floyd')
        floyd_artist_obj.commit()
        pink_floyd_id = floyd_artist_obj.id
        pool.commit()

        # Create and commit a related album
        dark_album_obj = Album(
            artist_id=pink_floyd_id, name='Dark side of the moon')
        dark_album_obj.add()
        pool.commit()

        # Create and commit another related album by the same artist
        wall = Album(
            artist_id=pink_floyd_id, name='The Wall',
            description='Interesting')
        wall.add()
        pool.commit()

        # Retrieve all albums by Pink Floyd
        album_results = Album.objects.filter_by(artist_id=pink_floyd_id)
        for album_obj in album_results:
            print("Pink Floyd album :", album_obj.name)

        # Will print:
        # Pink Floyd album : Dark side of the moon
        # Pink Floyd album : The Wall



Flask-Philo-SQLAlchemy Views
-------------------------------------


Flask-Philo-SQLAlchemy  provides functionality that makes easier to
integrate database access functionality in your views. All you need to do is
extend the class ``flask_philo_sqlalchemy.http.SQLAlchemyView`` to create  class based
view objects that already contain a ``flask_philo_sqlalchemy.connection.ConnectionPool``
object with a connection to each one of the databases defined in configuration:


::

    from flask_philo_sqlalchemy.http import SQLAlchemyView

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

        def post(self):
            obj = User(**request.json)
            obj.add()
            self.sqlalchemy_pool.commit()
            data = {'id': obj.id}
            return self.json_response(status=201, data=data)

        def put(self, id=None):
            obj = User.objects.get_for_update(id=id)
            obj.username = request.json['username']
            obj.update()
            self.sqlalchemy_pool.commit()
            obj = User.objects.get(id=id)
            data = {'id': obj.id, 'username': obj.username}
            return self.json_response(status=200, data=data)

        def delete(self, id=None):
            obj = User.objects.get(id=id)
            obj.delete()
            self.sqlalchemy_pool.commit()
            return self.json_response(status=200)




Unit Tests
-------------------------------

Flask-Philo-SQLAlchemyView initializes database connections for you
in unit testing. All you need to do is to extend the class
``flask_philo_sqlalchemy.test.SQLAlchemyTestCase``:


::

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

        def test_post(self):
            with self.app.app_context():
                assert 0 == User.objects.count()

                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                }
                data = json.dumps({'username': 'username'})
                client = self.app.test_client()
                result = client.post('/users', data=data, headers=headers)
                assert 201 == result.status_code
                assert 1 == User.objects.count()

        def test_put(self):
            with self.app.app_context():
                user = ModelFactory.create_user()
                assert 1 == User.objects.count()
                old_username = user.username

                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                }
                data = json.dumps({'username': 'newusername', 'id': user.id})
                url = 'users/{}'.format(user.id)

                client = self.app.test_client()
                result = client.put(url, data=data, headers=headers)
                assert 200 == result.status_code
                assert 1 == User.objects.count()
                j_content = json.loads(result.get_data().decode('utf-8'))

                assert j_content['id'] == user.id
                assert j_content['username'] != old_username
                assert j_content['username'] == 'newusername'

        def test_delete(self):
            with self.app.app_context():
                user1 = ModelFactory.create_user()
                assert 1 == User.objects.count()
                client = self.app.test_client()

                result = client.delete('/users/{}'.format(user1.id))
                assert 200 == result.status_code
                assert 0 == User.objects.count()


Using multiple  databases
-------------------------------------

Flask-Philo-SQLAlchemy allows you to connect to multiple database instances
from the same application.

To take advantage of this feature, simply add a ``Flask-Philo-SQLAlchemy``
block in an application configuration file in ``src/config``.

Here's an example of a typical configuration file:

::


    'Flask-Philo-SQLAlchemy': {
        'DEFAULT': 'postgresql://ds:dsps@pgdb:5432/ds_test',
        'MUSICDB': 'postgresql://user:password@host:port/songs_database_name',
    }




...with this configuration in place, we can now access a specific database while
using Flask-Philo-SQLAlchemy connection poool: 

::

    # Add a Genre object to our session
    blues_obj = Genre(name='Blues', description='Still got the blues')
    blues_obj.add()

    # Commit changes to the MUSIC_CATALOG database
    pool.commit(connection_name='MUSIC_CATALOG'))

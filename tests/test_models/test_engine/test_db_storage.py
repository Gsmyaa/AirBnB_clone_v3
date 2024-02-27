#!/usr/bin/python3
"""test for file storage"""
import unittest
from os import getenv
import MySQLdb
from models.state import State
from models.engine.db_storage import DBStorage


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'Not db storage')
class TestDBStorage(unittest.TestCase):
    '''this will test the DBStorage'''

    @classmethod
    def setUpClass(self):
        """set up for test"""
        self.User = getenv("HBNB_MYSQL_USER")
        self.Passwd = getenv("HBNB_MYSQL_PWD")
        self.Db = getenv("HBNB_MYSQL_DB")
        self.Host = getenv("HBNB_MYSQL_HOST")
        self.db = MySQLdb.connect(host=self.Host, user=self.User,
                                  passwd=self.Passwd, db=self.Db,
                                  charset="utf8")
        self.query = self.db.cursor()
        self.storage = DBStorage()
        self.storage.reload()

    @classmethod
    def teardown(self):
        """at the end of the test this will tear it down"""
        self.query.close()
        self.db.close()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'Not db storage')
    def test_read_tables(self):
        """existing tables"""
        self.query.execute("SHOW TABLES")
        salida = self.query.fetchall()
        self.assertEqual(len(salida), 7)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'Not db storage')
    def test_no_element_user(self):
        """no elem in users"""
        self.query.execute("SELECT * FROM users")
        salida = self.query.fetchall()
        self.assertEqual(len(salida), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'Not db storage')
    def test_no_element_cities(self):
        """no elem in cities"""
        self.query.execute("SELECT * FROM cities")
        salida = self.query.fetchall()
        self.assertEqual(len(salida), 0)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != 'db', 'Not db storage')
    def test_add(self):
        """Test same size between storage() and existing db"""
        self.query.execute("SELECT * FROM states")
        query_rows = self.query.fetchall()
        self.assertEqual(len(query_rows), 0)
        state = State(name="Ebonyi")
        state.save()
        self.db.autocommit(True)
        self.query.execute("SELECT * FROM states")
        query_rows = self.query.fetchall()
        self.assertEqual(len(query_rows), 1)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
    def test_get(self):
        """Test that get returns specific object, or none"""
        newState = State(name="New York")
        newState.save()
        newUser = User(email="bob@foobar.com", password="password")
        newUser.save()
        self.assertIs(newState, models.storage.get("State", newState.id))
        self.assertIs(None, models.storage.get("State", "blah"))
        self.assertIs(None, models.storage.get("blah", "blah"))
        self.assertIs(newUser, models.storage.get("User", newUser.id))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "not testing db storage")
    def test_count(self):
        """add new object to db"""
        startCount = models.storage.count()
        self.assertEqual(models.storage.count("Blah"), 0)
        newState = State(name="Montevideo")
        newState.save()
        newUser = User(email="ralexrivero@gmail.com.com", password="dummypass")
        newUser.save()
        self.assertEqual(models.storage.count("State"), startCount + 1)
        self.assertEqual(models.storage.count(), startCount + 2)


if __name__ == "__main__":
    unittest.main()

import os
from app import application
import unittest
import tempfile


class SwagifyTest(unittest.TestCase):

    def setUp(self):
        self.db_fd, application.config['DATABASE'] = tempfile.mkstemp()
        application.testing = True
        self.app = application.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(application.config['DATABASE'])

    def test_unauthorized_access(self):
        rv = self.app.get('/api/resource')
        assert b'Unauthorized Access' in rv.data

    def test_adding_new_user(self):
        user = {'name': 'foobar1', 'email': 'foobar@f2oobar.com', 'password': 'foobar'}
        rv = self.app.post('/api/users', query_string=user)
        assert b'{\n  "data": "Successfully registered!"\n}\n' in rv.data


if __name__ == '__main__':
    unittest.main()
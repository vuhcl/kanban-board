# Unittests

import os
from app import db
import app
import unittest
import tempfile
from app.models import User, Task
from passlib.hash import sha256_crypt
from werkzeug.exceptions import HTTPException

class AppTestCase(unittest.TestCase):
    def setUp(self):
        """Creates a new test client and initializes a new database"""
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.testing = True
        self.app = app.app.test_client()
        db.drop_all()
        db.create_all()

    def tearDown(self):
        """Closes the test database"""
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def signup(self, username, password):
        """Send request to sign up page"""
        return self.app.post('/signup', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def login(self, username, password):
        """Send request to login page"""
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def add(self, task):
        """Send request to add new task"""
        return self.app.post('/add', data=dict(
            task=task,
            status='to_do'
        ), follow_redirects=True)

    def change_status(self, id, status):
        """Send request to change status of task"""
        return self.app.get('/task/'+str(id)+'/'+str(status), data=dict(
            id=id,
            status=status
        ), follow_redirects=True)

    def delete_task(self, id):
        """Send request to delete task"""
        return self.app.get('/task/'+str(id), data=dict(
            id=id,
        ), follow_redirects=True)

    def logout(self):
        """Send request to log out page"""
        return self.app.get('/logout', follow_redirects=True)

    def test_signup(self):
        """Test sign up"""
        self.signup('admin', 'password')
        h = 'password'+'admin'
        user = db.session.query(User).filter(User.username=='admin').first()
        self.assertTrue(sha256_crypt.verify(h, user.password))

    def test_signup_duplicate(self):
        """Test if duplicated username is not excepted"""
        self.signup('admin', 'password')
        h = 'password'+'admin'
        user = db.session.query(User).filter(User.username=='admin').first()
        self.assertTrue(sha256_crypt.verify(h, user.password))
        response = self.signup('admin', 'pass')
        assert b'Username already existed!' in response.data

    def test_login_logout(self):
        """Test login and log out"""
        self.signup('admin', 'password')
        h = 'password'+'admin'
        user = db.session.query(User).filter(User.username=='admin').first()
        self.assertTrue(sha256_crypt.verify(h, user.password))
        response = self.login('admin', 'password')
        assert b'Logged in successfully!' in response.data
        response = self.logout()
        assert b'Logged out successfully!' in response.data

    def test_login_exceptions(self):
        """Test login exceptions"""
        self.signup('admin', 'password')
        h = 'password'+'admin'
        user = db.session.query(User).filter(User.username=='admin').first()
        self.assertTrue(sha256_crypt.verify(h, user.password))
        response = self.login('admin', 'pass')
        assert b'Incorrect password!' in response.data
        response = self.login('adminx', 'password')
        assert b'Invalid username!' in response.data

    def test_add_task(self):
        """Test that one can add tasks"""
        self.signup('admin', 'password')
        h = 'password'+'admin'
        user = db.session.query(User).filter(User.username=='admin').first()
        self.assertTrue(sha256_crypt.verify(h, user.password))
        response = self.login('admin', 'password')
        assert b'Logged in successfully!' in response.data
        self.add('Write unittests!')
        task = db.session.query(Task).filter(Task.task=='Write unittests!').first()
        self.assertEqual(task.task, 'Write unittests!')
        assert task.status is 'to_do'

    def test_move_task(self):
        """Test that one can move and delete tasks"""
        self.signup('admin', 'password')
        h = 'password'+'admin'
        user = db.session.query(User).filter(User.username=='admin').first()
        self.assertTrue(sha256_crypt.verify(h, user.password))
        response = self.login('admin', 'password')
        assert b'Logged in successfully!' in response.data
        
        self.add('Write unittests!')
        task = db.session.query(Task).filter(Task.task=='Write unittests!').first()
        self.assertEqual(task.task, 'Write unittests!')
        assert task.status is 'to_do'
        
        self.change_status(task.id, 'doing')
        task = db.session.query(Task).filter(Task.task=='Write unittests!').first()
        assert task.status is 'doing'
        
        self.change_status(task.id, 'done')
        task = db.session.query(Task).filter(Task.task=='Write unittests!').first()
        assert task.status is 'done'
        
        self.change_status(task.id, 'to_do')
        task = db.session.query(Task).filter(Task.task=='Write unittests!').first()
        assert task.status is 'to_do'
        
        self.delete_task(task.id)
        task = db.session.query(Task).filter(Task.id==task.id).first()
        assert task is None

    def test_validate_user(self):
        """Test that one needs to log in to edit the kanban board"""
        response = self.add('Write unittests!')
        assert b'401' in response.data
        response = self.change_status(1, 'doing')       
        assert b'401' in response.data
        response = self.delete_task(1)        
        assert b'401' in response.data

    def test_validate_task(self):
        """Test status code when trying to move or delete non-existent task"""
        self.signup('admin', 'password')
        h = 'password'+'admin'
        user = db.session.query(User).filter(User.username=='admin').first()
        self.assertTrue(sha256_crypt.verify(h, user.password))
        response = self.login('admin', 'password')
        assert b'Logged in successfully!' in response.data
        response = self.change_status(1, 'doing')        
        assert b'404' in response.data
        response = self.delete_task(1)        
        assert b'404' in response.data

if __name__ == '__main__':
    unittest.main()
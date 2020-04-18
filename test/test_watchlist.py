import unittest

from app import app, db, Movie, User


class WatchlistTestCase():
    
    def setUp(self):
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'
        )
        db.create_all()
        user = User(name='Test', username='test')
        user.set_password('123')
        movie = Movie(title='Test Movie Title', year='2019')
        db.session.add_all([user, movie])
        db.session.commit()
        
        self.client = app.test_client()
        self.runner = app.test_cli_runner()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_app_exist(self):
        self.assertIsNotNone(app)
        
    def test_app_is_testing(self):
        self.assertTrue(app.config['TESTING'])

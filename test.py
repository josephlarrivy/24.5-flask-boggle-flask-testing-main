from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class TestBoggle(TestCase):
    with app.test_client() as client:
        def SetUp(self):
            """setup every test"""
            app.config['TESTING'] = True

        def test_home(self):
            res = self.client.get('/')
            self.assertIsNone(session.get('playcount'))
            self.assertIn('<p>', res.data)
            self.assertIn('score', res.data)

        def test_words(self):
            with client.session_transaction() as sess_one:
                sess_one['board'] = [
                    ["H", "O", "P", "X", "X"],
                    ["X", "X", "X", "X", "X"],
                    ["X", "X", "X", "X", "X"],
                    ["X", "X", "X", "X", "X"],
                    ["X", "X", "X", "X", "X"]]
            res = self.client.get('/check-word?word=hop')
            self.assertEqual(res.json['result'], 'ok')

        def test_invalid_word(self):
            self.client.get('/')
            response = self.client.get('/check-word?word=impossible')
            self.assertEqual(response.json['result'], 'not-on-board')

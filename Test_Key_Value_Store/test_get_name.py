import flask
import os
import unittest
import time

app = flask.Flask(__name__)


class BasicTests(unittest.TestCase):

    def tearDown(self):
        pass

    def test_app_main(self):
        with app.test_request_context('/get/Sandeep?value=Chandel'):
            assert flask.request.path == '/get/Sandeep'
            assert flask.request.args['value'] == 'Chandel'

    def test_get_function(self):
        with app.test_request_context():
            from Key_Value_Process_Node import get, setinternal
            setinternal('Sandeep')
            self.assertLike(get(), '{"time":{},"value":"nan"}'.format(time.time()))

    def test_setkey_function(self):
        with app.test_request_context():
            from Key_Value_Process_Node import setkey
            self.assertLike(setkey('ABC'), '{"data":{"ABC":{"time":{},"value":NaN}}}'.format(time.time()))

    def test_setinternal_function(self):
        with app.test_request_context():
            from Key_Value_Process_Node import setinternal
            self.assertAlmostEquals(setinternal('ABC'), '{"data":{"ABC":{"time":{},"value":NaN}}}'.format(time.time()))


if __name__ == "__main__":
    unittest.main()
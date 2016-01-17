import test_helper

import unittest

from etvnet.error_handler import ErrorHandler

class Example(ErrorHandler):
    def handle_error(self, e):
        return e

    def success(self):
        def _(message):
            return message

        return self.handle_exception( _, self.handle_error, message='success')

    def error(self):
        def _(message):
            raise Exception(message)

        return self.handle_exception( _, self.handle_error, message='error')

class MyTest(unittest.TestCase):
    def setUp(self):
        self.subject = Example()

    def test_example(self):
        print(self.subject.success())

        print(self.subject.error())


if __name__ == '__main__':
    unittest.main()

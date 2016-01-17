import unittest

from contextlib import contextmanager

class Fun():
    @contextmanager
    def handle_exception(self, except_callback=None, **args):
        try:
            yield args
        except Exception as e:
            except_callback()

    def error_handler(self):
        print 'error'

    def fun(self, x):
        with self.handle_exception(self.error_handler):
            raise Exception('alex')
            # return x + 1

class MyTest(unittest.TestCase):
    def test(self):
        fun = Fun()

        fun.fun(3)

        # self.assertEqual(fun.fun(3), 4)

if __name__ == '__main__':
    unittest.main()

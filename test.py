import unittest

from hello import sayhello


class SayHelloTest(unittest.TestCase):
    def test_hello(self):
        pass
    def tearDown(self):
        pass
    def test_sayhello(self):
        rv=sayhello()
        self.assertEqual(rv, "Hello, World!")
if __name__ == '__main__':
    unittest.main()
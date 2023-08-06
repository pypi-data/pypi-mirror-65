from fruit.modules.target import Target
import unittest

def fun():
    pass

class TestTarget(unittest.TestCase):
    """Test the Target class of fruit for Target initialization and event calls"""

    def test_init(self):
        """Test the target initialization"""

        self.assertEqual(Target(fun, "TestName").name, "TestName")
        self.assertEqual(Target(fun, "TestName").help, "")
        self.assertEqual(Target(fun, "TestName", help="HelpText").help, "HelpText")

        # Test exceptions
        with self.assertRaises(TypeError):
            Target("x", "TestName")
        with self.assertRaises(TypeError):
            Target([], "TestName")

        # Empty Name
        with self.assertRaises(ValueError):
            Target(fun, "")

        # Bad name type
        with self.assertRaises(TypeError):
            Target(fun, 1)
        with self.assertRaises(TypeError):
            Target(fun, fun)
        with self.assertRaises(TypeError):
            Target(fun, [])

        # Bad help type
        with self.assertRaises(TypeError):
            Target(fun, "TestName", help=None)
        with self.assertRaises(TypeError):
            Target(fun, "TestName", help=1)
        with self.assertRaises(TypeError):
            Target(fun, "TestName", help=[])
        with self.assertRaises(TypeError):
            Target(fun, "TestName", help=["helptext"])

    def test_onactivate(self):
        """Test the OnActivate Event"""
        pass

    def test_ondeactivate(self):
        """Test the OnDeactivate Event"""
        pass
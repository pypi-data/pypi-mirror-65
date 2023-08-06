from fruit.modules.provider import Provider
import unittest

def test_fcn(arg: str):
    return arg

class TestProvider(unittest.TestCase):
    """Test the Provider modules of fruit"""

    def test_init(self):
        """Test the initializer of the provider class"""

        self.assertEqual(
            Provider("Name", "Description", test_fcn).name,
            "Name"
        )

        self.assertEqual(
            Provider("Name", "Description", test_fcn).help,
            "Description"
        )

        # Test value checking
        with self.assertRaises(ValueError):
            Provider("name", "", test_fcn)
        with self.assertRaises(ValueError):
            Provider("", "help", test_fcn)
        with self.assertRaises(ValueError):
            Provider("", "", test_fcn)
        
        # Test initializer errors for None
        with self.assertRaises(TypeError):
            Provider(None, "x", test_fcn)
        with self.assertRaises(TypeError):
            Provider("x", None, test_fcn)
        with self.assertRaises(TypeError):
            Provider(None, None, test_fcn)
        
        # Test initializer errors for Numbers
        with self.assertRaises(TypeError):
            Provider(10, "x", test_fcn)
        with self.assertRaises(TypeError):
            Provider("x", 10, test_fcn)
        with self.assertRaises(TypeError):
            Provider(10, 10, test_fcn)
        
        # Test initializer errors for lists
        with self.assertRaises(TypeError):
            Provider([], "x", test_fcn)
        with self.assertRaises(TypeError):
            Provider("x", [], test_fcn)
        with self.assertRaises(TypeError):
            Provider([], [], test_fcn)

        # Test the callable parameter
        with self.assertRaises(TypeError):
            Provider("x", "x", None)
        with self.assertRaises(TypeError):
            Provider("x", "x", 1)
        with self.assertRaises(TypeError):
            Provider("x", "x", [])
        with self.assertRaises(TypeError):
            Provider("x", "x", "function")
    
    def test_provider_call(self):
        """Test the provider function to always return a string"""
        
        self.assertEqual(
            Provider("name", "help", test_fcn)("FCN"),
            "FCN"
        )

        self.assertEqual(
            Provider("name", "help", test_fcn)(123),
            "123"
        )

        self.assertEqual(
            Provider("name", "help", test_fcn)([1,2,3]),
            "[1, 2, 3]"
        )

        self.assertEqual(
            Provider("name", "help", test_fcn)(['1','2','3']),
            "['1', '2', '3']"
        )


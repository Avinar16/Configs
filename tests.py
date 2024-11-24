import unittest
from io import StringIO
import sys
from main import *


class TestConfigConverter(unittest.TestCase):
    def test_simple_element(self):
        xml = "<name>value</name>"
        expected = '"value"'
        self.assertEqual(parse_xml_to_config(xml), expected)

    def test_array(self):
        xml = """
        <items>
            <item>one</item>
            <item>two</item>
            <item>three</item>
        </items>
        """
        expected = '[ "one" "two" "three" ]'
        self.assertEqual(parse_xml_to_config(xml), expected)

    def test_dictionary(self):
        xml = """
        <config>
            <key1>value1</key1>
            <key2>value2</key2>
        </config>
        """
        expected = '{\nkey1 = "value1";\nkey2 = "value2";\n}'
        self.assertEqual(parse_xml_to_config(xml), expected)

    def test_mixed_structure(self):
        xml = """
        <root>
            <array>
                <item>value1</item>
                <item>value2</item>
            </array>
            <key>value</key>
        </root>
        """
        expected = '{\narray = [ "value1" "value2" ];\nkey = "value";\n}'
        self.assertEqual(parse_xml_to_config(xml), expected)

    def test_constant_declaration(self):
        handle_constant_declaration("x is 5")
        self.assertEqual(constants["x"], 5)
        handle_constant_declaration("message is \"Hello, World!\"")
        self.assertEqual(constants["message"], "Hello, World!")

    def test_constant_expression_addition(self):
        constants["a"] = 10
        constants["b"] = 20
        result = evaluate_expression("?(+ a b)")
        self.assertEqual(result, 30)


if __name__ == "__main__":
    unittest.main()

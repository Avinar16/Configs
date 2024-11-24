import unittest
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


if __name__ == "__main__":
    unittest.main()

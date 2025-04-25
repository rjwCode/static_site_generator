import unittest
from htmlnode import LeafNode
from textnode import TextNode, TextType
from main import text_node_to_html_node

class TestNodeConvert(unittest.TestCase):
    def test_text_case(self):
        node = TextNode("sample text", TextType.TEXT)
        new_html_node = text_node_to_html_node(node)

        self.assertEqual(new_html_node.tag, None)
        self.assertEqual(new_html_node.value, "sample text")
    
    def test_bold_case(self):
        node = TextNode("sample", TextType.BOLD)
        new_html_node = text_node_to_html_node(node)

        self.assertEqual(new_html_node.tag, "b")
        self.assertEqual(new_html_node.value, "sample")

    def test_italic_case(self):
        node = TextNode("sample", TextType.ITALIC)
        new_html_node = text_node_to_html_node(node)

        self.assertEqual(new_html_node.tag, "i")
        self.assertEqual(new_html_node.value, "sample")

    def test_code_case(self):
        node = TextNode("sample", TextType.CODE)
        new_html_node = text_node_to_html_node(node)

        self.assertEqual(new_html_node.tag, "code")
        self.assertEqual(new_html_node.value, "sample")

    def test_link_case(self):
        node = TextNode("sample", TextType.LINK, "https://test.com")
        new_html_node = text_node_to_html_node(node)

        self.assertEqual(new_html_node.tag, "a")
        self.assertEqual(new_html_node.value, "sample")
        self.assertEqual(new_html_node.props, {"href": "https://test.com"})

    def test_image_case(self):
        node = TextNode("sample", TextType.IMAGE, "/src/images/sample.png")
        new_html_node = text_node_to_html_node(node)

        self.assertEqual(new_html_node.tag, "img")
        self.assertEqual(new_html_node.value, "")
        self.assertEqual(new_html_node.props, {"src": "/src/images/sample.png", "alt": "sample"})

    def test_no_type(self):
        node = TextNode("sample", None)
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

    def test_invalid_type(self):
        with self.assertRaises(AttributeError):
            node = TextNode("sample", TextType.RANDOM)
            text_node_to_html_node(node)
    
if __name__ == "__main__":
    unittest.main()
import unittest

from htmlnode import HTMLNode, LeafNode

class TestHtmlNode(unittest.TestCase):

    #HTMLNode Tests
    def test_one_prop(self):
        expected = ' href="https://test.com"'
        node = HTMLNode("a", "", None, {"href": "https://test.com"})

        self.assertEqual(node.props_to_html(), expected)
    def test_multiple_props(self):
        expected = ' src="test.jpg" width="300" height="400"'
        node = HTMLNode("img", "", None, {"src": "test.jpg", "width": "300", "height": "400"})

        self.assertEqual(node.props_to_html(), expected)
    def test_empty_props(self):
        expected = ""
        node = HTMLNode("p", "This is some sample text")

        self.assertEqual(node.props_to_html(), expected)

    #LeafNode Tests
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Page Title")
        self.assertEqual(node.to_html(), "<h1>Page Title</h1>")

    def test_leaf_no_tag(self):
        node = LeafNode(None, "sample text")
        self.assertEqual(node.to_html(), "sample text")

if __name__ == "__main__":
    unittest.main()
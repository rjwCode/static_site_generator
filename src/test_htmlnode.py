import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    #to_html() Nested Node Tests
    def test_to_html_test_shallow(self):
        parent = ParentNode("div", [LeafNode("span", "sample")])
        self.assertEqual(parent.to_html(), "<div><span>sample</span></div>")

    def test_to_html_nested_parent(self):
        inner_child = LeafNode("b", "BOLD")
        inner_parent = ParentNode("p", [inner_child])
        outer_parent = ParentNode("div", [inner_parent])
        self.assertEqual(outer_parent.to_html(), "<div><p><b>BOLD</b></p></div>")

    def test_to_html_nested_many_children(self):
        inner_child = LeafNode("b", "BOLD")
        inner_child2 = LeafNode("i", "ITALICS")
        inner_parent = ParentNode("p", [inner_child, inner_child2])
        outer_parent = ParentNode("div", [inner_parent])
        self.assertEqual(outer_parent.to_html(), "<div><p><b>BOLD</b><i>ITALICS</i></p></div>")
    
    def test_to_html_no_children(self):
        parent = ParentNode("h2", [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_no_tag(self):
        parent = ParentNode("", [LeafNode("s", "STRIKETHROUGH")])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_none_child(self):
        parent = ParentNode("h2", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_none_tag(self):
        parent = ParentNode(None, [LeafNode("s", "STRIKETHROUGH")])
        with self.assertRaises(ValueError):
            parent.to_html()


if __name__ == "__main__":
    unittest.main()
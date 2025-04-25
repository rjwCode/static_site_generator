import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("Different", TextType.CODE, "https://test.com")
        node2 = TextNode("Differentt", TextType.CODE, "https://test.com")

        self.assertNotEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("entry1", TextType.BOLD, "https://test.com")
        node2 = TextNode("entry1", TextType.CODE, "https://test.com")

        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = TextNode("entry1", TextType.IMAGE, "http://test.com")
        node2 = TextNode("entry1", TextType.IMAGE, "https://test.com")

        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = TextNode("entry1", TextType.IMAGE, "https://test.com")
        node2 = TextNode("entry1", TextType.IMAGE)

        self.assertNotEqual(node, node2)

    def test_eq2(self):
        node = TextNode("entry1", TextType.IMAGE, "https://test.com")
        node2 = TextNode("entry1", TextType.IMAGE, "https://test.com")

        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
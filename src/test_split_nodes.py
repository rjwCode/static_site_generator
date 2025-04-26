import unittest
from main import split_nodes_delimiter, split_single_node
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This contains a **bold section** and more text after", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This contains a ", TextType.TEXT),
                                     TextNode("bold section", TextType.BOLD),
                                     TextNode(" and more text after", TextType.TEXT)])
        
    def test_italics(self):
        node = TextNode("This contains an _italics section_ and more text after", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This contains an ", TextType.TEXT),
                                     TextNode("italics section", TextType.ITALIC),
                                     TextNode(" and more text after", TextType.TEXT)])
        
    def test_code(self):
        node = TextNode("This contains a `code section` and more text after", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This contains a ", TextType.TEXT),
                                     TextNode("code section", TextType.CODE),
                                     TextNode(" and more text after", TextType.TEXT)])
        
    def test_multi_delimiter(self):
        node = TextNode("This contains a `code section` and another `code section` and some other text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This contains a ", TextType.TEXT),
                                     TextNode("code section", TextType.CODE),
                                     TextNode(" and another ", TextType.TEXT),
                                     TextNode("code section", TextType.CODE),
                                     TextNode(" and some other text", TextType.TEXT)])
    
    def test_multi_node(self):
        nodes = [TextNode("This has a **bold section**", TextType.TEXT), TextNode("This has no markdown", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This has a ", TextType.TEXT),
                                     TextNode("bold section", TextType.BOLD),
                                     TextNode("This has no markdown", TextType.TEXT)])
    
    def test_start_markdown(self):
        node = TextNode("**bold section** text after", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("bold section", TextType.BOLD),
                                     TextNode(" text after", TextType.TEXT)])
    
    def test_invalid_markdown(self):
        node = TextNode("hello this has invalid **markdown", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
        


if __name__ == "__main__":
    unittest.main()
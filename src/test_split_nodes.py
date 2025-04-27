import unittest
from main import split_nodes_delimiter, split_single_node, split_nodes_image, split_nodes_link
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

    #Split Image Tests
    def test_not_text(self):
        node = TextNode("", TextType.CODE)
        result = split_nodes_image([node])
        
        self.assertEqual(result, [TextNode("", TextType.CODE, None)])
        
    def test_multiple_image(self):
        node = TextNode("image 1 ![alt](url) image 2 ![alt](url) more text", TextType.TEXT)
        result = split_nodes_image([node])

        self.assertEqual(result, [TextNode("image 1 ", TextType.TEXT),
                                  TextNode("alt", TextType.IMAGE, "url"),
                                  TextNode(" image 2 ", TextType.TEXT),
                                  TextNode("alt", TextType.IMAGE, "url"),
                                  TextNode(" more text", TextType.TEXT)])
    def test_multiple_nodes(self):
        nodes = [TextNode("This node has an ![alt](url) image", TextType.TEXT),
                 TextNode("This node also has an image ![alt](url)", TextType.TEXT)]
        result = split_nodes_image(nodes)

        self.assertEqual(result, [TextNode("This node has an ", TextType.TEXT),
                                  TextNode("alt", TextType.IMAGE, "url"),
                                  TextNode(" image", TextType.TEXT),
                                  TextNode("This node also has an image ", TextType.TEXT),
                                  TextNode("alt", TextType.IMAGE, "url")])
        
    #Split Link Tests
    def test_link_no_text(self):
        node = TextNode("", TextType.CODE)
        result = split_nodes_link([node])
        
        self.assertEqual(result, [TextNode("", TextType.CODE, None)])
        
    def test_multiple_link(self):
        node = TextNode("link 1 [alt](url) link 2 [alt](url) more text", TextType.TEXT)
        result = split_nodes_link([node])

        self.assertEqual(result, [TextNode("link 1 ", TextType.TEXT),
                                  TextNode("alt", TextType.LINK, "url"),
                                  TextNode(" link 2 ", TextType.TEXT),
                                  TextNode("alt", TextType.LINK, "url"),
                                  TextNode(" more text", TextType.TEXT)])
    def test_multiple_link_nodes(self):
        nodes = [TextNode("This node has a [alt](url) link", TextType.TEXT),
                 TextNode("This node also has a link [alt](url)", TextType.TEXT)]
        result = split_nodes_link(nodes)

        self.assertEqual(result, [TextNode("This node has a ", TextType.TEXT),
                                  TextNode("alt", TextType.LINK, "url"),
                                  TextNode(" link", TextType.TEXT),
                                  TextNode("This node also has a link ", TextType.TEXT),
                                  TextNode("alt", TextType.LINK, "url")])


if __name__ == "__main__":
    unittest.main()
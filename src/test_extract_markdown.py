import unittest
from textnode import TextNode, TextType
from main import extract_markdown_images, extract_markdown_links

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "Here is image one ![image one](src/img/image_one.png)," \
            "and here is another image ![image two](src/img/image_two.png)"
        )
        self.assertEqual(matches, [("image one", "src/img/image_one.png"), ("image two", "src/img/image_two.png")])

    def test_no_markdown(self):
        matches = extract_markdown_images("sample text no markdown")
        self.assertEqual(matches, [])

    def test_no_markdown_link(self):
        matches = extract_markdown_links("sample text with no markdown")
        self.assertEqual(matches, [])
    
    def test_extract_markdown_link(self):
        matches = extract_markdown_links("[to boot dev](https://www.boot.dev)")
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev")])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("[link one](https://link.one) and another link [link two](https://link.two)")
        self.assertEqual(matches, [("link one", "https://link.one"), ("link two", "https://link.two")])

if __name__ == "__main__":
    unittest.main()
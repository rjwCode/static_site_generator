import unittest
from markdown_blocks import markdown_to_blocks

class TestMarkdownBlocks(unittest.TestCase):
    def testBasicMarkdown(self):
        md = """
    Here is some **bold** text

    Another paragraph with _italic_ text
    It even has a `code` section

    - list item 1
    - list item 2
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Here is some **bold** text",
                "Another paragraph with _italic_ text\nIt even has a `code` section",
                "- list item 1\n- list item 2"
            ]
        )

    def testMarkdownEmpty(self):
        md = ""
        with self.assertRaises(ValueError):
            markdown_to_blocks(md)
        
    def testManyNewlines(self):
        md = """
    This text has lots of newlines.
    




    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This text has lots of newlines."
            ])
        
    def testWhiteSpace(self):
        md = """

    Lots of whitespace here <--->
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Lots of whitespace here <--->"
            ]
        )
if __name__ == "__main__":
    unittest.main()
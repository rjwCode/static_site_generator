import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

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

class TestMDBlockType(unittest.TestCase):
    def testEmptyBlock(self):
        block = ""
        with self.assertRaises(ValueError):
            block_to_block_type(block)

    def testCodeBlock(self):
        block = "```\nthis is a code block\n```"
        result = block_to_block_type(block)
        
        self.assertEqual(result, BlockType.CODE)

    def testEmptyCodeBlock(self):
        block = "```\n\n\n```"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.CODE)

    def testQuoteBlock(self):
        block = ">\n>"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.QUOTE)

    def testHeadingBlock(self):
        block = "### heading text"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.HEADING)

    def testUnorderedList(self):
        block = "- item 1\n- item 2"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.UNORDERED_LIST)
    
    def testOrderedList(self):
        block = "1. item 1\n2. item 2"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.ORDERED_LIST)
    
    def testIncorrectOrderedList(self):
        block = "2. item 1\n1. item 2"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.PARAGRAPH)

    def testParagraph(self):
        block = "This is a paragraph"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
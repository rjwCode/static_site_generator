import unittest
from markdown_blocks import markdown_to_blocks, extract_title, block_to_block_type, markdown_to_html_node, BlockType
from htmlnode import HTMLNode

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

    def testParagraph(self):
        block = "This is a paragraph"
        result = block_to_block_type(block)

        self.assertEqual(result, BlockType.PARAGRAPH)

class TestMarkDownToHTML(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_empty_markdown(self):
        md = ""
        with self.assertRaises(ValueError):
            markdown_to_html_node(md)


    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_headings(self):
        md = """
    # Heading 1
    ## Heading 2
    ### Heading 3 with **bold**

    #### Heading 4
    ##### Heading 5
    ###### Heading 6 with some _italic_ text

    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3 with <b>bold</b></h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6 with some <i>italic</i> text</h6></div>"
        )

    def test_ordered_list(self):
        md = """
    1. Item 1
    2. Item 2

    3. Item 1 list 2
    4. Item 2 list 2


    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item 2</li></ol><ol><li>Item 1 list 2</li><li>Item 2 list 2</li></ol></div>"
        )
    
    def test_unordered_list(self):
        md = """
    - Item 1
    - Item 2

    - Item 3
    - Item 4

    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li></ul><ul><li>Item 3</li><li>Item 4</li></ul></div>"
        )
    
    def test_quote(self):
        md = """
    > This is a blockquote in Markdown.
    > It can span multiple lines.
    > 
    > It can even contain multiple paragraphs
    > if you include a blank line with a \">\" character.


    """
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><blockquote><p>This is a blockquote in Markdown. It can span multiple lines.</p>" \
            "<p>It can even contain multiple paragraphs if you include a blank line with a \">\" character.</p></blockquote></div>"
        )
    def test_mixed_content(self):
        md = """
    # Heading

    Paragraph with **bold** text.

    - List item 1
    - List item 2

    > A blockquote
    """
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>Paragraph with <b>bold</b> text.</p><ul><li>List item 1</li><li>List item 2</li></ul><blockquote><p>A blockquote</p></blockquote></div>"
        )

class TestExtractTitle(unittest.TestCase):
    def testEmptyMarkdown(self):
        markdown = ""
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def testNoH1Header(self):
        markdown = """
    ## This markdown has no H1 header

    So it _should_ raise a value error

    """
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def testProperMarkdown(self):
        markdown = """
    # This is an h1 header

    Here is some extra text
    """
        result = extract_title(markdown)

        self.assertEqual(result,
                         "This is an h1 header")


if __name__ == "__main__":
    unittest.main()
from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from main import text_node_to_html_node, text_to_textnodes
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(md_block):
    if md_block == None or md_block == "":
        raise ValueError("markdown block should not be blank")

    is_heading = is_code = is_paragraph = False
    is_ordered_list = is_quote = is_unordered_list = True

    lines = md_block.split("\n")

    first_line = lines[0]
    last_line = lines[-1]
    if re.match(r"^#{1,6} ", first_line):
        is_heading = True
    
    if first_line.startswith('```') and last_line == '```' and len(lines) >= 3:
        is_code = True

    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break

    for line in lines:
        if not line.startswith("- "):
            is_unordered_list = False
            break

    if is_code:
        return BlockType.CODE
    if is_heading:
        return BlockType.HEADING
    if is_quote:
        return BlockType.QUOTE
    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    

    for line in lines:
        if not re.match(r"^\d+\.\s", line):
            is_ordered_list = False

    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    if markdown == None or markdown == "":
        raise ValueError("No markdown was provided")
    result_list = []
    text = markdown
    text_blocks = text.split("\n\n")

    for block in text_blocks:
        stripped_block = block.strip()
        if not stripped_block:
            continue
        
        #checking for multiple heading lines
        lines = stripped_block.split("\n")
        current_subblock = []

        for line in lines:
            #check for a heading
            if line.strip().startswith('#'):
                if current_subblock:
                    clean_lines = [l.strip() for l in current_subblock]
                    clean_block = "\n".join(clean_lines)
                    result_list.append(clean_block)
                    current_subblock = []
                
                current_subblock.append(line.strip())
            else:
                current_subblock.append(line.strip())

        if current_subblock:
            clean_block = "\n".join(current_subblock)
            result_list.append(clean_block)
    
    return result_list

def markdown_to_html_node(markdown):
    #split the input markdown document into blocks
    blocks = markdown_to_blocks(markdown)
    
    #create parent html_node
    parent_html_node = ParentNode("div", [])
    children = []

    #raise ValueError for None of "" value in the input markdown
    if markdown == "" or len(markdown) <= 0 or markdown == None:
        raise ValueError("Invalid markdown... must not be empty or None")

    #iterate over blocks
    for block in blocks:
        #get the block type
        type = block_to_block_type(block)
        print(f"Block: {block!r}, Type: {type}")

        if type == BlockType.PARAGRAPH:
            #create paragraph html node
            paragraph_node = ParentNode("p", None)

            #replace newlines with spaces
            paragraph_text = block.replace("\n", " ")

            #process inline markdown
            paragraph_node.children = text_to_children(paragraph_text)
            children.append(paragraph_node)
        
        elif type == BlockType.HEADING:
            #get the heading level
            heading_level = determine_heading_level(block)

            header_text = block[heading_level:].lstrip()

            #create heading html node
            heading_node = ParentNode(f"h{heading_level}", None)

            #process inline markdown
            heading_node.children = text_to_children(header_text)
            children.append(heading_node)

        elif type == BlockType.CODE:
            #create the parent pre node
            pre_node = ParentNode("pre", None)
            code_node = LeafNode("code", None)

            #Remove the outer formatting: ```
            lines = block.split("\n")
            if len(lines) > 2:
                code_content = "\n".join(lines[1:-1]) + "\n"
            else:
                code_content = "" #not enough lines, the minimum is 3 for a code block
            
            code_node.value = code_content

            #set code_node as a child of the pre node
            pre_node.children = [code_node]

            #add pre node containing the code node to children
            children.append(pre_node)

        elif type == BlockType.QUOTE:
            #create the blockquote node
            quote_node = ParentNode("blockquote", [])

            cleaned_lines = []

            #strip '>' characters from each line
            lines = block.split("\n")
            current_paragraph = []
            paragraphs = []

            for line in lines:
                if line.startswith(">"):
                    clean_line = line[1:].lstrip()
                    if clean_line == "":
                        if current_paragraph:
                            paragraphs.append(" ".join(current_paragraph))
                            current_paragraph = []
                    else:
                        current_paragraph.append(clean_line)
                else:
                    #if the line doesn't have ">"
                    clean_line = line.strip()
                    if clean_line:
                        current_paragraph.append(clean_line)
            
            if current_paragraph:
                paragraphs.append(" ".join(current_paragraph))

            #creating paragraph nodes for each section of paragraph text within the blockquote
            #and adding them as children to the quote node
            for paragraph_text in paragraphs:
                paragraph_node = ParentNode("p", None)
                paragraph_node.children = text_to_children(paragraph_text)
                quote_node.children.append(paragraph_node)

            #adding the quote node as a child of the outer parent div node
            children.append(quote_node)

        elif type == BlockType.UNORDERED_LIST:
            #create the outer "ul" node
            ul_node = ParentNode("ul", None)

            #break the list into items and create a new list for li nodes
            items = block.split("\n")
            list_items = []

            #iterate over list items
            for item in items:
                if not item.strip():
                    continue

                #strip list marker and whitespace
                item_content = item.lstrip("- *+").lstrip()

                #create list item "li" node for this item
                li_node = ParentNode("li", None)

                #process inline markdown for each list item
                li_node.children = text_to_children(item_content)

                #add the list item node to the list
                list_items.append(li_node)
            
            #add all li nodes as children to the ul node
            ul_node.children = list_items

            #add the ul node to the overall parent node's children
            children.append(ul_node)

        elif type == BlockType.ORDERED_LIST:
            #create the outer ordered list node "ol"
            ol_node = ParentNode("ol", None)

            #break the list into items, and create a new list for li nodes
            items = block.split("\n")
            list_items = []

            #iterate over list items
            for item in items:
                if not item.strip():
                    continue #skip empty list items

                parts = item.split(". ", 1)
                if len(parts) > 1:
                    item_content = parts[1]
                else:
                    item_content = item
                
                #create a list item node for the item
                li_node = ParentNode("li", None)

                #process inline markdown for each list item
                li_node.children = text_to_children(item_content)

                #add the list item node to the list of li nodes
                list_items.append(li_node)

            #add all li_nodes as children of the ol node
            ol_node.children = list_items

            #add the ul node as a child of the overall parent node
            children.append(ol_node)

    if len(children) == 0:
        print("CHILDREN IS EMPTY FOR SOME REASON")
    parent_html_node.children = children
    return parent_html_node

def text_to_children(text):
    print(f"Processing text: {text!r}")
    text_nodes = text_to_textnodes(text)
    print(f"Resulting text_nodes: {text_nodes}")
    html_nodes = []

    #iterate over text_nodes and convert them to html_nodes
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        print(f"Converted text_node to html_node: {html_node}")
        html_nodes.append(html_node)
    
    print(f"Final html_nodes: {html_nodes}")
    return html_nodes

def determine_heading_level(block):
    #initialize level, and increment for each present #
    level = 0
    for char in block:
        if char == '#':
            level += 1
        else:
            break
    
    #ensure the level is within the appropriate range (1-6)
    level = max(1, min(level, 6))

    return level

from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(md_block):
    is_heading = is_code = is_quote = is_unordered_list = is_paragraph = False
    is_ordered_list = True

    headings = re.findall(r"#{1,6}\s{1}.*", md_block, re.M)
    code_blocks = re.findall(r"^```\n?.*\n?```$", md_block, re.M | re.DOTALL)
    quote_blocks = re.findall(r"^>", md_block, re.M | re.DOTALL)
    unordered_list_elements = re.findall(r"^-\s[\w(\w )]*", md_block, re.M | re.DOTALL)
    possibly_ordered_list = re.findall(r"^\d\.\s.*\n?", md_block, re.M | re.DOTALL)

    if len(code_blocks) > 0:
        is_code = True
        return BlockType.CODE
    if len(headings) > 0:
        is_heading = True
        return BlockType.HEADING
    if len(quote_blocks) > 0:
        is_quote = True
        return BlockType.QUOTE
    if len(unordered_list_elements) > 0:
        is_unordered_list = True
        return BlockType.UNORDERED_LIST
    
    list_index_to_match = 1
    for item in possibly_ordered_list:
        list_index = re.findall(r"^\d+", item)[0]
        if list_index != str(list_index_to_match):
            is_ordered_list = False
            break
        list_index_to_match += 1

    if is_ordered_list:
        return BlockType.ORDERED_LIST
    if not is_heading and not is_code and not is_quote and not is_unordered_list and not is_ordered_list:
        is_paragraph = True
        if is_paragraph:
            return BlockType.PARAGRAPH


test = "hello"
print(test[0])

def markdown_to_blocks(markdown):
    if markdown == None or markdown == "":
        raise ValueError("No markdown was provided")
    result_list = []
    text = markdown
    text_blocks = text.split("\n\n")
    for block in text_blocks:
        stripped_block = block.strip()
        if stripped_block:
            lines = stripped_block.split("\n")
            clean_lines = [line.strip() for line in lines]
            clean_block = "\n".join(clean_lines)
            result_list.append(clean_block)
    
    return result_list


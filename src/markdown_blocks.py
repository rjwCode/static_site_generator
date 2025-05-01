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
    
    for i, line in enumerate(lines, 1):
        if not line.startswith(f"{i}. "):
            is_ordered_list = False
            break

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
        if stripped_block:
            lines = stripped_block.split("\n")
            clean_lines = [line.strip() for line in lines]
            clean_block = "\n".join(clean_lines)
            result_list.append(clean_block)
    
    return result_list


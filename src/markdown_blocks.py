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


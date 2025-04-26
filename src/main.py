from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("incorrect text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node_list.append(node)
        else:
            new_node_list.extend(split_single_node(node.text, delimiter, text_type))

    return new_node_list

def split_single_node(text, delimiter, text_type):
    result = []
    start_delimiter = text.find(delimiter)
    if start_delimiter == -1:
        return [TextNode(text, TextType.TEXT)] if text else []
    end_delimiter = text.find(delimiter, start_delimiter + len(delimiter))
    if end_delimiter == -1:
        raise Exception("Invalid markdown format, closing delimiter missing")
    if start_delimiter > 0:
        result.append(TextNode(text[:start_delimiter], TextType.TEXT))
    result.append(TextNode(text[start_delimiter + len(delimiter):end_delimiter], text_type))
    
    remaining_text = text[end_delimiter + len(delimiter):]
    result.extend(split_single_node(remaining_text, delimiter, text_type))
    
    return result
    


            

def main():
    node = TextNode("This is some sample text", TextType.LINK, "https://www.boot.dev")
    sample_node = TextNode("looking for * chars in my text to make this work", TextType.TEXT)
    print(sample_node.text.find('*'))
    print(sample_node.text[12])
    print(sample_node.text.find('*', 13, len(sample_node.text)))

if __name__ == "__main__":
    main()
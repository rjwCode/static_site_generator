from enum import Enum
from htmlnode import LeafNode, ParentNode
import re

class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italics"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class TextNode():
	def __init__(self, text, text_type, url=None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
			return True
		else:
			return False
	
	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
	

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
        result.append(TextNode(text[:start_delimiter + len(delimiter)], TextType.TEXT))
        result.extend(split_single_node(text[start_delimiter + len(delimiter):], delimiter, text_type))
        return result
    if start_delimiter > 0:
        result.append(TextNode(text[:start_delimiter], TextType.TEXT))
    result.append(TextNode(text[start_delimiter + len(delimiter):end_delimiter], text_type))
    
    remaining_text = text[end_delimiter + len(delimiter):]
    result.extend(split_single_node(remaining_text, delimiter, text_type))
    
    return result

def split_nodes_image(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            split_nodes.append(node)
            continue

        current_text = node.text
        for alt, url in images:
            markdown_img = f"![{alt}]({url})"
            parts = current_text.split(markdown_img, 1)

            if parts[0]:
                split_nodes.append(TextNode(parts[0], TextType.TEXT))
            split_nodes.append(TextNode(alt, TextType.IMAGE, url))

            current_text = parts[1] if len(parts) > 1 else ""

        if current_text:
            split_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return split_nodes

    
def split_nodes_link(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            split_nodes.append(node)
            continue
        
        current_text = node.text
        for link_text, url in links:
            markdown_link = f"[{link_text}]({url})"
            parts = current_text.split(markdown_link, 1)
            if parts[0]:
                split_nodes.append(TextNode(parts[0], TextType.TEXT))
            split_nodes.append(TextNode(link_text, TextType.LINK, url))

            current_text = parts[1] if len(parts) > 1 else ""
        
        if current_text:
            split_nodes.append(TextNode(current_text, TextType.TEXT))
    
    return split_nodes



def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes
	


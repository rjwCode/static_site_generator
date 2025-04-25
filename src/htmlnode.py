
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props == None or self.props == {}:
            return ""
        props_string = ""
        for key in self.props.keys():
            props_string += f" {key}=\"{self.props[key]}\""
        return props_string
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None or self.value == "":
            raise ValueError("no value set")
        elif self.tag == None or self.tag == "":
            return f"{self.value}"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("No tag set")
        elif self.children == None or self.children == []:
            raise ValueError("No children set")
        else:
            child_nodes = ""
            for child in self.children:
                child_nodes += child.to_html()

            return f"<{self.tag}>{child_nodes}</{self.tag}>"


        
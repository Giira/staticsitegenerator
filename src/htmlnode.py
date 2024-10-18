class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    
    def to_html(self):
        raise NotImplementedError
    

    def props_to_html(self):
        if self.props is None:
            return ""
        else:
            html_string = ""
            for item in list(self.props.items()):
                html_string += f' {item[0]}="{item[1]}"'
            return html_string
        

    def __eq__(self, HTMLNode):
        if self.tag == HTMLNode.tag and self.value == HTMLNode.value and self.children == HTMLNode.children and self.props == HTMLNode.props:
            return True
        else:
            return False
    

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)
        self.tag = tag
        self.value = value
        self.props = props


    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: no value")
        elif self.tag == None:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children, props)

        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: no tag")
        if self.children is None:
            raise ValueError("Invalid HTML: no children")
        html_string = ""
        for node in self.children:
            html_string += node.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html_string}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
    
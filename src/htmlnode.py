class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    
    def to_html(self):
        raise NotImplementedError
    

    def props_to_html(self):
        html_string = ""
        for item in list(self.props.items()):
            html_string += f" {item[0]}={item[1]}"
        return html_string
    

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html})"
    
    
from htmlnode import LeafNode

class TextNode():
    
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    
    def __eq__(self, TextNode):
        if self.text == TextNode.text and self.text_type == TextNode.text_type and self.url == TextNode.url:
            return True
        else:
            return False
        
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(TextNode):
    if TextNode.text_type == "text_type_text":
        return LeafNode(None, TextNode.text)
    if TextNode.text_type == "text_type_bold":
        return LeafNode("b", TextNode.text)
    if TextNode.text_type == "text_type_italic":
        return LeafNode("i", TextNode.text)
    if TextNode.text_type == "text_type_code":
        return LeafNode("code", TextNode.text)
    if TextNode.text_type == "text_type_link":
        return LeafNode("a", TextNode.text, {"href": TextNode.url})
    if TextNode.text_type == "text_type_image":
        return LeafNode("img", "", {"src": TextNode.url, "alt": TextNode.text})
    raise Exception("Invalid text type")

    
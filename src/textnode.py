class Textnode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    
    def __eq__(self, Textnode):
        if self.text == Textnode.text and self.text_type == Textnode.text_type and self.url == Textnode.url:
            return True
        else:
            return False
        
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
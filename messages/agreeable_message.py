from messages.message import Message

class AgreeeableMessage(Message):
    def __init__(self, content: str):
        super().__init__("user", content)
    
    def get_for_llm(self):
        """Format agreeable message for Claude"""
        return super().get_for_llm()
    
    def get_for_display(self):
        """Human-readable output"""
        return super().get_for_display()
    
        
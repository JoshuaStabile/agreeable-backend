class Message:
    def __init__(self, role: str, content: str):
        self.role: str = role
        self.content: str = content
        
    def get_for_llm(self):
        """Format message for Claude"""
        return {"role": self.role, "content": self.content}
    
    def get_for_display(self):
        """Human-readable output"""
        return self.content

from messages.message import Message
import textwrap

class AgreeeableMessage(Message):
    def __init__(self, content: str, custom_prompt: str):
        super().__init__("user", content)
        self.custom_prompt = custom_prompt
        self.format_content()
    
    def get_for_llm(self):
        """Format agreeable message for Claude"""
        return super().get_for_llm()
    
    def get_for_display(self):
        """Human-readable output"""
        return super().get_for_display()
    
    def format_content(self):
        """Format the message into XML-style blocks"""
        self.content = textwrap.dedent(f"""\
        <custom-prompt>
        {self.custom_prompt.strip()}
        </custom-prompt>

        <document-text>
        {self.content.strip()}
        </document-text>
        """)
        
    
        
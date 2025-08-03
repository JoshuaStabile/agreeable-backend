from anthropic import Anthropic
from typing import List
from messages.message import Message
import config
import prompts

anthropic_client = Anthropic(
    api_key=config.ANTHROPIC_API_KEY,
)


def call_claude(messages: List[Message]) -> str:
    messages = [msg.get_for_llm() for msg in messages]

    response = anthropic_client.messages.create(
        model=config.LLM_MODEL,
        max_tokens=config.MAX_TOKENS,
        system=prompts.AGREEABLE_SYSTEM_PROMPT,
        
        messages=messages,
    )
    return response.content[0].text

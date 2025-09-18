from __future__ import annotations

import os
import sys
import shlex
import subprocess
from dataclasses import dataclass
from textwrap import dedent

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

OPENROUTER_KEY=os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_KEY:
    sys.exit("API key invalid!")

System_Prompt=dedent("""\
You are a professional developer specializing in shell commands and system administration tasks.
Your task is to generate the correct, safe, and efficient shell commands based on the user's request.
                     
Process:
1. Think: Use the 'think' function to explain your reasoning step by step.
2. Provide the final response command: Use the 'answer' function to present the final shell command.
""")

@dataclass
class Answer:
    success:bool
    cmd: str|None
    failure: str|None

agent=Agent(
    model = OpenAIChatModel(
    'qwen/qwen3-coder',
    provider=OpenRouterProvider(api_key=OPENROUTER_KEY)),
    system_prompt=System_Prompt,
    output_type=Answer
)

@agent.tool_plain
def think(msg:str):
    print(f"(AI model thinking):{msg}\n")

@agent.tool_plain
def answer(success:bool,cmd:str | None, failure:str|None):
    return Answer(success, cmd, failure)

def main():
    
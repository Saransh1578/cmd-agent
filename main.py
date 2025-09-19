from __future__ import annotations

import os
import sys
import shlex
import subprocess
from dataclasses import dataclass
from textwrap import dedent
from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

load_dotenv()

GEMINI_KEY=os.getenv("GEMINI_API_KEY")
if not GEMINI_KEY:
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
    model = GoogleModel(
    'gemini-2.5-flash',
    provider=GoogleProvider(api_key=GEMINI_KEY)),
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
    user_prompt=" ".join(sys.argv[1:])
    if not user_prompt:
        print("No prompt provided!")
        sys.exit(1)
    response=agent.run_sync(user_prompt)
    result: Answer=response.output

    if result.success and result.cmd:
        print(f"[AI answer]: {result.cmd}")
        confirm=input("Execute? (Y/N):").strip().lower()
        if confirm in {"y","yes","Y"}:
            subprocess.run(["powershell", "-Command", result.cmd], check=True)

            
    else:
        print(f"[AI Answer]: {result.failure or 'Failed to generate command'}")


if __name__=="__main__":
    main()
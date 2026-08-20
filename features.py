import os
import groq
import prompts
import sys

from dotenv import load_dotenv

load_dotenv()
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
default_model = "groq/compound-mini"

def llm_api_call(system_prompt: str, user_prompt_template: str, model: str = default_model):
    code = get_user_input()
    if not code.strip():
        print("No code detected, please try again.\n\n")
        return
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt.strip(),
                },
                {
                    "role": "user",
                    "content": user_prompt_template.format(code = code).strip(),
                },
            ],
        )
        print(response.choices[0].message.content + "\n\n")

    except groq.APIConnectionError:
        print("Error: Unable to connect to the API. Please check your connection and try again.\n\n")

    except groq.APITimeoutError:
        print("Error: Request timed out. Please try again later.\n\n")

    except groq.RateLimitError:
        print("Error: Limit exceeded. Please wait a moment and try again.\n\n")

    except Exception as e:
        print(f"An unexpected error occurred: {e}\n\n")

def get_user_input():
    print("Enter your code below.")
    print("Press Ctrl+D (macOS/Linux) or Ctrl+Z then Enter (Windows) when finished.\n\n")
    return sys.stdin.read()

def explain_code():
    llm_api_call(
        system_prompt=prompts.EXPLAIN_CODE.system_prompt,
        user_prompt_template=prompts.EXPLAIN_CODE.user_prompt_template,
    )

def find_bugs():
    llm_api_call(
        system_prompt=prompts.FIND_BUGS.system_prompt,
        user_prompt_template=prompts.FIND_BUGS.user_prompt_template,
    )

def improve_code():
    llm_api_call(
        system_prompt=prompts.IMPROVE_CODE.system_prompt,
        user_prompt_template=prompts.IMPROVE_CODE.user_prompt_template,
    )

def generate_tests():
    llm_api_call(
        system_prompt=prompts.GENERATE_TESTS.system_prompt,
        user_prompt_template=prompts.GENERATE_TESTS.user_prompt_template,
    )

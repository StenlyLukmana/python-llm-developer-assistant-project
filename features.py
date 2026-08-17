import os
import groq

from dotenv import load_dotenv

load_dotenv()
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
default_model = "llama-3.1-8b-instant"

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
    print("Type END on a new line when finished.\n\n")
    code_lines = []
    while True:
        user_input = input()
        if user_input.upper() == "END":
            break
        code_lines.append(user_input)

    return "\n".join(code_lines)

def explain_code():
    llm_api_call(
        system_prompt="""
        You are an expert Python teacher who explains code concisely to beginners.
        Your goal is to help the user understand how their code works.
        Do not rewrite code unless asked to.
        Avoid unnecessary terms and jargon.
        When you use it, explain it simply.
        """,   
        user_prompt_template="""
        Explain the following Python code.

        Requirements:
        - Summarize what it does.
        - Explain the important parts.
        - Identify potentially confusing parts.
        - Mention any potential issues, but do not focus on fixing. If there are no major issues, say so instead of inventing issues.
        - Use code snippets if they help make an explanation clearer.

        Code:
        {code}
        """
    )

def find_bugs():
    llm_api_call(
        system_prompt="""
        You are an expert Python code reviewer who specializes in finding bugs.
        Be precise, concise, focus on locating and fixing bugs.
        Do not claim that something is a bug unless there is a reasonable basis.
        Distinguish between actual bugs, potential problems, and style suggestions.
        """,
        user_prompt_template="""
        Analyze the following Python code for bugs and potential problems.
        
        If you don't find any obvious issues, say so rather than inventing issues.

        For each issue you find:
        - Identify the affected part of the code.
        - Explain why it is a problem.
        - Suggest a fix and explain why it fixes the issue.

        Code:
        {code}
        """
    )

def improve_code():
    llm_api_call(
        system_prompt="""
        You are an experienced Python developer helping improve code quality.
        Preserve the original behavior of the program unless a change is necessary.
        Prioritize readability, simplicity, maintainability, and best practices.
        """,   
        user_prompt_template="""
        Review the following Python code and suggest improvements.

        Focus on:
        - Readability
        - Simplicity
        - Python best practices
        - Function structure
        - Avoiding unnecessary code
        - Maintainability

        Code:
        {code}
        """
    )

def generate_tests():
    llm_api_call(
        system_prompt="""
        You are an experienced test engineer.
        Your job is to design tests that verify whether the Python code behaves correctly.
        Think about normal cases, edge cases, and invalid inputs.
        """,   
        user_prompt_template="""
        Generate tests cases for the following code.

        Requirements:
        - Identify the main behavior that should be tested.
        - Include normal cases, edge cases, and invalid inputs where appropriate.
        - Use pytest syntax.
        - Make each test focused on one behavior.
        - Briefly explain what each test verifies.
        - Do not modify the original code.

        Code:
        {code}
        """
    )

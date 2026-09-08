import os
import sys

from dotenv import load_dotenv
from groq import Groq, APIConnectionError, APITimeoutError, RateLimitError
from pydantic import ValidationError, BaseModel
from typing import Type, Optional

import prompts
import schemas

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
default_model = "openai/gpt-oss-120b"

def llm_api_call(
        system_prompt: str, 
        user_prompt_template: str, 
        response_model: Type[BaseModel],
        model: str = default_model, 
    ) -> tuple[BaseModel,None] | tuple[None, str]:
    code = get_user_input()
    if not code.strip():
        return None, "No code detected, please try again."
    
    try:
        response = client.chat.completions.create(
            model=model,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": response_model.__name__.lower(),
                    "schema": response_model.model_json_schema(),
                },
            },
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt_template.format(code = code).strip()},
            ],
        )

        raw_json = response.choices[0].message.content
        return response_model.model_validate_json(raw_json), None

    except (APIConnectionError, APITimeoutError, RateLimitError) as e:
        return None, f"Network error communicating with Groq: {e}"
    except ValidationError as e:
        err_details = "\n".join([f"- Field '{'->'.join(str(x) for x in error['loc'])}': {error['msg']}" for error in e.errors()])
        return None, f"[Pydantic caught {e.error_count()} validation error(s)!]\n{err_details}"
    except Exception as e:
        return None, f"An unexpected error occurred: {e}\n\n"

def get_user_input() -> str:
    print("Enter your code below.")
    print("Press Ctrl+D (macOS/Linux) or Ctrl+Z then Enter (Windows) when finished.\n\n")
    return sys.stdin.read()

def explain_code():
    report, error = llm_api_call(
        system_prompt=prompts.EXPLAIN_CODE.system_prompt,
        user_prompt_template=prompts.EXPLAIN_CODE.user_prompt_template,
        response_model=schemas.ExplainCodeReport,
    )

    if error:
        print(f"Error: {error}\n")
        return

    print("================")
    print("CODE EXPLANATION")
    print("================")
    print("\n=== Summary ===")
    print(f"{report.summary}\n")

    print("\n=== Key Highlights ===")
    for snippet in report.important_parts:
        print(f"--> [{snippet.snippet}]: {snippet.explanation}\n")

    if report.potential_issues:
        print("\n=== Potential Concerns ===")
        for issue in report.potential_issues:
            print(f"--> [{issue.snippet}]: {issue.explanation}\n")

    print("")


def find_bugs():
    report, error = llm_api_call(
        system_prompt=prompts.FIND_BUGS.system_prompt,
        user_prompt_template=prompts.FIND_BUGS.user_prompt_template,
        response_model=schemas.FindBugsReport,
    )

    if error:
        print(f"Error: {error}\n")
        return

    print("==========")
    print("BUG REPORT")
    print("==========")
    if report.issues:
        for issue in report.issues:
            print(f"--> [{issue.issue_type.upper()}] At Line {issue.line_number}: {issue.problem}")
            print(f"Explanation: {issue.explanation}")
            print(f"Fix: {issue.fix}")
            print(f"    {issue.fix_implementation}\n")
        print("\n=== Corrected Code ===")
        print(f"{report.corrected_code}\n")
    else:
        print("No bugs found")

    print("")


def improve_code():
    report, error = llm_api_call(
        system_prompt=prompts.IMPROVE_CODE.system_prompt,
        user_prompt_template=prompts.IMPROVE_CODE.user_prompt_template,
        response_model=schemas.ImproveCodeReport,
    )

    if error:
        print(f"Error: {error}\n")
        return

    print("=========================")
    print("IMPROVEMENT SUGGESTION(S)")
    print("=========================")
    if report.improvements:
        for improvement in report.improvements:
            print(f"--> [{improvement.improvement_type.upper()}] At Line {improvement.line_number}: {improvement.problem}")
            print(f"Explanation: {improvement.explanation}")
            print(f"Improvement: {improvement.improvement}")
            print(f"    {improvement.improvement_implementation}\n")
    else:
        print("No improvements needed")
    if report.improved_code:
        print("\n=== Improved Code ===")
        print(f"{report.improved_code}\n")
    print("")


def generate_tests():
    report, error = llm_api_call(
        system_prompt=prompts.GENERATE_TESTS.system_prompt,
        user_prompt_template=prompts.GENERATE_TESTS.user_prompt_template,
        response_model=schemas.GenerateTestsReport,
    )

    if error:
        print(f"Error: {error}\n")
        return

    print("============")
    print("TEST CASE(S)")
    print("============")
    for test in report.tests:
        print(f"--> [{test.description}]")
        print(f"Purpose: {test.purpose}")
        print(f"    {test.test_code}\n")
    print("")

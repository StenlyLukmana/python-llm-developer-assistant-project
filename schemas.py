from pydantic import BaseModel, Field
from typing import Literal, List

'''
explain_code()
'''
class CodeSnippetExplanation(BaseModel):
    explanation_type: Literal["important_part", "potential_issue"] = Field(description="CLassification of the code explanation(s)")
    snippet: str = Field(description="Code snippet of important part or potential issue")
    explanation: str = Field(description="Explanation of important part or potential issue")

class ExplainCodeReport(BaseModel):
    summary: str = Field(description="Summary of what the code does and how it works")
    important_parts: List[CodeSnippetExplanation] = Field(description="List of important parts of the code")
    potential_issues: List[CodeSnippetExplanation] = Field(description="List of potential issues")



'''
find_bugs()
'''
class CodeIssue(BaseModel):
    issue_type: Literal["bug", "potential_problem"] = Field(description="Classification of the issue(s)")
    line_number: int = Field(description="Exact 1-based line number where the issue occurs")
    problem: str = Field(description="Short summary of the issue")
    explanation: str = Field(description="Detailed explanation of why this is an issue")
    fix: str = Field(description="Remediation step")
    fix_implementation: str = Field(description="Corrected code snippet")

class FindBugsReport(BaseModel):
    issues: List[CodeIssue] = Field(description="List of found issue(s)")
    corrected_code: str = Field(description="Corrected code block")



'''
improve_code()
'''
class CodeImprovement(BaseModel):
    improvement_type: Literal["readability", "simplicity", "best_practice", "maintainability", "functionality"] = Field(description="Classification of the improvement(s)")
    line_number: int = Field(description="Exact 1-based line number where the issue occurs")
    problem: str = Field(description="Short summary of the issue")
    explanation: str = Field(description="Detailed explanation of why this needs to be improved")
    improvement: str = Field(description="Improvement step")
    imrpovement_implementation: str = Field(description="Imrpoved code snippet")

class ImproveCodeReport(BaseModel):
    improvements: List[CodeImprovement] = Field(description="List of suggested improvement(s)")
    improved_code: str = Field(description="Improved code block")



'''
generate_tests()
'''
class TestingCode(BaseModel):
    description: str = Field(description="Short summary of the purpose of the test")
    purpose: str = Field(description="Detailed explanation of the behavior being tested and what the test is trying to verify")
    test_code: str = Field(description="Code for the test case")

class GenerateTestsReport(BaseModel):
    tests: List[TestingCode] = Field(description="List of test(s)")
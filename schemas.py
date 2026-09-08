from pydantic import BaseModel, Field
from typing import Literal, List, Optional

'''
explain_code()
'''
class CodeSnippetExplanation(BaseModel):
    snippet: str = Field(description="Code snippet of important part or potential issue")
    explanation: str = Field(description="Explanation of important part or potential issue")

class ExplainCodeReport(BaseModel):
    summary: str = Field(description="Summary of what the code does and how it works")
    important_parts: List[CodeSnippetExplanation] = Field(description="List of important parts of the code")
    potential_issues: List[CodeSnippetExplanation] = Field(
        default=[], 
        description="List of potential issues, leave empty if no issues are found",
    )



'''
find_bugs()
'''
class CodeIssue(BaseModel):
    issue_type: Literal["bug", "potential_problem"] = Field(description="Classification of the issue")
    line_number: int = Field(description="Exact 1-based line number where the issue occurs")
    problem: str = Field(description="Short summary of the issue")
    explanation: str = Field(description="Detailed explanation of why this is an issue")
    fix: str = Field(description="Remediation step")
    fix_implementation: str = Field(description="Corrected code snippet")

class FindBugsReport(BaseModel):
    issues: List[CodeIssue] = Field(
        default=[],
        description="List of found issues, leave empty if no issues are found",
    )
    corrected_code: Optional[str] = Field(
        default=None, 
        description="Corrected code block, must be null if no issues are found",
    )



'''
improve_code()
'''
class CodeImprovement(BaseModel):
    improvement_type: Literal["simplicity", "best_practice", "maintainability"] = Field(description="Classification of the improvement")
    line_number: int = Field(description="Exact 1-based line number where the issue occurs")
    problem: str = Field(description="Short summary of the issue")
    explanation: str = Field(description="Detailed explanation of why this needs to be improved")
    improvement: str = Field(description="Improvement step")
    improvement_implementation: str = Field(description="Improved code snippet")

class ImproveCodeReport(BaseModel):
    improvements: List[CodeImprovement] = Field(
        default=[],
        description="List of suggested improvements, leave empty if no issues are found",
    )
    improved_code: Optional[str] = Field(
        default=None,
        description="Improved code block, must be null if no issues are found",
    )



'''
generate_tests()
'''
class TestingCode(BaseModel):
    test_type: Literal["normal", "edge_case", "invalid_input"] = Field(description="Classification of the test")
    description: str = Field(description="Short summary of the purpose of the test")
    purpose: str = Field(description="Detailed explanation of the behavior being tested and what the test is trying to verify")
    test_code: str = Field(description="Code for the test case")

class GenerateTestsReport(BaseModel):
    tests: List[TestingCode] = Field(description="List of tests")
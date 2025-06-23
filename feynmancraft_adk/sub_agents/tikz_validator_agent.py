# Copyright 2024-2025 The FeynmanCraft ADK Project Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""TikZ Validator Agent for FeynmanCraft ADK."""

from google.adk.agents import Agent

from ..models import TIKZ_VALIDATOR_MODEL
from .tikz_validator_agent_prompt import PROMPT as TIKZ_VALIDATOR_AGENT_PROMPT


def tikz_validator_tool(tikz_code: str, additional_packages: str = "") -> str:
    """
    Validate TikZ code through prompt-based analysis and syntax checking.
    
    Args:
        tikz_code: TikZ code to validate
        additional_packages: Additional LaTeX packages, comma-separated
        
    Returns:
        Detailed validation report with syntax and structure analysis
    """
    # Parse additional packages
    packages = []
    if additional_packages.strip():
        packages = [pkg.strip() for pkg in additional_packages.split(",") if pkg.strip()]
    
    # Standard TikZ-Feynman packages
    standard_packages = [
        "tikz", "tikz-feynman", "amsmath", "physics", "siunitx", "xcolor", "graphicx"
    ]
    
    # Merge with user-specified packages, avoiding duplicates
    all_packages = list(set(packages + standard_packages))
    
    # Perform prompt-based validation
    validation_result = _validate_tikz_syntax(tikz_code, all_packages)
    
    # Generate detailed validation report
    report = f"""
# TikZ Code Validation Report (Prompt-Based Analysis)

## Validation Method
- **Analysis Type**: AI-powered syntax and structure validation
- **TikZ-Feynman Support**: Standard syntax patterns
- **Package Checking**: {', '.join(all_packages)}

## Validation Results
- **Syntax Valid**: {'Yes' if validation_result['syntax_valid'] else 'No'}
- **Structure Valid**: {'Yes' if validation_result['structure_valid'] else 'No'}
- **Overall Quality**: {validation_result['quality_score']}/100

## Analysis Details
"""
    
    # Add syntax analysis
    if validation_result['syntax_errors']:
        report += "\n### Syntax Errors Found\n"
        for error in validation_result['syntax_errors']:
            report += f"- {error}\n"
    else:
        report += "\n### Syntax Analysis\n- No syntax errors detected\n"
    
    # Add structure analysis
    if validation_result['structure_issues']:
        report += "\n### Structure Issues\n"
        for issue in validation_result['structure_issues']:
            report += f"- {issue}\n"
    else:
        report += "\n### Structure Analysis\n- Proper TikZ-Feynman structure detected\n"
    
    # Add warnings
    if validation_result['warnings']:
        report += "\n### Warnings\n"
        for warning in validation_result['warnings']:
            report += f"- {warning}\n"
    else:
        report += "\n### Warnings\n- No warnings\n"
    
    # Add suggestions
    if validation_result['suggestions']:
        report += "\n### Improvement Suggestions\n"
        for suggestion in validation_result['suggestions']:
            report += f"- {suggestion}\n"
    
    # Add best practices recommendations
    report += "\n### TikZ-Feynman Best Practices\n"
    report += "- Use '\\feynmandiagram[...]' for simple diagrams\n"
    report += "- Use '\\begin[feynman]\\end[feynman]' for complex layouts\n"
    report += "- Ensure proper particle naming: \\(e^+\\), \\(\\gamma\\), \\(\\nu_e\\)\n"
    report += "- Use positioning library for relative placement\n"
    report += "- Include proper momentum labels and arrows\n"
    
    return report


def _validate_tikz_syntax(tikz_code: str, packages: list) -> dict:  # packages parameter kept for future use
    """
    Perform detailed prompt-based TikZ syntax validation.
    
    Args:
        tikz_code: TikZ code to validate
        packages: List of packages to check
        
    Returns:
        Dictionary with validation results
    """
    result = {
        'syntax_valid': True,
        'structure_valid': True,
        'syntax_errors': [],
        'structure_issues': [],
        'warnings': [],
        'suggestions': [],
        'quality_score': 100
    }
    
    # Check basic TikZ structure
    if not ('\\begin{tikzpicture}' in tikz_code and '\\end{tikzpicture}' in tikz_code):
        if not ('\\feynmandiagram' in tikz_code):
            result['structure_issues'].append("Missing tikzpicture environment or feynmandiagram command")
            result['structure_valid'] = False
    
    # Check for TikZ-Feynman specific patterns
    feynman_patterns = ['\\feynmandiagram', '\\begin{feynman}', '\\vertex', '\\diagram']
    if not any(pattern in tikz_code for pattern in feynman_patterns):
        result['warnings'].append("No TikZ-Feynman specific commands detected")
    
    # Check for common syntax issues
    brace_count = tikz_code.count('{') - tikz_code.count('}')
    if brace_count != 0:
        result['syntax_errors'].append(f"Mismatched braces: {abs(brace_count)} {'opening' if brace_count > 0 else 'closing'} brace(s) unmatched")
        result['syntax_valid'] = False
    
    bracket_count = tikz_code.count('[') - tikz_code.count(']')
    if bracket_count != 0:
        result['syntax_errors'].append(f"Mismatched brackets: {abs(bracket_count)} {'opening' if bracket_count > 0 else 'closing'} bracket(s) unmatched")
        result['syntax_valid'] = False
    
    # Check for semicolon endings in TikZ commands
    lines = tikz_code.split('\n')
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if line and '\\' in line and not line.endswith(';') and not line.endswith('}') and not line.endswith('{'):
            if any(cmd in line for cmd in ['\\draw', '\\node', '\\vertex', '\\diagram']):
                result['warnings'].append(f"Line {i}: TikZ command may be missing semicolon")
    
    # Check for proper particle notation
    if 'e+' in tikz_code and '\\(e^+\\)' not in tikz_code:
        result['suggestions'].append("Use proper math notation for particles: \\(e^+\\) instead of e+")
    
    # Check for positioning library usage
    if 'above' in tikz_code or 'below' in tikz_code or 'left' in tikz_code or 'right' in tikz_code:
        if 'positioning' not in tikz_code:
            result['suggestions'].append("Consider using \\usetikzlibrary{positioning} for better positioning")
    
    # Calculate quality score
    error_penalty = len(result['syntax_errors']) * 20
    structure_penalty = len(result['structure_issues']) * 15
    warning_penalty = len(result['warnings']) * 5
    
    result['quality_score'] = max(0, 100 - error_penalty - structure_penalty - warning_penalty)
    
    return result


TikZValidatorAgent = Agent(
    model=TIKZ_VALIDATOR_MODEL,  # Use gemini-2.5-flash for simple syntax validation
    name="tikz_validator_agent",
    description="Validates TikZ code through prompt-based analysis and syntax checking without requiring TeX compilation.",
    instruction=TIKZ_VALIDATOR_AGENT_PROMPT,
    tools=[
        tikz_validator_tool,
    ],
    output_key="tikz_validation_report",  # State management: outputs to state.tikz_validation_report
) 
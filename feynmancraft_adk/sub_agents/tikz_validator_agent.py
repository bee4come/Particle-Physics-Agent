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

from .. import MODEL
from ..tools import validate_tikz_compilation
from .tikz_validator_agent_prompt import PROMPT as TIKZ_VALIDATOR_AGENT_PROMPT


def tikz_validator_tool(tikz_code: str, additional_packages: str = "") -> str:
    """
    Validate TikZ code compilation.
    
    Args:
        tikz_code: TikZ code to validate
        additional_packages: Additional LaTeX packages, comma-separated
        
    Returns:
        Detailed validation report
    """
    # Parse additional packages
    packages = []
    if additional_packages.strip():
        packages = [pkg.strip() for pkg in additional_packages.split(",") if pkg.strip()]
    
    # Use LaTeX compiler to validate code
    result = validate_tikz_compilation(tikz_code, packages)
    
    # Generate detailed validation report
    report = f"""
# TikZ Code Validation Report

## Compilation Status
- **Compilation Success**: {'Yes' if result['success'] else 'No'}
- **PDF Generated**: {'Yes' if result['pdf_generated'] else 'No'}
- **Return Code**: {result.get('return_code', 'N/A')}

## Analysis Results
"""
    
    if 'analysis' in result:
        analysis = result['analysis']
        report += f"""
- **Error Type**: {analysis.get('error_type', 'None')}
- **Quality Score**: {analysis.get('quality_score', 0)}/100

### Detected Errors
"""
        for error in analysis.get('errors', []):
            report += f"- {error}\n"
        
        if not analysis.get('errors'):
            report += "- No compilation errors\n"
            
        report += "\n### Warnings\n"
        for warning in analysis.get('warnings', []):
            report += f"- {warning}\n"
            
        if not analysis.get('warnings'):
            report += "- No warnings\n"
            
        report += "\n### Suggestions\n"
        for suggestion in analysis.get('suggestions', []):
            report += f"- {suggestion}\n"
    
    # Add compilation output (if there are errors)
    if not result['success'] and 'error' in result:
        report += f"\n## Error Information\n```\n{result['error']}\n```\n"
    
    if result.get('stderr'):
        report += f"\n## Standard Error Output\n```\n{result['stderr']}\n```\n"
    
    return report


TikZValidatorAgent = Agent(
    model=MODEL,
    name="tikz_validator_agent",
    description="Validates TikZ code compilation using local TeX Live.",
    instruction=TIKZ_VALIDATOR_AGENT_PROMPT,
    tools=[
        tikz_validator_tool,
    ],
    output_key="tikz_validation_report",  # State management: outputs to state.tikz_validation_report
) 
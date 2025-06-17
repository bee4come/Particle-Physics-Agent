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

"""
Code Agent for FeynmanCraft ADK.
This agent is responsible for securely executing Python code snippets
for physics rule validation.
"""

import subprocess
import tempfile
import os
from typing import Dict, Any, List

from google.adk.agents import Agent

from .. import MODEL


async def execute_python_code(code: str) -> Dict[str, Any]:
    """
    Executes a string of Python code in a secure, isolated subprocess.

    Args:
        code: The Python code string to execute.

    Returns:
        A dictionary with the execution result.
    """
    try:
        # Create a temporary file to safely execute the provided code.
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name

        # Execute the code in a subprocess and capture the output.
        result = subprocess.run(
            ["python", temp_file_path],
            capture_output=True,
            text=True,
            timeout=15,  # 15-second timeout for security
        )

    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": "Code execution timed out (>15 seconds).",
            "error": "TimeoutError",
            "success": False,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"An unexpected error occurred before execution: {e}",
            "error": "PreExecutionError",
            "success": False,
        }
    finally:
        # Ensure the temporary file is always cleaned up.
        if "temp_file_path" in locals() and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

    if result.returncode == 0:
        # Successfully executed. Try to parse stdout as a float.
        try:
            output_value = float(result.stdout.strip())
            return {
                "status": "success",
                "output": output_value,
                "raw_stdout": result.stdout.strip(),
                "error": "",
                "success": True,
            }
        except ValueError:
            # Output was not a number, return it as a string.
            return {
                "status": "success",
                "output": result.stdout.strip(),
                "raw_stdout": result.stdout.strip(),
                "error": "Output is not a numeric value.",
                "success": True, # The code ran, so success is true.
            }
    else:
        # Code execution failed.
        return {
            "status": "error",
            "message": "Code execution failed with a non-zero exit code.",
            "error": result.stderr.strip(),
            "success": False,
        }


CodeAgent = Agent(
    name="code_agent",
    model=MODEL, # Using a capable model for potential future code-gen tasks.
    description="Generates and executes Python code for physics calculations in a secure environment.",
    instruction="""You are a powerful and secure code-generating agent.
Your primary function is to write and execute Python code to perform calculations based on physics rules.

**Workflow:**

1.  **Receive a Task**: You will be given a task, typically including a `code_spec` from a physics rule and the specific `inputs` values for the current calculation. The `code_spec` contains a `template` (a reference implementation), a list of `inputs`, and an `output` description.

2.  **Generate Code**: Your most important job is to **write Python code** that correctly implements the logic from the `code_spec`.
    -   The `template` in the `code_spec` is a reference. You should understand its logic, but you **can and should write your own, more robust code**.
    -   Your generated code must use the variable names provided in the `inputs`.
    -   The final line of your code **must be a `print()` statement** that outputs the calculated result.

3.  **Execute Code**: Once you have generated the code, you MUST use the `execute_python_code` tool to run it. Pass the complete, generated code string to the tool.

4.  **Return the Result**: The tool will return a JSON object with the execution result. Return this JSON object directly to the calling agent.
""",
    tools=[execute_python_code],
) 
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

"""LaTeX compilation tools for TikZ validation."""

import os
import subprocess
import tempfile
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple


logger = logging.getLogger(__name__)


class LaTeXCompiler:
    """LaTeX compiler for TikZ-Feynman diagrams."""
    
    def __init__(self, tex_command: str = "pdflatex", working_dir: Optional[str] = None):
        """
        Initialize LaTeX compiler.
        
        Args:
            tex_command: LaTeX command to use (pdflatex, lualatex, xelatex)
            working_dir: Working directory for compilation (None for temp dir)
        """
        self.tex_command = tex_command
        self.working_dir = working_dir
        self._check_tex_installation()
    
    def _check_tex_installation(self):
        """Check if TeX Live is installed and accessible."""
        try:
            result = subprocess.run(
                [self.tex_command, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode != 0:
                raise RuntimeError(f"TeX command {self.tex_command} not found")
            logger.info(f"TeX Live detected: {result.stdout.split(chr(10))[0]}")
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            raise RuntimeError(f"TeX Live not found or not accessible: {e}")
    
    def compile_tikz(self, tikz_code: str, packages: Optional[List[str]] = None) -> Dict:
        """
        Compile TikZ code and return validation results.
        
        Args:
            tikz_code: TikZ code to validate
            packages: Additional LaTeX packages to include
            
        Returns:
            Dictionary containing compilation results
        """
        # Create full LaTeX document
        full_document = self.create_full_document(tikz_code, packages)
        
        # Create temporary directory for compilation
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            tex_file = temp_path / "diagram.tex"
            
            # Write LaTeX file
            tex_file.write_text(full_document, encoding='utf-8')
            
            # Compile with pdflatex
            result = self._run_compilation(tex_file)
            
            return result
    
    def create_full_document(self, tikz_code: str, packages: Optional[List[str]] = None) -> str:
        """Create a complete LaTeX document from TikZ code."""
        if packages is None:
            packages = []
        
        # Default packages for TikZ-Feynman
        default_packages = [
            "tikz",
            "tikz-feynman",
            "amsmath",
            "amssymb",
            "physics"
        ]
        
        all_packages = default_packages + [pkg for pkg in packages if pkg not in default_packages]
        
        # Create document template
        document = f"""\\documentclass{{article}}
\\usepackage[margin=1cm]{{geometry}}
\\usepackage{{xcolor}}
"""
        
        # Add packages
        for package in all_packages:
            document += f"\\usepackage{{{package}}}\n"
        
        # TikZ libraries
        document += """
\\usetikzlibrary{arrows.meta}
\\usetikzlibrary{decorations.markings}
\\usetikzlibrary{calc}
\\usetikzlibrary{positioning}

\\begin{document}
\\thispagestyle{empty}

"""
        
        # Add TikZ code
        if not tikz_code.strip().startswith("\\begin{tikzpicture}"):
            # Wrap bare feynmandiagram in tikzpicture if needed
            if "\\feynmandiagram" in tikz_code:
                document += "\\begin{tikzpicture}\n"
                document += tikz_code
                document += "\n\\end{tikzpicture}\n"
            else:
                document += tikz_code
        else:
            document += tikz_code
        
        document += "\n\\end{document}"
        
        return document
    
    def _run_compilation(self, tex_file: Path) -> Dict:
        """Run LaTeX compilation and analyze results."""
        work_dir = tex_file.parent
        
        try:
            # Run pdflatex twice for proper references
            for run_num in range(2):
                result = subprocess.run(
                    [
                        self.tex_command,
                        "-interaction=nonstopmode",
                        "-output-directory", str(work_dir),
                        str(tex_file)
                    ],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=work_dir
                )
                
                if run_num == 1:  # Analyze only the final run
                    final_result = result
            
            # Check if PDF was generated
            pdf_file = work_dir / (tex_file.stem + ".pdf")
            pdf_generated = pdf_file.exists()
            
            # Parse log file for detailed error analysis
            log_file = work_dir / (tex_file.stem + ".log")
            log_content = ""
            if log_file.exists():
                log_content = log_file.read_text(encoding='utf-8', errors='ignore')
            
            # Analyze compilation results
            analysis = self._analyze_compilation_output(
                final_result.stdout,
                final_result.stderr,
                log_content,
                pdf_generated
            )
            
            return {
                "success": pdf_generated and final_result.returncode == 0,
                "pdf_generated": pdf_generated,
                "return_code": final_result.returncode,
                "stdout": final_result.stdout,
                "stderr": final_result.stderr,
                "log_content": log_content,
                "analysis": analysis,
                "pdf_path": str(pdf_file) if pdf_generated else None
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "pdf_generated": False,
                "error": "Compilation timeout (>30 seconds)",
                "analysis": {
                    "error_type": "timeout",
                    "suggestions": ["Check for infinite loops in TikZ code", "Simplify the diagram"]
                }
            }
        except Exception as e:
            return {
                "success": False,
                "pdf_generated": False,
                "error": f"Compilation failed: {str(e)}",
                "analysis": {
                    "error_type": "system_error",
                    "suggestions": ["Check TeX Live installation", "Verify file permissions"]
                }
            }
    
    def _analyze_compilation_output(self, stdout: str, stderr: str, log_content: str, pdf_generated: bool) -> Dict:
        """Analyze LaTeX compilation output for detailed error reporting."""
        analysis = {
            "error_type": None,
            "errors": [],
            "warnings": [],
            "suggestions": [],
            "quality_score": 0
        }
        
        # Common error patterns
        error_patterns = {
            "undefined_command": [
                r"Undefined control sequence",
                r"Unknown command"
            ],
            "missing_package": [
                r"File.*not found",
                r"Package.*not found"
            ],
            "syntax_error": [
                r"Missing.*inserted",
                r"Extra.*ignored",
                r"Paragraph ended before"
            ],
            "tikz_error": [
                r"Package tikz Error",
                r"Package pgf Error"
            ],
            "feynman_error": [
                r"tikz-feynman.*error",
                r"feynmandiagram.*error"
            ]
        }
        
        # Search for errors in log content
        for error_type, patterns in error_patterns.items():
            for pattern in patterns:
                import re
                if re.search(pattern, log_content, re.IGNORECASE):
                    analysis["error_type"] = error_type
                    analysis["errors"].append(f"{error_type}: Pattern '{pattern}' found")
        
        # Check for warnings
        warning_patterns = [
            r"Warning:",
            r"LaTeX Warning:",
            r"Package.*Warning"
        ]
        
        for pattern in warning_patterns:
            import re
            matches = re.findall(pattern + r".*", log_content, re.IGNORECASE)
            analysis["warnings"].extend(matches[:5])  # Limit to 5 warnings
        
        # Generate suggestions based on error type
        if analysis["error_type"]:
            analysis["suggestions"] = self._get_error_suggestions(analysis["error_type"])
        
        # Calculate quality score
        if pdf_generated:
            analysis["quality_score"] = 100 - len(analysis["warnings"]) * 5
            if analysis["quality_score"] < 0:
                analysis["quality_score"] = 0
        
        return analysis
    
    def _get_error_suggestions(self, error_type: str) -> List[str]:
        """Get suggestions based on error type."""
        suggestions = {
            "undefined_command": [
                "Check TikZ-Feynman command syntax",
                "Ensure all required packages are loaded",
                "Verify particle and vertex naming conventions"
            ],
            "missing_package": [
                "Install missing LaTeX packages",
                "Check TeX Live installation",
                "Add missing \\usepackage declarations"
            ],
            "syntax_error": [
                "Check bracket and brace matching",
                "Verify TikZ syntax compliance",
                "Review coordinate specifications"
            ],
            "tikz_error": [
                "Check TikZ library requirements",
                "Verify coordinate calculations",
                "Review path specifications"
            ],
            "feynman_error": [
                "Check tikz-feynman syntax",
                "Verify particle types and properties",
                "Review diagram layout specifications"
            ]
        }
        
        return suggestions.get(error_type, ["Review LaTeX compilation log for details"])


def validate_tikz_compilation(tikz_code: str, packages: Optional[List[str]] = None) -> Dict:
    """
    Convenience function to validate TikZ code compilation.
    
    Args:
        tikz_code: TikZ code to validate
        packages: Additional packages to include
        
    Returns:
        Validation results dictionary
    """
    compiler = LaTeXCompiler()
    return compiler.compile_tikz(tikz_code, packages) 
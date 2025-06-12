import os
import subprocess
import tempfile
from typing import Tuple, Optional

DEFAULT_TEX_TEMPLATE = """
\\documentclass{standalone}
\\usepackage{tikz}
% Add any other necessary TikZ libraries or custom preamble here
% e.g., \\usetikzlibrary{arrows,shapes,automata,positioning,calc,patterns,decorations.pathmorphing,decorations.markings}
\\begin{document}
{tikz_code}
\\end{document}
"""

def compile_tikz_code(
    tikz_code: str,
    latex_executable: str = "pdflatex",
    timeout_seconds: int = 30,
    template: str = DEFAULT_TEX_TEMPLATE
) -> Tuple[bool, str, Optional[bytes]]:
    """
    Compiles a string of TikZ code into a PDF using a LaTeX compiler.

    Args:
        tikz_code: The TikZ code string to compile (contents of tikzpicture environment).
        latex_executable: The LaTeX compiler to use (e.g., "pdflatex", "lualatex").
        timeout_seconds: Maximum time allowed for compilation.
        template: The LaTeX document template to use. Must contain "{tikz_code}".

    Returns:
        A tuple (success: bool, log: str, pdf_content: Optional[bytes]).
        - success: True if compilation was successful, False otherwise.
        - log: The combined stdout and stderr from the LaTeX compiler.
        - pdf_content: The binary content of the generated PDF if successful, else None.
    """
    if not isinstance(tikz_code, str):
        return False, "TikZ code must be a string.", None

    full_tex_code = template.format(tikz_code=tikz_code)

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_filename = "main.tex"
        pdf_filename = "main.pdf"
        tex_filepath = os.path.join(tmpdir, tex_filename)
        pdf_filepath = os.path.join(tmpdir, pdf_filename)

        with open(tex_filepath, "w", encoding="utf-8") as f:
            f.write(full_tex_code)

        command = [
            latex_executable,
            "-interaction=nonstopmode",
            "-output-directory=" + tmpdir, # Ensure output goes to tmpdir
            tex_filename,
        ]

        try:
            proc = subprocess.run(
                command,
                cwd=tmpdir,  # Run from tmpdir to find main.tex
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                encoding="utf-8",
                errors="replace" # Handle potential encoding errors in logs
            )
            success = proc.returncode == 0
            log_output = proc.stdout + "\n" + proc.stderr

            if success and os.path.exists(pdf_filepath):
                with open(pdf_filepath, "rb") as pf:
                    pdf_bytes = pf.read()
                return True, log_output, pdf_bytes
            else:
                return False, log_output, None

        except FileNotFoundError:
            return False, f"{latex_executable} not found. Please ensure it is installed and in your PATH.", None
        except subprocess.TimeoutExpired:
            return False, f"Compilation timed out after {timeout_seconds} seconds.", None
        except Exception as e:
            return False, f"An unexpected error occurred during compilation: {str(e)}", None

if __name__ == '__main__':
    sample_tikz_valid = """
    \\begin{tikzpicture}
        \\draw (0,0) circle (1cm);
        \\node at (0,0) {Hello};
    \\end{tikzpicture}
    """

    sample_tikz_invalid_syntax = """
    \\begin{tikzpicture}
        \\draw (0,0) circle (1cm;
        \\node at (0,0) {Error};
    \\end{tikzpicture}
    """
    
    sample_tikz_missing_package = """
    \\begin{tikzpicture}
        \\node [cylinder, draw, shape border rotate=90, aspect=0.2] {DB};
    \\end{tikzpicture}
    """ # Needs \usetikzlibrary{shapes.geometric}

    print("--- Testing valid TikZ code ---")
    success, log, pdf = compile_tikz_code(sample_tikz_valid)
    print(f"Success: {success}")
    # print(f"Log:\n{log}")
    if pdf:
        print(f"PDF size: {len(pdf)} bytes")
        with open("valid_tikz_output.pdf", "wb") as f_out:
            f_out.write(pdf)
        print("PDF saved to valid_tikz_output.pdf")
    else:
        print(f"Log (relevant part):\n{log[-500:]}") # Show last 500 chars of log on failure

    print("\n--- Testing invalid TikZ syntax ---")
    success, log, pdf = compile_tikz_code(sample_tikz_invalid_syntax)
    print(f"Success: {success}")
    if not success:
        print(f"Log (relevant part):\n{log[-500:]}")

    print("\n--- Testing TikZ with missing library (expected to fail without template modification) ---")
    # This will likely fail because the default template doesn't include shapes.geometric
    success, log, pdf = compile_tikz_code(sample_tikz_missing_package)
    print(f"Success: {success}")
    if not success:
        print(f"Log (relevant part):\n{log[-500:]}")

    # Example of using a custom template for missing libraries
    custom_template_for_cylinder = """
    \\documentclass{standalone}
    \\usepackage{tikz}
    \\usetikzlibrary{shapes.geometric} % Added missing library
    \\begin{document}
    {tikz_code}
    \\end{document}
    """
    print("\n--- Testing TikZ with missing library (with custom template) ---")
    success, log, pdf = compile_tikz_code(sample_tikz_missing_package, template=custom_template_for_cylinder)
    print(f"Success: {success}")
    if pdf:
        print(f"PDF size: {len(pdf)} bytes")
        with open("custom_template_output.pdf", "wb") as f_out:
            f_out.write(pdf)
        print("PDF saved to custom_template_output.pdf")
    else:
        print(f"Log (relevant part):\n{log[-500:]}") 
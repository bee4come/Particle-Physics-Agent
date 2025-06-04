# test_agent_accuracy.py
import os
from dotenv import load_dotenv
from agents.tikz_feynman_agent import TikzFeynmanAgent
import argparse
import re

# Test cases: (description, expected_tikz_output)
TEST_CASES = [
    (
        "An electron emits a photon and continues as an electron.",
        """\\feynmandiagram [horizontal=a to c] {
  a [particle=e⁻] -- [fermion] b,
  b -- [fermion] c [particle=e⁻],
  b -- [photon] d [particle=γ],
};"""
    ),
    (
        "A muon and anti-muon annihilate into a Z boson, which decays into an electron and a positron.",
        """\\feynmandiagram [horizontal=a to d] {
  a [particle=μ⁻] -- [fermion] b -- [fermion] c [particle=μ⁺],
  b -- [boson, edge label=Z] d,
  d -- [fermion] e [particle=e⁻],
  d -- [anti fermion] f [particle=e⁺],
};"""
    ),
    (
        "A photon splits into an electron and a positron.",
        """\\feynmandiagram [horizontal=a to b] {
  a [particle=γ] -- [photon] b,
  b -- [fermion] c [particle=e⁻],
  b -- [anti fermion] d [particle=e⁺],
};"""
    ),
    (
        "A quark emits a gluon and continues as a quark.",
        """\\feynmandiagram [horizontal=a to c] {
  a [particle=q] -- [fermion] b,
  b -- [fermion] c [particle=q],
  b -- [gluon] d [particle=g],
};"""
    ),
    (
        "An up quark and anti-down quark annihilate into a W⁺ boson.",
        """\\feynmandiagram [horizontal=a to b] {
  a [particle=u] -- [fermion] b,
  c [particle=\\bar{d}] -- [anti fermion] b,
  b -- [boson, edge label=W⁺] d,
};"""
    ),
    (
        "A top quark decays into a bottom quark and a W⁺ boson.",
        """\\feynmandiagram [horizontal=a to c] {
  a [particle=t] -- [fermion] b -- [fermion] c [particle=b],
  b -- [boson] d [particle=W⁺],
};"""
    ),
    (
        "An electron and positron annihilate into two photons.",
        """\\feynmandiagram [horizontal=a to c] {
  a [particle=e⁻] -- [fermion] b -- [anti fermion] c [particle=e⁺],
  b -- [photon] d [particle=γ],
  b -- [photon] e [particle=γ],
};"""
    ),
    (
        "A gluon splits into two gluons.",
        """\\feynmandiagram [horizontal=a to b] {
  a [particle=g] -- [gluon] b,
  b -- [gluon] c [particle=g],
  b -- [gluon] d [particle=g],
};"""
    ),
    (
        "A Z boson decays into a neutrino and anti-neutrino.",
        """\\feynmandiagram [horizontal=a to b] {
  a [particle=Z] -- [boson] b,
  b -- [fermion] c [particle=ν],
  b -- [anti fermion] d [particle=\\bar{ν}],
};"""
    ),
    (
        "A W⁻ boson decays into an electron and anti-neutrino.",
        """\\feynmandiagram [horizontal=a to b] {
  a [particle=W⁻] -- [boson] b,
  b -- [fermion] c [particle=e⁻],
  b -- [anti fermion] d [particle=\\bar{ν}_e],
};"""
    )
]

def normalize_tikz(tikz_code: str) -> str:
    """Normalizes TikZ code for comparison using user's improved suggestions."""
    if not tikz_code:
        return ""

    # Remove extra curly braces if they wrap the entire content that itself starts with \feynmandiagram
    # This specifically targets {{ \feynmandiagram ... }} -> { \feynmandiagram ... }
    # and also { \feynmandiagram ... }; -> \feynmandiagram ... ;
    # A common pattern seems to be the LLM outputting the content for inside the braces,
    # then wrapping it with an extra pair.
    
    # First, strip outer whitespace from the whole code block
    code = tikz_code.strip()

    # Attempt to fix extra braces: {{...}} -> {...}
    # This regex looks for content starting with \feynmandiagram wrapped in double braces
    # and replaces it with single braces.
    # It also handles if the \feynmandiagram itself is missing the outer braces but the content is double-braced.
    
    # If the code starts with `\feynmandiagram` and is wrapped in `{{...}}`
    if code.startswith("{{") and code.endswith("}}") and "\\feynmandiagram" in code[2:-2]:
        code = code[1:-1] # Remove one layer of braces
    # If the code is just the content part, wrapped in `{{...}}`
    elif code.startswith("{{") and code.endswith("}}") and "\\feynmandiagram" not in code[2:-2]:
         # This case is tricky, assume it's the content for inside \feynmandiagram
         # For now, let's assume the agent is supposed to return the full \feynmandiagram command
         pass


    # Replace unicode particles with LaTeX form
    code = code.replace("μ⁻", "\\mu^-").replace("μ⁺", "\\mu^+").replace("μ", "\\mu")
    code = code.replace("γ", "\\gamma")
    code = code.replace("ν", "\\nu")
    code = code.replace("e⁻", "e^-").replace("e⁺", "e^+") # Handle common superscripts if not already LaTeX
    code = code.replace("⁻", "^-").replace("⁺", "^+") # General superscript
    
    # Standardize common LaTeX particle representations that might vary
    code = re.sub(r"\\\(\s*e\s*\^?\s*-\s*\\\)", r"e^-", code)      # \(e^-\) to e^-
    code = re.sub(r"\\\(\s*e\s*\^?\s*\+\s*\\\)", r"e^+", code)      # \(e^+\) to e^+
    code = re.sub(r"\\\(\s*\\gamma\s*\\\)", r"\\gamma", code)     # \(gamma\) to \gamma
    code = re.sub(r"\\\(\s*\\mu\s*\^?\s*-\s*\\\)", r"\\mu^-", code)  # \(mu^-\) to \mu^-
    code = re.sub(r"\\\(\s*\\mu\s*\^?\s*\+\s*\\\)", r"\\mu^+", code)  # \(mu^+\) to \mu^+
    
    def repl_barnu(match):
        # group(1) captures '(\s*_e\s*)?' part. If it exists, it means _e was present.
        if match.group(1) and '_e' in match.group(1):
            return r"\bar{\nu}_e"
        return r"\bar{\nu}"
    code = re.sub(r"\\\(\s*\\bar\{\s*\\nu\s*\}\s*(\s*_e\s*)?\\\)", repl_barnu, code)

    def repl_nu(match):
        if match.group(1) and '_e' in match.group(1):
            return r"\nu_e"
        return r"\nu"
    code = re.sub(r"\\\(\s*\\nu\s*(\s*_e\s*)?\\\)", repl_nu, code)

    code = re.sub(r"\\\(\s*W\s*\^?\s*\+\s*\\\)", r"W^+", code)     # \(W^+\) to W^+
    code = re.sub(r"\\\(\s*W\s*\^?\s*-\s*\\\)", r"W^-", code)     # \(W^-\) to W^-
    code = re.sub(r"\\\(\s*Z\s*(\s*0\s*)?\\\)", r"Z", code)        # \(Z\) or \(Z0\) to Z
    code = re.sub(r"d\s*̅", r"\\bar{d}", code)                   # d̅ to \bar{d} (common in output)
    code = re.sub(r"\\\(\s*\\bar\{\s*d\s*\}\s*\\\)", r"\\bar{d}", code) # \(\bar{d}\) to \bar{d}


    # Normalize internal whitespace: strip leading/trailing from each line, remove empty lines, single space elsewhere
    lines = [line.strip() for line in code.splitlines()]
    lines = [line for line in lines if line]
    code = " ".join(lines)
    code = re.sub(r"\s+", " ", code)
    
    # Remove spaces around critical characters for TikZ structure
    for char in [',', ';', '{', '}', '[', ']', '=', '--']:
        code = code.replace(f" {char} ", char)
        code = code.replace(f" {char}", char)
        code = code.replace(f"{char} ", char)

    # Ensure semicolon at the end of the diagram block content if it's within braces
    # This is tricky because the agent might return just the content or the full command
    # If it's the full command, the semicolon should be *inside* the last brace.
    # Example: \feynmandiagram[...] { ... ;};
    # Let's assume the agent returns the content that goes inside the braces,
    # or the full command. The expected format has a semicolon before the final closing brace.
    
    # If the code looks like a feynmandiagram block, ensure the content ends with a semicolon
    # before the final closing brace.
    match = re.search(r"(\\feynmandiagram.*?\{)(.*?)(\})", code)
    if match:
        diagram_start = match.group(1)
        content = match.group(2).strip()
        diagram_end = match.group(3)
        if content and not content.endswith(',') and not content.endswith(';'):
            # Check if the last non-whitespace char before potential particle label is a node
            # This is heuristic. A proper parser would be better.
            # If the content ends like `d[particle=g]`, add semicolon.
            if re.search(r"\w+(\[.*?\])?$", content):
                 content += ";"
        code = f"{diagram_start}{content}{diagram_end}"
    
    # One final pass for overall strip
    return code.strip()


def run_tests(agent: TikzFeynmanAgent, test_cases_to_run=None):
    passed_count = 0
    failed_count = 0

    cases_to_process = TEST_CASES
    if test_cases_to_run:
        try:
            indices = [int(x.strip()) -1 for x in test_cases_to_run.split(',')]
            cases_to_process = [TEST_CASES[i] for i in indices if 0 <= i < len(TEST_CASES)]
        except ValueError:
            print(f"Error: Invalid test case numbers: {test_cases_to_run}. Please provide comma-separated numbers.")
            return


    for i, (description, expected_tikz) in enumerate(cases_to_process):
        print(f"\n--- Test Case {TEST_CASES.index((description, expected_tikz)) + 1}/{len(TEST_CASES)} ---")
        print(f"Description: {description}")
        
        generated_tikz = agent.generate_tikz_code(description)
        
        norm_expected = normalize_tikz(expected_tikz)
        norm_generated = normalize_tikz(generated_tikz)

        print("\nExpected TikZ (Normalized):")
        print(norm_expected)
        print("\nGenerated TikZ (Normalized):")
        print(norm_generated)

        if "Error:" in generated_tikz or "failed due to:" in generated_tikz:
            print("\nStatus: FAILED (Agent returned an error)")
            failed_count += 1
        elif norm_generated == norm_expected:
            print("\nStatus: PASSED")
            passed_count += 1
        else:
            print("\nStatus: FAILED (Mismatch)")
            failed_count += 1
            print("\n--- Full Expected TikZ ---")
            print(expected_tikz)
            print("\n--- Full Generated TikZ ---")
            print(generated_tikz)
            print("--- End Full Output ---")


    print("\n--- Test Summary ---")
    print(f"Total Tests: {len(cases_to_process)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Run test suite for TikZFeynmanAgent.")
    parser.add_argument("--model", type=str, help="Optional: Specify the model name to use.")
    parser.add_argument("--provider", choices=["gemini", "deepseek"], default="gemini", help="LLM provider to use (default: gemini)")
    parser.add_argument("--tests", type=str, help="Optional: Comma-separated list of test case numbers to run (e.g., 1,3,5). Runs all if not specified.")
    args = parser.parse_args()

    if args.provider == "gemini" and not os.getenv("GOOGLE_API_KEY"):
        print("错误：GOOGLE_API_KEY 未在环境变量中设置，并且未在 .env 文件中找到。")
        print("请创建 .env 文件并加入 GOOGLE_API_KEY=\"YOUR_KEY\", 或设置环境变量。")
        return
    if args.provider == "deepseek" and not os.getenv("DEEPSEEK_API_KEY"):
        print("错误：DEEPSEEK_API_KEY 未在环境变量中设置，并且未在 .env 文件中找到。")
        print("请在 .env 中设置 DEEPSEEK_API_KEY 或使用环境变量。")
        return

    try:
        agent = TikzFeynmanAgent(model_name=args.model if args.model else None,
                                 provider=args.provider)
    except ValueError as e:
        print(f"Agent 初始化错误: {e}")
        return
        
    run_tests(agent, args.tests)

if __name__ == "__main__":
    main()

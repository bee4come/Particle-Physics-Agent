import re

TIKZ_BLOCK_REGEX = re.compile(r"""\\begin\{tikzpicture\}.*?\\end\{tikzpicture}""", re.DOTALL)

def extract_tikz_block(text: str) -> str | None:
    """
    Extracts the first TikZ picture block from the given text using regex.

    Args:
        text: The input string possibly containing a TikZ picture.

    Returns:
        The extracted TikZ block including \\begin{tikzpicture} and \\end{tikzpicture},
        or None if no block is found.
    """
    if not isinstance(text, str):
        return None
    match = TIKZ_BLOCK_REGEX.search(text)
    return match.group(0) if match else None

if __name__ == '__main__':
    sample_text_with_tikz = """
    Some text before the diagram.
    \\begin{tikzpicture}
        \\draw (0,0) circle (1cm);
    \\end{tikzpicture}
    Some text after the diagram.
    And another one:
    \\begin{tikzpicture}
        \\node at (0,0) {Hello};
    \\end{tikzpicture}
    """
    sample_text_without_tikz = """
    This text has no TikZ diagram.
    Just plain old text.
    """
    
    extracted_block = extract_tikz_block(sample_text_with_tikz)
    if extracted_block:
        print("Extracted TikZ Block:")
        print(extracted_block)
    else:
        print("No TikZ block found in the first sample.")

    extracted_block_none = extract_tikz_block(sample_text_without_tikz)
    if extracted_block_none:
        print("Extracted TikZ Block (should be None):")
        print(extracted_block_none)
    else:
        print("No TikZ block found in the second sample, as expected.")

    # Test with non-string input
    extracted_block_invalid = extract_tikz_block(123)
    if extracted_block_invalid:
        print("Extracted TikZ Block (should be None for invalid input):")
        print(extracted_block_invalid)
    else:
        print("No TikZ block found for invalid input, as expected.") 
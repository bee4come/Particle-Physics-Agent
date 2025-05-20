from particle_data import get_particle_by_name_or_alias, find_interactions, TIKZ_FEYNMAN_DIAGRAMS

def generate_latex_code(interaction):
    """Generate LaTeX TikZ Feynman code for an interaction"""
    
    # Get TikZ code for the interaction
    tikz_code = TIKZ_FEYNMAN_DIAGRAMS.get(interaction['name'], TIKZ_FEYNMAN_DIAGRAMS["DEFAULT"])
    
    # Replace \to with \rightarrow in equations and ensure proper math delimiters
    equation = interaction.get('equation', '').replace('\\to', '\\rightarrow')
    
    # Generate complete LaTeX code with proper preamble information
    latex_template = f"""\\documentclass{{article}}
\\usepackage{{tikz}}
\\usepackage[compat=1.0.0]{{tikz-feynman}}

\\begin{{document}}

\\begin{{figure}}
\\centering
\\begin{{tikzpicture}}
  \\begin{{feynman}}
{tikz_code}
  \\end{{feynman}}
\\end{{tikzpicture}}
\\caption{{{interaction['name']}: $${equation}$$}}
\\end{{figure}}

\\end{{document}}
"""
    return latex_template

def show_interaction_details(interaction):
    """Display detailed information about an interaction"""
    print("\n===== INTERACTION DETAILS =====")
    print(f"Name: {interaction['name']}")
    
    if interaction['type'] == "fundamental":
        print(f"Type: Fundamental Interaction")
        print(f"Description: {interaction['description']}")
    else:
        print(f"Type: Specific Physical Process")
        print(f"Equation: {interaction['equation']}")
        print(f"Description: {interaction['description']}")
    
    # Show more information for specific processes
    if interaction['type'] == "process" and 'products' in interaction:
        print("\nReaction Products:")
        for product in interaction['products']:
            product_data = get_particle_by_name_or_alias(product)
            if product_data:
                print(f"  • {product_data['name']} ({product_data['symbol']})")
                print(f"    - Type: {product_data['type']}")
                print(f"    - Charge: {product_data['charge']}")
                print(f"    - Spin: {product_data['spin']}")
    
    # Generate and display LaTeX code
    latex_code = generate_latex_code(interaction)
    print("\n===== LaTeX TikZ Feynman Code =====")
    print(latex_code)
    
    # Try to copy LaTeX code to clipboard
    try:
        import pyperclip
        pyperclip.copy(latex_code)
        print("LaTeX code has been copied to clipboard!")
    except ImportError:
        print("Tip: Install pyperclip package to enable clipboard copy: pip install pyperclip")

def show_latex_setup_instructions():
    """Display instructions for setting up LaTeX environment for TikZ-Feynman diagrams"""
    print("\n===== LATEX SETUP INSTRUCTIONS =====")
    print("To use the generated TikZ-Feynman diagrams in your LaTeX document:")
    print("\n1. IMPORTANT: TikZ-Feynman requires TeX Live 2018 or earlier")
    print("   Later versions have compatibility issues")
    print("\n2. Copy the entire generated code to a .tex file")
    print("\n3. Compilation options:")
    print("   a) Preferred: Use LuaLaTeX directly for automatic vertex positioning")
    print("      lualatex yourfile.tex")
    print("   b) Alternative workflow: pdflatex -> lualatex -> pdflatex")
    print("\n4. Math mode:")
    print("   • All mathematical expressions must be enclosed in math delimiters")
    print("   • Use $...$ for inline math")
    print("   • Use \\[...\\] for displayed math")
    print("   • Vertex labels already include $ delimiters: {$e^-$}")
    print("\n5. The generated code is a complete document with all required packages:")
    print("""   \\documentclass{article}
   \\usepackage{tikz}
   \\usepackage[compat=1.0.0]{tikz-feynman}
   
   \\begin{document}
   
   \\begin{figure}
   \\centering
   \\begin{tikzpicture}
     \\begin{feynman}
       % Feynman diagram code with proper math delimiters
       \\vertex (a) at (0,0) {$e^-$};  % Note the $ signs for math mode
     \\end{feynman}
   \\end{tikzpicture}
   \\caption{Interaction name: $equation in math mode$}
   \\end{figure}
   
   \\end{document}""")
    
    print("\nSee more details at: https://www.overleaf.com/learn/latex/Feynman_diagrams")

def main():
    """Command-line tool for finding particle interactions"""
    print("\nParticle Interaction Finder")
    print("==========================\n")
    print("Enter particle names, separated by spaces (e.g., 'electron photon' or 'e- gamma')")
    print("Type 'setup' for LaTeX setup instructions")
    print("Type 'exit' to quit program\n")
    
    while True:
        # Get user input
        user_input = input("\nEnter particle names (space-separated): ")
        
        if user_input.lower() == 'exit':
            print("Exiting program...")
            break
            
        if user_input.lower() == 'setup':
            show_latex_setup_instructions()
            continue
        
        # Split user input to get particle name list
        particle_names = [name.strip() for name in user_input.split() if name.strip()]
        
        if len(particle_names) < 1:
            print("Error: Please enter at least one particle name")
            continue
            
        print(f"\nLooking for interactions between {', '.join(particle_names)}...")
        
        # Find particle data
        particles = []
        particle_ids = []
        
        for name in particle_names:
            particle_data = get_particle_by_name_or_alias(name)
            if particle_data:
                particles.append(particle_data)
                particle_ids.append(particle_data["id"])
            else:
                print(f"Warning: Particle '{name}' not found")
        
        if len(particles) < 1:
            print("Error: No valid particle data found")
            continue
            
        # Find interactions
        interactions = find_interactions(particle_ids)
        
        # Display results
        print("\nFound particles:")
        for p in particles:
            print(f"  • {p['name']} ({p['symbol']})")
            print(f"    - Charge: {p['charge']}")
            print(f"    - Spin: {p['spin']}")
            print(f"    - Mass: {p['mass_gev']} GeV/c²")
            print(f"    - Type: {p['type']}")
        
        # Display interactions with numbering
        if interactions:
            interaction_map = {}  # Map index to interaction
            index = 1
            
            print("\nPossible interactions:")
            
            # First show fundamental interaction types
            fundamental = [i for i in interactions if i.get("type") == "fundamental"]
            if fundamental:
                print("\nFundamental Interaction Types:")
                for interaction in fundamental:
                    print(f"  [{index}] {interaction['name']}")
                    print(f"    - {interaction['description']}")
                    interaction_map[index] = interaction
                    index += 1
            
            # Then show specific processes
            processes = [i for i in interactions if i.get("type") == "process"]
            if processes:
                print("\nSpecific Physical Processes:")
                for process in processes:
                    print(f"  [{index}] {process['name']}")
                    print(f"    - Equation: {process['equation']}")
                    print(f"    - Description: {process['description']}")
                    interaction_map[index] = process
                    index += 1
            
            # Prompt user to select an interaction for details
            print("\nSelect an interaction number to view details (Enter 0 to exit):")
            try:
                selection = int(input("Select (0-{0}): ".format(len(interaction_map))))
                if selection == 0:
                    print("Exiting program...")
                    break
                elif 1 <= selection <= len(interaction_map):
                    show_interaction_details(interaction_map[selection])
                    print("\nProgram complete.")
                    break  # Exit after showing details
                else:
                    print(f"Invalid selection, please enter a number between 0 and {len(interaction_map)}")
            except ValueError:
                print("Please enter a valid number")
        else:
            print("\nNo specific interaction found between these particles.")
            continue

if __name__ == "__main__":
    main() 
# run_agent_cli.py
import os
import argparse
from agents.tikz_feynman_agent import TikzFeynmanAgent
from dotenv import load_dotenv

def main():
    load_dotenv() # Load variables from .env file into environment

    parser = argparse.ArgumentParser(description="Generate TikZ-Feynman code or search the local knowledge base.")
    
    # Group for generation related arguments
    generation_group = parser.add_argument_group('Generation Options')
    generation_group.add_argument("description", type=str, nargs='?', default=None, help="The physics process description for TikZ generation (e.g., 'an electron emits a photon'). If not provided and --search is not used, will prompt interactively.")
    generation_group.add_argument("--output", "-o", type=str, help="Optional: Path to save the full .tex document for generated TikZ code. If --wrap-document is also used, this file will contain the wrapped document.")
    generation_group.add_argument("--model", type=str, help="Optional: Specify the Gemini model name to use for generation, overriding .env or agent default.")
    generation_group.add_argument("--strict", action='store_true', help="Enable strict mode. If generation validation fails, no code is output.")
    generation_group.add_argument("--wrap-document", action='store_true', help="Wrap the generated TikZ code in a complete standalone LaTeX document.")

    # Group for search related arguments
    search_group = parser.add_argument_group('Search Options')
    search_group.add_argument("--search", "-s", type=str, dest="search_query", help="Search query to find relevant records in the local knowledge base.")
    search_group.add_argument("--limit", "-k", type=int, default=5, help="Optional: Number of search results to return (default: 5).")


    args = parser.parse_args()

    if args.search_query:
        from kb.db import query_records_by_description # Import here to avoid issues if kb not fully set up for non-search paths
        print(f"\nSearching knowledge base for: \"{args.search_query}\" (limit {args.limit})...")
        try:
            results = query_records_by_description(args.search_query, k=args.limit)
            if results:
                print(f"\nFound {len(results)} record(s):")
                for r in results:
                    tikz_preview = r.tikz.replace('\n', ' ').strip()[:80]
                    print(f"  - Reaction: {r.reaction}")
                    print(f"    Description: {r.description}")
                    print(f"    TikZ (preview): {tikz_preview}...")
                    # print(f"    Topic: {r.topic}, Process: {r.process_type}, Source: {r.source}") # Optional more details
            else:
                print("  No matching records found.")
        except Exception as e:
            print(f"Error during search: {e}")
        return # Exit after search

    # If not searching, proceed with generation
    # Check for API key after loading .env, before agent instantiation
    # The agent will also check, but this provides a CLI-level early exit.
    if not os.getenv("GOOGLE_API_KEY"):
        print("错误：GOOGLE_API_KEY 未在环境变量中设置，并且未在 .env 文件中找到。")
        print("请创建 .env 文件并加入 GOOGLE_API_KEY=\"YOUR_KEY\", 或设置环境变量。")
        print("参考 .env.example 文件。")
        return

    try:
        # Pass model from CLI args if provided, otherwise agent uses its logic (env var or default)
        agent = TikzFeynmanAgent(model_name=args.model if args.model else None)
    except ValueError as e:
        print(f"Agent 初始化错误: {e}")
        return
    
    description_to_process = args.description
    if not description_to_process: # Will only be true if search_query was also not provided
        try:
            description_to_process = input("请输入物理过程描述 (用于生成 TikZ 代码): ")
        except EOFError:
            print("错误：未提供描述或搜索查询。请通过命令行参数提供。")
            parser.print_help()
            return
            
    if not description_to_process: # Still no description after prompt
        print("错误：未提供描述用于生成 TikZ 代码。")
        parser.print_help()
        return

    print(f"\n准备为描述生成 TikZ 代码: \"{description_to_process}\"")
    try:
        tikz_code_segment = agent.generate_tikz_code(description_to_process)
        
        if "Error:" in tikz_code_segment or "failed due to:" in tikz_code_segment :
             print(f"\n代码生成失败或返回错误：\n{tikz_code_segment}")
             return

        if args.strict:
            print("严格模式已启用：正在验证生成的代码...")
            # We need to access the _validate_tikz_code method.
            # It's conventionally private, but for this CLI interaction, it's acceptable.
            # Alternatively, generate_tikz_code could return a tuple (code, is_valid)
            # but that changes its primary API.
            if not agent._validate_tikz_code(tikz_code_segment):
                print("\n生成的代码未通过严格模式验证。")
                print("可能缺少关键的 TikZ-Feynman 样式 (例如 [fermion], [photon])。")
                print("建议：请检查您的描述或尝试在非严格模式下生成。")
                return # Exit without printing or saving

        if args.wrap_document:
            full_tex_document = f"""\\documentclass{{standalone}}
\\usepackage[compat=1.1.0]{{tikz-feynman}}

\\begin{{document}}
{tikz_code_segment}
\\end{{document}}"""
            if args.output:
                try:
                    with open(args.output, "w", encoding="utf-8") as f:
                        f.write(full_tex_document)
                    print(f"\n完整的 standalone LaTeX 文档已保存到: {args.output}")
                except IOError as e:
                    print(f"\n错误：无法写入文件 {args.output}。错误信息: {e}")
            else:
                print("\n生成的完整 standalone LaTeX 文档：")
                print(full_tex_document)
        
        else: # Original behavior if --wrap-document is not used
            print("\n生成的 TikZ 代码片段：")
            print(tikz_code_segment)

            if args.output:
                # Default wrapping if --output is used without --wrap-document
                # (using article class as before, for consistency if someone relied on it)
                # Or, we could decide that --output without --wrap-document saves only the fragment.
                # For now, keeping the previous --output behavior when --wrap-document is absent.
                article_wrapped_tex_document = f"""\\documentclass{{article}}
\\usepackage[compat=1.1.0]{{tikz-feynman}}

\\begin{{document}}

\\begin{{figure}}
{tikz_code_segment}
\\end{{figure}}

\\end{{document}}
"""
                try:
                    with open(args.output, "w", encoding="utf-8") as f:
                        f.write(article_wrapped_tex_document)
                    print(f"\n完整的 .tex 文档 (article class) 已保存到: {args.output}")
                except IOError as e:
                    print(f"\n错误：无法写入文件 {args.output}。错误信息: {e}")
            else:
                print("\n提示：您可以使用 --output <文件名.tex> 参数将完整文档保存到文件，或使用 --wrap-document 直接输出完整 standalone 文档。")

    except Exception as e:
        print(f"生成过程中发生严重错误: {e}")

if __name__ == "__main__":
    main()

# MCP for TikZ Feynman (中文文档)

**MCP for TikZ Feynman** 是一个AI驱动的工具，旨在通过自然语言描述自动生成 LaTeX TikZ-Feynman 图表代码。本项目致力于简化科研人员和学生在 LaTeX 中创建费曼图的流程。

本项目当前使用 Google Gemini API 进行自然语言处理和代码生成，并通过本地知识库（KB）和向量检索来增强 few-shot prompt 的能力。

关于详细的开发路线图、未来目标和阶段规划，请参阅 [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md)。

## 核心功能

*   **自然语言转 TikZ 代码：** 输入物理过程的自然语言描述，Agent 将结合从知识库中检索到的相似示例（如果可用）来生成相应的 TikZ-Feynman 代码。
*   **本地知识库检索：** 可以通过命令行工具搜索已存储在本地知识库中的费曼图数据。

## 系统要求

*   Conda (用于环境管理)
*   Python 3.9+
*   一个拥有 Gemini API 访问权限的 Google API 密钥。
*   （可选，用于构建Annoy索引）C++ Build Tools (Windows用户在安装 `annoy` 依赖时可能需要)。

## 安装与设置指南

1.  **克隆代码仓库：**
    ```bash
    git clone https://github.com/bee4come/MCP-for-Tikz-.git # 请替换为实际仓库地址
    cd MCP-for-Tikz-
    ```

2.  **创建并激活 Conda 环境：**
    ```bash
    conda create --name tikz_mcp_env python=3.9 -y
    conda activate tikz_mcp_env
    ```

3.  **安装依赖：**
    从 `requirements.txt` 文件安装所需的 Python 包：
    ```bash
    pip install -r requirements.txt
    ```

4.  **设置 API 密钥与配置 (.env 文件)：**
    *   复制项目根目录下的 `.env.example` 文件，并将其重命名为 `.env`。
    *   编辑 `.env` 文件，至少填入您的 `GOOGLE_API_KEY`，或者填写 `DEEPSEEK_API_KEY` 以使用 DeepSeek 模型。
        ```dotenv
        # .env 文件示例
        GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"

        # 若使用 DeepSeek，可设置
        #DEEPSEEK_API_KEY="YOUR_DEEPSEEK_API_KEY_HERE"
        #DEEPSEEK_MODEL_NAME="deepseek-chat"
        #DEEPSEEK_API_BASE="https://api.deepseek.com"
        
        # 用于 Agent 生成 TikZ 代码的 Gemini 模型 (可选, 默认: gemini-1.5-pro-latest)
        GEMINI_MODEL_NAME="gemini-1.5-pro-latest"
        
        # 用于生成向量嵌入的 Gemini 模型 (可选, 默认: text-embedding-004)
        GEMINI_EMBEDDING_MODEL_NAME="text-embedding-004"
        ```
    脚本将自动从此 `.env` 文件加载配置。

5.  **准备知识库数据源 (JSON)：**
    *   确保 `feynman_kb_enhanced.json` 文件位于项目根目录。此文件包含用于填充知识库的初始数据。

6.  **构建本地知识库 (数据库和向量索引)：**
    在激活 `tikz_mcp_env` 环境后，于项目根目录执行以下命令：
    *   **a. 迁移数据并生成嵌入：**
        ```bash
        python -m kb.migrate_json
        ```
        此脚本会：
        *   初始化 `data/feynman_kb.duckdb` 数据库。
        *   读取 `feynman_kb_enhanced.json`。
        *   为每条记录生成向量嵌入（通过 Gemini API）。
        *   将记录及其嵌入存入数据库。
        请注意此步骤（尤其是首次运行本地模型时）可能需要一些时间下载模型和处理数据。

    *   **b. 构建 Annoy 索引：**
        ```bash
        python -m kb.build_ann_index
        ```
        此脚本会：
        *   从数据库读取向量嵌入。
        *   构建 Annoy 索引文件 (`data/feynman_kb.ann`) 和 ID 映射文件 (`data/feynman_kb_id_map.json`)，用于快速向量检索。

## 运行 Agent (命令行工具)

项目提供了一个命令行工具 `run_agent_cli.py` 来与 Agent 交互。

**运行命令行工具：**

1.  确保您的 `tikz_mcp_env` Conda 环境已激活。
2.  确保已按照上述说明配置了 API 密钥和知识库。
3.  执行脚本：
    *   **生成 TikZ 代码** (Agent 会尝试使用知识库进行 few-shot 增强)：
        ```bash
        # 使用默认描述进行交互式输入
        python run_agent_cli.py 
        # 或提供描述参数
        python run_agent_cli.py "一个电子发射一个光子并继续作为电子存在"
        # 指定输出文件和生成模型
        python run_agent_cli.py "一个μ子衰变" --model gemini-1.5-pro-latest -o muon_decay.tex
        # 使用 DeepSeek 模型示例
        python run_agent_cli.py "一个电子发射一个光子" --provider deepseek
        ```
    *   **搜索本地知识库** (基于文本描述)：
        ```bash
        python run_agent_cli.py --search "electron scattering"
        python run_agent_cli.py --search "Z boson" --limit 3 
        ```
    *   获取帮助信息：
        ```bash
        python run_agent_cli.py --help
        ```

## 贡献

欢迎参与贡献！有关未来的工作方向，请参阅 `DEVELOPMENT_PLAN.md`。

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

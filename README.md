# MCP for TikZ Feynman (中文文档)

**MCP for TikZ Feynman** 是一个AI驱动的工具，旨在通过自然语言描述自动生成 LaTeX TikZ-Feynman 图表代码。本项目致力于简化科研人员和学生在 LaTeX 中创建费曼图的流程。

本项目当前使用 Google Gemini API 进行自然语言处理和代码生成。

关于详细的开发路线图、未来目标和阶段规划，请参阅 [DEVELOPMENT_PLAN.md](DEVELOPMENT_PLAN.md) (开发计划文档，稍后也将更新为中文版)。

## 核心功能 (MVP)

*   **自然语言转 TikZ 代码：** 输入物理过程的自然语言描述（例如：“一个电子发射一个光子并继续作为电子存在”），即可获得相应的 TikZ-Feynman 代码。

## 系统要求

*   Conda (用于环境管理)
*   Python 3.9+
*   一个拥有 Gemini API 访问权限的 Google API 密钥。

## 安装与设置指南

1.  **克隆代码仓库：**
    ```bash
    git clone <repository_url> # 请将 <repository_url> 替换为实际的仓库地址
    cd MCP-for-Tikz-
    ```

2.  **创建并激活 Conda 环境：**
    建议创建一个名为 `tikz_mcp_env` 且使用 Python 3.9 的 Conda 环境。
    ```bash
    conda create --name tikz_mcp_env python=3.9 -y
    conda activate tikz_mcp_env
    ```

3.  **安装依赖：**
    从 `requirements.txt` 文件安装所需的 Python 包：
    ```bash
    pip install -r requirements.txt
    ```
    或者，如果您希望在不每次激活环境的情况下直接在指定环境中运行命令，可以使用：
    ```bash
    conda run -n tikz_mcp_env pip install -r requirements.txt
    ```

4.  **设置 API 密钥：**
    您需要将您的 Google API 密钥和可选的模型名称配置在 `.env` 文件中，或者设置为环境变量。

    **推荐方式：使用 `.env` 文件**
    1.  复制项目根目录下的 `.env.example` 文件，并将其重命名为 `.env`。
    2.  编辑 `.env` 文件，填入您的 `GOOGLE_API_KEY` 和希望使用的 `GEMINI_MODEL_NAME`。
        ```dotenv
        GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY_HERE"
        GEMINI_MODEL_NAME="gemini-2.5-flash-preview-04-17" 
        ```
    脚本将自动从此 `.env` 文件加载配置。

    **或者：设置环境变量** (如果未找到 `.env` 文件或特定变量缺失，脚本会尝试读取环境变量)
    *   `GOOGLE_API_KEY`: 您的 Google API 密钥。
    *   `GEMINI_MODEL_NAME` (可选): 您希望使用的 Gemini 模型名称 (例如 `gemini-1.5-pro`，默认为 `gemini-2.5-flash-preview-04-17`)。

    设置环境变量示例：
    *   Linux/macOS: `export GOOGLE_API_KEY="YOUR_API_KEY"`
    *   Windows (命令提示符): `set GOOGLE_API_KEY=YOUR_API_KEY`
    *   Windows (PowerShell): `$env:GOOGLE_API_KEY="YOUR_API_KEY"`

## 运行 Agent (命令行工具)

项目提供了一个命令行工具 `run_agent_cli.py` 来与 Agent 交互。

**运行命令行工具：**

1.  确保您的 `tikz_mcp_env` Conda 环境已激活。
2.  确保已按照上述说明配置了 API 密钥 (通过 `.env` 文件或环境变量)。
3.  执行脚本：
    *   获取帮助信息：
        ```bash
        python run_agent_cli.py --help
        ```
    *   通过参数提供描述 (将使用 `.env` 或默认模型)：
        ```bash
        python run_agent_cli.py "一个电子发射一个光子"
        ```
    *   指定模型并输出到文件：
        ```bash
        python run_agent_cli.py "一个μ子衰变成一个电子、一个反电中微子和一个μ中微子" --model gemini-1.5-pro -o muon_decay.tex
        ```
    *   交互式输入描述：
        ```bash
        python run_agent_cli.py
        ```
    或者使用 `conda run` (确保 `.env` 文件在工作目录或环境变量已设置)：
    ```bash
    conda run -n tikz_mcp_env python run_agent_cli.py "一个电子发射一个光子"
    ```

## 贡献

欢迎参与贡献！有关未来的工作方向，请参阅 `DEVELOPMENT_PLAN.md`。

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件 (假设后续会添加标准的 LICENSE 文件)。

# 工作日志 (Work Log)

本文档记录了 MCP for TikZ Feynman 项目的主要开发活动和变更。

## 初期 MVP 搭建与迭代 (截至 Action Plan 0 → 1 之前)

*   **项目初始化**:
    *   创建了基础的 `requirements.txt` (初始包含 `openai`, `streamlit`, 后续调整)。
    *   创建了 `.gitignore` 文件。
*   **核心 Agent (`agents/tikz_feynman_agent.py`)**:
    *   初始版本使用 OpenAI API。
    *   根据用户要求，切换为使用 Google Gemini API。
    *   迭代优化了 Prompt 以提高 TikZ 代码生成质量，包括加入粒子标签的尝试。
*   **示例与测试**:
    *   创建了 `prompts/feynman_examples.md` 用于存放 few-shot 示例。
    *   创建了 `test_agent_accuracy.py` 用于批量测试 Agent 输出，并迭代改进了其中的 `normalize_tikz` 函数以更好地比较实际输出与期望输出。
*   **用户接口**:
    *   曾尝试创建基于 Streamlit 的 Web UI (`webui/app.py`)。
    *   根据用户反馈，移除了 Web UI 组件，并将 `streamlit` 从 `requirements.txt` 中移除/注释。
    *   创建了基础的命令行工具 `run_agent_cli.py` (使用 `argparse`) 用于直接与 Agent 交互。
*   **文档**:
    *   创建并多次修订了 `README.md` 和 `DEVELOPMENT_PLAN.md`。
    *   将主要文档翻译为中文。
    *   文档内容随项目方向调整（例如，移除 Web UI 相关说明，增加 CLI 说明）。
*   **环境配置**:
    *   指导用户创建 Conda 环境 `tikz_mcp_env`。
    *   协助解决依赖安装问题，特别是 `annoy` 包在 Windows 上需要 C++ Build Tools 的问题。
    *   引入 `python-dotenv` 支持，允许从 `.env` 文件加载 API 密钥和模型配置。创建了 `.env.example`。

## "行动方案 0 → 1": 知识库 (KB) 模块构建

此阶段专注于构建一个可检索、可进化的费曼图知识库。

*   **1. 环境与依赖更新**:
    *   `requirements.txt` 文件中追加了新依赖: `pydantic>=2`, `duckdb==0.10.*`, `sqlite-utils>=3.36`, `tqdm`, `sentence-transformers>=2.3` (后根据策略调整), `annoy`, `requests`。
    *   经历了 `sentence-transformers` 的移除和重新引入（根据用户对本地备选方案的决策调整）。

*   **2. 目录结构变更**:
    *   创建了新的 `kb/` Python 包目录。
    *   在 `kb/` 中创建了模块文件: `__init__.py`, `db.py`, `schema.py`, `embedding.py`, `migrate_json.py`。

*   **3. 核心代码实现 (`kb/` 模块)**:
    *   **`kb/schema.py`**:
        *   定义了 `FeynmanRecord` Pydantic 模型，用于规范知识库中每条记录的结构。
    *   **`kb/embedding.py`**:
        *   实现了向量嵌入生成逻辑，目标维度 `EMB_DIM = 768`。
        *   **Gemini API**:
            *   最初尝试使用 `requests` 直接调用 REST API，遇到了模型名称和端点问题 (`gemini-embedding-exp-03-07` 的 404错误)。
            *   根据用户反馈和提供的 SDK 用法，改为使用 `google.generativeai` Python 客户端库 (`genai.configure()` 和 `genai.embed_content()`)。
            *   解决了 Gemini 模型返回维度 (3072d) 与期望维度 (768d) 不匹配的问题，通过建议用户在 `.env` 中配置确认输出768维的模型（如 `text-embedding-004` 或 `embedding-001`）并使代码优先读取该配置。
            *   当前默认使用 `text-embedding-004`。
        *   **本地 BGE 模型**:
            *   最初作为备选方案引入 `BAAI/bge-base-zh-v1.5` (768维)。
            *   曾根据用户指示一度移除本地备选逻辑。
            *   根据用户最新的“最小可行补丁”指示，重新引入了 BGE 本地模型作为 Gemini API 调用失败或未配置 API 密钥时的备选方案。
            *   优化了本地模型的初始化逻辑，从模块加载时初始化改为惰性初始化（在 `embed_with_bge` 首次需要时）。*(注：当前最新版本是在模块加载时初始化，但之前的讨论中有过惰性初始化的想法)*。当前版本是在模块加载时初始化。
        *   `get_embedding()` 函数实现了优先尝试 Gemini，失败则回退到本地 BGE 的逻辑。
        *   `enrich_record_with_embedding()` 函数用于为 `FeynmanRecord` 对象填充向量嵌入。
    *   **`kb/db.py`**:
        *   实现了与 DuckDB 数据库的交互。
        *   `init_db()`: 创建 `data/feynman_kb.duckdb` 文件和 `feynman` 表。
        *   `_serialize_embedding()` 和 `_deserialize_embedding()`: 处理向量列表与数据库 BLOB 类型之间的转换。
        *   `upsert_record()`: 将 `FeynmanRecord` 对象（包括其粒子列表和向量嵌入）写入数据库。
        *   `query_records_by_description()`: 实现基于 `description` 字段的 `ILIKE` 文本模糊搜索。修正了 `con.sql()` 方法的参数传递方式，解决了 `incompatible function arguments` 错误。
    *   **`kb/migrate_json.py`**:
        *   实现了从项目根目录的 `feynman_kb_enhanced.json` 文件读取数据。
        *   对每条记录调用 `enrich_record_with_embedding()` 生成向量。
        *   调用 `upsert_record()` 将处理后的记录存入 DuckDB。
        *   加入了 `tqdm` 进度条和错误处理。
        *   用户已确认此脚本在本地成功运行，处理了48条记录，并且 `data/feynman_kb.duckdb` 文件已生成。

*   **4. CLI 增强 (`run_agent_cli.py`)**:
    *   使用 `argparse` 为 CLI 工具增加了 `--search` (或 `-s`) 和 `--limit` (或 `-k`) 参数。
    *   实现了当 `--search` 参数被使用时，调用 `kb.db.query_records_by_description()` 并打印搜索结果的功能。
    *   经过用户测试，使用通用搜索词（如 "electron"）已能成功从数据库中检索并显示记录，验证了数据库填充和基础搜索功能的正确性。特定搜索词无结果的问题被归因于数据内容本身。

*   **5. 当前状态 (截至此日志)**:
    *   知识库骨架 (`kb/*.py`) 已完成。
    *   数据迁移脚本 (`kb.migrate_json.py`) 已由用户确认成功运行，数据和（部分或全部）嵌入已存入 `data/feynman_kb.duckdb`。
    *   CLI 的 `--search` 功能已初步实现并通过了基本验证。
    *   下一个计划的里程碑是 CI (GitHub Actions) 的配置。

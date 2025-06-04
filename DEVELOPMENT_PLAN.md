# MCP for TikZ Feynman - 开发计划 (中文版)

本文档概述了 MCP for TikZ Feynman 项目的开发计划。

## 核心目标

1.  **自然语言转 TikZ：** 使用户能够通过自然语言描述生成 TikZ-Feynman 图表代码。
2.  **图片转 TikZ (未来目标)：** 探索并可能实现从费曼图图片生成 TikZ 代码的功能 (费曼图 OCR)。

## 阶段一：MVP - 自然语言转 TikZ (Gemini API)

**状态：初始文件已创建，基础功能已实现，Web UI 已移除。**

### 1.1. Agent 核心逻辑
*   **任务：** 确保 `agents/tikz_feynman_agent.py` 中的核心 Agent 逻辑能够稳定运行，并通过 Google Gemini API 生成 TikZ 代码。
    *   **负责人：** Cline (bee)
*   **任务：** 更新 `README.md` (已完成)，提供正确的安装、API 密钥设置 (Google API Key for Gemini) 和 Agent 运行说明。
    *   **负责人：** Cline (bee)

### 1.2. 初步测试与反馈
*   **任务：** 通过直接调用 Agent (例如，使用 `run_agent_example.py` 脚本) 进行初步测试，使用不同的自然语言描述。
    *   **参与者：** 用户, JYEU
*   **任务：** 收集关于 Gemini API 生成代码的准确性、鲁棒性以及对不同描述风格适应性的反馈。
    *   **负责人：** Cline (bee) 整理。

## 阶段二：知识库与检索增强 (S-1 & S-2 from Action Plan 0->1)

**状态：核心组件已实现，包括数据迁移、向量嵌入（Gemini）、Annoy索引构建、向量检索、Few-shot Prompt组装、CLI文本搜索。**

### 2.1. 知识库构建 (`kb` 模块)
*   **数据迁移**: `feynman_kb_enhanced.json` -> DuckDB (`data/feynman_kb.duckdb`) (已完成)
*   **向量嵌入**: 使用 Gemini API 为记录生成768维向量。 (已完成)
*   **Annoy 索引**: 构建并保存 Annoy 索引 (`data/feynman_kb.ann`) 和 ID 映射。 (已完成)

### 2.2. 检索与 Prompt 增强
*   **向量检索**: 实现 `kb.retriever.query_records_by_vector`。 (已完成)
*   **Few-Shot Prompt**: 实现 `kb.prompt.compose_prompt`，根据检索结果动态构建提示。 (已完成)
*   **Agent 集成**: `agents.tikz_feynman_agent` 已更新，使用知识库检索和 few-shot prompt，并设置 `temperature=0`。 (已完成)

### 2.3. CLI 功能
*   **文本搜索**: `run_agent_cli.py` 已集成 `--search` 功能，可执行基于描述的文本模糊搜索。 (已完成)

## 阶段三：CI 与部署准备

### 3.1. GitHub Actions CI
*   **任务：** 配置 CI 流程 (`.github/workflows/test.yml`)，包括依赖安装、数据迁移、基本搜索测试、向量嵌入覆盖率检查。 (已创建配置文件)
    *   **负责人：** Cline (bee)
*   **目标：** CI 流程通过（"绿灯"）。

### 3.2. 文档完善与版本发布 (v0.2 Tag)
*   **任务：** 更新 `README.md`、`WORKLOG.md`、`DEVELOPMENT_PLAN.md` 等文档。
*   **任务：** 根据已完成功能，准备发布 v0.2 版本标签。
    *   **负责人：** Cline (bee)

## 阶段四：后续加固与质量提升 (用户建议)

### 4.1. 知识库内容优化
*   **任务：** 更新知识库（`feynman_kb_enhanced.json` 或直接操作数据库）中的示例，确保其 TikZ 代码风格统一且符合"出版级"标准（例如，使用边样式 `[fermion]/[photon]`，规范节点命名等）。
    *   **负责人：** JYEU, 用户

### 4.2. 生成后自动验证与重试
*   **任务：** 在 Agent 生成 TikZ 代码后，加入一个验证步骤。通过解析 TikZ 字符串，检查是否缺少关键样式（如 `[fermion]`, `[photon]` 等）。
*   **任务：** 如果验证失败（例如，样式缺失），Agent 可以自动尝试重新生成一次（可能使用不同的内部参数或微调后的提示）。
    *   **负责人：** Cline (bee)
    *   **状态：** 初步完成 (Agent 已实现验证和重试逻辑)。

### 4.3. CLI `--strict` 模式
*   **任务：** 为 `run_agent_cli.py` 添加一个 `--strict` 模式开关。
*   **任务：** 在此模式下，Agent 生成的 TikZ 代码如果未通过上述"自动验证"，则不输出生成的代码，而是提示用户"生成不合格，已回退（或建议）使用标准模板/或提示用户检查输入"。
    *   **负责人：** Cline (bee)
    *   **状态：** 初步完成 (CLI `--strict` 模式已添加)。

### 4.4. KB 自学习 (增量更新机制)
*   **目标：** 实现知识库的即时增量学习能力，允许通过验证的、由 CLI 生成的新 TikZ 片段自动更新知识库（DuckDB 和 Annoy 索引），并通过异步机制定期将增量数据落盘到用户特定的 JSON 文件。
*   **方案 (B-1)：** 即时增量写库 + 周期性 JSON 落盘。
    *   **核心组件：**
        *   `kb/annoy_index.py`: 封装 Annoy 索引的加载、增量记录添加 (`add_record_to_index`) 和搜索。增量添加涉及内存中索引的重建和即时保存。
        *   `kb/autosave.py`: 实现待处理记录的队列 (`queue_record_for_autosave`) 和通过 `atexit` 及守护线程定期将队列中记录刷新到 `data/feynman_kb_user.json` 的逻辑。
        *   `run_agent_cli.py`: 在成功生成并通过验证后，调用 `kb.db.upsert_record` (写入 DuckDB)，`kb.annoy_index.add_record_to_index` (更新 Annoy 索引)，以及 `kb.autosave.queue_record_for_autosave` (排队等待 JSON 落盘)。
    *   **数据文件：**
        *   `data/feynman_kb_base.json`: 基础知识库，只读。
        *   `data/feynman_kb_user.json`: 用户生成的、通过验证的增量记录，由 `kb/autosave.py` 维护。
        *   `data/feynman_kb.duckdb`: 实时通过 `upsert_record` 更新。
        *   `data/feynman_kb.ann`, `data/feynman_kb_id_map.json`: 实时通过 `add_record_to_index` 更新和保存。
    *   **负责人：** Cline (bee)
    *   **状态：** 进行中。`kb/annoy_index.py` 和 `kb/autosave.py` 初稿已完成。下一步是集成到 `run_agent_cli.py`。
*   **后续任务 (根据用户建议)：**
    *   **CLI `--wrap-document` 选项：** (已完成) 在 `run_agent_cli.py` 中添加选项，输出包含 TikZ 代码的完整 standalone LaTeX 文档。
    *   **README 更新：** 说明增量学习机制、安全写策略和定期合并的流程。
    *   **CI Nightly Job：** 配置 GitHub Actions 定时任务，用于合并 `feynman_kb_user.json` 到 `feynman_kb_base.json`（或新的基线版本），并完全重建知识库（DuckDB, Annoy 索引）。

### 4.5. 引入基于LLM的物理过程预解析与验证 (新)
*   **目标：** 在主LLM生成TikZ代码之前，通过LLM Function Calling机制辅助解析用户输入的自然语言描述，提取结构化的反应物和生成物信息。结合PDG（Particle Data Group）API获取的权威粒子数据和本地物理规则库（如电荷、轻子数、重子数守恒），对解析出的反应进行预验证，并将此增强上下文提供给主TikZ生成LLM。
*   **核心价值：**
    *   **提升首次生成准确性：** 为TikZ生成LLM提供更准确、经过物理规则初步校验的上下文信息，引导其生成更符合物理原理的费曼图。
    *   **减少无效调用：** 对于明显违反物理守恒定律的用户描述，可以在早期阶段识别，并考虑直接向用户反馈或引导其修正，从而避免不必要的LLM计算资源消耗。
    *   **增强鲁棒性：** 提高对模糊、不规范用户输入的理解和处理能力。
*   **涉及模块与核心功能实现：**
    *   **1. LLM辅助解析用户描述 (`agents/tikz_feynman_agent.py` 或新模块 `agents/llm_particle_parser.py`)**
        *   **函数模式定义 (`Tool Schema`):** 设计名为 `extract_particle_reaction_components` 的函数模式 (JSON Schema)，包含 `user_description` (输入), `incoming_particles` (输出列表), `outgoing_particles` (输出列表), `process_type` (可选输出) 等参数。此模式将提供给LLM。
        *   **LLM交互方法 (例如在 `TikzFeynmanAgent` 中新增 `_invoke_llm_for_reaction_parsing(description: str) -> Optional[Dict]`)**: 此方法负责：
            *   构建包含上述函数模式的请求，调用LLM（如Gemini API）处理用户输入的 `description`。
            *   接收并解析LLM返回的Function Calling结果（一个包含提取出的粒子列表的JSON对象）。
            *   初步处理LLM返回的原始粒子名列表。
    *   **2. 粒子信息标准化与物理验证 (`alpha/physics_validator.py`)**
        *   **本地粒子属性与映射 (`PARTICLE_PHYSICS_PROPERTIES`, `CANONICAL_NAME_MAP`):** 维护和扩展现有的本地数据库，包含粒子规范名称、别名、电荷、轻子数 (Le, Lmu, Ltau)、重子数 (B) 等守恒量。
        *   **PDG API 集成 (`alpha/particle_interactions.py` 中的 `get_particles_from_pdg` 或 `physics_validator.py` 中的新辅助函数):** 确保可以根据粒子名称从PDG数据库获取权威数据 (如质量、标准LaTeX符号、PDG确认的量子数等)。
        *   **核心验证函数 (例如 `validate_reaction_with_llm_parsed_data(llm_parsed_output: Dict, pdg_api_instance) -> Tuple[bool, List[str], Dict]`)**: 此新函数将负责：
            *   接收来自LLM解析的原始粒子列表 (`llm_parsed_output`)。
            *   使用 `CANONICAL_NAME_MAP` 和PDG查询对粒子名称进行标准化和属性填充，形成包含完整物理属性的结构化反应表示 (`structured_reaction_with_properties`)。
            *   调用 `check_conservation_laws(structured_reaction_with_properties)` (可能需要增强) 来检查电荷、轻子数、重子数等是否守恒。
            *   返回验证结果 (布尔值)、反馈信息列表、以及包含所有标准化和补充后粒子信息的字典。
    *   **3. Agent主流程修改 (`agents/tikz_feynman_agent.py`)**
        *   **修改 `generate_tikz_code(original_description: str)` 方法：**
            *   **步骤A (预处理):** 调用 `_invoke_llm_for_reaction_parsing(original_description)` 获取LLM对用户描述的结构化解析。
            *   **步骤B (验证与信息整合):** 如果步骤A成功，则调用 `alpha.physics_validator.validate_reaction_with_llm_parsed_data()` 对LLM的解析结果进行标准化、PDG数据补充和物理守恒检查。
            *   **步骤C (构建增强上下文):** 将原始用户描述、LLM的结构化解析结果、PDG粒子数据摘要、物理验证结果（成功信息或具体的冲突警告）整合成一个详细的上下文块 (`enhanced_context_for_tikz_llm`)。
            *   **步骤D (RAG检索):** （可选，需评估）考虑是基于 `original_description` 还是基于LLM解析/标准化后的粒子信息进行RAG知识库的向量检索，以获取更相关的TikZ示例。
            *   **步骤E (最终提示组合):** 调用 `kb.prompt.compose_prompt(rag_examples, enhanced_context_for_tikz_llm)` (可能需要调整`compose_prompt`以适应更复杂的上下文输入) 来构建最终发送给TikZ生成LLM的提示。
            *   **步骤F (TikZ生成与后处理):** 调用主LLM生成TikZ代码。如果预验证发现问题，可以在生成的代码前添加注释警告。
*   **数据流概要：**
    `User Input` -> `TikzFeynmanAgent._invoke_llm_for_reaction_parsing` (LLM Function Call) -> `LLM Parsed Particles (JSON)` -> `alpha.physics_validator.validate_reaction_with_llm_parsed_data` (Standardization, PDG Query, Conservation Check) -> `Validated Reaction Info & Feedback` -> `TikzFeynmanAgent.generate_tikz_code` (Context Augmentation & RAG) -> `Enhanced Prompt` -> `TikZ Generation LLM` -> `TikZ Code Output`.
*   **负责人：** (待定)
*   **状态：** 计划中。

## 阶段五：图片转 TikZ (费曼图 OCR) - 长期研发

### 5.1. VLM 调研与评估
*   **任务：**调研和评估现有的视觉语言模型 (VLM，如 GPT-4V, Gemini Vision, LLaVA) 理解费曼图的能力。
    *   **负责人：** JYEU, Cline (bee)
*   **任务：**进行小范围实验，评估 VLM 从图表图片直接生成 TikZ 代码或结构化表示的性能。

### 5.2. 数据策略 (如需自定义模型/微调)
*   **任务：**制定费曼图图片及其对应 TikZ 代码的数据收集和标注规范。
    *   **负责人：** JYEU
*   **任务：**设计数据存储和管理方案。
    *   **负责人：** Cline (bee)

### 5.3. 技术设计
*   **任务：**基于调研和数据策略，设计图片转 TikZ 功能的技术架构。

## 技术栈 (当前)
*   **LLM API (生成)：** Google Gemini (例如 `gemini-1.5-pro-latest`)
*   **LLM API (嵌入)：** Google Gemini (例如 `text-embedding-004`)
*   **Agent 逻辑：** Python (`agents/tikz_feynman_agent.py`)
*   **知识库存储：** DuckDB (`data/feynman_kb.duckdb`)
*   **向量索引：** Annoy (`data/feynman_kb.ann`)
*   **CLI 工具：** Python + argparse (`run_agent_cli.py`)
*   **运行环境：** Conda (`tikz_mcp_env`)
*   **核心依赖：** `google-generativeai`, `python-dotenv`, `pydantic`, `duckdb`, `annoy`, `requests`, `tqdm`

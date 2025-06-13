# FeynmanCraft ADK

**多代理TikZ费曼图生成系统** - 基于Google Agent Development Kit (ADK)

![License](https://img.shields.io/badge/license-MIT%2FApache--2.0-blue)
![ADK](https://img.shields.io/badge/ADK-1.2.1-green)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)

## 🎯 项目简介

FeynmanCraft ADK 是一个基于 Google Agent Development Kit 构建的多代理系统，用于从自然语言描述自动生成高质量的 TikZ 费曼图代码。该项目旨在参加 **Google Cloud × ADK Hackathon**，提交截止日期为2025年6月23日。

### 核心特性 (目标)

- 🤖 **多代理协作**: 基于ADK框架的专业化代理系统 (规划中)
- 🧠 **知识驱动**: 通过知识库检索和 Few-shot 学习提升生成质量 (规划中)
- 🔬 **物理智能**: 内置物理规则验证和粒子数据库 (部分实现, 规划中)
- 📝 **自然语言输入**: 从描述直接生成TikZ代码 (MVP已实现)
- ⚡ **实时生成**: 快速生成可编译的LaTeX代码 (MVP已实现)
- 🕸️ **网络增强**: 可从网络获取信息以辅助生成 (规划中)
- 🔧 **可扩展架构**: 模块化设计，易于扩展新功能 (进行中)

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Google ADK 1.2.1+
- Conda (推荐, 用于管理环境 `fey`)
- LaTeX (可选，用于编译验证生成的TikZ代码)
- Google AI API Key (用于Gemini模型)

### 安装步骤

1.  **克隆项目**
    ```bash
    git clone <repository-url>
    cd feynmancraft-adk
    ```

2.  **创建并激活Conda环境** (推荐)
    ```bash
    conda create --name fey python=3.9 -y
    conda activate fey
    ```

3.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

4.  **设置环境变量**
    *   复制环境变量模板 (如果 `env.example` 存在, 否则手动创建 `.env`):
        ```bash
        # cp env.example .env 
        ```
    *   在项目根目录创建或编辑 `.env` 文件，并添加您的Google AI API密钥:
        ```env
        GOOGLE_API_KEY="your_google_ai_api_key_here"
        # Optional: Google Cloud Project for BigQuery
        # GOOGLE_CLOUD_PROJECT="your-gcp-project-id" 
        ```

5.  **运行代理 (MVP)**
    确保已激活 `fey` conda环境。
    ```bash
    cd feynmancraft-adk
    adk run app
    ```
    启动后，ADK Dev UI 会在本地端口 (通常是 `http://localhost:40000`) 打开，您可以在那里与 `OrchestratorAgent` 交互。

### 使用示例 (ADK Dev UI)

在 ADK Dev UI 中：
1.  选择 `OrchestratorAgent`。
2.  在输入框中输入自然语言描述，例如:
    ```
    electron positron annihilation to two photons
    ```
3.  点击 "Run"。系统会生成对应的TikZ代码和简要说明。

## 🏗️ 项目架构

### 当前实现 (MVP - 阶段2完成)

```
feynmancraft-adk/
├── app/                    # ADK应用入口 (符合ADK标准)
│   ├── __init__.py
│   └── agent.py            # root_agent (OrchestratorAgent) 定义
├── agents/                 # 代理实现
│   ├── __init__.py
│   ├── orchestrator_agent.py  # 主协调代理 (MVP核心)
│   ├── diagram_generator_agent.py # (存根)
│   ├── feedback_agent.py       # (存根)
│   ├── harvest_agent.py        # (存根)
│   ├── kb_retriever_agent.py   # (存根)
│   ├── physics_validator_agent.py # (存根)
│   ├── planner_agent.py        # (存根)
│   └── tikz_validator_agent.py # (部分实现 feyncore 调用)
├── feyncore/               # 核心功能库 (可复用组件)
│   ├── __init__.py
│   ├── physics/            # 物理数据和验证逻辑
│   ├── tikz_utils/         # TikZ工具函数
│   └── compilation/        # LaTeX编译器
├── schemas.py              # Pydantic数据模型定义
├── test_runner.py          # 简易本地测试脚本
├── requirements.txt        # Python依赖
├── README.md               # 本文档
└── legacy/                 # 原始项目代码 (MCP-for-Tikz, tikz-hunter)
```

### 代理系统 (MVP)

- **OrchestratorAgent**: 作为 `root_agent`，接收用户输入，使用内置的 `generate_tikz_diagram` 工具 (ADK tool) 来识别物理过程并直接生成TikZ代码。这是当前MVP的核心功能。
- 其他代理 (`PlannerAgent`, `KBRetrieverAgent`, `DiagramGeneratorAgent`, `TikZValidatorAgent`, `PhysicsValidatorAgent`, `FeedbackAgent`, `HarvestAgent`) 目前是基本存根，将在后续阶段逐步实现。

## 📋 开发计划

### ✅ 阶段0: 项目初始化 (已完成)
- [x] 创建 `feynmancraft-adk` 项目仓库。
- [x] 将 `MCP-for-Tikz-` 和 `tikz-hunter` 迁移到 `legacy/` 目录。
- [x] 添加 `LICENSE-MIT`, `LICENSE-APACHE`, 和基础 `README.md`。

### ✅ 阶段1: 核心库抽象 (已完成) 
- [x] 创建 `feyncore/` Python包。
- [x] **Physics**: 迁移粒子数据 (`particle_data.py` 等) 到 `feyncore/physics/`。创建 `physics_validator.py` 存根。
- [x] **TikZ Utilities**: 提取TikZ代码块逻辑到 `feyncore/tikz_utils/extractor.py`。
- [x] **Compilation**: 提取LaTeX编译逻辑到 `feyncore/compilation/compiler.py`。
- [x] 添加必要的 `__init__.py` 文件。

### ✅ 阶段2: ADK代理基础与MVP (已完成)
- [x] 创建 `agents/` 目录和所有代理的存根Python文件。
- [x] 定义 `schemas.py` Pydantic数据模型。
- [x] **OrchestratorAgent MVP**: 实现一个可工作的 `OrchestratorAgent`，它使用ADK的 `Tool` 功能（一个名为 `generate_tikz_diagram` 的函数）直接根据输入描述生成TikZ代码。这是当前可运行的MVP。
- [x] **ADK项目结构**: 调整项目结构 (`app/agent.py`, `app/__init__.py`) 以符合ADK标准，允许通过 `adk run app` 启动。
- [x] **环境与依赖**: 完善 `requirements.txt`，解决ADK版本和CLI运行问题。
- [x] **测试**: 确保MVP能在ADK Dev UI中成功运行并生成简单费曼图。

### 🔄 阶段3: 多代理扩展与知识库初步集成 (当前阶段)
- [ ] **KBRetrieverAgent**:
    - [ ] 实现与 **Google BigQuery** 的集成。
    - [ ] 定义BigQuery表结构 (例如: `reaction_id`, `description`, `tikz_code`, `particles`, `source`, `embedding_vector`).
    - [ ] 实现基于文本描述的相似度查询 (BigQuery的向量搜索或文本搜索)。
- [ ] **HarvestAgent**:
    - [ ] 集成 `legacy/tikz-hunter/agents/harvester_agent.py` 的核心逻辑。
    - [ ] 使用 `PyGithub` 搜索GitHub上的 `.tex` 文件。
    - [ ] 使用 `feyncore.tikz_utils.extractor` 提取TikZ代码块。
    - [ ] (可选) 使用一个简单的LLM调用 (类似ParserAgent的旧逻辑) 初步解析元数据 (topic, reaction, particles)。
    - [ ] 将收集和解析的数据写入 **Google BigQuery** 知识库。
- [ ] **DiagramGeneratorAgent**:
    - [ ] 修改以接收来自 `KBRetrieverAgent` 的 few-shot 示例。
    - [ ] 使用 `google.adk.Model` (`gemini-1.5-pro-latest`) 和组合的prompt (包含示例) 生成TikZ代码。
- [ ] **TikZValidatorAgent**:
    - [ ] 确保 `feyncore.compilation.compiler.compile_tikz_code` 能被正确调用。
    - [ ] 返回结构化的 `ValidationReport`。
- [ ] **PhysicsValidatorAgent**:
    - [ ] 实现基于 `feyncore.physics` 中粒子数据和守恒定律的初步验证逻辑。
    - [ ] 利用 `pdg` 包获取粒子信息。
- [ ] **OrchestratorAgent (增强)**:
    - [ ] 实现调用新的 `KBRetrieverAgent`, `DiagramGeneratorAgent`, `TikZValidatorAgent`, `PhysicsValidatorAgent` 的工作流。
    - [ ] **Web搜索**: 如果 `KBRetrieverAgent` 返回的示例不足或质量不高，则使用 `google.adk.tools.GoogleSearchTool` 搜索网络 (例如，搜索 "tikz feynman diagram for electron positron annihilation")。
    - [ ] 从搜索结果中尝试提取TikZ代码片段 (可能需要 `beautifulsoup4` 和 `feyncore.tikz_utils.extractor`) 作为临时的 few-shot 示例。

### 📅 阶段4: 完整工作流与高级验证 (计划中)
- [ ] **PlannerAgent**: 实现根据用户请求动态规划代理调用顺序的逻辑 (可能使用LLM)。
- [ ] **FeedbackAgent**: 聚合所有验证报告，生成最终用户反馈。
- [ ] **完整的多代理编排**: 在 `OrchestratorAgent` 中实现一个更复杂的、有条件分支和循环的 `google.adk.Workflow`。
- [ ] **错误处理与重试**: 在各代理和工作流中加入更健壮的错误处理和重试机制。

### 📅 阶段5: 知识库自学习与优化 (计划中)
- [ ] **KB写入**: 将成功生成并通过所有验证的TikZ图及其元数据写回BigQuery知识库 (由 `FeedbackAgent` 或 `OrchestratorAgent` 触发)。
- [ ] **Embedding生成**: 对于新加入知识库的条目，计算其描述的向量嵌入 (例如使用Vertex AI Embedding API或Gemini Embedding API) 并存入BigQuery，用于未来的相似度检索。
- [ ] **提示工程优化**: 基于测试和用户反馈持续优化各LLM的提示。

### 📅 阶段6: 部署与评估 (计划中)
- [ ] **Google Cloud部署**: 准备将代理系统部署到Cloud Run或Vertex AI Agent Engine。
- [ ] **Web界面 (可选)**: 基于Streamlit或React创建一个简单的Web界面。
- [ ] **性能评估**: 使用ADK的评估框架测试系统的准确性和鲁棒性。
- [ ] **文档完善**: 完成所有技术文档和用户手册。

## 🛠️ 技术栈

- **核心框架**: Google Agent Development Kit (ADK) 1.2.1
- **语言模型**: Google Gemini (e.g., `gemini-2.0-flash` for tools, `gemini-1.5-pro-latest` for generation)
- **数据验证**: Pydantic
- **物理数据**: PDG (Particle Data Group) package, `feyncore/physics`
- **LaTeX处理**: `feyncore/compilation`
- **知识库**: Google BigQuery (for storing and querying TikZ examples and embeddings)
- **代码采集**: PyGithub, BeautifulSoup4, lxml
- **开发环境**: Conda, Python 3.9+

## 🎨 支持的物理过程 (MVP - OrchestratorAgent Tool)

当前 `OrchestratorAgent` 内置工具支持的费曼图类型：

- ✅ 电子-正电子湮灭 → 双光子
- ✅ 电子轫致辐射 (电子发射光子)
- ✅ 缪子衰变
- ✅ 基础费米子传播
- 🔄 更多过程将在 `DiagramGeneratorAgent` 和知识库完善后通过LLM动态支持。

## 🧪 测试和验证

### 本地测试 (推荐使用 `test_runner.py`)
```bash
# (确保conda环境fey已激活)
cd feynmancraft-adk
python test_runner.py 
```
此脚本会尝试进行一些基础的代理功能测试。

### ADK Dev UI 集成测试
```bash
# (确保conda环境fey已激活)
cd feynmancraft-adk
adk run app
```
然后在浏览器中打开 `http://localhost:40000` (或ADK指定的端口) 与 `OrchestratorAgent` 交互。

## 📚 比赛信息

本项目专为 **Google Cloud × ADK Hackathon** 开发：

- **类别**: Content Creation and Generation
- **目标**: 多代理协作自动生成科学内容 (TikZ费曼图)
- **截止日期**: 2025年6月23日
- **技术亮点**: 
  - ADK多代理架构
  - BigQuery知识库集成与检索
  - 结合LLM的物理过程理解与代码生成
  - 网络搜索增强的知识获取

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启Pull Request

## 📄 许可证

本项目采用双许可证：

- MIT License - 详见 [LICENSE-MIT](LICENSE-MIT)
- Apache License 2.0 - 详见 [LICENSE-APACHE](LICENSE-APACHE)

## 🔗 相关链接

- [Google ADK 文档](https://google.github.io/adk-docs/)
- [Google Cloud ADK Hackathon](https://cloud.google.com/adk-hackathon) (假设链接)
- [TikZ-Feynman 文档](https://ctan.org/pkg/tikz-feynman)

---

**Built with ❤️ for the physics and AI community** 
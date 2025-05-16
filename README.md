# MCP-for-Tikz-



## 🧭 项目计划：MCP for TikZ Feynman

### 🧩 项目概述

**MCP for TikZ Feynman** 是一个开源 AI Agent 项目，致力于通过自然语言、结构化描述或图形化界面，**自动生成 TikZ Feynman 费曼图代码**，加速物理科研人员在 LaTeX 中的图像构建效率。该项目基于 Model Context Protocol（MCP）进行构建，支持未来拓展到 VSCode / Overleaf / JupyterLab 插件生态。

---

### 🎯 项目目标（Objectives）

| 阶段      | 目标                                                 |
| ------- | -------------------------------------------------- |
| Phase 1 | 实现一个能够将自然语言描述转化为 TikZ 费曼图代码的 LLM Agent（基础模型）       |
| Phase 2 | 实现语法检查、图像预览（通过 LaTeX 编译或预渲染）与一键复制功能                |
| Phase 3 | 构建 Playground Web UI 和 REST API 接口，支持在线交互          |
| Phase 4 | 实现 VSCode 插件支持 MCP 插入 TikZ-Feynman 模板              |
| Phase 5 | 拓展 Agent 支持 `.docx` 转 `.tex`、BibTeX 管理等 LaTeX 生态任务 |

---

### 🏗️ 项目模块划分

| 模块                  | 功能说明                                                         |
| ------------------- | ------------------------------------------------------------ |
| Prompt Engine       | Few-shot Prompt + Function Calling                           |
| TikZ Code Generator | 根据结构化描述输出 TikZ 代码                                            |
| Feynman DSL Parser  | 自定义 Domain-Specific Language（如 `electron -> photon -> muon`） |
| Playground UI       | 用于展示、调试、输出图形与代码的 Web 界面（Streamlit/FastAPI）                   |
| MCP Agent Wrapper   | 封装 CrewAI/AutoGen/OpenDevin等多 Agent 框架适配层                    |
| Data & Template     | 内置 TikZ-Feynman 模板库与训练/测试数据集                                 |

---

### 🧪 技术路线

* 使用 GPT-4o / Claude / Qwen2.5-VL 作为初始 Agent 模型
* 构建 Prompt 模板以支持：

  * 自然语言 → TikZ代码
  * 粒子过程 → 有向图描述 → TikZ
* 构建 Dataset：

  * arXiv 抓取 `.tex` 代码（含 tikz-feynman 环节）
  * 收集结构化物理过程描述
* 构建 DSL 转 TikZ 映射规则
* 后续计划训练专用模型用于代码生成微调（LLaMA/CodeGemma）

---

### 🧑‍💻 项目成员与分工（建议）

| 成员    | 职责                        |
| ----- | ------------------------- |
| bee   | 技术统筹、Prompt 架构设计、API 实现   |
| JYEU  | 物理学科专家、TikZ调研、数据标注与测试用例设计 |
| （待招募） | Web前端 + VSCode插件开发        |

---

### 🧱 预期交付物（MVP）

1. MCP Agent 接口，支持自然语言输入输出 TikZ 费曼图代码
2. 图像预览功能，编译并展示结果图（调用 pdflatex + ImageMagick）
3. 支持结构化物理过程输入格式（如 QED/QCD）
4. 提供多个 Prompt 示例、TikZ 图代码和输出结果
5. 代码开源，MIT License，适配 CrewAI / AutoGen 接口

---

### 📆 时间线（Milestone）

| 时间节点    | 目标内容                                                     |
| ------- | -------------------------------------------------------- |
| Week 1  | 创建 GitHub Repo，搭建项目框架，初始数据收集与 prompt 设计                  |
| Week 2  | 构建 MVP：自然语言 → TikZ Generator（CLI/Notebook 原型）            |
| Week 3  | 构建 Playground（Streamlit UI），实现图像预览与代码复制功能                |
| Week 4  | 构建 MCP Agent Wrapper，集成 VSCode 插件初版，撰写开发文档               |
| Week 5+ | 提交 arXiv / 会议 poster 作为 showcase，拉 GitHub star、投稿比赛或申请资助 |

---

### 📚 附录：参考工具 & 依赖组件

* [`tikz-feynman`](https://ctan.org/pkg/tikz-feynman)
* [`CrewAI`](https://docs.crewai.io)
* [`LangChain`](https://www.langchain.com/)
* [`AutoGen`](https://microsoft.github.io/autogen/)
* [`Qwen-VL`](https://huggingface.co/Qwen/Qwen1.5-VL)
* [`arXiv API`](https://arxiv.org/help/api)

---

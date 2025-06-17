# FeynmanCraft ADK

**智能多代理TikZ费曼图生成系统** - 基于Google Agent Development Kit (ADK) v1.0.0

![Version](https://img.shields.io/badge/version-0.2.0-brightgreen)
![License](https://img.shields.io/badge/license-MIT%2FApache--2.0-blue)
![ADK](https://img.shields.io/badge/ADK-1.0.0-green)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-Beta-yellow)

## 🎯 项目简介

FeynmanCraft ADK 是一个基于 Google Agent Development Kit 构建的**自主学习智能研究助手**，能够从自然语言描述自动生成高质量的 TikZ 费曼图代码。该项目采用创新的**三层知识获取架构**，具备动态网络搜索和持续学习能力。

### 🚀 核心创新

- 🧠 **三层知识架构**: 静态知识库 + 动态网络搜索 + 智能生成
- 🔍 **自主学习能力**: 遇到未知问题时主动搜索学习
- 🤖 **7代理协作系统**: 专业化代理分工协作
- 📊 **BigQuery知识库**: 高性能向量搜索和语义检索
- 🌐 **WebResearchAgent**: 实时网络知识补充
- 🔬 **物理智能验证**: 多层物理正确性检查
- ⚡ **智能路由决策**: 基于查询质量的自动路径选择

## 🏗️ 系统架构

### 三层知识获取架构

```
Layer 1: 静态知识库 (BigQuery) ← tikz-hunter 离线构建
    ↓ (知识库不足时)
Layer 2: 动态网络搜索 (WebResearchAgent) ← 实时补充
    ↓ (完全未知时)
Layer 3: 智能生成 (DiagramGeneratorAgent) ← 创新合成
```

### 智能工作流

```
用户请求 → PlannerAgent → OrchestratorAgent
    ↓
决策分支:
├─ 知识库充足 → KBRetrieverAgent → DiagramGeneratorAgent
├─ 知识库不足 → WebResearchAgent → 验证链 → DiagramGeneratorAgent  
└─ 完全未知 → 创新生成模式 → 强化验证

验证链: TikZValidator → PhysicsValidator → FeedbackAgent
```

## 🤖 代理系统

### 核心代理 (7个)

1. **OrchestratorAgent** - 智能路由器和决策中心
2. **PlannerAgent** - 物理过程解析和任务规划
3. **KBRetrieverAgent** - BigQuery知识库检索专家
4. **WebResearchAgent** - 动态网络搜索专家 ⭐ 新增
5. **DiagramGeneratorAgent** - TikZ-Feynman代码生成专家
6. **TikZValidatorAgent** - LaTeX编译验证
7. **PhysicsValidatorAgent** - 物理正确性验证
8. **FeedbackAgent** - 结果聚合和用户反馈

### tikz-hunter 集成

- **定位**: 离线知识库生产工厂
- **功能**: 批量采集、清洗、验证TikZ数据
- **输出**: 高质量结构化数据 → BigQuery
- **运行模式**: 定期批处理，不参与实时请求

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Google ADK 1.0.0+
- Conda (推荐)
- LaTeX (可选，用于本地编译验证)
- Google AI API Key
- Google Cloud Project (用于BigQuery)

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd feynmancraft-adk
   ```

2. **创建Conda环境**
   ```bash
   conda create --name fey python=3.11 -y
   conda activate fey
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **配置环境变量**
   ```bash
   # 创建 .env 文件
   cat > .env << EOF
   GOOGLE_API_KEY="your_google_ai_api_key_here"
   GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
   ADK_MODEL_NAME="gemini-2.0-flash"  # 可选，默认值
   EOF
   ```

5. **运行系统**
   ```bash
   conda run -n fey adk run feynmancraft_adk
   ```

### 使用示例

在 ADK Dev UI 中输入：

```
请生成一个电子-正电子湮灭产生两个光子的费曼图
```

系统将：
1. 🔍 首先查询BigQuery知识库
2. 🌐 如需要，进行网络搜索补充
3. 🎨 生成高质量TikZ代码
4. ✅ 进行物理和语法验证
5. 📝 提供详细反馈和建议

## 📊 项目结构

```
feynmancraft-adk/
├── feynmancraft_adk/           # 主包 (ADK标准结构)
│   ├── __init__.py            # 模型配置和日志设置
│   ├── agent.py               # root_agent定义
│   ├── schemas.py             # Pydantic数据模型
│   ├── sub_agents/            # 代理实现
│   │   ├── orchestrator_agent.py
│   │   ├── planner_agent.py
│   │   ├── kb_retriever_agent.py
│   │   ├── web_research_agent.py  # 🆕 网络搜索代理
│   │   ├── diagram_generator_agent.py
│   │   ├── tikz_validator_agent.py
│   │   ├── physics_validator_agent.py
│   │   └── feedback_agent.py
│   ├── shared_libraries/       # 共享工具库
│   │   ├── prompt_utils.py
│   │   ├── tikz_compiler.py
│   │   └── config.py
│   └── tools/                 # 工具函数
│       ├── bigquery_kb_tool.py    # 🆕 BigQuery集成
│       ├── web_search_tool.py     # 🆕 网络搜索工具
│       └── vector_search_tool.py  # 🆕 向量搜索
├── feyncore/                  # 核心功能库
│   ├── physics/               # 物理数据和验证
│   ├── tikz_utils/           # TikZ工具函数
│   └── compilation/          # LaTeX编译器
├── tikz-hunter/              # 离线数据采集系统
├── legacy/                   # 历史代码
├── DEVELOPMENTplan.md        # 详细开发计划
└── README.md                 # 本文档
```

## 🎯 技术指标

### 性能目标
- ✅ TikZ代码编译成功率 ≥ 85%
- ✅ 物理验证准确率 ≥ 90%
- ✅ 知识库查询响应时间 ≤ 3秒
- ✅ 端到端处理时间 ≤ 45秒 (含网络搜索)
- ✅ 系统可用性 ≥ 95%

### 智能化指标
- ✅ 知识库命中率 ≥ 80%
- ✅ 网络搜索成功率 ≥ 70%
- ✅ 用户满意度 ≥ 90%
- ✅ 知识库自动扩充率 ≥ 10条/天
- ✅ 重复查询网络依赖下降率 ≥ 50%

## 🔬 支持的物理过程

### 当前支持 (基础版本)
- ✅ 电子-正电子湮灭 → 双光子
- ✅ 缪子衰变 → 电子 + 中微子
- ✅ 质子-反质子散射
- ✅ W/Z玻色子衰变
- ✅ 康普顿散射

### 扩展支持 (通过网络搜索)
- 🔍 QCD过程 (胶子交换)
- 🔍 希格斯机制相关过程
- 🔍 超对称粒子过程
- 🔍 中微子振荡
- 🔍 暗物质相互作用

## 🛠️ 技术栈

### 核心框架
- **Google ADK 1.0.0** - 多代理编排框架
- **Google Gemini** - 语言模型 (gemini-2.0-flash)
- **BigQuery** - 知识库存储和向量搜索
- **Pydantic** - 数据验证和序列化

### 专业工具
- **TikZ-Feynman** - 费曼图绘制
- **LaTeX** - 文档编译
- **PDG Package** - 粒子数据
- **Google Search API** - 网络搜索
- **Vertex AI** - 向量嵌入

### 开发工具
- **Conda** - 环境管理
- **pytest** - 测试框架
- **GitHub Actions** - CI/CD
- **Docker** - 容器化部署

## 📈 开发进度

### ✅ 已完成 (75%)
- **Core Architecture**: ADK框架完全就位
- **Data Models**: 完整的Pydantic数据模型
- **Agent Framework**: 6个专业代理已配置
- **Basic Utilities**: TikZ编译、配置系统等

### 🟡 进行中 (20%)
- **BigQuery Integration**: 知识库迁移
- **WebResearchAgent**: 网络搜索能力
- **Agent Prompts**: 专业化提示词优化

### ❌ 待开始 (5%)
- **Learning Mechanisms**: 自主学习能力
- **Advanced Validation**: 高级物理验证
- **Performance Optimization**: 性能优化

## 🎯 项目里程碑

### 第1-2天: 知识库基础设施 🗄️
- BigQuery表结构设计和数据迁移
- tikz-hunter数据集成
- 基础查询工具开发

### 第3-4天: 智能决策层 🧠
- OrchestratorAgent升级为智能路由器
- 多路径决策逻辑实现
- DiagramGeneratorAgent提示词优化

### 第5-6天: 动态网络研究 🔍
- WebResearchAgent开发
- Google Search API集成
- 搜索结果质量过滤

### 第7-8天: 系统集成 🔄
- 物理验证系统强化
- 完整工作流集成
- 智能路由测试

### 第9-10天: 优化部署 🚀
- 智能缓存和学习机制
- 全面测试和性能优化
- 文档完善和交付准备

## 📦 最新版本

### v0.2.0 (2025-01-17)
- 🎯 **双模式知识库系统**：BigQuery（生产）+ 本地（开发）
- 🔍 **向量搜索**：基于 Annoy 的高性能相似度搜索
- 🔄 **智能切换**：自动故障转移和混合搜索策略
- 📊 **多种搜索方式**：语义搜索、关键词搜索、粒子搜索
- ⚙️ **灵活配置**：通过环境变量控制系统行为

详见 [CHANGELOG.md](CHANGELOG.md)

## 🏆 创新亮点

### 自适应智能系统
1. **知识边界感知**: 系统能识别自己的知识盲区
2. **主动学习能力**: 遇到未知问题时主动搜索学习
3. **质量自我监控**: 持续评估和改进输出质量
4. **用户反馈驱动**: 基于用户反馈优化决策逻辑

### 三层容错机制
1. **Layer 1**: 静态知识库 (最快，最可靠)
2. **Layer 2**: 动态网络搜索 (中等速度，高覆盖)
3. **Layer 3**: 创新生成 (最慢，但能处理全新问题)

## 🤝 贡献指南

我们欢迎社区贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

### 开发环境设置
```bash
# 克隆项目
git clone <repository-url>
cd feynmancraft-adk

# 设置开发环境
conda create --name fey-dev python=3.9 -y
conda activate fey-dev
pip install -r requirements-dev.txt

# 运行测试
pytest tests/

# 代码格式化
black feynmancraft_adk/
isort feynmancraft_adk/
```

## 📄 许可证

本项目采用双许可证：
- [MIT License](LICENSE-MIT)
- [Apache License 2.0](LICENSE-APACHE)

您可以选择其中任一许可证使用本项目。

## 🙏 致谢

- **Google ADK Team** - 提供强大的多代理开发框架
- **TikZ-Feynman Community** - 优秀的费曼图绘制工具
- **Particle Data Group** - 权威的粒子物理数据
- **开源社区** - 无数优秀的开源工具和库

## 📞 联系方式

- **项目主页**: [GitHub Repository](https://github.com/your-username/feynmancraft-adk)
- **问题反馈**: [GitHub Issues](https://github.com/your-username/feynmancraft-adk/issues)
- **讨论交流**: [GitHub Discussions](https://github.com/your-username/feynmancraft-adk/discussions)

---

**FeynmanCraft ADK - 让物理图表生成变得智能而简单** 🚀 
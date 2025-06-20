# Particle Physics Agent

**智能多代理TikZ费曼图生成系统** - 基于Google Agent Development Kit (ADK) v1.0.0

![Version](https://img.shields.io/badge/version-0.3.4-brightgreen)
![License](https://img.shields.io/badge/license-MIT%2FApache--2.0-blue)
![ADK](https://img.shields.io/badge/ADK-1.0.0-green)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-Beta-yellow)

## 🎯 项目简介

Particle Physics Agent 是一个基于 Google Agent Development Kit 构建的**自主学习智能研究助手**，能够从自然语言描述自动生成高质量的 TikZ 费曼图代码。该项目采用创新的**双重验证架构**，具备MCP增强的物理验证能力。

### 🚀 核心创新

- 🧠 **双重验证架构**: 内部物理工具 + MCP工具交叉验证
- 🔍 **MCP工具集成**: 20+专业粒子物理MCP工具自动触发
- 🤖 **6代理协作系统**: 精简专业化代理分工协作
- 📊 **本地知识库**: Annoy向量搜索 + JSON关键词搜索混合检索
- 🔬 **增强物理验证**: 150+粒子的详细物理属性验证
- 🌐 **自然语言处理**: 支持中英文物理过程描述
- ⚡ **智能路由决策**: 基于查询质量的自动路径选择
- 📐 **TikZ代码生成**: 发布级质量的LaTeX费曼图代码

## 🏗️ 系统架构

### 智能工作流

```
用户请求 → PlannerAgent → KBRetrieverAgent → PhysicsValidatorAgent (MCP) 
    ↓                              ↓                    ↓
自然语言解析 → 混合知识库搜索 → MCP增强物理验证
    ↓                              ↓                    ↓
DiagramGeneratorAgent → TikZValidatorAgent → FeedbackAgent
    ↓                              ↓                    ↓
TikZ代码生成 → LaTeX编译验证 → 最终响应合成
```

**MCP工具在每次物理验证阶段自动触发**，提供:
- 双重验证：内部工具 + MCP工具交叉验证
- 增强数据：150+粒子的详细物理属性
- 智能诊断：粒子查找错误的自动诊断和建议

## 🤖 代理系统

### 核心代理 (6个)

1. **PlannerAgent** - 自然语言解析和任务规划
2. **KBRetrieverAgent** - 本地向量搜索和关键词检索
3. **PhysicsValidatorAgent** - MCP增强的物理正确性验证
4. **DiagramGeneratorAgent** - TikZ-Feynman代码生成专家
5. **TikZValidatorAgent** - LaTeX编译验证
6. **FeedbackAgent** - 结果聚合和用户反馈

### MCP工具集成 (20+工具)

**PhysicsValidatorAgent** 集成了完整的MCP粒子物理工具包:
- **粒子搜索**: `search_particle_mcp` - 高级粒子数据库搜索
- **属性获取**: `get_particle_properties_mcp` - 详细粒子属性
- **量子数验证**: `validate_quantum_numbers_mcp` - 高级量子数验证
- **衰变分析**: `get_branching_fractions_mcp` - 衰变模式分析
- **粒子比较**: `compare_particles_mcp` - 多粒子属性比较
- **单位转换**: `convert_units_mcp` - 物理单位智能转换
- **属性检查**: `check_particle_properties_mcp` - 综合属性验证

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Google ADK 1.0.0+
- Conda (推荐) 或 Docker
- LaTeX (可选，用于本地编译验证)
- Google AI API Key
- 可选：Google Cloud Project (用于部署)

### Docker 部署 (推荐)

使用 Docker 可以快速部署完整的 TeX Live 环境和所有依赖：

```bash
# 1. 克隆项目
git clone <repository-url>
cd Particle-Physics-Agent

# 2. 配置环境变量
cp env.template .env
# 编辑 .env 文件，添加你的 Google API Key

# 3. 运行构建和测试脚本
./scripts/build-and-test.sh

# 4. 启动服务
docker-compose up -d feynmancraft
```

访问 `http://localhost:8080` 开始使用！

### 开发模式 (Docker)
```bash
# 开发模式启动 (支持热重载)
docker-compose --profile dev up -d feynmancraft-dev
# 访问 http://localhost:40000
```

### 本地安装步骤

如果你选择本地安装而不使用 Docker：

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd Particle-Physics-Agent
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

5. **启动Web界面**
   ```bash
   cd feynmancraft_adk
   adk web . --port 8000
   ```
   
   打开浏览器访问 `http://localhost:8000` 开始使用

### 使用示例

**启动Web界面**：
```bash
cd feynmancraft_adk
adk web . --port 8000
```

在Web界面中输入：
```
请生成一个电子-正电子湮灭产生两个光子的费曼图
```

**系统工作流程**：
1. 📋 **PlannerAgent** - 解析自然语言并制定执行计划
2. 📚 **KBRetrieverAgent** - 搜索相关TikZ示例
3. 🔬 **PhysicsValidatorAgent** - 使用MCP工具验证物理正确性
4. 🎨 **DiagramGeneratorAgent** - 生成TikZ代码
5. ✅ **TikZValidatorAgent** - LaTeX编译验证
6. 📝 **FeedbackAgent** - 综合最终响应

## 📊 项目结构

```
Particle-Physics-Agent/
├── feynmancraft_adk/           # 主包 (ADK标准结构)
│   ├── __init__.py            # 模型配置和日志设置
│   ├── agent.py               # root_agent定义
│   ├── schemas.py             # Pydantic数据模型
│   ├── data/                  # 知识库数据文件
│   │   ├── feynman_kb.json        # 本地知识库
│   │   ├── pprules.json           # 物理规则数据
│   │   └── embeddings/            # 向量嵌入缓存
│   ├── sub_agents/            # 6个核心代理实现
│   │   ├── planner_agent.py           # 自然语言解析和规划
│   │   ├── kb_retriever_agent.py      # 知识库检索
│   │   ├── physics_validator_agent.py # MCP增强物理验证
│   │   ├── diagram_generator_agent.py # TikZ代码生成
│   │   ├── tikz_validator_agent.py    # LaTeX编译验证
│   │   ├── feedback_agent.py          # 结果聚合反馈
│   │   └── code_agent.py              # 工具函数
│   ├── shared_libraries/       # 共享工具库
│   │   ├── config.py              # 环境配置
│   │   ├── prompt_utils.py        # 提示词工具
│   │   └── physics/               # 物理数据和工具
│   ├── integrations/           # 外部服务集成
│   │   └── mcp/                   # MCP工具集成
│   │       ├── mcp_client.py          # MCP客户端
│   │       ├── mcp_config.json        # MCP配置
│   │       └── particle_name_mappings.py # 粒子名称映射
│   ├── tools/                 # 工具函数
│   │   ├── kb/                    # 知识库工具
│   │   │   ├── bigquery.py            # BigQuery集成 (未使用)
│   │   │   ├── local.py               # 本地向量搜索
│   │   │   ├── search.py              # 统一搜索接口
│   │   │   ├── data_loader.py         # 数据加载器
│   │   │   └── embedding_manager.py   # 嵌入管理
│   │   ├── physics/               # 物理工具
│   │   │   ├── physics_tools.py       # MCP物理工具
│   │   │   ├── search.py              # 物理规则搜索
│   │   │   ├── data_loader.py         # 物理数据加载
│   │   │   └── embedding_manager.py   # 物理嵌入管理
│   │   ├── integrations/          # 集成工具接口 (直接使用../integrations/mcp)
│   │   └── latex_compiler.py      # LaTeX编译器
│   ├── docs/                  # 项目文档
│   │   ├── AGENT_TREE.md          # 代理架构文档
│   │   └── bigquery_setup.md      # BigQuery设置指南 (未使用)
│   └── scripts/               # 部署和管理脚本
│       ├── build_local_index.py   # 构建本地索引
│       ├── upload_to_bigquery.py  # 上传到BigQuery (未使用)
│       └── release.py             # 发布脚本
├── requirements.txt           # Python依赖
├── scripts/                   # 构建和部署脚本
│   └── build-and-test.sh         # Docker构建和测试管道
├── docker-compose.yml         # Docker编排配置
├── Dockerfile                 # Docker镜像构建
├── env.template               # 环境变量模板
├── QUICKSTART.md             # 快速启动指南
├── DEVELOPMENTplan.md        # 开发计划
├── CHANGELOG.md              # 更新日志
├── VERSION                   # 版本信息
└── README.md                 # 本文档
```

## 🛠️ 技术栈

### 核心框架
- **Google ADK 1.0.0** - 多代理编排框架
- **Google Gemini** - 语言模型 (gemini-2.0-flash)
- **MCP (Model Context Protocol)** - 增强的工具通信协议
- **Pydantic** - 数据验证和序列化

### 专业工具
- **TikZ-Feynman** - 费曼图绘制
- **LaTeX** - 文档编译
- **MCP Particle Physics Tools** - 20+专业粒子物理工具
- **Annoy** - 本地向量相似性搜索
- **Vertex AI** - 向量嵌入生成

### 开发工具
- **Conda** - 环境管理
- **pytest** - 测试框架
- **GitHub Actions** - CI/CD
- **Docker** - 容器化部署
- **TeX Live 2022** - 完整的 LaTeX 环境
- **Build Pipeline** - 自动化构建和测试基础设施

## 🎯 项目里程碑

### ✅ 已完成里程碑
- **第一阶段**: 核心ADK框架和6代理系统 ✅
- **第二阶段**: MCP工具集成和双重验证 ✅
- **第三阶段**: 混合知识库和智能路由 ✅
- **第四阶段**: 项目优化和代码清理 ✅
- **第五阶段**: Docker部署和构建基础设施 ✅

### 🎯 下一步计划
- **性能优化**: 提升响应速度和资源效率
- **扩展测试**: 更多物理过程和边缘案例
- **云原生部署**: Kubernetes支持和自动扩缩容
- **监控和观测**: 添加应用性能监控和日志聚合

## 📦 最新版本

### v0.3.4 - Docker 部署与构建基础设施版本
- 🐳 **Docker 支持**：完整的容器化部署，包含 TeX Live 2022 和 TikZ-Feynman 支持
- 🛠️ **构建和测试管道**：全面的验证流水线 (`scripts/build-and-test.sh`)
  - Docker 镜像构建验证
  - TeX Live 安装测试
  - TikZ 包编译验证
  - FeynmanCraft LaTeX 编译器测试
  - 费曼图编译质量评分
  - 服务集成测试和健康检查
- 🔧 **依赖修复**：解决包版本冲突和构建问题
  - 修复 PDG 包版本从 `>=0.3.0` 到 `>=0.2.0`
  - 添加构建依赖工具用于 C++ 包编译
  - 解决 Docker 环境中 Annoy 包编译问题
- 📁 **架构清理**：精简 MCP 集成层，移除不必要的包装器
- 📝 **文档准确性**：全面的事实核查和修正，移除误导性的 BigQuery 声明

### v0.3.3 - 工作流增强版本
- 🔄 **分支管理优化**：将`hackathon`分支重命名为`main`，清理代码库结构
- 📝 **文档完善**：更新README项目结构图，修正目录结构和文件列表
- 🔧 **工作流分析**：识别并记录代理工作流执行不完整的问题
- 🌐 **Web界面改进**：改进ADK web服务器部署和代理检测
- 🛠️ **MCP工具调试**：调查并解决PDG包依赖和MCP连接问题

### v0.3.2 - 项目重构版本
- 📁 **项目结构优化**：将`docs/`和`scripts/`移入`feynmancraft_adk/`目录
- 📄 **许可证合并**：将MIT和Apache 2.0双许可证合并为单一LICENSE文件
- 🔧 **ADK兼容性修复**：修复ADK Web UI中的代理检测问题
- 📝 **文档更新**：更新所有文档中的路径引用

### v0.3.1 - 项目优化版本
- 🗑️ **代码清理**：移除未使用的OrchestratorAgent和HarvestAgent
- ⚡ **架构精简**：聚焦6个核心代理的生产级工作流
- 📝 **文档更新**：更新README和项目结构反映优化后的代码库
- 🔧 **导入优化**：清理sub_agents模块导入结构

详见 [CHANGELOG.md](CHANGELOG.md)

## 🏆 创新亮点

### MCP增强的智能验证系统 🔬
1. **双重验证机制**: 每次物理验证自动触发内部工具+MCP工具双重验证
2. **专业粒子数据库**: 150+粒子的详细物理属性、量子数、衰变模式
3. **智能错误诊断**: 粒子查找失败时自动提供建议和修正
4. **教育友好**: 对复杂物理过程提供深入的教育解释

### 本地知识架构
1. **向量语义搜索**: Annoy索引实现快速相似性搜索
2. **关键词精确匹配**: JSON数据的文本和粒子搜索
3. **混合检索策略**: 自动结合向量搜索和关键词匹配
4. **持续学习**: 基于用户反馈的知识库扩充

### 工作流智能化
1. **自然语言理解**: 支持中英文物理过程描述
2. **完整代理序列**: 六代理协作确保全面验证
3. **质量自我监控**: 持续评估和改进输出质量
4. **教育模式**: 对无法图示的过程提供教育解释

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

本项目采用双许可证：MIT License 和 Apache License 2.0。

请查看 [LICENSE](LICENSE) 文件了解详细信息。您可以选择其中任一许可证使用本项目。

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
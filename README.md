# FeynmanCraft ADK

**智能多代理TikZ费曼图生成系统** - 基于Google Agent Development Kit (ADK) v1.0.0

![Version](https://img.shields.io/badge/version-0.3.1-brightgreen)
![License](https://img.shields.io/badge/license-MIT%2FApache--2.0-blue)
![ADK](https://img.shields.io/badge/ADK-1.0.0-green)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-Beta-yellow)

## 🎯 项目简介

FeynmanCraft ADK 是一个基于 Google Agent Development Kit 构建的**自主学习智能研究助手**，能够从自然语言描述自动生成高质量的 TikZ 费曼图代码。该项目采用创新的**双重验证架构**，具备MCP增强的物理验证能力。

### 🚀 核心创新

- 🧠 **双重验证架构**: 内部物理工具 + MCP工具交叉验证
- 🔍 **MCP工具集成**: 20+专业粒子物理MCP工具自动触发
- 🤖 **6代理协作系统**: 精简专业化代理分工协作
- 📊 **混合知识库**: BigQuery + 本地向量搜索自动切换
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
2. **KBRetrieverAgent** - BigQuery/本地知识库混合检索
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
│   └── tools/                 # 工具函数
│       ├── bigquery_kb_tool.py    # BigQuery集成
│       └── local_kb_tool.py       # 本地向量搜索
├── feyncore/                  # 核心功能库
│   ├── compilation/           # LaTeX编译器
│   └── tikz_utils/           # TikZ工具函数
├── docs/                     # 项目文档
├── scripts/                  # 部署和管理脚本
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
- **MCP (Model Context Protocol)** - 增强的工具通信协议
- **BigQuery** - 知识库存储和向量搜索
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

## 📈 开发进度

### ✅ 已完成 (90%)
- **Core Architecture**: ADK框架完全就位，6代理工作流优化
- **Data Models**: 完整的Pydantic数据模型
- **Agent Framework**: 6个专业代理已配置并测试通过
- **MCP Integration**: 20+物理工具集成和双重验证系统
- **Knowledge Base**: BigQuery + 本地向量搜索混合系统
- **Physics Validation**: 增强的物理验证与教育功能
- **Documentation**: 完整的项目文档和使用指南

### 🟡 进行中 (8%)
- **Performance Optimization**: 响应时间和资源使用优化
- **Extended Testing**: 边缘案例和错误处理完善
- **User Experience**: 界面优化和用户反馈集成

### ❌ 计划中 (2%)
- **Web Interface**: 独立Web界面开发
- **API Endpoints**: RESTful API接口开发

## 🎯 项目里程碑

### ✅ 已完成里程碑
- **第一阶段**: 核心ADK框架和6代理系统 ✅
- **第二阶段**: MCP工具集成和双重验证 ✅
- **第三阶段**: 混合知识库和智能路由 ✅
- **第四阶段**: 项目优化和代码清理 ✅

### 🎯 下一步计划
- **性能优化**: 提升响应速度和资源效率
- **扩展测试**: 更多物理过程和边缘案例
- **生产部署**: Docker容器化和云原生部署

## 📦 最新版本

### v0.3.1 (2025-01-17) - 项目优化版本
- 🗑️ **代码清理**：移除未使用的OrchestratorAgent和HarvestAgent
- ⚡ **架构精简**：聚焦6个核心代理的生产级工作流
- 📝 **文档更新**：更新README和项目结构反映优化后的代码库
- 🔧 **导入优化**：清理sub_agents模块导入结构

### v0.3.0 (2025-01-17) - MCP集成版本
- 🔬 **MCP工具集成**：20+粒子物理MCP工具自动触发
- 🎯 **双重验证系统**：内部工具 + MCP工具交叉验证
- 🔍 **智能粒子搜索**：综合粒子数据库with诊断功能
- 📊 **增强物理验证**：详细粒子属性、量子数、衰变分析
- ⚙️ **工作流优化**：确保完整的六代理序列执行
- 🔄 **混合知识库**：BigQuery + 本地向量搜索自动切换

详见 [CHANGELOG.md](CHANGELOG.md)

## 🏆 创新亮点

### MCP增强的智能验证系统 🔬
1. **双重验证机制**: 每次物理验证自动触发内部工具+MCP工具双重验证
2. **专业粒子数据库**: 150+粒子的详细物理属性、量子数、衰变模式
3. **智能错误诊断**: 粒子查找失败时自动提供建议和修正
4. **教育友好**: 对复杂物理过程提供深入的教育解释

### 自适应知识架构
1. **BigQuery生产级**: 高性能向量搜索和语义检索
2. **本地开发模式**: Annoy向量索引的快速原型开发
3. **智能降级**: 自动故障转移和混合搜索策略
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
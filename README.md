# FeynmanCraft ADK

**多代理TikZ费曼图生成系统** - 基于Google Agent Development Kit (ADK)

![License](https://img.shields.io/badge/license-MIT%2FApache--2.0-blue)
![ADK](https://img.shields.io/badge/ADK-1.2.1-green)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)

## 🎯 项目简介

FeynmanCraft ADK 是一个基于 Google Agent Development Kit 构建的多代理系统，用于从自然语言描述自动生成高质量的 TikZ 费曼图代码。该项目旨在参加 **Google Cloud × ADK Hackathon**，提交截止日期为2025年6月23日。

### 核心特性

- 🤖 **多代理协作**: 基于ADK框架的专业化代理系统
- 🔬 **物理智能**: 内置物理验证和粒子数据库
- 📝 **自然语言输入**: 从描述直接生成TikZ代码
- ⚡ **实时生成**: 快速生成可编译的LaTeX代码
- 🔧 **可扩展架构**: 模块化设计，易于扩展新功能

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Google ADK 1.2.1+
- LaTeX (可选，用于编译验证)

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd feynmancraft-adk
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **设置环境变量**
```bash
# 复制环境变量模板
cp env.example .env
# 编辑.env文件，添加您的Google AI API密钥
```

4. **运行代理**
```bash
adk run app
```

### 使用示例

启动后，您可以输入自然语言描述：

```
[user]: electron positron annihilation to two photons
```

系统会生成对应的TikZ代码：

```latex
\begin{tikzpicture}
  \begin{feynman}
    \vertex (a) {\(e^-\)};
    \vertex [right=of a] (b);
    \vertex [right=of b] (c) {\(\gamma\)};
    \vertex [below=of a] (d) {\(e^+\)};
    \vertex [below=of c] (e) {\(\gamma\)};
    \diagram* {
      (a) -- [fermion] (b) -- [photon] (c),
      (d) -- [anti fermion] (b) -- [photon] (e)
    };
  \end{feynman}
\end{tikzpicture}
```

## 🏗️ 项目架构

### 当前实现 (MVP)

```
feynmancraft-adk/
├── app/                    # ADK应用入口
│   ├── __init__.py
│   └── agent.py           # root_agent定义
├── agents/                # 代理实现
│   └── orchestrator_agent.py  # 主协调代理
├── feyncore/              # 核心功能库
│   ├── physics/           # 物理数据和验证
│   ├── tikz_utils/        # TikZ工具函数
│   └── compilation/       # LaTeX编译器
├── schemas.py             # 数据模型定义
└── requirements.txt       # 依赖管理
```

### 代理系统

- **OrchestratorAgent**: 主协调代理，处理用户输入并生成TikZ代码
- **generate_tikz_diagram**: 核心工具函数，基于物理过程生成相应的TikZ代码

## 📋 开发计划

### ✅ 阶段0: 项目初始化 (已完成)
- [x] 项目结构搭建
- [x] 双许可证配置 (MIT/Apache-2.0)
- [x] 基础ADK集成

### ✅ 阶段1: 核心库抽象 (已完成) 
- [x] feyncore物理数据模块
- [x] TikZ工具函数提取
- [x] LaTeX编译器封装

### ✅ 阶段2: ADK代理基础 (已完成)
- [x] OrchestratorAgent实现
- [x] 基础TikZ生成功能
- [x] ADK工具集成
- [x] 简单物理过程支持

### 🔄 阶段3: 多代理扩展 (进行中)
- [ ] KBRetrieverAgent - 知识库检索代理
- [ ] DiagramGeneratorAgent - 专门的生成代理  
- [ ] PhysicsValidatorAgent - 物理验证代理
- [ ] TikZValidatorAgent - 编译验证代理
- [ ] 代理间通信协调

### 📅 阶段4: 知识库集成 (计划中)
- [ ] 迁移legacy项目知识库
- [ ] 向量检索系统
- [ ] Few-shot学习支持
- [ ] 动态示例检索

### 📅 阶段5: 高级功能 (计划中)
- [ ] 物理规则验证引擎
- [ ] 自动化LaTeX编译验证
- [ ] 错误纠正和重试机制
- [ ] 质量评估系统

### 📅 阶段6: 部署准备 (计划中)
- [ ] Google Cloud部署配置
- [ ] Vertex AI Agent Engine集成
- [ ] Web界面开发
- [ ] 性能优化和监控

## 🛠️ 技术栈

- **核心框架**: Google Agent Development Kit (ADK) 1.2.1
- **语言模型**: Google Gemini 2.0 Flash
- **数据验证**: Pydantic
- **物理数据**: PDG (Particle Data Group)
- **LaTeX处理**: 自定义编译器模块

## 🎨 支持的物理过程

当前支持的费曼图类型：

- ✅ 电子-正电子湮灭 → 双光子
- ✅ 电子轫致辐射 (电子发射光子)
- ✅ 缪子衰变
- ✅ 基础费米子传播
- 🔄 更多过程持续添加中...

## 🧪 测试和验证

### 本地测试
```bash
# 测试代理功能
python agents/orchestrator_agent.py

# 使用测试运行器
python test_runner.py
```

### ADK集成测试
```bash
# 启动ADK开发环境
adk run app
```

## 📚 比赛信息

本项目专为 **Google Cloud × ADK Hackathon** 开发：

- **类别**: Content Creation and Generation
- **目标**: 多代理协作自动生成科学内容 (TikZ费曼图)
- **截止日期**: 2025年6月23日
- **技术亮点**: 
  - ADK多代理架构
  - 物理智能验证
  - 自学习知识库系统

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启Pull Request

## 📄 许可证

本项目采用双许可证：

- MIT License - 详见 [LICENSE-MIT](LICENSE-MIT)
- Apache License 2.0 - 详见 [LICENSE-APACHE](LICENSE-APACHE)

## 🔗 相关链接

- [Google ADK 文档](https://google.github.io/adk-docs/)
- [Google Cloud ADK Hackathon](https://cloud.google.com/)
- [TikZ-Feynman 文档](https://ctan.org/pkg/tikz-feynman)

---

**Built with ❤️ for the physics and AI community** 
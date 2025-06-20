# FeynmanCraft ADK 快速启动指南

**增强版多代理系统 - 集成MCP物理验证工具**

## 🚀 5分钟快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd Particle-Physics-Agent
```

### 2. 环境设置
```bash
# 创建 Conda 环境
conda create --name fey python=3.11 -y
conda activate fey

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env 文件，至少设置：
# GOOGLE_API_KEY=your-api-key-here
```

### 4. 设置知识库

#### 构建本地索引（推荐）
```bash
# 构建向量索引用于语义搜索
python feynmancraft_adk/scripts/build_local_index.py

# 在 .env 中设置（可选）
KB_MODE=local
```

#### 混合模式（默认）
```bash
# 在 .env 中设置
KB_MODE=hybrid
# 系统会自动结合向量搜索和关键词匹配
```

### 5. 运行系统
```bash
# 导航到代理目录
cd feynmancraft_adk

# 启动 ADK Web UI
adk web . --port 8000

# 浏览器会打开 http://localhost:8000
# 如果端口 8000 忙碌，请尝试端口 8001、8002 等
```

### 6. 测试示例

在 ADK Web UI 中输入：
- "生成电子-正电子湮灭的费曼图"
- "画一个 Z 玻色子衰变到轻子对的图"
- "显示康普顿散射过程"
- "muon decay diagram"（测试MCP工具）
- "两个上夸克和一个下夸克"（测试自然语言解析）

## 🔧 故障排除

### 问题：找不到 adk 命令
```bash
# 确保安装了 google-adk
pip install google-adk
```

### 问题：API 认证失败
```bash
# 检查 API key
echo $GOOGLE_API_KEY

# 对于其他 Google AI 服务，运行：
gcloud auth application-default login
```

### 问题：没有搜索结果
```bash
# 检查知识库文件
ls feynmancraft_adk/data/feynman_kb.json

# 重建本地索引
python feynmancraft_adk/scripts/build_local_index.py
```

### 问题：端口冲突
```bash
# 尝试不同端口
adk web . --port 8001
adk web . --port 8002
# 等等
```

## 📊 系统状态检查
```bash
# 导航到项目根目录
cd ..

# 运行快速测试
python quick_test.py

# 运行完整测试
python test_system.py
```

## 🎯 下一步

1. 阅读 [README.md](README.md) 了解完整功能概述
2. 运行 `python feynmancraft_adk/scripts/build_local_index.py` 构建向量索引
3. 探索 `feynmancraft_adk/sub_agents/` 了解各个代理的功能
4. 尝试修改提示词以优化生成结果

## 💡 提示与新功能

### 🔬 MCP物理验证
- **自动触发**: 每次物理验证都会自动使用MCP工具
- **双重验证**: 内部工具 + MCP工具交叉验证
- **详细分析**: 150+粒子的专业物理数据
- **智能诊断**: 粒子查找错误自动建议修正

### 🗃️ 知识库模式
- **本地模式**: Annoy向量索引 + JSON关键词搜索
- **混合模式**: 自动结合语义搜索和精确匹配，最佳检索效果
- **环境控制**: 使用 `KB_MODE` 环境变量切换模式

### 🤖 工作流程
- **完整序列**: 六个代理按序执行，确保全面验证
- **自然语言**: 支持中英文物理过程描述
- **教育模式**: 对无法图示的过程提供教育解释

### 🎨 六代理系统
1. **PlannerAgent**: 自然语言解析和任务规划
2. **KBRetrieverAgent**: 混合知识库搜索
3. **PhysicsValidatorAgent**: MCP增强物理验证
4. **DiagramGeneratorAgent**: TikZ代码生成
5. **TikZValidatorAgent**: LaTeX编译验证
6. **FeedbackAgent**: 最终响应合成

---

遇到问题？查看 [GitHub Issues](https://github.com/your-username/Particle-Physics-Agent/issues) 或创建新 issue。
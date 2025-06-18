# FeynmanCraft ADK 快速启动指南

**增强版多代理系统 - 集成MCP物理验证工具**

## 🚀 5分钟快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd feynmancraft-adk
```

### 2. 设置环境
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

### 4. 选择知识库模式

#### 选项 A: 本地模式（推荐初学者）
```bash
# 在 .env 中设置
KB_MODE=local

# 构建本地索引（可选，用于向量搜索）
python scripts/build_local_index.py
```

#### 选项 B: BigQuery 模式（生产环境）
```bash
# 在 .env 中设置
KB_MODE=bigquery
GOOGLE_CLOUD_PROJECT=your-project-id

# 上传数据到 BigQuery
python scripts/upload_to_bigquery.py
```

#### 选项 C: 混合模式（默认）
```bash
# 在 .env 中设置
KB_MODE=hybrid
# 系统会自动尝试 BigQuery，失败时回退到本地
```

### 5. 运行系统
```bash
# 启动 ADK Dev UI
adk run feynmancraft_adk

# 浏览器会自动打开 http://localhost:40000
```

### 6. 测试示例

在 ADK Dev UI 中输入：
- "生成电子-正电子湮灭的费曼图"
- "画一个 Z 玻色子衰变到轻子对的图"
- "显示康普顿散射过程"
- "muon decay diagram" (测试MCP工具)
- "两个上夸克和一个下夸克" (测试自然语言解析)

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

# 对于 BigQuery，运行：
gcloud auth application-default login
```

### 问题：没有搜索结果
```bash
# 检查知识库文件
ls feynmancraft_adk/data/feynman_kb.json

# 重建本地索引
python scripts/build_local_index.py
```

## 📊 系统状态检查
```bash
# 运行快速测试
python quick_test.py

# 运行完整测试
python test_system.py
```

## 🎯 下一步

1. 阅读 [README.md](README.md) 了解完整功能
2. 查看 [docs/bigquery_setup.md](docs/bigquery_setup.md) 设置生产环境
3. 探索 `feynmancraft_adk/sub_agents/` 了解各个代理的功能
4. 尝试修改提示词优化生成效果

## 💡 提示与新功能

### 🔬 MCP物理验证
- **自动触发**: 每次物理验证都会自动使用MCP工具
- **双重验证**: 内部工具 + MCP工具交叉验证
- **详细分析**: 150+粒子的专业物理数据
- **智能诊断**: 粒子查找错误自动建议修正

### 🗃️ 知识库模式
- **本地模式**: 适合开发和测试，包含向量搜索
- **BigQuery模式**: 适合生产环境和大规模数据
- **混合模式**: 自动故障转移，最佳可用性
- **环境控制**: 使用 `KB_MODE` 环境变量轻松切换

### 🤖 工作流程
- **完整序列**: 六代理按序执行，确保全面验证
- **自然语言**: 支持中英文物理过程描述
- **教育模式**: 对无法图示的过程提供教育解释

---

遇到问题？查看 [GitHub Issues](https://github.com/your-username/feynmancraft-adk/issues) 或创建新 issue。
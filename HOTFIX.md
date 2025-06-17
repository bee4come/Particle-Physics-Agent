# Hotfix for v0.2.0

## 问题
运行 `adk run feynmancraft_adk` 时出现以下错误：
```
ImportError: cannot import name 'language_models' from 'google.cloud.aiplatform.preview'
```

## 原因
两个子代理文件中使用了已废弃的 `google.cloud.aiplatform.preview.language_models` 模块，该模块在较新版本的 Google Cloud AI Platform 中已被移除。

## 修复内容

### 1. 修复 `physics_validator_agent.py`
- 移除 `from google.cloud.aiplatform.preview import language_models`
- 重写 `_get_embedding()` 函数使用 `google.generativeai` API
- 重写 `_embed_and_cache_rules()` 函数

### 2. 修复 `kb_retriever_agent.py`
- 重写 `_get_embedding()` 函数使用 `google.generativeai` API
- 重写 `_embed_and_cache_kb()` 函数

### 3. 修复 `__init__.py`
- 添加异常处理，允许在没有 Google 依赖的情况下导入包

## 修复后的功能
- 使用 Gemini `text-embedding-004` 模型生成 768 维向量
- 统一使用 `google.generativeai` API（与项目其他部分一致）
- 保持向后兼容性和错误处理

## 测试
运行以下命令测试修复：

```bash
# 基础测试
python quick_test.py

# 模拟测试
python mock_test.py

# 详细测试
python test_local_kb_detailed.py

# 运行系统
adk run feynmancraft_adk
```

## 版本更新
这是 v0.2.0 的热修复，应标记为 v0.2.1。

## 相关文件
- `feynmancraft_adk/sub_agents/physics_validator_agent.py`
- `feynmancraft_adk/sub_agents/kb_retriever_agent.py`
- `feynmancraft_adk/__init__.py`
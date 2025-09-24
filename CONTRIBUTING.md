# 贡献指南

感谢您对NeuralFive项目的关注！我们欢迎所有形式的贡献。

## 如何贡献

### 报告Bug

- 使用GitHub Issues报告bug
- 提供详细的复现步骤
- 包含环境信息（Python版本、操作系统等）
- 提供错误日志和相关截图

### 功能建议

- 在提交新功能建议前，请先搜索现有Issues
- 详细描述功能需求和用例场景
- 说明该功能对项目的价值

### 代码贡献

1. **Fork项目**
   ```bash
   git clone https://github.com/your-username/neuralfive.git
   cd neuralfive
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **开发规范**
   - 遵循PEP 8编码规范
   - 添加类型注解
   - 编写单元测试
   - 更新相关文档

4. **代码质量检查**
   ```bash
   # 格式化代码
   black src/ tests/
   isort src/ tests/
   
   # 静态检查
   flake8 src/ tests/
   mypy src/
   bandit -r src/
   
   # 运行测试
   pytest
   ```

5. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   git push origin feature/your-feature-name
   ```

6. **创建Pull Request**
   - 提供清晰的标题和描述
   - 关联相关Issues
   - 确保CI检查通过

## 提交信息规范

使用以下格式：

```
类型: 简短描述

详细说明（可选）

Closes #123
```

### 提交类型

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

## 代码审查

- 所有PR都需要至少一个审查者
- 审查者会关注代码质量、测试覆盖和文档
- 根据反馈进行修改并重新提交

## 开发环境

### 要求

- Python 3.8+
- 虚拟环境（推荐）

### 安装开发依赖

```bash
pip install -r requirements-dev.txt
pre-commit install
```

## 测试

### 运行测试

```bash
# 所有测试
pytest

# 特定测试文件
pytest tests/test_ai_engine.py

# 带覆盖率
pytest --cov=src --cov-report=html
```

### 测试类型

- 单元测试：`tests/unit/`
- 集成测试：`tests/integration/`
- 性能测试：`tests/performance/`

## 文档

- 更新相关文档以反映代码更改
- 使用清晰的语言和示例
- 包含API文档和使用说明

## 行为准则

- 尊重所有贡献者
- 欢迎新成员
- 保持专业和友善的交流
- 专注于建设性的反馈

## 联系方式

如有问题，请通过以下方式联系：

- GitHub Issues
- GitHub Discussions
- 项目维护者邮箱

再次感谢您的贡献！
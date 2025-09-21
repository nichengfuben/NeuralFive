# 贡献指南

感谢您对 StrategicMind 项目的关注！我们欢迎所有形式的贡献。

## 🤝 如何贡献

### 报告问题

如果您发现了 bug 或有功能建议，请：

1. 检查 [Issues](https://github.com/yourusername/strategicmind/issues) 是否已有相关问题
2. 创建新的 Issue，详细描述问题或建议
3. 使用合适的标签（bug、enhancement、question 等）

### 提交代码

1. **Fork 项目**
   ```bash
   git clone https://github.com/yourusername/strategicmind.git
   cd strategicmind
   ```

2. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **安装开发依赖**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **运行测试**
   ```bash
   pytest tests/
   ```

5. **代码格式化**
   ```bash
   black src/
   isort src/
   ```

6. **提交代码**
   ```bash
   git add .
   git commit -m "feat: add your feature"
   git push origin feature/your-feature-name
   ```

7. **创建 Pull Request**

## 📝 代码规范

### Python 代码风格

- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 遵循 PEP 8 规范
- 使用类型注解

### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

### 测试要求

- 新功能必须包含测试
- 测试覆盖率不低于 80%
- 使用 pytest 作为测试框架

## 🏗️ 开发环境设置

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/strategicmind.git
cd strategicmind
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements-dev.txt
```

### 4. 安装预提交钩子

```bash
pre-commit install
```

### 5. 运行测试

```bash
pytest tests/ -v
```

## 📋 开发检查清单

在提交 PR 之前，请确保：

- [ ] 代码通过了所有测试
- [ ] 代码符合 Black 和 isort 规范
- [ ] 添加了必要的文档字符串
- [ ] 更新了相关的文档
- [ ] 提交信息符合规范

## 🐛 调试指南

### 常见问题

1. **导入错误**
   - 确保在项目根目录运行
   - 检查 Python 路径设置

2. **测试失败**
   - 检查依赖是否正确安装
   - 确保测试数据完整

3. **性能问题**
   - 使用性能监控工具
   - 检查 Numba 编译是否正常

### 调试工具

```bash
# 运行特定测试
pytest tests/test_ai_engine.py::TestStrategicAI::test_make_move -v

# 生成覆盖率报告
pytest --cov=src/strategicmind tests/

# 性能分析
python -m cProfile -s cumulative src/strategicmind/main.py
```

## 📚 文档贡献

### 文档结构

- `docs/` - 项目文档
- `examples/` - 使用示例
- `README.md` - 项目介绍
- 代码中的 docstring

### 文档规范

- 使用 Markdown 格式
- 包含代码示例
- 保持简洁明了
- 定期更新

## 🎯 贡献领域

我们特别欢迎以下领域的贡献：

- **AI算法优化** - 提升搜索效率和准确性
- **用户界面** - 改进用户体验
- **性能优化** - 提升运行效率
- **测试覆盖** - 增加测试用例
- **文档完善** - 改进文档质量
- **国际化** - 支持更多语言

## 💬 社区交流

- **GitHub Issues** - 问题讨论
- **GitHub Discussions** - 功能讨论
- **Pull Requests** - 代码审查

## 📄 许可证

通过贡献代码，您同意您的贡献将在 MIT 许可证下发布。

## 🙏 致谢

感谢所有贡献者的努力，让 StrategicMind 变得更好！

---

如果您有任何问题，请随时在 Issues 中提问。我们期待您的贡献！

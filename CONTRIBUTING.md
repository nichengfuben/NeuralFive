# 贡献指南

感谢您对SmartFive项目的兴趣！我们欢迎各种形式的贡献，包括但不限于代码、文档、测试和建议。

## 如何贡献

### 报告Bug

如果您发现了Bug，请在GitHub上创建一个Issue，包含以下信息：
- 清晰的标题和描述
- 复现步骤
- 预期行为和实际行为
- 环境信息（操作系统、Python版本等）
- 屏幕截图（如果适用）

### 提交功能请求

如果您有新的功能想法，请创建一个Issue，描述：
- 功能的详细说明
- 解决的问题
- 可能的实现方式

### 提交代码

1. Fork项目到您的GitHub账户
2. 创建一个新的分支 (`git checkout -b feature/your-feature-name`)
3. 进行您的更改
4. 提交您的更改 (`git commit -am 'Add some feature'`)
5. 推送到分支 (`git push origin feature/your-feature-name`)
6. 创建一个Pull Request

## 代码规范

- 遵循PEP 8代码风格
- 添加适当的注释和文档字符串
- 编写测试用例（如果适用）
- 确保所有测试通过

## 开发环境设置

1. Fork并克隆仓库
2. 创建虚拟环境: `python -m venv venv`
3. 激活虚拟环境: `source venv/bin/activate` (Linux/macOS) 或 `venv\Scripts\activate` (Windows)
4. 安装依赖: `pip install -r requirements.txt`

## 测试

运行测试确保您的更改不会破坏现有功能：
```bash
python -m pytest
```

## 代码审查

所有Pull Request都需要通过代码审查。请耐心等待维护者的反馈。

## 行为准则

请遵守我们的行为准则，创建一个友好、包容的社区环境。

## 联系方式

如有任何问题，请通过GitHub Issue或邮箱联系我们。
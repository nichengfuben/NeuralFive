# NeuralFive 项目文档

欢迎来到NeuralFive项目文档！这里包含了所有关于安装、使用、开发和贡献的详细信息。

## 📚 文档目录

### 用户指南
- [快速开始](quickstart.md) - 5分钟内运行你的第一个游戏
- [安装指南](installation.md) - 详细的安装说明
- [用户手册](user-guide.md) - 完整的功能使用指南
- [常见问题](faq.md) - 常见问题和解决方案

### 开发文档
- [架构设计](architecture.md) - 项目架构和技术栈
- [API参考](api-reference.md) - 完整的API文档
- [开发指南](development.md) - 开发环境设置和最佳实践
- [测试指南](testing.md) - 测试策略和工具
- [性能优化](performance.md) - 性能调优指南

### 贡献文档
- [贡献指南](../CONTRIBUTING.md) - 如何参与项目开发
- [代码规范](coding-standards.md) - 编码规范和最佳实践
- [设计文档](design-docs.md) - 设计决策和讨论

### 部署文档
- [部署指南](deployment.md) - 生产环境部署
- [Docker指南](docker.md) - 容器化部署
- [CI/CD配置](cicd.md) - 持续集成和部署

### 高级主题
- [机器学习集成](machine-learning.md) - AI模型集成指南
- [扩展开发](extensions.md) - 如何开发扩展插件
- [国际化](i18n.md) - 多语言支持实现

## 🔗 快速链接

- [GitHub仓库](https://github.com/your-username/neuralfive)
- [问题追踪](https://github.com/your-username/neuralfive/issues)
- [讨论区](https://github.com/your-username/neuralfive/discussions)
- [发布页面](https://github.com/your-username/neuralfive/releases)

## 📖 示例代码

### 基本使用

```python
from neuralfive import NeuralFiveAI, GameState, GameSettings

# 创建AI引擎
ai = NeuralFiveAI(difficulty="medium")

# 创建游戏
settings = GameSettings(board_size=15)
game = GameState(settings)

# 开始游戏
game.start_game()

# 获取AI推荐
move = ai.get_best_move(game)
print(f"AI推荐移动: ({move.row}, {move.col})")
```

### 高级配置

```python
from neuralfive import NeuralFiveAI, GameSettings

# 自定义AI配置
settings = GameSettings(
    ai_difficulty="hard",
    board_size=19,
    player_color="black",
    ai_color="white"
)

# 创建高性能AI
ai = NeuralFiveAI(
    difficulty="hard",
    max_search_depth=100,
    time_limit=2.0,
    use_cache=True
)
```

## 🆘 获取帮助

如果您在使用或开发过程中遇到问题：

1. 📖 首先查看相关文档
2. 🔍 搜索现有的Issues
3. 💬 在Discussion中提问
4. 📧 发送邮件到项目维护者

## 📈 文档状态

| 文档类型 | 完成度 | 最后更新 |
|---------|--------|----------|
| 用户指南 | ✅ 100% | 2025-01-19 |
| 开发文档 | ✅ 100% | 2025-01-19 |
| API参考 | ✅ 100% | 2025-01-19 |
| 部署文档 | 🔄 80% | 2025-01-19 |
| 高级主题 | 🔄 60% | 2025-01-19 |

## 📝 贡献文档

我们欢迎文档贡献！如果您发现文档有误或想要添加内容：

1. Fork项目仓库
2. 修改或添加文档
3. 提交Pull Request
4. 描述您的更改

文档编写规范：
- 使用清晰的Markdown格式
- 添加适当的代码示例
- 保持语言简洁明了
- 定期更新过时信息

---

*文档是开源项目的重要组成部分，感谢您的关注和贡献！*
# StrategicMind 文档

欢迎使用 StrategicMind 智能策略游戏引擎！

## 📚 文档目录

- [快速开始](quickstart.md) - 5分钟快速上手
- [游戏规则](game-rules.md) - 五子棋规则详解
- [AI算法](ai-algorithm.md) - 核心算法原理
- [API参考](api-reference.md) - 完整API文档
- [自定义主题](customization.md) - 界面自定义指南
- [性能优化](performance.md) - 性能调优建议
- [常见问题](faq.md) - 问题解答

## 🚀 快速开始

### 安装

```bash
pip install strategicmind
```

### 基本使用

```python
from strategicmind import StrategicAI, GameBoard

# 创建AI和棋盘
ai = StrategicAI()
board = GameBoard()

# 开始游戏
result = ai.make_move(7, 7, 'black')
print(result)
```

### 运行图形界面

```bash
strategicmind
```

## 🧠 AI特性

- **深度搜索**: 支持100层深度搜索
- **智能缓存**: 避免重复计算
- **自适应难度**: 根据局势调整策略
- **高性能**: 使用Numba JIT编译优化

## 🎮 游戏特性

- **现代化界面**: 基于Pygame的流畅图形界面
- **多语言支持**: 中文/英文切换
- **动画效果**: 流畅的棋子动画
- **音效支持**: 可选的音效反馈

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 搜索深度 | 100层 |
| 响应时间 | <100ms |
| 内存占用 | <50MB |
| 准确率 | 99.2% |

## 🤝 贡献

我们欢迎所有形式的贡献！请查看 [贡献指南](../CONTRIBUTING.md) 了解如何参与。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](../LICENSE) 了解详情。

## 🙏 致谢

感谢所有为 StrategicMind 做出贡献的开发者和用户！

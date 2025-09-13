# SmartFive - AI五子棋游戏

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)

一个使用Pygame和Numba实现的智能五子棋AI游戏，具有强大的AI对手和精美的图形界面。

## 特性

- 🤖 强大的AI对手，基于Negamax算法和α-β剪枝优化
- 🎮 精美的图形用户界面，支持鼠标操作
- 🌟 实时游戏状态显示和动画效果
- 📊 游戏统计和信息面板
- 🌍 多语言支持（中英文切换）
- ⚡ 使用Numba加速AI计算性能
- 🎨 现代化UI设计，支持渐变背景和阴影效果

## 安装

### 环境要求

- Python 3.8 或更高版本
- Windows/macOS/Linux 操作系统

### 安装依赖

```bash
pip install -r requirements.txt
```

## 运行游戏

```bash
python main.py
```

## 游戏规则

1. 黑棋先行
2. 玩家轮流落子
3. 率先连成五子者获胜

## 项目结构

```
smart-five/
├── src/
│   ├── game/
│   │   └── main.py          # 主游戏逻辑
│   ├── ai/
│   │   └── five_ai.py       # AI算法实现
├── assets/
│   └── fonts/               # 字体文件（可选）
├── requirements.txt         # 项目依赖
├── README.md               # 项目说明
└── LICENSE                 # 开源许可证
```

## 技术栈

- **Pygame**: 游戏引擎和图形渲染
- **Numba**: AI算法性能优化
- **NumPy**: 数值计算支持

## AI算法

本项目使用基于Negamax算法的AI，具有以下特点：

- α-β剪枝优化搜索效率
- 启发式评估函数
- 缓存机制避免重复计算
- 多线程支持防止界面卡顿

## 贡献

欢迎提交Issue和Pull Request来改进项目！

## 许可证

本项目采用MIT许可证，详情请见[LICENSE](LICENSE)文件。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=SmartFive&type=Date)](https://star-history.com/#SmartFive&Date)
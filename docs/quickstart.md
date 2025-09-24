# 快速开始指南

本指南将帮助您在5分钟内运行NeuralFive五子棋AI！

## 🚀 安装

### 系统要求

- Python 3.8+
- pip包管理器
- 2GB可用内存
- 100MB磁盘空间

### 快速安装

```bash
# 1. 克隆项目
git clone https://github.com/your-username/neuralfive.git
cd neuralfive

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 安装包
pip install -e .
```

## 🎮 开始游戏

### 图形界面模式

```bash
# 启动游戏
python -m neuralfive

# 或使用快捷方式
neuralfive
```

### 命令行模式

```bash
# 命令行对战
python -m neuralfive --mode cli

# 指定难度
python -m neuralfive --mode cli --difficulty hard
```

### Python脚本模式

```python
from neuralfive import NeuralFiveAI, GameState, GameSettings

# 创建AI和游戏
ai = NeuralFiveAI(difficulty="medium")
settings = GameSettings()
game = GameState(settings)

# 开始游戏
game.start_game()

# 进行几步游戏
print("开始游戏！")
print(f"当前玩家: {game.current_player}")

# 玩家移动
game.make_move(7, 7, "black")
print(f"玩家落子: (7, 7)")

# AI移动
ai_move = ai.get_best_move(game)
game.make_move(ai_move.row, ai_move.col, "white")
print(f"AI落子: ({ai_move.row}, {ai_move.col})")

# 检查获胜者
if game.winner:
    print(f"获胜者: {game.winner}")
```

## 🎯 基本操作

### 图形界面

1. **启动游戏**: 运行 `python -m neuralfive`
2. **选择难度**: 点击界面上的难度按钮
3. **开始游戏**: 点击"开始游戏"按钮
4. **落子**: 点击棋盘上的交叉点
5. **撤销**: 按Ctrl+Z或点击撤销按钮
6. **重置**: 按Ctrl+R或点击重置按钮

### 命令行操作

```bash
# 开始新游戏
python -m neuralfive --mode cli

# 输入坐标格式: 行 列
# 例如: 7 7 (表示第7行第7列)

# 特殊命令:
# undo - 撤销上一步
# reset - 重新开始
# quit - 退出游戏
# help - 显示帮助
```

## ⚙️ 配置选项

### 难度设置

- **简单**: 搜索深度10，适合初学者
- **中等**: 搜索深度50，适合一般玩家
- **困难**: 搜索深度100，适合高手挑战

### 棋盘大小

- 标准: 15x15 (默认)
- 大型: 19x19
- 小型: 13x13

### 语言设置

```python
# 在代码中设置语言
from neuralfive.gui import NeuralFiveGUI

gui = NeuralFiveGUI()
gui.set_language("zh")  # 中文
gui.set_language("en")  # 英文
```

## 🎨 自定义主题

```python
# 自定义颜色主题
from neuralfive.gui import NeuralFiveGUI

gui = NeuralFiveGUI()
gui.set_theme({
    "board_color": (240, 230, 140),  # 棋盘颜色
    "line_color": (0, 0, 0),         # 网格线颜色
    "black_stone": (0, 0, 0),        # 黑子颜色
    "white_stone": (255, 255, 255),  # 白子颜色
})
```

## 🔍 故障排除

### 常见问题

#### 1. 游戏无法启动

```bash
# 检查Python版本
python --version
# 需要Python 3.8+

# 检查依赖
pip check

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

#### 2. 图形界面显示异常

```bash
# 检查Pygame安装
python -c "import pygame; print(pygame.version.ver)"

# 更新显卡驱动
# Windows: 设备管理器 -> 显示适配器
# macOS: 系统偏好设置 -> 软件更新
```

#### 3. AI响应慢

```bash
# 降低难度
python -m neuralfive --difficulty easy

# 检查系统资源
top  # Linux/macOS
taskmgr  # Windows
```

#### 4. 中文显示问题

```bash
# 安装中文字体
# Windows: 系统通常已包含
# Linux: sudo apt-get install fonts-wqy-zenhei
# macOS: 系统通常已包含
```

## 📈 下一步

完成快速开始后，您可以：

1. 📖 阅读[完整用户手册](user-guide.md)
2. 🔧 查看[API参考](api-reference.md)
3. 🧪 探索[高级功能](advanced-features.md)
4. 🏗️ 了解[开发指南](development.md)
5. 🤝 参与[社区贡献](../CONTRIBUTING.md)

## 💡 提示和技巧

### 提高胜率

1. **控制中心**: 优先占据棋盘中心区域
2. **防守优先**: 及时阻止对手的三连和四连
3. **创造双三**: 同时创造两个三连，让对手无法同时防守
4. **利用AI**: 观察AI的移动模式，学习高级策略

### 性能优化

1. **关闭动画**: 在设置中关闭动画效果
2. **降低分辨率**: 使用较小的窗口大小
3. **减少搜索深度**: 选择较低的难度级别

### 学习资源

- [五子棋规则](https://en.wikipedia.org/wiki/Gomoku)
- [基本策略](https://www.wikihow.com/Play-Gomoku)
- [高级技巧](https://gomokuworld.com/gomoku-strategy/)

## 🆘 获取帮助

- 📖 查看完整文档
- 🔍 搜索GitHub Issues
- 💬 加入社区讨论
- 📧 发送邮件求助

---

**恭喜！** 🎉 您已经成功运行了NeuralFive！现在可以开始享受智能五子棋的乐趣了。
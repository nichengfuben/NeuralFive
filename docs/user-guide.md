# NeuralFive 用户指南

## 目录
1. [快速开始](#快速开始)
2. [游戏界面](#游戏界面)
3. [AI设置](#ai设置)
4. [高级功能](#高级功能)
5. [故障排除](#故障排除)
6. [提示与技巧](#提示与技巧)

## 快速开始

### 安装
```bash
pip install neuralfive
```

### 启动游戏
```bash
# 图形界面模式
neuralfive --gui

# 命令行模式
neuralfive --cli
```

### 基本操作
- **鼠标点击**: 在棋盘上落子
- **键盘快捷键**:
  - `Ctrl+Z`: 撤销上一步
  - `Ctrl+R`: 重新开始
  - `Ctrl+Q`: 退出游戏
  - `F1`: 显示帮助

## 游戏界面

### 主界面
- **棋盘**: 15×15标准五子棋棋盘
- **状态栏**: 显示当前玩家、游戏状态、AI思考时间
- **控制面板**: 游戏设置、AI难度、语言切换

### 菜单功能
- **文件**: 新建游戏、保存对局、加载对局
- **设置**: AI难度、界面主题、声音设置
- **帮助**: 游戏规则、操作指南、关于

## AI设置

### 难度等级
- **初级**: 搜索深度3层，适合新手
- **中级**: 搜索深度5层，平衡性能
- **高级**: 搜索深度7层，挑战性强
- **专家**: 搜索深度10层，最高难度

### 思考时间
- **快速**: 每步1-3秒
- **标准**: 每步3-10秒
- **深度思考**: 每步10-30秒
- **无限思考**: 直到找到最佳落子

### 评估策略
- **基础评估**: 基于棋子连接数
- **高级评估**: 包含位置价值和形状识别
- **机器学习**: 使用训练好的模型评估

## 高级功能

### 对局分析
```bash
neuralfive --analyze game_record.json
```

### AI训练
```bash
neuralfive --train --dataset games.pgn --epochs 100
```

### 批量测试
```bash
neuralfive --benchmark --games 100 --ai1 expert --ai2 advanced
```

### 自定义配置
创建 `config.json` 文件：
```json
{
  "ai": {
    "depth": 7,
    "evaluation": "advanced",
    "use_opening_book": true,
    "use_endgame_table": true
  },
  "ui": {
    "theme": "dark",
    "animation": true,
    "sound": true,
    "language": "zh_CN"
  },
  "game": {
    "board_size": 15,
    "time_control": "standard",
    "allow_undo": true,
    "auto_save": true
  }
}
```

## 故障排除

### 常见问题

**Q: 游戏启动失败**
A: 检查Python版本是否为3.8+，确保所有依赖已安装

**Q: AI响应慢**
A: 降低AI难度或缩短思考时间，检查系统资源使用情况

**Q: 界面显示异常**
A: 更新显卡驱动，尝试切换软件渲染模式

**Q: 无法保存对局**
A: 检查文件权限，确保游戏目录有写入权限

### 性能优化
- 关闭不必要的动画效果
- 降低AI搜索深度
- 使用更快的评估函数
- 启用多线程处理

## 提示与技巧

### 对战策略
1. **开局**: 控制中心位置，建立优势
2. **中盘**: 攻守平衡，寻找双杀机会
3. **残局**: 精确计算，避免失误

### AI分析
- 查看AI的胜率评估
- 分析关键转折点
- 学习AI的攻防思路

### 训练建议
- 收集高质量对局数据
- 定期更新训练模型
- 调整网络结构和超参数

### 快捷键大全
- `Space`: 暂停/继续AI思考
- `Tab`: 显示AI建议
- `Enter`: 确认落子
- `Esc`: 取消当前操作

## 获取更多帮助
- GitHub Issues: https://github.com/your-username/neuralfive/issues
- 文档: https://neuralfive.readthedocs.io
- 社区: https://github.com/your-username/neuralfive/discussions
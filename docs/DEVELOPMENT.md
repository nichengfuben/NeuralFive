# 开发指南

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
├── docs/                    # 文档
│   ├── AI_ALGORITHM.md     # AI算法详解
│   └── DEVELOPMENT.md      # 开发指南
├── requirements.txt         # 项目依赖
├── README.md               # 项目说明
├── CONTRIBUTING.md         # 贡献指南
└── LICENSE                 # 开源许可证
```

## 环境搭建

### Python版本要求

项目需要Python 3.8或更高版本。

### 安装依赖

```bash
pip install -r requirements.txt
```

### 开发依赖

对于开发和测试，您可能还需要安装额外的依赖：

```bash
pip install pytest pytest-cov black isort flake8 mypy
```

## 代码规范

### 代码风格

项目遵循PEP 8代码风格规范。可以使用以下工具进行代码格式化：

```bash
# 格式化代码
black src/

# 排序导入
isort src/
```

### 类型检查

使用mypy进行类型检查：

```bash
mypy src/
```

### 代码检查

使用flake8进行代码检查：

```bash
flake8 src/
```

## 测试

### 运行测试

```bash
pytest
```

### 运行测试并生成覆盖率报告

```bash
pytest --cov=src --cov-report=html
```

## 架构说明

### 游戏模块 (src/game)

主游戏逻辑位于`src/game/main.py`文件中，包含：

1. Pygame初始化和事件处理
2. 游戏状态管理
3. 图形界面渲染
4. 用户交互处理

### AI模块 (src/ai)

AI算法实现位于`src/ai/five_ai.py`文件中，包含：

1. 棋盘状态管理
2. Negamax算法实现
3. 评估函数
4. 移动排序和优化

## 贡献流程

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 发布流程

1. 更新版本号
2. 更新CHANGELOG.md
3. 创建Git标签
4. 推送到GitHub
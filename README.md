# NeuralFive

一个高性能的神经网络五子棋AI引擎，支持GUI界面和命令行操作。

## 特性

- 🧠 基于神经网络的AI引擎
- 🎮 图形用户界面（Pygame）
- 💻 命令行界面
- 📊 性能基准测试
- 🐳 Docker支持
- 📈 机器学习优化
- 🧪 完整的测试覆盖

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/nichengfuben/NeuralFive
cd neuralfive

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 安装预提交钩子
pre-commit install
```

### 运行

```bash
# GUI模式
python -m neuralfive --gui

# 命令行模式
python -m neuralfive --cli

# 基准测试
python -m neuralfive-benchmark
```

### Docker

```bash
# 构建镜像
docker build -t neuralfive .

# 运行容器
docker run -p 8000:8000 neuralfive

# 开发环境
docker-compose up neuralfive-dev
```

## 开发

### 项目结构

```
neuralfive/
├── src/                    # 源代码
│   ├── main.py            # 主入口
│   ├── cli.py             # 命令行接口
│   ├── benchmark.py       # 基准测试
│   └── neuralfive/        # 核心包
├── tests/                 # 测试文件
├── docs/                  # 文档
├── requirements.txt       # 生产依赖
├── requirements-dev.txt   # 开发依赖
├── pyproject.toml         # 项目配置
└── Dockerfile             # Docker配置
```

### 代码质量

```bash
# 代码格式化
black src/ tests/
isort src/ tests/

# 代码检查
flake8 src/ tests/
mypy src/
bandit -r src/

# 运行测试
pytest
pytest --cov=src --cov-report=html
```

### 文档

```bash
# 构建文档
cd docs
make html

# 查看文档
open _build/html/index.html
```

## 贡献

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 作者

- 你的名字 - [@yourtwitter](https://twitter.com/yourtwitter)

## 致谢

- 五子棋AI算法研究社区
- Pygame开发团队
- 开源机器学习框架贡献者

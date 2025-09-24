# NeuralFive 项目开发指南

## 项目结构

```
neuralfive/
├── src/
│   └── neuralfive/
│       ├── __init__.py          # 包初始化
│       ├── ai_engine.py         # AI引擎核心
│       ├── game_state.py        # 游戏状态管理
│       ├── gui.py               # 图形界面
│       └── __main__.py          # 命令行入口
├── tests/                       # 测试文件
├── docs/                        # 文档
├── assets/                      # 资源文件
├── examples/                    # 示例代码
└── .github/workflows/           # CI/CD配置
```

## 开发环境设置

### 1. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate     # Windows
```

### 2. 安装依赖
```bash
pip install -r requirements-dev.txt
```

### 3. 安装预提交钩子
```bash
pre-commit install
```

### 4. 安装项目
```bash
pip install -e .
```

## 开发流程

### 代码质量检查
```bash
# 格式化代码
black src tests
isort src tests

# 静态类型检查
mypy src

# 代码检查
flake8 src tests
pylint src

# 安全检查
bandit -r src/

# 运行预提交钩子
pre-commit run --all-files
```

### 测试
```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_ai_engine.py

# 运行测试并生成覆盖率报告
pytest --cov=neuralfive --cov-report=html

# 运行性能测试
pytest -m performance

# 运行基准测试
pytest --benchmark-only
```

### 文档
```bash
# 生成文档
cd docs
make html

# 查看文档
open _build/html/index.html
```

## 发布流程

### 1. 更新版本号
在 `pyproject.toml` 和 `src/neuralfive/__init__.py` 中更新版本号。

### 2. 更新CHANGELOG
在 `CHANGELOG.md` 中添加新版本信息。

### 3. 创建发布分支
```bash
git checkout -b release/v1.0.0
```

### 4. 运行完整测试
```bash
pytest
pre-commit run --all-files
```

### 5. 合并到main分支
```bash
git checkout main
git merge release/v1.0.0
git tag v1.0.0
git push origin main --tags
```

### 6. 构建和发布
```bash
python -m build
twine upload dist/*
```

## 性能优化

### 基准测试
```bash
pytest tests/ -m performance --benchmark-json benchmark.json
```

### 性能分析
```bash
# 内存分析
python -m memory_profiler src/neuralfive/ai_engine.py

# 行级分析
kernprof -l -v src/neuralfive/ai_engine.py
```

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 调试技巧

### 日志配置
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 性能调试
```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# 你的代码

profiler.disable()
stats = pstats.Stats(profiler).sort_stats('cumulative')
stats.print_stats(20)
```

## 常见问题

### Q: 如何解决依赖冲突？
A: 使用虚拟环境，并定期更新依赖版本。

### Q: 测试覆盖率不够怎么办？
A: 使用 `pytest --cov=neuralfive --cov-report=html` 查看覆盖率报告，针对未覆盖的代码编写测试。

### Q: 性能优化建议？
A: 使用 `@numba.jit` 装饰器优化计算密集型函数，使用 `@lru_cache` 缓存重复计算。

## 联系方式

- GitHub Issues: https://github.com/your-username/neuralfive/issues
- Discussions: https://github.com/your-username/neuralfive/discussions
- Email: contact@neuralfive.com
# SmartFive - AI五子棋游戏 Makefile

# 变量定义
PYTHON := python
PIP := pip
PROJECT_NAME := smartfive

# 帮助信息
.PHONY: help
help:
	@echo "SmartFive - AI五子棋游戏"
	@echo ""
	@echo "Usage:"
	@echo "  make install          安装项目依赖"
	@echo "  make run              运行游戏"
	@echo "  make test             运行测试"
	@echo "  make clean            清理临时文件"
	@echo "  make dist             构建分发包"
	@echo "  make install-dev      安装开发依赖"
	@echo "  make lint             代码检查"
	@echo "  make format           代码格式化"

# 安装项目依赖
.PHONY: install
install:
	$(PIP) install -r requirements.txt

# 安装开发依赖
.PHONY: install-dev
install-dev:
	$(PIP) install -r requirements.txt
	$(PIP) install pytest black isort flake8 mypy

# 运行游戏
.PHONY: run
run:
	$(PYTHON) -m src.game.main

# 运行测试
.PHONY: test
test:
	$(PYTHON) run_tests.py

# 代码检查
.PHONY: lint
lint:
	$(PYTHON) -m flake8 src tests
	$(PYTHON) -m pylint src tests

# 代码格式化
.PHONY: format
format:
	$(PYTHON) -m black src tests
	$(PYTHON) -m isort src tests

# 清理临时文件
.PHONY: clean
clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# 构建分发包
.PHONY: dist
dist:
	$(PYTHON) setup.py sdist bdist_wheel

# 安装本地开发版本
.PHONY: develop
develop:
	$(PIP) install -e .
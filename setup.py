#!/usr/bin/env python3
"""
StrategicMind - 智能策略游戏引擎
安装配置文件
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 读取requirements文件
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="strategicmind",
    version="1.0.0",
    author="StrategicMind Team",
    author_email="contact@strategicmind.dev",
    description="一个基于深度搜索算法的智能策略游戏引擎",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/strategicmind",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/strategicmind/issues",
        "Source": "https://github.com/yourusername/strategicmind",
        "Documentation": "https://strategicmind.readthedocs.io/",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
            "myst-parser>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "strategicmind=strategicmind.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "strategicmind": [
            "assets/*",
            "assets/images/*",
            "assets/sounds/*",
            "assets/fonts/*",
        ],
    },
    keywords=[
        "ai", "artificial-intelligence", "game", "strategy", "gomoku", 
        "five-in-a-row", "minimax", "negamax", "alpha-beta", "pygame"
    ],
    zip_safe=False,
)

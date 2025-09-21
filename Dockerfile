# 使用官方Python运行时作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY src/ ./src/
COPY setup.py .
COPY README.md .

# 安装项目
RUN pip install -e .

# 创建非root用户
RUN useradd --create-home --shell /bin/bash strategicmind
USER strategicmind

# 暴露端口
EXPOSE 8080

# 设置启动命令
CMD ["python", "-m", "src.strategicmind.main"]

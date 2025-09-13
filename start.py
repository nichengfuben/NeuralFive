#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartFive - AI五子棋游戏启动脚本
"""

import sys
import os

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

try:
    # 导入并运行游戏主模块
    from game import main
    main.main()
except ImportError as e:
    print(f"无法导入游戏模块: {e}")
    print("请确保所有依赖已正确安装")
    sys.exit(1)
except Exception as e:
    print(f"游戏运行出错: {e}")
    sys.exit(1)
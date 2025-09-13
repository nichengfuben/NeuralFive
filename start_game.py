#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartFive - AI五子棋游戏启动脚本
"""

import sys
import os

def main():
    """启动游戏"""
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 添加src目录到Python路径
    src_path = os.path.join(current_dir, 'src')
    sys.path.insert(0, src_path)
    
    try:
        # 导入并运行游戏
        from game.main import GomokuGame
        import pygame
        
        # 初始化游戏
        game = GomokuGame()
        
        # 运行游戏主循环
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # 这里可以添加更多的事件处理
                
            # 这里可以添加游戏逻辑更新
            
            # 这里可以添加屏幕更新
            
        pygame.quit()
        
    except ImportError as e:
        print(f"无法导入游戏模块: {e}")
        print("请确保所有依赖已正确安装")
        sys.exit(1)
    except Exception as e:
        print(f"游戏运行出错: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
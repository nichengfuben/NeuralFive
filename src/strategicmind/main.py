"""
StrategicMind 主程序入口

智能策略游戏引擎的主程序
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.strategicmind.ui.game_window import GameWindow
from src.strategicmind.utils.config import Config
from src.strategicmind.utils.logger import Logger


def main():
    """主函数"""
    try:
        # 初始化配置
        config = Config()
        config.validate()
        
        # 初始化日志
        logger = Logger()
        logger.info("StrategicMind 启动中...")
        
        # 创建并运行游戏窗口
        game = GameWindow(
            width=config.get('window_width', 900),
            height=config.get('window_height', 700)
        )
        
        # 应用配置
        game.set_language(config.get('language', 'zh'))
        game.game_state.set_ai_difficulty(config.get('ai_difficulty', 'hard'))
        game.game_state.enable_animations = config.get('enable_animations', True)
        game.game_state.sound_enabled = config.get('sound_enabled', True)
        
        logger.info("游戏窗口创建成功，开始运行...")
        game.run()
        
    except KeyboardInterrupt:
        print("\n游戏被用户中断")
    except Exception as e:
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("感谢使用 StrategicMind！")


if __name__ == "__main__":
    main()

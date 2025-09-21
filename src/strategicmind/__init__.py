"""
StrategicMind - 智能策略游戏引擎

一个基于深度搜索算法的智能策略游戏引擎，专为五子棋等策略游戏设计。
提供高性能的AI引擎、现代化的用户界面和丰富的配置选项。

主要特性:
- 基于Negamax算法和Alpha-Beta剪枝的智能AI
- 使用Numba JIT编译优化性能
- 现代化的Pygame图形界面
- 支持中英文切换
- 高度可配置的搜索参数

作者: StrategicMind Team
版本: 1.0.0
许可证: MIT
"""

__version__ = "1.0.0"
__author__ = "StrategicMind Team"
__email__ = "contact@strategicmind.dev"
__license__ = "MIT"

# 导入主要模块
from .ai.engine import StrategicAI
from .game.board import GameBoard
from .game.rules import GameRules
from .ui.game_window import GameWindow

__all__ = [
    "StrategicAI",
    "GameBoard", 
    "GameRules",
    "GameWindow",
]

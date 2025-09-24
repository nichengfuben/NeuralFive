"""
NeuralFive - 智能五子棋AI系统

一个基于深度学习和优化算法的高性能五子棋AI引擎。
"""

__version__ = "1.0.0"
__author__ = "AI Research Team"
__email__ = "contact@neuralfive.com"

from .ai_engine import NeuralFiveAI
from .game_state import GameState, Move
from .evaluation import PositionEvaluator

__all__ = [
    "NeuralFiveAI",
    "GameState", 
    "Move",
    "PositionEvaluator"
]
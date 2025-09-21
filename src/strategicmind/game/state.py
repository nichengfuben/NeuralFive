"""
游戏状态管理

管理游戏的整体状态，包括当前玩家、游戏阶段、历史记录等
"""

from typing import List, Tuple, Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass
import time


class GameStatus(Enum):
    """游戏状态"""
    MENU = "menu"           # 主菜单
    PLAYING = "playing"     # 游戏中
    PAUSED = "paused"       # 暂停
    GAME_OVER = "game_over" # 游戏结束
    SETTINGS = "settings"   # 设置


class PlayerType(Enum):
    """玩家类型"""
    HUMAN = "human"         # 人类玩家
    AI = "ai"              # AI玩家


@dataclass
class Move:
    """移动记录"""
    row: int
    col: int
    color: str
    timestamp: float
    player_type: PlayerType
    thinking_time: Optional[float] = None


@dataclass
class GameResult:
    """游戏结果"""
    winner: Optional[str]
    reason: str
    move_count: int
    duration: float
    ai_thinking_time: float


class GameState:
    """游戏状态管理类"""
    
    def __init__(self, board_size: int = 15):
        """
        初始化游戏状态
        
        Args:
            board_size: 棋盘大小
        """
        self.board_size = board_size
        self.status = GameStatus.MENU
        self.current_player = "black"
        self.player_colors = {"black": None, "white": None}
        self.player_types = {"black": PlayerType.HUMAN, "white": PlayerType.AI}
        
        # 游戏历史
        self.move_history: List[Move] = []
        self.game_start_time = None
        self.game_end_time = None
        
        # 统计信息
        self.ai_thinking_time = 0.0
        self.total_moves = 0
        
        # 设置
        self.ai_difficulty = "hard"
        self.search_depth = 100
        self.enable_animations = True
        self.sound_enabled = True
    
    def start_game(self, black_player: str, white_player: str):
        """
        开始新游戏
        
        Args:
            black_player: 黑棋玩家类型 ('human' 或 'ai')
            white_player: 白棋玩家类型 ('human' 或 'ai')
        """
        self.status = GameStatus.PLAYING
        self.current_player = "black"
        self.player_types["black"] = PlayerType(black_player)
        self.player_types["white"] = PlayerType(white_player)
        self.move_history.clear()
        self.game_start_time = time.time()
        self.game_end_time = None
        self.ai_thinking_time = 0.0
        self.total_moves = 0
    
    def end_game(self, winner: Optional[str], reason: str = "五子连珠"):
        """
        结束游戏
        
        Args:
            winner: 获胜者 ('black', 'white', None表示平局)
            reason: 结束原因
        """
        self.status = GameStatus.GAME_OVER
        self.game_end_time = time.time()
    
    def make_move(self, row: int, col: int, color: str, 
                  player_type: PlayerType, thinking_time: Optional[float] = None):
        """
        记录移动
        
        Args:
            row: 行坐标
            col: 列坐标
            color: 棋子颜色
            player_type: 玩家类型
            thinking_time: 思考时间（AI专用）
        """
        move = Move(
            row=row,
            col=col,
            color=color,
            timestamp=time.time(),
            player_type=player_type,
            thinking_time=thinking_time
        )
        
        self.move_history.append(move)
        self.total_moves += 1
        
        if thinking_time:
            self.ai_thinking_time += thinking_time
        
        # 切换玩家
        self.current_player = "white" if color == "black" else "black"
    
    def get_current_player_type(self) -> PlayerType:
        """获取当前玩家类型"""
        return self.player_types[self.current_player]
    
    def is_ai_turn(self) -> bool:
        """检查是否为AI回合"""
        return self.get_current_player_type() == PlayerType.AI
    
    def get_game_duration(self) -> float:
        """获取游戏持续时间"""
        if self.game_start_time is None:
            return 0.0
        
        end_time = self.game_end_time or time.time()
        return end_time - self.game_start_time
    
    def get_game_result(self) -> Optional[GameResult]:
        """获取游戏结果"""
        if self.status != GameStatus.GAME_OVER:
            return None
        
        # 确定获胜者
        winner = None
        if self.move_history:
            last_move = self.move_history[-1]
            # 这里需要结合棋盘状态判断获胜者
            # 简化实现，实际需要更复杂的逻辑
            winner = last_move.color
        
        return GameResult(
            winner=winner,
            reason="五子连珠",
            move_count=self.total_moves,
            duration=self.get_game_duration(),
            ai_thinking_time=self.ai_thinking_time
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取游戏统计信息"""
        return {
            'total_moves': self.total_moves,
            'game_duration': self.get_game_duration(),
            'ai_thinking_time': self.ai_thinking_time,
            'average_thinking_time': self.ai_thinking_time / max(self.total_moves // 2, 1),
            'moves_per_minute': self.total_moves / max(self.get_game_duration() / 60, 0.1),
            'current_player': self.current_player,
            'current_player_type': self.get_current_player_type().value,
            'game_status': self.status.value
        }
    
    def reset(self):
        """重置游戏状态"""
        self.status = GameStatus.MENU
        self.current_player = "black"
        self.player_colors = {"black": None, "white": None}
        self.player_types = {"black": PlayerType.HUMAN, "white": PlayerType.AI}
        self.move_history.clear()
        self.game_start_time = None
        self.game_end_time = None
        self.ai_thinking_time = 0.0
        self.total_moves = 0
    
    def pause_game(self):
        """暂停游戏"""
        if self.status == GameStatus.PLAYING:
            self.status = GameStatus.PAUSED
    
    def resume_game(self):
        """恢复游戏"""
        if self.status == GameStatus.PAUSED:
            self.status = GameStatus.PLAYING
    
    def get_move_history(self) -> List[Move]:
        """获取移动历史"""
        return self.move_history.copy()
    
    def get_last_move(self) -> Optional[Move]:
        """获取最后一步移动"""
        return self.move_history[-1] if self.move_history else None
    
    def set_ai_difficulty(self, difficulty: str):
        """设置AI难度"""
        self.ai_difficulty = difficulty
        difficulty_settings = {
            "easy": 50,
            "medium": 75,
            "hard": 100,
            "expert": 150
        }
        self.search_depth = difficulty_settings.get(difficulty, 100)
    
    def get_settings(self) -> Dict[str, Any]:
        """获取游戏设置"""
        return {
            'ai_difficulty': self.ai_difficulty,
            'search_depth': self.search_depth,
            'enable_animations': self.enable_animations,
            'sound_enabled': self.sound_enabled,
            'board_size': self.board_size
        }
    
    def update_settings(self, **kwargs):
        """更新游戏设置"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

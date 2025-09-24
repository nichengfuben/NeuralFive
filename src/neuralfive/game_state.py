"""
游戏状态管理模块

管理五子棋游戏的完整状态，包括棋盘状态、历史记录、
游戏流程控制等功能。
"""

import numpy as np
from typing import Optional, List, Tuple
from dataclasses import dataclass
from enum import Enum

class GameStatus(Enum):
    """游戏状态枚举"""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    AI_THINKING = "ai_thinking"

class PlayerType(Enum):
    """玩家类型枚举"""
    HUMAN = "human"
    AI = "ai"

@dataclass
class GameSettings:
    """游戏设置"""
    board_size: int = 15
    ai_difficulty: str = "expert"
    player_color: str = "black"
    ai_color: str = "white"
    time_limit: int = 30  # 每步时间限制（秒）
    allow_undo: bool = True
    sound_enabled: bool = True

class GameState:
    """
    游戏状态管理器
    
    负责管理五子棋游戏的完整状态，包括：
    - 棋盘状态
    - 游戏流程
    - 历史记录
    - 计时器
    - 统计信息
    """
    
    def __init__(self, settings: Optional[GameSettings] = None):
        """
        初始化游戏状态
        
        Args:
            settings: 游戏设置，如果为None则使用默认设置
        """
        self.settings = settings or GameSettings()
        self.status = GameStatus.MENU
        
        # 棋盘状态
        self.board = np.zeros(
            (self.settings.board_size, self.settings.board_size), 
            dtype=np.int32
        )
        
        # 游戏流程
        self.current_player = self.settings.player_color
        self.move_history = []
        self.move_count = 0
        
        # 计时器
        self.game_start_time = None
        self.move_start_time = None
        self.total_time = {"black": 0, "white": 0}
        self.move_time = {"black": 0, "white": 0}
        
        # 统计信息
        self.statistics = {
            "total_moves": 0,
            "ai_moves": 0,
            "human_moves": 0,
            "ai_thinking_time": 0,
            "longest_move": 0,
            "shortest_move": float('inf')
        }
        
        # 游戏结果
        self.winner = None
        self.winning_line = None
        self.game_over_reason = None
    
    def start_game(self) -> None:
        """开始新游戏"""
        self.status = GameStatus.PLAYING
        self.game_start_time = np.datetime64('now')
        self.move_start_time = np.datetime64('now')
        self.reset_board()
    
    def reset_board(self) -> None:
        """重置棋盘"""
        self.board = np.zeros(
            (self.settings.board_size, self.settings.board_size), 
            dtype=np.int32
        )
        self.move_history.clear()
        self.move_count = 0
        self.current_player = self.settings.player_color
        self.winner = None
        self.winning_line = None
        self.game_over_reason = None
        self.statistics = {
            "total_moves": 0,
            "ai_moves": 0,
            "human_moves": 0,
            "ai_thinking_time": 0,
            "longest_move": 0,
            "shortest_move": float('inf')
        }
    
    def make_move(self, row: int, col: int, color: str) -> bool:
        """
        在指定位置下棋
        
        Args:
            row: 行坐标 (0-14)
            col: 列坐标 (0-14)
            color: 棋子颜色 ("black" 或 "white")
            
        Returns:
            bool: 是否成功落子
        """
        if not self.is_valid_move(row, col):
            return False
        
        if color != self.current_player:
            return False
        
        # 更新棋盘
        color_num = 1 if color == "black" else 2
        self.board[row, col] = color_num
        
        # 记录移动
        move_info = {
            "row": row,
            "col": col,
            "color": color,
            "move_number": self.move_count + 1,
            "timestamp": np.datetime64('now')
        }
        self.move_history.append(move_info)
        self.move_count += 1
        
        # 更新统计
        self._update_move_statistics(color)
        
        # 检查游戏是否结束
        if self.check_winner():
            self.status = GameStatus.GAME_OVER
            self.winner = color
            return True
        
        # 切换玩家
        self.current_player = "white" if color == "black" else "black"
        self.move_start_time = np.datetime64('now')
        
        return True
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """
        检查移动是否有效
        
        Args:
            row: 行坐标
            col: 列坐标
            
        Returns:
            bool: 移动是否有效
        """
        if self.status != GameStatus.PLAYING:
            return False
        
        if not (0 <= row < self.settings.board_size and 
                0 <= col < self.settings.board_size):
            return False
        
        return self.board[row, col] == 0
    
    def undo_move(self) -> bool:
        """
        撤销上一步移动
        
        Returns:
            bool: 是否成功撤销
        """
        if not self.settings.allow_undo or not self.move_history:
            return False
        
        # 移除最后一步
        last_move = self.move_history.pop()
        row, col = last_move["row"], last_move["col"]
        
        # 更新棋盘
        self.board[row, col] = 0
        self.move_count -= 1
        
        # 切换回上一个玩家
        self.current_player = "white" if last_move["color"] == "black" else "black"
        
        return True
    
    def check_winner(self) -> Optional[str]:
        """
        检查是否有获胜者
        
        Returns:
            str: 获胜者颜色，如果没有则返回None
        """
        # 检查所有可能的五连
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for row in range(self.settings.board_size):
            for col in range(self.settings.board_size):
                if self.board[row, col] == 0:
                    continue
                
                color_num = self.board[row, col]
                color = "black" if color_num == 1 else "white"
                
                for dr, dc in directions:
                    count = 1
                    line_start = (row, col)
                    line_end = (row, col)
                    
                    # 正向检查
                    r, c = row + dr, col + dc
                    while (0 <= r < self.settings.board_size and 
                           0 <= c < self.settings.board_size and 
                           self.board[r, c] == color_num):
                        count += 1
                        line_end = (r, c)
                        r += dr
                        c += dc
                    
                    # 反向检查
                    r, c = row - dr, col - dc
                    while (0 <= r < self.settings.board_size and 
                           0 <= c < self.settings.board_size and 
                           self.board[r, c] == color_num):
                        count += 1
                        line_start = (r, c)
                        r -= dr
                        c -= dc
                    
                    if count >= 5:
                        self.winning_line = (line_start, line_end)
                        return color
        
        return None
    
    def is_board_full(self) -> bool:
        """检查棋盘是否已满"""
        return self.move_count >= self.settings.board_size ** 2
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """
        获取所有有效移动位置
        
        Returns:
            List[Tuple[int, int]]: 有效移动位置列表
        """
        valid_moves = []
        
        for row in range(self.settings.board_size):
            for col in range(self.settings.board_size):
                if self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        
        return valid_moves
    
    def get_game_info(self) -> dict:
        """
        获取游戏信息
        
        Returns:
            dict: 游戏信息字典
        """
        current_time = np.datetime64('now')
        
        return {
            "status": self.status.value,
            "current_player": self.current_player,
            "move_count": self.move_count,
            "total_moves": len(self.move_history),
            "winner": self.winner,
            "game_duration": (current_time - self.game_start_time).item() 
                             if self.game_start_time else 0,
            "last_move_time": self.move_history[-1]["timestamp"] 
                             if self.move_history else None,
            "statistics": self.statistics.copy()
        }
    
    def _update_move_statistics(self, color: str) -> None:
        """更新移动统计信息"""
        current_time = np.datetime64('now')
        
        if self.move_start_time:
            move_duration = (current_time - self.move_start_time).item()
            
            # 更新移动时间统计
            self.statistics["longest_move"] = max(
                self.statistics["longest_move"], move_duration
            )
            self.statistics["shortest_move"] = min(
                self.statistics["shortest_move"], move_duration
            )
        
        # 更新移动计数
        self.statistics["total_moves"] += 1
        if color == self.settings.player_color:
            self.statistics["human_moves"] += 1
        else:
            self.statistics["ai_moves"] += 1
    
    def export_game_data(self) -> dict:
        """
        导出游戏数据
        
        Returns:
            dict: 完整的游戏数据
        """
        return {
            "settings": {
                "board_size": self.settings.board_size,
                "ai_difficulty": self.settings.ai_difficulty,
                "player_color": self.settings.player_color,
                "ai_color": self.settings.ai_color
            },
            "game_state": {
                "status": self.status.value,
                "current_player": self.current_player,
                "winner": self.winner,
                "winning_line": self.winning_line,
                "board": self.board.tolist()
            },
            "move_history": self.move_history.copy(),
            "statistics": self.statistics.copy()
        }
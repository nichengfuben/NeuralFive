"""
游戏棋盘管理

提供棋盘状态管理、移动验证、胜负判断等功能
"""

from typing import List, Tuple, Optional, Dict, Any
import numpy as np


class GameBoard:
    """游戏棋盘类"""
    
    def __init__(self, size: int = 15):
        """
        初始化棋盘
        
        Args:
            size: 棋盘大小 (默认15x15)
        """
        self.size = size
        self.board = np.zeros((size, size), dtype=int)
        self.move_history = []
        self.last_move = None
        
        # 棋盘状态常量
        self.EMPTY = 0
        self.BLACK = 1
        self.WHITE = 2
    
    def reset(self):
        """重置棋盘"""
        self.board.fill(self.EMPTY)
        self.move_history.clear()
        self.last_move = None
    
    def make_move(self, row: int, col: int, color: str) -> bool:
        """
        在指定位置下棋
        
        Args:
            row: 行坐标
            col: 列坐标
            color: 棋子颜色 ('black' 或 'white')
            
        Returns:
            是否成功下棋
        """
        if not self.is_valid_move(row, col):
            return False
        
        piece_value = self.BLACK if color == 'black' else self.WHITE
        self.board[row][col] = piece_value
        self.move_history.append((row, col, color))
        self.last_move = (row, col)
        
        return True
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """
        检查移动是否有效
        
        Args:
            row: 行坐标
            col: 列坐标
            
        Returns:
            是否有效
        """
        return (0 <= row < self.size and 
                0 <= col < self.size and 
                self.board[row][col] == self.EMPTY)
    
    def get_board_state(self) -> List[List[int]]:
        """获取棋盘状态"""
        return self.board.tolist()
    
    def get_board_string(self) -> str:
        """获取棋盘字符串表示"""
        result = []
        for row in self.board:
            line = ""
            for cell in row:
                if cell == self.BLACK:
                    line += "B"
                elif cell == self.WHITE:
                    line += "W"
                else:
                    line += "."
            result.append(line)
        return "\n".join(result)
    
    def check_winner(self) -> Optional[str]:
        """
        检查是否有获胜者
        
        Returns:
            获胜者颜色 ('black', 'white') 或 None
        """
        if not self.last_move:
            return None
        
        row, col = self.last_move
        color = self.board[row][col]
        
        # 检查四个方向
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count = self._count_consecutive(row, col, dx, dy, color)
            if count >= 5:
                return 'black' if color == self.BLACK else 'white'
        
        return None
    
    def _count_consecutive(self, row: int, col: int, dx: int, dy: int, color: int) -> int:
        """计算连续棋子数量"""
        count = 1
        
        # 向正方向计数
        r, c = row + dx, col + dy
        while (0 <= r < self.size and 0 <= c < self.size and 
               self.board[r][c] == color):
            count += 1
            r += dx
            c += dy
        
        # 向负方向计数
        r, c = row - dx, col - dy
        while (0 <= r < self.size and 0 <= c < self.size and 
               self.board[r][c] == color):
            count += 1
            r -= dx
            c -= dy
        
        return count
    
    def is_full(self) -> bool:
        """检查棋盘是否已满"""
        return np.all(self.board != self.EMPTY)
    
    def get_empty_positions(self) -> List[Tuple[int, int]]:
        """获取所有空位置"""
        positions = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == self.EMPTY:
                    positions.append((i, j))
        return positions
    
    def get_neighbor_positions(self, row: int, col: int, radius: int = 2) -> List[Tuple[int, int]]:
        """获取指定位置周围的空位置"""
        positions = []
        for i in range(max(0, row - radius), min(self.size, row + radius + 1)):
            for j in range(max(0, col - radius), min(self.size, col + radius + 1)):
                if (i != row or j != col) and self.board[i][j] == self.EMPTY:
                    positions.append((i, j))
        return positions
    
    def get_game_info(self) -> Dict[str, Any]:
        """获取游戏信息"""
        return {
            'size': self.size,
            'move_count': len(self.move_history),
            'last_move': self.last_move,
            'is_full': self.is_full(),
            'winner': self.check_winner(),
            'empty_count': len(self.get_empty_positions())
        }
    
    def copy(self) -> 'GameBoard':
        """创建棋盘副本"""
        new_board = GameBoard(self.size)
        new_board.board = self.board.copy()
        new_board.move_history = self.move_history.copy()
        new_board.last_move = self.last_move
        return new_board

"""
游戏规则模块

定义五子棋游戏规则和约束
"""

from typing import List, Tuple, Optional, Dict, Any
from enum import Enum


class GamePhase(Enum):
    """游戏阶段"""
    OPENING = "opening"      # 开局
    MIDDLE = "middle"        # 中局
    ENDGAME = "endgame"      # 残局


class GameRules:
    """五子棋游戏规则"""
    
    def __init__(self, board_size: int = 15):
        """
        初始化游戏规则
        
        Args:
            board_size: 棋盘大小
        """
        self.board_size = board_size
        self.win_length = 5  # 获胜所需连子数
        
        # 禁手规则（可选）
        self.forbidden_moves_enabled = False
        self.double_three_forbidden = True
        self.double_four_forbidden = True
        self.overline_forbidden = True
    
    def is_valid_move(self, board: List[List[int]], row: int, col: int, 
                     color: str) -> Tuple[bool, str]:
        """
        检查移动是否合法
        
        Args:
            board: 棋盘状态
            row: 行坐标
            col: 列坐标
            color: 棋子颜色
            
        Returns:
            (是否合法, 错误信息)
        """
        # 检查坐标范围
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return False, "坐标超出棋盘范围"
        
        # 检查位置是否为空
        if board[row][col] != 0:
            return False, "该位置已有棋子"
        
        # 检查禁手规则
        if self.forbidden_moves_enabled:
            is_forbidden, reason = self._check_forbidden_move(board, row, col, color)
            if is_forbidden:
                return False, f"禁手: {reason}"
        
        return True, ""
    
    def _check_forbidden_move(self, board: List[List[int]], row: int, col: int, 
                             color: str) -> Tuple[bool, str]:
        """检查禁手规则"""
        if color != 'black':  # 只有黑棋有禁手
            return False, ""
        
        # 检查双三禁手
        if self.double_three_forbidden and self._is_double_three(board, row, col):
            return True, "双三禁手"
        
        # 检查双四禁手
        if self.double_four_forbidden and self._is_double_four(board, row, col):
            return True, "双四禁手"
        
        # 检查长连禁手
        if self.overline_forbidden and self._is_overline(board, row, col):
            return True, "长连禁手"
        
        return False, ""
    
    def _is_double_three(self, board: List[List[int]], row: int, col: int) -> bool:
        """检查双三禁手"""
        # 简化实现，实际需要更复杂的逻辑
        three_count = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            if self._count_line(board, row, col, dx, dy, 1) == 3:
                three_count += 1
        
        return three_count >= 2
    
    def _is_double_four(self, board: List[List[int]], row: int, col: int) -> bool:
        """检查双四禁手"""
        four_count = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            if self._count_line(board, row, col, dx, dy, 1) == 4:
                four_count += 1
        
        return four_count >= 2
    
    def _is_overline(self, board: List[List[int]], row: int, col: int) -> bool:
        """检查长连禁手"""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            if self._count_line(board, row, col, dx, dy, 1) > 5:
                return True
        
        return False
    
    def _count_line(self, board: List[List[int]], row: int, col: int, 
                   dx: int, dy: int, color: int) -> int:
        """计算指定方向的连子数"""
        count = 1
        
        # 向正方向计数
        r, c = row + dx, col + dy
        while (0 <= r < self.board_size and 0 <= c < self.board_size and 
               board[r][c] == color):
            count += 1
            r += dx
            c += dy
        
        # 向负方向计数
        r, c = row - dx, col - dy
        while (0 <= r < self.board_size and 0 <= c < self.board_size and 
               board[r][c] == color):
            count += 1
            r -= dx
            c -= dy
        
        return count
    
    def check_winner(self, board: List[List[int]], last_move: Tuple[int, int]) -> Optional[str]:
        """
        检查获胜者
        
        Args:
            board: 棋盘状态
            last_move: 最后一步移动
            
        Returns:
            获胜者颜色或None
        """
        if not last_move:
            return None
        
        row, col = last_move
        color = board[row][col]
        
        if color == 0:
            return None
        
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dx, dy in directions:
            count = self._count_line(board, row, col, dx, dy, color)
            if count >= self.win_length:
                return 'black' if color == 1 else 'white'
        
        return None
    
    def get_game_phase(self, move_count: int) -> GamePhase:
        """
        获取当前游戏阶段
        
        Args:
            move_count: 已下棋子数
            
        Returns:
            游戏阶段
        """
        if move_count <= 10:
            return GamePhase.OPENING
        elif move_count <= 50:
            return GamePhase.MIDDLE
        else:
            return GamePhase.ENDGAME
    
    def get_opening_moves(self) -> List[Tuple[int, int]]:
        """获取开局推荐移动"""
        center = self.board_size // 2
        return [
            (center, center),           # 中心
            (center - 1, center - 1),   # 左上
            (center + 1, center + 1),   # 右下
            (center - 1, center + 1),   # 右上
            (center + 1, center - 1),   # 左下
        ]
    
    def is_opening_move(self, row: int, col: int) -> bool:
        """检查是否为开局移动"""
        center = self.board_size // 2
        distance = abs(row - center) + abs(col - center)
        return distance <= 2
    
    def get_rule_info(self) -> Dict[str, Any]:
        """获取规则信息"""
        return {
            'board_size': self.board_size,
            'win_length': self.win_length,
            'forbidden_moves_enabled': self.forbidden_moves_enabled,
            'double_three_forbidden': self.double_three_forbidden,
            'double_four_forbidden': self.double_four_forbidden,
            'overline_forbidden': self.overline_forbidden,
        }
    
    def set_forbidden_rules(self, enabled: bool, double_three: bool = True, 
                           double_four: bool = True, overline: bool = True):
        """设置禁手规则"""
        self.forbidden_moves_enabled = enabled
        self.double_three_forbidden = double_three
        self.double_four_forbidden = double_four
        self.overline_forbidden = overline

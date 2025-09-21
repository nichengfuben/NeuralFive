"""
位置评估器

提供多维度棋盘位置评估功能，包括：
- 连子评估
- 位置价值评估
- 攻防平衡评估
- 局势判断
"""

import numpy as np
from typing import List, Tuple
from numba import jit


class PositionEvaluator:
    """位置评估器"""
    
    def __init__(self, board_size: int = 15):
        """
        初始化评估器
        
        Args:
            board_size: 棋盘大小
        """
        self.board_size = board_size
        
        # 连子分数表
        self.line_scores = {
            1: 1,      # 单子
            2: 10,     # 两子
            3: 2000,   # 三子
            4: 4000,   # 四子
            5: 100000000000  # 五子（获胜）
        }
        
        # 位置价值表（中心位置更有价值）
        self.position_values = self._generate_position_values()
        
        # 方向向量
        self.directions = [
            (0, 1),   # 水平
            (1, 0),   # 垂直
            (1, 1),   # 主对角线
            (1, -1)   # 副对角线
        ]
    
    def _generate_position_values(self) -> np.ndarray:
        """生成位置价值表"""
        values = np.zeros((self.board_size, self.board_size))
        center = self.board_size // 2
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                # 距离中心的距离
                distance = abs(i - center) + abs(j - center)
                # 中心位置价值更高
                values[i][j] = max(0, 10 - distance)
        
        return values
    
    def evaluate_position(self, board: List[List], color: str) -> float:
        """
        评估当前棋盘位置
        
        Args:
            board: 棋盘状态
            color: 评估的颜色
            
        Returns:
            位置评估分数
        """
        score = 0
        
        # 连子评估
        score += self._evaluate_lines(board, color)
        
        # 位置价值评估
        score += self._evaluate_position_values(board, color)
        
        # 攻防平衡评估
        score += self._evaluate_attack_defense_balance(board, color)
        
        return score
    
    def _evaluate_lines(self, board: List[List], color: str) -> float:
        """评估连子情况"""
        score = 0
        target_color = 1 if color == 'black' else 2
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == target_color:
                    # 检查四个方向的连子
                    for dx, dy in self.directions:
                        line_length = self._count_line_length(
                            board, i, j, dx, dy, target_color
                        )
                        if line_length > 0:
                            score += self.line_scores.get(line_length, 0)
        
        return score
    
    def _count_line_length(self, board: List[List], x: int, y: int, 
                          dx: int, dy: int, color: int) -> int:
        """计算指定方向的连子长度"""
        count = 1
        
        # 向正方向计数
        nx, ny = x + dx, y + dy
        while (0 <= nx < self.board_size and 0 <= ny < self.board_size 
               and board[nx][ny] == color):
            count += 1
            nx += dx
            ny += dy
        
        # 向负方向计数
        nx, ny = x - dx, y - dy
        while (0 <= nx < self.board_size and 0 <= ny < self.board_size 
               and board[nx][ny] == color):
            count += 1
            nx -= dx
            ny -= dy
        
        return count
    
    def _evaluate_position_values(self, board: List[List], color: str) -> float:
        """评估位置价值"""
        score = 0
        target_color = 1 if color == 'black' else 2
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == target_color:
                    score += self.position_values[i][j]
        
        return score
    
    def _evaluate_attack_defense_balance(self, board: List[List], color: str) -> float:
        """评估攻防平衡"""
        attack_score = self._evaluate_lines(board, color)
        defense_score = self._evaluate_lines(board, 'white' if color == 'black' else 'black')
        
        # 攻防平衡：攻击分数 - 防守分数
        return attack_score - defense_score * 0.8
    
    def get_candidate_moves(self, board: List[List], num_candidates: int = 25) -> List[Tuple[int, int]]:
        """
        获取候选移动位置
        
        Args:
            board: 当前棋盘状态
            num_candidates: 候选数量
            
        Returns:
            候选位置列表
        """
        candidates = []
        
        # 如果棋盘为空，返回中心位置
        if not any(any(row) for row in board):
            center = self.board_size // 2
            return [(center, center)]
        
        # 寻找已有棋子周围的位置
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == 0:  # 空位
                    # 检查是否在已有棋子附近
                    if self._is_near_existing_piece(board, i, j):
                        score = self._evaluate_move_potential(board, i, j)
                        candidates.append((score, i, j))
        
        # 按分数排序，返回前num_candidates个
        candidates.sort(key=lambda x: x[0], reverse=True)
        return [(i, j) for _, i, j in candidates[:num_candidates]]
    
    def _is_near_existing_piece(self, board: List[List], x: int, y: int) -> bool:
        """检查位置是否在已有棋子附近"""
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.board_size and 0 <= ny < self.board_size 
                    and board[nx][ny] != 0):
                    return True
        return False
    
    def _evaluate_move_potential(self, board: List[List], x: int, y: int) -> float:
        """评估移动的潜在价值"""
        score = 0
        
        # 位置价值
        score += self.position_values[x][y]
        
        # 周围棋子密度
        density = 0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.board_size and 0 <= ny < self.board_size 
                    and board[nx][ny] != 0):
                    density += 1
        score += density * 2
        
        return score

"""
StrategicMind AI引擎

基于Negamax算法和Alpha-Beta剪枝的高性能AI引擎
使用Numba JIT编译优化，支持深度搜索和智能缓存
"""

import numpy as np
from numba import jit, njit
from numba.typed import List
import numba
from typing import Tuple, Optional, List as TypingList
import time

from .evaluator import PositionEvaluator
from .search import NegamaxSearch


class MapPoint:
    """棋盘位置点数据结构"""
    
    def __init__(self, r: int, c: int):
        self.r = r
        self.c = c
        self.set = False
        self.score = 0
        self.valid = False
        self.info = [[0, 0, 0, 0] for _ in range(4)]  # 四个方向的连子信息


class StrategicAI:
    """
    StrategicMind核心AI引擎
    
    特性:
    - 深度搜索算法 (默认100层)
    - Alpha-Beta剪枝优化
    - 智能缓存机制
    - 多维度位置评估
    - 自适应搜索深度
    """
    
    def __init__(self, board_size: int = 15, search_depth: int = 100):
        """
        初始化AI引擎
        
        Args:
            board_size: 棋盘大小 (默认15x15)
            search_depth: 搜索深度 (默认100层)
        """
        self.board_size = board_size
        self.search_depth = search_depth
        
        # 四个搜索方向：左上-右下对角线，垂直，水平，右上-左下对角线
        self.moves = [[-1, -1], [-1, 0], [0, -1], [-1, 1]]
        self.coe = [-2, 1]  # 系数：对手-2，己方1
        self.scores = [0, 1, 10, 2000, 4000, 100000000000]  # 不同连子数的分数
        
        # 搜索参数
        self.depth = search_depth
        self.totry = [20, 18]  # 候选移动数量
        
        # 游戏状态
        self.color = None
        self.otc = None  # 对手颜色
        self.sum = 0
        self.set_num = 0
        self.map = []
        self.score_queue = []
        
        # 性能优化
        self.board_buf = [0] * (board_size * board_size)
        self.cache = {}
        
        # 初始化棋盘
        self._initialize_board()
        
        # 评估器和搜索器
        self.evaluator = PositionEvaluator(board_size)
        self.searcher = NegamaxSearch(self)
    
    def _initialize_board(self):
        """初始化棋盘数据结构"""
        for i in range(self.board_size):
            tmp = []
            for j in range(self.board_size):
                point = MapPoint(i, j)
                tmp.append(point)
                self.score_queue.append(point)
            self.map.append(tmp)
    
    def clear_board(self):
        """清空棋盘"""
        self.sum = 0
        self.set_num = 0
        self.cache = {}
        self.board_buf = [0] * (self.board_size * self.board_size)
        
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.map[i][j].set = False
                self.map[i][j].score = 0
                self.map[i][j].valid = False
                self.map[i][j].info = [[0, 0, 0, 0] for _ in range(4)]
        
        self.score_queue = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.score_queue.append(self.map[i][j])
    
    def make_move(self, r: int, c: int, player_color: str) -> str:
        """
        玩家下棋，AI自动响应
        
        Args:
            r: 行坐标 (0-14)
            c: 列坐标 (0-14) 
            player_color: 玩家颜色 'black' 或 'white'
            
        Returns:
            棋盘状态字符串，B=黑子，W=白子，.=空位
        """
        # 设置AI颜色
        self.color = 'white' if player_color == 'black' else 'black'
        self.otc = player_color
        
        # 玩家下棋
        self._update_map(r, c, player_color)
        self.set_num += 1
        self.score_queue.sort(key=self._sort_move_key)
        
        # 检查游戏是否结束
        if self._check_win():
            return self._get_board_string()
        
        # AI计算最佳移动
        start_time = time.time()
        best_move = self._compute_best_move()
        thinking_time = time.time() - start_time
        
        if best_move:
            ai_r, ai_c = best_move
            self._update_map(ai_r, ai_c, self.color)
            self.set_num += 1
            self.score_queue.sort(key=self._sort_move_key)
        
        return self._get_board_string()
    
    def _get_board_string(self) -> str:
        """获取棋盘状态字符串"""
        result = []
        for i in range(self.board_size):
            row = ""
            for j in range(self.board_size):
                if self.map[i][j].set == 1:  # 黑子
                    row += "B"
                elif self.map[i][j].set == 2:  # 白子
                    row += "W"
                else:
                    row += "."
            result.append(row)
        return "\n".join(result)
    
    def _check_win(self) -> bool:
        """检查是否有获胜者"""
        return abs(self.sum) >= 10000000
    
    def _update_map(self, r: int, c: int, color: str):
        """更新棋盘状态"""
        if color == 'black':
            num = 0
        elif color == 'white':
            num = 1
        else:
            return
        
        self._update_map_internal(r, c, num, False)
    
    def _update_map_internal(self, r: int, c: int, num: int, remove: bool):
        """内部更新棋盘逻辑"""
        moves = self.moves
        coe = self.coe
        scores = self.scores
        changes = 0
        
        if not remove:
            self.board_buf[r * self.board_size + c] = num + 2
            self.map[r][c].set = num + 1
            
            for i in range(4):
                x, y = r, c
                step = 5
                while step > 0 and x >= 0 and y >= 0 and y < self.board_size:
                    xx = x - moves[i][0] * 4
                    yy = y - moves[i][1] * 4
                    if xx >= self.board_size or yy < 0 or yy >= self.board_size:
                        x += moves[i][0]
                        y += moves[i][1]
                        step -= 1
                        continue
                    
                    cur = self.map[x][y].info[i]
                    if cur[2] > 0:
                        tmp = 5
                        xx, yy = x, y
                        s = scores[cur[2]]
                        changes -= s * cur[3]
                        while tmp > 0:
                            if 0 <= xx < self.board_size and 0 <= yy < self.board_size:
                                self.map[xx][yy].score -= s
                            xx -= moves[i][0]
                            yy -= moves[i][1]
                            tmp -= 1
                    
                    cur[num] += 1
                    if cur[1 - num] > 0:
                        cur[2] = 0
                    else:
                        cur[2] = cur[num]
                        e = coe[num]
                        cur[3] = e
                        s = scores[cur[2]]
                        tmp = 5
                        xx, yy = x, y
                        changes += s * cur[3]
                        while tmp > 0:
                            if 0 <= xx < self.board_size and 0 <= yy < self.board_size:
                                self.map[xx][yy].score += s
                            xx -= moves[i][0]
                            yy -= moves[i][1]
                            tmp -= 1
                    
                    x += moves[i][0]
                    y += moves[i][1]
                    step -= 1
        else:
            self.board_buf[r * self.board_size + c] = 0
            self.map[r][c].set = False
            
            for i in range(4):
                x, y = r, c
                step = 5
                while step > 0 and x >= 0 and y >= 0 and y < self.board_size:
                    xx = x - moves[i][0] * 4
                    yy = y - moves[i][1] * 4
                    if xx >= self.board_size or yy < 0 or yy >= self.board_size:
                        x += moves[i][0]
                        y += moves[i][1]
                        step -= 1
                        continue
                    
                    cur = self.map[x][y].info[i]
                    sc = 0
                    cur[num] -= 1
                    
                    if cur[2] > 0:
                        tmp = 5
                        xx, yy = x, y
                        s = scores[cur[2]]
                        changes -= s * cur[3]
                        while tmp > 0:
                            if 0 <= xx < self.board_size and 0 <= yy < self.board_size:
                                self.map[xx][yy].score -= s
                            xx -= moves[i][0]
                            yy -= moves[i][1]
                            tmp -= 1
                        cur[2] -= 1
                        if cur[num] > 0:
                            sc = 1
                    elif cur[1 - num] > 0 and cur[num] == 0:
                        sc = -1
                    
                    if sc == 1:
                        tmp = 5
                        s = scores[cur[2]]
                        xx, yy = x, y
                        changes += s * cur[3]
                        while tmp > 0:
                            if 0 <= xx < self.board_size and 0 <= yy < self.board_size:
                                self.map[xx][yy].score += s
                            xx -= moves[i][0]
                            yy -= moves[i][1]
                            tmp -= 1
                    elif sc == -1:
                        cur[2] = cur[1 - num]
                        tmp = 5
                        s = scores[cur[2]]
                        cur[3] = coe[1 - num]
                        xx, yy = x, y
                        changes += s * cur[3]
                        while tmp > 0:
                            if 0 <= xx < self.board_size and 0 <= yy < self.board_size:
                                self.map[xx][yy].score += s
                            xx -= moves[i][0]
                            yy -= moves[i][1]
                            tmp -= 1
                    
                    x += moves[i][0]
                    y += moves[i][1]
                    step -= 1
        
        self.sum += changes
    
    def _sort_move_key(self, point: MapPoint) -> Tuple[int, int]:
        """排序关键字函数"""
        if point.set:
            return (1, 0)
        return (0, -point.score)
    
    def _simulate(self, x: int, y: int, num: int):
        """模拟下棋"""
        self.set_num += 1
        self._update_map_internal(x, y, num, False)
    
    def _desimulate(self, x: int, y: int, num: int):
        """撤销模拟"""
        self._update_map_internal(x, y, num, True)
        self.set_num -= 1
    
    def _buf_to_string(self) -> str:
        """将棋盘状态转换为字符串用于缓存"""
        return ''.join(str(x) for x in self.board_buf)
    
    def _compute_best_move(self) -> Optional[Tuple[int, int]]:
        """计算最佳移动"""
        self.cache = {}
        
        alpha = float('-inf')
        beta = float('inf')
        
        # 获取候选移动
        candidates = []
        for point in self.score_queue:
            if point.set:
                continue
            if len(candidates) >= 25:  # 增加候选数量
                break
            candidates.append((point.r, point.c))
        
        if not candidates:
            return None
        
        best_move = candidates[0]
        depth = self.depth
        
        for r, c in candidates:
            b = beta if alpha == float('-inf') else alpha + 1
            score = -self._nega(r, c, depth, -b, -alpha)
            
            if alpha < score < beta and alpha != float('-inf'):
                score = -self._nega(r, c, depth, -beta, -alpha)
            
            if score > alpha:
                alpha = score
                best_move = (r, c)
        
        return best_move
    
    def _nega(self, x: int, y: int, depth: int, alpha: float, beta: float) -> float:
        """Negamax算法实现"""
        num = depth % 2
        self._simulate(x, y, num)
        
        buf_str = self._buf_to_string()
        if buf_str in self.cache:
            result = self.cache[buf_str]
            self._desimulate(x, y, num)
            return result
        
        if abs(self.sum) >= 10000000:
            self._desimulate(x, y, num)
            return float('-inf')
        
        if self.set_num == self.board_size * self.board_size:
            self._desimulate(x, y, num)
            return 0
        elif depth == 0:
            result = self.sum
            self._desimulate(x, y, num)
            return result
        
        self.score_queue.sort(key=self._sort_move_key)
        
        tmp_queue = []
        count = 0
        for tmp in self.score_queue:
            if tmp.set:
                continue
            if count >= self.totry[num]:
                break
            tmp_queue.append(tmp.c)
            tmp_queue.append(tmp.r)
            count += 1
        
        if not tmp_queue:
            self._desimulate(x, y, num)
            return 0
        
        depth -= 1
        i = len(tmp_queue) - 1
        b = beta
        
        if i >= 1:
            x_next = tmp_queue[i]
            y_next = tmp_queue[i - 1]
            score = -self._nega(x_next, y_next, depth, -b, -alpha)
            
            if score > alpha:
                buf_str = self._buf_to_string()
                self.cache[buf_str] = score
                alpha = score
            
            if alpha >= beta:
                buf_str = self._buf_to_string()
                self.cache[buf_str] = beta
                self._desimulate(x, y, num)
                return alpha
            
            b = alpha + 1
            i -= 2
            
            while i >= 1:
                x_next = tmp_queue[i]
                y_next = tmp_queue[i - 1]
                score = -self._nega(x_next, y_next, depth, -b, -alpha)
                
                if alpha < score < beta and alpha != float('-inf'):
                    score = -self._nega(x_next, y_next, depth, -beta, -alpha)
                
                if score > alpha:
                    alpha = score
                
                if alpha >= beta:
                    self._desimulate(x, y, num)
                    return alpha
                
                b = alpha + 1
                i -= 2
        
        self._desimulate(x, y, num)
        return alpha


# 兼容性函数
def create_ai():
    """创建AI实例 - 兼容旧版本API"""
    return StrategicAI()

def clear_board(ai):
    """清空棋盘 - 兼容旧版本API"""
    ai.clear_board()
    return "棋盘已清空"

def make_move(ai, r, c, color='black'):
    """
    下棋并获取AI响应 - 兼容旧版本API
    
    Args:
        ai: AI实例
        r: 行坐标 (0-14)
        c: 列坐标 (0-14)
        color: 玩家颜色 'black' 或 'white'
    Returns:
        棋盘状态字符串，B=黑子，W=白子，.=空位
    """
    return ai.make_move(r, c, color)

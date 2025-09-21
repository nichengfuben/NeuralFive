"""
搜索算法模块

实现Negamax搜索算法和Alpha-Beta剪枝优化
"""

from typing import Tuple, Optional, List
import time


class NegamaxSearch:
    """Negamax搜索算法实现"""
    
    def __init__(self, ai_engine):
        """
        初始化搜索器
        
        Args:
            ai_engine: AI引擎实例
        """
        self.ai = ai_engine
        self.nodes_searched = 0
        self.cache_hits = 0
        self.start_time = 0
        self.max_time = 5.0  # 最大搜索时间（秒）
    
    def search(self, depth: int, alpha: float, beta: float) -> float:
        """
        执行Negamax搜索
        
        Args:
            depth: 搜索深度
            alpha: Alpha值
            beta: Beta值
            
        Returns:
            最佳分数
        """
        self.nodes_searched = 0
        self.cache_hits = 0
        self.start_time = time.time()
        
        return self._negamax(depth, alpha, beta)
    
    def _negamax(self, depth: int, alpha: float, beta: float) -> float:
        """Negamax算法核心实现"""
        # 检查时间限制
        if time.time() - self.start_time > self.max_time:
            return self._evaluate_current_position()
        
        self.nodes_searched += 1
        
        # 检查终止条件
        if depth == 0 or self.ai._check_win():
            return self._evaluate_current_position()
        
        # 检查缓存
        board_key = self.ai._buf_to_string()
        if board_key in self.ai.cache:
            self.cache_hits += 1
            return self.ai.cache[board_key]
        
        # 获取候选移动
        candidates = self._get_candidates()
        if not candidates:
            return 0
        
        best_score = float('-inf')
        
        for move in candidates:
            # 模拟移动
            self._make_move(move)
            
            # 递归搜索
            score = -self._negamax(depth - 1, -beta, -alpha)
            
            # 撤销移动
            self._undo_move(move)
            
            # 更新最佳分数
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            
            # Alpha-Beta剪枝
            if alpha >= beta:
                break
        
        # 缓存结果
        self.ai.cache[board_key] = best_score
        
        return best_score
    
    def _get_candidates(self) -> List[Tuple[int, int]]:
        """获取候选移动"""
        candidates = []
        
        # 按分数排序获取候选位置
        self.ai.score_queue.sort(key=self.ai._sort_move_key)
        
        count = 0
        for point in self.ai.score_queue:
            if point.set:
                continue
            if count >= self.ai.totry[0]:  # 使用第一个候选数量
                break
            candidates.append((point.r, point.c))
            count += 1
        
        return candidates
    
    def _make_move(self, move: Tuple[int, int]):
        """模拟下棋"""
        r, c = move
        num = self.ai.set_num % 2
        self.ai._simulate(r, c, num)
    
    def _undo_move(self, move: Tuple[int, int]):
        """撤销下棋"""
        r, c = move
        num = (self.ai.set_num - 1) % 2
        self.ai._desimulate(r, c, num)
    
    def _evaluate_current_position(self) -> float:
        """评估当前位置"""
        return self.ai.sum
    
    def get_search_stats(self) -> dict:
        """获取搜索统计信息"""
        search_time = time.time() - self.start_time
        return {
            'nodes_searched': self.nodes_searched,
            'cache_hits': self.cache_hits,
            'search_time': search_time,
            'nodes_per_second': self.nodes_searched / max(search_time, 0.001),
            'cache_hit_rate': self.cache_hits / max(self.nodes_searched, 1)
        }

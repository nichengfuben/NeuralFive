# NeuralFive 架构设计

## 系统架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    用户界面层 (UI Layer)                      │
├─────────────────────────────────────────────────────────────┤
│  GUI组件    │  命令行接口  │  Web API  │  游戏渲染引擎     │
│  GUI.py     │  CLI.py     │  API.py   │  Renderer.py     │
├─────────────────────────────────────────────────────────────┤
│                    应用层 (Application Layer)               │
├─────────────────────────────────────────────────────────────┤
│  游戏控制器  │  AI控制器    │  状态管理器 │  事件处理器     │
│  GameCtrl   │  AICtrl     │  StateMgr  │  EventHandler   │
├─────────────────────────────────────────────────────────────┤
│                    领域层 (Domain Layer)                    │
├─────────────────────────────────────────────────────────────┤
│  游戏状态    │  AI引擎      │  评估函数   │  搜索算法       │
│  GameState  │  AIEngine   │  Evaluator │  SearchAlgo     │
├─────────────────────────────────────────────────────────────┤
│                    基础设施层 (Infrastructure Layer)          │
├─────────────────────────────────────────────────────────────┤
│  配置管理    │  日志系统    │  持久化存储 │  资源管理       │
│  Config     │  Logger     │  Storage    │  ResourceMgr    │
└─────────────────────────────────────────────────────────────┘
```

## 核心组件设计

### 1. 游戏状态管理 (Game State Management)

```python
# src/game/game_state.py
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple
import numpy as np

class PlayerType(Enum):
    BLACK = 1
    WHITE = -1
    EMPTY = 0

class GameStatus(Enum):
    ONGOING = "ongoing"
    BLACK_WINS = "black_wins"
    WHITE_WINS = "white_wins"
    DRAW = "draw"

@dataclass
class Move:
    """落子动作"""
    row: int
    col: int
    player: PlayerType
    timestamp: float
    evaluation_score: Optional[float] = None

@dataclass
class GameState:
    """游戏状态核心类"""
    board_size: int = 15
    board: np.ndarray = None
    current_player: PlayerType = PlayerType.BLACK
    game_status: GameStatus = GameStatus.ONGOING
    move_history: List[Move] = None
    
    def __post_init__(self):
        if self.board is None:
            self.board = np.zeros((self.board_size, self.board_size), dtype=np.int8)
        if self.move_history is None:
            self.move_history = []
    
    def make_move(self, row: int, col: int) -> bool:
        """执行落子动作"""
        if not self.is_valid_move(row, col):
            return False
        
        move = Move(row, col, self.current_player, time.time())
        self.board[row, col] = self.current_player.value
        self.move_history.append(move)
        
        # 检查获胜
        if self.check_winner_at(row, col):
            self.game_status = GameStatus.BLACK_WINS if self.current_player == PlayerType.BLACK else GameStatus.WHITE_WINS
        elif len(self.move_history) >= self.board_size * self.board_size:
            self.game_status = GameStatus.DRAW
        else:
            self.current_player = PlayerType.WHITE if self.current_player == PlayerType.BLACK else PlayerType.BLACK
        
        return True
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """检查落子是否有效"""
        return (0 <= row < self.board_size and 
                0 <= col < self.board_size and 
                self.board[row, col] == PlayerType.EMPTY.value and
                self.game_status == GameStatus.ONGOING)
    
    def check_winner_at(self, row: int, col: int) -> bool:
        """检查指定位置是否形成五连"""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 水平、垂直、对角线
        player = self.board[row, col]
        
        for dr, dc in directions:
            count = 1
            
            # 正向计数
            r, c = row + dr, col + dc
            while (0 <= r < self.board_size and 
                   0 <= c < self.board_size and 
                   self.board[r, c] == player):
                count += 1
                r += dr
                c += dc
            
            # 反向计数
            r, c = row - dr, col - dc
            while (0 <= r < self.board_size and 
                   0 <= c < self.board_size and 
                   self.board[r, c] == player):
                count += 1
                r -= dr
                c -= dc
            
            if count >= 5:
                return True
        
        return False
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """获取所有有效落子位置"""
        valid_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_valid_move(row, col):
                    valid_moves.append((row, col))
        return valid_moves
    
    def evaluate_position(self) -> float:
        """评估当前局面"""
        # 简化的评估函数
        score = 0
        
        # 评估每个位置
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row, col] != PlayerType.EMPTY.value:
                    position_score = self.evaluate_position_at(row, col)
                    if self.board[row, col] == PlayerType.BLACK.value:
                        score += position_score
                    else:
                        score -= position_score
        
        return score
    
    def evaluate_position_at(self, row: int, col: int) -> float:
        """评估指定位置的分数"""
        player = self.board[row, col]
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            blocked = 0
            
            # 正向计数
            r, c = row + dr, col + dc
            while (0 <= r < self.board_size and 
                   0 <= c < self.board_size and 
                   self.board[r, c] == player):
                count += 1
                r += dr
                c += dc
            
            # 检查是否被阻挡
            if (r < 0 or r >= self.board_size or 
                c < 0 or c >= self.board_size or 
                self.board[r, c] == -player):
                blocked += 1
            
            # 反向计数
            r, c = row - dr, col - dc
            while (0 <= r < self.board_size and 
                   0 <= c < self.board_size and 
                   self.board[r, c] == player):
                count += 1
                r -= dr
                c -= dc
            
            # 检查是否被阻挡
            if (r < 0 or r >= self.board_size or 
                c < 0 or c >= self.board_size or 
                self.board[r, c] == -player):
                blocked += 1
            
            # 计算分数
            if blocked < 2:  # 没有被完全阻挡
                if count == 5:
                    score += 100000
                elif count == 4:
                    score += 1000 if blocked == 0 else 100
                elif count == 3:
                    score += 100 if blocked == 0 else 10
                elif count == 2:
                    score += 10 if blocked == 0 else 1
        
        return score
```

### 2. AI引擎设计 (AI Engine Design)

```python
# src/ai/ai_engine.py
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, Tuple
import numpy as np
from dataclasses import dataclass

class DifficultyLevel(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

@dataclass
class SearchResult:
    """搜索结果"""
    best_move: Tuple[int, int]
    evaluation_score: float
    search_depth: int
    nodes_explored: int
    search_time: float

class SearchAlgorithm(ABC):
    """搜索算法基类"""
    
    @abstractmethod
    def search(self, board: np.ndarray, player: PlayerType, 
               depth: int, time_limit: float) -> SearchResult:
        """搜索最佳落子"""
        pass

class AlphaBeta(SearchAlgorithm):
    """Alpha-Beta剪枝算法"""
    
    def __init__(self, evaluator):
        self.evaluator = evaluator
        self.nodes_explored = 0
        self.transposition_table = {}
    
    def search(self, board: np.ndarray, player: PlayerType, 
               depth: int, time_limit: float) -> SearchResult:
        """执行Alpha-Beta搜索"""
        start_time = time.time()
        self.nodes_explored = 0
        
        best_move = None
        best_score = -np.inf
        alpha = -np.inf
        beta = np.inf
        
        # 获取所有可能的落子
        valid_moves = self.get_ordered_moves(board, player)
        
        for move in valid_moves:
            if time.time() - start_time > time_limit:
                break
            
            # 执行落子
            new_board = board.copy()
            new_board[move] = player.value
            
            # 递归搜索
            score = -self.alpha_beta(new_board, -player, depth - 1, 
                                     -beta, -alpha, time_limit - (time.time() - start_time))
            
            if score > best_score:
                best_score = score
                best_move = move
            
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        
        search_time = time.time() - start_time
        
        return SearchResult(
            best_move=best_move,
            evaluation_score=best_score,
            search_depth=depth,
            nodes_explored=self.nodes_explored,
            search_time=search_time
        )
    
    def alpha_beta(self, board: np.ndarray, player: PlayerType, depth: int,
                   alpha: float, beta: float, time_limit: float) -> float:
        """递归Alpha-Beta搜索"""
        self.nodes_explored += 1
        
        if time.time() - self.start_time > time_limit:
            return self.evaluator.evaluate(board, player)
        
        if depth == 0:
            return self.evaluator.evaluate(board, player)
        
        # 检查游戏结束
        winner = self.check_winner(board)
        if winner != PlayerType.EMPTY:
            if winner == player:
                return np.inf
            else:
                return -np.inf
        
        valid_moves = self.get_ordered_moves(board, player)
        
        for move in valid_moves:
            new_board = board.copy()
            new_board[move] = player.value
            
            score = -self.alpha_beta(new_board, -player, depth - 1, 
                                   -beta, -alpha, time_limit)
            
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        
        return alpha
    
    def get_ordered_moves(self, board: np.ndarray, player: PlayerType) -> list:
        """获取排序的落子位置"""
        moves = []
        
        # 获取所有空位置
        empty_positions = np.argwhere(board == PlayerType.EMPTY.value)
        
        # 评估每个位置的潜力
        for pos in empty_positions:
            row, col = pos
            score = self.evaluate_move_potential(board, row, col, player)
            moves.append(((row, col), score))
        
        # 按分数排序
        moves.sort(key=lambda x: x[1], reverse=True)
        
        return [move[0] for move in moves[:min(10, len(moves))]]
    
    def evaluate_move_potential(self, board: np.ndarray, row: int, col: int, 
                                player: PlayerType) -> float:
        """评估落子潜力"""
        # 简化的评估函数
        score = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            blocked = 0
            
            # 正向计数
            r, c = row + dr, col + dc
            while (0 <= r < board.shape[0] and 
                   0 <= c < board.shape[1] and 
                   board[r, c] == player.value):
                count += 1
                r += dr
                c += dc
            
            # 检查阻挡
            if (r < 0 or r >= board.shape[0] or 
                c < 0 or c >= board.shape[1] or 
                board[r, c] == -player.value):
                blocked += 1
            
            # 反向计数
            r, c = row - dr, col - dc
            while (0 <= r < board.shape[0] and 
                   0 <= c < board.shape[1] and 
                   board[r, c] == player.value):
                count += 1
                r -= dr
                c -= dc
            
            # 检查阻挡
            if (r < 0 or r >= board.shape[0] or 
                c < 0 or c >= board.shape[1] or 
                board[r, c] == -player.value):
                blocked += 1
            
            # 计算分数
            if blocked < 2:
                if count >= 4:
                    score += 1000
                elif count == 3:
                    score += 100
                elif count == 2:
                    score += 10
                else:
                    score += 1
        
        return score

class NeuralFiveAI:
    """NeuralFive AI引擎"""
    
    def __init__(self, difficulty: DifficultyLevel = DifficultyLevel.MEDIUM):
        self.difficulty = difficulty
        self.search_depth = self.get_search_depth(difficulty)
        self.evaluator = PositionEvaluator()
        self.search_algorithm = AlphaBeta(self.evaluator)
        self.time_limit = self.get_time_limit(difficulty)
    
    def get_search_depth(self, difficulty: DifficultyLevel) -> int:
        """获取搜索深度"""
        depth_map = {
            DifficultyLevel.EASY: 2,
            DifficultyLevel.MEDIUM: 4,
            DifficultyLevel.HARD: 6,
            DifficultyLevel.EXPERT: 8
        }
        return depth_map.get(difficulty, 4)
    
    def get_time_limit(self, difficulty: DifficultyLevel) -> float:
        """获取时间限制"""
        time_map = {
            DifficultyLevel.EASY: 1.0,
            DifficultyLevel.MEDIUM: 2.0,
            DifficultyLevel.HARD: 5.0,
            DifficultyLevel.EXPERT: 10.0
        }
        return time_map.get(difficulty, 2.0)
    
    def get_best_move(self, board: np.ndarray) -> Optional[Tuple[int, int]]:
        """获取最佳落子"""
        # 检查是否有立即获胜的机会
        winning_move = self.find_winning_move(board, PlayerType.BLACK)
        if winning_move:
            return winning_move
        
        # 检查是否需要阻挡对手获胜
        blocking_move = self.find_winning_move(board, PlayerType.WHITE)
        if blocking_move:
            return blocking_move
        
        # 执行完整搜索
        result = self.search_algorithm.search(
            board, PlayerType.BLACK, self.search_depth, self.time_limit
        )
        
        return result.best_move
    
    def find_winning_move(self, board: np.ndarray, player: PlayerType) -> Optional[Tuple[int, int]]:
        """寻找获胜落子"""
        empty_positions = np.argwhere(board == PlayerType.EMPTY.value)
        
        for pos in empty_positions:
            row, col = pos
            
            # 模拟落子
            test_board = board.copy()
            test_board[row, col] = player.value
            
            # 检查是否获胜
            if self.check_winner_at(test_board, row, col, player):
                return (row, col)
        
        return None
    
    def check_winner_at(self, board: np.ndarray, row: int, col: int, 
                        player: PlayerType) -> bool:
        """检查指定位置是否获胜"""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            
            # 正向计数
            r, c = row + dr, col + dc
            while (0 <= r < board.shape[0] and 
                   0 <= c < board.shape[1] and 
                   board[r, c] == player.value):
                count += 1
                r += dr
                c += dc
            
            # 反向计数
            r, c = row - dr, col - dc
            while (0 <= r < board.shape[0] and 
                   0 <= c < board.shape[1] and 
                   board[r, c] == player.value):
                count += 1
                r -= dr
                c -= dc
            
            if count >= 5:
                return True
        
        return False
```

## 设计模式应用

### 1. 策略模式 (Strategy Pattern)
用于不同的搜索算法和评估函数。

### 2. 工厂模式 (Factory Pattern)
用于创建不同类型的AI引擎和游戏模式。

### 3. 观察者模式 (Observer Pattern)
用于游戏状态变化和UI更新。

### 4. 单例模式 (Singleton Pattern)
用于全局配置和资源管理。

### 5. 模板方法模式 (Template Method Pattern)
用于游戏循环和AI搜索框架。

## 性能优化设计

### 1. 内存管理
- 对象池复用
- 延迟加载
- 内存映射文件

### 2. 计算优化
- Numba JIT编译
- 向量化操作
- 缓存机制

### 3. 并行处理
- 多进程搜索
- 异步I/O
- 任务队列

### 4. 数据结构优化
- 位运算表示
- 压缩存储
- 哈希表优化

## 扩展性设计

### 1. 插件系统
- 算法插件
- 评估函数插件
- UI主题插件

### 2. 配置系统
- 动态配置加载
- 环境变量支持
- 配置文件热重载

### 3. 模块化设计
- 低耦合高内聚
- 接口隔离
- 依赖注入
# NeuralFive API 文档

## 概述

NeuralFive 提供了完整的 API 接口，支持游戏控制、AI 分析、状态查询等功能。

## 核心 API

### 游戏状态 API

#### GameState 类

```python
class GameState:
    """游戏状态管理"""
    
    def __init__(self, board_size: int = 15):
        """
        初始化游戏状态
        
        Args:
            board_size: 棋盘大小，默认为15
        """
        pass
    
    def make_move(self, row: int, col: int) -> bool:
        """
        执行落子动作
        
        Args:
            row: 行坐标 (0-14)
            col: 列坐标 (0-14)
            
        Returns:
            bool: 落子是否成功
            
        Raises:
            ValueError: 坐标超出范围
            RuntimeError: 游戏已结束
        """
        pass
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """
        检查落子是否有效
        
        Args:
            row: 行坐标
            col: 列坐标
            
        Returns:
            bool: 是否有效
        """
        pass
    
    def check_winner(self) -> Optional[PlayerType]:
        """
        检查获胜者
        
        Returns:
            Optional[PlayerType]: 获胜玩家，如果没有则为None
        """
        pass
    
    def get_board_state(self) -> np.ndarray:
        """
        获取棋盘状态
        
        Returns:
            np.ndarray: 15x15 棋盘数组
            1: 黑棋
            -1: 白棋
            0: 空位
        """
        pass
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """
        获取所有有效落子位置
        
        Returns:
            List[Tuple[int, int]]: 有效位置列表
        """
        pass
    
    def reset(self) -> None:
        """
        重置游戏状态
        """
        pass
    
    def to_dict(self) -> dict:
        """
        转换为字典格式
        
        Returns:
            dict: 游戏状态字典
        """
        pass
    
    def from_dict(self, data: dict) -> None:
        """
        从字典恢复状态
        
        Args:
            data: 游戏状态字典
        """
        pass
```

### AI 引擎 API

#### NeuralFiveAI 类

```python
class NeuralFiveAI:
    """NeuralFive AI引擎"""
    
    def __init__(self, difficulty: DifficultyLevel = DifficultyLevel.MEDIUM):
        """
        初始化AI引擎
        
        Args:
            difficulty: 难度等级
                - EASY: 简单
                - MEDIUM: 中等
                - HARD: 困难
                - EXPERT: 专家
        """
        pass
    
    def get_best_move(self, board: np.ndarray) -> Optional[Move]:
        """
        获取最佳落子
        
        Args:
            board: 棋盘状态
            
        Returns:
            Optional[Move]: 最佳落子，如果没有则为None
        """
        pass
    
    def evaluate_position(self, board: np.ndarray) -> float:
        """
        评估棋盘位置
        
        Args:
            board: 棋盘状态
            
        Returns:
            float: 评估分数
        """
        pass
    
    def set_difficulty(self, difficulty: DifficultyLevel) -> None:
        """
        设置难度等级
        
        Args:
            difficulty: 难度等级
        """
        pass
    
    def get_analysis_info(self) -> dict:
        """
        获取分析信息
        
        Returns:
            dict: 分析信息
                - nodes_explored: 探索节点数
                - search_depth: 搜索深度
                - evaluation_score: 评估分数
                - search_time: 搜索时间
        """
        pass
```

#### Move 类

```python
@dataclass
class Move:
    """落子动作"""
    row: int
    col: int
    evaluation_score: Optional[float] = None
    confidence: Optional[float] = None
    
    def __post_init__(self):
        """验证坐标有效性"""
        if not (0 <= self.row < 15 and 0 <= self.col < 15):
            raise ValueError("坐标超出范围")
```

### 搜索算法 API

#### SearchAlgorithm 基类

```python
class SearchAlgorithm(ABC):
    """搜索算法基类"""
    
    @abstractmethod
    def search(self, board: np.ndarray, player: PlayerType, 
               depth: int, time_limit: float) -> SearchResult:
        """
        搜索最佳落子
        
        Args:
            board: 棋盘状态
            player: 当前玩家
            depth: 搜索深度
            time_limit: 时间限制
            
        Returns:
            SearchResult: 搜索结果
        """
        pass
    
    def get_name(self) -> str:
        """获取算法名称"""
        pass
```

#### AlphaBeta 类

```python
class AlphaBeta(SearchAlgorithm):
    """Alpha-Beta剪枝算法"""
    
    def __init__(self, evaluator: PositionEvaluator, 
                 use_transposition_table: bool = True,
                 use_move_ordering: bool = True):
        """
        初始化Alpha-Beta算法
        
        Args:
            evaluator: 位置评估器
            use_transposition_table: 是否使用置换表
            use_move_ordering: 是否使用落子排序
        """
        pass
    
    def set_evaluation_weights(self, weights: dict) -> None:
        """
        设置评估权重
        
        Args:
            weights: 权重字典
        """
        pass
```

#### MonteCarlo 类

```python
class MonteCarlo(SearchAlgorithm):
    """蒙特卡洛树搜索算法"""
    
    def __init__(self, simulations: int = 1000, 
                 exploration_constant: float = 1.414):
        """
        初始化蒙特卡洛算法
        
        Args:
            simulations: 模拟次数
            exploration_constant: 探索常数
        """
        pass
    
    def set_simulation_policy(self, policy: str) -> None:
        """
        设置模拟策略
        
        Args:
            policy: 策略名称
                - random: 随机策略
                - greedy: 贪心策略
                - ucb: UCB策略
        """
        pass
```

### 评估函数 API

#### PositionEvaluator 类

```python
class PositionEvaluator:
    """位置评估器"""
    
    def __init__(self, pattern_weights: Optional[dict] = None):
        """
        初始化评估器
        
        Args:
            pattern_weights: 模式权重字典
        """
        pass
    
    def evaluate(self, board: np.ndarray, player: PlayerType) -> float:
        """
        评估棋盘位置
        
        Args:
            board: 棋盘状态
            player: 评估玩家
            
        Returns:
            float: 评估分数
        """
        pass
    
    def evaluate_position_at(self, board: np.ndarray, row: int, col: int, 
                           player: PlayerType) -> float:
        """
        评估指定位置
        
        Args:
            board: 棋盘状态
            row: 行坐标
            col: 列坐标
            player: 玩家
            
        Returns:
            float: 位置分数
        """
        pass
    
    def set_pattern_weights(self, weights: dict) -> None:
        """
        设置模式权重
        
        Args:
            weights: 权重字典
        """
        pass
    
    def get_pattern_weights(self) -> dict:
        """
        获取当前模式权重
        
        Returns:
            dict: 权重字典
        """
        pass
```

### 配置 API

#### Config 类

```python
class Config:
    """配置管理"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        初始化配置
        
        Args:
            config_file: 配置文件路径
        """
        pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            Any: 配置值
        """
        pass
    
    def set(self, key: str, value: Any) -> None:
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
        """
        pass
    
    def save(self, file_path: str) -> None:
        """
        保存配置到文件
        
        Args:
            file_path: 文件路径
        """
        pass
    
    def load(self, file_path: str) -> None:
        """
        从文件加载配置
        
        Args:
            file_path: 文件路径
        """
        pass
```

## 使用示例

### 基本游戏控制

```python
from neuralfive import GameState, NeuralFiveAI, DifficultyLevel

# 创建游戏状态
game = GameState(board_size=15)

# 创建AI引擎
ai = NeuralFiveAI(difficulty=DifficultyLevel.MEDIUM)

# 执行落子
game.make_move(7, 7)  # 玩家在(7,7)落子

# AI思考
ai_move = ai.get_best_move(game.get_board_state())
if ai_move:
    game.make_move(ai_move.row, ai_move.col)

# 检查获胜者
winner = game.check_winner()
if winner:
    print(f"获胜者: {winner}")
```

### 高级AI分析

```python
from neuralfive import AlphaBeta, PositionEvaluator

# 创建评估器
evaluator = PositionEvaluator()

# 创建搜索算法
search_algo = AlphaBeta(evaluator, use_transposition_table=True)

# 执行搜索
result = search_algo.search(
    board=game.get_board_state(),
    player=PlayerType.BLACK,
    depth=6,
    time_limit=5.0
)

print(f"最佳落子: {result.best_move}")
print(f"评估分数: {result.evaluation_score}")
print(f"探索节点: {result.nodes_explored}")
print(f"搜索时间: {result.search_time}")
```

### 批量分析

```python
import numpy as np
from neuralfive import NeuralFiveAI

# 创建多个棋盘位置进行分析
test_positions = [
    np.array([...]),  # 位置1
    np.array([...]),  # 位置2
    np.array([...]),  # 位置3
]

ai = NeuralFiveAI(difficulty=DifficultyLevel.HARD)
results = []

for position in test_positions:
    move = ai.get_best_move(position)
    score = ai.evaluate_position(position)
    results.append({
        'move': move,
        'score': score,
        'analysis': ai.get_analysis_info()
    })

# 分析结果
for i, result in enumerate(results):
    print(f"位置 {i+1}:")
    print(f"  最佳落子: {result['move']}")
    print(f"  评估分数: {result['score']}")
    print(f"  分析信息: {result['analysis']}")
```

## 错误处理

### 异常类型

```python
class NeuralFiveError(Exception):
    """NeuralFive基础异常"""
    pass

class InvalidMoveError(NeuralFiveError):
    """无效落子异常"""
    pass

class GameOverError(NeuralFiveError):
    """游戏结束异常"""
    pass

class AIEngineError(NeuralFiveError):
    """AI引擎异常"""
    pass

class ConfigurationError(NeuralFiveError):
    """配置异常"""
    pass
```

### 错误处理示例

```python
from neuralfive import GameState, InvalidMoveError, GameOverError

game = GameState()

try:
    # 尝试无效落子
    game.make_move(-1, -1)
except InvalidMoveError as e:
    print(f"无效落子: {e}")

try:
    # 游戏结束后尝试落子
    # ... 游戏逻辑 ...
    game.make_move(7, 7)
except GameOverError as e:
    print(f"游戏已结束: {e}")
```

## 性能优化

### 内存优化

```python
# 使用内存池减少分配
from neuralfive import GameState, create_game_pool

# 创建游戏池
game_pool = create_game_pool(size=10)

# 从池中获取游戏实例
game = game_pool.get()

# 使用完毕后归还
game.reset()
game_pool.put(game)
```

### 并行处理

```python
from concurrent.futures import ThreadPoolExecutor
from neuralfive import NeuralFiveAI

# 创建AI实例池
ai_instances = [NeuralFiveAI() for _ in range(4)]

def analyze_position(args):
    ai, board = args
    return ai.get_best_move(board)

# 并行分析多个位置
with ThreadPoolExecutor(max_workers=4) as executor:
    positions = [board1, board2, board3, board4]
    tasks = [(ai, pos) for ai, pos in zip(ai_instances, positions)]
    results = list(executor.map(analyze_position, tasks))
```

## 扩展接口

### 自定义搜索算法

```python
from neuralfive import SearchAlgorithm, SearchResult

class MyCustomSearch(SearchAlgorithm):
    def search(self, board, player, depth, time_limit):
        # 实现自定义搜索逻辑
        best_move = self.my_search_logic(board, player, depth)
        
        return SearchResult(
            best_move=best_move,
            evaluation_score=self.evaluate(board, player),
            search_depth=depth,
            nodes_explored=self.nodes_count,
            search_time=time_spent
        )

# 使用自定义算法
ai = NeuralFiveAI()
ai.set_search_algorithm(MyCustomSearch())
```

### 自定义评估函数

```python
from neuralfive import PositionEvaluator

class MyEvaluator(PositionEvaluator):
    def evaluate_position_at(self, board, row, col, player):
        # 实现自定义评估逻辑
        score = 0
        
        # 自定义评估算法
        score += self.evaluate_patterns(board, row, col, player)
        score += self.evaluate_position_control(board, row, col, player)
        score += self.evaluate_mobility(board, row, col, player)
        
        return score

# 使用自定义评估器
ai = NeuralFiveAI()
ai.set_evaluator(MyEvaluator())
```
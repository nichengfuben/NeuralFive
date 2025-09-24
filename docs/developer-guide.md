# NeuralFive 开发者文档

## 架构设计

### 核心组件

#### AI引擎 (`ai_engine.py`)
```python
class NeuralFiveAI:
    """五子棋AI引擎核心类"""
    
    def __init__(self, difficulty: str = "medium"):
        self.difficulty = difficulty
        self.evaluator = PositionEvaluator()
        self.search_depth = self._get_search_depth(difficulty)
    
    def get_best_move(self, board: np.ndarray) -> Move:
        """获取最佳落子位置"""
        # 实现Minimax搜索 + Alpha-Beta剪枝
        pass
    
    def evaluate_position(self, board: np.ndarray) -> float:
        """评估棋盘位置价值"""
        # 基于启发式规则的评估函数
        pass
```

#### 游戏状态管理 (`game_state.py`)
```python
class GameState:
    """游戏状态管理器"""
    
    def __init__(self, board_size: int = 15):
        self.board = np.zeros((board_size, board_size))
        self.current_player = PlayerType.BLACK
        self.move_history = []
        self.game_status = GameStatus.ONGOING
    
    def make_move(self, row: int, col: int) -> bool:
        """执行落子操作"""
        # 验证落子合法性
        # 更新棋盘状态
        # 检查游戏结束条件
        pass
    
    def check_winner(self) -> Optional[PlayerType]:
        """检查获胜方"""
        # 检查水平、垂直、对角线方向
        pass
```

#### 图形界面 (`gui.py`)
```python
class NeuralFiveGUI:
    """五子棋游戏图形界面"""
    
    def __init__(self):
        self.game = GameState()
        self.ai = NeuralFiveAI()
        self.theme = Theme.DARK
    
    def handle_click(self, pos: Tuple[int, int]):
        """处理鼠标点击事件"""
        # 坐标转换
        # 落子逻辑
        # 界面更新
        pass
    
    def draw_board(self):
        """绘制棋盘"""
        # 绘制网格
        # 绘制棋子
        # 绘制UI元素
        pass
```

### 数据流设计

```
用户输入 → GUI事件处理 → 游戏逻辑 → AI计算 → 结果展示
     ↓           ↓           ↓         ↓        ↓
鼠标点击 → 坐标转换 → 落子验证 → 搜索算法 → 界面更新
键盘输入 → 快捷键处理 → 状态更新 → 评估函数 → 状态显示
```

## 算法实现

### 搜索算法

#### Minimax + Alpha-Beta剪枝
```python
def minimax(board: np.ndarray, depth: int, alpha: float, beta: float, 
           maximizing: bool) -> Tuple[float, Move]:
    """Minimax搜索算法"""
    
    if depth == 0 or is_terminal_node(board):
        return evaluate_position(board), None
    
    best_move = None
    if maximizing:
        max_eval = -np.inf
        for move in get_legal_moves(board):
            make_move(board, move)
            eval, _ = minimax(board, depth-1, alpha, beta, False)
            undo_move(board, move)
            
            if eval > max_eval:
                max_eval = eval
                best_move = move
            
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta剪枝
        
        return max_eval, best_move
    else:
        min_eval = np.inf
        for move in get_legal_moves(board):
            make_move(board, move)
            eval, _ = minimax(board, depth-1, alpha, beta, True)
            undo_move(board, move)
            
            if eval < min_eval:
                min_eval = eval
                best_move = move
            
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha剪枝
        
        return min_eval, best_move
```

#### 迭代深化
```python
def iterative_deepening(board: np.ndarray, max_time: float) -> Move:
    """迭代深化搜索"""
    
    best_move = None
    start_time = time.time()
    
    for depth in range(1, MAX_DEPTH):
        if time.time() - start_time > max_time:
            break
        
        eval, move = minimax(board, depth, -np.inf, np.inf, True)
        if move:
            best_move = move
    
    return best_move
```

### 评估函数

#### 模式识别
```python
class PositionEvaluator:
    """位置评估器"""
    
    def __init__(self):
        self.patterns = self._init_patterns()
        self.weights = self._init_weights()
    
    def evaluate(self, board: np.ndarray, player: PlayerType) -> float:
        """评估棋盘位置"""
        score = 0
        
        # 评估不同方向
        for direction in [HORIZONTAL, VERTICAL, DIAGONAL1, DIAGONAL2]:
            score += self._evaluate_direction(board, player, direction)
        
        # 位置价值
        score += self._evaluate_position_value(board, player)
        
        # 机动性
        score += self._evaluate_mobility(board, player)
        
        return score
    
    def _evaluate_direction(self, board: np.ndarray, player: PlayerType, 
                           direction: Direction) -> float:
        """评估特定方向"""
        score = 0
        
        for pattern, weight in self.patterns.items():
            count = self._count_pattern(board, pattern, direction)
            score += count * weight
        
        return score
```

#### 特征提取
```python
def extract_features(board: np.ndarray, player: PlayerType) -> np.ndarray:
    """提取棋盘特征"""
    
    features = []
    
    # 连子特征
    for length in range(1, 6):
        for direction in DIRECTIONS:
            count = count_continuous_stones(board, player, length, direction)
            features.append(count)
    
    # 空间特征
    features.append(calculate_center_control(board, player))
    features.append(calculate_mobility(board, player))
    features.append(calculate_threats(board, player))
    
    # 形状特征
    features.extend(extract_shape_features(board, player))
    
    return np.array(features)
```

## 性能优化

### Numba加速
```python
from numba import jit, int32, float32

@jit(int32(int32[:,:], int32, int32), nopython=True, cache=True)
def count_pattern_numba(board: np.ndarray, pattern: int, player: int) -> int:
    """Numba加速的模式计数"""
    count = 0
    rows, cols = board.shape
    
    for i in range(rows):
        for j in range(cols):
            if check_pattern_at(board, i, j, pattern, player):
                count += 1
    
    return count
```

### 并行计算
```python
from multiprocessing import Pool
from functools import partial

def evaluate_positions_parallel(positions: List[np.ndarray], 
                             evaluator: PositionEvaluator) -> List[float]:
    """并行评估多个位置"""
    
    with Pool() as pool:
        scores = pool.map(evaluator.evaluate, positions)
    
    return scores
```

### 内存优化
```python
class MemoryEfficientAI:
    """内存优化的AI实现"""
    
    def __init__(self, max_memory_mb: int = 512):
        self.max_memory = max_memory_mb * 1024 * 1024
        self.transposition_table = LRUCache(maxsize=100000)
    
    def get_best_move(self, board: np.ndarray) -> Move:
        """内存感知的最优落子"""
        # 实现内存限制的搜索
        pass
```

## 扩展接口

### 自定义评估函数
```python
class CustomEvaluator(PositionEvaluator):
    """自定义评估器"""
    
    def __init__(self, weights: Dict[str, float]):
        super().__init__()
        self.custom_weights = weights
    
    def evaluate(self, board: np.ndarray, player: PlayerType) -> float:
        """自定义评估逻辑"""
        base_score = super().evaluate(board, player)
        custom_score = self._custom_evaluation(board, player)
        
        return base_score + custom_score
```

### 插件系统
```python
class PluginManager:
    """插件管理器"""
    
    def __init__(self):
        self.plugins = {}
    
    def register_plugin(self, name: str, plugin: Any):
        """注册插件"""
        self.plugins[name] = plugin
    
    def get_plugin(self, name: str) -> Optional[Any]:
        """获取插件"""
        return self.plugins.get(name)
```

## 测试策略

### 单元测试
```python
class TestAIEngine:
    """AI引擎测试"""
    
    def test_minimax_basic(self):
        """测试基本Minimax算法"""
        board = create_test_board()
        ai = NeuralFiveAI()
        
        score, move = ai.minimax(board, 3, -np.inf, np.inf, True)
        
        assert move is not None
        assert score != 0
    
    def test_evaluation_symmetry(self):
        """测试评估函数对称性"""
        board1 = create_symmetric_board()
        board2 = create_rotated_board(board1)
        
        eval1 = ai.evaluate_position(board1)
        eval2 = ai.evaluate_position(board2)
        
        assert abs(eval1 - eval2) < EPSILON
```

### 集成测试
```python
class TestGameIntegration:
    """游戏集成测试"""
    
    def test_full_game_simulation(self):
        """完整游戏模拟测试"""
        game = GameState()
        ai = NeuralFiveAI()
        
        while game.game_status == GameStatus.ONGOING:
            if game.current_player == PlayerType.BLACK:
                # AI落子
                move = ai.get_best_move(game.board)
                game.make_move(move.row, move.col)
            else:
                # 随机落子（模拟对手）
                move = get_random_move(game)
                game.make_move(move.row, move.col)
        
        assert game.game_status != GameStatus.ONGOING
```

### 性能测试
```python
class TestPerformance:
    """性能测试"""
    
    @pytest.mark.benchmark
    def test_ai_speed(self, benchmark):
        """测试AI计算速度"""
        ai = NeuralFiveAI()
        board = create_complex_board()
        
        result = benchmark(ai.get_best_move, board)
        
        assert benchmark.stats['mean'] < 1.0  # 平均时间小于1秒
```

## 部署指南

### 打包配置
```python
# setup.py
from setuptools import setup, find_packages

setup(
    name="neuralfive",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.24.0",
        "pygame>=2.5.0",
        "numba>=0.57.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
        ],
        "ml": [
            "tensorflow>=2.12.0",
            "scikit-learn>=1.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "neuralfive=neuralfive.__main__:main",
        ],
    },
)
```

### Docker配置
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
RUN pip install -e .

CMD ["python", "-m", "neuralfive", "--gui"]
```

### CI/CD配置
```yaml
# .github/workflows/ci.yml
name: CI/CD

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
    
    - name: Run tests
      run: |
        pytest --cov=neuralfive --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```
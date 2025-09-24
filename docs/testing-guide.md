# NeuralFive 测试指南

## 测试策略

### 测试金字塔
```
         /\
        /  \
       / UI \
      /------\
     / 集成  \
    /--------\
   /  单元   \
  /----------\
 /   基准    \
/============\
```

## 单元测试

### 测试结构
```python
# tests/unit/test_game_state.py
import pytest
import numpy as np
from src.game.game_state import GameState, PlayerType, GameStatus

class TestGameState:
    """游戏状态单元测试"""
    
    def setup_method(self):
        """测试前置设置"""
        self.game = GameState(board_size=15)
    
    def test_initialization(self):
        """测试初始化"""
        assert self.game.board_size == 15
        assert self.game.current_player == PlayerType.BLACK
        assert self.game.game_status == GameStatus.ONGOING
        assert len(self.game.move_history) == 0
    
    def test_make_move_valid(self):
        """测试有效落子"""
        result = self.game.make_move(7, 7)
        
        assert result is True
        assert self.game.board[7, 7] == PlayerType.BLACK
        assert self.game.current_player == PlayerType.WHITE
        assert len(self.game.move_history) == 1
    
    def test_make_move_invalid_position(self):
        """测试无效位置落子"""
        # 超出边界
        result = self.game.make_move(15, 15)
        assert result is False
        
        # 负数坐标
        result = self.game.make_move(-1, -1)
        assert result is False
    
    def test_make_move_occupied_position(self):
        """测试已占用位置落子"""
        self.game.make_move(7, 7)  # 先落子
        result = self.game.make_move(7, 7)  # 再次落子
        
        assert result is False
        assert self.game.board[7, 7] == PlayerType.BLACK
    
    def test_check_winner_horizontal(self):
        """测试水平获胜"""
        # 创建水平五连
        for col in range(5):
            self.game.make_move(7, col)
            if col < 4:
                self.game.make_move(6, col)  # 对手落子
        
        winner = self.game.check_winner()
        assert winner == PlayerType.BLACK
        assert self.game.game_status == GameStatus.BLACK_WINS
    
    def test_check_winner_vertical(self):
        """测试垂直获胜"""
        # 创建垂直五连
        for row in range(5):
            self.game.make_move(row, 7)
            if row < 4:
                self.game.make_move(row, 6)  # 对手落子
        
        winner = self.game.check_winner()
        assert winner == PlayerType.BLACK
        assert self.game.game_status == GameStatus.BLACK_WINS
    
    def test_check_winner_diagonal(self):
        """测试对角线获胜"""
        # 创建对角线五连
        for i in range(5):
            self.game.make_move(i, i)
            if i < 4:
                self.game.make_move(i, i+1)  # 对手落子
        
        winner = self.game.check_winner()
        assert winner == PlayerType.BLACK
        assert self.game.game_status == GameStatus.BLACK_WINS
    
    def test_check_draw(self):
        """测试平局"""
        # 填充棋盘但不产生获胜
        moves = []
        for row in range(15):
            for col in range(15):
                if (row + col) % 2 == 0:
                    moves.append((row, col))
        
        for row, col in moves[:224]:  # 除了最后一个位置
            self.game.make_move(row, col)
        
        # 检查游戏状态
        assert self.game.game_status == GameStatus.ONGOING
        
        # 最后一个落子
        last_move = moves[224]
        self.game.make_move(*last_move)
        
        # 应该平局
        assert self.game.game_status == GameStatus.DRAW
```

### AI引擎测试
```python
# tests/unit/test_ai_engine.py
import pytest
import numpy as np
from src.ai.ai_engine import NeuralFiveAI, DifficultyLevel
from src.game.game_state import GameState, PlayerType

class TestNeuralFiveAI:
    """AI引擎单元测试"""
    
    def setup_method(self):
        """测试前置设置"""
        self.ai = NeuralFiveAI(difficulty=DifficultyLevel.MEDIUM)
    
    def test_initialization(self):
        """测试初始化"""
        assert self.ai.difficulty == DifficultyLevel.MEDIUM
        assert self.ai.search_depth == 4
        assert self.ai.evaluator is not None
    
    def test_get_best_move_basic(self):
        """测试基本最佳落子"""
        game = GameState()
        
        # 在中心附近落子
        move = self.ai.get_best_move(game.board)
        
        assert move is not None
        assert 5 <= move.row <= 9
        assert 5 <= move.col <= 9
    
    def test_get_best_move_winning_position(self):
        """测试获胜位置"""
        game = GameState()
        
        # 创建四连局面
        for i in range(4):
            game.make_move(7, i)
            if i < 3:
                game.make_move(6, i)
        
        # AI应该识别获胜机会
        move = self.ai.get_best_move(game.board)
        
        assert move is not None
        # 应该落在(7, 4)完成五连
        assert move.row == 7
        assert move.col == 4
    
    def test_get_best_move_blocking_position(self):
        """测试阻挡位置"""
        game = GameState()
        
        # 创建对手四连局面
        for i in range(4):
            game.make_move(7, i)  # AI落子
            game.make_move(8, i)  # 对手四连
        
        # AI应该识别需要阻挡
        move = self.ai.get_best_move(game.board)
        
        assert move is not None
        # 应该阻挡在(8, 4)
        assert move.row == 8
        assert move.col == 4
    
    def test_evaluate_position_symmetry(self):
        """测试评估函数对称性"""
        # 创建对称棋盘
        board1 = np.zeros((15, 15))
        board1[7, 7] = PlayerType.BLACK
        board1[7, 8] = PlayerType.WHITE
        
        board2 = np.zeros((15, 15))
        board2[7, 7] = PlayerType.BLACK
        board2[8, 7] = PlayerType.WHITE  # 旋转90度
        
        eval1 = self.ai.evaluate_position(board1)
        eval2 = self.ai.evaluate_position(board2)
        
        # 评估值应该相近
        assert abs(eval1 - eval2) < 0.1
    
    def test_difficulty_levels(self):
        """测试不同难度等级"""
        difficulties = [
            (DifficultyLevel.EASY, 2),
            (DifficultyLevel.MEDIUM, 4),
            (DifficultyLevel.HARD, 6),
            (DifficultyLevel.EXPERT, 8)
        ]
        
        for difficulty, expected_depth in difficulties:
            ai = NeuralFiveAI(difficulty=difficulty)
            assert ai.search_depth == expected_depth
```

## 集成测试

### 游戏流程测试
```python
# tests/integration/test_game_flow.py
import pytest
from src.game.game_state import GameState
from src.ai.ai_engine import NeuralFiveAI
from src.gui.gui import NeuralFiveGUI

class TestGameFlow:
    """游戏流程集成测试"""
    
    def test_ai_vs_ai_game(self):
        """测试AI对AI完整游戏"""
        
        game = GameState()
        ai1 = NeuralFiveAI(difficulty="easy")
        ai2 = NeuralFiveAI(difficulty="easy")
        
        move_count = 0
        max_moves = 225  # 最大可能步数
        
        while game.game_status == GameStatus.ONGOING and move_count < max_moves:
            if game.current_player == PlayerType.BLACK:
                move = ai1.get_best_move(game.board)
            else:
                move = ai2.get_best_move(game.board)
            
            if move:
                game.make_move(move.row, move.col)
                move_count += 1
            else:
                break
        
        # 游戏应该正常结束
        assert game.game_status != GameStatus.ONGOING
        assert move_count > 0
        assert move_count <= max_moves
    
    def test_gui_integration(self):
        """测试GUI集成"""
        
        # 创建GUI（不显示）
        gui = NeuralFiveGUI(headless=True)
        
        # 测试基本功能
        assert gui.game is not None
        assert gui.ai is not None
        
        # 模拟点击
        click_pos = (400, 400)  # 棋盘中心
        gui.handle_click(click_pos)
        
        # 检查游戏状态
        assert len(gui.game.move_history) >= 1
    
    def test_save_load_game(self):
        """测试游戏保存和加载"""
        
        # 创建游戏并进行几步
        game1 = GameState()
        moves = [(7, 7), (7, 8), (8, 7), (8, 8)]
        
        for row, col in moves:
            game1.make_move(row, col)
        
        # 保存游戏
        save_data = game1.to_dict()
        
        # 加载游戏
        game2 = GameState()
        game2.from_dict(save_data)
        
        # 验证状态一致
        assert np.array_equal(game1.board, game2.board)
        assert game1.current_player == game2.current_player
        assert game1.game_status == game2.game_status
        assert game1.move_history == game2.move_history
```

### 性能测试
```python
# tests/integration/test_performance.py
import time
import pytest
import numpy as np
from src.ai.ai_engine import NeuralFiveAI
from src.game.game_state import GameState

class TestPerformance:
    """性能集成测试"""
    
    @pytest.mark.performance
    def test_ai_response_time(self):
        """测试AI响应时间"""
        
        ai = NeuralFiveAI(difficulty="medium")
        game = GameState()
        
        # 进行10步棋
        for i in range(10):
            start_time = time.time()
            move = ai.get_best_move(game.board)
            response_time = time.time() - start_time
            
            assert response_time < 2.0  # 响应时间小于2秒
            
            if move:
                game.make_move(move.row, move.col)
    
    @pytest.mark.performance
    def test_memory_usage(self):
        """测试内存使用"""
        
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # 创建多个AI实例
        ais = []
        for i in range(10):
            ai = NeuralFiveAI(difficulty="hard")
            ais.append(ai)
        
        # 运行一些计算
        game = GameState()
        for ai in ais:
            ai.get_best_move(game.board)
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # 内存增长应该合理
        assert memory_increase < 100 * 1024 * 1024  # 小于100MB
    
    @pytest.mark.performance
    def test_scalability(self):
        """测试可扩展性"""
        
        difficulties = ["easy", "medium", "hard"]
        response_times = []
        
        for difficulty in difficulties:
            ai = NeuralFiveAI(difficulty=difficulty)
            game = GameState()
            
            start_time = time.time()
            ai.get_best_move(game.board)
            response_time = time.time() - start_time
            
            response_times.append(response_time)
        
        # 响应时间应该随难度增加而增加
        assert response_times[0] < response_times[1] < response_times[2]
```

## 端到端测试

### 完整游戏测试
```python
# tests/e2e/test_complete_game.py
import pytest
import subprocess
import time
import os

class TestCompleteGame:
    """完整游戏端到端测试"""
    
    def test_command_line_game(self):
        """测试命令行游戏"""
        
        # 启动游戏进程
        cmd = ["python", "-m", "neuralfive", "--cli", "--ai-easy"]
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            # 等待游戏启动
            time.sleep(2)
            
            # 发送一些命令
            commands = ["7 7\n", "7 8\n", "8 7\n", "8 8\n", "quit\n"]
            
            for cmd in commands:
                process.stdin.write(cmd)
                process.stdin.flush()
                time.sleep(0.5)
            
            # 获取输出
            output, error = process.communicate(timeout=10)
            
            # 验证输出包含预期内容
            assert "NeuralFive" in output
            assert "Gomoku" in output
            
        finally:
            if process.poll() is None:
                process.terminate()
                process.wait()
    
    def test_gui_launch(self):
        """测试GUI启动"""
        
        # 启动GUI（无头模式）
        cmd = ["python", "-m", "neuralfive", "--gui", "--headless"]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            # 等待GUI启动
            time.sleep(3)
            
            # 检查进程是否还在运行
            assert process.poll() is None
            
            # 终止进程
            process.terminate()
            process.wait(timeout=5)
            
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()
```

## 基准测试

### 算法基准
```python
# tests/benchmark/test_algorithms.py
import pytest
import time
import numpy as np
from src.ai.algorithms import Minimax, AlphaBeta, MonteCarlo

class TestAlgorithmBenchmark:
    """算法基准测试"""
    
    @pytest.mark.benchmark
    def test_minimax_performance(self, benchmark):
        """测试Minimax算法性能"""
        
        minimax = Minimax(depth=3)
        board = self.create_test_board()
        
        result = benchmark(minimax.search, board)
        
        assert result is not None
        assert benchmark.stats['mean'] < 1.0  # 平均时间小于1秒
    
    @pytest.mark.benchmark
    def test_alphabeta_performance(self, benchmark):
        """测试AlphaBeta算法性能"""
        
        alphabeta = AlphaBeta(depth=5)
        board = self.create_test_board()
        
        result = benchmark(alphabeta.search, board)
        
        assert result is not None
        assert benchmark.stats['mean'] < 0.5  # 应该比Minimax快
    
    @pytest.mark.benchmark
    def test_monte_carlo_performance(self, benchmark):
        """测试蒙特卡洛算法性能"""
        
        mc = MonteCarlo(simulations=1000)
        board = self.create_test_board()
        
        result = benchmark(mc.search, board)
        
        assert result is not None
        assert benchmark.stats['mean'] < 2.0
    
    def create_test_board(self):
        """创建测试棋盘"""
        board = np.zeros((15, 15))
        # 添加一些棋子
        board[7, 7] = 1
        board[7, 8] = -1
        board[8, 7] = 1
        return board
```

## 测试工具

### 测试辅助函数
```python
# tests/utils/test_helpers.py
import numpy as np
from src.game.game_state import GameState, PlayerType

def create_winning_position(player=PlayerType.BLACK):
    """创建获胜位置"""
    game = GameState()
    
    # 创建四连
    for i in range(4):
        game.make_move(7, i)
        if i < 3:
            game.make_move(6, i)  # 对手落子
    
    return game

def create_blocking_position():
    """创建需要阻挡的位置"""
    game = GameState()
    
    # 创建对手四连
    for i in range(4):
        game.make_move(7, i)  # AI落子
        game.make_move(8, i)  # 对手四连
    
    return game

def create_symmetric_board():
    """创建对称棋盘"""
    board = np.zeros((15, 15))
    
    # 对称放置棋子
    for i in range(5):
        board[7+i, 7] = PlayerType.BLACK
        board[7-i, 7] = PlayerType.BLACK
        board[7, 7+i] = PlayerType.WHITE
        board[7, 7-i] = PlayerType.WHITE
    
    return board

def assert_valid_move(move, board):
    """断言有效移动"""
    assert move is not None
    assert 0 <= move.row < board.shape[0]
    assert 0 <= move.col < board.shape[1]
    assert board[move.row, move.col] == 0
```

### 测试配置
```python
# tests/conftest.py
import pytest
import tempfile
import os

@pytest.fixture
def temp_save_file():
    """临时保存文件"""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture
def mock_game_state():
    """模拟游戏状态"""
    from src.game.game_state import GameState
    return GameState()

@pytest.fixture(scope="session")
def benchmark_config():
    """基准测试配置"""
    return {
        'min_iterations': 10,
        'max_time': 10.0,
        'warmup_iterations': 3
    }
```

## 测试运行

### 运行所有测试
```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 运行端到端测试
pytest tests/e2e/

# 运行性能测试
pytest tests/benchmark/ -m benchmark

# 生成覆盖率报告
pytest --cov=src --cov-report=html

# 并行运行测试
pytest -n auto

# 详细输出
pytest -v

# 只运行失败的测试
pytest --lf
```

### 持续集成
```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
    
    - name: Run linting
      run: |
        flake8 src/ tests/
        mypy src/
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml --cov-report=term
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```
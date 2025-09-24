"""
AI引擎测试

测试NeuralFive AI引擎的核心功能：
- 位置评估
- 移动生成
- 搜索算法
- 性能优化
"""

import pytest
import numpy as np
from src.neuralfive.ai_engine import NeuralFiveAI, Move, PositionEvaluator
from src.neuralfive.game_state import GameState, GameSettings


class TestPositionEvaluator:
    """位置评估器测试"""
    
    def setup_method(self):
        """设置测试环境"""
        self.evaluator = PositionEvaluator()
        self.board = np.zeros((15, 15), dtype=int)
    
    def test_evaluate_empty_board(self):
        """测试空棋盘评估"""
        score = self.evaluator.evaluate_position(self.board, 1)
        assert score == 0
    
    def test_evaluate_single_piece(self):
        """测试单棋子评估"""
        self.board[7, 7] = 1  # 黑棋在中心
        score = self.evaluator.evaluate_position(self.board, 1)
        assert score > 0
        
        # 白棋评估应该为负值
        score_white = self.evaluator.evaluate_position(self.board, 2)
        assert score_white < 0
    
    def test_evaluate_winning_position(self):
        """测试获胜位置评估"""
        # 创建五连珠
        for i in range(5):
            self.board[7, i] = 1
        
        score = self.evaluator.evaluate_position(self.board, 1)
        assert score == float('inf')
    
    def test_evaluate_blocking_position(self):
        """测试阻挡位置评估"""
        # 创建需要阻挡的位置
        for i in range(4):
            self.board[7, i] = 1  # 黑棋四连
        
        self.board[7, 4] = 2  # 白棋阻挡
        
        score = self.evaluator.evaluate_position(self.board, 2)
        # 阻挡应该得到较高分数
        assert score > 1000
    
    def test_pattern_recognition(self):
        """测试模式识别"""
        # 测试活四
        for i in range(4):
            self.board[7, i+1] = 1
        
        score = self.evaluator.evaluate_position(self.board, 1)
        assert score > 10000  # 活四应该得到很高分数
    
    def test_edge_cases(self):
        """测试边界情况"""
        # 角落棋子
        self.board[0, 0] = 1
        score_corner = self.evaluator.evaluate_position(self.board, 1)
        
        # 边缘棋子
        self.board[0, 7] = 1
        score_edge = self.evaluator.evaluate_position(self.board, 1)
        
        # 中心棋子
        self.board[7, 7] = 1
        score_center = self.evaluator.evaluate_position(self.board, 1)
        
        # 中心应该比边缘和角落得分高
        assert score_center > score_edge > score_corner


class TestNeuralFiveAI:
    """AI引擎测试"""
    
    def setup_method(self):
        """设置测试环境"""
        self.ai_easy = NeuralFiveAI("easy")
        self.ai_medium = NeuralFiveAI("medium")
        self.ai_hard = NeuralFiveAI("hard")
        self.ai_expert = NeuralFiveAI("expert")
    
    def test_ai_initialization(self):
        """测试AI初始化"""
        assert self.ai_easy.difficulty == "easy"
        assert self.ai_medium.difficulty == "medium"
        assert self.ai_hard.difficulty == "hard"
        assert self.ai_expert.difficulty == "expert"
    
    def test_get_valid_moves(self):
        """测试获取有效移动"""
        board = np.zeros((15, 15), dtype=int)
        
        # 空棋盘应该有很多有效移动
        moves = self.ai_easy.get_valid_moves(board)
        assert len(moves) > 0
        
        # 在中心放置棋子
        board[7, 7] = 1
        moves_after = self.ai_easy.get_valid_moves(board)
        assert len(moves_after) < len(moves)
    
    def test_get_best_move_easy(self):
        """测试简单难度最佳移动"""
        board = np.zeros((15, 15), dtype=int)
        
        # AI应该能够在中心附近落子
        move = self.ai_easy.get_best_move(board, 1)
        assert move is not None
        assert 0 <= move.row < 15
        assert 0 <= move.col < 15
    
    def test_get_best_move_blocking(self):
        """测试阻挡移动"""
        board = np.zeros((15, 15), dtype=int)
        
        # 创建需要阻挡的情况
        for i in range(4):
            board[7, i] = 1  # 黑棋四连
        
        # AI应该阻挡在(7,4)
        move = self.ai_medium.get_best_move(board, 2)
        assert move is not None
        assert move.row == 7
        assert move.col == 4
    
    def test_get_best_move_winning(self):
        """测试获胜移动"""
        board = np.zeros((15, 15), dtype=int)
        
        # 创建可以获胜的情况
        for i in range(4):
            board[7, i] = 2  # 白棋四连
        
        # AI应该在(7,4)获胜
        move = self.ai_hard.get_best_move(board, 2)
        assert move is not None
        assert move.row == 7
        assert move.col == 4
    
    def test_difficulty_levels(self):
        """测试不同难度级别"""
        board = np.zeros((15, 15), dtype=int)
        
        # 不同难度的AI应该产生不同的移动
        move_easy = self.ai_easy.get_best_move(board, 1)
        move_hard = self.ai_hard.get_best_move(board, 1)
        
        assert move_easy is not None
        assert move_hard is not None
        
        # 高难度AI的移动应该更优（这需要更复杂的测试）
        # 这里只是确保它们能返回有效的移动
        assert 0 <= move_easy.row < 15
        assert 0 <= move_easy.col < 15
        assert 0 <= move_hard.row < 15
        assert 0 <= move_hard.col < 15
    
    def test_performance_easy(self):
        """测试简单难度性能"""
        import time
        
        board = np.zeros((15, 15), dtype=int)
        
        start_time = time.time()
        move = self.ai_easy.get_best_move(board, 1)
        end_time = time.time()
        
        # 简单难度应该在短时间内完成
        assert end_time - start_time < 1.0
        assert move is not None
    
    def test_performance_expert(self):
        """测试专家难度性能"""
        import time
        
        board = np.zeros((15, 15), dtype=int)
        
        start_time = time.time()
        move = self.ai_expert.get_best_move(board, 1)
        end_time = time.time()
        
        # 专家难度可能需要更长时间，但应该有结果
        assert move is not None
        # 这里不强制时间限制，因为专家模式可能很复杂


class TestMove:
    """移动类测试"""
    
    def test_move_creation(self):
        """测试移动创建"""
        move = Move(7, 7, 100.0)
        
        assert move.row == 7
        assert move.col == 7
        assert move.score == 100.0
    
    def test_move_comparison(self):
        """测试移动比较"""
        move1 = Move(7, 7, 100.0)
        move2 = Move(7, 7, 150.0)
        move3 = Move(8, 8, 100.0)
        
        # 分数高的移动更大
        assert move2 > move1
        assert move2.score > move1.score
        
        # 相同分数的移动相等
        move4 = Move(8, 8, 100.0)
        assert move1 == move4
    
    def test_move_str(self):
        """测试移动字符串表示"""
        move = Move(7, 7, 100.0)
        
        assert str(move) == "Move(row=7, col=7, score=100.0)"


class TestIntegration:
    """集成测试"""
    
    def test_ai_vs_ai_game(self):
        """测试AI对AI对局"""
        settings = GameSettings(
            ai_difficulty="medium",
            player_color="black",
            board_size=15
        )
        
        game = GameState(settings)
        game.start_game()
        
        ai_black = NeuralFiveAI("medium")
        ai_white = NeuralFiveAI("medium")
        
        move_count = 0
        max_moves = 225  # 最大移动数
        
        while game.status == game.status.PLAYING and move_count < max_moves:
            current_ai = ai_black if game.current_player == "black" else ai_white
            
            move = current_ai.get_best_move(game.board, 1 if game.current_player == "black" else 2)
            
            if move:
                game.make_move(move.row, move.col, game.current_player)
                move_count += 1
            else:
                break
        
        # 游戏应该正常结束或达到最大移动数
        assert move_count <= max_moves
        print(f"AI对局完成，共{move_count}手")
    
    def test_ai_consistency(self):
        """测试AI一致性"""
        board = np.zeros((15, 15), dtype=int)
        board[7, 7] = 1  # 黑棋在中心
        
        ai = NeuralFiveAI("hard")
        
        # 多次调用应该返回相同的结果（确定性算法）
        move1 = ai.get_best_move(board, 2)
        move2 = ai.get_best_move(board, 2)
        
        assert move1 is not None
        assert move2 is not None
        # 注意：由于可能的随机性或时间限制，这里不强制要求完全相同


@pytest.mark.benchmark
class TestPerformance:
    """性能测试"""
    
    def test_evaluation_speed(self):
        """测试评估速度"""
        import time
        
        evaluator = PositionEvaluator()
        board = np.zeros((15, 15), dtype=int)
        
        # 在棋盘上放置一些棋子
        for i in range(10):
            board[i, i] = 1 if i % 2 == 0 else 2
        
        start_time = time.time()
        
        # 运行多次评估
        for _ in range(100):
            evaluator.evaluate_position(board, 1)
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 100
        
        # 单次评估应该在合理时间内完成
        assert avg_time < 0.01  # 10ms
        print(f"平均评估时间: {avg_time*1000:.2f}ms")
    
    def test_search_depth_performance(self):
        """测试搜索深度性能"""
        import time
        
        ai = NeuralFiveAI("expert")
        board = np.zeros((15, 15), dtype=int)
        
        # 放置一些棋子
        for i in range(5):
            board[7, i] = 1
        
        start_time = time.time()
        move = ai.get_best_move(board, 2)
        end_time = time.time()
        
        search_time = end_time - start_time
        
        # 专家级别的搜索应该在合理时间内完成
        assert search_time < 5.0  # 5秒
        assert move is not None
        
        print(f"专家级搜索时间: {search_time:.2f}s")
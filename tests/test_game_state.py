"""
游戏状态测试

测试NeuralFive游戏状态管理功能：
- 棋盘状态管理
- 移动验证
- 胜负判断
- 游戏流程控制
"""

import pytest
import numpy as np
from src.neuralfive.game_state import GameState, GameStatus, GameSettings


class TestGameSettings:
    """游戏设置测试"""
    
    def test_default_settings(self):
        """测试默认设置"""
        settings = GameSettings()
        
        assert settings.ai_difficulty == "medium"
        assert settings.player_color == "black"
        assert settings.ai_color == "white"
        assert settings.board_size == 15
    
    def test_custom_settings(self):
        """测试自定义设置"""
        settings = GameSettings(
            ai_difficulty="hard",
            player_color="white",
            ai_color="black",
            board_size=19
        )
        
        assert settings.ai_difficulty == "hard"
        assert settings.player_color == "white"
        assert settings.ai_color == "black"
        assert settings.board_size == 19
    
    def test_settings_validation(self):
        """测试设置验证"""
        # 有效的设置
        settings = GameSettings()
        assert settings.is_valid()
        
        # 无效的难度
        settings.ai_difficulty = "invalid"
        assert not settings.is_valid()
        
        # 无效的颜色
        settings.ai_difficulty = "medium"
        settings.player_color = "invalid"
        assert not settings.is_valid()
        
        # 无效的棋盘大小
        settings.player_color = "black"
        settings.board_size = 10
        assert not settings.is_valid()


class TestGameState:
    """游戏状态测试"""
    
    def setup_method(self):
        """设置测试环境"""
        self.settings = GameSettings()
        self.game = GameState(self.settings)
    
    def test_initialization(self):
        """测试初始化"""
        assert self.game.settings == self.settings
        assert self.game.board_size == 15
        assert self.game.status == GameStatus.READY
        assert self.game.current_player == "black"
        assert self.game.winner is None
        assert len(self.game.move_history) == 0
    
    def test_start_game(self):
        """测试开始游戏"""
        self.game.start_game()
        
        assert self.game.status == GameStatus.PLAYING
        assert self.game.current_player == "black"
        assert self.game.winner is None
    
    def test_is_valid_move(self):
        """测试移动有效性"""
        self.game.start_game()
        
        # 有效移动
        assert self.game.is_valid_move(7, 7)
        
        # 无效移动 - 超出边界
        assert not self.game.is_valid_move(-1, 7)
        assert not self.game.is_valid_move(7, -1)
        assert not self.game.is_valid_move(15, 7)
        assert not self.game.is_valid_move(7, 15)
        
        # 无效移动 - 位置已被占用
        self.game.make_move(7, 7, "black")
        assert not self.game.is_valid_move(7, 7)
    
    def test_make_move(self):
        """测试落子"""
        self.game.start_game()
        
        # 有效落子
        success = self.game.make_move(7, 7, "black")
        assert success
        assert self.game.board[7, 7] == 1
        assert self.game.current_player == "white"
        assert len(self.game.move_history) == 1
        
        # 无效落子 - 位置已被占用
        success = self.game.make_move(7, 7, "white")
        assert not success
        assert self.game.board[7, 7] == 1  # 仍然是黑棋
    
    def test_check_winner_horizontal(self):
        """测试横向五连"""
        self.game.start_game()
        
        # 创建横向五连
        for i in range(5):
            self.game.make_move(7, 7 + i, "black")
        
        assert self.game.winner == "black"
        assert self.game.status == GameStatus.FINISHED
    
    def test_check_winner_vertical(self):
        """测试纵向五连"""
        self.game.start_game()
        
        # 创建纵向五连
        for i in range(5):
            self.game.make_move(7 + i, 7, "white")
        
        assert self.game.winner == "white"
        assert self.game.status == GameStatus.FINISHED
    
    def test_check_winner_diagonal(self):
        """测试斜向五连"""
        self.game.start_game()
        
        # 创建主对角线五连
        for i in range(5):
            self.game.make_move(7 + i, 7 + i, "black")
        
        assert self.game.winner == "black"
        assert self.game.status == GameStatus.FINISHED
        
        # 重置游戏，测试副对角线
        self.game = GameState(self.settings)
        self.game.start_game()
        
        # 创建副对角线五连
        for i in range(5):
            self.game.make_move(7 + i, 11 - i, "white")
        
        assert self.game.winner == "white"
        assert self.game.status == GameStatus.FINISHED
    
    def test_check_winner_edge_cases(self):
        """测试边界获胜情况"""
        self.game.start_game()
        
        # 棋盘边缘的五连
        for i in range(5):
            self.game.make_move(0, i, "black")
        
        assert self.game.winner == "black"
        
        # 重置游戏
        self.game = GameState(self.settings)
        self.game.start_game()
        
        # 棋盘角落的五连
        for i in range(5):
            self.game.make_move(i, i, "white")
        
        assert self.game.winner == "white"
    
    def test_check_winner_more_than_five(self):
        """测试超过五连的情况"""
        self.game.start_game()
        
        # 创建六连（应该仍然算获胜）
        for i in range(6):
            self.game.make_move(7, 7 + i, "black")
        
        assert self.game.winner == "black"
    
    def test_undo_move(self):
        """测试撤销移动"""
        self.game.start_game()
        
        # 进行几步移动
        self.game.make_move(7, 7, "black")
        self.game.make_move(6, 6, "white")
        self.game.make_move(7, 8, "black")
        
        assert len(self.game.move_history) == 3
        assert self.game.current_player == "white"
        
        # 撤销一步
        success = self.game.undo_move()
        assert success
        assert len(self.game.move_history) == 2
        assert self.game.board[7, 8] == 0  # 位置应该被清空
        assert self.game.current_player == "black"
        
        # 撤销两步
        success = self.game.undo_move()
        assert success
        assert len(self.game.move_history) == 1
        assert self.game.board[6, 6] == 0
        assert self.game.current_player == "white"
    
    def test_undo_move_empty_history(self):
        """测试撤销空历史"""
        self.game.start_game()
        
        success = self.game.undo_move()
        assert not success
        assert len(self.game.move_history) == 0
    
    def test_reset_game(self):
        """测试重置游戏"""
        self.game.start_game()
        
        # 进行几步移动
        self.game.make_move(7, 7, "black")
        self.game.make_move(6, 6, "white")
        
        # 重置游戏
        self.game.reset_game()
        
        assert self.game.status == GameStatus.READY
        assert len(self.game.move_history) == 0
        assert self.game.winner is None
        assert np.all(self.game.board == 0)
    
    def test_get_game_info(self):
        """测试获取游戏信息"""
        self.game.start_game()
        
        # 进行几步移动
        self.game.make_move(7, 7, "black")
        self.game.make_move(6, 6, "white")
        
        info = self.game.get_game_info()
        
        assert info["move_count"] == 2
        assert info["current_player"] == "black"
        assert info["status"] == "playing"
        assert info["winner"] is None
    
    def test_get_game_info_finished(self):
        """测试获取已结束游戏的信息"""
        self.game.start_game()
        
        # 创建获胜局面
        for i in range(5):
            self.game.make_move(7, 7 + i, "black")
        
        info = self.game.get_game_info()
        
        assert info["move_count"] == 5
        assert info["winner"] == "black"
        assert info["status"] == "finished"
    
    def test_ai_thinking_status(self):
        """测试AI思考状态"""
        settings = GameSettings(ai_color="black")
        game = GameState(settings)
        game.start_game()
        
        # 设置AI思考状态
        game.status = GameStatus.AI_THINKING
        
        info = game.get_game_info()
        assert info["status"] == "ai_thinking"


class TestBoardValidation:
    """棋盘验证测试"""
    
    def test_board_size_validation(self):
        """测试棋盘大小验证"""
        # 有效的棋盘大小
        settings = GameSettings(board_size=15)
        game = GameState(settings)
        assert game.board_size == 15
        
        # 另一个有效的棋盘大小
        settings = GameSettings(board_size=19)
        game = GameState(settings)
        assert game.board_size == 19
    
    def test_out_of_bounds_moves(self):
        """测试越界移动"""
        self.game = GameState(GameSettings())
        self.game.start_game()
        
        # 各种越界情况
        invalid_moves = [
            (-1, 7),   # 负行
            (7, -1),   # 负列
            (15, 7),   # 行太大
            (7, 15),   # 列太大
            (20, 20),  # 都太大
        ]
        
        for row, col in invalid_moves:
            assert not self.game.is_valid_move(row, col)
            success = self.game.make_move(row, col, "black")
            assert not success


class TestMoveHistory:
    """移动历史测试"""
    
    def test_move_history_tracking(self):
        """测试移动历史记录"""
        self.game = GameState(GameSettings())
        self.game.start_game()
        
        # 进行几步移动
        moves = [
            (7, 7, "black"),
            (6, 6, "white"),
            (7, 8, "black"),
            (6, 7, "white"),
        ]
        
        for row, col, color in moves:
            self.game.make_move(row, col, color)
        
        # 检查历史记录
        assert len(self.game.move_history) == 4
        
        for i, (row, col, color) in enumerate(moves):
            move = self.game.move_history[i]
            assert move["row"] == row
            assert move["col"] == col
            assert move["color"] == color
            assert "timestamp" in move
    
    def test_move_history_after_undo(self):
        """测试撤销后的移动历史"""
        self.game = GameState(GameSettings())
        self.game.start_game()
        
        # 进行移动
        self.game.make_move(7, 7, "black")
        self.game.make_move(6, 6, "white")
        
        # 撤销
        self.game.undo_move()
        
        # 历史记录应该只剩一个移动
        assert len(self.game.move_history) == 1
        assert self.game.move_history[0]["row"] == 7
        assert self.game.move_history[0]["col"] == 7
    
    def test_move_history_after_reset(self):
        """测试重置后的移动历史"""
        self.game = GameState(GameSettings())
        self.game.start_game()
        
        # 进行移动
        self.game.make_move(7, 7, "black")
        self.game.make_move(6, 6, "white")
        
        # 重置
        self.game.reset_game()
        
        # 历史记录应该为空
        assert len(self.game.move_history) == 0


class TestEdgeCases:
    """边界情况测试"""
    
    def test_empty_board_winner(self):
        """测试空棋盘获胜检查"""
        self.game = GameState(GameSettings())
        self.game.start_game()
        
        # 空棋盘不应该有获胜者
        winner = self.game.check_winner(7, 7, "black")
        assert winner is None
        assert self.game.winner is None
    
    def test_single_piece_winner(self):
        """测试单棋子获胜检查"""
        self.game = GameState(GameSettings())
        self.game.start_game()
        
        # 单棋子不应该获胜
        self.game.make_move(7, 7, "black")
        winner = self.game.check_winner(7, 7, "black")
        assert winner is None
        assert self.game.winner is None
    
    def test_full_board_no_winner(self):
        """测试满棋盘无获胜者"""
        self.game = GameState(GameSettings())
        self.game.start_game()
        
        # 填满棋盘但不产生五连
        for row in range(15):
            for col in range(15):
                if (row + col) % 2 == 0:
                    self.game.make_move(row, col, "black")
                else:
                    self.game.make_move(row, col, "white")
        
        # 不应该有获胜者
        assert self.game.winner is None
        assert self.game.status == GameStatus.PLAYING
    
    def test_concurrent_moves(self):
        """测试连续落子"""
        self.game = GameState(GameSettings())
        self.game.start_game()
        
        # 快速连续落子
        for i in range(3):
            self.game.make_move(i, i, "black")
            self.game.make_move(i, i+1, "white")
        
        # 检查状态
        assert len(self.game.move_history) == 6
        assert self.game.current_player == "black"
    
    def test_invalid_player_color(self):
        """测试无效玩家颜色"""
        self.game = GameState(GameSettings())
        self.game.start_game()
        
        # 尝试用无效颜色落子
        success = self.game.make_move(7, 7, "invalid_color")
        assert not success
        assert self.game.board[7, 7] == 0


@pytest.mark.performance
class TestPerformance:
    """性能测试"""
    
    def test_winner_check_performance(self):
        """测试获胜检查性能"""
        import time
        
        self.game = GameState(GameSettings())
        self.game.start_game()
        
        # 创建一个复杂的棋盘状态
        for i in range(10):
            for j in range(10):
                if (i + j) % 3 == 0:
                    self.game.board[i, j] = 1
                elif (i + j) % 3 == 1:
                    self.game.board[i, j] = 2
        
        # 测试获胜检查性能
        start_time = time.time()
        
        for _ in range(100):
            self.game.check_winner(7, 7, "black")
        
        end_time = time.time()
        avg_time = (end_time - start_time) / 100
        
        # 单次获胜检查应该在合理时间内完成
        assert avg_time < 0.001  # 1ms
        print(f"平均获胜检查时间: {avg_time*1000:.3f}ms")
    
    def test_move_validation_performance(self):
        """测试移动验证性能"""
        import time
        
        self.game = GameState(GameSettings())
        self.game.start_game()
        
        # 填充一些棋子
        for i in range(5):
            for j in range(5):
                self.game.board[i, j] = (i + j) % 2 + 1
        
        # 测试移动验证性能
        start_time = time.time()
        
        valid_moves = 0
        for row in range(15):
            for col in range(15):
                if self.game.is_valid_move(row, col):
                    valid_moves += 1
        
        end_time = time.time()
        
        # 验证应该在合理时间内完成
        assert end_time - start_time < 0.01  # 10ms
        assert valid_moves > 0
        
        print(f"移动验证时间: {(end_time-start_time)*1000:.2f}ms")
        print(f"有效移动数: {valid_moves}")
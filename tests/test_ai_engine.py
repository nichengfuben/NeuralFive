"""
AI引擎测试

测试StrategicAI的核心功能
"""

import pytest
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.strategicmind.ai.engine import StrategicAI


class TestStrategicAI:
    """StrategicAI测试类"""
    
    def setup_method(self):
        """测试前准备"""
        self.ai = StrategicAI()
    
    def test_ai_initialization(self):
        """测试AI初始化"""
        assert self.ai.board_size == 15
        assert self.ai.search_depth == 100
        assert self.ai.color is None
        assert self.ai.sum == 0
        assert self.ai.set_num == 0
    
    def test_clear_board(self):
        """测试清空棋盘"""
        # 先下一些棋子
        self.ai._update_map(7, 7, 'black')
        self.ai._update_map(7, 8, 'white')
        
        # 清空棋盘
        self.ai.clear_board()
        
        assert self.ai.sum == 0
        assert self.ai.set_num == 0
        assert all(not point.set for row in self.ai.map for point in row)
    
    def test_make_move(self):
        """测试下棋功能"""
        # 玩家下黑棋
        result = self.ai.make_move(7, 7, 'black')
        
        assert result is not None
        assert 'B' in result
        assert self.ai.color == 'white'  # AI应该是白方
        assert self.ai.otc == 'black'    # 对手是黑方
    
    def test_board_string_format(self):
        """测试棋盘字符串格式"""
        self.ai.make_move(7, 7, 'black')
        board_str = self.ai._get_board_string()
        
        lines = board_str.split('\n')
        assert len(lines) == 15  # 15行
        assert all(len(line) == 15 for line in lines)  # 每行15个字符
        assert all(char in 'BW.' for line in lines for char in line)  # 只包含B、W、.
    
    def test_win_detection(self):
        """测试获胜检测"""
        # 创建五子连珠
        for i in range(5):
            self.ai._update_map(7, 7 + i, 'black')
        
        assert self.ai._check_win()
    
    def test_ai_search_depth(self):
        """测试AI搜索深度"""
        # 设置较浅的搜索深度进行测试
        self.ai.depth = 2
        self.ai.make_move(7, 7, 'black')
        
        # AI应该能够返回一个有效的移动
        # 这里主要测试不会出错
        assert True  # 如果到这里说明没有异常
    
    def test_performance(self):
        """测试性能"""
        import time
        
        start_time = time.time()
        self.ai.make_move(7, 7, 'black')
        end_time = time.time()
        
        # AI响应时间应该在合理范围内（小于5秒）
        assert end_time - start_time < 5.0


if __name__ == "__main__":
    pytest.main([__file__])

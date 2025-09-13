#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI模块测试
"""

import sys
import os
import unittest

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'src')
sys.path.insert(0, src_path)

from ai.five_ai import FiveInARowAI

class TestFiveInARowAI(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        self.ai = FiveInARowAI()
    
    def test_init(self):
        """测试AI初始化"""
        self.assertIsNotNone(self.ai)
        self.assertEqual(len(self.ai.map), 15)
        self.assertEqual(len(self.ai.score_queue), 225)
    
    def test_clear_board(self):
        """测试清空棋盘"""
        # 先在棋盘上放置一些棋子
        self.ai.update_map(7, 7, 'black')
        self.ai.update_map(7, 8, 'white')
        
        # 清空棋盘
        self.ai.clear_board()
        
        # 检查棋盘是否已清空
        for i in range(15):
            for j in range(15):
                self.assertFalse(self.ai.map[i][j].set)
    
    def test_get_board_string(self):
        """测试获取棋盘状态字符串"""
        # 初始状态应该是空棋盘
        board_str = self.ai.get_board_string()
        lines = board_str.split('\n')
        
        self.assertEqual(len(lines), 15)
        for line in lines:
            self.assertEqual(len(line), 15)
            self.assertEqual(line, '.' * 15)
    
    def test_update_map(self):
        """测试更新棋盘"""
        # 在中心位置放置黑子
        self.ai.update_map(7, 7, 'black')
        
        # 检查棋子是否正确放置
        self.assertTrue(self.ai.map[7][7].set)
        self.assertEqual(self.ai.map[7][7].set, 1)  # 黑子标记为1
    
    def test_make_move(self):
        """测试下棋"""
        # 玩家在中心位置放置黑子
        board_state = self.ai.make_move(7, 7, 'black')
        
        # 检查返回的棋盘状态
        self.assertIsInstance(board_state, str)
        self.assertIn('B', board_state)  # 应该包含黑子

if __name__ == '__main__':
    unittest.main()
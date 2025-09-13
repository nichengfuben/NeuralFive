#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行脚本
"""

import sys
import os
import unittest

def run_tests():
    """运行所有测试"""
    # 添加src和tests目录到Python路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_path = os.path.join(current_dir, 'src')
    tests_path = os.path.join(current_dir, 'tests')
    sys.path.insert(0, src_path)
    sys.path.insert(0, tests_path)
    
    # 发现并运行测试
    loader = unittest.TestLoader()
    start_dir = os.path.join(current_dir, 'tests')
    suite = loader.discover(start_dir, pattern='test*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
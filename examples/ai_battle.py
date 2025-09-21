"""
AI对战示例

展示两个AI之间的对战
"""

from strategicmind import StrategicAI, GameBoard, GameRules
import time


def ai_vs_ai():
    """AI对战示例"""
    print("AI vs AI 对战示例")
    print("=" * 50)
    
    # 创建两个AI
    ai1 = StrategicAI(search_depth=50)  # 较浅的搜索深度
    ai2 = StrategicAI(search_depth=100)  # 较深的搜索深度
    
    board = GameBoard()
    rules = GameRules()
    
    print("AI1 (深度50) vs AI2 (深度100)")
    print("游戏开始！")
    print()
    
    current_player = 'black'
    move_count = 0
    max_moves = 100  # 防止无限循环
    
    while move_count < max_moves:
        move_count += 1
        print(f"第 {move_count} 步: {current_player} 回合")
        
        # 获取当前AI
        current_ai = ai1 if current_player == 'black' else ai2
        
        # 获取空位置
        empty_positions = board.get_empty_positions()
        if not empty_positions:
            print("棋盘已满，平局！")
            break
        
        # 随机选择一个空位置（简化示例）
        import random
        row, col = random.choice(empty_positions)
        
        # 下棋
        if board.make_move(row, col, current_player):
            print(f"{current_player} 下在 ({row}, {col})")
            
            # 检查获胜者
            winner = board.check_winner()
            if winner:
                print(f"游戏结束！{winner} 获胜！")
                print(f"AI1 ({ai1.search_depth}层) vs AI2 ({ai2.search_depth}层)")
                break
            
            # 切换玩家
            current_player = 'white' if current_player == 'black' else 'black'
        else:
            print(f"{current_player} 下棋失败！")
            break
        
        # 显示棋盘状态
        if move_count % 10 == 0:  # 每10步显示一次
            print("当前棋盘状态：")
            print(board.get_board_string())
            print("-" * 30)
        
        # 添加延迟以便观察
        time.sleep(0.1)
    
    # 显示最终结果
    print("\n最终棋盘状态：")
    print(board.get_board_string())
    
    game_info = board.get_game_info()
    print(f"\n游戏统计：")
    print(f"总步数: {game_info['move_count']}")
    print(f"获胜者: {game_info['winner'] or '平局'}")


def performance_test():
    """性能测试示例"""
    print("\n性能测试")
    print("=" * 30)
    
    ai = StrategicAI()
    board = GameBoard()
    
    # 测试AI响应时间
    test_moves = [(7, 7), (7, 8), (8, 7), (8, 8)]
    
    for i, (row, col) in enumerate(test_moves):
        color = 'black' if i % 2 == 0 else 'white'
        
        start_time = time.time()
        result = ai.make_move(row, col, color)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # 转换为毫秒
        print(f"移动 {i+1}: {response_time:.2f}ms")
    
    print(f"平均响应时间: {response_time:.2f}ms")


if __name__ == "__main__":
    ai_vs_ai()
    performance_test()

"""
StrategicMind 基本使用示例

展示如何使用 StrategicMind 进行基本的五子棋游戏
"""

from strategicmind import StrategicAI, GameBoard, GameRules


def main():
    """基本使用示例"""
    print("StrategicMind 基本使用示例")
    print("=" * 50)
    
    # 创建AI和棋盘
    ai = StrategicAI()
    board = GameBoard()
    rules = GameRules()
    
    print("游戏开始！")
    print("棋盘状态：")
    print(board.get_board_string())
    print()
    
    # 模拟游戏过程
    moves = [
        (7, 7, 'black'),   # 玩家下黑棋
        (7, 8, 'white'),   # AI下白棋
        (8, 7, 'black'),   # 玩家下黑棋
        (8, 8, 'white'),   # AI下白棋
    ]
    
    for i, (row, col, color) in enumerate(moves, 1):
        print(f"第 {i} 步: {color} 下在 ({row}, {col})")
        
        # 检查移动是否合法
        is_valid, reason = rules.is_valid_move(board.get_board_state(), row, col, color)
        if not is_valid:
            print(f"非法移动: {reason}")
            continue
        
        # 下棋
        if board.make_move(row, col, color):
            print("下棋成功！")
            
            # 检查是否有获胜者
            winner = board.check_winner()
            if winner:
                print(f"游戏结束！{winner} 获胜！")
                break
            
            # 如果是玩家下棋，让AI响应
            if color == 'black':
                print("AI 思考中...")
                ai_result = ai.make_move(row, col, color)
                print("AI 响应：")
                print(ai_result)
        else:
            print("下棋失败！")
        
        print("当前棋盘状态：")
        print(board.get_board_string())
        print("-" * 30)
    
    # 显示游戏统计
    game_info = board.get_game_info()
    print(f"游戏统计：")
    print(f"总步数: {game_info['move_count']}")
    print(f"获胜者: {game_info['winner'] or '无'}")
    print(f"棋盘是否已满: {game_info['is_full']}")


if __name__ == "__main__":
    main()

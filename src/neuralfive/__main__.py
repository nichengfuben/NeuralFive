"""
NeuralFive - AI五子棋

命令行入口点，提供多种启动方式：
- 图形界面模式
- 命令行模式
- 训练模式
- 分析模式
"""

import argparse
import sys
from typing import Optional

from .gui import NeuralFiveGUI, UITheme
from .ai_engine import NeuralFiveAI
from .game_state import GameState, GameSettings


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="NeuralFive - AI五子棋",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
    # 启动图形界面
    python -m neuralfive
    
    # 指定主题
    python -m neuralfive --theme dark
    
    # 命令行模式
    python -m neuralfive --cli --difficulty hard
    
    # 训练模式
    python -m neuralfive --train --episodes 1000
    
    # 分析模式
    python -m neuralfive --analyze --position "7,7:1;6,6:2"
        """
    )
    
    # 基本选项
    parser.add_argument(
        "--theme",
        choices=["classic", "modern", "dark"],
        default="modern",
        help="UI主题 (默认: modern)"
    )
    
    parser.add_argument(
        "--language",
        choices=["zh_CN", "en_US"],
        default="zh_CN",
        help="界面语言 (默认: zh_CN)"
    )
    
    # 模式选择
    mode_group = parser.add_mutually_exclusive_group()
    
    mode_group.add_argument(
        "--cli",
        action="store_true",
        help="命令行模式"
    )
    
    mode_group.add_argument(
        "--train",
        action="store_true",
        help="训练模式"
    )
    
    mode_group.add_argument(
        "--analyze",
        action="store_true",
        help="分析模式"
    )
    
    # 游戏选项
    parser.add_argument(
        "--difficulty",
        choices=["easy", "medium", "hard", "expert"],
        default="medium",
        help="AI难度 (默认: medium)"
    )
    
    parser.add_argument(
        "--board-size",
        type=int,
        choices=[15, 19],
        default=15,
        help="棋盘大小 (默认: 15)"
    )
    
    parser.add_argument(
        "--player-color",
        choices=["black", "white"],
        default="black",
        help="玩家棋色 (默认: black)"
    )
    
    # 训练选项
    parser.add_argument(
        "--episodes",
        type=int,
        default=100,
        help="训练局数 (默认: 100)"
    )
    
    # 分析选项
    parser.add_argument(
        "--position",
        type=str,
        help="分析位置 (格式: row,col:piece;row,col:piece)"
    )
    
    # 输出选项
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="详细输出"
    )
    
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="静默模式"
    )
    
    return parser.parse_args()


def run_gui(args: argparse.Namespace) -> None:
    """运行图形界面"""
    try:
        theme_map = {
            "classic": UITheme.CLASSIC,
            "modern": UITheme.MODERN,
            "dark": UITheme.DARK
        }
        
        gui = NeuralFiveGUI(theme=theme_map[args.theme])
        gui.current_language = args.language
        gui.run()
        
    except ImportError as e:
        print(f"错误: 缺少依赖包 {e}")
        print("请安装: pip install pygame")
        sys.exit(1)
    except Exception as e:
        print(f"运行错误: {e}")
        sys.exit(1)


def run_cli(args: argparse.Namespace) -> None:
    """运行命令行模式"""
    print("NeuralFive 命令行模式")
    print("=" * 30)
    
    # 创建游戏设置
    settings = GameSettings(
        ai_difficulty=args.difficulty,
        player_color=args.player_color,
        board_size=args.board_size
    )
    
    # 创建AI引擎
    ai = NeuralFiveAI(args.difficulty)
    
    # 创建游戏状态
    game = GameState(settings)
    game.start_game()
    
    print(f"AI难度: {args.difficulty}")
    print(f"玩家棋色: {args.player_color}")
    print(f"棋盘大小: {args.board_size}x{args.board_size}")
    print("\n游戏开始!")
    print("输入格式: row col (例如: 7 7)")
    print("输入 'quit' 退出游戏")
    print("输入 'undo' 撤销上一步")
    print("输入 'help' 显示帮助")
    
    while game.status == game.status.PLAYING:
        # 显示棋盘
        print("\n" + "=" * 30)
        print_game_board(game)
        
        # 显示当前玩家
        current_player = "玩家" if game.current_player == settings.player_color else "AI"
        print(f"当前玩家: {current_player}")
        
        if game.current_player == settings.player_color:
            # 玩家回合
            while True:
                try:
                    user_input = input("请输入落子位置 (row col): ").strip().lower()
                    
                    if user_input == 'quit':
                        print("游戏结束")
                        return
                    elif user_input == 'undo':
                        game.undo_move()
                        break
                    elif user_input == 'help':
                        print("帮助信息:")
                        print("- 输入两个数字表示落子位置 (行 列)")
                        print("- 行和列的范围是 0-14 (15x15棋盘)")
                        print("- 输入 'undo' 撤销上一步")
                        print("- 输入 'quit' 退出游戏")
                        continue
                    
                    # 解析输入
                    row, col = map(int, user_input.split())
                    
                    if game.is_valid_move(row, col):
                        success = game.make_move(row, col, settings.player_color)
                        if success:
                            break
                    else:
                        print("无效位置，请重新输入")
                        
                except ValueError:
                    print("输入格式错误，请输入两个数字")
                except Exception as e:
                    print(f"输入错误: {e}")
        
        else:
            # AI回合
            print("AI思考中...")
            try:
                move = ai.get_best_move(game.board, settings.ai_color)
                if move:
                    game.make_move(move.row, move.col, settings.ai_color)
                    print(f"AI落子: {move.row} {move.col}")
                else:
                    print("AI无法找到有效落子")
                    break
            except Exception as e:
                print(f"AI计算错误: {e}")
                break
        
        # 检查游戏结束
        if game.winner:
            print("\n" + "=" * 30)
            print_game_board(game)
            
            if game.winner == settings.player_color:
                print("恭喜获胜!")
            else:
                print("AI获胜!")
            break
    
    print("\n游戏结束")


def print_game_board(game: GameState) -> None:
    """打印游戏棋盘"""
    print("  ", end="")
    for col in range(game.board_size):
        print(f"{col:2}", end=" ")
    print()
    
    for row in range(game.board_size):
        print(f"{row:2}", end=" ")
        for col in range(game.board_size):
            piece = game.board[row, col]
            if piece == 0:
                print("· ", end=" ")
            elif piece == 1:
                print("● ", end=" ")
            else:
                print("○ ", end=" ")
        print()


def run_training(args: argparse.Namespace) -> None:
    """运行训练模式"""
    print(f"训练模式 - {args.episodes} 局")
    print("=" * 40)
    
    # 这里可以添加训练逻辑
    print("训练功能开发中...")
    print("将支持:")
    print("- AI自我对弈训练")
    print("- 策略网络优化")
    print("- 价值网络训练")
    print("- 模型保存和加载")


def run_analysis(args: argparse.Namespace) -> None:
    """运行分析模式"""
    print("分析模式")
    print("=" * 20)
    
    if not args.position:
        print("错误: 请提供 --position 参数")
        return
    
    # 解析位置
    try:
        board = parse_position(args.position)
        print("当前局面:")
        print_board_analysis(board)
        
        # 分析评估
        ai = NeuralFiveAI("expert")
        evaluation = ai.evaluate_position(board)
        print(f"\n位置评估: {evaluation}")
        
        # 建议着法
        best_move = ai.get_best_move(board, 1)  # 1表示黑棋
        if best_move:
            print(f"建议着法: {best_move.row}, {best_move.col}")
        
    except Exception as e:
        print(f"分析错误: {e}")


def parse_position(position_str: str) -> list:
    """解析位置字符串"""
    board = [[0 for _ in range(15)] for _ in range(15)]
    
    if not position_str:
        return board
    
    # 格式: row,col:piece;row,col:piece
    moves = position_str.split(';')
    for move in moves:
        if not move:
            continue
        
        pos, piece = move.split(':')
        row, col = map(int, pos.split(','))
        board[row][col] = int(piece)
    
    return board


def print_board_analysis(board: list) -> None:
    """打印分析棋盘"""
    print("  ", end="")
    for col in range(15):
        print(f"{col:2}", end=" ")
    print()
    
    for row in range(15):
        print(f"{row:2}", end=" ")
        for col in range(15):
            piece = board[row][col]
            if piece == 0:
                print("· ", end=" ")
            elif piece == 1:
                print("● ", end=" ")
            else:
                print("○ ", end=" ")
        print()


def main():
    """主函数"""
    args = parse_args()
    
    try:
        if args.cli:
            run_cli(args)
        elif args.train:
            run_training(args)
        elif args.analyze:
            run_analysis(args)
        else:
            run_gui(args)
            
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"程序运行错误: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
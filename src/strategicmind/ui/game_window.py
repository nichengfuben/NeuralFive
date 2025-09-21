"""
主游戏窗口

基于Pygame的现代化游戏界面，支持中英文切换和流畅动画
"""

import pygame
import sys
import threading
import time
import os
from typing import Optional, Tuple, Dict, Any

from ..ai.engine import StrategicAI
from ..game.board import GameBoard
from ..game.state import GameState, GameStatus, PlayerType
from ..game.rules import GameRules
from .menu import MainMenu
from .game_ui import GameUI
from .settings import SettingsUI


class GameWindow:
    """主游戏窗口类"""
    
    def __init__(self, width: int = 900, height: int = 700):
        """
        初始化游戏窗口
        
        Args:
            width: 窗口宽度
            height: 窗口高度
        """
        # 初始化Pygame
        pygame.init()
        
        # 窗口设置
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("StrategicMind - 智能策略游戏引擎")
        
        # 设置字体
        self.setup_fonts()
        
        # 游戏组件
        self.clock = pygame.time.Clock()
        self.board = GameBoard()
        self.game_state = GameState()
        self.game_rules = GameRules()
        self.ai = StrategicAI()
        
        # UI组件
        self.main_menu = MainMenu(self)
        self.game_ui = GameUI(self)
        self.settings_ui = SettingsUI(self)
        
        # 当前界面
        self.current_ui = self.main_menu
        
        # 颜色定义
        self.colors = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'brown': (205, 170, 125),
            'dark_brown': (139, 90, 43),
            'green': (34, 139, 34),
            'red': (220, 20, 60),
            'blue': (30, 144, 255),
            'gray': (128, 128, 128),
            'light_gray': (200, 200, 200),
            'yellow': (255, 215, 0),
            'orange': (255, 165, 0),
            'gold': (255, 215, 0),
        }
        
        # 动画效果
        self.animation_time = 0
        self.thinking_dots = 0
        self.thinking_timer = 0
        
        # AI线程
        self.ai_thinking = False
        self.ai_thread = None
        self.ai_move_result = None
        
        # 语言设置
        self.language = "zh"  # 默认中文
        self.texts = self._load_texts()
    
    def setup_fonts(self):
        """设置字体系统"""
        font_paths = []
        
        if sys.platform == 'win32':
            font_paths = [
                'C:/Windows/Fonts/msyh.ttc',
                'C:/Windows/Fonts/simsun.ttc',
                'C:/Windows/Fonts/simhei.ttf',
            ]
        elif sys.platform == 'darwin':
            font_paths = [
                '/System/Library/Fonts/PingFang.ttc',
                '/Library/Fonts/Songti.ttc',
            ]
        else:
            font_paths = [
                '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            ]
        
        font_loaded = False
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    self.font = pygame.font.Font(font_path, 22)
                    self.small_font = pygame.font.Font(font_path, 16)
                    self.large_font = pygame.font.Font(font_path, 32)
                    self.title_font = pygame.font.Font(font_path, 42)
                    font_loaded = True
                    break
                except:
                    continue
        
        if not font_loaded:
            self.font = pygame.font.Font(None, 28)
            self.small_font = pygame.font.Font(None, 20)
            self.large_font = pygame.font.Font(None, 40)
            self.title_font = pygame.font.Font(None, 56)
            self.use_english = True
        else:
            self.use_english = False
    
    def _load_texts(self) -> Dict[str, Dict[str, str]]:
        """加载多语言文本"""
        return {
            'zh': {
                'title': 'StrategicMind',
                'subtitle': '—— 智能策略游戏引擎 ——',
                'choose': '请选择您的棋色',
                'black': '执黑',
                'white': '执白',
                'restart': '重新开始',
                'menu': '返回菜单',
                'info': '游戏信息',
                'your_turn': '您的回合',
                'ai_thinking': 'AI思考中',
                'current': '当前回合',
                'player': '玩家',
                'ai': 'AI',
                'black_move': '黑方行动',
                'white_move': '白方行动',
                'win': '恭喜您获胜！',
                'lose': 'AI获胜！',
                'draw': '平局！',
                'first': '（先手）',
                'second': '（后手）',
                'vs': '对战双方',
                'tips': '游戏提示',
                'tip1': '• 点击交叉点落子',
                'tip2': '• 红框标记最后一手',
                'tip3': '• 五子连珠获胜',
                'rules': '游戏规则：',
                'rule1': '• 黑棋先行',
                'rule2': '• 轮流落子',
                'rule3': '• 五子连珠获胜'
            },
            'en': {
                'title': 'StrategicMind',
                'subtitle': '—— Intelligent Strategy Game Engine ——',
                'choose': 'Choose Your Color',
                'black': 'Black',
                'white': 'White',
                'restart': 'New Game',
                'menu': 'Main Menu',
                'info': 'Game Info',
                'your_turn': 'Your Turn',
                'ai_thinking': 'AI Thinking',
                'current': 'Current',
                'player': 'Player',
                'ai': 'AI',
                'black_move': 'Black Move',
                'white_move': 'White Move',
                'win': 'You Win!',
                'lose': 'AI Wins!',
                'draw': 'Draw!',
                'first': '(First)',
                'second': '(Second)',
                'vs': 'Players',
                'tips': 'Tips',
                'tip1': '• Click intersection to move',
                'tip2': '• Red mark shows last move',
                'tip3': '• Connect 5 stones to win',
                'rules': 'Rules:',
                'rule1': '• Black moves first',
                'rule2': '• Take turns to play',
                'rule3': '• 5 in a row wins'
            }
        }
    
    def get_text(self, key: str) -> str:
        """获取显示文本"""
        return self.texts[self.language].get(key, key)
    
    def set_language(self, language: str):
        """设置语言"""
        if language in self.texts:
            self.language = language
    
    def switch_ui(self, ui_name: str):
        """切换界面"""
        ui_map = {
            'menu': self.main_menu,
            'game': self.game_ui,
            'settings': self.settings_ui,
        }
        if ui_name in ui_map:
            self.current_ui = ui_map[ui_name]
    
    def start_game(self, player_color: str):
        """开始游戏"""
        self.game_state.start_game(
            black_player='human' if player_color == 'black' else 'ai',
            white_player='ai' if player_color == 'black' else 'human'
        )
        self.board.reset()
        self.ai.clear_board()
        self.switch_ui('game')
        
        # 如果AI先手，让AI下第一步
        if self.game_state.current_player == 'black' and self.game_state.is_ai_turn():
            self._ai_first_move()
    
    def _ai_first_move(self):
        """AI先手"""
        def ai_first():
            time.sleep(0.5)
            # AI下中心位置
            center = self.board.size // 2
            self.board.make_move(center, center, 'black')
            self.game_state.make_move(center, center, 'black', PlayerType.AI)
            self.ai.make_move(center, center, 'white')  # 设置AI为白方
        
        self.ai_thread = threading.Thread(target=ai_first)
        self.ai_thread.daemon = True
        self.ai_thread.start()
    
    def make_player_move(self, row: int, col: int) -> bool:
        """玩家下棋"""
        if not self.game_state.is_ai_turn() and self.game_state.status == GameStatus.PLAYING:
            if self.board.make_move(row, col, self.game_state.current_player):
                self.game_state.make_move(row, col, self.game_state.current_player, PlayerType.HUMAN)
                
                # 检查游戏是否结束
                winner = self.board.check_winner()
                if winner:
                    self.game_state.end_game(winner)
                    return True
                
                # 如果游戏继续，让AI下棋
                if self.game_state.status == GameStatus.PLAYING:
                    self._ai_move()
                
                return True
        return False
    
    def _ai_move(self):
        """AI下棋"""
        if self.game_state.is_ai_turn() and not self.ai_thinking:
            self.ai_thinking = True
            self.ai_move_result = None
            
            def ai_think():
                start_time = time.time()
                board_str = self.ai.make_move(
                    self.game_state.move_history[-1].row,
                    self.game_state.move_history[-1].col,
                    self.game_state.move_history[-1].color
                )
                thinking_time = time.time() - start_time
                self.ai_move_result = (board_str, thinking_time)
            
            self.ai_thread = threading.Thread(target=ai_think)
            self.ai_thread.daemon = True
            self.ai_thread.start()
    
    def check_ai_move(self):
        """检查AI是否完成思考"""
        if self.ai_thinking and self.ai_move_result is not None:
            self.ai_thinking = False
            board_str, thinking_time = self.ai_move_result
            self.ai_move_result = None
            
            # 解析AI的移动
            self._parse_ai_board(board_str)
            
            # 检查游戏是否结束
            winner = self.board.check_winner()
            if winner:
                self.game_state.end_game(winner)
            elif self.game_state.status == GameStatus.PLAYING:
                # 切换回玩家回合
                pass
    
    def _parse_ai_board(self, board_str: str):
        """解析AI返回的棋盘字符串"""
        lines = board_str.strip().split('\n')
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == 'B' and self.board.board[i][j] != 1:
                    self.board.make_move(i, j, 'black')
                    self.game_state.make_move(i, j, 'black', PlayerType.AI)
                elif char == 'W' and self.board.board[i][j] != 2:
                    self.board.make_move(i, j, 'white')
                    self.game_state.make_move(i, j, 'white', PlayerType.AI)
    
    def reset_game(self):
        """重置游戏"""
        if self.ai_thread and self.ai_thread.is_alive():
            self.ai_thread.join(timeout=0.1)
        
        self.board.reset()
        self.game_state.reset()
        self.ai.clear_board()
        self.ai_thinking = False
        self.ai_move_result = None
    
    def draw_gradient_background(self):
        """绘制渐变背景"""
        for y in range(self.height):
            color_value = 220 + (y * 35 // self.height)
            color = (color_value, color_value, min(255, color_value + 10))
            pygame.draw.line(self.screen, color, (0, y), (self.width, y))
    
    def run(self):
        """主游戏循环"""
        running = True
        
        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.ai_thread and self.ai_thread.is_alive():
                        self.ai_thread.join(timeout=0.1)
                    running = False
                else:
                    # 将事件传递给当前UI
                    self.current_ui.handle_event(event)
            
            # 更新游戏状态
            if self.current_ui == self.game_ui:
                self.check_ai_move()
            
            # 更新动画
            self.animation_time += 0.05
            if self.ai_thinking:
                self.thinking_timer += 1
                if self.thinking_timer % 30 == 0:
                    self.thinking_dots = (self.thinking_dots + 1) % 4
            
            # 绘制
            self.draw_gradient_background()
            self.current_ui.draw()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


def main():
    """主函数"""
    game = GameWindow()
    game.run()


if __name__ == "__main__":
    main()

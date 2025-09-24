"""
NeuralFive图形用户界面

基于Pygame的现代五子棋游戏界面，支持：
- 响应式布局和动画效果
- 多语言支持
- AI难度选择
- 游戏状态显示
- 撤销功能
- 游戏回放
"""

import pygame
import sys
import threading
import time
import os
from typing import Optional, Tuple, Dict, List
from dataclasses import dataclass
from enum import Enum

from .game_state import GameState, GameStatus, GameSettings
from .ai_engine import NeuralFiveAI

# 游戏常量
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
BOARD_SIZE = 15
CELL_SIZE = 40
BOARD_START_X = 50
BOARD_START_Y = 80
BOARD_WIDTH = CELL_SIZE * (BOARD_SIZE - 1)

# 颜色定义
COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'BROWN': (205, 170, 125),
    'DARK_BROWN': (139, 90, 43),
    'GREEN': (34, 139, 34),
    'RED': (220, 20, 60),
    'BLUE': (30, 144, 255),
    'GRAY': (128, 128, 128),
    'LIGHT_GRAY': (200, 200, 200),
    'YELLOW': (255, 215, 0),
    'ORANGE': (255, 165, 0),
    'GOLD': (255, 215, 0),
    'BACKGROUND': (240, 248, 255),
    'PANEL': (248, 250, 252)
}

class UITheme(Enum):
    """UI主题"""
    CLASSIC = "classic"
    MODERN = "modern"
    DARK = "dark"

@dataclass
class UIElements:
    """UI元素位置"""
    # 主菜单按钮
    black_button: pygame.Rect
    white_button: pygame.Rect
    difficulty_buttons: List[pygame.Rect]
    
    # 游戏界面按钮
    restart_button: pygame.Rect
    undo_button: pygame.Rect
    menu_button: pygame.Rect
    
    # 信息面板
    info_panel: pygame.Rect
    status_panel: pygame.Rect

class NeuralFiveGUI:
    """
    NeuralFive图形用户界面
    
    提供现代化的五子棋游戏界面，支持完整的游戏流程
    和丰富的用户交互功能。
    """
    
    def __init__(self, theme: UITheme = UITheme.MODERN):
        """
        初始化GUI
        
        Args:
            theme: UI主题
        """
        pygame.init()
        
        # 设置窗口
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("NeuralFive - AI五子棋")
        
        # 设置图标
        self._setup_window_icon()
        
        # 初始化游戏组件
        self.game_state = None
        self.ai_engine = None
        self.settings = GameSettings()
        
        # UI设置
        self.theme = theme
        self.clock = pygame.time.Clock()
        self.fonts = {}
        self._setup_fonts()
        
        # 动画和效果
        self.animation_time = 0
        self.particle_effects = []
        self.last_hover_pos = None
        
        # AI线程
        self.ai_thread = None
        self.ai_thinking = False
        self.ai_move_result = None
        
        # 多语言支持
        self.current_language = "zh_CN"
        self.texts = self._load_texts()
        
        # 初始化UI元素
        self.ui_elements = self._create_ui_elements()
        
        # 游戏状态
        self.running = True
        self.current_screen = "menu"  # menu, game, settings
        
    def _setup_window_icon(self) -> None:
        """设置窗口图标"""
        try:
            # 创建简单的图标
            icon_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
            icon_surface.fill((0, 0, 0, 0))
            
            # 绘制五子棋图标
            pygame.draw.circle(icon_surface, COLORS['BLACK'], (16, 16), 12)
            pygame.draw.circle(icon_surface, COLORS['WHITE'], (16, 16), 10, 2)
            
            pygame.display.set_icon(icon_surface)
        except:
            pass
    
    def _setup_fonts(self) -> None:
        """设置字体系统"""
        # 尝试加载系统中文字体
        font_paths = self._get_system_font_paths()
        
        font_loaded = False
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    self.fonts['normal'] = pygame.font.Font(font_path, 22)
                    self.fonts['small'] = pygame.font.Font(font_path, 16)
                    self.fonts['large'] = pygame.font.Font(font_path, 32)
                    self.fonts['title'] = pygame.font.Font(font_path, 42)
                    font_loaded = True
                    break
                except:
                    continue
        
        # 如果没有找到合适字体，使用默认字体
        if not font_loaded:
            self.fonts['normal'] = pygame.font.Font(None, 28)
            self.fonts['small'] = pygame.font.Font(None, 20)
            self.fonts['large'] = pygame.font.Font(None, 40)
            self.fonts['title'] = pygame.font.Font(None, 56)
    
    def _get_system_font_paths(self) -> List[str]:
        """获取系统字体路径"""
        if sys.platform == 'win32':
            return [
                'C:/Windows/Fonts/msyh.ttc',      # 微软雅黑
                'C:/Windows/Fonts/simsun.ttc',     # 宋体
                'C:/Windows/Fonts/simhei.ttf',     # 黑体
            ]
        elif sys.platform == 'darwin':
            return [
                '/System/Library/Fonts/PingFang.ttc',
                '/Library/Fonts/Songti.ttc',
            ]
        else:
            return [
                '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            ]
    
    def _load_texts(self) -> Dict[str, str]:
        """加载文本资源"""
        texts = {
            "zh_CN": {
                "title": "NeuralFive AI五子棋",
                "subtitle": "挑战最强AI",
                "choose_color": "选择您的棋色",
                "choose_difficulty": "选择AI难度",
                "black": "执黑",
                "white": "执白",
                "easy": "简单",
                "medium": "中等",
                "hard": "困难",
                "expert": "专家",
                "start_game": "开始游戏",
                "restart": "重新开始",
                "undo": "撤销",
                "menu": "主菜单",
                "your_turn": "您的回合",
                "ai_thinking": "AI思考中",
                "you_win": "恭喜获胜！",
                "ai_wins": "AI获胜！",
                "draw": "平局！",
                "game_info": "游戏信息",
                "move_count": "步数",
                "time_used": "用时",
                "ai_level": "AI等级",
                "rules": "游戏规则",
                "rule1": "• 黑棋先行",
                "rule2": "• 轮流落子",
                "rule3": "• 五子连珠获胜",
                "tips": "游戏提示",
                "tip1": "• 点击交叉点落子",
                "tip2": "• 红框标记最后一手",
                "tip3": "• 思考时间越短AI越强"
            },
            "en_US": {
                "title": "NeuralFive AI Gomoku",
                "subtitle": "Challenge the Strongest AI",
                "choose_color": "Choose Your Color",
                "choose_difficulty": "Select AI Difficulty",
                "black": "Black",
                "white": "White",
                "easy": "Easy",
                "medium": "Medium",
                "hard": "Hard",
                "expert": "Expert",
                "start_game": "Start Game",
                "restart": "Restart",
                "undo": "Undo",
                "menu": "Menu",
                "your_turn": "Your Turn",
                "ai_thinking": "AI Thinking",
                "you_win": "You Win!",
                "ai_wins": "AI Wins!",
                "draw": "Draw!",
                "game_info": "Game Info",
                "move_count": "Moves",
                "time_used": "Time",
                "ai_level": "AI Level",
                "rules": "Game Rules",
                "rule1": "• Black moves first",
                "rule2": "• Take turns",
                "rule3": "• Connect 5 to win",
                "tips": "Game Tips",
                "tip1": "• Click intersection to move",
                "tip2": "• Red mark shows last move",
                "tip3": "• Shorter thinking time = stronger AI"
            }
        }
        
        return texts.get(self.current_language, texts["zh_CN"])
    
    def _create_ui_elements(self) -> UIElements:
        """创建UI元素"""
        # 主菜单按钮
        black_button = pygame.Rect(270, 350, 150, 55)
        white_button = pygame.Rect(480, 350, 150, 55)
        
        # 难度按钮
        difficulty_buttons = [
            pygame.Rect(200, 450, 100, 40),  # Easy
            pygame.Rect(320, 450, 100, 40),  # Medium
            pygame.Rect(440, 450, 100, 40),  # Hard
            pygame.Rect(560, 450, 100, 40),  # Expert
        ]
        
        # 游戏界面按钮
        restart_button = pygame.Rect(640, 280, 230, 45)
        undo_button = pygame.Rect(640, 340, 110, 45)
        menu_button = pygame.Rect(760, 340, 110, 45)
        
        # 信息面板
        info_panel = pygame.Rect(640, 80, 230, 180)
        status_panel = pygame.Rect(640, 420, 230, 200)
        
        return UIElements(
            black_button=black_button,
            white_button=white_button,
            difficulty_buttons=difficulty_buttons,
            restart_button=restart_button,
            undo_button=undo_button,
            menu_button=menu_button,
            info_panel=info_panel,
            status_panel=status_panel
        )
    
    def run(self) -> None:
        """运行GUI主循环"""
        while self.running:
            self.animation_time += 1
            
            # 处理事件
            for event in pygame.event.get():
                self._handle_event(event)
            
            # 更新AI线程
            self._update_ai_thread()
            
            # 渲染界面
            self._render()
            
            # 更新显示
            pygame.display.flip()
            self.clock.tick(60)
        
        # 清理资源
        self._cleanup()
    
    def _handle_event(self, event: pygame.event.Event) -> None:
        """处理事件"""
        if event.type == pygame.QUIT:
            self.running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_click(event.pos)
        
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_hover(event.pos)
        
        elif event.type == pygame.KEYDOWN:
            self._handle_keyboard(event)
    
    def _handle_mouse_click(self, pos: Tuple[int, int]) -> None:
        """处理鼠标点击"""
        if self.current_screen == "menu":
            self._handle_menu_click(pos)
        elif self.current_screen == "game":
            self._handle_game_click(pos)
    
    def _handle_menu_click(self, pos: Tuple[int, int]) -> None:
        """处理主菜单点击"""
        # 颜色选择
        if self.ui_elements.black_button.collidepoint(pos):
            self.settings.player_color = "black"
            self.settings.ai_color = "white"
            self.current_screen = "game"
            self.start_new_game()
        
        elif self.ui_elements.white_button.collidepoint(pos):
            self.settings.player_color = "white"
            self.settings.ai_color = "black"
            self.current_screen = "game"
            self.start_new_game()
        
        # 难度选择
        for i, button in enumerate(self.ui_elements.difficulty_buttons):
            if button.collidepoint(pos):
                difficulties = ["easy", "medium", "hard", "expert"]
                self.settings.ai_difficulty = difficulties[i]
    
    def _handle_game_click(self, pos: Tuple[int, int]) -> None:
        """处理游戏界面点击"""
        # 棋盘点击
        if self._is_board_click(pos):
            self._handle_board_click(pos)
        
        # 按钮点击
        elif self.ui_elements.restart_button.collidepoint(pos):
            self.start_new_game()
        
        elif self.ui_elements.undo_button.collidepoint(pos):
            self.undo_move()
        
        elif self.ui_elements.menu_button.collidepoint(pos):
            self.current_screen = "menu"
    
    def _handle_board_click(self, pos: Tuple[int, int]) -> None:
        """处理棋盘点击"""
        if not self.game_state or self.game_state.status != GameStatus.PLAYING:
            return
        
        row, col = self._screen_to_board_coords(pos)
        
        if self.game_state.is_valid_move(row, col):
            # 玩家落子
            success = self.game_state.make_move(row, col, self.settings.player_color)
            
            if success:
                # 检查游戏是否结束
                if self.game_state.winner:
                    return
                
                # AI思考
                self._start_ai_thinking()
    
    def _handle_mouse_hover(self, pos: Tuple[int, int]) -> None:
        """处理鼠标悬停"""
        if self.current_screen == "game":
            board_pos = self._screen_to_board_coords(pos)
            if board_pos != self.last_hover_pos:
                self.last_hover_pos = board_pos
                self._add_hover_effect(board_pos)
    
    def _handle_keyboard(self, event: pygame.event.Event) -> None:
        """处理键盘事件"""
        if event.key == pygame.K_ESCAPE:
            self.current_screen = "menu"
        
        elif event.key == pygame.K_r:
            self.start_new_game()
        
        elif event.key == pygame.K_u:
            self.undo_move()
    
    def _is_board_click(self, pos: Tuple[int, int]) -> bool:
        """检查是否点击了棋盘区域"""
        x, y = pos
        return (BOARD_START_X <= x < BOARD_START_X + BOARD_WIDTH and
                BOARD_START_Y <= y < BOARD_START_Y + BOARD_WIDTH)
    
    def _screen_to_board_coords(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """将屏幕坐标转换为棋盘坐标"""
        x, y = pos
        
        # 计算最近的交叉点
        col = round((x - BOARD_START_X) / CELL_SIZE)
        row = round((y - BOARD_START_Y) / CELL_SIZE)
        
        # 限制在有效范围内
        row = max(0, min(row, BOARD_SIZE - 1))
        col = max(0, min(col, BOARD_SIZE - 1))
        
        return row, col
    
    def start_new_game(self) -> None:
        """开始新游戏"""
        # 创建新的游戏状态
        self.game_state = GameState(self.settings)
        self.game_state.start_game()
        
        # 创建AI引擎
        self.ai_engine = NeuralFiveAI(self.settings.ai_difficulty)
        
        # 如果AI先手，开始AI思考
        if self.settings.ai_color == "black":
            self._start_ai_thinking()
    
    def undo_move(self) -> None:
        """撤销移动"""
        if self.game_state:
            self.game_state.undo_move()
    
    def _start_ai_thinking(self) -> None:
        """开始AI思考"""
        if self.ai_thinking or not self.ai_engine:
            return
        
        self.ai_thinking = True
        self.game_state.status = GameStatus.AI_THINKING
        
        # 启动AI线程
        self.ai_thread = threading.Thread(target=self._ai_worker)
        self.ai_thread.daemon = True
        self.ai_thread.start()
    
    def _ai_worker(self) -> None:
        """AI工作线程"""
        try:
            move = self.ai_engine.get_best_move(self.settings.ai_color)
            self.ai_move_result = move
        except Exception as e:
            print(f"AI计算错误: {e}")
            self.ai_move_result = None
    
    def _update_ai_thread(self) -> None:
        """更新AI线程状态"""
        if self.ai_thinking and self.ai_thread and not self.ai_thread.is_alive():
            self.ai_thinking = False
            
            if self.ai_move_result and self.game_state:
                # AI落子
                move = self.ai_move_result
                self.game_state.make_move(move.row, move.col, self.settings.ai_color)
                self.game_state.status = GameStatus.PLAYING
            
            self.ai_move_result = None
    
    def _add_hover_effect(self, pos: Tuple[int, int]) -> None:
        """添加悬停效果"""
        # 这里可以添加粒子效果或其他视觉反馈
        pass
    
    def _render(self) -> None:
        """渲染界面"""
        # 清空屏幕
        self.screen.fill(COLORS['BACKGROUND'])
        
        if self.current_screen == "menu":
            self._render_menu()
        elif self.current_screen == "game":
            self._render_game()
    
    def _render_menu(self) -> None:
        """渲染主菜单"""
        # 标题
        title_text = self.fonts['title'].render(
            self.texts['title'], True, COLORS['BLACK']
        )
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
        self.screen.blit(title_text, title_rect)
        
        # 副标题
        subtitle_text = self.fonts['large'].render(
            self.texts['subtitle'], True, COLORS['GRAY']
        )
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, 180))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # 颜色选择
        color_text = self.fonts['large'].render(
            self.texts['choose_color'], True, COLORS['BLACK']
        )
        color_rect = color_text.get_rect(center=(WINDOW_WIDTH // 2, 280))
        self.screen.blit(color_text, color_rect)
        
        # 颜色按钮
        self._render_button(
            self.ui_elements.black_button,
            self.texts['black'],
            COLORS['BLACK'],
            COLORS['WHITE']
        )
        
        self._render_button(
            self.ui_elements.white_button,
            self.texts['white'],
            COLORS['WHITE'],
            COLORS['BLACK']
        )
        
        # 难度选择
        difficulty_text = self.fonts['large'].render(
            self.texts['choose_difficulty'], True, COLORS['BLACK']
        )
        difficulty_rect = difficulty_text.get_rect(center=(WINDOW_WIDTH // 2, 410))
        self.screen.blit(difficulty_text, difficulty_rect)
        
        # 难度按钮
        difficulties = ["easy", "medium", "hard", "expert"]
        for i, button in enumerate(self.ui_elements.difficulty_buttons):
            is_selected = self.settings.ai_difficulty == difficulties[i]
            self._render_button(
                button,
                self.texts[difficulties[i]],
                COLORS['BLUE'] if is_selected else COLORS['LIGHT_GRAY'],
                COLORS['WHITE']
            )
    
    def _render_game(self) -> None:
        """渲染游戏界面"""
        if not self.game_state:
            return
        
        # 绘制棋盘
        self._render_board()
        
        # 绘制棋子
        self._render_pieces()
        
        # 绘制信息面板
        self._render_info_panel()
        
        # 绘制按钮
        self._render_game_buttons()
        
        # 绘制状态信息
        self._render_status_panel()
    
    def _render_board(self) -> None:
        """渲染棋盘"""
        # 棋盘背景
        board_rect = pygame.Rect(
            BOARD_START_X - 25,
            BOARD_START_Y - 25,
            BOARD_WIDTH + 50,
            BOARD_WIDTH + 50
        )
        
        pygame.draw.rect(self.screen, COLORS['BROWN'], board_rect, border_radius=8)
        pygame.draw.rect(self.screen, COLORS['DARK_BROWN'], board_rect, 3, border_radius=8)
        
        # 网格线
        for i in range(BOARD_SIZE):
            # 横线
            start_pos = (BOARD_START_X, BOARD_START_Y + i * CELL_SIZE)
            end_pos = (BOARD_START_X + BOARD_WIDTH, BOARD_START_Y + i * CELL_SIZE)
            pygame.draw.line(self.screen, COLORS['BLACK'], start_pos, end_pos, 1)
            
            # 竖线
            start_pos = (BOARD_START_X + i * CELL_SIZE, BOARD_START_Y)
            end_pos = (BOARD_START_X + i * CELL_SIZE, BOARD_START_Y + BOARD_WIDTH)
            pygame.draw.line(self.screen, COLORS['BLACK'], start_pos, end_pos, 1)
        
        # 星位
        star_points = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
        for row, col in star_points:
            x = BOARD_START_X + col * CELL_SIZE
            y = BOARD_START_Y + row * CELL_SIZE
            pygame.draw.circle(self.screen, COLORS['BLACK'], (x, y), 4)
    
    def _render_pieces(self) -> None:
        """渲染棋子"""
        if not self.game_state:
            return
        
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.game_state.board[row, col]
                
                if piece == 0:  # 空位
                    continue
                
                x = BOARD_START_X + col * CELL_SIZE
                y = BOARD_START_Y + row * CELL_SIZE
                
                if piece == 1:  # 黑子
                    pygame.draw.circle(self.screen, COLORS['BLACK'], (x, y), 15)
                else:  # 白子
                    pygame.draw.circle(self.screen, COLORS['WHITE'], (x, y), 15)
                    pygame.draw.circle(self.screen, COLORS['BLACK'], (x, y), 15, 1)
        
        # 标记最后一手
        if self.game_state.move_history:
            last_move = self.game_state.move_history[-1]
            x = BOARD_START_X + last_move['col'] * CELL_SIZE
            y = BOARD_START_Y + last_move['row'] * CELL_SIZE
            pygame.draw.circle(self.screen, COLORS['RED'], (x, y), 5)
    
    def _render_info_panel(self) -> None:
        """渲染信息面板"""
        # 面板背景
        pygame.draw.rect(self.screen, COLORS['PANEL'], self.ui_elements.info_panel)
        pygame.draw.rect(self.screen, COLORS['GRAY'], self.ui_elements.info_panel, 2)
        
        # 标题
        title_text = self.fonts['large'].render(
            self.texts['game_info'], True, COLORS['BLACK']
        )
        self.screen.blit(title_text, (self.ui_elements.info_panel.x + 10, 
                                     self.ui_elements.info_panel.y + 10))
        
        # 游戏信息
        if self.game_state:
            info = self.game_state.get_game_info()
            
            # 当前玩家
            current_text = self.fonts['normal'].render(
                f"{self.texts['your_turn']}: {info['current_player']}", 
                True, COLORS['BLACK']
            )
            self.screen.blit(current_text, (self.ui_elements.info_panel.x + 10,
                                            self.ui_elements.info_panel.y + 50))
            
            # 步数
            moves_text = self.fonts['normal'].render(
                f"{self.texts['move_count']}: {info['move_count']}", 
                True, COLORS['BLACK']
            )
            self.screen.blit(moves_text, (self.ui_elements.info_panel.x + 10,
                                        self.ui_elements.info_panel.y + 80))
            
            # AI等级
            level_text = self.fonts['normal'].render(
                f"{self.texts['ai_level']}: {self.settings.ai_difficulty}", 
                True, COLORS['BLACK']
            )
            self.screen.blit(level_text, (self.ui_elements.info_panel.x + 10,
                                        self.ui_elements.info_panel.y + 110))
    
    def _render_game_buttons(self) -> None:
        """渲染游戏按钮"""
        # 重新开始按钮
        self._render_button(
            self.ui_elements.restart_button,
            self.texts['restart'],
            COLORS['GREEN'],
            COLORS['WHITE']
        )
        
        # 撤销按钮
        undo_enabled = (self.game_state and 
                       self.game_state.move_history and 
                       not self.ai_thinking)
        
        self._render_button(
            self.ui_elements.undo_button,
            self.texts['undo'],
            COLORS['BLUE'] if undo_enabled else COLORS['GRAY'],
            COLORS['WHITE']
        )
        
        # 菜单按钮
        self._render_button(
            self.ui_elements.menu_button,
            self.texts['menu'],
            COLORS['ORANGE'],
            COLORS['WHITE']
        )
    
    def _render_status_panel(self) -> None:
        """渲染状态面板"""
        # 面板背景
        pygame.draw.rect(self.screen, COLORS['PANEL'], self.ui_elements.status_panel)
        pygame.draw.rect(self.screen, COLORS['GRAY'], self.ui_elements.status_panel, 2)
        
        # 标题
        status_text = self.fonts['large'].render(
            self.texts['tips'], True, COLORS['BLACK']
        )
        self.screen.blit(status_text, (self.ui_elements.status_panel.x + 10,
                                      self.ui_elements.status_panel.y + 10))
        
        # 状态信息
        tips = [self.texts['tip1'], self.texts['tip2'], self.texts['tip3']]
        
        for i, tip in enumerate(tips):
            tip_text = self.fonts['small'].render(tip, True, COLORS['GRAY'])
            self.screen.blit(tip_text, (self.ui_elements.status_panel.x + 10,
                                      self.ui_elements.status_panel.y + 50 + i * 25))
        
        # AI思考状态
        if self.ai_thinking:
            thinking_text = self.fonts['normal'].render(
                self.texts['ai_thinking'], True, COLORS['RED']
            )
            self.screen.blit(thinking_text, (self.ui_elements.status_panel.x + 10,
                                           self.ui_elements.status_panel.y + 120))
    
    def _render_button(self, rect: pygame.Rect, text: str, 
                      bg_color: Tuple[int, int, int], 
                      text_color: Tuple[int, int, int]) -> None:
        """渲染按钮"""
        # 按钮背景
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=5)
        pygame.draw.rect(self.screen, COLORS['BLACK'], rect, 2, border_radius=5)
        
        # 按钮文字
        text_surface = self.fonts['normal'].render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def _cleanup(self) -> None:
        """清理资源"""
        if self.ai_thread and self.ai_thread.is_alive():
            # 注意：Python线程无法强制终止，这里只是等待
            self.ai_thread.join(timeout=1.0)
        
        pygame.quit()
        sys.exit()

def main():
    """主函数"""
    try:
        gui = NeuralFiveGUI()
        gui.run()
    except KeyboardInterrupt:
        print("\n游戏被用户中断")
    except Exception as e:
        print(f"游戏运行错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
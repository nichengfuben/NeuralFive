"""
游戏界面

提供游戏进行中的界面，包括棋盘、侧边栏、控制按钮等
"""

import pygame
from typing import TYPE_CHECKING, Optional, Tuple

if TYPE_CHECKING:
    from .game_window import GameWindow


class GameUI:
    """游戏界面类"""
    
    def __init__(self, game_window: 'GameWindow'):
        """
        初始化游戏界面
        
        Args:
            game_window: 游戏窗口实例
        """
        self.game_window = game_window
        self.screen = game_window.screen
        self.colors = game_window.colors
        
        # 棋盘设置
        self.board_size = 15
        self.cell_size = 40
        self.board_start_x = 50
        self.board_start_y = 80
        self.board_width = self.cell_size * (self.board_size - 1)
        
        # 按钮定义
        self.restart_button = pygame.Rect(640, 280, 230, 45)
        self.menu_button = pygame.Rect(640, 340, 230, 45)
        self.settings_button = pygame.Rect(640, 400, 230, 45)
        
        # 鼠标悬停位置
        self.hover_pos: Optional[Tuple[int, int]] = None
    
    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            if self.restart_button.collidepoint(pos):
                self.game_window.reset_game()
                self.game_window.start_game('black')  # 默认黑棋开始
            elif self.menu_button.collidepoint(pos):
                self.game_window.reset_game()
                self.game_window.switch_ui('menu')
            elif self.settings_button.collidepoint(pos):
                self.game_window.switch_ui('settings')
            else:
                # 处理棋盘点击
                board_pos = self._get_board_pos(pos)
                if board_pos:
                    row, col = board_pos
                    self.game_window.make_player_move(row, col)
        
        elif event.type == pygame.MOUSEMOTION:
            # 更新鼠标悬停位置
            self.hover_pos = self._get_board_pos(event.pos)
    
    def _get_board_pos(self, mouse_pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """将鼠标位置转换为棋盘坐标"""
        x, y = mouse_pos
        col = round((x - self.board_start_x) / self.cell_size)
        row = round((y - self.board_start_y) / self.cell_size)
        
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            board_x = self.board_start_x + col * self.cell_size
            board_y = self.board_start_y + row * self.cell_size
            distance = ((x - board_x) ** 2 + (y - board_y) ** 2) ** 0.5
            if distance <= self.cell_size // 2:
                return row, col
        return None
    
    def draw(self):
        """绘制游戏界面"""
        self._draw_board()
        self._draw_stones()
        self._draw_hover()
        self._draw_sidebar()
        
        # 如果游戏结束，绘制获胜信息
        if self.game_window.game_state.status.value == 'game_over':
            self._draw_winner()
    
    def _draw_board(self):
        """绘制棋盘"""
        # 绘制棋盘背景
        board_rect = pygame.Rect(
            self.board_start_x - 25,
            self.board_start_y - 25,
            self.board_width + 50,
            self.board_width + 50
        )
        pygame.draw.rect(self.screen, self.colors['brown'], board_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.colors['dark_brown'], board_rect, 3, border_radius=5)
        
        # 绘制网格线
        for i in range(self.board_size):
            # 横线
            start_pos = (self.board_start_x, self.board_start_y + i * self.cell_size)
            end_pos = (self.board_start_x + self.board_width, self.board_start_y + i * self.cell_size)
            pygame.draw.line(self.screen, self.colors['black'], start_pos, end_pos, 1)
            
            # 竖线
            start_pos = (self.board_start_x + i * self.cell_size, self.board_start_y)
            end_pos = (self.board_start_x + i * self.cell_size, self.board_start_y + self.board_width)
            pygame.draw.line(self.screen, self.colors['black'], start_pos, end_pos, 1)
        
        # 绘制星位
        star_points = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
        for row, col in star_points:
            x = self.board_start_x + col * self.cell_size
            y = self.board_start_y + row * self.cell_size
            pygame.draw.circle(self.screen, self.colors['black'], (x, y), 4)
        
        # 绘制坐标标签
        self._draw_coordinates()
    
    def _draw_coordinates(self):
        """绘制坐标标签"""
        for i in range(self.board_size):
            # 横坐标 A-O
            label = chr(65 + i)
            text = self.game_window.small_font.render(label, True, self.colors['dark_brown'])
            x = self.board_start_x + i * self.cell_size - text.get_width() // 2
            y = self.board_start_y + self.board_width + 10
            self.screen.blit(text, (x, y))
            
            # 纵坐标 1-15
            label = str(15 - i)
            text = self.game_window.small_font.render(label, True, self.colors['dark_brown'])
            x = self.board_start_x - 30
            y = self.board_start_y + i * self.cell_size - text.get_height() // 2
            self.screen.blit(text, (x, y))
    
    def _draw_stones(self):
        """绘制棋子"""
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.game_window.board.board[row][col]:
                    x = self.board_start_x + col * self.cell_size
                    y = self.board_start_y + row * self.cell_size
                    
                    # 绘制阴影
                    shadow_surf = pygame.Surface((self.cell_size * 2, self.cell_size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(shadow_surf, (0, 0, 0, 40), 
                                     (self.cell_size, self.cell_size), self.cell_size // 2 - 2)
                    self.screen.blit(shadow_surf, (x - self.cell_size + 3, y - self.cell_size + 3))
                    
                    # 绘制棋子
                    if self.game_window.board.board[row][col] == 1:  # 黑子
                        pygame.draw.circle(self.screen, self.colors['black'], (x, y), self.cell_size // 2 - 2)
                        pygame.draw.circle(self.screen, (50, 50, 50), 
                                         (x - 5, y - 5), self.cell_size // 4, 2)
                    else:  # 白子
                        pygame.draw.circle(self.screen, self.colors['white'], (x, y), self.cell_size // 2 - 2)
                        pygame.draw.circle(self.screen, (80, 80, 80), (x, y), self.cell_size // 2 - 2, 1)
                        pygame.draw.circle(self.screen, (245, 245, 245), 
                                         (x - 5, y - 5), self.cell_size // 4, 2)
                    
                    # 标记最后一步
                    if (self.game_window.board.last_move == (row, col) and 
                        self.game_window.game_state.move_history):
                        color = self.colors['red'] if self.game_window.board.board[row][col] == 1 else self.colors['orange']
                        pygame.draw.rect(self.screen, color, 
                                       (x - 5, y - 5, 10, 10), 2)
    
    def _draw_hover(self):
        """绘制鼠标悬停效果"""
        if (self.hover_pos and 
            self.game_window.game_state.status.value == 'playing' and 
            not self.game_window.ai_thinking):
            row, col = self.hover_pos
            if (0 <= row < self.board_size and 0 <= col < self.board_size and 
                not self.game_window.board.board[row][col]):
                if self.game_window.game_state.current_player == self.game_window.game_state.current_player:
                    x = self.board_start_x + col * self.cell_size
                    y = self.board_start_y + row * self.cell_size
                    
                    # 半透明预览
                    s = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
                    color = (0, 0, 0, 80) if self.game_window.game_state.current_player == "black" else (255, 255, 255, 80)
                    pygame.draw.circle(s, color, (self.cell_size // 2, self.cell_size // 2), self.cell_size // 2 - 2)
                    self.screen.blit(s, (x - self.cell_size // 2, y - self.cell_size // 2))
                    
                    # 十字准星
                    pygame.draw.line(self.screen, self.colors['red'], (x - 10, y), (x + 10, y), 1)
                    pygame.draw.line(self.screen, self.colors['red'], (x, y - 10), (x, y + 10), 1)
    
    def _draw_sidebar(self):
        """绘制侧边栏信息"""
        # 侧边栏背景
        sidebar_rect = pygame.Rect(620, 80, 260, 540)
        pygame.draw.rect(self.screen, self.colors['white'], sidebar_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.colors['gray'], sidebar_rect, 2, border_radius=10)
        
        # 游戏信息标题
        title = self.game_window.font.render(
            self.game_window.get_text('info'), True, self.colors['black']
        )
        title_rect = title.get_rect(center=(750, 110))
        self.screen.blit(title, title_rect)
        
        pygame.draw.line(self.screen, self.colors['gray'], (640, 135), (860, 135), 1)
        
        # 当前状态
        self._draw_current_status()
        
        # 按钮
        self._draw_buttons()
        
        # 游戏提示
        self._draw_tips()
    
    def _draw_current_status(self):
        """绘制当前状态"""
        y_offset = 155
        
        # 显示当前状态
        if not self.game_window.ai_thinking:
            if self.game_window.game_state.current_player == 'black':
                status_text = self.game_window.get_text('black_move')
                status_color = self.colors['black']
            else:
                status_text = self.game_window.get_text('white_move')
                status_color = self.colors['black']
        else:
            dots = "." * self.game_window.thinking_dots
            status_text = self.game_window.get_text('ai_thinking') + dots
            status_color = self.colors['orange']
        
        text = self.game_window.font.render(status_text, True, status_color)
        self.screen.blit(text, (640, y_offset))
        
        # 当前执子方
        y_offset += 35
        if self.game_window.game_state.current_player == "black":
            pygame.draw.circle(self.screen, self.colors['black'], (660, y_offset + 10), 9)
        else:
            pygame.draw.circle(self.screen, self.colors['white'], (660, y_offset + 10), 9)
            pygame.draw.circle(self.screen, self.colors['black'], (660, y_offset + 10), 9, 1)
    
    def _draw_buttons(self):
        """绘制控制按钮"""
        mouse_pos = pygame.mouse.get_pos()
        
        # 重新开始按钮
        self._draw_sidebar_button(
            self.restart_button,
            self.game_window.get_text('restart'),
            self.colors['green'],
            mouse_pos
        )
        
        # 返回菜单按钮
        self._draw_sidebar_button(
            self.menu_button,
            self.game_window.get_text('menu'),
            self.colors['blue'],
            mouse_pos
        )
        
        # 设置按钮
        self._draw_sidebar_button(
            self.settings_button,
            "设置" if self.game_window.language == 'zh' else "Settings",
            self.colors['orange'],
            mouse_pos
        )
    
    def _draw_sidebar_button(self, rect: pygame.Rect, text: str, color: tuple, mouse_pos: tuple):
        """绘制侧边栏按钮"""
        hover = rect.collidepoint(mouse_pos)
        bg_color = (240, 240, 240) if hover else self.colors['white']
        
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=5)
        pygame.draw.rect(self.screen, color, rect, 2, border_radius=5)
        
        text_surface = self.game_window.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def _draw_tips(self):
        """绘制游戏提示"""
        y_offset = 400
        pygame.draw.line(self.screen, self.colors['light_gray'], (640, y_offset), (860, y_offset), 1)
        
        y_offset += 20
        text = self.game_window.small_font.render(
            self.game_window.get_text('tips'), True, self.colors['black']
        )
        self.screen.blit(text, (640, y_offset))
        
        tips = [
            self.game_window.get_text('tip1'),
            self.game_window.get_text('tip2'),
            self.game_window.get_text('tip3')
        ]
        
        y_offset += 25
        for tip in tips:
            text = self.game_window.small_font.render(tip, True, self.colors['gray'])
            self.screen.blit(text, (640, y_offset))
            y_offset += 22
    
    def _draw_winner(self):
        """绘制获胜信息"""
        result = self.game_window.game_state.get_game_result()
        if not result or not result.winner:
            return
        
        # 半透明遮罩
        overlay = pygame.Surface((self.game_window.width, self.game_window.height))
        overlay.set_alpha(180)
        overlay.fill(self.colors['black'])
        self.screen.blit(overlay, (0, 0))
        
        # 动画效果
        scale = 1 + 0.2 * abs(pygame.math.Vector2(0, 1).rotate(self.game_window.animation_time * 100).y)
        
        # 结果框
        box_rect = pygame.Rect(250, 250, 400, 200)
        pygame.draw.rect(self.screen, self.colors['white'], box_rect, border_radius=20)
        
        # 显示结果
        if result.winner == 'black':
            text = self.game_window.get_text('win') if self.game_window.game_state.player_types['black'] == 'human' else self.game_window.get_text('lose')
            color = self.colors['green']
            border_color = self.colors['gold']
        else:
            text = self.game_window.get_text('win') if self.game_window.game_state.player_types['white'] == 'human' else self.game_window.get_text('lose')
            color = self.colors['green']
            border_color = self.colors['gold']
        
        pygame.draw.rect(self.screen, border_color, box_rect, 5, border_radius=20)
        
        # 文字
        win_text = self.game_window.large_font.render(text, True, color)
        win_rect = win_text.get_rect(center=(450, 330))
        self.screen.blit(win_text, win_rect)
        
        # 提示
        hint = self.game_window.small_font.render("Click button to continue", True, self.colors['gray'])
        hint_rect = hint.get_rect(center=(450, 380))
        self.screen.blit(hint, hint_rect)

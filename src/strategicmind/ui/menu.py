"""
主菜单界面

提供游戏开始、设置、退出等功能
"""

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_window import GameWindow


class MainMenu:
    """主菜单类"""
    
    def __init__(self, game_window: 'GameWindow'):
        """
        初始化主菜单
        
        Args:
            game_window: 游戏窗口实例
        """
        self.game_window = game_window
        self.screen = game_window.screen
        self.colors = game_window.colors
        
        # 按钮定义
        self.black_button = pygame.Rect(270, 350, 150, 55)
        self.white_button = pygame.Rect(480, 350, 150, 55)
        self.settings_button = pygame.Rect(375, 450, 150, 45)
        self.quit_button = pygame.Rect(375, 510, 150, 45)
    
    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            if self.black_button.collidepoint(pos):
                self.game_window.start_game('black')
            elif self.white_button.collidepoint(pos):
                self.game_window.start_game('white')
            elif self.settings_button.collidepoint(pos):
                self.game_window.switch_ui('settings')
            elif self.quit_button.collidepoint(pos):
                pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def draw(self):
        """绘制主菜单"""
        # 标题背景
        title_bg = pygame.Rect(200, 100, 500, 120)
        pygame.draw.rect(self.screen, self.colors['white'], title_bg, border_radius=15)
        pygame.draw.rect(self.screen, self.colors['dark_brown'], title_bg, 3, border_radius=15)
        
        # 标题
        title = self.game_window.title_font.render(
            self.game_window.get_text('title'), True, self.colors['dark_brown']
        )
        title_rect = title.get_rect(center=(self.game_window.width // 2, 160))
        self.screen.blit(title, title_rect)
        
        # 副标题
        subtitle = self.game_window.font.render(
            self.game_window.get_text('subtitle'), True, self.colors['gray']
        )
        subtitle_rect = subtitle.get_rect(center=(self.game_window.width // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # 提示文字
        prompt = self.game_window.large_font.render(
            self.game_window.get_text('choose'), True, self.colors['black']
        )
        prompt_rect = prompt.get_rect(center=(self.game_window.width // 2, 290))
        self.screen.blit(prompt, prompt_rect)
        
        # 按钮
        mouse_pos = pygame.mouse.get_pos()
        
        # 黑棋按钮
        self._draw_button(
            self.black_button, 
            self.game_window.get_text('black'),
            self.colors['black'],
            mouse_pos
        )
        
        # 白棋按钮
        self._draw_button(
            self.white_button,
            self.game_window.get_text('white'),
            self.colors['white'],
            mouse_pos,
            border_color=self.colors['black']
        )
        
        # 设置按钮
        self._draw_button(
            self.settings_button,
            "设置" if self.game_window.language == 'zh' else "Settings",
            self.colors['blue'],
            mouse_pos
        )
        
        # 退出按钮
        self._draw_button(
            self.quit_button,
            "退出" if self.game_window.language == 'zh' else "Quit",
            self.colors['red'],
            mouse_pos
        )
        
        # 规则说明
        self._draw_rules()
    
    def _draw_button(self, rect: pygame.Rect, text: str, color: tuple, 
                    mouse_pos: tuple, border_color: tuple = None):
        """绘制按钮"""
        hover = rect.collidepoint(mouse_pos)
        bg_color = (240, 240, 240) if hover else self.colors['white']
        border_color = border_color or color
        
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=10)
        pygame.draw.rect(self.screen, border_color, rect, 3 if hover else 2, border_radius=10)
        
        # 绘制棋子图标（仅对黑白按钮）
        if rect in [self.black_button, self.white_button]:
            circle_pos = (rect.x + 35, rect.centery)
            pygame.draw.circle(self.screen, color, circle_pos, 16)
            if color == self.colors['white']:
                pygame.draw.circle(self.screen, self.colors['black'], circle_pos, 16, 2)
        
        # 绘制文字
        text_surface = self.game_window.large_font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def _draw_rules(self):
        """绘制规则说明"""
        y_offset = 450
        rules = [
            self.game_window.get_text('rules'),
            self.game_window.get_text('rule1'),
            self.game_window.get_text('rule2'),
            self.game_window.get_text('rule3')
        ]
        
        for rule in rules:
            text = self.game_window.small_font.render(rule, True, self.colors['gray'])
            rect = text.get_rect(center=(self.game_window.width // 2, y_offset))
            self.screen.blit(text, rect)
            y_offset += 28

"""
设置界面

提供游戏设置功能，包括AI难度、语言、音效等
"""

import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game_window import GameWindow


class SettingsUI:
    """设置界面类"""
    
    def __init__(self, game_window: 'GameWindow'):
        """
        初始化设置界面
        
        Args:
            game_window: 游戏窗口实例
        """
        self.game_window = game_window
        self.screen = game_window.screen
        self.colors = game_window.colors
        
        # 按钮定义
        self.back_button = pygame.Rect(50, 50, 120, 40)
        self.language_button = pygame.Rect(300, 200, 200, 50)
        self.difficulty_button = pygame.Rect(300, 280, 200, 50)
        self.animation_button = pygame.Rect(300, 360, 200, 50)
        self.sound_button = pygame.Rect(300, 440, 200, 50)
        
        # 设置选项
        self.languages = ['zh', 'en']
        self.difficulties = ['easy', 'medium', 'hard', 'expert']
        self.current_language = 0
        self.current_difficulty = 2  # 默认hard
    
    def handle_event(self, event: pygame.event.Event):
        """处理事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            if self.back_button.collidepoint(pos):
                self.game_window.switch_ui('menu')
            elif self.language_button.collidepoint(pos):
                self.current_language = (self.current_language + 1) % len(self.languages)
                self.game_window.set_language(self.languages[self.current_language])
            elif self.difficulty_button.collidepoint(pos):
                self.current_difficulty = (self.current_difficulty + 1) % len(self.difficulties)
                self.game_window.game_state.set_ai_difficulty(self.difficulties[self.current_difficulty])
            elif self.animation_button.collidepoint(pos):
                self.game_window.game_state.enable_animations = not self.game_window.game_state.enable_animations
            elif self.sound_button.collidepoint(pos):
                self.game_window.game_state.sound_enabled = not self.game_window.game_state.sound_enabled
    
    def draw(self):
        """绘制设置界面"""
        # 标题
        title = self.game_window.title_font.render(
            "设置" if self.game_window.language == 'zh' else "Settings", 
            True, self.colors['black']
        )
        title_rect = title.get_rect(center=(self.game_window.width // 2, 100))
        self.screen.blit(title, title_rect)
        
        # 返回按钮
        self._draw_button(
            self.back_button,
            "← 返回" if self.game_window.language == 'zh' else "← Back",
            self.colors['blue']
        )
        
        # 设置选项
        self._draw_setting_option(
            self.language_button,
            "语言" if self.game_window.language == 'zh' else "Language",
            "中文" if self.languages[self.current_language] == 'zh' else "English"
        )
        
        self._draw_setting_option(
            self.difficulty_button,
            "AI难度" if self.game_window.language == 'zh' else "AI Difficulty",
            self.difficulties[self.current_difficulty].title()
        )
        
        self._draw_setting_option(
            self.animation_button,
            "动画效果" if self.game_window.language == 'zh' else "Animations",
            "开启" if self.game_window.game_state.enable_animations else "关闭"
        )
        
        self._draw_setting_option(
            self.sound_button,
            "音效" if self.game_window.language == 'zh' else "Sound",
            "开启" if self.game_window.game_state.sound_enabled else "关闭"
        )
        
        # 说明文字
        self._draw_description()
    
    def _draw_button(self, rect: pygame.Rect, text: str, color: tuple):
        """绘制按钮"""
        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)
        bg_color = (240, 240, 240) if hover else self.colors['white']
        
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=5)
        pygame.draw.rect(self.screen, color, rect, 2, border_radius=5)
        
        text_surface = self.game_window.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
    
    def _draw_setting_option(self, rect: pygame.Rect, label: str, value: str):
        """绘制设置选项"""
        mouse_pos = pygame.mouse.get_pos()
        hover = rect.collidepoint(mouse_pos)
        bg_color = (240, 240, 240) if hover else self.colors['white']
        
        pygame.draw.rect(self.screen, bg_color, rect, border_radius=5)
        pygame.draw.rect(self.screen, self.colors['gray'], rect, 2, border_radius=5)
        
        # 标签
        label_surface = self.game_window.font.render(label, True, self.colors['black'])
        label_rect = label_surface.get_rect(center=(rect.x - 100, rect.centery))
        self.screen.blit(label_surface, label_rect)
        
        # 值
        value_surface = self.game_window.font.render(value, True, self.colors['blue'])
        value_rect = value_surface.get_rect(center=rect.center)
        self.screen.blit(value_surface, value_rect)
        
        # 箭头
        arrow = "▶" if hover else "▶"
        arrow_surface = self.game_window.font.render(arrow, True, self.colors['gray'])
        arrow_rect = arrow_surface.get_rect(center=(rect.right - 20, rect.centery))
        self.screen.blit(arrow_surface, arrow_rect)
    
    def _draw_description(self):
        """绘制说明文字"""
        y_offset = 550
        descriptions = [
            "StrategicMind - 智能策略游戏引擎",
            "基于深度搜索算法的高性能AI",
            "支持多种难度和自定义设置"
        ] if self.game_window.language == 'zh' else [
            "StrategicMind - Intelligent Strategy Game Engine",
            "High-performance AI based on deep search algorithms",
            "Supports multiple difficulties and custom settings"
        ]
        
        for desc in descriptions:
            text = self.game_window.small_font.render(desc, True, self.colors['gray'])
            text_rect = text.get_rect(center=(self.game_window.width // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 25

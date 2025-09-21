"""
配置管理模块

提供游戏配置的加载、保存和管理功能
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class GameConfig:
    """游戏配置类"""
    # AI设置
    ai_difficulty: str = "hard"
    search_depth: int = 100
    max_thinking_time: float = 5.0
    
    # 界面设置
    language: str = "zh"
    enable_animations: bool = True
    sound_enabled: bool = True
    window_width: int = 900
    window_height: int = 700
    
    # 游戏设置
    board_size: int = 15
    enable_forbidden_moves: bool = False
    
    # 性能设置
    enable_performance_monitoring: bool = True
    log_level: str = "INFO"


class Config:
    """配置管理类"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = GameConfig()
        self.load()
    
    def load(self) -> bool:
        """
        加载配置文件
        
        Returns:
            是否加载成功
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.config = GameConfig(**data)
                return True
        except Exception as e:
            print(f"加载配置文件失败: {e}")
        return False
    
    def save(self) -> bool:
        """
        保存配置文件
        
        Returns:
            是否保存成功
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.config), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
        return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键
            default: 默认值
            
        Returns:
            配置值
        """
        return getattr(self.config, key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """
        设置配置值
        
        Args:
            key: 配置键
            value: 配置值
            
        Returns:
            是否设置成功
        """
        try:
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                return True
        except Exception as e:
            print(f"设置配置失败: {e}")
        return False
    
    def update(self, **kwargs) -> bool:
        """
        批量更新配置
        
        Args:
            **kwargs: 配置键值对
            
        Returns:
            是否更新成功
        """
        try:
            for key, value in kwargs.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
            return True
        except Exception as e:
            print(f"更新配置失败: {e}")
        return False
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有配置"""
        return asdict(self.config)
    
    def reset_to_default(self):
        """重置为默认配置"""
        self.config = GameConfig()
    
    def validate(self) -> bool:
        """验证配置有效性"""
        try:
            # 验证AI难度
            valid_difficulties = ['easy', 'medium', 'hard', 'expert']
            if self.config.ai_difficulty not in valid_difficulties:
                self.config.ai_difficulty = 'hard'
            
            # 验证搜索深度
            if not (1 <= self.config.search_depth <= 200):
                self.config.search_depth = 100
            
            # 验证语言
            valid_languages = ['zh', 'en']
            if self.config.language not in valid_languages:
                self.config.language = 'zh'
            
            # 验证棋盘大小
            if not (5 <= self.config.board_size <= 25):
                self.config.board_size = 15
            
            # 验证窗口大小
            if self.config.window_width < 600:
                self.config.window_width = 900
            if self.config.window_height < 400:
                self.config.window_height = 700
            
            return True
        except Exception:
            return False

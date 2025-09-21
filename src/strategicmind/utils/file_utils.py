"""
文件操作工具模块

提供文件操作相关的实用函数
"""

import os
import json
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class FileUtils:
    """文件操作工具类"""
    
    @staticmethod
    def ensure_dir(directory: Union[str, Path]) -> bool:
        """
        确保目录存在
        
        Args:
            directory: 目录路径
            
        Returns:
            是否成功创建或目录已存在
        """
        try:
            Path(directory).mkdir(parents=True, exist_ok=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def read_json(file_path: Union[str, Path]) -> Optional[Dict[str, Any]]:
        """
        读取JSON文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            JSON数据或None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return None
    
    @staticmethod
    def write_json(data: Dict[str, Any], file_path: Union[str, Path]) -> bool:
        """
        写入JSON文件
        
        Args:
            data: 要写入的数据
            file_path: 文件路径
            
        Returns:
            是否写入成功
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    @staticmethod
    def read_pickle(file_path: Union[str, Path]) -> Optional[Any]:
        """
        读取Pickle文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            反序列化数据或None
        """
        try:
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None
    
    @staticmethod
    def write_pickle(data: Any, file_path: Union[str, Path]) -> bool:
        """
        写入Pickle文件
        
        Args:
            data: 要写入的数据
            file_path: 文件路径
            
        Returns:
            是否写入成功
        """
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(data, f)
            return True
        except Exception:
            return False
    
    @staticmethod
    def read_text(file_path: Union[str, Path]) -> Optional[str]:
        """
        读取文本文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件内容或None
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception:
            return None
    
    @staticmethod
    def write_text(content: str, file_path: Union[str, Path]) -> bool:
        """
        写入文本文件
        
        Args:
            content: 文件内容
            file_path: 文件路径
            
        Returns:
            是否写入成功
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception:
            return False
    
    @staticmethod
    def file_exists(file_path: Union[str, Path]) -> bool:
        """
        检查文件是否存在
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件是否存在
        """
        return Path(file_path).exists()
    
    @staticmethod
    def get_file_size(file_path: Union[str, Path]) -> int:
        """
        获取文件大小
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件大小（字节）
        """
        try:
            return Path(file_path).stat().st_size
        except Exception:
            return 0
    
    @staticmethod
    def list_files(directory: Union[str, Path], pattern: str = "*") -> List[Path]:
        """
        列出目录中的文件
        
        Args:
            directory: 目录路径
            pattern: 文件模式
            
        Returns:
            文件路径列表
        """
        try:
            return list(Path(directory).glob(pattern))
        except Exception:
            return []
    
    @staticmethod
    def backup_file(file_path: Union[str, Path]) -> bool:
        """
        备份文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否备份成功
        """
        try:
            path = Path(file_path)
            if not path.exists():
                return False
            
            backup_path = path.with_suffix(f"{path.suffix}.backup")
            path.rename(backup_path)
            return True
        except Exception:
            return False

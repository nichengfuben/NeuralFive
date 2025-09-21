"""
性能监控模块

提供性能监控和统计功能
"""

import time
import psutil
from typing import Dict, Any, Optional
from collections import defaultdict


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        """初始化性能监控器"""
        self.start_time = time.time()
        self.metrics = defaultdict(list)
        self.current_operations = {}
    
    def start_operation(self, operation_name: str) -> str:
        """
        开始监控操作
        
        Args:
            operation_name: 操作名称
            
        Returns:
            操作ID
        """
        operation_id = f"{operation_name}_{int(time.time() * 1000)}"
        self.current_operations[operation_id] = {
            'name': operation_name,
            'start_time': time.time(),
            'start_memory': psutil.Process().memory_info().rss
        }
        return operation_id
    
    def end_operation(self, operation_id: str) -> Dict[str, Any]:
        """
        结束监控操作
        
        Args:
            operation_id: 操作ID
            
        Returns:
            操作统计信息
        """
        if operation_id not in self.current_operations:
            return {}
        
        operation = self.current_operations.pop(operation_id)
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss
        
        stats = {
            'name': operation['name'],
            'duration': end_time - operation['start_time'],
            'memory_used': end_memory - operation['start_memory'],
            'end_time': end_time
        }
        
        self.metrics[operation['name']].append(stats)
        return stats
    
    def get_system_info(self) -> Dict[str, Any]:
        """获取系统信息"""
        process = psutil.Process()
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'memory_used_mb': process.memory_info().rss / 1024 / 1024,
            'uptime': time.time() - self.start_time
        }
    
    def get_operation_stats(self, operation_name: str) -> Dict[str, Any]:
        """获取操作统计信息"""
        if operation_name not in self.metrics:
            return {}
        
        operations = self.metrics[operation_name]
        if not operations:
            return {}
        
        durations = [op['duration'] for op in operations]
        memory_used = [op['memory_used'] for op in operations]
        
        return {
            'count': len(operations),
            'total_duration': sum(durations),
            'avg_duration': sum(durations) / len(durations),
            'min_duration': min(durations),
            'max_duration': max(durations),
            'total_memory_used': sum(memory_used),
            'avg_memory_used': sum(memory_used) / len(memory_used)
        }
    
    def get_all_stats(self) -> Dict[str, Any]:
        """获取所有统计信息"""
        stats = {
            'system': self.get_system_info(),
            'operations': {}
        }
        
        for operation_name in self.metrics:
            stats['operations'][operation_name] = self.get_operation_stats(operation_name)
        
        return stats
    
    def reset(self):
        """重置统计信息"""
        self.metrics.clear()
        self.current_operations.clear()
        self.start_time = time.time()

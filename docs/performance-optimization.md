# NeuralFive 性能优化指南

## 性能基准

### 当前性能指标
- **搜索速度**: 100,000 节点/秒
- **评估精度**: 95% 胜率 vs 随机对手
- **内存使用**: < 512MB
- **响应时间**: < 1秒 (中等难度)

## 优化策略

### 1. 搜索算法优化

#### Alpha-Beta剪枝优化
```python
class OptimizedSearch:
    """优化的搜索算法"""
    
    def __init__(self):
        self.transposition_table = {}
        self.killer_moves = [[None] * MAX_DEPTH for _ in range(2)]
        self.history_table = {}
    
    def alpha_beta(self, board, depth, alpha, beta, maximizing):
        """优化的Alpha-Beta搜索"""
        
        # 置换表查询
        board_hash = self.hash_board(board)
        if board_hash in self.transposition_table:
            entry = self.transposition_table[board_hash]
            if entry.depth >= depth:
                if entry.flag == EXACT:
                    return entry.value
                elif entry.flag == LOWER:
                    alpha = max(alpha, entry.value)
                elif entry.flag == UPPER:
                    beta = min(beta, entry.value)
                
                if alpha >= beta:
                    return entry.value
        
        # 杀手启发式
        moves = self.order_moves(board, killer_moves[self.ply])
        
        # 历史启发式
        moves.sort(key=lambda m: self.history_table.get(m, 0), reverse=True)
        
        # 搜索逻辑...
        return best_value
```

#### 迭代深化
```python
def iterative_deepening_search(board, max_time, max_depth=20):
    """迭代深化搜索"""
    
    start_time = time.time()
    best_move = None
    
    for depth in range(1, max_depth + 1):
        if time.time() - start_time > max_time * 0.8:
            break
        
        # 使用之前深度的结果作为排序依据
        move = search_with_time_limit(board, depth, max_time - (time.time() - start_time))
        if move:
            best_move = move
        
        # 更新剩余时间
        remaining_time = max_time - (time.time() - start_time)
        if remaining_time < 0.1:
            break
    
    return best_move
```

### 2. 评估函数优化

#### 快速模式识别
```python
@numba.jit(nopython=True, cache=True)
def fast_pattern_match(board, patterns):
    """快速模式匹配"""
    
    scores = np.zeros(4)  # 四个方向
    
    for direction in range(4):
        for i in range(board.shape[0]):
            for j in range(board.shape[1]):
                # 预计算模式匹配
                pattern_score = 0
                for pattern, value in patterns:
                    if matches_pattern(board, i, j, pattern, direction):
                        pattern_score += value
                
                scores[direction] += pattern_score
    
    return scores
```

#### 特征缓存
```python
class FeatureCache:
    """特征缓存系统"""
    
    def __init__(self, max_size=100000):
        self.cache = LRUCache(maxsize=max_size)
        self.hit_count = 0
        self.miss_count = 0
    
    def get_features(self, board_hash):
        """获取缓存的特征"""
        if board_hash in self.cache:
            self.hit_count += 1
            return self.cache[board_hash]
        
        self.miss_count += 1
        return None
    
    def cache_features(self, board_hash, features):
        """缓存特征"""
        self.cache[board_hash] = features
    
    def hit_rate(self):
        """缓存命中率"""
        total = self.hit_count + self.miss_count
        return self.hit_count / total if total > 0 else 0
```

### 3. 内存管理

#### 对象池
```python
class MovePool:
    """移动对象池"""
    
    def __init__(self, max_size=10000):
        self.pool = []
        self.max_size = max_size
    
    def acquire(self):
        """获取移动对象"""
        if self.pool:
            return self.pool.pop()
        return Move()
    
    def release(self, move):
        """释放移动对象"""
        if len(self.pool) < self.max_size:
            move.reset()
            self.pool.append(move)

class BoardPool:
    """棋盘对象池"""
    
    def __init__(self, max_size=1000):
        self.pool = []
        self.max_size = max_size
    
    def acquire(self, size=15):
        """获取棋盘对象"""
        if self.pool:
            board = self.pool.pop()
            board.fill(0)
            return board
        return np.zeros((size, size), dtype=np.int8)
    
    def release(self, board):
        """释放棋盘对象"""
        if len(self.pool) < self.max_size:
            self.pool.append(board)
```

#### 内存映射
```python
class MemoryMappedBoard:
    """内存映射棋盘"""
    
    def __init__(self, size=15):
        self.size = size
        self.board = np.memmap(
            'board.dat', 
            dtype=np.int8, 
            mode='w+', 
            shape=(size, size)
        )
    
    def __del__(self):
        """清理内存映射"""
        if hasattr(self, 'board'):
            del self.board
            if os.path.exists('board.dat'):
                os.remove('board.dat')
```

### 4. 并行计算

#### 多进程搜索
```python
class ParallelSearch:
    """并行搜索"""
    
    def __init__(self, num_processes=None):
        self.num_processes = num_processes or mp.cpu_count()
        self.pool = mp.Pool(processes=self.num_processes)
    
    def search_parallel(self, board, moves, depth):
        """并行搜索多个分支"""
        
        # 分割搜索空间
        chunk_size = len(moves) // self.num_processes
        chunks = [moves[i:i+chunk_size] for i in range(0, len(moves), chunk_size)]
        
        # 并行搜索
        results = self.pool.starmap(
            self.search_chunk,
            [(board, chunk, depth) for chunk in chunks]
        )
        
        # 合并结果
        best_move = max(results, key=lambda x: x[0])
        return best_move
    
    def search_chunk(self, board, moves, depth):
        """搜索一个分支"""
        best_score = -np.inf
        best_move = None
        
        for move in moves:
            new_board = board.copy()
            make_move(new_board, move)
            score = -self.alpha_beta(new_board, depth-1, -np.inf, np.inf, False)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_score, best_move
```

#### GPU加速
```python
import cupy as cp

class GPUEvaluator:
    """GPU加速评估器"""
    
    def __init__(self):
        self.gpu_patterns = cp.array(self.load_patterns())
    
    def evaluate_batch(self, boards):
        """批量评估棋盘"""
        
        # 将棋盘数据转移到GPU
        gpu_boards = cp.array(boards)
        
        # 并行评估
        scores = cp.zeros(len(boards))
        
        for i, board in enumerate(gpu_boards):
            scores[i] = self._gpu_evaluate(board)
        
        # 返回CPU
        return cp.asnumpy(scores)
    
    @cp.fuse()
    def _gpu_evaluate(self, board):
        """GPU评估函数"""
        # 使用CUDA核函数进行并行计算
        score = 0
        for pattern in self.gpu_patterns:
            score += cp.sum(board * pattern)
        return score
```

### 5. 数据结构优化

#### 位运算表示
```python
class BitBoard:
    """位棋盘表示"""
    
    def __init__(self, size=15):
        self.size = size
        self.black_board = 0
        self.white_board = 0
        self.empty_board = (1 << (size * size)) - 1
    
    def make_move(self, pos, player):
        """执行落子"""
        mask = 1 << pos
        
        if player == BLACK:
            self.black_board |= mask
        else:
            self.white_board |= mask
        
        self.empty_board &= ~mask
    
    def check_win(self, player):
        """快速检查获胜"""
        board = self.black_board if player == BLACK else self.white_board
        
        # 水平检查
        horizontal = board & (board << 1) & (board << 2) & (board << 3) & (board << 4)
        if horizontal:
            return True
        
        # 垂直检查
        vertical = board & (board << self.size) & (board << (self.size * 2)) & \
                  (board << (self.size * 3)) & (board << (self.size * 4))
        if vertical:
            return True
        
        # 对角线检查
        diagonal1 = board & (board << (self.size + 1)) & (board << (self.size + 1) * 2) & \
                   (board << (self.size + 1) * 3) & (board << (self.size + 1) * 4)
        if diagonal1:
            return True
        
        return False
```

#### 压缩存储
```python
class CompressedBoard:
    """压缩棋盘存储"""
    
    def __init__(self, size=15):
        self.size = size
        self.data = np.zeros((size * size + 3) // 4, dtype=np.uint8)
    
    def set_cell(self, row, col, value):
        """设置单元格值"""
        pos = row * self.size + col
        byte_pos = pos // 4
        bit_pos = (pos % 4) * 2
        
        # 清除原有值
        self.data[byte_pos] &= ~(3 << bit_pos)
        # 设置新值
        self.data[byte_pos] |= (value & 3) << bit_pos
    
    def get_cell(self, row, col):
        """获取单元格值"""
        pos = row * self.size + col
        byte_pos = pos // 4
        bit_pos = (pos % 4) * 2
        
        return (self.data[byte_pos] >> bit_pos) & 3
```

## 性能监控

### 性能指标收集
```python
class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.metrics = {
            'search_time': [],
            'evaluation_time': [],
            'nodes_per_second': [],
            'memory_usage': [],
            'cache_hit_rate': []
        }
    
    def start_timing(self, metric):
        """开始计时"""
        self.start_time = time.time()
        self.metric_name = metric
    
    def end_timing(self):
        """结束计时"""
        elapsed = time.time() - self.start_time
        self.metrics[self.metric_name].append(elapsed)
    
    def collect_metrics(self):
        """收集系统指标"""
        process = psutil.Process()
        self.metrics['memory_usage'].append(process.memory_info().rss)
    
    def get_report(self):
        """生成性能报告"""
        report = {}
        for metric, values in self.metrics.items():
            if values:
                report[metric] = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'min': np.min(values),
                    'max': np.max(values)
                }
        
        return report
```

### 实时性能显示
```python
class PerformanceHUD:
    """性能HUD显示"""
    
    def __init__(self, font_size=16):
        self.font = pygame.font.Font(None, font_size)
        self.enabled = True
        self.update_interval = 100  # 毫秒
        self.last_update = 0
    
    def update(self, monitor):
        """更新显示"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update < self.update_interval:
            return
        
        self.last_update = current_time
        self.metrics = monitor.get_report()
    
    def draw(self, surface):
        """绘制HUD"""
        if not self.enabled or not self.metrics:
            return
        
        y = 10
        for metric, stats in self.metrics.items():
            text = f"{metric}: {stats['mean']:.3f}s"
            surface.blit(self.font.render(text, True, (255, 255, 255)), (10, y))
            y += 20
```

## 基准测试

### 标准化测试集
```python
class BenchmarkSuite:
    """基准测试套件"""
    
    def __init__(self):
        self.test_positions = self.load_test_positions()
        self.reference_engine = ReferenceEngine()
    
    def run_benchmark(self, engine, iterations=100):
        """运行基准测试"""
        
        results = {
            'accuracy': [],
            'speed': [],
            'consistency': []
        }
        
        for position in self.test_positions:
            # 准确性测试
            move = engine.get_best_move(position, time_limit=1.0)
            reference_move = self.reference_engine.get_best_move(position, time_limit=10.0)
            
            accuracy = self.evaluate_move_quality(move, reference_move)
            results['accuracy'].append(accuracy)
            
            # 速度测试
            start_time = time.time()
            for _ in range(iterations):
                engine.get_best_move(position, time_limit=0.1)
            
            avg_time = (time.time() - start_time) / iterations
            results['speed'].append(avg_time)
            
            # 一致性测试
            moves = []
            for _ in range(10):
                moves.append(engine.get_best_move(position, time_limit=0.1))
            
            consistency = self.calculate_consistency(moves)
            results['consistency'].append(consistency)
        
        return self.generate_report(results)
```
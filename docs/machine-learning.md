# NeuralFive 机器学习集成指南

## 神经网络架构

### 卷积神经网络 (CNN)
```python
import tensorflow as tf
from tensorflow.keras import layers, models

class GomokuCNN:
    """五子棋CNN模型"""
    
    def __init__(self, board_size=15, num_channels=128):
        self.board_size = board_size
        self.num_channels = num_channels
        self.model = self.build_model()
    
    def build_model(self):
        """构建CNN模型"""
        
        # 输入层
        board_input = layers.Input(shape=(self.board_size, self.board_size, 3))
        
        # 卷积层块
        x = self._conv_block(board_input, self.num_channels, 3)
        x = self._residual_block(x, self.num_channels)
        x = self._residual_block(x, self.num_channels)
        x = self._residual_block(x, self.num_channels)
        
        # 策略头
        policy = layers.Conv2D(2, 1, activation='relu')(x)
        policy = layers.Flatten()(policy)
        policy = layers.Dense(self.board_size * self.board_size, activation='softmax')(policy)
        
        # 价值头
        value = layers.Conv2D(1, 1, activation='relu')(x)
        value = layers.Flatten()(value)
        value = layers.Dense(256, activation='relu')(value)
        value = layers.Dense(1, activation='tanh')(value)
        
        model = models.Model(inputs=board_input, outputs=[policy, value])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss=['categorical_crossentropy', 'mse'],
            metrics=['accuracy', 'mse']
        )
        
        return model
    
    def _conv_block(self, x, filters, kernel_size):
        """卷积块"""
        x = layers.Conv2D(filters, kernel_size, padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)
        return x
    
    def _residual_block(self, x, filters):
        """残差块"""
        shortcut = x
        
        x = self._conv_block(x, filters, 3)
        x = layers.Conv2D(filters, 3, padding='same')(x)
        x = layers.BatchNormalization()(x)
        
        x = layers.Add()([shortcut, x])
        x = layers.ReLU()(x)
        
        return x
```

### 强化学习
```python
class GomokuRL:
    """五子棋强化学习"""
    
    def __init__(self, model, mcts_simulations=800, c_puct=1.0):
        self.model = model
        self.mcts = MCTS(model, mcts_simulations, c_puct)
        self.memory = []
        self.epsilon = 0.2
    
    def self_play(self, num_games=100):
        """自我对弈"""
        
        for game in range(num_games):
            game_memory = []
            board = GomokuBoard()
            
            while not board.is_game_over():
                # MCTS搜索
                root = self.mcts.search(board)
                
                # 获取动作概率
                action_probs = np.zeros(board.size * board.size)
                for child in root.children.values():
                    action_probs[child.action] = child.visit_count
                
                action_probs /= np.sum(action_probs)
                
                # 添加噪声增加探索
                if len(game_memory) < 30:  # 开局阶段
                    noise = np.random.dirichlet([0.3] * len(action_probs))
                    action_probs = 0.75 * action_probs + 0.25 * noise
                
                # 选择动作
                action = np.random.choice(len(action_probs), p=action_probs)
                
                # 保存状态
                state = board.get_state()
                game_memory.append([state, action_probs, board.current_player])
                
                # 执行动作
                board.make_move(action)
            
            # 计算最终奖励
            winner = board.get_winner()
            reward = 0
            if winner == BLACK:
                reward = 1
            elif winner == WHITE:
                reward = -1
            
            # 更新记忆
            for i, (state, probs, player) in enumerate(game_memory):
                if player == BLACK:
                    game_memory[i][2] = reward
                else:
                    game_memory[i][2] = -reward
            
            self.memory.extend(game_memory)
    
    def train(self, batch_size=32, epochs=10):
        """训练模型"""
        
        if len(self.memory) < batch_size:
            return
        
        for epoch in range(epochs):
            # 随机采样
            batch_indices = np.random.choice(len(self.memory), batch_size)
            batch = [self.memory[i] for i in batch_indices]
            
            states = np.array([example[0] for example in batch])
            target_policies = np.array([example[1] for example in batch])
            target_values = np.array([example[2] for example in batch])
            
            # 训练
            history = self.model.model.fit(
                states, 
                [target_policies, target_values],
                batch_size=batch_size,
                epochs=1,
                verbose=0
            )
            
            print(f"Epoch {epoch+1}/{epochs} - Loss: {history.history['loss'][0]:.4f}")
```

### MCTS集成
```python
class MCTS:
    """蒙特卡洛树搜索"""
    
    def __init__(self, model, simulations=800, c_puct=1.0):
        self.model = model
        self.simulations = simulations
        self.c_puct = c_puct
    
    def search(self, board):
        """执行MCTS搜索"""
        
        root = MCTSNode(board)
        
        for _ in range(self.simulations):
            node = root
            
            # 选择
            while not node.is_leaf() and not node.board.is_game_over():
                node = node.select_child(self.c_puct)
            
            # 扩展
            if not node.board.is_game_over():
                # 获取神经网络预测
                state = node.board.get_state()
                policy, value = self.model.model.predict(state.reshape(1, *state.shape))
                
                # 扩展节点
                node.expand(policy[0])
                
                # 评估
                reward = value[0][0]
            else:
                # 游戏结束，获取真实奖励
                winner = node.board.get_winner()
                if winner == node.board.current_player:
                    reward = 1
                elif winner == EMPTY:
                    reward = 0
                else:
                    reward = -1
            
            # 回溯
            node.backup(-reward)
        
        return root

class MCTSNode:
    """MCTS节点"""
    
    def __init__(self, board, parent=None, action=None, prior=0):
        self.board = board
        self.parent = parent
        self.action = action
        self.prior = prior
        
        self.visit_count = 0
        self.total_reward = 0
        self.children = {}
    
    def select_child(self, c_puct):
        """选择子节点"""
        
        best_score = -np.inf
        best_action = None
        
        for action, child in self.children.items():
            # UCB公式
            score = child.total_reward / child.visit_count + \
                   c_puct * child.prior * np.sqrt(self.visit_count) / (1 + child.visit_count)
            
            if score > best_score:
                best_score = score
                best_action = action
        
        return self.children[best_action]
    
    def expand(self, policy):
        """扩展节点"""
        
        for action in self.board.get_legal_moves():
            if action not in self.children:
                # 创建新棋盘
                new_board = self.board.copy()
                new_board.make_move(action)
                
                # 创建子节点
                prior = policy[action]
                self.children[action] = MCTSNode(new_board, parent=self, action=action, prior=prior)
    
    def backup(self, reward):
        """回溯更新"""
        
        self.visit_count += 1
        self.total_reward += reward
        
        if self.parent:
            self.parent.backup(-reward)
    
    def is_leaf(self):
        """检查是否为叶节点"""
        return len(self.children) == 0
```

## 数据生成

### 自我对弈数据
```python
class DataGenerator:
    """数据生成器"""
    
    def __init__(self, model, num_games=1000):
        self.model = model
        self.num_games = num_games
        self.mcts = MCTS(model)
    
    def generate_dataset(self):
        """生成数据集"""
        
        dataset = {
            'states': [],
            'policies': [],
            'values': []
        }
        
        for game in range(self.num_games):
            print(f"Game {game+1}/{self.num_games}")
            
            game_data = self.play_game()
            
            dataset['states'].extend(game_data['states'])
            dataset['policies'].extend(game_data['policies'])
            dataset['values'].extend(game_data['values'])
        
        # 转换为numpy数组
        dataset['states'] = np.array(dataset['states'])
        dataset['policies'] = np.array(dataset['policies'])
        dataset['values'] = np.array(dataset['values'])
        
        return dataset
    
    def play_game(self):
        """进行一局游戏"""
        
        board = GomokuBoard()
        game_data = {
            'states': [],
            'policies': [],
            'values': []
        }
        
        while not board.is_game_over():
            # MCTS搜索
            root = self.mcts.search(board)
            
            # 获取动作概率
            action_probs = np.zeros(board.size * board.size)
            for child in root.children.values():
                action_probs[child.action] = child.visit_count
            
            action_probs /= np.sum(action_probs)
            
            # 保存状态
            state = board.get_state()
            game_data['states'].append(state)
            game_data['policies'].append(action_probs)
            
            # 选择动作
            action = np.random.choice(len(action_probs), p=action_probs)
            board.make_move(action)
        
        # 计算最终奖励
        winner = board.get_winner()
        reward = 0
        if winner == BLACK:
            reward = 1
        elif winner == WHITE:
            reward = -1
        
        # 更新价值
        game_data['values'] = [reward if i % 2 == 0 else -reward 
                              for i in range(len(game_data['states']))]
        
        return game_data
```

### 数据增强
```python
class DataAugmenter:
    """数据增强器"""
    
    def __init__(self):
        self.augmentations = [
            self.rotate_90,
            self.rotate_180,
            self.rotate_270,
            self.flip_horizontal,
            self.flip_vertical,
            self.flip_diagonal
        ]
    
    def augment_dataset(self, dataset):
        """增强数据集"""
        
        augmented = {
            'states': [],
            'policies': [],
            'values': []
        }
        
        for i in range(len(dataset['states'])):
            state = dataset['states'][i]
            policy = dataset['policies'][i]
            value = dataset['values'][i]
            
            # 原始数据
            augmented['states'].append(state)
            augmented['policies'].append(policy)
            augmented['values'].append(value)
            
            # 增强数据
            for aug_func in self.augmentations:
                aug_state, aug_policy = aug_func(state, policy)
                augmented['states'].append(aug_state)
                augmented['policies'].append(aug_policy)
                augmented['values'].append(value)
        
        # 转换为numpy数组
        augmented['states'] = np.array(augmented['states'])
        augmented['policies'] = np.array(augmented['policies'])
        augmented['values'] = np.array(augmented['values'])
        
        return augmented
    
    def rotate_90(self, state, policy):
        """旋转90度"""
        
        # 旋转状态
        rotated_state = np.rot90(state, k=1, axes=(0, 1))
        
        # 旋转策略
        size = int(np.sqrt(len(policy)))
        policy_board = policy.reshape(size, size)
        rotated_policy = np.rot90(policy_board, k=1).flatten()
        
        return rotated_state, rotated_policy
    
    def flip_horizontal(self, state, policy):
        """水平翻转"""
        
        # 翻转状态
        flipped_state = np.flip(state, axis=1)
        
        # 翻转策略
        size = int(np.sqrt(len(policy)))
        policy_board = policy.reshape(size, size)
        flipped_policy = np.flip(policy_board, axis=1).flatten()
        
        return flipped_state, flipped_policy
```

## 模型训练

### 训练流程
```python
class ModelTrainer:
    """模型训练器"""
    
    def __init__(self, model, batch_size=32, learning_rate=0.001):
        self.model = model
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        
        self.optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        self.loss_fn = {
            'policy': tf.keras.losses.CategoricalCrossentropy(),
            'value': tf.keras.losses.MeanSquaredError()
        }
    
    def train_epoch(self, dataset):
        """训练一个epoch"""
        
        dataset_size = len(dataset['states'])
        indices = np.random.permutation(dataset_size)
        
        total_loss = 0
        num_batches = 0
        
        for i in range(0, dataset_size, self.batch_size):
            batch_indices = indices[i:i+self.batch_size]
            
            # 准备批次数据
            batch_states = dataset['states'][batch_indices]
            batch_policies = dataset['policies'][batch_indices]
            batch_values = dataset['values'][batch_indices]
            
            # 训练步骤
            loss = self.train_step(batch_states, batch_policies, batch_values)
            total_loss += loss
            num_batches += 1
        
        return total_loss / num_batches
    
    @tf.function
    def train_step(self, states, policies, values):
        """训练步骤"""
        
        with tf.GradientTape() as tape:
            # 前向传播
            pred_policies, pred_values = self.model.model(states, training=True)
            
            # 计算损失
            policy_loss = self.loss_fn['policy'](policies, pred_policies)
            value_loss = self.loss_fn['value'](values, pred_values)
            total_loss = policy_loss + value_loss
        
        # 反向传播
        gradients = tape.gradient(total_loss, self.model.model.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.model.model.trainable_variables))
        
        return total_loss
    
    def train(self, dataset, num_epochs=100, validation_split=0.1):
        """完整训练流程"""
        
        # 分割训练和验证数据
        split_idx = int(len(dataset['states']) * (1 - validation_split))
        
        train_dataset = {
            'states': dataset['states'][:split_idx],
            'policies': dataset['policies'][:split_idx],
            'values': dataset['values'][:split_idx]
        }
        
        val_dataset = {
            'states': dataset['states'][split_idx:],
            'policies': dataset['policies'][split_idx:],
            'values': dataset['values'][split_idx:]
        }
        
        # 训练循环
        for epoch in range(num_epochs):
            # 训练
            train_loss = self.train_epoch(train_dataset)
            
            # 验证
            val_loss = self.evaluate(val_dataset)
            
            print(f"Epoch {epoch+1}/{num_epochs}")
            print(f"Train Loss: {train_loss:.4f}")
            print(f"Val Loss: {val_loss:.4f}")
            
            # 早停检查
            if self.early_stopping(val_loss):
                print("Early stopping triggered")
                break
    
    def evaluate(self, dataset):
        """评估模型"""
        
        dataset_size = len(dataset['states'])
        total_loss = 0
        num_batches = 0
        
        for i in range(0, dataset_size, self.batch_size):
            batch_states = dataset['states'][i:i+self.batch_size]
            batch_policies = dataset['policies'][i:i+self.batch_size]
            batch_values = dataset['values'][i:i+self.batch_size]
            
            # 前向传播
            pred_policies, pred_values = self.model.model(batch_states, training=False)
            
            # 计算损失
            policy_loss = self.loss_fn['policy'](batch_policies, pred_policies)
            value_loss = self.loss_fn['value'](batch_values, pred_values)
            total_loss += policy_loss + value_loss
            num_batches += 1
        
        return total_loss / num_batches
```

## 模型评估

### 对战测试
```python
class ModelEvaluator:
    """模型评估器"""
    
    def __init__(self, model, opponent_engine, num_games=100):
        self.model = model
        self.opponent = opponent_engine
        self.num_games = num_games
    
    def evaluate_model(self):
        """评估模型性能"""
        
        results = {
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'win_rate': 0.0,
            'avg_game_length': 0
        }
        
        game_lengths = []
        
        for game in range(self.num_games):
            print(f"Evaluation Game {game+1}/{self.num_games}")
            
            # 交替先手
            model_first = game % 2 == 0
            result, length = self.play_game(model_first)
            
            if result == 'win':
                results['wins'] += 1
            elif result == 'loss':
                results['losses'] += 1
            else:
                results['draws'] += 1
            
            game_lengths.append(length)
        
        # 计算统计信息
        results['win_rate'] = results['wins'] / self.num_games
        results['avg_game_length'] = np.mean(game_lengths)
        
        return results
    
    def play_game(self, model_first):
        """进行一局对战"""
        
        board = GomokuBoard()
        game_length = 0
        
        while not board.is_game_over() and game_length < 225:  # 最大步数限制
            game_length += 1
            
            if (board.current_player == BLACK) == model_first:
                # 模型落子
                state = board.get_state()
                policy, _ = self.model.model.predict(state.reshape(1, *state.shape))
                
                # 选择最佳动作
                legal_moves = board.get_legal_moves()
                move_probs = policy[0][legal_moves]
                move = legal_moves[np.argmax(move_probs)]
                
            else:
                # 对手落子
                move = self.opponent.get_best_move(board.board)
                move = move.row * board.size + move.col
            
            board.make_move(move)
        
        # 判断结果
        winner = board.get_winner()
        if winner == EMPTY:
            return 'draw', game_length
        elif (winner == BLACK) == model_first:
            return 'win', game_length
        else:
            return 'loss', game_length
```
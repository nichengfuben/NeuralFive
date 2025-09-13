# AI算法详解

## 算法概述

SmartFive的AI基于Negamax算法，这是一种用于零和博弈的递归算法，是Minimax算法的变体。Negamax算法利用了零和博弈中双方收益之和为零的特性，将Minimax算法中的最大化和最小化统一为最大化操作。

## 核心算法

### Negamax算法

Negamax算法的基本思想是：
```
function negamax(node, depth, α, β, color) is
    if depth = 0 or node is a terminal node then
        return color × the heuristic value of node
    end if
    childNodes := generateMoves(node)
    childNodes := orderMoves(childNodes)
    value := −∞
    foreach child in childNodes do
        value := max(value, −negamax(child, depth − 1, −β, −α, −color))
        α := max(α, value)
        if α ≥ β then
            break (* cut-off *)
        end if
    end foreach
    return value
end function
```

### α-β剪枝优化

α-β剪枝是一种搜索树剪枝技术，用于减少搜索树中需要评估的节点数量。它通过维护两个值α和β来实现：
- α：到目前为止路径上的最大值
- β：到目前为止路径上的最小值

当α≥β时，可以剪掉剩余的分支，因为它们不会影响最终结果。

## 启发式评估函数

评估函数是AI的核心，用于评估当前棋盘状态的优劣。我们的评估函数考虑了以下因素：

1. **连子模式**：检测潜在的连五、活四、死四、活三、死三等模式
2. **位置权重**：棋盘中心位置权重更高
3. **攻击与防守**：同时考虑自己和对手的潜在威胁

### 评分系统

我们为不同的连子模式分配了不同的分数：
- 连五：10000000分（胜利）
- 活四：100000分
- 死四：10000分
- 活三：1000分
- 死三：100分
- 活二：10分
- 死二：1分

## 优化技术

### 1. 移动排序

为了提高α-β剪枝的效率，我们对候选移动进行排序，优先考虑最有希望的移动。

### 2. 缓存机制

使用哈希表缓存已计算的棋盘状态，避免重复计算。

### 3. 迭代加深

逐步增加搜索深度，确保在时间限制内找到最佳移动。

### 4. 多线程支持

AI计算在单独的线程中运行，防止界面卡顿。

## 算法复杂度

- 时间复杂度：O(b^d)，其中b是分支因子，d是搜索深度
- 空间复杂度：O(d)，递归调用栈的深度

## 性能优化

使用Numba库对关键计算函数进行JIT编译，显著提高计算速度。
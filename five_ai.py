import numpy as np
from numba import jit, njit
from numba.typed import List
import numba

class MapPoint:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.set = False
        self.score = 0
        self.valid = False
        self.info = [[0, 0, 0, 0] for _ in range(4)]

class FiveInARowAI:
    def __init__(self):
        # 四个方向：左上-右下对角线，垂直，水平，右上-左下对角线
        self.moves = [[-1, -1], [-1, 0], [0, -1], [-1, 1]]
        self.coe = [-2, 1]  # 系数：对手-2，己方1
        self.scores = [0, 1, 10, 2000, 4000, 100000000000]  # 不同连子数的分数
        
        # 提升到理论极限参数
        self.depth = 100 # 增加搜索深度
        self.totry = [20, 18]  # 增加候选移动数量
        
        self.color = None
        self.otc = None  # 对手颜色
        self.sum = 0
        self.set_num = 0
        self.map = []
        self.score_queue = []
        
        # 初始化15x15棋盘
        for i in range(15):
            tmp = []
            for j in range(15):
                a = MapPoint(i, j)
                tmp.append(a)
                self.score_queue.append(a)
            self.map.append(tmp)
        
        self.board_buf = [0] * 225
        self.cache = {}
    
    def clear_board(self):
        """清空棋盘"""
        self.sum = 0
        self.set_num = 0
        self.cache = {}
        self.board_buf = [0] * 225
        
        for i in range(15):
            for j in range(15):
                self.map[i][j].set = False
                self.map[i][j].score = 0
                self.map[i][j].valid = False
                self.map[i][j].info = [[0, 0, 0, 0] for _ in range(4)]
        
        self.score_queue = []
        for i in range(15):
            for j in range(15):
                self.score_queue.append(self.map[i][j])
    
    def make_move(self, r, c, player_color):
        """
        玩家下棋，AI自动响应
        player_color: 'black' 或 'white'
        返回: 棋盘状态字符串
        """
        # 设置AI颜色
        self.color = 'white' if player_color == 'black' else 'black'
        self.otc = player_color
        
        # 玩家下棋
        self.update_map(r, c, player_color)
        self.set_num += 1
        self.score_queue.sort(key=self.sort_move_key)
        
        # 检查游戏是否结束
        if self.check_win():
            return self.get_board_string()
        
        # AI计算最佳移动
        best_move = self.compute_best_move()
        
        if best_move:
            ai_r, ai_c = best_move
            self.update_map(ai_r, ai_c, self.color)
            self.set_num += 1
            self.score_queue.sort(key=self.sort_move_key)
        
        return self.get_board_string()
    
    def get_board_string(self):
        """获取棋盘状态字符串"""
        result = []
        for i in range(15):
            row = ""
            for j in range(15):
                if self.map[i][j].set == 1:  # 黑子 (num=0对应set=1)
                    row += "B"
                elif self.map[i][j].set == 2:  # 白子 (num=1对应set=2)
                    row += "W"
                else:
                    row += "."
            result.append(row)
        return "\n".join(result)
    
    def check_win(self):
        """检查是否有获胜者"""
        return abs(self.sum) >= 10000000
    
    def update_map(self, r, c, color):
        """更新棋盘"""
        if color == 'black':
            num = 0
        elif color == 'white':
            num = 1
        else:
            return
        
        return self._update_map(r, c, num, False)
    
    def _update_map(self, r, c, num, remove):
        """内部更新棋盘逻辑"""
        moves = self.moves
        coe = self.coe
        scores = self.scores
        changes = 0
        
        if not remove:
            self.board_buf[r * 15 + c] = num + 2
            self.map[r][c].set = num + 1
            
            for i in range(4):
                x, y = r, c
                step = 5
                while step > 0 and x >= 0 and y >= 0 and y < 15:
                    xx = x - moves[i][0] * 4
                    yy = y - moves[i][1] * 4
                    if xx >= 15 or yy < 0 or yy >= 15:
                        x += moves[i][0]
                        y += moves[i][1]
                        step -= 1
                        continue
                    
                    cur = self.map[x][y].info[i]
                    if cur[2] > 0:
                        tmp = 5
                        xx, yy = x, y
                        s = scores[cur[2]]
                        changes -= s * cur[3]
                        while tmp > 0:
                            if 0 <= xx < 15 and 0 <= yy < 15:
                                self.map[xx][yy].score -= s
                            xx -= moves[i][0]
                            yy -= moves[i][1]
                            tmp -= 1
                    
                    cur[num] += 1
                    if cur[1 - num] > 0:
                        cur[2] = 0
                    else:
                        cur[2] = cur[num]
                        e = coe[num]
                        cur[3] = e
                        s = scores[cur[2]]
                        tmp = 5
                        xx, yy = x, y
                        changes += s * cur[3]
                        while tmp > 0:
                            if 0 <= xx < 15 and 0 <= yy < 15:
                                self.map[xx][yy].score += s
                            xx -= moves[i][0]
                            yy -= moves[i][1]
                            tmp -= 1
                    
                    x += moves[i][0]
                    y += moves[i][1]
                    step -= 1
        else:
            self.board_buf[r * 15 + c] = 0
            self.map[r][c].set = False
            
            for i in range(4):
                x, y = r, c
                step = 5
                while step > 0 and x >= 0 and y >= 0 and y < 15:
                    xx = x - moves[i][0] * 4
                    yy = y - moves[i][1] * 4
                    if xx >= 15 or yy < 0 or yy >= 15:
                        x += moves[i][0]
                        y += moves[i][1]
                        step -= 1
                        continue
                    
                    cur = self.map[x][y].info[i]
                    sc = 0
                    cur[num] -= 1
                    
                    if cur[2] > 0:
                        tmp = 5
                        xx, yy = x, y
                        s = scores[cur[2]]
                        changes -= s * cur[3]
                        while tmp > 0:
                            if 0 <= xx < 15 and 0 <= yy < 15:
                                self.map[xx][yy].score -= s
                            xx -= moves[i][0]
                            yy -= moves[i][1]
                            tmp -= 1
                        cur[2] -= 1
                        if cur[num] > 0:
                            sc = 1
                    elif cur[1 - num] > 0 and cur[num] == 0:
                        sc = -1
                    
                    if sc == 1:
                        tmp = 5
                        s = scores[cur[2]]
                        xx, yy = x, y
                        changes += s * cur[3]
                        while tmp > 0:
                            if 0 <= xx < 15 and 0 <= yy < 15:
                                self.map[xx][yy].score += s
                            xx -= moves[i][0]
                            yy -= moves[i][1]
                            tmp -= 1
                    elif sc == -1:
                        cur[2] = cur[1 - num]
                        tmp = 5
                        s = scores[cur[2]]
                        cur[3] = coe[1 - num]
                        xx, yy = x, y
                        changes += s * cur[3]
                        while tmp > 0:
                            if 0 <= xx < 15 and 0 <= yy < 15:
                                self.map[xx][yy].score += s
                            xx -= moves[i][0]
                            yy -= moves[i][1]
                            tmp -= 1
                    
                    x += moves[i][0]
                    y += moves[i][1]
                    step -= 1
        
        self.sum += changes
    
    def sort_move_key(self, point):
        """排序关键字函数"""
        if point.set:
            return (1, 0)
        return (0, -point.score)
    
    def simulate(self, x, y, num):
        """模拟下棋"""
        self.set_num += 1
        self._update_map(x, y, num, False)
    
    def desimulate(self, x, y, num):
        """撤销模拟"""
        self._update_map(x, y, num, True)
        self.set_num -= 1
    
    def buf_to_string(self):
        """将棋盘状态转换为字符串用于缓存"""
        return ''.join(str(x) for x in self.board_buf)
    
    def nega(self, x, y, depth, alpha, beta):
        """Negamax算法实现"""
        num = depth % 2
        self.simulate(x, y, num)
        
        buf_str = self.buf_to_string()
        if buf_str in self.cache:
            result = self.cache[buf_str]
            self.desimulate(x, y, num)
            return result
        
        if abs(self.sum) >= 10000000:
            self.desimulate(x, y, num)
            return float('-inf')
        
        if self.set_num == 225:
            self.desimulate(x, y, num)
            return 0
        elif depth == 0:
            result = self.sum
            self.desimulate(x, y, num)
            return result
        
        self.score_queue.sort(key=self.sort_move_key)
        
        tmp_queue = []
        count = 0
        for tmp in self.score_queue:
            if tmp.set:
                continue
            if count >= self.totry[num]:
                break
            tmp_queue.append(tmp.c)
            tmp_queue.append(tmp.r)
            count += 1
        
        if not tmp_queue:
            self.desimulate(x, y, num)
            return 0
        
        depth -= 1
        i = len(tmp_queue) - 1
        b = beta
        
        if i >= 1:
            x_next = tmp_queue[i]
            y_next = tmp_queue[i - 1]
            score = -self.nega(x_next, y_next, depth, -b, -alpha)
            
            if score > alpha:
                buf_str = self.buf_to_string()
                self.cache[buf_str] = score
                alpha = score
            
            if alpha >= beta:
                buf_str = self.buf_to_string()
                self.cache[buf_str] = beta
                self.desimulate(x, y, num)
                return alpha
            
            b = alpha + 1
            i -= 2
            
            while i >= 1:
                x_next = tmp_queue[i]
                y_next = tmp_queue[i - 1]
                score = -self.nega(x_next, y_next, depth, -b, -alpha)
                
                if alpha < score < beta:
                    score = -self.nega(x_next, y_next, depth, -beta, -alpha)
                
                if score > alpha:
                    alpha = score
                
                if alpha >= beta:
                    self.desimulate(x, y, num)
                    return alpha
                
                b = alpha + 1
                i -= 2
        
        self.desimulate(x, y, num)
        return alpha
    
    def compute_best_move(self):
        """计算最佳移动"""
        self.cache = {}
        
        alpha = float('-inf')
        beta = float('inf')
        
        # 获取候选移动
        candidates = []
        for tmp in self.score_queue:
            if tmp.set:
                continue
            if len(candidates) >= 25:  # 增加候选数量
                break
            candidates.append((tmp.r, tmp.c))
        
        if not candidates:
            return None
        
        best_move = candidates[0]
        depth = self.depth
        
        for r, c in candidates:
            b = beta if alpha == float('-inf') else alpha + 1
            score = -self.nega(r, c, depth, -b, -alpha)
            
            if alpha < score < beta and alpha != float('-inf'):
                score = -self.nega(r, c, depth, -beta, -alpha)
            
            if score > alpha:
                alpha = score
                best_move = (r, c)
        
        return best_move


# 封装的两个函数入口
def create_ai():
    """创建AI实例"""
    return FiveInARowAI()

def clear_board(ai):
    """清空棋盘"""
    ai.clear_board()
    return "棋盘已清空"

def make_move(ai, r, c, color='black'):
    """
    下棋并获取AI响应
    参数:
        ai: AI实例
        r: 行坐标 (0-14)
        c: 列坐标 (0-14)
        color: 玩家颜色 'black' 或 'white'
    返回:
        棋盘状态字符串，B=黑子，W=白子，.=空位
    """
    return ai.make_move(r, c, color)

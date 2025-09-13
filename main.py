import pygame
import sys
import threading
import time
import os
from five_ai import create_ai, clear_board, make_move

# 初始化Pygame
pygame.init()

# 游戏常量
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
BOARD_SIZE = 15
CELL_SIZE = 40
BOARD_START_X = 50
BOARD_START_Y = 80
BOARD_WIDTH = CELL_SIZE * (BOARD_SIZE - 1)

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (205, 170, 125)
DARK_BROWN = (139, 90, 43)
GREEN = (34, 139, 34)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
YELLOW = (255, 215, 0)
ORANGE = (255, 165, 0)
GOLD = (255, 215, 0)

class GomokuGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("AI五子棋")
        
        # 设置字体 - 使用pygame默认字体以避免中文问题
        self.setup_fonts()
        
        self.clock = pygame.time.Clock()
        
        # 游戏状态
        self.ai = create_ai()
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.game_state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.player_color = None
        self.ai_color = None
        self.current_turn = "black"
        self.winner = None
        self.last_move = None
        self.hover_pos = None
        self.message = ""
        
        # AI线程相关
        self.ai_thinking = False
        self.ai_thread = None
        self.ai_move_result = None
        
        # UI元素 - 调整位置
        self.black_button = pygame.Rect(270, 350, 150, 55)
        self.white_button = pygame.Rect(480, 350, 150, 55)
        self.restart_button = pygame.Rect(640, 280, 230, 45)
        self.back_button = pygame.Rect(640, 340, 230, 45)
        
        # 动画效果
        self.animation_time = 0
        self.thinking_dots = 0
        self.thinking_timer = 0
    
    def setup_fonts(self):
        """设置字体系统"""
        # 尝试加载系统中文字体
        font_paths = []
        
        if sys.platform == 'win32':
            # Windows字体路径
            font_paths = [
                'C:/Windows/Fonts/msyh.ttc',      # 微软雅黑
                'C:/Windows/Fonts/simsun.ttc',     # 宋体
                'C:/Windows/Fonts/simhei.ttf',     # 黑体
            ]
        elif sys.platform == 'darwin':
            # macOS字体路径
            font_paths = [
                '/System/Library/Fonts/PingFang.ttc',
                '/Library/Fonts/Songti.ttc',
            ]
        else:
            # Linux字体路径
            font_paths = [
                '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
                '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
            ]
        
        # 尝试加载字体文件
        font_loaded = False
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    self.font = pygame.font.Font(font_path, 22)
                    self.small_font = pygame.font.Font(font_path, 16)
                    self.large_font = pygame.font.Font(font_path, 32)
                    self.title_font = pygame.font.Font(font_path, 42)
                    font_loaded = True
                    break
                except:
                    continue
        
        # 如果没有找到中文字体，使用英文
        if not font_loaded:
            self.font = pygame.font.Font(None, 28)
            self.small_font = pygame.font.Font(None, 20)
            self.large_font = pygame.font.Font(None, 40)
            self.title_font = pygame.font.Font(None, 56)
            self.use_english = True
        else:
            self.use_english = False
    
    def get_text(self, key):
        """获取显示文本（中英文切换）"""
        texts = {
            'title': 'ai_wzq' if self.use_english else 'AI五子棋',
            'subtitle': '-- Challenge AI --' if self.use_english else '—— 挑战AI ——',
            'choose': 'Choose Your Color' if self.use_english else '请选择您的棋色',
            'black': 'Black' if self.use_english else '执黑',
            'white': 'White' if self.use_english else '执白',
            'restart': 'New Game' if self.use_english else '重新开始',
            'menu': 'Main Menu' if self.use_english else '返回菜单',
            'info': 'Game Info' if self.use_english else '游戏信息',
            'your_turn': 'Your Turn' if self.use_english else '您的回合',
            'ai_thinking': 'AI Thinking' if self.use_english else 'AI思考中',
            'current': 'Current' if self.use_english else '当前回合',
            'player': 'Player' if self.use_english else '玩家',
            'ai': 'AI',
            'black_move': 'Black Move' if self.use_english else '黑方行动',
            'white_move': 'White Move' if self.use_english else '白方行动',
            'win': 'You Win!' if self.use_english else '恭喜您获胜！',
            'lose': 'AI Wins!' if self.use_english else 'AI获胜！',
            'draw': 'Draw!' if self.use_english else '平局！',
            'first': '(First)' if self.use_english else '（先手）',
            'second': '(Second)' if self.use_english else '（后手）',
            'vs': 'Players' if self.use_english else '对战双方',
            'tips': 'Tips' if self.use_english else '游戏提示',
            'tip1': '• Click intersection to move' if self.use_english else '• 点击交叉点落子',
            'tip2': '• Red mark shows last move' if self.use_english else '• 红框标记最后一手',
            'tip3': '• Connect 5 stones to win' if self.use_english else '• 五子连珠获胜',
            'rules': 'Rules:' if self.use_english else '游戏规则：',
            'rule1': '• Black moves first' if self.use_english else '• 黑棋先行',
            'rule2': '• Take turns to play' if self.use_english else '• 轮流落子',
            'rule3': '• 5 in a row wins' if self.use_english else '• 五子连珠获胜'
        }
        return texts.get(key, key)
    
    def draw_gradient_background(self):
        """绘制渐变背景"""
        for y in range(WINDOW_HEIGHT):
            color_value = 220 + (y * 35 // WINDOW_HEIGHT)
            color = (color_value, color_value, min(255, color_value + 10))
            pygame.draw.line(self.screen, color, (0, y), (WINDOW_WIDTH, y))
    
    def draw_board(self):
        """绘制棋盘"""
        # 绘制棋盘背景
        board_rect = pygame.Rect(
            BOARD_START_X - 25,
            BOARD_START_Y - 25,
            BOARD_WIDTH + 50,
            BOARD_WIDTH + 50
        )
        pygame.draw.rect(self.screen, BROWN, board_rect, border_radius=5)
        pygame.draw.rect(self.screen, DARK_BROWN, board_rect, 3, border_radius=5)
        
        # 绘制网格线
        for i in range(BOARD_SIZE):
            # 横线
            start_pos = (BOARD_START_X, BOARD_START_Y + i * CELL_SIZE)
            end_pos = (BOARD_START_X + BOARD_WIDTH, BOARD_START_Y + i * CELL_SIZE)
            pygame.draw.line(self.screen, BLACK, start_pos, end_pos, 1)
            
            # 竖线
            start_pos = (BOARD_START_X + i * CELL_SIZE, BOARD_START_Y)
            end_pos = (BOARD_START_X + i * CELL_SIZE, BOARD_START_Y + BOARD_WIDTH)
            pygame.draw.line(self.screen, BLACK, start_pos, end_pos, 1)
        
        # 绘制星位
        star_points = [(3, 3), (3, 11), (11, 3), (11, 11), (7, 7)]
        for row, col in star_points:
            x = BOARD_START_X + col * CELL_SIZE
            y = BOARD_START_Y + row * CELL_SIZE
            pygame.draw.circle(self.screen, BLACK, (x, y), 4)
        
        # 绘制坐标标签
        for i in range(BOARD_SIZE):
            # 横坐标 A-O
            label = chr(65 + i)
            text = self.small_font.render(label, True, DARK_BROWN)
            x = BOARD_START_X + i * CELL_SIZE - text.get_width() // 2
            y = BOARD_START_Y + BOARD_WIDTH + 10
            self.screen.blit(text, (x, y))
            
            # 纵坐标 1-15
            label = str(15 - i)
            text = self.small_font.render(label, True, DARK_BROWN)
            x = BOARD_START_X - 30
            y = BOARD_START_Y + i * CELL_SIZE - text.get_height() // 2
            self.screen.blit(text, (x, y))
    
    def draw_stones(self):
        """绘制棋子"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col]:
                    x = BOARD_START_X + col * CELL_SIZE
                    y = BOARD_START_Y + row * CELL_SIZE
                    
                    # 绘制阴影
                    shadow_surf = pygame.Surface((CELL_SIZE * 2, CELL_SIZE * 2), pygame.SRCALPHA)
                    pygame.draw.circle(shadow_surf, (0, 0, 0, 40), 
                                     (CELL_SIZE, CELL_SIZE), CELL_SIZE // 2 - 2)
                    self.screen.blit(shadow_surf, (x - CELL_SIZE + 3, y - CELL_SIZE + 3))
                    
                    # 绘制棋子
                    if self.board[row][col] == "black":
                        pygame.draw.circle(self.screen, BLACK, (x, y), CELL_SIZE // 2 - 2)
                        pygame.draw.circle(self.screen, (50, 50, 50), 
                                         (x - 5, y - 5), CELL_SIZE // 4, 2)
                    else:
                        pygame.draw.circle(self.screen, WHITE, (x, y), CELL_SIZE // 2 - 2)
                        pygame.draw.circle(self.screen, (80, 80, 80), (x, y), CELL_SIZE // 2 - 2, 1)
                        pygame.draw.circle(self.screen, (245, 245, 245), 
                                         (x - 5, y - 5), CELL_SIZE // 4, 2)
                    
                    # 标记最后一步
                    if self.last_move == (row, col):
                        color = RED if self.board[row][col] == "black" else ORANGE
                        pygame.draw.rect(self.screen, color, 
                                       (x - 5, y - 5, 10, 10), 2)
    
    def draw_hover(self):
        """绘制鼠标悬停效果"""
        if self.hover_pos and self.game_state == "PLAYING" and not self.ai_thinking:
            row, col = self.hover_pos
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and not self.board[row][col]:
                if self.current_turn == self.player_color:
                    x = BOARD_START_X + col * CELL_SIZE
                    y = BOARD_START_Y + row * CELL_SIZE
                    
                    # 半透明预览
                    s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    color = (0, 0, 0, 80) if self.current_turn == "black" else (255, 255, 255, 80)
                    pygame.draw.circle(s, color, (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 2 - 2)
                    self.screen.blit(s, (x - CELL_SIZE // 2, y - CELL_SIZE // 2))
                    
                    # 十字准星
                    pygame.draw.line(self.screen, RED, (x - 10, y), (x + 10, y), 1)
                    pygame.draw.line(self.screen, RED, (x, y - 10), (x, y + 10), 1)
    
    def draw_menu(self):
        """绘制主菜单"""
        # 标题背景
        title_bg = pygame.Rect(200, 100, 500, 120)
        pygame.draw.rect(self.screen, WHITE, title_bg, border_radius=15)
        pygame.draw.rect(self.screen, DARK_BROWN, title_bg, 3, border_radius=15)
        
        # 标题
        title = self.title_font.render(self.get_text('title'), True, DARK_BROWN)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 160))
        self.screen.blit(title, title_rect)
        
        # 副标题
        subtitle = self.font.render(self.get_text('subtitle'), True, GRAY)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)
        
        # 提示文字
        prompt = self.large_font.render(self.get_text('choose'), True, BLACK)
        prompt_rect = prompt.get_rect(center=(WINDOW_WIDTH // 2, 290))
        self.screen.blit(prompt, prompt_rect)
        
        # 按钮
        mouse_pos = pygame.mouse.get_pos()
        
        # 黑棋按钮
        black_hover = self.black_button.collidepoint(mouse_pos)
        black_color = (240, 240, 240) if black_hover else WHITE
        pygame.draw.rect(self.screen, black_color, self.black_button, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, self.black_button, 3 if black_hover else 2, border_radius=10)
        
        pygame.draw.circle(self.screen, BLACK, 
                         (self.black_button.x + 35, self.black_button.centery), 16)
        text = self.large_font.render(self.get_text('black'), True, BLACK)
        text_rect = text.get_rect(center=(self.black_button.x + 90, self.black_button.centery))
        self.screen.blit(text, text_rect)
        
        # 白棋按钮
        white_hover = self.white_button.collidepoint(mouse_pos)
        white_color = (240, 240, 240) if white_hover else WHITE
        pygame.draw.rect(self.screen, white_color, self.white_button, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, self.white_button, 3 if white_hover else 2, border_radius=10)
        
        pygame.draw.circle(self.screen, WHITE, 
                         (self.white_button.x + 35, self.white_button.centery), 16)
        pygame.draw.circle(self.screen, BLACK, 
                         (self.white_button.x + 35, self.white_button.centery), 16, 2)
        text = self.large_font.render(self.get_text('white'), True, BLACK)
        text_rect = text.get_rect(center=(self.white_button.x + 90, self.white_button.centery))
        self.screen.blit(text, text_rect)
        
        # 规则说明
        y_offset = 450
        rules = [
            self.get_text('rules'),
            self.get_text('rule1'),
            self.get_text('rule2'),
            self.get_text('rule3')
        ]
        
        for rule in rules:
            text = self.small_font.render(rule, True, GRAY)
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, rect)
            y_offset += 28
    
    def draw_sidebar(self):
        """绘制侧边栏信息"""
        # 侧边栏背景
        sidebar_rect = pygame.Rect(620, 80, 260, 540)
        pygame.draw.rect(self.screen, WHITE, sidebar_rect, border_radius=10)
        pygame.draw.rect(self.screen, GRAY, sidebar_rect, 2, border_radius=10)
        
        # 游戏信息标题
        title = self.font.render(self.get_text('info'), True, BLACK)
        title_rect = title.get_rect(center=(750, 110))
        self.screen.blit(title, title_rect)
        
        pygame.draw.line(self.screen, GRAY, (640, 135), (860, 135), 1)
        
        # 当前回合信息
        y_offset = 155
        
        # 显示当前状态
        if not self.ai_thinking:
            if self.current_turn == self.player_color:
                status_text = self.get_text('your_turn')
                status_color = GREEN
            else:
                status_text = self.get_text('ai_thinking')
                status_color = ORANGE
        else:
            self.thinking_timer += 1
            if self.thinking_timer % 30 == 0:
                self.thinking_dots = (self.thinking_dots + 1) % 4
            dots = "." * self.thinking_dots
            status_text = self.get_text('ai_thinking') + dots
            status_color = ORANGE
        
        text = self.font.render(status_text, True, status_color)
        self.screen.blit(text, (640, y_offset))
        
        # 当前执子方
        y_offset += 35
        if self.current_turn == "black":
            pygame.draw.circle(self.screen, BLACK, (660, y_offset + 10), 9)
            text = self.font.render(self.get_text('black_move'), True, BLACK)
        else:
            pygame.draw.circle(self.screen, WHITE, (660, y_offset + 10), 9)
            pygame.draw.circle(self.screen, BLACK, (660, y_offset + 10), 9, 1)
            text = self.font.render(self.get_text('white_move'), True, BLACK)
        self.screen.blit(text, (680, y_offset))
        
        # 分隔线
        y_offset += 35
        pygame.draw.line(self.screen, LIGHT_GRAY, (640, y_offset), (860, y_offset), 1)
        
        # 对战双方
        y_offset += 20
        text = self.font.render(self.get_text('vs'), True, BLACK)
        self.screen.blit(text, (640, y_offset))
        
        # 按钮
        mouse_pos = pygame.mouse.get_pos()
        
        # 重新开始按钮
        restart_hover = self.restart_button.collidepoint(mouse_pos)
        restart_color = (240, 240, 240) if restart_hover else WHITE
        pygame.draw.rect(self.screen, restart_color, self.restart_button, border_radius=5)
        pygame.draw.rect(self.screen, GREEN, self.restart_button, 2, border_radius=5)
        text = self.font.render(self.get_text('restart'), True, GREEN)
        text_rect = text.get_rect(center=self.restart_button.center)
        self.screen.blit(text, text_rect)
        
        # 返回菜单按钮
        back_hover = self.back_button.collidepoint(mouse_pos)
        back_color = (240, 240, 240) if back_hover else WHITE
        pygame.draw.rect(self.screen, back_color, self.back_button, border_radius=5)
        pygame.draw.rect(self.screen, BLUE, self.back_button, 2, border_radius=5)
        text = self.font.render(self.get_text('menu'), True, BLUE)
        text_rect = text.get_rect(center=self.back_button.center)
        self.screen.blit(text, text_rect)
        
        # 游戏提示
        y_offset = 400
        pygame.draw.line(self.screen, LIGHT_GRAY, (640, y_offset), (860, y_offset), 1)
        
        y_offset += 20
        text = self.small_font.render(self.get_text('tips'), True, BLACK)
        self.screen.blit(text, (640, y_offset))
        
        tips = [
            self.get_text('tip1'),
            self.get_text('tip2'),
            self.get_text('tip3')
        ]
        
        y_offset += 25
        for tip in tips:
            text = self.small_font.render(tip, True, GRAY)
            self.screen.blit(text, (640, y_offset))
            y_offset += 22
    
    def draw_winner(self):
        """绘制获胜信息"""
        if self.winner:
            # 半透明遮罩
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # 动画
            self.animation_time += 0.05
            scale = 1 + 0.2 * abs(pygame.math.Vector2(0, 1).rotate(self.animation_time * 100).y)
            
            # 结果框
            box_rect = pygame.Rect(250, 250, 400, 200)
            pygame.draw.rect(self.screen, WHITE, box_rect, border_radius=20)
            
            # 显示结果
            if self.winner == self.player_color:
                text = self.get_text('win')
                color = GREEN
                border_color = GOLD
            elif self.winner == "draw":
                text = self.get_text('draw')
                color = BLUE
                border_color = BLUE
            else:
                text = self.get_text('lose')
                color = RED
                border_color = RED
            
            pygame.draw.rect(self.screen, border_color, box_rect, 5, border_radius=20)
            
            # 文字
            win_text = self.large_font.render(text, True, color)
            win_rect = win_text.get_rect(center=(450, 330))
            self.screen.blit(win_text, win_rect)
            
            # 提示
            hint = self.small_font.render("Click button to continue", True, GRAY)
            hint_rect = hint.get_rect(center=(450, 380))
            self.screen.blit(hint, hint_rect)
    
    def get_board_pos(self, mouse_pos):
        """将鼠标位置转换为棋盘坐标"""
        x, y = mouse_pos
        col = round((x - BOARD_START_X) / CELL_SIZE)
        row = round((y - BOARD_START_Y) / CELL_SIZE)
        
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            board_x = BOARD_START_X + col * CELL_SIZE
            board_y = BOARD_START_Y + row * CELL_SIZE
            distance = ((x - board_x) ** 2 + (y - board_y) ** 2) ** 0.5
            if distance <= CELL_SIZE // 2:
                return row, col
        return None
    
    def ai_think_thread(self, row, col):
        """AI思考线程"""
        try:
            board_str = self.ai.make_move(row, col, self.player_color)
            self.ai_move_result = board_str
        except Exception as e:
            print(f"AI error: {e}")
            self.ai_move_result = None
    
    def make_player_move(self, row, col):
        """玩家下棋"""
        if self.board[row][col] is None and self.current_turn == self.player_color and not self.ai_thinking:
            self.board[row][col] = self.player_color
            self.last_move = (row, col)
            self.current_turn = self.ai_color
            
            self.ai_thinking = True
            self.ai_move_result = None
            self.ai_thread = threading.Thread(target=self.ai_think_thread, args=(row, col))
            self.ai_thread.daemon = True
            self.ai_thread.start()
    
    def check_ai_move(self):
        """检查AI是否完成思考"""
        if self.ai_thinking and self.ai_move_result is not None:
            self.ai_thinking = False
            
            if self.ai_move_result:
                self.parse_ai_board(self.ai_move_result)
            
            self.check_game_over()
            
            if not self.winner:
                self.current_turn = self.player_color
    
    def parse_ai_board(self, board_str):
        """解析AI返回的棋盘字符串"""
        lines = board_str.strip().split('\n')
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == 'B':
                    if self.board[i][j] != "black":
                        self.board[i][j] = "black"
                        if (i, j) != self.last_move:
                            self.last_move = (i, j)
                elif char == 'W':
                    if self.board[i][j] != "white":
                        self.board[i][j] = "white"
                        if (i, j) != self.last_move:
                            self.last_move = (i, j)
                else:
                    self.board[i][j] = None
    
    def check_game_over(self):
        """检查游戏是否结束"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col]:
                    color = self.board[row][col]
                    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
                    for dr, dc in directions:
                        count = 1
                        r, c = row + dr, col + dc
                        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == color:
                            count += 1
                            r += dr
                            c += dc
                        r, c = row - dr, col - dc
                        while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == color:
                            count += 1
                            r -= dr
                            c -= dc
                        
                        if count >= 5:
                            self.winner = color
                            self.game_state = "GAME_OVER"
                            return
        
        if all(self.board[i][j] is not None for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
            self.winner = "draw"
            self.game_state = "GAME_OVER"
    
    def reset_game(self):
        """重置游戏"""
        if self.ai_thread and self.ai_thread.is_alive():
            self.ai_thread.join(timeout=0.1)
        
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.ai = create_ai()
        clear_board(self.ai)
        self.current_turn = "black"
        self.winner = None
        self.last_move = None
        self.message = ""
        self.animation_time = 0
        self.ai_thinking = False
        self.ai_move_result = None
        self.thinking_timer = 0
        self.thinking_dots = 0
        self.game_state = "PLAYING"
        
        if self.ai_color == "black":
            self.current_turn = "black"
            self.ai_thinking = True
            self.ai_thread = threading.Thread(target=self.ai_first_move)
            self.ai_thread.daemon = True
            self.ai_thread.start()
    
    def ai_first_move(self):
        """AI先手"""
        time.sleep(0.5)
        self.board[7][7] = "black"
        self.last_move = (7, 7)
        self.ai_thinking = False
        self.current_turn = "white"
    
    def handle_menu_click(self, pos):
        """处理菜单点击"""
        if self.black_button.collidepoint(pos):
            self.player_color = "black"
            self.ai_color = "white"
            self.game_state = "PLAYING"
            self.reset_game()
        elif self.white_button.collidepoint(pos):
            self.player_color = "white"
            self.ai_color = "black"
            self.game_state = "PLAYING"
            self.reset_game()
    
    def handle_game_click(self, pos):
        """处理游戏点击"""
        if self.restart_button.collidepoint(pos):
            self.reset_game()
        elif self.back_button.collidepoint(pos):
            if self.ai_thread and self.ai_thread.is_alive():
                self.ai_thread.join(timeout=0.1)
            self.game_state = "MENU"
            return
        
        if self.current_turn == self.player_color and not self.winner and not self.ai_thinking:
            board_pos = self.get_board_pos(pos)
            if board_pos:
                row, col = board_pos
                self.make_player_move(row, col)
    
    def run(self):
        """主游戏循环"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.ai_thread and self.ai_thread.is_alive():
                        self.ai_thread.join(timeout=0.1)
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == "MENU":
                        self.handle_menu_click(event.pos)
                    elif self.game_state in ["PLAYING", "GAME_OVER"]:
                        self.handle_game_click(event.pos)
                elif event.type == pygame.MOUSEMOTION:
                    if self.game_state == "PLAYING":
                        self.hover_pos = self.get_board_pos(event.pos)
            
            if self.game_state == "PLAYING":
                self.check_ai_move()
            
            self.draw_gradient_background()
            
            if self.game_state == "MENU":
                self.draw_menu()
            else:
                self.draw_board()
                self.draw_hover()
                self.draw_stones()
                self.draw_sidebar()
                if self.game_state == "GAME_OVER":
                    self.draw_winner()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()


def main():
    game = GomokuGame()
    game.run()


if __name__ == "__main__":
    main()

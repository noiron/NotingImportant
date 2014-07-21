# -*- coding:utf8 -*-

class Tetris(object):
    W = 12      # board区域横向多少个格子
    H = 20      # 纵向多少个格子
    TILEW = 20  # 每个格子的高、宽的像素数
    START =  (100, 20)  # board在屏幕上的位置
    SPACE = 1000    # 方块在多少毫秒内会落下

    def __init__(self, screen):
        self.stat = "game"
        self.WIDTH = self.TILEW * self.W
        self.HEIGHT = self.TILEW * self.H
        self.screen = screen
        # board数组，空则为None
        self.board = []
        for i in xrange(self.H):
            line = [ None ] * self.W
            self.board.append(line)
        # 一些需要显示的信息
        self.level = 1
        self.killed = 0
        self.score = 0
        # 多少毫秒后会落下，当然在init里肯定是不变的（level总是一）
        self.time = self.SPACE * 0.8 ** (self.level - 1)
        # 这个保存自从上一次落下后经历的时间
        self.elapsed = 0
        # used for judge pressed firstly or for a long time
        self.pressing = 0
        # 当前的shape
        self.shape = Shape(self.START, (self.WIDTH, self.HEIGHT),
            (self.W, self.H))
        # shape需要知道周围世界的事情
        self.shape.set_board(self.board)
        # 这个是“世界”的“快照”
        self.board_image = pygame.Surface((self.WIDTH, self.HEIGHT))
        # 做一些初始化的绘制
        self.screen.blit(pygame.image.load(util.file_path("background.jpg")).convert(),
            (0, 0))
        self.display_info()
            

    def update(self, elapse):
        # 在游戏阶段，每次都会调用这个，用来接受输入，更新画面
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                self.pressing = 1   # 一按下，记录“我按下了”，然后就移动
                self.move(e.key == K_UP, e.key == K_DOWN, 
                    e.key == K_LEFT, e.key == K_RIGHT)
                if e.key == K_ESCAPE:
                    self.stat = 'menu'
            elif e.type == KEYUP and self.pressing:
                self.pressing = 0   # 如果释放，就撤销“我按下了”的状态
            elif e.type == QUIT:
                self.stat = 'quit'
        if self.pressing:
            pressed = pygame.key.get_pressed()  # 把按键状态交给move
            self.move(pressed[K_UP], pressed[K_DOWN],
                pressed[K_LEFT], pressed[K_RIGHT])
        self.elapsed += elapse  # 这里是在指定时间后让方块自动落下
        if self.elapsed >= self.time:
            self.next() 
            self.elapsed = self.elapsed - self.time
            self.draw()
        return self.stat



    def move(self, u, d, l, r):
        # 控制当前方块的状态
        pass

    def check_line(self):
        # 判断已经落下方块的状态，然后调用kill_line
        pass

    def kill_line(self, filled = []):
        # 删除填满的行，需要播放个消除动画 
        if len(filled)  == 0:
            return

        mask = pygame.Surface((self.WIDTH, self.TILEW), SRCALPHA, 32)
        for i in xrange(5):
            if i % 2 == 0:
                # 比较透明
                mask.fill((255, 255, 255, 100))
            else:
                # 比较不透明
                mask.fill((255, 255, 255, 200))
            self.screen.blit(self.board_image. self.START)
            # 覆盖在满的行上面
            for line in filled:
                self.screen.blit(mask, (
                    self.START[0],
                    self.START[1] + line * self.TILEW))
                pygame.display.update()
            pygame.time.wait(80)
        # 这里是使用删除填满的行再在顶部填空行的方式
        [self.board.pop(l) for l in sorted(filled, reverse = True)]
        [self.board.insert(0, [None] * self.W) for l in filled]
        self.get_score(len(filled))


    def get_score(self, num):
        # 计算得分
        pass

    def add_to_board(self):
        # 将触底的方块加入到board数组中
        pass

    def create_board_image(self):
        # 创造出一个稳定方块的图像
        pass

    def next(self):
        # 产生下一个方块
        pass

    def draw(self):
        # 把当前状态画出来
        pass

    def display_info(self):
        # 显示各种信息（分数，等级等），调用下面的_display***
        pass

    def _display_score(self):
        pass 

    def _display_next(self):
        pass

    def game_over(self):
        # 游戏结束
        pass



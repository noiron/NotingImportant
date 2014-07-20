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
            

    def update(self, elapse):
        # 在游戏阶段，每次都会调用这个，用来接受输入，更新画面
        pass

    def move(self, u, d, l, r):
        # 控制当前方块的状态
        pass

    def check_line(self):
        # 判断已经落下方块的状态，然后调用kill_line
        pass

    def kill_line(self, filled = []):
        # 删除填满的行，需要播放个消除动画 

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



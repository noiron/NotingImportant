# -*- coding:utf8 -*-

class Shape(object):
    # shape是画在一个矩阵上面的
    # 因为我们有不同的模式，所以矩阵的信息也要详细给出
    SHAPEW = 4  # 这个是矩阵的宽度
    SHAPEH = 4  # 这个是高度
    SHAPES = (
        (   ((0,0,0,),
             (0,1,1,0),
             (0,1,1,0),
             (0,0,0,0),),
        )
        # 还有其他图形，省略
        )，
    COLORS = ((0xcc, 0x66, 0x66),   # 各个shape的颜色
        )

    def __init__(self, board_start, (board_width, board_height), (w, h)):
        self.start = board_start
        self.W, self.H = w, h
        self.length = board_width / w   # 一个tille的长宽（正方形）
        self.x, self.y = 0, 0   # shape的起始位置
        self.index = 0          # 当前shape在SHAPES内的索引
        self.indexN = 0         # 下一个shape在SHAPES内的索引
        self.subindex = 0       # shape是在怎样的一个朝向
        self.shapes = []        # 记录当前shape可能的朝向
        self.color = () 
        self.shape = None
        # 这两个Surface用来存放

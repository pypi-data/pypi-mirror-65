from src.validators import ints_gt_0


class Size:
    def __init__(self, width: int, height: int):
        ints_gt_0(width, height)
        self.width = width
        self.height = height

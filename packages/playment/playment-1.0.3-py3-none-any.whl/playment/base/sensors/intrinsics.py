class Intrinsics:
    def __init__(self, cx: float, cy: float, fx: float, fy: float, k1: float, k2: float,
                 k3: float, k4: float, p1: float, p2: float, skew: float, scale_factor: float):
        self.cx = cx
        self.cy = cy
        self.fx = fx
        self.fy = fy
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.k4 = k4
        self.p1 = p1
        self.p2 = p2
        self.skew = skew
        self.scale_factor = scale_factor

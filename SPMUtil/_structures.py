import numpy as np
from matplotlib.patches import Rectangle


class Rect2D:

    def __str__(self):
        return "left_bottom:" + str(self.points) + ", window_size: (" + str(self.xbox) + ", " + str(self.ybox) + ")"

    def __init__(self, points=(0,0), xbox=1, ybox=1):
        # if points[0] < 0:
        #     points[0] = 0
        # if points[1] < 0:
        #     points[1] = 0
        if xbox < 1:
            xbox = 1
        if ybox < 1:
            ybox = 1
        self.points = (int(points[0]), int(points[1]))
        self.xbox = int(xbox)
        self.ybox = int(ybox)


    def extract_2d_map_from_rect(self, map: np.ndarray):
        x_point, y_point = self.points[0], self.points[1]
        return map[y_point:y_point+self.ybox, x_point:x_point+self.xbox]

    def draw_rect_patch_on_matplot(self, ax):
        _rect = Rectangle(self.points, self.xbox, self.ybox, linewidth=1, edgecolor="r", facecolor="none")
        ax.add_patch(_rect)

    @staticmethod
    def get_random_rect(data: np.ndarray, x_box_min, x_box_max, y_box_min, y_box_max, fixed_center=None):
        if len(data.shape) != 2:
            raise ValueError("Wrong Data Shape")
        size = (np.random.uniform(low=x_box_min, high=x_box_max, size=1),
                np.random.uniform(low=y_box_min, high=y_box_max, size=1))
        if fixed_center is None:
            points = np.random.uniform(low=0, high=data.shape[0]-size[0]), np.random.uniform(low=0, high=data.shape[1]-size[1])
        else:
            points = fixed_center[0] - size[0]/2, fixed_center[1] - size[1]/2

        return Rect2D(points, size[0], size[1])





class measurement_param:

    def __init__(self, max_z, data_count, f0=150000, k=25, amp=17):
        # resonance frequency Hz
        self.f0 = f0
        # spring constant N/m
        self.k = k
        # amplitude(Ang)
        self.amp = amp
        # ang
        self.max_z = max_z
        # force curve data count
        self.data_count = data_count
        # ang
        self.dh = max_z / (data_count - 1)
        # ang
        self.z = np.zeros(data_count)
        for i in range(0, data_count):
            self.z[i] = self.dh * i


class force_curve:

    def __init__(self, x, y):
        self.x = x
        self.y = y



class inflecion_point_param:

    def __init__(self, point):
        self.point = point # index
        self.s_factor = -1
        self.is_well_posed = (self.s_factor >= -1)
        self.wel_posed_boundary = 0 # with unit


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x + other, self.y + other)
        else:
            return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector2(self.x - other, self.y - other)
        else:
            return Vector2(self.x - other.x, self.y - other.y)

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    @staticmethod
    def zero():
        return Vector2(0., 0.)

    @staticmethod
    def distance(vec1, vec2) -> float:
        return np.sqrt(np.square(vec1.x - vec2.x) + np.square(vec1.y - vec2.y))

    @staticmethod
    def limited(value: float, range) -> bool:
        if range.x <= value <= range.y:
            return True
        else:
            return False


class Vector3:
    def __init__(self, _x, _y, _z):
        self.x = _x
        self.y = _y
        self.z = _z

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + "," + str(self.z) + ")"

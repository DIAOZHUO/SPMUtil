import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
from SPMUtil.structures.rect_2d import Rect2D


class LineSelector(object):
    def __init__(self, ax=None):
        self.ax = ax or plt.gca()
        self.line, _ = self.ax.plot(1, 1, 1, c="r")
        self.x = np.zeros(2)
        self.y = np.zeros(2)
        self.mouse_down = False

        self.ax.figure.canvas.mpl_connect('button_press_event', self._click)
        self.ax.figure.canvas.mpl_connect('button_release_event', self._release)
        self.ax.figure.canvas.mpl_connect("motion_notify_event", self._callback)

    def _click(self, event):
        if event.button is MouseButton.LEFT and not self.mouse_down:
            if event.xdata is not None and event.ydata is not None:
                self.x[0] = int(event.xdata)
                self.y[0] = int(event.ydata)
                self.mouse_down = True


    def _callback(self, event):
        if self.mouse_down and event.xdata is not None and event.ydata is not None:
            self.x[1] = int(event.xdata)
            self.y[1] = int(event.ydata)

        self.line.set_data(self.x, self.y)
        self.ax.figure.canvas.draw()

    def _release(self, event):
        if self.mouse_down and event.button is MouseButton.LEFT:
            if event.xdata is not None and event.ydata is not None:
                self.x[1] = int(event.xdata)
                self.y[1] = int(event.ydata)
                self.mouse_down = False
                self.line.set_data(self.x, self.y)
                self.ax.figure.canvas.draw()

    # from - to
    def select_line(self, map: np.ndarray):
        plt.title("please select a line and close this window.")
        plt.imshow(map)
        plt.show()
        pts = *self.x, *self.y
        return (pts[0], pts[2]), (pts[1], pts[3])



if __name__ == '__main__':
    map = np.random.random(size=(100, 100))
    region = LineSelector()
    import SPMUtil
    line = SPMUtil.formula.line_proline(map, *region.select_line(map))
    plt.plot(line)
    plt.show()

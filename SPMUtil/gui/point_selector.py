import numpy as np
import matplotlib.pyplot as plt


class PointSelector(object):
    def __init__(self, ax=None):
        self.ax = ax or plt.gca()
        self.sca = self.ax.scatter([], [], c="r")

        self.blc = np.zeros(2)
        self.im_active = False

        def selector(event):
            if event.key in ['Z', 'z'] and self.im_active:
                if len(self.point_list) > 0:
                    self.point_list.pop(len(self.point_list)-1)
                    self._update_canvas()

        self.ax.figure.canvas.mpl_connect('button_press_event', self._onclick)
        self.ax.figure.canvas.mpl_connect('key_press_event', selector)
        self.point_list = []

    def _update_canvas(self):
        self.sca.remove()
        if len(self.point_list) > 0:
            self.sca = self.ax.scatter(*zip(*self.point_list), c="r")
        else:
            self.sca = self.ax.scatter([], [], c="r")
        self.ax.figure.canvas.draw()

    def _onclick(self, event):
        X_coordinate = event.xdata
        Y_coordinate = event.ydata
        self.point_list.append([X_coordinate, Y_coordinate])
        self._update_canvas()


    def select_point(self, map: np.ndarray):
        self.point_list = []
        self.im_active = True
        plt.title("please select points and close this window.")
        plt.imshow(map)
        plt.show()
        self.im_active = False
        return self.point_list



if __name__ == '__main__':
    map = np.random.random(size=(100, 100))
    region = PointSelector()
    print(region.select_point(map))


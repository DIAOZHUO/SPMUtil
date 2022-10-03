import SPMUtil as spmu
import tkinter as tk
import asyncio
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class TiltCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tilt Calculator")
        self.protocol("WM_DELETE_WINDOW", self.close)
        frame1 = tk.Frame(self)
        frame1.pack()

        fig = plt.Figure()
        self._ax = fig.add_subplot(1, 1, 1)
        self._fig_canvas = FigureCanvasTkAgg(fig, frame1)
        self._fig_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        frame2 = tk.Frame(self)
        frame2.pack()
        self.min_limit = tk.DoubleVar()
        self.max_limit = tk.DoubleVar()
        self.min_limit.set(-1)
        self.max_limit.set(1)
        self.min_limit.trace_add("write", self._on_limit_value_change)
        self.max_limit.trace_add("write", self._on_limit_value_change)

        tk.Entry(frame2, textvariable=self.min_limit).grid(row=0, column=0)
        tk.Entry(frame2, textvariable=self.max_limit).grid(row=0, column=2)
        self.scale_var = tk.DoubleVar()
        self.scale = tk.Scale(frame2, variable=self.scale_var, command=self._slider_scroll, orient=tk.HORIZONTAL,
                          length=300, width=20, sliderlength=20,
                          from_=self.min_limit.get(), to=self.max_limit.get(),
                          resolution=(self.max_limit.get()-self.min_limit.get())/10000)
        self.scale.grid(row=0, column=1)

        button1 = tk.Button(frame2, text="Auto", command=self._on_auto_button_click)
        button1.grid(row=1, column=1)
        button2 = tk.Button(frame2, text="Apply", command=self._on_apply_button_click)
        button2.grid(row=1, column=2)

        self.line, self.line_x = np.ndarray(0), np.ndarray(0)
        self._output_ready = False
        self._callback = None
        self._tilt_result = (0,0)
        self._rot_idx = 0
        self.param = spmu.PythonScanParam()

    def _on_limit_value_change(self, *arg):
        try:
            self.scale.configure(from_=self.min_limit.get(), to=self.max_limit.get(),
                                 resolution=(self.max_limit.get()-self.min_limit.get())/10000)
        except:
            pass

    def _on_apply_button_click(self):
        v = self.scale_var.get()
        if self._rot_idx % 4 == 0:
            self._tilt_result = v / (self.param.Aux1MaxVoltage - self.param.Aux1MinVoltage), 0
        elif self._rot_idx % 4 == 1:
            self._tilt_result = 0, v / (self.param.Aux2MaxVoltage - self.param.Aux2MinVoltage)
        elif self._rot_idx % 4 == 2:
            self._tilt_result = v / (self.param.Aux1MinVoltage - self.param.Aux1MaxVoltage), 0
        else:
            self._tilt_result = 0, v / (self.param.Aux2MinVoltage - self.param.Aux2MaxVoltage)

        if not self._callback is None:
            self._callback(self._tilt_result)
            self._callback = None

        self._run = False
        self.destroy()

    def _on_auto_button_click(self):
        coef = np.polyfit(self.line_x, self.line, 1)
        self.scale_var.set(coef[0])
        self._slider_scroll(None)

    def _slider_scroll(self, event=None):
        self._ax.clear()
        self._ax.plot(self.line - self.line_x * self.scale_var.get())
        self._fig_canvas.draw()

    def calc_tilt(self, line, param: spmu.PythonScanParam, callback=None):
        self._callback = callback

        rot_idx = param.ZRotation // 90
        if param.Aux1Type == "X" and param.Aux2Type == "Y":
            pass
        elif param.Aux1Type == "Y" and param.Aux2Type == "X":
            rot_idx += 1
        else:
            raise ValueError("Unsupported Python Param Setting")

        self._rot_idx = rot_idx
        self.line = line
        self.param = param
        self.line_x = np.linspace(0, 1, len(self.line))
        self._ax.plot(line)
        self._ax.get_xaxis().set_visible(False)

        line_value_range = np.max(line) - np.min(line)
        self.min_limit.set(-line_value_range / 2.0)
        self.max_limit.set(line_value_range / 2.0)

        self.mainloop()
        return self._tilt_result

    def calc_tilt_async(self, line, param: spmu.PythonScanParam, callback=None):
        self._callback = callback

        rot_idx = param.ZRotation // 90
        if param.Aux1Type == "X" and param.Aux2Type == "Y":
            pass
        elif param.Aux1Type == "Y" and param.Aux2Type == "X":
            rot_idx += 1
        else:
            raise ValueError("Unsupported Python Param Setting")

        self._rot_idx = rot_idx
        self.line = line
        self.param = param
        self.line_x = np.linspace(0, 1, len(self.line))
        self._ax.plot(line)
        self._ax.get_xaxis().set_visible(False)

        self._run = True
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._updater())



    async def _updater(self):
        while self._run:
            self.update()
            await asyncio.sleep(0.1)

    def close(self):
        self._run = False
        self.destroy()


if __name__ == '__main__':
    data = spmu.DataSerializer("./20220124_si110/248_20220124_si110_drift.pkl")
    data.load()
    param = spmu.PythonScanParam.from_dataSerilizer(data)
    print(param)
    tc = TiltCalculator()
    result = tc.calc_tilt(data.data_dict[spmu.cache_2d_scope.FWFW_ZMap.name][:, 100], param)
    print(result)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time, os
import uuid
import numpy as np
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog

import SPMUtil as spmu
from SPMUtil.gui.rangeSlider import RangeSlider
from SPMUtil.structures.scan_data_format import *




def json_tree(tree, parent, dictionary):
    for key in dictionary:
        uid = uuid.uuid4()
        if isinstance(dictionary[key], dict):
            tree.insert(parent, 'end', uid, text=key)
            json_tree(tree, uid, dictionary[key])
        elif isinstance(dictionary[key], list):
            tree.insert(parent, 'end', uid, text=key + '[]')
            json_tree(tree,
                                        uid,
                                        dict([(i, x) for i, x in enumerate(dictionary[key])]))
        else:
            value = dictionary[key]
            if value is None:
                value = 'None'
            tree.insert(parent, 'end', uid, text=key, value=value)



def clearFrame(frame, unpack_frame = True):
    # destroy all widgets from frame
    for widget in frame.winfo_children():
        widget.destroy()

    # this will clear frame and frame will be empty
    # if you want to hide the empty panel then
    if unpack_frame:
        frame.pack_forget()



class InspectorImageProcessingFrame(object):
    __callbacks = []
    __handle_enable = True

    def process_map(self, reset_range_bar=False):
        InspectorImageProcessingFrame.__handle_enable = False

        if self.flattenMode == self.flattenMode.Off:
            map = self.map_data
        elif self.flattenMode == self.flattenMode.Average:
            map = spmu.flatten_map(self.map_data, flatten=spmu.FlattenMode.Average)
        elif self.flattenMode == self.flattenMode.LinearFit:
            map = spmu.apply_flatten_plane(self.map_data, self.linearFitX, self.linearFitY)
        elif self.flattenMode == self.flattenMode.PolyFit:
            map = spmu.flatten_map(self.map_data, flatten=spmu.FlattenMode.PolyFit)
        else:
            map = self.map_data
            messagebox.showerror("error", "this mode is not in implement")

        map = spmu.filter_2d.SmoothMap(map, self.gaussianFilterCount)
        min, max = np.min(map), np.max(map)
        self.__rs.setLowerBound(min)
        self.__rs.setUpperBound(max)
        if reset_range_bar or self.will_range_bar_change:
            self.__rs.setLower(min)
            self.__rs.setUpper(max)
            self.will_range_bar_change = False

        self.__rs.setMajorTickSpacing((max - min) / 10)
        self.__rs.setMinorTickSpacing((max - min) / 100)
        map = np.clip(map, self.colorbarRangeMin, self.colorbarRangeMax)
        InspectorImageProcessingFrame.__handle_enable = True
        return map




    def update_map_data(self, map_data):
        print("map_data update")
        InspectorImageProcessingFrame.__handle_enable = False
        self.map_data = map_data
        min, max = np.min(self.map_data), np.max(self.map_data)
        self.__rs.setLowerBound(min)
        self.__rs.setUpperBound(max)
        self.__rs.setLower(min)
        self.__rs.setUpper(max)
        self.__rs.setMajorTickSpacing((max - min) / 10)
        self.__rs.setMinorTickSpacing((max - min) / 100)
        InspectorImageProcessingFrame.__handle_enable = True


    def __init__(self, root_widget, map_data):
        self.map_data = map_data

        self.gaussianFilterCount = 1
        self.flattenMode = spmu.FlattenMode.Off
        self.linearFitX = 0.0
        self.linearFitY = 0.0
        self.colorbarRangeMax = 1
        self.colorbarRangeMin = 0
        self.__rs = None
        self.root_widget = root_widget

        self.__lowerEntryString = StringVar()
        self.__upperEntryString = StringVar()
        self.__gaussianFilterEntryString = IntVar()
        self.__gaussianFilterEntryString.set(1)
        self.__xtiltEntryString = StringVar()
        self.__ytiltEntryString = StringVar()

        self.__rs = RangeSlider(self.root_widget, lowerBound=-1, upperBound=1, initialLowerBound=self.colorbarRangeMin, initialUpperBound=self.colorbarRangeMax)
        self.__rs.config(width=650, height=80)
        self.__rs.setPaintTicks(True)
        self.__rs.setSnapToTicks(False)
        self.__rs.setFocus()
        self.__rs.pack(side=TOP)


        frame2 = Frame(self.root_widget)
        frame2.pack()
        self.__xtiltValueLabel = Label(frame2, text="Xtilt Value")
        self.__xtiltValueEntry = Entry(frame2, textvariable=self.__xtiltEntryString)
        self.__xtiltEntryString.trace("w", self.__xtiltEntry_onChange)
        self.__ytiltValueLabel = Label(frame2, text="Ytilt Value")
        self.__ytiltValueEntry = Entry(frame2, textvariable=self.__ytiltEntryString)
        self.__ytiltEntryString.trace("w", self.__ytiltEntry_onChange)
        self.__calcTiltButton = Button(frame2, text='calc tilt',command=self.on_button_calcTilt_clicked)

        self.__xtiltValueLabel.pack(side=LEFT)
        self.__xtiltValueEntry.pack(side=LEFT)
        self.__ytiltValueLabel.pack(side=LEFT)
        self.__ytiltValueEntry.pack(side=LEFT)
        self.__calcTiltButton.pack(side=LEFT)

        frame3 = Frame(self.root_widget)
        frame3.pack()
        flatten_mode_string = [option.name for option in spmu.FlattenMode]
        self.flatten_name_option = StringVar(value=flatten_mode_string[0])
        Label(frame3, text='flatten method').pack(side=LEFT)
        OptionMenu(frame3, self.flatten_name_option, *flatten_mode_string).pack(side=LEFT)
        self.flatten_name_option.trace("w", self.on_flatten_option_change)


        frame1 = Frame(self.root_widget)
        frame1.pack()
        self.__minValueLabel = Label(frame1, text="Lower Value Limiter")
        self.__minValueEntry = Entry(frame1, textvariable=self.__lowerEntryString)
        self.__lowerEntryString.trace("w", self.__lowerEntry_onChange)
        self.__maxValueLabel = Label(frame1, text="Upper Value Limiter")
        self.__maxValueEntry = Entry(frame1, textvariable=self.__upperEntryString)
        self.__upperEntryString.trace("w", self.__upperEntry_onChange)

        self.__gaussianFilterLabel = Label(frame1, text="Gaussian Filter Count")
        self.__gaussianFilterValueEntry = Entry(frame1, textvariable=self.__gaussianFilterEntryString)
        self.__gaussianFilterEntryString.trace("w", self.__gaussianfilter_onChange)

        self.__gaussianFilterLabel.pack(side=LEFT)
        self.__gaussianFilterValueEntry.pack(side=LEFT)
        self.__minValueLabel.pack(side=LEFT)
        self.__minValueEntry.pack(side=LEFT)
        self.__maxValueEntry.pack(side=RIGHT)
        self.__maxValueLabel.pack(side=RIGHT)



        self.__rs.subscribe(self.slider_changeState)
        self.slider_changeState(None)

        # self.update_map_data(map_data)
        self.will_range_bar_change = False

    def subscribe(self, callback):
        self.__callbacks.append(callback)

    def notify(self):
        for call in self.__callbacks:
            call()


    '''
    Event - slider change state
    - Binded to the notify event of our slider controller
    - This will be called whenever the slider changes
    '''

    def slider_changeState(self, e):
        if (self.root_widget.focus_displayof() != self.__minValueEntry):
            self.__minValueEntry.delete(0, END)
            self.__minValueEntry.insert(0, self.__rs.getLower())

        if (self.root_widget.focus_displayof() != self.__maxValueEntry):
            self.__maxValueEntry.delete(0, END)
            self.__maxValueEntry.insert(0, self.__rs.getUpper())




    def __upperEntry_onChange(self, e, a, mode):
        try:
            f = float(self.__upperEntryString.get())
            self.colorbarRangeMax = f
            if (f != self.__rs.getUpper()):
                self.__rs.setUpper(f)
            # if InspectorImageProcessingFrame.__handle_enable:
            #     self.notify()
        except:
            None

    def __lowerEntry_onChange(self, e, a, mode):
        try:
            f = float(self.__lowerEntryString.get())
            self.colorbarRangeMin = f
            if (f != self.__rs.getLower()):
                self.__rs.setLower(f)
            # if InspectorImageProcessingFrame.__handle_enable:
            #     self.notify()
        except:
            None

    def __gaussianfilter_onChange(self, e, a, mode):
        try:
            f = self.__gaussianFilterEntryString.get()
            if f < 1:
                f = 1
                self.__gaussianFilterEntryString.set(1)
            self.gaussianFilterCount = int(f)
        except:
            None

    def __xtiltEntry_onChange(self, e, a, mode):
        try:
            f = self.__xtiltEntryString.get()
            self.linearFitX = float(f)
        except:
            None

    def __ytiltEntry_onChange(self, e, a, mode):
        try:
            f = self.__ytiltEntryString.get()
            self.linearFitY = float(f)
        except:
            None


    def on_button_calcTilt_clicked(self, *args):
        coef_x, coef_y = spmu.get_flatten_param(self.map_data, flatten=spmu.FlattenMode.LinearFit)
        self.linearFitX = coef_x
        self.linearFitY = coef_y
        self.__xtiltEntryString.set(coef_x)
        self.__ytiltEntryString.set(coef_y)

    def on_flatten_option_change(self, *args):
        key = spmu.FlattenMode[self.flatten_name_option.get()]

        self.will_range_bar_change = True
        self.flattenMode = key
        self.notify()







class DataInspector(object):

    last_process_time = 0

    def __init__(self):

        self.window = Tk()
        self.window.title("Scan Data Inspector")
        self.window.bind('<Return>', self.on_enter_key_down)
        self.setting_dict = {}

        self.load_setting()


        self.v1 = StringVar()
        self.frame1 = Frame(self.window)
        self.pathLabel = Label(self.frame1, textvariable=self.v1).grid(row=0, column=0)
        self.openScanButtonButton = Button(self.frame1, text='Open Scan Data', width=15, command=self.on_button_openfile_clicked).grid(row=0, column=1)
        self.frame1.pack()

        self.dict_data_name_option = StringVar()
        self.xzp_data_file_option = StringVar()

        self.frame2 = Frame(self.window)
        self.frame2.pack()

        self.frame3 = Frame(self.window)
        self.frame3.pack()


        self.fig = plt.Figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        map = np.random.random((100, 100))
        plot = self.ax.imshow(map)
        self.cbar = self.fig.colorbar(plot)
        self.plot_2d_canvas = FigureCanvasTkAgg(self.fig, master=self.frame3)
        plt.show()
        self.plot_2d_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.plot_2d_canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)
        self.dict_tree_frame = ttk.Frame(self.frame3, padding="3")


        self.frame4VisibleButtonText = StringVar()
        self.frame4VisibleButtonText.set('▼')
        Button(self.window, textvariable=self.frame4VisibleButtonText, width=2, height=1,
               command=self.on_button_visible_clicked).pack()
        self.frame4 = Frame(self.window)
        # self.frame4.pack()

        self.hideOption = True

        self.IPFrame = InspectorImageProcessingFrame(self.frame4, map_data=map)
        self.IPFrame.subscribe(self.on_image_process_param_updated)

        self.dataSerializer = None
        self.dataSerializerPackage = None

    def main(self):
        self.window.mainloop()


    def on_button_visible_clicked(self, *args):
        self.hideOption = not self.hideOption
        if self.hideOption:
            self.frame4VisibleButtonText.set('▼')
            self.frame4.pack_forget()
        else:
            self.frame4VisibleButtonText.set('▲')
            self.frame4.pack()

    def on_xzp_data_name_option_change(self, *args):
        # print(self.xzp_data_file_option.get())
        data = self.dataSerializerPackage.get_dataSerializer(self.xzp_data_file_option.get())
        self.on_file_updates(data)
        # data = spmu.DataSerializer(self.xzp_data_file_option.get())
        # self.load_data(data)


    def on_data_name_option_change(self, *args):
        self.plot_2d_canvas.get_tk_widget().pack_forget()
        clearFrame(self.dict_tree_frame)

        # print(self.dict_data_name_option.get())
        key = self.dict_data_name_option.get()
        if key in [ScanDataHeader.GetKeyName(), StageConfigure.GetKeyName(),
                   PythonScanParam.GetKeyName(), HardwareConfigure.GetKeyName()]:
            dict_data = json.loads(self.dataSerializer.data_dict[key])

            tree = ttk.Treeview(self.dict_tree_frame, columns='Values')
            tree.column('Values', width=100, anchor='center')
            tree.heading('Values', text='Values')
            json_tree(tree, '', dict_data)
            tree.pack(fill=BOTH, expand=1)
            self.dict_tree_frame.pack()

        elif key == "ArrayBuilderParam":
            tree = ttk.Treeview(self.dict_tree_frame, columns='Values')
            tree.column('Values', width=100, anchor='center')
            tree.heading('Values', text='Values')
            json_tree(tree, '', self.dataSerializer.data_dict[key])
            tree.pack(fill=BOTH, expand=1)
            self.dict_tree_frame.pack()

        elif key in [option.name for option in cache_2d_scope]:
            map = np.array(self.dataSerializer.data_dict[key])
            self.IPFrame.update_map_data(map)
            self.on_image_process_param_updated(reset_range_bar=True)

            self.plot_2d_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
            self.plot_2d_canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

        elif key in [option.name for option in cache_1d_scope]:
            pass
        elif key == "click here to select data":
            pass
        else:
            if isinstance(self.dataSerializer.data_dict[key], str) and self.is_json(self.dataSerializer.data_dict[key]):
                dict_data = json.loads(self.dataSerializer.data_dict[key])
                tree = ttk.Treeview(self.dict_tree_frame, columns='Values')
                tree.column('Values', width=100, anchor='center')
                tree.heading('Values', text='Values')
                json_tree(tree, '', dict_data)
                tree.pack(fill=BOTH, expand=1)
                self.dict_tree_frame.pack()
            elif isinstance(self.dataSerializer.data_dict[key], dict):
                tree = ttk.Treeview(self.dict_tree_frame, columns='Values')
                tree.column('Values', width=100, anchor='center')
                tree.heading('Values', text='Values')
                json_tree(tree, '', self.dataSerializer.data_dict[key])
                tree.pack(fill=BOTH, expand=1)
                self.dict_tree_frame.pack()
            else:
                messagebox.showerror("error", "not supported data type: " + key)

    @staticmethod
    def is_json(myjson):
        try:
            json.loads(myjson)
        except ValueError as e:
            return False
        return True

    def on_button_openfile_clicked(self):
        file = filedialog.askopenfile(filetypes=[('data files', ['*.pkl', '*.xzp'])], initialdir=self.setting_dict['InitalFolderPath'])
        if file:
            fiilename, extension = os.path.splitext(file.name)
            if hasattr(self.xzp_data_file_option, "trace_id"):
                self.xzp_data_file_option.trace_vdelete("w", self.xzp_data_file_option.trace_id)
            if hasattr(self.dict_data_name_option, "trace_id"):
                self.dict_data_name_option.trace_vdelete("w", self.dict_data_name_option.trace_id)

            if extension == ".pkl":
                self.v1.set(file.name)
                data = spmu.DataSerializer(file.name)
                try:
                    data.load()
                    self.on_file_updates(data)
                except ValueError:
                    messagebox.showerror("error", "cannot read this file...")


            elif extension == ".xzp":
                self.v1.set(file.name)
                del self.dataSerializerPackage
                pack = spmu.DataSerializerPackage(file.name, custom_ext=".xzp")
                pack.load()

                OptionMenu(self.frame1, self.xzp_data_file_option, *pack.datas_name_list).grid(row=0, column=2)
                self.xzp_data_file_option.trace_id = \
                    self.xzp_data_file_option.trace("w", self.on_xzp_data_name_option_change)
                self.dataSerializerPackage = pack

            file.close()
            self.write_setting('InitalFolderPath', os.path.dirname(file.name))



    def on_file_updates(self, data: spmu.DataSerializer):
        self.dataSerializer = data
        self.plot_2d_canvas.get_tk_widget().pack_forget()
        clearFrame(self.frame2, unpack_frame=False)

        self.dict_data_name_option.set("click here to select data")
        Label(self.frame2, text='data name').grid(row=0, column=0)
        OptionMenu(self.frame2, self.dict_data_name_option, *data.data_dict.keys()).grid(row=0, column=1)
        self.dict_data_name_option.trace_id = self.dict_data_name_option.trace("w", self.on_data_name_option_change)


    def on_image_process_param_updated(self, reset_range_bar=False):
        # print("image updated")
        current_time = round(time.time() * 1000)
        if current_time - DataInspector.last_process_time < 500:
            return
        map = self.IPFrame.process_map(reset_range_bar=reset_range_bar)
        # print(reset_range_bar)
        config = StageConfigure.from_dataSerilizer(self.dataSerializer)
        param = PythonScanParam.from_dataSerilizer(self.dataSerializer)

        if self.dict_data_name_option.get() in [cache_2d_scope.FWFW_ZMap.name,
                                                cache_2d_scope.FWBW_ZMap.name,
                                                cache_2d_scope.BWFW_ZMap.name,
                                                cache_2d_scope.BWBW_ZMap.name]:

            if config.Z_Scan_Option == "Tube Scanner":
                map = map * float(self.setting_dict["TubeZ"])
            elif config.Z_Scan_Option == "High Speed Scanner":
                map = map * float(self.setting_dict["HSZ"])

        plot = self.ax.imshow(map, cmap="afmhot")


        xrange = np.abs(param.Aux1MaxVoltage - param.Aux1MinVoltage)
        yrange = np.abs(param.Aux2MaxVoltage - param.Aux2MaxVoltage)
        if config.XY_Scan_Option == 'Tube Scanner':
            self.ax.set_xticklabels(["0", str(round(xrange * float(self.setting_dict["TubeX"]), 4)) + "nm"])
            self.ax.set_yticklabels(["0", str(round(yrange * float(self.setting_dict["TubeY"]), 4)) + "nm"])
        elif config.XY_Scan_Option == "High Speed Scanner":
            self.ax.set_xticklabels(["0", str(round(xrange * float(self.setting_dict["HSX"]), 4)) + "nm"])
            self.ax.set_yticklabels(["0", str(round(yrange * float(self.setting_dict["HSY"]), 4)) + "nm"])



        self.cbar.update_normal(plot)
        self.plot_2d_canvas.draw()

        DataInspector.last_process_time = current_time




    def on_enter_key_down(self, e):
        self.IPFrame.notify()





    def load_setting(self):
        self.setting_dict.clear()
        if os.path.isfile("./DataInspectorSetting.ini"):
            with open("./DataInspectorSetting.ini") as f:
                for line in f.readlines():
                    strs = line.split("=")
                    if len(strs) > 1:
                        self.setting_dict[strs[0].replace(" ", "").replace("\n", "")] = strs[1].replace(" ", "").replace("\n", "")
        else:
            self.confirm_setting()

    def write_setting(self, key, value):
        if os.path.isfile("./DataInspectorSetting.ini"):
            with open("./DataInspectorSetting.ini", "r") as f:
                lines = f.readlines()
            with open("./DataInspectorSetting.ini", "w") as f:
                for line in lines:
                    if key in line:
                        f.write(key+"="+str(value)+"\n")
                    else:
                        f.write(line)
        else:
            self.confirm_setting()

    def confirm_setting(self):
        res = messagebox.askquestion("Generate Setting File", "can not find setting files (DataInspectorSetting.ini) at %s, do you want to generate it?" % os.path.abspath("./DataInspectorSetting.ini"))
        if res == 'yes':
            with open("./DataInspectorSetting.ini", "w") as f:
                f.write('[Gernal]\nInitalFolderPath=C:/\n2DMapKey=["Output_FW_ZMap", "Output_BW_ZMap"]\n[Calibration]\nTubeX = 21.85\nTubeY = 21.85\nTubeZ = 6.05\nHSX = 1\nHSY = 1\nHSZ = 1')

            messagebox.showinfo("Generate Setting File", "created setting file at %s." % os.path.abspath("./DataInspectorSetting.ini"))
            self.load_setting()
        else:
            pass


if __name__ == "__main__":
    DataInspector().main()


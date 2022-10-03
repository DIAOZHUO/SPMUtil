import json
import uuid
import tkinter as tk
import tkinter.ttk as ttk
import asyncio

class JsonEditor(tk.Tk):

    def __init__(self, show_private_member=True):
        super().__init__()
        self.title("JSON editor")
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.show_private_member = show_private_member

        self._int_options = {}
        self.uuid_value_name_dict = {}
        self.raw_dict = {}
        self.edit_dict = {}

        self.result_dict = {}
        self._callback = None
        self._run = False

    def EditDictAsync(self, m_dict: dict, IntOptions: dict=None, callback=None):
        self._build_edit_gui(m_dict, IntOptions, callback)
        self._run = True
        loop = asyncio.get_event_loop()
        # loop.create_task(self._updater(0.1))
        loop.run_until_complete(self._updater())


    def EditDict(self, m_dict: dict, IntOptions: dict=None, callback=None):
        self._build_edit_gui(m_dict, IntOptions, callback)
        self.mainloop()


    async def _updater(self):
        while self._run:
            self.update()
            await asyncio.sleep(0.1)

    def _close_ed(self, parent, edwin):
        parent.focus_set()
        edwin.destroy()


    def _set_cell(self, edwin, w, tvar):
        value = tvar.get()
        # print(self.uuid_value_name_dict[w.focus()], value)
        t = None
        try:
            t = type(self.raw_dict[self.uuid_value_name_dict[w.focus()]])
            if t is bool:
                assert (value == "0" or value == "1")
                value = int(value)
            self.edit_dict[self.uuid_value_name_dict[w.focus()]] = t(value)
            w.item(w.focus(), values=(value,))
        except:
            if t is not None:
                print("error type!", value, "can not be casted to", t)
            else:
                print("unknown error.")

        self._close_ed(w, edwin)


    def _edit_cell(self, e):
        w = e.widget
        if w and len(w.item(w.focus(), 'values')) > 0:
            edwin = tk.Toplevel(e.widget)
            edwin.protocol("WM_DELETE_WINDOW", lambda: self._close_ed(w, edwin))
            edwin.wait_visibility()
            edwin.grab_set()
            edwin.overrideredirect(1)
            opt_name = w.focus()
            (x, y, width, height) = w.bbox(opt_name, 'Values')
            edwin.geometry('%dx%d+%d+%d' % (width, height, x/4, y))
            value = w.item(opt_name, 'values')[0]
            tvar = tk.StringVar()
            tvar.set(str(value))
            ed = None

            if self.uuid_value_name_dict[opt_name] in self._int_options:
                constraints = self._int_options[self.uuid_value_name_dict[opt_name]]
                ed = tk.Spinbox(edwin, from_=constraints[0], to=constraints[1],
                                increment=constraints[2], textvariable=tvar)
            else:
                ed = tk.Entry(edwin, textvariable=tvar)
            if ed:
                ed.config(background='LightYellow')
                #ed.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W, tk.E))
                ed.pack()
                ed.focus_set()
            edwin.bind('<Return>', lambda e: self._set_cell(edwin, w, tvar))
            edwin.bind('<Escape>', lambda e: self._close_ed(w, edwin))


    def _JSONTree(self, Tree, Parent, Dictionary, show_private_member=True):
        for key in Dictionary:
            if not show_private_member and type(key) is str and key[0] == "_":
                continue

            uid = uuid.uuid4()
            self.uuid_value_name_dict[uid.__str__()] = key
            if isinstance(Dictionary[key], dict):
                Tree.insert(Parent, 'end', uid, text=key)
                self._JSONTree(Tree, uid, Dictionary[key], show_private_member)
            elif isinstance(Dictionary[key], list):
                Tree.insert(Parent, 'end', uid, text=key + '[]')
                self._JSONTree(Tree, uid, dict([(i, x) for i, x in enumerate(Dictionary[key])]), show_private_member)
            else:
                value = Dictionary[key]
                if isinstance(value, str) or isinstance(value, str):
                    value = value.replace(' ', '_')
                Tree.insert(Parent, 'end', uid, text=key, value=value)

    # opt_name: (from_, to, increment)
    # IntOptions = {
    #     'age': (1.0, 200.0, 1.0),
    # }
    def _build_edit_gui(self, m_dict: dict, IntOptions: dict = None, callback=None):
        self.raw_dict = m_dict.copy()
        self.edit_dict = m_dict
        self.uuid_value_name_dict.clear()
        self._callback = callback

        if IntOptions is not None:
            self._int_options = IntOptions

        # Setup the Frames
        TreeFrame = ttk.Frame(self, padding="3")
        TreeFrame.grid(row=0, column=0, sticky=tk.NSEW)

        # Setup the Tree
        tree = ttk.Treeview(TreeFrame, columns=('Values'))
        tree.column('Values', width=100, anchor='center')
        tree.heading('Values', text='Values')
        tree.bind('<Double-1>', self._edit_cell)
        tree.bind('<Return>', self._edit_cell)
        self._JSONTree(tree, '', m_dict, self.show_private_member)
        tree.pack(fill=tk.BOTH, expand=1)

        CancelButton = ttk.Button(self, text="Cancel", command=self.on_cancel_click)
        CancelButton.grid(row=1, column=0)
        OKButton = ttk.Button(self, text="Apply", command=self.on_apply_click)
        OKButton.grid(row=2, column=0)
        # Limit windows minimum dimensions
        self.update_idletasks()
        self.minsize(self.winfo_reqwidth(), self.winfo_reqheight())


    def on_cancel_click(self):
        self.result_dict = self.raw_dict
        self._run = False
        self.destroy()

    def on_apply_click(self):
        self.result_dict = self.edit_dict
        self._run = False
        if self._callback is not None:
            self._callback(self.result_dict)
        self.destroy()

    def close(self):
        self._run = False
        self.destroy()



if __name__ == "__main__" :

    def cb(a):
        print(333)

    IntOptions = {
        'age': (1.0, 200.0, 1.0),
    }

    Data = {
        "firstName": "John",
        "lastName": "Smith",
        "gender": "male",
        "age": 32,
        "address": {
            "streetAddress": "21 2nd Street",
            "city": "New York",
            "state": "NY",
            "postalCode": "10021"},
        "phoneNumbers": [
            {"type": "home", "number": "212 555-1234" },
            {"type": "fax",
             "number": "646 555-4567",
             "alphabet": [
                 "abc",
                 "def",
                 "ghi"]
             }
        ]}

    editor = JsonEditor()
    print(111)
    editor.EditDictAsync(Data, IntOptions, callback=cb)
    print(222)
    loop = asyncio.get_event_loop()
    loop.run_forever()

import tkinter as tk
import traceback

__version__ = "1.2.0"
debug = False

def debug_print(*args, **kwargs):
    if debug:
        print(*args, **kwargs)

class LabelList:
    """
    This class is used to record the label list.
    """
    def __init__(self):
        self.frame = None
        self.__start_label = None
        self.__end_label = None
        self.label_list = []
        self.last_idx = -1

    @property
    def start_label(self):
        return self.__start_label
    
    @start_label.setter
    def start_label(self, label: tk.Label):
        if self.__start_label is None:
            self.__start_label = label
            self.__start_label.pack(side=tk.LEFT, fill=tk.X)

    @property
    def end_label(self):
        return self.__end_label

    @end_label.setter
    def end_label(self, label: tk.Label):
        if self.__end_label is None:
            self.__end_label = label
            self.__end_label.pack(side=tk.LEFT, fill=tk.X)

    def add(self, idx, **kwargs):
        self.last_idx = idx
        if len(self.label_list) <= idx:
            self.label_list.append(tk.Label(**kwargs))
        else:
            if "fg" in kwargs:
                self.label_list[idx].config(fg=kwargs["fg"])
            if "bg" in kwargs:
                self.label_list[idx].config(bg=kwargs["bg"])
            if "text" in kwargs:
                self.label_list[idx].config(text=kwargs["text"])

    def complete(self):
        """
        This method is used to complete the label list.
        Pack the required label, and pack_forget the rest.
        """
        for idx in range(len(self.label_list)):
            if idx > self.last_idx:
                self.label_list[idx].pack_forget()
            else:
                self.label_list[idx].pack(side=tk.LEFT, fill=tk.X)
        self.__end_label.pack(side=tk.LEFT, fill=tk.X)

    def clear(self):
        """
        This method is used to pack_forget all the label in the label list.
        """
        for label in self.label_list:
            label.pack_forget()

class App(tk.Tk):
    """
    main window.
    """
    def __init__(self):
        super().__init__()
        self.title(f"HEX, DEC, BIN convert to IDX V{__version__}")
        width = 1200
        height = 200
        x = (self.winfo_screenwidth() - width) / 2
        y = (self.winfo_screenheight() - height) / 2
        self.geometry(f"{width}x{height}+{int(x)}+{int(y)}")

        self.default_bg_color = self.cget("bg")

        self.title_font = ("Consolas", 10)
        self.data_font = ("Consolas", 8)
        self.mode = ""

        self.result_frame_list = []
        self.label_class = [LabelList(), LabelList(), LabelList()]

        self.upper_frame = tk.Frame(self)
        self.upper_frame.pack(fill=tk.BOTH)
        self.upper_center_frame = tk.Frame(self.upper_frame)
        self.upper_center_frame.pack()
        self.bottom_frame = tk.Frame(self.upper_frame)
        self.bottom_frame.pack(fill=tk.BOTH)

        self.hex_label = tk.Label(self.upper_center_frame, text="  This app is used to convert HEX, DEC, BIN to IDX.                       ", font=self.title_font)
        self.hex_label.grid(row=0, column=0, columnspan=3, sticky="w")

        tk.Label(self.upper_center_frame, text="  Enter HEX Number: ", font=self.title_font).grid(row=1, column=0, sticky="w")
        self.hex_entry = tk.Entry(self.upper_center_frame, width=40)
        self.hex_entry.grid(row=1, column=1, sticky="w")
        self.hex_entry.bind("<KeyRelease>", lambda event: self.start_convert(event, "hex"))

        tk.Label(self.upper_center_frame, text="  Enter DEC Number: ", font=self.title_font).grid(row=2, column=0, sticky="w")
        self.dec_entry = tk.Entry(self.upper_center_frame, width=40)
        self.dec_entry.grid(row=2, column=1, sticky="w")
        self.dec_entry.bind("<KeyRelease>", lambda event: self.start_convert(event, "dec"))

        tk.Label(self.upper_center_frame, text="  Enter BIN Number: ", font=self.title_font).grid(row=3, column=0, sticky="w")
        self.bin_entry = tk.Entry(self.upper_center_frame, width=40)
        self.bin_entry.grid(row=3, column=1, sticky="w")
        self.bin_entry.bind("<KeyRelease>", lambda event: self.start_convert(event, "bin"))

        tk.Label(self.upper_center_frame, text="  Mark Start Index: ", font=self.title_font).grid(row=4, column=0, sticky="w")
        self.mark_start_entry = tk.Entry(self.upper_center_frame, width=5)
        self.mark_start_entry.grid(row=4, column=1, sticky="w")
        self.mark_start_entry.bind("<KeyRelease>", self.start_convert)

        tk.Label(self.upper_center_frame, text="  Mark End Index: ", font=self.title_font).grid(row=5, column=0, sticky="w")
        self.mark_end_entry = tk.Entry(self.upper_center_frame, width=5)
        self.mark_end_entry.grid(row=5, column=1, sticky="w")
        self.mark_end_entry.bind("<KeyRelease>", self.start_convert)

        self.warning_label = tk.Label(self.upper_center_frame, text="", font=self.title_font, fg="#AA0000")
        self.warning_label.grid(row=6, column=1, sticky="w")
        self.warning_msg = []

    def is_input_num_ok(self):
        flag = True
        mode = self.mode
        try:
            if mode == "hex" and self.hex_entry.get() != "":
                self.dec_entry.delete(0, tk.END)
                self.bin_entry.delete(0, tk.END)
                if int(self.hex_entry.get().lower().replace("0x", ""), 16) < 0:
                    self.warning_msg.append("HEX number must be positive.")
                    flag = False
        except Exception as e:
            debug_print(e)
            self.warning_msg.append("Invalid HEX number.")
            flag = False

        try:
            if mode == "dec" and self.dec_entry.get() != "":
                self.hex_entry.delete(0, tk.END)
                self.bin_entry.delete(0, tk.END)
                if int(self.dec_entry.get()) < 0:
                    self.warning_msg.append("DEC number must be positive.")
                    flag = False
        except Exception as e:
            debug_print(e)
            self.warning_msg.append("Invalid DEC number.")
            flag = False

        try:
            if mode == "bin" and self.bin_entry.get() != "":
                self.hex_entry.delete(0, tk.END)
                self.dec_entry.delete(0, tk.END)
                if int(self.bin_entry.get(), 2) < 0:
                    self.warning_msg.append("BIN number must be positive.")
                    flag = False
        except Exception as e:
            debug_print(e)
            self.warning_msg.append("Invalid BIN number.")
            flag = False

        return flag
    
    def is_mark_idx_ok(self):
        flag = True
        if self.mark_start_entry.get() != "" or self.mark_end_entry.get() != "":
            try:
                if int(self.mark_start_entry.get()) < 0:
                    self.warning_msg.append("Start index must be positive.")
                    flag = False
            except:
                self.warning_msg.append("Invalid start index.")
                flag = False

            try:
                if int(self.mark_end_entry.get()) < 0:
                    self.warning_msg.append("End index must be positive.")
                    flag = False
            except:
                self.warning_msg.append("Invalid end index.")
                flag = False

        return flag

    def show_warning(self):
        self.warning_label.config(text="\n".join(self.warning_msg))

    def get_mark_idx(self):
        try:
            if self.mark_start_entry.get() == "" and self.mark_end_entry.get() == "":
                return False, None, None

            start_idx = int(self.mark_start_entry.get())
            end_idx = int(self.mark_end_entry.get())

            if start_idx > end_idx:
                return True, end_idx, start_idx
            else:
                return True, start_idx, end_idx
        except:
            return False, None, None
        
    def start_convert(self, event=None, mode=None):
        if mode:
            self.mode = mode
        self.warning_label.config(text="")
        self.warning_msg = []
        self.convert()

    def convert(self, hex_num=None, dec_num=None, bin_num=None):
        is_input_num_ok = self.is_input_num_ok()
        if is_input_num_ok:
            if self.mode == "dec":
                dec_num = int(self.dec_entry.get())
                hex_num = hex(dec_num)[2:]
                bin_num = bin(dec_num)[2:]
                self.hex_entry.delete(0, tk.END)
                self.hex_entry.insert(0, f"0x{hex_num.upper()}")
                self.bin_entry.delete(0, tk.END)
                self.bin_entry.insert(0, bin_num)
            elif self.mode == "hex":
                hex_num = self.hex_entry.get().lower().replace("0x", "")
                dec_num = int(hex_num, 16)
                bin_num = bin(dec_num)[2:]
                self.dec_entry.delete(0, tk.END)
                self.dec_entry.insert(0, dec_num)
                self.bin_entry.delete(0, tk.END)
                self.bin_entry.insert(0, bin_num)
            elif self.mode == "bin":
                bin_num = self.bin_entry.get()
                hex_num = hex(int(bin_num, 2))[2:]
                dec_num = int(hex_num, 16)
                self.hex_entry.delete(0, tk.END)
                self.hex_entry.insert(0, f"0x{hex_num.upper()}")
                self.dec_entry.delete(0, tk.END)
                self.dec_entry.insert(0, dec_num)

            debug_print("Hex: ", hex_num)
            debug_print("Dec: ", dec_num)
            debug_print("Bin: ", bin_num)

            # convert hex to bin and fill leading zero
            binary = bin_num.zfill(len(hex_num) * 4)
            print("binary: ", binary)

        self.is_mark_idx_ok()
        self.show_warning()

        if not is_input_num_ok:
            return
        
        try:
            result_hex = " HEX: "
            result_binary = " BIN: "
            result_index = " IDX: "

            if len(binary) <= 10:
                space = 2
            elif len(binary) <= 100:
                space = 3
            elif len(binary) <= 1000:
                space = 4
            else:
                space = 5

            num = 0

            # mark color
            valid, mark_start_idx, mark_end_idx = self.get_mark_idx()
            if not valid:
                mark_start_idx = -1
                mark_end_idx = -1
            else:
                print("len(binary): ", len(binary))
                print("mark_start_idx: ", mark_start_idx)
                print("mark_end_idx: ", mark_end_idx)
                mark_start_idx = len(binary) - mark_start_idx - 1
                mark_end_idx = len(binary) - mark_end_idx - 1
            debug_print("mark_valid: ", valid)
            debug_print("mark_start_idx: ", mark_start_idx)
            debug_print("mark_end_idx: ", mark_end_idx)

            # display hex
            if len(self.result_frame_list) < 1:
                self.result_frame_list.append(tk.Frame(self.bottom_frame))
            else:
                self.label_class[0].end_label.pack_forget()
            self.label_class[0].start_label = tk.Label(self.result_frame_list[0], text=result_hex, font=self.data_font)
            for i in range(len(binary)):
                if (i + 1) % 4 == 0:
                    mark_start_byte = i // 4 * 4
                    mark_end_byte = (i // 4 + 1) * 4 - 1
                    bg = "yellow" if mark_start_idx >= mark_start_byte and mark_end_idx <= mark_end_byte else self.default_bg_color
                    if bg:
                        self.label_class[0].add(idx=i, master=self.result_frame_list[0], text=f"{hex_num[num].upper():>{space-1}}", font=self.data_font, bg=bg)
                    else:
                        self.label_class[0].add(idx=i, master=self.result_frame_list[0], text=f"{hex_num[num].upper():>{space-1}}", font=self.data_font)
                    num += 1
                else:
                    self.label_class[0].add(idx=i, master=self.result_frame_list[0], text=f"{(space -1) * ' '}", font=self.data_font)
            self.label_class[0].end_label = tk.Label(self.result_frame_list[0], text="", font=self.data_font)
            self.label_class[0].complete()
            debug_print("")

            for i in range(len(binary)):
                debug_print(f"{i:>{space}}", end="")
            debug_print("")

            # display binary
            if len(self.result_frame_list) < 2:
                self.result_frame_list.append(tk.Frame(self.bottom_frame))
            else:
                self.label_class[1].end_label.pack_forget()
            self.label_class[1].start_label = tk.Label(self.result_frame_list[1], text=result_binary, font=self.data_font)
            for i in range(len(binary)):
                fg = "#EE0000" if mark_start_idx >= i and mark_end_idx <= i else "black"
                self.label_class[1].add(idx=i, master=self.result_frame_list[1], text=f"{binary[i]:>{space-1}}", font=self.data_font, fg=fg)
                debug_print(f"{binary[i]:>{space}}", end="")

            self.label_class[1].end_label = tk.Label(self.result_frame_list[1], text=" ", font=self.data_font)
            self.label_class[1].complete()
            debug_print("")

            # display index
            if len(self.result_frame_list) < 3:
                self.result_frame_list.append(tk.Frame(self.bottom_frame))
            else:
                self.label_class[2].end_label.pack_forget()
            self.label_class[2].start_label = tk.Label(self.result_frame_list[2], text=result_index, font=self.data_font)
            for i in range(len(binary)):
                index = len(binary) - i - 1
                fg = "#0000FF" if mark_start_idx >= i and mark_end_idx <= i else "black"
                self.label_class[2].add(idx=i, master=self.result_frame_list[2], text=f"{index:>{space-1}}", font=self.data_font, fg=fg)
                debug_print(f"{index:>{space}}", end="")
            self.label_class[2].end_label = tk.Label(self.result_frame_list[2], text=" ", font=self.data_font)
            self.label_class[2].complete()

            for frame in self.result_frame_list:
                frame.pack(fill=tk.BOTH)

        except Exception as e:
            debug_print(e)
            debug_print(traceback.format_exc())
        
        # update window size
        self.geometry("")

if __name__ == "__main__":
    app = App()
    app.mainloop()

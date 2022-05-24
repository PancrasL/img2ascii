import _thread
import copy
from tkinter import *
from tkinter import filedialog

from img2ascii import *

global_config = Config()

def run(config):
    result = AsciiImg(config).convert()
    print(result, flush=True)

class GUI():
    def __init__(self):
        self.root = Tk()
        
    def start(self):
        self.init_window()
        self.root.mainloop()

    # 设置窗口
    def init_window(self):
        self.root.title("Gift To LK")  # 窗口名
        self.root.geometry('800x500+10+10')

        # 文件路径 row = 0
        Label(self.root, text="文件路径：", width=20).grid(row=0, column=0)
        self.selected_filepath = Label(self.root, text="")
        self.selected_filepath.grid(row=0, column=2, pady=10)
        self.select_file = Button(
            self.root, text="选择文件", width=15, command=self.select_file)
        self.select_file.grid(row=0, column=1)

        # 填充字符 row = 1
        Label(self.root, text="填充字符(至少6个)").grid(row=1, column=0)
        v = StringVar(self.root, "".join(global_config.symbols))
        self.input_entry = Entry(self.root, width=30, textvariable=v)
        self.input_entry.grid(row=1, column=1, pady=10)

        # 颜色总数(0表示不适用颜色) row = 2
        Label(self.root, text="颜色总数(0表示不适用颜色)").grid(row=2, column=0, pady=10)
        self.color_disable = IntVar()
        Radiobutton(self.root, text="开启彩色",
                    variable=self.color_disable, value=0).grid(row=2, column=1)
        Radiobutton(self.root, text="关闭彩色",
                    variable=self.color_disable, value=1).grid(row=2, column=2)

        # 宽度限制 row = 3
        Label(self.root, text="宽度限制").grid(row=3, column=0)
        self.width_limit_scale = Scale(self.root,
                                       length=300,
                                       from_=50,
                                       to=500,
                                       tickinterval=100,
                                       orient='horizontal',
                                       resolution=10
                                       )
        self.width_limit_scale.set(global_config.width_limit)
        self.width_limit_scale.grid(row=3, column=1)

        # 相似度 row = 4
        Label(self.root, text="相似性跨度(越小图片越细节)").grid(row=4, column=0)
        self.similarity_scale = Scale(self.root,
                                      length=300,
                                      from_=1000,
                                      to=20000,
                                      tickinterval=5000,
                                      orient='horizontal',
                                      resolution=500
                                      )
        self.similarity_scale.set(global_config.similarity)
        self.similarity_scale.grid(row=4, column=1)

        # 生成结果
        self.generate_button = Button(
            self.root, text="生成ASCII图片", bg="lightblue", width=10, command=self.generate)
        self.generate_button.grid(row=5, column=0, padx=10, pady=10)

    # 生成ASCII图片
    def generate(self):
        # 获取配置
        global_config.symbols = list(self.input_entry.get())
        global_config.color_disable = self.color_disable.get() == 1
        global_config.similarity = self.similarity_scale.get()
        global_config.width_limit = self.width_limit_scale.get()
        # 调用异步线程生成图片，避免阻塞桌面程序
        config = copy.deepcopy(global_config)
        _thread.start_new_thread (run, (config,))

    # 选择文件
    def select_file(self):
        global_config.filepath = filedialog.askopenfilename()
        self.selected_filepath.config(text=global_config.filepath)

if __name__ == '__main__':
    app = GUI()
    app.start()

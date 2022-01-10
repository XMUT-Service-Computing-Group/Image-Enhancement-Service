import os
import threading
import tkinter as tk
import tkinter.filedialog as tkf
from pathlib import Path
from tkinter import messagebox

from PIL import Image

from Real_ESRGAN.inference_realesrgan import enhancement


def GUI():
    window = tk.Tk()
    rad_var = tk.IntVar()
    window.title('')
    nScreenWid, nScreenHei = window.maxsize()
    window.geometry('%dx%d+%d+%d' % (500, 150, (nScreenWid - 500) / 2, (nScreenHei - 150) / 2))

    label1 = tk.Label(window, text="输入图像：")
    label1.place(x=10, y=25)

    button1 = tk.Button(window, text="选择", command=lambda: open_file(path1))
    button1.place(x=70, y=20)

    path1 = tk.Entry(window, width=50)
    path1.place(x=110, y=25)

    label2 = tk.Label(window, text="输出路径：")
    label2.place(x=10, y=65)

    button2 = tk.Button(window, text="选择", command=lambda: save_files(path2))
    button2.place(x=70, y=60)

    path2 = tk.Entry(window, width=50)
    path2.place(x=110, y=65)

    label3 = tk.Label(window, text="生成模式：")
    label3.place(x=10, y=100)

    radio1 = tk.Radiobutton(window, text="自动", variable=rad_var, value=1)
    radio1.place(x=70, y=100)
    radio1.select()

    radio2 = tk.Radiobutton(window, text="jpg", variable=rad_var, value=2)
    radio2.place(x=130, y=100)

    radio3 = tk.Radiobutton(window, text="png", variable=rad_var, value=3)
    radio3.place(x=190, y=100)

    button3 = tk.Button(window, text="生成", command=lambda: blend(path1.get(), path2.get(), rad_var.get(), button3))
    button3.place(x=450, y=100)

    window.mainloop()


def open_file(path):
    path.insert(0, tkf.askopenfilename(filetypes=[("图片", ".png .jpg .jpeg")]))


def save_files(path):
    path.insert(0, tkf.askdirectory())


def blend(path1, path2, ext, button):
    if ext == 1:
        ext = 'auto'
    elif ext == 2:
        ext = 'jpg'
    elif ext == 3:
        ext = 'png'
    if not Path(path1).is_file():
        tk.messagebox.showerror('错误', "图片不存在！")
        return
    if path1[path1.rfind('.') + 1:] == "png":
        temp = Image.open(path1)
        temp = temp.convert('RGB')
        print(os.path.splitext(os.path.basename(path1))[0])
        temp.save(path1 + '_temp.jpg', quality=95)
        path1 = path1 + '_temp.jpg'
    if path2 == "":
        tk.messagebox.showerror('错误', "生成路径为空！")
        return
    if not Path(path2).is_dir():
        os.makedirs(path2)
        return
    BlendThread(path1, path2, ext, button).start()
    InfoThread(button).start()


class BlendThread(threading.Thread):

    def __init__(self, path1, path2, ext, button):
        threading.Thread.__init__(self)
        self.path1 = path1
        self.path2 = path2
        self.ext = ext
        self.button = button

    def run(self):
        message = enhancement(self.path1, self.path2, self.ext)
        self.button['text'] = "生成"
        self.button.place(x=450, y=100)
        tk.messagebox.showinfo('信息', message)
        if "_temp" in self.path1:
            os.remove(self.path1)


class InfoThread(threading.Thread):
    def __init__(self, button):
        threading.Thread.__init__(self)
        self.button = button

    def run(self):
        self.button.place(x=420, y=100)
        self.button['text'] = "生成中……"


if __name__ == '__main__':
    GUI()

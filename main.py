import os
import threading
import tkinter as tk
import tkinter.filedialog as tkf
#import tkinter.font as tf
from pathlib import Path
from tkinter import END

# from PIL import Image

from Real_ESRGAN.inference_realesrgan import enhancement


def GUI():
    window = tk.Tk()
    # rad_var = tk.IntVar()
    window.title('图像增强软件')
    nScreenWid, nScreenHei = window.maxsize()
    window.geometry('%dx%d+%d+%d' % (500, 150, (nScreenWid - 500) / 2, (nScreenHei - 150) / 2))
    
    def set_path_2(path1):
        dirname = os.path.dirname(path1)
        #basename = os.path.basename(path1)
        #print(dirname)
        return dirname
        
    
    label1 = tk.Label(window, text="输入图像：")
    label1.place(x=10, y=25)

    button1 = tk.Button(window, text="选择", command=lambda: openfile(path1))
    button1.place(x=70, y=20)

    path1 = tk.Entry(window, width=50)
    path1.place(x=110, y=25)

    label_enhance_scale = tk.Label(window, text='倍数')
    label_enhance_scale.place(x=70, y=60)
    
    entry_enhance_scale = tk.Entry(window, width=6)
    entry_enhance_scale.place(x=110, y=60)
    entry_enhance_scale.insert(0, 4)
    
    button_enhance = tk.Button(window, text='开始增强', 
                               command=lambda: enhance(path1.get(), set_path_2(path1.get()), 
                                                       entry_enhance_scale.get(), button_enhance))
    button_enhance.place(x=70, y=100)

    window.mainloop()


def openfile(path):
    path.delete(0, END)
    path.insert(0, tkf.askopenfilename(filetypes=[('图片', '.png .jpg .jpeg .tif')]))


def savefiles(path):
    path.delete(0, END)
    path.insert(0, tkf.askdirectory())


def enhance(path1, path2, entry_enhance_scale, button):
    if not Path(path2).is_dir():
        os.makedirs(path2)
    if not Path(path1).is_file():
        tk.messagebox.showerror('错误', '图片不存在！')
        return
    if path2 == "":
        tk.messagebox.showerror('错误', '生成路径为空！')
        return
    if not str(entry_enhance_scale).replace('.', '', 1).isdigit():
        tk.messagebox.showerror('错误', "参数不是数字！")
        return
    if float(entry_enhance_scale) < 0:
        tk.messagebox.showerror('错误', "倍数不能小于0！")
        return
    if entry_enhance_scale == "":
        tk.messagebox.showerror('错误', "参数不能为空！")
        return
    
    enhanceThread(path1, path2, entry_enhance_scale, button).start()
    InfoThreadEnhance(button).start()

class enhanceThread(threading.Thread):

    def __init__(self, path1, path2, scale, button):
        threading.Thread.__init__(self)
        self.path1 = path1
        #base = os.path.basename(path1)
        #basename = os.path.splitext(base)[0]
        self.path2 = path2 + '/'
        self.scale = scale
        self.button = button

    def run(self):
        message = enhancement(self.path1, self.path2, float(self.scale))
        self.button['text'] = "开始增强"
        self.button.place(x=70, y=100)
        tk.messagebox.showinfo('信息', message)
        if "_temp" in self.path1:
            os.remove(self.path1)
            
class InfoThreadEnhance(threading.Thread):
    def __init__(self, button):
        threading.Thread.__init__(self)
        self.button = button

    def run(self):
        self.button.place(x=70, y=100)
        self.button['text'] = "图像增强中……"


if __name__ == '__main__':
    GUI()

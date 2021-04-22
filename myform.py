import tkinter
from tkinter import messagebox
from tkinter import filedialog
class messg:
    enable = 1
    
    @classmethod
    def showinfo(cls, title, massage):
        if messg.enable == 1:
            root = tkinter.Tk()
            root.withdraw()
            messagebox.showinfo(title, massage)

def open_input_file(init_dir, form_title, extension):
    root = tkinter.Tk()
    root.withdraw()
    fileName = filedialog.askopenfilename(initialdir=init_dir, title=form_title,
                                               filetypes=(("howCode files", "*."+extension), ("All files", "*.*")))
    return fileName

if __name__ == "__main__":
    title   = "CHAO"
    massage = "Buoi sang vui ve"
    messg.showinfo(title, massage)

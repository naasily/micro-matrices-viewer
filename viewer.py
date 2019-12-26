from tkinter import *
from tkinter import Menu
from tkinter import filedialog
import csv
from PIL import ImageTk, Image


def clicked():
    file = filedialog.askopenfilename()

    with open(file) as tsv:
        reader = csv.reader(tsv, dialect="excel-tab")
        lines = list(reader)
        probes = lines[0]
        classes = lines[1]

        img = Image.new('RGB', (len(probes), len(lines)), "black")
        pixels = img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                pixels[i, j] = (i % 255, j % 255, 100)

        image = ImageTk.PhotoImage(img)
        label = Label(window, image=image)
        label.pack(side="bottom", fill="both", expand="yes")
        label.image = image


window = Tk()
window.title("Micro Matrices Viewer")
window.geometry('500x500')

menu = Menu(window)

choose_file = Menu(menu, tearoff=0)
choose_file.add_command(label='Choose file', command=clicked)
menu.add_cascade(label='File', menu=choose_file)

window.config(menu=menu)
window.mainloop()


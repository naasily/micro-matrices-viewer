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

        image_width = len(probes)
        image_height = len(lines)

        img = Image.new('RGB', (image_width, image_height), "black")
        pixels = img.load()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                pixels[i, j] = (i % 255, j % 255, 100)

        img = img.resize((image_width * 10, image_height * 10))
        image = ImageTk.PhotoImage(img)
        label = Label(frame, image=image)
        label.pack(side="bottom", fill="both", expand="yes")
        label.image = image


def on_frame_configured(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


window = Tk()
window.title("Micro Matrices Viewer")
window.geometry('500x500')

canvas = Canvas(window, borderwidth=0, background="#ffffff")
frame = Frame(canvas, background="#ffffff")
vsb = Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="top", fill="both", expand=True)
canvas.create_window((4,4), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: on_frame_configured(canvas))

menu = Menu(frame)

choose_file = Menu(menu, tearoff=0)
choose_file.add_command(label='Choose file', command=clicked)
menu.add_cascade(label='File', menu=choose_file)

window.config(menu=menu)
window.mainloop()


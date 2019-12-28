from tkinter import *
from tkinter import Menu
from tkinter import filedialog
import csv
from PIL import ImageTk, Image
import cv2
import numpy as np
import statistics as stat
import math

matrix = np.zeros((2, 2, 3), np.uint8)
multiplication_factor = 10


def calculate_heat_map_color(value, left_range, right_range):
    green_pixel_value = 0
    red_pixel_value = 0

    position = (value - left_range) / (right_range - left_range)
    pixel_positon = position * 510
    if pixel_positon < 255:
        green_pixel_value = 255 - pixel_positon
    elif pixel_positon > 255:
        red_pixel_value = pixel_positon - 255
    return int(red_pixel_value), int(green_pixel_value), 0


def mouse_click(event):
    x_index = math.ceil(event.x / multiplication_factor)
    y_index = math.ceil(event.y / multiplication_factor)
    probe_label.configure(text="Current clicked probe: " + matrix[0][x_index])
    genome_label.configure(text="Current clicked genome: " + matrix[y_index][0])


def pack_labels():
    probe_label.pack(anchor="nw", padx=(10, 0), pady=(10, 0))
    genome_label.pack(anchor="nw", padx=(10, 0), pady=(10, 0))
    image_label.pack(side="bottom", fill="both", expand="yes", pady=(10, 0))


def clicked():
    global matrix
    file = filedialog.askopenfilename()

    with open(file) as tsv:
        reader = csv.reader(tsv, dialect="excel-tab")
        matrix = list(reader)
        image_width = len(matrix[0]) - 1
        image_height = len(matrix) - 2
        img = np.zeros((image_height, image_width, 3), np.uint8)
        for i in range(2, image_height):
            row = list(matrix[i])
            del row[0]
            row = list(map(float, row))
            dev = stat.stdev(row)
            mean = stat.mean(row)
            left_range = mean - 4 * dev
            right_range = mean + 4 * dev
            for j in range(1, image_width):
                img[i - 2, j - 1] = calculate_heat_map_color(row[j], left_range, right_range)

        resized = cv2.resize(img, (image_width * multiplication_factor, image_height * multiplication_factor),
                             interpolation=cv2.INTER_AREA)
        image = Image.fromarray(resized)
        window.image = image = ImageTk.PhotoImage(image)

        image_label.configure(image=image)
        image_label.bind("<Button>", mouse_click)
        image_label.image = image
        pack_labels()


def on_frame_configured(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


window = Tk()
window.title("Micro Matrices Viewer")
window.geometry('500x500')

canvas = Canvas(window, borderwidth=0, background="#ffffff")
frame = Frame(canvas, background="#ffffff")
scroll_bar = Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll_bar.set)

scroll_bar.pack(side="right", fill="both")
canvas.pack(side="top", fill="both", expand=True)
canvas.create_window((4,4), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: on_frame_configured(canvas))
probe_label = Label(frame, text="Current clicked probe: ")
genome_label = Label(frame, text="Current clicked genome: ")
image_label = Label(frame)

menu = Menu(frame)
choose_file = Menu(menu, tearoff=0)
choose_file.add_command(label='Load', command=clicked)
menu.add_cascade(label='File', menu=choose_file)

window.config(menu=menu)
window.mainloop()


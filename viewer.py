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
canvas_horizontal_line_id = 0
canvas_vertical_line_id = 0
micro_matrix_image = np.zeros((2, 2, 3), np.uint8)
current_y_position = 0
canvas_image_id = 0


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
    canvas = event.widget
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)

    global canvas_horizontal_line_id
    global canvas_vertical_line_id
    x_index = math.ceil(x / multiplication_factor)
    y_index = math.ceil(y / multiplication_factor)
    probe_label.configure(text="Current clicked probe: " + matrix[0][x_index])
    genome_label.configure(text="Current clicked genome: " + matrix[y_index][0])

    canvas.after(1, canvas.delete, canvas_horizontal_line_id)
    canvas.after(1, canvas.delete, canvas_vertical_line_id)
    canvas_horizontal_line_id = canvas.create_line(0, y, (len(matrix[0]) - 1) * multiplication_factor,
                                                   y, fill="red")
    canvas_vertical_line_id = canvas.create_line(x, 0, x, (len(matrix) - 2) * multiplication_factor,
                                                 fill="red")


def pack_labels():
    probe_label.pack(padx=(10, 0), pady=(10, 0))
    genome_label.pack(padx=(10, 0), pady=(10, 0))
    class_label.pack(anchor="nw")
    top_arrow_label.pack(side="top")
    down_arrow_label.pack(side="bottom")


def create_classes_label(classes):
    del classes[0]
    img = np.zeros((1, len(classes), 3), np.uint8)
    for idx, c in enumerate(classes):
        if c == '1':
            img[0][idx] = (255, 0, 0)
        if c == '2':
            img[0][idx] = (0, 255, 0)
        if c == '3':
            img[0][idx] = (0, 0, 255)

    img = cv2.resize(img, (img.shape[1] * multiplication_factor, img.shape[0] * multiplication_factor),
                     interpolation=cv2.INTER_AREA)
    image = Image.fromarray(img)
    window.classes_image = classes_image = ImageTk.PhotoImage(image)
    class_label.configure(image=classes_image)


def show_data():
    draw_micro_matrix()
    canvas.bind("<Button-1>", mouse_click)
    create_classes_label(list(matrix[1]))
    pack_labels()


def draw_micro_matrix():
    global micro_matrix_image
    global current_y_position
    global canvas_image_id
    canvas.after(1, canvas.delete, canvas_image_id)
    cropped_image = micro_matrix_image[current_y_position:400 + current_y_position, 0:len(micro_matrix_image[0])]
    image = Image.fromarray(cropped_image)
    window.image = image = ImageTk.PhotoImage(image)
    canvas.create_image(image.width(), image.height(), image=image, anchor="se")


def load_file():
    global matrix
    global micro_matrix_image
    file = filedialog.askopenfilename()

    with open(file) as tsv:
        reader = csv.reader(tsv, dialect="excel-tab")
        matrix = list(reader)
        image_width = len(matrix[0]) - 1
        image_height = len(matrix) - 2
        img = np.zeros((image_height - 2, image_width - 1, 3), np.uint8)
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

        micro_matrix_image = cv2.resize(img, (image_width * multiplication_factor, image_height * multiplication_factor),
                             interpolation=cv2.INTER_AREA)
        show_data()


def top_arrow_click():
    global current_y_position
    global multiplication_factor
    if current_y_position > 0:
        current_y_position = current_y_position - multiplication_factor
        draw_micro_matrix()


def down_arrow_click():
    global current_y_position
    if current_y_position < len(micro_matrix_image):
        current_y_position = current_y_position + multiplication_factor
        draw_micro_matrix()


window = Tk()
window.title("Micro Matrices Viewer")
window.geometry('500x500')

canvas = Canvas(window, borderwidth=0, background="#ffffff")
image_frame = Frame(canvas, background="#ffffff")

info_frame = Frame(window)
info_frame.pack(anchor="nw")

arrows_frame = Frame(window)
arrows_frame.pack(side=RIGHT, fill=Y)

horizontal_scroll_bar = Scrollbar(window, orient="horizontal", command=canvas.xview)
canvas.configure(xscrollcommand=horizontal_scroll_bar.set)
horizontal_scroll_bar.pack(side="bottom", fill="both")

canvas.pack(side="top", fill="both", expand=True)
canvas.create_window((0, 0), window=image_frame, anchor="nw")

image_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

probe_label = Label(info_frame, text="Current clicked probe: ")
genome_label = Label(info_frame, text="Current clicked genome: ")
class_label = Label(info_frame)

top_arrow_image = PhotoImage(file="top_arrow.png")
down_arrow_image = PhotoImage(file="down_arrow.png")
top_arrow_label = Button(arrows_frame, image=top_arrow_image, command=top_arrow_click, height=20, width=10)
down_arrow_label = Button(arrows_frame, image=down_arrow_image, command=down_arrow_click, height=20, width=10)

menu = Menu(image_frame)
choose_file = Menu(menu, tearoff=0)
choose_file.add_command(label='Load', command=load_file)
menu.add_cascade(label='File', menu=choose_file)

window.config(menu=menu)
window.mainloop()


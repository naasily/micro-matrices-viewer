from tkinter import *
from tkinter import Menu
from tkinter import filedialog
import csv
from PIL import ImageTk, Image
import cv2
import numpy as np
import matplotlib.pyplot as plt


def calculate_heat_map_color(value, max, min):
    green_pixel_value = 0
    red_pixel_value = 0

    #range = max - min
    position = (value - min) / (max - min)
    pixel_positon = position * 510
    #red_pixel_value = 255 - pixel_positon
    if pixel_positon > 255:
        green_pixel_value = pixel_positon - 255
    elif pixel_positon < 255:
        red_pixel_value = pixel_positon
    #print("value", value, "max", max, "min", min,"pixel values", int(red_pixel_value), " ", int(green_pixel_value))
    return int(red_pixel_value), int(green_pixel_value), 0

    # 0 - 100
    # 40
    # 40 / 100 = 0.4
    # 510 * 0.4 = 204

# 510
# 255, 0, 0 - red
# 0, 255, 0 - green

def clicked():
    file = filedialog.askopenfilename()

    with open(file) as tsv:
        reader = csv.reader(tsv, dialect="excel-tab")
        lines = list(reader)
        probes = lines[0]
        classes = lines[1]

        image_width = len(classes) - 1
        image_height = len(lines) - 2
        img = np.zeros((image_height, image_width, 3), np.uint8)
        #img = Image.new('RGB', (image_width, image_height), "black")
        #pixels = img.load()
        #print(img.size)
        #print(img.shape)
        for i in range(2, image_height):
            row = lines[i]
            del row[0]
            for j in range(1, image_width):
                row = list(map(float, row))
                img[i, j] = calculate_heat_map_color(row[j], max(row), min(row))

        resized = cv2.resize(img, (image_width * 10, image_height * 10), interpolation=cv2.INTER_AREA)
        #img = img.resize((image_width * 10, image_height * 10))
        image = Image.fromarray(resized)
        window.image = image = ImageTk.PhotoImage(image)
        #image.save('image3.png')
        # cv2.imwrite('image2.png', resized)
        label = Label(frame, image=image)
        label.pack(side="bottom", fill="both", expand="yes")
        label.image = image
        # canvas.delete("IMG")
        # canvas.create_image((0, 0), image=image, anchor=NW, tags="IMG")
        # # canvas.pack()
        # # canvas.update()
        # canvas.update_idletasks()
        # frame.update_idletasks()
        # window.update_idletasks()


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

menu = Menu(frame)

choose_file = Menu(menu, tearoff=0)
choose_file.add_command(label='Choose file', command=clicked)
menu.add_cascade(label='File', menu=choose_file)

# window.image = image = ImageTk.PhotoImage('image3.png')
# label = Label(frame, image=image)
# label.pack(side="bottom", fill="both", expand="yes")
# label.image = image

# img = plt.imread('image3.png')
# plt.imshow(img)
# plt.show()

window.config(menu=menu)
window.mainloop()


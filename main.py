"""
Created with help of https://mathematica.stackexchange.com/questions/137156/where-is-abbott-how-to-make-logograms-from-the-film-arrival
I do not know Mathematica at all so some of it may be off. oskarboer@gmail.com
"""
import math
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.patches import PathPatch
from matplotlib.path import Path

import io
import cv2

import tkinter as tk
from PIL import Image, ImageTk

# local file with default values
import parameters
from logogram_drawing import *
import cairo_render

params_dict = parameters.parameters_dict
params = parameters.parameters


root = tk.Tk()


def redraw():
    global logogram_image
    # logogram_image = draw_logogram(params_dict)
    logogram_image = cairo_render.cairo_render_logogram(params_dict)

    cv2.imwrite('result.jpg', logogram_image)

    resized = cv2.resize(logogram_image, dsize=(800, 800), interpolation=cv2.INTER_CUBIC)
    tmp = ImageTk.PhotoImage(image=Image.fromarray(resized))
    return tmp

def update_image():
    global img # a critical thing since the pointer should be existing, otherwise the image is not shown
    img = redraw()
    canvas.itemconfigure(image_container, image=img)


img = redraw()


canvas = tk.Canvas(root, width=800, height=800)
canvas.grid(column=1, row=0, sticky=tk.EW)
image_container = canvas.create_image(0, 0, image=img, anchor='nw')


slider_frame = tk.Frame(root)
slider_frame.grid(column=0, row=0, sticky=tk.N)


def trackbar_callback(key, val):
    global params_dict
    # here we try to preserve the initial type, since the slider returns an str
    t = type(params_dict[key])
    print(key, params_dict[key], t)
    params_dict[key] = t(val)
    update_image()

for i in range(len(params)):
    slider_start = (params[i][3])
    slider_end = (params[i][4])
    if len(params[i]) == 6:
        slider_resolution = (params[i][5])
    else:
        slider_resolution = (slider_end - slider_start) / 10.0
    slider_val = params[i][0]
    slider_name = params[i][2]
    
    slider_labl = tk.Label(slider_frame, text=slider_name).grid(row=i, column=0, pady=4, padx=4)
    scale = tk.Scale(slider_frame, from_=slider_start,
                     to=slider_end, length=200, resolution=slider_resolution,
                     orient=tk.HORIZONTAL, command=lambda v, name=slider_val: trackbar_callback(name, v))

    scale.grid(column=1, row=i)


# cv2.imwrite('result.jpg', logogram_image)

root.mainloop()




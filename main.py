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




# def get_callbacks():
#     trackbar_callbacks = {}
#     for key in params_dict.keys():
#         def trackbar_callback(val):
#             global params_dict
#             # here we try to preserve the initial type, since the slider returns an str
#             t = type(params_dict[key])
#             print(key, params_dict[key], t)
#             params_dict[key] = t(val)
#             update_image()
#         
#         trackbar_callbacks[key] = copy_func(tmp)
#     return trackbar_callbacks


# trackbar_callbacks = get_callbacks()

def trackbar_callback_rmin(val):
    global params_dict
    t = type(params_dict["rmin"])
    params_dict["rmin"] = t(val)
    update_image()

def trackbar_callback_rmax(val):
    global params_dict
    t = type(params_dict["rmax"])
    params_dict["rmax"] = t(val)
    update_image()

def trackbar_callback_wmin(val):
    global params_dict
    t = type(params_dict["wmin"])
    params_dict["wmin"] = t(val)
    update_image()

def trackbar_callback_wmax(val):
    global params_dict
    t = type(params_dict["wmax"])
    params_dict["wmax"] = t(val)
    update_image()

def trackbar_callback_cv(val):
    global params_dict
    t = type(params_dict["cv"])
    params_dict["cv"] = t(val)
    update_image()

def trackbar_callback_nc(val):
    global params_dict
    t = type(params_dict["nc"])
    params_dict["nc"] = t(val)
    update_image()

def trackbar_callback_phi0(val):
    global params_dict
    t = type(params_dict["phi0"])
    params_dict["phi0"] = t(val)
    update_image()

def trackbar_callback_dmin(val):
    global params_dict
    t = type(params_dict["dmin"])
    params_dict["dmin"] = t(val)
    update_image()

def trackbar_callback_dmax(val):
    global params_dict
    t = type(params_dict["dmax"])
    params_dict["dmax"] = t(val)
    update_image()
    
def trackbar_callback_nd(val):
    global params_dict
    t = type(params_dict["nd"])
    params_dict["nd"] = t(val)
    update_image()
  
def trackbar_callback_rbmin(val):
    global params_dict
    t = type(params_dict["rbmin"])
    params_dict["rbmin"] = t(val)
    update_image()
   
def trackbar_callback_rbmax(val):
    global params_dict
    t = type(params_dict["rbmax"])
    params_dict["rbmax"] = t(val)
    update_image()

def trackbar_callback_bmin(val):
    global params_dict
    t = type(params_dict["bmin"])
    params_dict["bmin"] = t(val)
    update_image()

def trackbar_callback_bmax(val):
    global params_dict
    t = type(params_dict["bmax"])
    params_dict["bmax"] = t(val)
    update_image()
    
def trackbar_callback_nb(val):
    global params_dict
    t = type(params_dict["nb"])
    params_dict["nb"] = t(val)
    update_image()
    
def trackbar_callback_phi1(val):
    global params_dict
    t = type(params_dict["phi1"])
    params_dict["phi1"] = t(val)
    update_image()
    
def trackbar_callback_pmin(val):
    global params_dict
    t = type(params_dict["pmin"])
    params_dict["pmin"] = t(val)
    update_image()

def trackbar_callback_pmax(val):
    global params_dict
    t = type(params_dict["pmax"])
    params_dict["pmax"] = t(val)
    update_image()

def trackbar_callback_nxmin(val):
    global params_dict
    t = type(params_dict["nxmin"])
    params_dict["nxmin"] = t(val)
    update_image()

def trackbar_callback_nxmax(val):
    global params_dict
    t = type(params_dict["nxmax"])
    params_dict["nxmax"] = t(val)
    update_image()

def trackbar_callback_tlenmin(val):
    global params_dict
    t = type(params_dict["tlenmin"])
    params_dict["tlenmin"] = t(val)
    update_image()

def trackbar_callback_tlenmax(val):
    global params_dict
    t = type(params_dict["tlenmax"])
    params_dict["tlenmax"] = t(val)
    update_image()

def trackbar_callback_noiseExp(val):
    global params_dict
    t = type(params_dict["noiseExp"])
    params_dict["noiseExp"] = t(val)
    update_image()

def trackbar_callback_scale(val):
    global params_dict
    t = type(params_dict["scale"])
    params_dict["scale"] = t(val)
    update_image()

def trackbar_callback_ntendrils(val):
    global params_dict
    t = type(params_dict["ntendrils"])
    params_dict["ntendrils"] = t(val)
    update_image()

def trackbar_callback_b(val):
    global params_dict
    t = type(params_dict["b"])
    params_dict["b"] = t(val)
    update_image()

def trackbar_callback_seed(val):
    global params_dict
    t = type(params_dict["seed"])
    params_dict["seed"] = t(val)
    update_image()
    
 

d = {"rmin":trackbar_callback_rmin, "rmax":trackbar_callback_rmax, "wmin":trackbar_callback_wmin, "wmax":trackbar_callback_wmax,
"cv":trackbar_callback_cv, "nc":trackbar_callback_nc, "phi0":trackbar_callback_phi0, "dmin":trackbar_callback_dmin,
"dmax":trackbar_callback_dmax, "nd":trackbar_callback_nd, "rbmin":trackbar_callback_rbmin, "rbmax":trackbar_callback_rbmax,
"bmin":trackbar_callback_bmin, "bmax":trackbar_callback_bmax, "nb":trackbar_callback_nb, "phi1":trackbar_callback_phi1, "pmin":trackbar_callback_pmin,
"pmax":trackbar_callback_pmax, "nxmin":trackbar_callback_nxmin, "nxmax":trackbar_callback_nxmax, "tlenmin":trackbar_callback_tlenmin,
"tlenmax":trackbar_callback_tlenmax, "noiseExp":trackbar_callback_noiseExp, "scale":trackbar_callback_scale, "ntendrils":trackbar_callback_ntendrils,
"b":trackbar_callback_b, "seed":trackbar_callback_seed}


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
                     orient=tk.HORIZONTAL, command=d[params[i][0]])
    scale.grid(column=1, row=i)


# cv2.imwrite('result.jpg', logogram_image)

root.mainloop()












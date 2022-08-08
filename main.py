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
from PIL import Image
import cv2

# Drawind functions
def arc(x, y, r, a1, a2, linewidth, ax, resolution=100):
    #draw arc
    arc_angles = np.linspace(a1, a2, resolution)
    arc_xs = r * np.cos(arc_angles) + x
    arc_ys = r * np.sin(arc_angles) + y
    ax.plot(arc_xs, arc_ys, color = 'black', lw = linewidth)




# Math creation functions. In the stack answer he draws everthing immideatly, 
# I first calculate it and then use matplotlib to draw.
def chop(expr, delta=10**-10):
    return np.ma.masked_inside(expr, -delta, delta).filled(0)

def rescale(arr):
    return (arr - np.min(arr)) / (np.max(arr) - np.min(arr))

def NoiseGen(n, e):
    fe = np.array(range(1, int(n/2) + 1)) ** e
    f = math.e ** (complex(0,1) * 2.0 * math.pi * np.random.random(int(n/2))) / fe
    f[-1] = f[-1].real
    f_rev = np.conj(f[:-1][::-1])
    d = chop(np.fft.ifft(np.concatenate(([0], f, f_rev))))
    return rescale(d)

def AnglePath(t):
    out = [np.array([0.0, 0.0])]
    x, y = 0, 0
    angle = 0
    for i in t:
        angle += i
        x += np.cos(angle)
        y += np.sin(angle)
        out.append(np.array([x, y]))
    return np.array(out)

# Main function with all the fun
def Logogram(rmin, rmax, wmin, wmax, cv, nc, dmin, dmax, 
    nd, b, phi0, seed, rbmin, rbmax, pmin, pmax, bmin, bmax,
    nb, phi1, nxmin, nxmax, tlenmin, tlenmax, noiseExp, scale, 
    ntendrils):

    radius = 1000.0
    np.random.seed(seed)
    
    circles = []
    for i in range(nc):
    # (* circles composing circular stroke *)
        r = np.random.uniform(rmin * radius, rmax * radius) # radius
        c = np.random.uniform(-r * cv, r * cv, 2) # coordinate
        p = np.random.uniform(0, 6.283, 2) + phi0 # spcifies which par of arc to draw. "gives a circular or ellipse arc from angle θ1 to θ2." 
        w = np.random.uniform(wmin, wmax) # Thickness
        
        circles.append([r, c, p, w])
    
    # (* additional disks composing circular stroke *)
    disks = []
    for i in range(nd):
        tmp = np.random.uniform(rmin * radius, rmax * radius)
        t = np.random.uniform(0, 6.283) + phi0
        c = tmp * np.array([np.cos(t), np.sin(t)]) # cooridinate
        ellipsnes = np.random.uniform(radius * dmin, radius * dmax, 2)
        
        disks.append([c, ellipsnes])
    
    # (* disks composing blob on circular stroke *)
    
    blob_disks = []
    for i in range(nb):
        r = np.random.uniform(rbmin * radius, rbmax * radius)
        dp = np.random.uniform(pmin, pmax)
        c = r * np.array([np.cos(phi1 + dp), np.sin(phi1 + dp)])
        ellipsnes = np.random.uniform(radius * bmin, radius * bmax, 2)
        blob_disks.append([c, ellipsnes])
    
    # (* tendrils on blob *)
    tendrils = []
    for i in range(ntendrils):
        nx = np.random.uniform(nxmin, nxmax)
        tlen = 2 * np.random.randint(tlenmin, tlenmax) # TODO: check it randint works the same in Mathematica. Is it [a, b] or [a, b) 
        noise = nx * NoiseGen(tlen, noiseExp)
        noise = noise - np.mean(noise)
        tmp = phi1 + np.random.uniform(pmin, pmax)
        c0 = radius * np.array([np.cos(tmp), np.sin(tmp)])
        
        path = c0 + scale * (-1)**np.random.randint(0, 2) * AnglePath(noise)
        thickness = 0.008
        tendrils.append([path, thickness])
    return circles, disks, blob_disks, tendrils


# I set default parametrs here for the beggining.
rmin, rmax = 0.98, 1.02
wmin, wmax = 0.0003, 0.0010
cv, nc = 0.05, 300
dmin, dmax = 0.010, 0.030
nd = 50
b = 0.8
phi0 = 5.0
seed = 0
rbmin, rbmax = 0.98, 1.02
pmin, pmax = 0.0, 0.8
bmin, bmax = 0.020, 0.070
nb = 30
phi1 = 2.0
nxmin, nxmax = 0.1, 0.5
tlenmin, tlenmax = 10, 20
noiseExp, scale = 1.0, 10.0 
ntendrils = 7


circles, disks, blob_disks, tendrils = Logogram(
    rmin, rmax, wmin, wmax, cv, nc, dmin, dmax,
    nd, b, phi0, seed, rbmin, rbmax, pmin, pmax, bmin, bmax,
    nb, phi1, nxmin, nxmax, tlenmin, tlenmax, noiseExp, scale,
    ntendrils)

# Creating main plot
plt.figure()
ax = plt.gca()
fig = plt.gcf()
fig.set_size_inches(10, 10)

# In mathematica thikness defined as a percent of the graph width, 
# so given that widht is 1000 I use this multiplier. Play with it.
thickness_modifier = 1000.0

for r, c, p, w in circles:
    arc(c[0], c[1], r, p[0], p[1], w * thickness_modifier, ax)

for xy, wh in disks:
    ellipse = Ellipse(xy=xy, width=wh[0] * 2, height=wh[1] * 2, color='black') # here I multiply by 2 since in Mathematica argument is radius, while in matplotlib -- diameter
    ax.add_patch(ellipse)

for xy, wh in blob_disks:
    ellipse = Ellipse(xy=xy, width=wh[0] * 4, height=wh[1] * 4, color='black') # here I ... (look before)
    ax.add_patch(ellipse)

for path, thikness in tendrils:
    path = [[t[0].real, t[1].real] for t in path]
    path = Path(path)
    patch = PathPatch(path, facecolor ='none', capstyle='round', lw = thikness * thickness_modifier * 1.5)
    ax.add_patch(patch)





ax.set_aspect('equal', 'box')

# https://stackoverflow.com/questions/8598673/how-to-save-a-pylab-figure-into-in-memory-file-which-can-be-read-into-pil-image/8598881
# Converting plot to PIL image
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
im = Image.open(buf)

# PIL image to cv2 image (np array) 
cv_img = np.array(im)
gray_image = cv2.cvtColor(cv_img, cv2.COLOR_RGB2GRAY).astype('uint8')

# https://reference.wolfram.com/language/ref/DiskMatrix.html?q=DiskMatrix
# making it look like DiskMatrix from mathematica:
kernel = np.ones((5, 5), 'uint8')
kernel[0, 0] = 0
kernel[0, -1] = 0
kernel[-1, 0] = 0
kernel[-1, -1] = 0

dilated = cv2.dilate(gray_image, kernel)

blur = cv2.blur(dilated,(5,5))

# https://learnopencv.com/otsu-thresholding-with-opencv/
# Using some smart thresholding tecnique, to automaticaly find the best one,
# seems like mathematica using this one by default
# https://reference.wolfram.com/language/ref/Binarize.html?q=Binarize
# Binarize[image] uses Otsu's cluster variance maximization method.
otsu_threshold, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU,)


cv2.imshow('image', threshold)

while cv2.waitKey(50) != 27: # press ESC
    pass


cv2.destroyAllWindows()

cv2.imwrite('result.jpg',threshold)

# im.show()

buf.close()
# plt.show()












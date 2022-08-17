import cairo
import math
import numpy as np
import cv2

# local file with default values
from logogram_drawing import *
import parameters


WIDTH, HEIGHT = 1000, 1000

params_dict = parameters.parameters_dict
params = parameters.parameters
SCALE_FACTOR = 3000


# for i in circles:
    # print(i)

def scale_xy(val):
    return (val / SCALE_FACTOR) + 0.5

def path_ellipse(cr, x, y, width, height, angle=0):
    """
    x      - center x
    y      - center y
    width  - width of ellipse  (in x direction when angle=0)
    height - height of ellipse (in y direction when angle=0)
    angle  - angle in radians to rotate, clockwise
    """
    cr.save()
    cr.translate(x, y)
    cr.rotate(angle)
    cr.scale(width / 2.0, height / 2.0)
    cr.arc(0.0, 0.0, 1.0, 0.0, 2.0 * math.pi)
    cr.restore()

def cairo_render_logogram(params_dict):
    circles, disks, blob_disks, tendrils = Logogram(*params_dict.values())

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
    context = cairo.Context(surface)

    context.rectangle(0, 0, WIDTH, HEIGHT)
    context.set_source_rgb(1, 1, 1)
    context.fill()

    context.scale(1000, 1000)
    context.set_line_width(0.04)
    context.set_source_rgb(0, 0, 0)

    for r, c, p, w in circles:
        x = scale_xy(c[0])
        y = scale_xy(c[1])
        
        context.arc(x, y, r / SCALE_FACTOR, p[0], p[1])
        context.set_line_width(w)
        context.stroke()


    for xy, wh in disks:
        x = scale_xy(xy[0])
        y = scale_xy(xy[1])
        w, h = wh[0] * 2 / SCALE_FACTOR, wh[1] * 2 / SCALE_FACTOR
        
        path_ellipse(context, x, y, w, h)
        context.fill_preserve()
        context.set_line_width(0.0001)
        context.stroke()

    for xy, wh in blob_disks:
        x = scale_xy(xy[0])
        y = scale_xy(xy[1])
        w, h = wh[0] * 2 / SCALE_FACTOR, wh[1] * 2 / SCALE_FACTOR
        
        path_ellipse(context, x, y, w, h)
        context.fill_preserve()
        context.set_line_width(0.0001)
        context.stroke()

    for path, thikness in tendrils:
        path = [[t[0].real, t[1].real] for t in path]
        context.set_line_cap(cairo.LINE_CAP_ROUND)
        
        x = scale_xy(path[0][0])
        y = scale_xy(path[0][1])       
        context.move_to(x, y)
        for x, y in path[1:]:
            x = scale_xy(x)
            y = scale_xy(y)
            context.line_to(x, y)
            
        context.set_line_width(thikness)
        context.stroke()
    
    # Convert to numpy
    buf = surface.get_data()
    data = np.ndarray(shape=(1000, 1000, 4),
                     dtype=np.uint8,
                     buffer=buf)
    
    # Dilation/Blur part with opencv
    gray_image = cv2.cvtColor(data, cv2.COLOR_RGB2GRAY).astype('uint8')

    # https://reference.wolfram.com/language/ref/DiskMatrix.html?q=DiskMatrix
    # making it look like DiskMatrix from mathematica:
    kernel = np.ones((5, 5), 'uint8')
    kernel[0, 0] = 0
    kernel[0, -1] = 0
    kernel[-1, 0] = 0
    kernel[-1, -1] = 0

    dilated = cv2.dilate(gray_image, kernel)

    blur = cv2.blur(dilated, (5,5))

    # https://learnopencv.com/otsu-thresholding-with-opencv/
    # Using some smart thresholding tecnique, to automaticaly find the best one,
    # seems like mathematica using this one by default
    # https://reference.wolfram.com/language/ref/Binarize.html?q=Binarize
    # Binarize[image] uses Otsu's cluster variance maximization method.
    otsu_threshold, threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return threshold



if __name__ == "__main__":
    img = cairo_render_logogram(parameters.parameters_dict)
    cv2.imshow("Show image", img)
    while cv2.waitKey(0) != 32:
        pass
        

    cv2.destroyAllWindows()











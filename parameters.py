

# parameter, default value, name of the parameter, min resonable value, max resonable value, resonable step
parameters = [
    ["rmin", 0.98, "Minimum Circle Radius", 0.9, 1.1],
    ["rmax", 1.02, "Maximum Circle Radius", 0.9, 1.1],

    ["wmin", 0.0003, "Minimum Line Thickness", 0.0002, 0.008],
    ["wmax", 0.0010, "Maximum Line Thickness", 0.0002, 0.008],

    ["cv", 0.05, "Circle Centre Variation", 0.01, 0.2],
    ["nc", 300, "Number of Circles", 20, 1000, 20],
         
    ["phi0", 5.0, "Angle of Circle Gap", 0.0, 6.3],
    ["dmin", 0.010, "Minimum Disk Radius", 0.001, 0.2],
    ["dmax", 0.030, "Maximum Disk Radius", 0.001, 0.2],
    ["nd", 50, "Number of Disks", 10, 300, 10],


    ["rbmin", 0.98, "Minimum Radial Distance", 0.9, 1.1],
    ["rbmax", 1.02, "Maximum Radial Distance", 0.9, 1.5],

    ["bmin", 0.020, "Minimum Blob Radius", 0.001, 0.2],
    ["bmax", 0.070, "Maximum Blob Radius", 0.001, 0.2],
    ["nb", 30, "Number of Blob Disks", 5, 200, 5],

    ["phi1", 2.0, "Initial Blob Angle", 0.0, 6.3],
    ["pmin", 0.0, "Minimum Angular Extent", 0.0, 0.5],
    ["pmax", 0.8, "Maximum Angular Extent", 0.1, 2.5],


    ["nxmin", 0.1, "Minimum Curliness", 0.01, 1.0],
    ["nxmax", 0.5, "Maximum Curliness", 0.03, 1.0],

    ["tlenmin", 10, "Minimum Tendril Length", 2, 100, 1],
    ["tlenmax", 20, "Maximum Tendril Length", 2, 100, 1],

    ["noiseExp", 1.0, "Noise Exponent", 0.1, 3.0],
    ["scale", 10.0, "Tendril Step Size", 1.0, 50.0],
    ["ntendrils", 7, "Number Of Tendrils", 2, 50, 1],


    ["b", 0.8, "Binarize Threshold", 0.1, 1.0],
    ["seed", 0, "Random Number Seed", 0, 1000, 1]
]


# create a dictionary of parameters
k = [i[0] for i in parameters]
val = [i[1] for i in parameters]

parameters_dict = dict(zip(k, val))


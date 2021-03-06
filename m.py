import math
import numpy as np
import sys


# Returns numpy vector with given direction and magnitude
def get_vector(direction, magnitude):
    # Todo : return type to numpy vector.
    return np.array([magnitude * math.cos(direction), magnitude * math.sin(direction), 0], np.float32)


# Convert vector to string
def vec2str(vec, dig=5):
    r = ''
    for i in vec:
        r += str(round(i, dig)) + ' '
    return r


# Return edge points of a cogwheel with given parameter
def get_cog_edge(radius, tooth_count, tooth_size, height):
    d = math.pi / tooth_count
    d2 = d / 2

    r1 = []
    for i in range(tooth_count * 2):
        r1.append(get_vector(d * i, radius))

    bottom = []
    for i in range(tooth_count * 2):
        bottom.append(r1[i])
        if i % 2 == 0:
            bottom.append(r1[i] + get_vector(d * i + d2, tooth_size))
            bottom.append(r1[i + 1] + get_vector(d * i + d2, tooth_size))
    top = []
    height = np.array([0, 0, height], np.float32)
    for i in bottom:
        top.append(i + height)
    return top, bottom


# Generate obj file from edge points
def get_obj_str(edge_points):
    top = edge_points[0]
    bottom = edge_points[1]
    l = ['v 0.00 0.00 0.00', 'v 0.00 0.00 ' + str(top[0][2])]

    # Add vertex
    for t in top:
        l.append('v ' + vec2str(t))
    for b in bottom:
        l.append('v ' + vec2str(b))

    lt = len(top)

    # Fill top and bottom
    for i in range(lt - 1):
        l.append('f 2 ' + str(i + 3) + ' ' + str(i + 4))
        l.append('f 1 ' + str(i + lt + 3) + ' ' + str(i + lt + 4))

    # Fill Side
    for i in range(lt - 1):
        l.append('f ' + str(i + 3) + ' ' + str(i + lt + 3) + ' ' + str(i + lt + 4))
        l.append('f ' + str(i + 3) + ' ' + str(i + 4) + ' ' + str(i + lt + 4))

    l.append('f 2 ' + str(lt + 2) + ' 3')
    l.append('f 1 ' + str(lt * 2 + 2) + ' ' + str(lt + 3))

    l.append('f ' + str(lt + 2) + ' ' + str(lt * 2 + 2) + ' ' + str(lt + 3))
    l.append('f ' + str(lt + 2) + ' ' + '3' + ' ' + str(lt + 3))

    return l


# Get appropriate parameters that make tooth cube.
def get_appropriate_value(tooth_count, tooth_size=2):
    return tooth_size * tooth_count / math.pi, tooth_count, tooth_size, tooth_size

def is_number(arg):
    try:
        int(arg)
        return True
    except:
        return False

if len(sys.argv) == 0:
    print("You must pass an argument to specify the count of teeth.")
    sys.exit()
elif not is_number(sys.argv[1]):
    print(f"The count of teeth must be a number. The input was {sys.argv[1]}.")
    sys.exit()

tooth = int(sys.argv[1])

if tooth <= 0:
    print(f"The count of teeth must be greater then 0. The input was {tooth}.")
    sys.exit()

# Generate 24-toothed cogwheel
with open(sys.argv[1]+'-toothed cog.obj', 'w') as f:
    for l in get_obj_str(get_cog_edge(*get_appropriate_value(tooth))):
        f.write(l + '\n')

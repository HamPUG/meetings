#+
# Load into Blender’s Text Editor and run to demonstrate
# a repeating task doing transformations on the default cube.
#-

import math
import time
import bpy
from mathutils import \
    Matrix, \
    Vector

DEG = math.pi / 180

count = 10

def rotate_cube() :
    global count
    obj = bpy.data.objects["Cube"]
    obj.matrix_basis = Matrix.Rotation(22.5 * DEG, 4, Vector((0, 1, 0))) @ obj.matrix_basis
    count -= 1
    if count > 0 :
        result = 1
    else :
        result = None
    #end if
    return result
#end rotate_cube

bpy.app.timers.register(rotate_cube)

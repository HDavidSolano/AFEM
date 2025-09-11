from afem.sketch import *
from afem.geometry import *
from afem.sketch import *
from afem.topology import *

from OCC.Display.SimpleGui import init_display

v, start, add_menu, add_fcn = init_display(backend_str='wx')
# Create a new cross-section
cs = Airfoil()

# Generate a 2-D profile by reading and approximating an airfoil file from
# the UIUC database. Close the trailing edge if necessary.
cs.read_uiuc('./clarky.txt', close=True)

# Define a plane at the root and scale
pln1 = PlaneByAxes(axes='xz').plane
cs.build(pln1, scale=5)
wire1 = cs.wires[0]
v.DisplayShape(wire1.displayed_shape)
# Define plane at the tip and rotate
pln2 = PlaneByAxes((3, 15, 0), axes='xz').plane
cs.build(pln2, scale=1.5, rotate=3)
wire2 = cs.wires[0]
v.DisplayShape(wire2.displayed_shape)

# Use the wires to loft a solid
shape = LoftShape([wire1, wire2], True).shape
v.DisplayShape(shape.displayed_shape)

start()


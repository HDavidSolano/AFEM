from afem.geometry import *
from afem.topology import *

from OCC.Display.SimpleGui import init_display

v, start, add_menu, add_fcn = init_display(backend_str='wx')

# Create a box by size
builder = BoxBySize(10, 10, 10)
box = builder.solid
box.set_transparency(0.5)

# Create a cylinder partially inside the box
circle = CircleByNormal((5, 5, 5), (0, 0, 1), 2).circle
face = FaceByPlanarWire(circle).face
cyl = SolidByDrag(face, (0, 0, 15)).solid

# View the two shapes
# v.DisplayShape(box.displayed_shape)
# v.DisplayShape(cyl.displayed_shape)
# start()

# Fuse the shapes
fuse = FuseShapes(box, cyl)
fused_shape = fuse.shape
fused_shape.set_transparency(0.5)  # TODO: seems to do nothing
# v.DisplayShape(fused_shape.object)
# start()

# Cut the cylinder from the box
cut = CutShapes(box, cyl)
cut_shape = cut.shape
# v.DisplayShape(cut_shape.object)
# start()


# Common material between the two shapes
common = CommonShapes(box, cyl)
common_shape = common.shape
# v.DisplayShape(common_shape.object)
# start()

# Intersect the shapes
sec = IntersectShapes(box, cyl)
sec_shape = sec.shape
# v.DisplayShape(sec_shape.object)
# start()

# Split the box with the cylinder. The resulting shape is a compound with
# two solids.
split = SplitShapes(box, cyl)
split_shape = split.shape
split_shape.set_transparency(0.5)
# v.DisplayShape(split_shape.object)
# start()
#
# Locally split one face of the box with a plane
pln = PlaneByAxes((5, 5, 5), 'xz').plane

local = LocalSplit(builder.front_face, pln, box)
local_shape = local.shape
local_shape.set_transparency(0.5)
# v.DisplayShape(local_shape.object)
# start()

# Offset the box
offset = OffsetShape(box, 2)
offset_shape = offset.shape
offset_shape.set_transparency(0.5)
# v.DisplayShape(box.object)
# v.DisplayShape(offset_shape.object)
# start()

# Rebuild the box with the results of the cut tool.
rebuild = RebuildShapeByTool(box, cut)
new_shape = rebuild.new_shape
# v.DisplayShape(new_shape.object)
# start()

# Check the new shape for errors
check = CheckShape(new_shape)
print('Shape is valid:', check.is_valid)
print('Shape type:', new_shape.shape_type)
# v.DisplayShape(new_shape.object)
# start()

# Since a face is removed it is no longer a valid solid but a shell. Try to
# fix the shape.
fix = FixShape(new_shape)
fixed_shape = fix.shape
pass
check = CheckShape(fixed_shape)
print('Shape is valid:', check.is_valid)
print('Shape type:', fixed_shape.shape_type)
# v.DisplayShape(fixed_shape.object)
# start()

# Find free edges of a shape
tool = ExploreFreeEdges(fixed_shape)

v.DisplayShape(tool.free_edges[0].object)
start()
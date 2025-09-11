from afem.config import Settings
from math import tan, radians
from afem.oml import Body
from afem.sketch import *
from afem.geometry import *
from afem.structure import *
from afem.topology import *
from OCC.Display.SimpleGui import init_display

v, start, add_menu, add_fcn = init_display(backend_str='wx')

Settings.log_to_console()

# Set units to inch.
Settings.set_units('in')

# Parameters
semispan = 107.  # wing semi-span
sweep = 34.  # Leading edge sweep
uk = 0.28  # Percent semi-span to locate section cross-section
c1 = 51.5  # Root chord
c2 = 31.  # Chord of second section
c3 = 7.  # Tip chord
t3 = 3.  # Tip washout in degrees

# Define leading edge points of cross-sections
p1x, p1y = 0., 0.
p2x = semispan * uk * tan(radians(sweep))
p2y = semispan * uk
p3x = semispan * tan(radians(sweep))
p3y = semispan

# Create a cross-section using an UIUC airfoil file
cs = Airfoil()
cs.read_uiuc('clarky.txt')

# Define cross section planes
pln1 = PlaneByAxes((p1x, p1y, 0), axes='xz').plane
pln2 = PlaneByAxes((p2x, p2y, 0), axes='xz').plane
pln3 = PlaneByAxes((p3x, p3y, 0), axes='xz').plane

# Build cross sections
cs.build(pln1, scale=c1)
wire1 = cs.wires[0]
cs.build(pln2, scale=c2)
wire2 = cs.wires[0]
cs.build(pln3, scale=c3, rotate=t3)
wire3 = cs.wires[0]

# Loft a solid
shape = LoftShape([wire1, wire2, wire3], True, make_ruled=True).shape

# Make a body
wing = Body(shape, 'Wing')
wing.set_transparency(0.5)
wing.set_color(1, 0, 0)

# to be between 0 and 1 for convenience.
chord1 = cs.build_chord(pln1, scale=c1)
chord2 = cs.build_chord(pln2, scale=c2)
chord3 = cs.build_chord(pln3, scale=c3, rotate=t3)
sref = NurbsSurfaceByInterp([chord1, chord2, chord3], 1).surface
sref.set_udomain(0., 1.)
sref.set_vdomain(0., 1.)

# Set the wing reference surface
wing.set_sref(sref)


# Define a group to put the structure in
wingbox = GroupAPI.create_group('wing box')
spars_assy = wingbox.create_subgroup('spar assy', active=True)
ribs_assy = wingbox.create_subgroup('rib assy', active=False)

# Define a front spar between parameters on the wing reference surface
fspar = SparByParameters('fspar', 0.15, 0.1, 0.15, 0.98, wing).part
# Define a rear spar between parameters on the wing reference surface
rspar = SparByParameters('rspar', 0.65, 0.1, 0.65, 0.98, wing).part

# Activate rib assembly
ribs_assy.activate()

# Define root rib between front and rear spar
root = RibByPoints('root', fspar.cref.p1, rspar.cref.p1, wing).part

# Define tip rib between front and rear spar
tip = RibByPoints('tip', fspar.cref.p2, rspar.cref.p2, wing).part

# Add ribs between root and tip perpendicular to rear spar reference curve
ribs = RibsAlongCurveByDistance('rib', rspar.cref, 10., fspar, rspar, wing,
                                d1=10., d2=-10.).parts

# Activate spar assembly
spars_assy.activate()

# Add a front center spar considering the intersection between the front
# spar and the root rib. If this is not considered, the front center spar
# may be oriented in such a way that causes it to have a gap with the front

# spar and root rib.
p1 = wing.sref.eval(0.25, .0)
pln = PlaneByIntersectingShapes(fspar.shape, root.shape, p1).plane
fcspar = SparByPoints('fcspar', p1, root.cref.p1, wing, pln).part

# Add rear center spar
p1 = wing.sref.eval(0.75, .0)
pln = PlaneByIntersectingShapes(rspar.shape, root.shape, p1).plane
rcspar = SparByPoints('rcspar', p1, root.cref.p2, wing, pln).part

# Activate rib assembly
ribs_assy.activate()

# Add center ribs using a reference plane alonge the rear center spar
ref_pln = PlaneByAxes(origin=(0., 0., 0.), axes='xz').plane
ribs2 = RibsAlongCurveByNumber('center rib', rcspar.cref, 3, fcspar, rcspar,
                              wing, ref_pln, d1=6, d2=-18).parts

# Join the internal structure using their reference curves to check for
# actual intersection
internal_parts = wingbox.get_parts()
FuseSurfacePartsByCref(internal_parts)

# Discard faces of parts using the reference curve
DiscardByCref(internal_parts)

# Activate wingbox assembly
wingbox.activate()



# Extract the shell of wing to define the wing skin
skin = SkinByBody('skin', wing).part
skin.set_transparency(0.5)



# Join the wing skin with the internal structure
skin.fuse(*internal_parts)



# Discard wing skin that is touching the wing reference surface. This
# should leave only the upper and lower skins.
print(skin.shape.shape_type)
skin.discard_by_dmin(wing.sref, 0.1)




# After removing the faces, the skin is now a compound of two shells, one
# upper shell and one lower. Use the Part.fix() to alter the shape from an
# invalid shell to a compound of two shells.
print('Skin shape type before fix:', skin.shape.shape_type)
skin.fix()
print('Skin shape type after fix:', skin.shape.shape_type)


# Check for free edges
shape = GroupAPI.get_shape()
tool = ExploreFreeEdges(shape)

for part in wingbox.get_parts():
    v.DisplayShape(part.displayed_shape)
v.DisplayShape(skin.displayed_shape)
start()
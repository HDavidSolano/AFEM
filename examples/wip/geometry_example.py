from afem.geometry import *
from OCC.Display.SimpleGui import init_display

v, start, add_menu, add_fcn = init_display(backend_str='wx')

# Create a point directly from the entity. Default is (0, 0, 0).
p1 = Point()

# Create a point by array-like
p2 = PointByArray([5, 0, 5]).point

# Create a point by x-, y-, and z-coordinates.
p3 = PointByXYZ(10, 0, 0).point

# Interpolate the points with a curve
c1 = NurbsCurveByInterp([p1, p2, p3]).curve

v.DisplayShape(p1)
v.DisplayShape(p2)
v.DisplayShape(p3)
v.DisplayShape(c1.object)

#TODO: Fix curve.copy() since it now returns Geom.Geom and not Geom.Nurbs, for instance

# Create a new curve and translate
c2 = NurbsCurveByInterp([p1, p2, p3]).curve
c2.translate((0, 10, 0))

v.DisplayShape(c2.object)

# Create new curve and translate again
c3 = NurbsCurveByInterp([p1, p2, p3]).curve
c3.translate((0, 20, 10))
v.DisplayShape(c3.object)

# Approximate a surface
s1 = NurbsSurfaceByApprox([c1, c2, c3]).surface

# Extract an iso-curve
c4 = s1.u_iso(10.)

v.DisplayShape(s1.object)
v.DisplayShape(c4.displayed_shape)
# Create points along the curve
pnts = PointsAlongCurveByDistance(c4, 1.).points
for point in pnts:
    v.DisplayShape(point)

# Extract iso-curve
c5 = s1.v_iso(0.5)

# Intersect two curves
cci = IntersectCurveCurve(c4, c5)
v.DisplayShape(c5.displayed_shape)
v.DisplayShape(cci.points[0], color='BLACK')
pnts2 = PointsAlongCurveByDistance(c5, 1.).points
for point in pnts2:
    v.DisplayShape(point)

# Define a plane along a curve
pln = PlaneFromParameter(c4, 0., 2.).plane

# Intersect a surface and a plane
ssi = IntersectSurfaceSurface(s1, pln)
v.DisplayShape(ssi.curves[0].object)

# Project a point to a surface
p4 = pln.eval(5, 5)
proj = ProjectPointToSurface(p4, s1)
line = NurbsCurveByInterp([p4, proj.nearest_point]).curve
v.DisplayShape(line.object)
start()
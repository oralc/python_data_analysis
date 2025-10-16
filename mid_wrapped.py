import math

def angle_midpoint(a1, a2):
    # Convert degrees to radians
    r1 = math.radians(a1)
    r2 = math.radians(a2)

    # Convert to unit vectors
    x1, y1 = math.cos(r1), math.sin(r1)
    x2, y2 = math.cos(r2), math.sin(r2)

    # Average the vectors
    xm, ym = (x1 + x2) / 2, (y1 + y2) / 2

    # Convert back to angle
    midpoint_rad = math.atan2(ym, xm)
    midpoint_deg = math.degrees(midpoint_rad)

    # Normalize to [-180, 180]
    if midpoint_deg > 180:
        midpoint_deg -= 360
    elif midpoint_deg < -180:
        midpoint_deg += 360


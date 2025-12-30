import math

def get_intersections(c1, r1, c2, r2):
    """
    Calculate intersection points of two circles.
    c1, c2: (x, y) tuples
    r1, r2: radii
    Returns list of (x, y) intersection points.
    """
    d = math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
    
    if d > r1 + r2: return [] # Separate
    if d < abs(r1 - r2): return [] # Contained
    if d == 0: return [] # Coincident
    
    a = (r1**2 - r2**2 + d**2) / (2*d)
    h = math.sqrt(max(0, r1**2 - a**2))
    
    x2 = c1[0] + a * (c2[0] - c1[0]) / d
    y2 = c1[1] + a * (c2[1] - c1[1]) / d
    
    x3_1 = x2 + h * (c2[1] - c1[1]) / d
    y3_1 = y2 - h * (c2[0] - c1[0]) / d
    
    x3_2 = x2 - h * (c2[1] - c1[1]) / d
    y3_2 = y2 + h * (c2[0] - c1[0]) / d
    
    return [(x3_1, y3_1), (x3_2, y3_2)]

def get_angle(center, point):
    return math.atan2(point[1] - center[1], point[0] - center[0])

def generate_arc_path(center, radius, start_angle, end_angle):
    # Convert angles to degrees for Skia (if needed) but here we generate points
    # For .icon we often use CUBIC_TO approximations or ARC_TO if supported.
    # Skia path commands in .icon:
    # MOVE_TO, x, y
    # ARC_TO, rx, ry, angle, large_arc_flag, sweep_flag, x, y
    
    # We will use ARC_TO.
    # Start point
    sx = center[0] + radius * math.cos(start_angle)
    sy = center[1] + radius * math.sin(start_angle)
    
    # End point
    ex = center[0] + radius * math.cos(end_angle)
    ey = center[1] + radius * math.sin(end_angle)
    
    # Large arc flag
    diff = end_angle - start_angle
    while diff < 0: diff += 2*math.pi
    large_arc = 1 if diff > math.pi else 0
    sweep = 1 # Assuming clockwise/counter-clockwise logic, verify
    
    # Output format
    return f"MOVE_TO, {sx:.2f}, {sy:.2f},\nARC_TO, {radius:.2f}, {radius:.2f}, 0, {large_arc}, {sweep}, {ex:.2f}, {ey:.2f}"

# Logo Parameters form SVG (Scaled to 32px)
S = 32.0 / 1024.0
C_MAIN = (513.3 * S, 510.8 * S) # (16.04, 15.96)
R_MAIN = 454.9 * S              # 14.21

# Stroke width 209 -> Half width for inner/outer
W_STROKE = 209 * S
H_STROKE = W_STROKE / 2.0

# Circle 2 (Bottom Right)
C2 = (758.2 * S, 988.4 * S)
R2_BASE = 411.5 * S
R2_OUTER = R2_BASE + H_STROKE
R2_INNER = R2_BASE - H_STROKE

# Circle 3 (Top Left)
C3 = (262.0 * S, 81.4 * S)
R3_BASE = 411.5 * S
R3_OUTER = R3_BASE + H_STROKE
R3_INNER = R3_BASE - H_STROKE

print("// Generated via convert_svg_geometry.py")
print(f"CANVAS_DIMENSIONS, 32,")

# Calculate Arc 1 (From Circle 2)
# We need the part of R2_OUTER/INNER that is INSIDE R_MAIN
# Intersection of R2_OUTER with R_MAIN
inter_outer = get_intersections(C2, R2_OUTER, C_MAIN, R_MAIN)
inter_inner = get_intersections(C2, R2_INNER, C_MAIN, R_MAIN)

# We expect 2 points for each if they intersect
if len(inter_outer) == 2 and len(inter_inner) == 2:
    # We need to sort points by angle or visual logic
    # The shape is the area BETWEEN outer and inner, bounded by the main circle clip.
    # So we trace:
    # 1. Inner Arc from P_In_1 to P_In_2
    # 2. Main Circle Arc from P_In_2 to P_Out_2 (Connecting the cut)
    # 3. Outer Arc from P_Out_2 to P_Out_1 (Reverse)
    # 4. Main Circle Arc from P_Out_1 to P_In_1 (Closing)
    
    # Determine the correct arc segment (the one INSIDE the main circle)
    # Center of main circle is (16,16). C2 is (23, 30).
    # The intersection points:
    pass 
    # Logic simplified: assuming the points returned are correct, we check which arc midpoint is inside R_MAIN
    
    def get_valid_arc(center, radius, p1, p2, clip_center, clip_radius):
        a1 = get_angle(center, p1)
        a2 = get_angle(center, p2)
        
        # Check mid angle
        mid = (a1 + a2) / 2
        mx = center[0] + radius * math.cos(mid)
        my = center[1] + radius * math.sin(mid)
        dist = math.sqrt((mx - clip_center[0])**2 + (my - clip_center[1])**2)
        
        # We want the part INSIDE
        if dist < clip_radius:
            return a1, a2
        else:
            # The other way around
            return a2, a1 + 2*math.pi # Wrap around

    # Outer Arc Angles
    oa1, oa2 = get_valid_arc(C2, R2_OUTER, inter_outer[0], inter_outer[1], C_MAIN, R_MAIN)
    # Inner Arc Angles
    ia1, ia2 = get_valid_arc(C2, R2_INNER, inter_inner[0], inter_inner[1], C_MAIN, R_MAIN)
    
    # Path: Inner Arc (Forward) -> Connect via Clip -> Outer Arc (Backward) -> Close
    # Note: Directions need to be consistent.
    
    # Let's verify angles.
    # C2 is bottom-right. The arc inside C_MAIN is mostly Top-Left of C2.
    
    # Generate Output
    # Start at Inner Start
    sx = C2[0] + R2_INNER * math.cos(ia1)
    sy = C2[1] + R2_INNER * math.sin(ia1)
    
    print(f"MOVE_TO, {sx:.2f}, {sy:.2f},")
    
    # Arc Inner (to ia2)
    ex = C2[0] + R2_INNER * math.cos(ia2)
    ey = C2[1] + R2_INNER * math.sin(ia2)
    # Sweep 1 (Clockwise) or 0? 
    # Standard math angle goes CCW. Skia might be CW?
    # Usually Positive Sweep = CW in screen coords?
    # Let's assume CCW (0) for now if calculated mathematically.
    print(f"ARC_TO, {R2_INNER:.2f}, {R2_INNER:.2f}, 0, 0, 1, {ex:.2f}, {ey:.2f}, // Inner Arc")
    
    # Line/Arc along Clip to Outer Start?
    # Intersection of Inner end with Clip -> Outer end with Clip
    # This segment follows the Clip Circle (R_MAIN)
    # From (ex, ey) to Outer Arc Intersect (approx nearest)
    # Note: This is complex. We might just LINE_TO if they are close, or simple ARC.
    # Let's assume we connect to the corresponding Outer Point.
    
    ox = C2[0] + R2_OUTER * math.cos(oa2)
    oy = C2[1] + R2_OUTER * math.sin(oa2)
    print(f"LINE_TO, {ox:.2f}, {oy:.2f}, // Join to Outer")
    
    # Outer Arc (Backward to oa1)
    ox_start = C2[0] + R2_OUTER * math.cos(oa1)
    oy_start = C2[1] + R2_OUTER * math.sin(oa1)
    print(f"ARC_TO, {R2_OUTER:.2f}, {R2_OUTER:.2f}, 0, 0, 0, {ox_start:.2f}, {oy_start:.2f}, // Outer Arc")
    
    print("CLOSE,")
    print("NEW_PATH,")

# Repeat for Circle 3 (Use same logic)
inter_outer_3 = get_intersections(C3, R3_OUTER, C_MAIN, R_MAIN)
inter_inner_3 = get_intersections(C3, R3_INNER, C_MAIN, R_MAIN)

if len(inter_outer_3) == 2:
    oa1, oa2 = get_valid_arc(C3, R3_OUTER, inter_outer_3[0], inter_outer_3[1], C_MAIN, R_MAIN)
    ia1, ia2 = get_valid_arc(C3, R3_INNER, inter_inner_3[0], inter_inner_3[1], C_MAIN, R_MAIN)
    
    sx = C3[0] + R3_INNER * math.cos(ia1)
    sy = C3[1] + R3_INNER * math.sin(ia1)
    print(f"MOVE_TO, {sx:.2f}, {sy:.2f},")
    ex = C3[0] + R3_INNER * math.cos(ia2)
    ey = C3[1] + R3_INNER * math.sin(ia2)
    print(f"ARC_TO, {R3_INNER:.2f}, {R3_INNER:.2f}, 0, 0, 1, {ex:.2f}, {ey:.2f},")
    ox = C3[0] + R3_OUTER * math.cos(oa2)
    oy = C3[1] + R3_OUTER * math.sin(oa2)
    print(f"LINE_TO, {ox:.2f}, {oy:.2f},")
    ox_start = C3[0] + R3_OUTER * math.cos(oa1)
    oy_start = C3[1] + R3_OUTER * math.sin(oa1)
    print(f"ARC_TO, {R3_OUTER:.2f}, {R3_OUTER:.2f}, 0, 0, 0, {ox_start:.2f}, {oy_start:.2f},")
    print("CLOSE")


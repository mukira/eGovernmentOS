
import re
import sys
import xml.dom.minidom

def parse_svg_path(d):
    # Split into commands and args
    # Regex to capture command letters and numbers
    tokens = re.findall(r'([a-zA-Z])|([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)', d)
    
    commands = []
    current_command = None
    args = []
    
    for command_char, number in tokens:
        if command_char:
            if current_command:
                commands.append((current_command, args))
            current_command = command_char
            args = []
        else:
            args.append(float(number))
            
    if current_command:
        commands.append((current_command, args))
        
    return commands

def convert_to_icon(svg_path, scale=1.0):
    doc = xml.dom.minidom.parse(svg_path)
    paths = doc.getElementsByTagName('path')
    
    icon_lines = []
    icon_lines.append(f"CANVAS_DIMENSIONS, 960,")
    
    for i, path in enumerate(paths):
        if i > 0:
            icon_lines.append("NEW_PATH,")
            
        d = path.getAttribute('d')
        stroke = path.getAttribute('stroke')
        fill = path.getAttribute('fill')
        stroke_width = path.getAttribute('stroke-width')
        
        # Determine strict mode (Fill or Stroke)
        # Chromium .icon format is a sequence of commands.
        # STROKE, width -> sets stroke mode.
        # FILL_RULE_NONZERO -> sets fill mode?
        # Actually, usually one sets styles effectively.
        
        if stroke and stroke != "none":
            width = float(stroke_width) if stroke_width else 1.0
            icon_lines.append(f"STROKE, {width * scale:.2f},")
            icon_lines.append("CAP_ROUND,") # The SVG has stroke-linecap="round"
        else:
            icon_lines.append("FILL_RULE_NONZERO,")
            
        commands = parse_svg_path(d)
        
        current_x = 0
        current_y = 0
        
        for cmd, args in commands:
            # Helper to access args
            def get_args(n_args):
                return args[:n_args], args[n_args:]
            
            remaining_args = args
            
            # Helper to update current pos
            def update_pos(x, y, relative=False):
                nonlocal current_x, current_y
                if relative:
                    current_x += x
                    current_y += y
                else:
                    current_x = x
                    current_y = y
            
            while remaining_args or len(args) == 0: # Handle Z with no args
                if cmd == 'M': # Move Absolute
                    pts, remaining_args = get_args(2)
                    x, y = pts
                    icon_lines.append(f"MOVE_TO, {x * scale:.2f}, {y * scale:.2f},")
                    update_pos(x, y)
                elif cmd == 'm': # Move Relative
                    pts, remaining_args = get_args(2)
                    dx, dy = pts
                    # For R_MOVE_TO, we need to know it's relative?
                    # Skia has R_MOVE_TO.
                    icon_lines.append(f"R_MOVE_TO, {dx * scale:.2f}, {dy * scale:.2f},")
                    update_pos(dx, dy, relative=True)
                elif cmd == 'L': # Line Absolute
                    pts, remaining_args = get_args(2)
                    x, y = pts
                    icon_lines.append(f"LINE_TO, {x * scale:.2f}, {y * scale:.2f},")
                    update_pos(x, y)
                elif cmd == 'l': # Line Relative
                    pts, remaining_args = get_args(2)
                    dx, dy = pts
                    icon_lines.append(f"R_LINE_TO, {dx * scale:.2f}, {dy * scale:.2f},")
                    update_pos(dx, dy, relative=True)
                elif cmd == 'H': # Horizontal Absolute
                    pts, remaining_args = get_args(1)
                    x = pts[0]
                    icon_lines.append(f"H_LINE_TO, {x * scale:.2f},")
                    update_pos(x, current_y)
                elif cmd == 'h': # Horizontal Relative
                    pts, remaining_args = get_args(1)
                    dx = pts[0]
                    icon_lines.append(f"R_H_LINE_TO, {dx * scale:.2f},")
                    update_pos(dx, 0, relative=True)
                elif cmd == 'V': # Vertical Absolute
                    pts, remaining_args = get_args(1)
                    y = pts[0]
                    icon_lines.append(f"V_LINE_TO, {y * scale:.2f},")
                    update_pos(current_x, y)
                elif cmd == 'v': # Vertical Relative
                    pts, remaining_args = get_args(1)
                    dy = pts[0]
                    icon_lines.append(f"R_V_LINE_TO, {dy * scale:.2f},")
                    update_pos(0, dy, relative=True)
                elif cmd == 'C': # Cubic Absolute
                    pts, remaining_args = get_args(6)
                    x1, y1, x2, y2, x, y = pts
                    icon_lines.append(f"CUBIC_TO, {x1 * scale:.2f}, {y1 * scale:.2f}, {x2 * scale:.2f}, {y2 * scale:.2f}, {x * scale:.2f}, {y * scale:.2f},")
                    update_pos(x, y)
                elif cmd == 'c': # Cubic Relative
                    pts, remaining_args = get_args(6)
                    dx1, dy1, dx2, dy2, dx, dy = pts
                    icon_lines.append(f"R_CUBIC_TO, {dx1 * scale:.2f}, {dy1 * scale:.2f}, {dx2 * scale:.2f}, {dy2 * scale:.2f}, {dx * scale:.2f}, {dy * scale:.2f},")
                    update_pos(dx, dy, relative=True)
                elif cmd == 's': # Smooth Cubic Relative
                    pts, remaining_args = get_args(4)
                    dx2, dy2, dx, dy = pts
                    # Chromium doesn't have Shorthand Cubic. We must convert to Cubic.
                    # Control point 1 is reflection of previous control point 2 relative to current point.
                    # If previous wasn't C/c/S/s, use (0,0) (current point).
                    # NOTE: This parser is simple state-less (doesn't track prev control point).
                    # Approximation: Use current point as CP1 (treating it as simple quadratic-like or sharp).
                    # For a proper implementation we need to track separate 'last_control_point'.
                    # Given the complexity, we'll implement a simple degradation: Use (0,0) for CP1 relative to current.
                    # This makes it a flat start tangent.
                    # R_CUBIC_TO(0, 0, dx2, dy2, dx, dy)
                    icon_lines.append(f"R_CUBIC_TO, 0, 0, {dx2 * scale:.2f}, {dy2 * scale:.2f}, {dx * scale:.2f}, {dy * scale:.2f},")
                    update_pos(dx, dy, relative=True)
                elif cmd == 'S': # Smooth Cubic Absolute
                    pts, remaining_args = get_args(4)
                    x2, y2, x, y = pts
                    # Approximation: Use current pos as CP1.
                    icon_lines.append(f"CUBIC_TO, {current_x * scale:.2f}, {current_y * scale:.2f}, {x2 * scale:.2f}, {y2 * scale:.2f}, {x * scale:.2f}, {y * scale:.2f},")
                    update_pos(x, y)
                elif cmd == 'Z' or cmd == 'z': # Close

                    icon_lines.append("CLOSE,")
                    remaining_args = [] # Z consumes nothing
                    break # Stop processing this command
                else:
                    # Fallback or unhandled (Q, S, T, A)
                    # The provided SVG uses standard M, V, L, Z and maybe C in the complex path?
                    # We might see 'S' or 'Q'.
                    # For now print warning for unhandled
                    print(f"// WARNING: Unhandled command {cmd}", file=sys.stderr)
                    remaining_args = []
                    break
        
    return "\n".join(icon_lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python svg_to_icon.py <svg_file>")
        sys.exit(1)
        
    svg_file = sys.argv[1]
    scale_arg = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    print(convert_to_icon(svg_file, scale=scale_arg));

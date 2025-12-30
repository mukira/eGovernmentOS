
import re
import sys
import xml.dom.minidom
import traceback

def parse_svg_path(d):
    # Split into commands and args
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
            if number:
                args.append(float(number))
            
    if current_command:
        commands.append((current_command, args))
        
    return commands

def convert_to_icon(svg_path, scale=1.0):
    try:
        doc = xml.dom.minidom.parse(svg_path)
        paths = doc.getElementsByTagName('path')
        
        icon_lines = []
        icon_lines.append(f"CANVAS_DIMENSIONS, 960,")
        
        for i, path in enumerate(paths):
            if i > 0:
                icon_lines.append("NEW_PATH,")
                
            d = path.getAttribute('d')
            if not d: continue
            
            icon_lines.append("FILL_RULE_NONZERO,")
            
            commands = parse_svg_path(d)
            
            current_x = 0
            current_y = 0
            
            for cmd, args in commands:
                sys.stderr.write(f"Cmd: {cmd}, Args: {len(args)}\n")
                
                def update_pos(x, y, relative=False):
                    nonlocal current_x, current_y
                    if relative:
                        current_x += x
                        current_y += y
                    else:
                        current_x = x
                        current_y = y
                
                # Z case
                if cmd.lower() == 'z':
                    icon_lines.append("CLOSE,")
                    continue
                
                remaining_args = args
                while remaining_args:
                    def pop_args(n):
                        nonlocal remaining_args
                        if len(remaining_args) < n:
                            raise ValueError(f"Not enough args for {cmd}: need {n}, got {len(remaining_args)}")
                        res = remaining_args[:n]
                        remaining_args = remaining_args[n:]
                        return res

                    if cmd == 'M':
                        pts = pop_args(2)
                        x, y = pts
                        icon_lines.append(f"MOVE_TO, {x * scale:.2f}, {y * scale:.2f},")
                        update_pos(x, y)
                        cmd = 'L' 
                    elif cmd == 'm':
                        pts = pop_args(2)
                        dx, dy = pts
                        icon_lines.append(f"R_MOVE_TO, {dx * scale:.2f}, {dy * scale:.2f},")
                        update_pos(dx, dy, relative=True)
                        cmd = 'l'
                    elif cmd == 'L':
                        pts = pop_args(2)
                        x, y = pts
                        icon_lines.append(f"LINE_TO, {x * scale:.2f}, {y * scale:.2f},")
                        update_pos(x, y)
                    elif cmd == 'l':
                        pts = pop_args(2)
                        dx, dy = pts
                        icon_lines.append(f"R_LINE_TO, {dx * scale:.2f}, {dy * scale:.2f},")
                        update_pos(dx, dy, relative=True)
                    elif cmd == 'H':
                        pts = pop_args(1)
                        x = pts[0]
                        icon_lines.append(f"H_LINE_TO, {x * scale:.2f},")
                        update_pos(x, current_y)
                    elif cmd == 'h':
                        pts = pop_args(1)
                        dx = pts[0]
                        icon_lines.append(f"R_H_LINE_TO, {dx * scale:.2f},")
                        update_pos(dx, 0, relative=True)
                    elif cmd == 'V':
                        pts = pop_args(1)
                        y = pts[0]
                        icon_lines.append(f"V_LINE_TO, {y * scale:.2f},")
                        update_pos(current_x, y)
                    elif cmd == 'v':
                        pts = pop_args(1)
                        dy = pts[0]
                        icon_lines.append(f"R_V_LINE_TO, {dy * scale:.2f},")
                        update_pos(0, dy, relative=True)
                    elif cmd == 'C':
                        pts = pop_args(6)
                        x1, y1, x2, y2, x, y = pts
                        icon_lines.append(f"CUBIC_TO, {x1 * scale:.2f}, {y1 * scale:.2f}, {x2 * scale:.2f}, {y2 * scale:.2f}, {x * scale:.2f}, {y * scale:.2f},")
                        update_pos(x, y)
                    elif cmd == 'c':
                        pts = pop_args(6)
                        dx1, dy1, dx2, dy2, dx, dy = pts
                        icon_lines.append(f"R_CUBIC_TO, {dx1 * scale:.2f}, {dy1 * scale:.2f}, {dx2 * scale:.2f}, {dy2 * scale:.2f}, {dx * scale:.2f}, {dy * scale:.2f},")
                        update_pos(dx, dy, relative=True)
                    elif cmd == 's':
                        pts = pop_args(4)
                        dx2, dy2, dx, dy = pts
                        icon_lines.append(f"R_CUBIC_TO, 0, 0, {dx2 * scale:.2f}, {dy2 * scale:.2f}, {dx * scale:.2f}, {dy * scale:.2f},")
                        update_pos(dx, dy, relative=True)
                    elif cmd == 'S':
                        pts = pop_args(4)
                        x2, y2, x, y = pts
                        icon_lines.append(f"CUBIC_TO, {current_x * scale:.2f}, {current_y * scale:.2f}, {x2 * scale:.2f}, {y2 * scale:.2f}, {x * scale:.2f}, {y * scale:.2f},")
                        update_pos(x, y)
                    else:
                        sys.stderr.write(f"Unknown cmd: {cmd}\n")
                        break
                        
        return "\n".join(icon_lines)
    except Exception as e:
        sys.stderr.write(traceback.format_exc())
        return str(e)

if __name__ == "__main__":
    svg_file = sys.argv[1]
    scale_arg = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    output_content = convert_to_icon(svg_file, scale=scale_arg)
    
    if len(sys.argv) > 3:
        with open(sys.argv[3], 'w') as f:
            f.write(output_content)
    else:
        print(output_content)

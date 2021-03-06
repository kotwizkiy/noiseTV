defaults = '''300 #float. Can be 0 (actually, means 3600)
100 #int (px)
mouse #color palette: 'b/w'/'rainbow'/'wheel-saturation'/'wheel-hue'/'mouse'/'keyboard'/'%x %y'(int,int)
cross #'cross'/'arrow'/'no'
2D #'2D'/'3D'
#Read more at: https://github.com/kotwizkiy/noiseTV/README.md'''

try:
    config_file = open('config', 'r')
except Exception:
    print('No config file!')
    config_file = open('config', 'w')
    config_file.write(defaults)
    config_file.close()
    config_file = open('config', 'r')
global wheel, kb_x, kb_y, config
wheel = 0
kb_x, kb_y = 0, 0
config = []
for lin in config_file:
    config.append(lin)


def draw_a_wall(col, side, all_hue):
    for i in xrange(0, width, side):
        for j in xrange(0, height, side):
            if all_hue:
                fill(random(col[0]), random(col[1]), random(255))
            else:
                fill(random(col[0] - 30, col[0] + 30),
                     random(col[1]), random(255))
            rect(i, j, side, side)


def setup():
    global config
    size(displayWidth, displayHeight, P3D)
    cursor_type = config[3].split()[0]
    if cursor_type.lower() == 'no':
        noCursor()
    elif cursor_type.lower() == 'cross':
        cursor(CROSS)
    else:
        cursor(ARROW)
    if (frame is not None):
        frame.setResizable(True)
    bpm = float(config[0].split()[0])
    if bpm != 0:
        frameRate(bpm / 60.0)
    else:
        pass
    colorMode(HSB, width, height, 255)
    noStroke()
    background(0)


def draw():
    global config, wheel, kb_x, kb_y
    side = int(config[1].split()[0])
    palette = config[2].split()[0]
    all_hue = True
    if palette.lower() == 'b/w':
        col = (0, 0)
    elif palette.lower() == 'rainbow':
        col = (width, height)
    elif palette.lower() == 'mouse':
        col = mouseX, mouseY
        all_hue = False
    elif palette.lower() == 'wheel-saturation':
        col = (width, wheel % height)
    elif palette.lower() == 'wheel-hue':
        col = wheel % width, height
        all_hue = False
    elif palette.lower() == 'keyboard':
        col = kb_x % width, height - (kb_y % height)
        all_hue = False
    else:
        tmp = config[2].split()
        col = int(tmp[0]) * (width / 255.0),  int(tmp[1]) * (height / 255.0)

    mode = config[4].split()[0]
    if mode.lower() == '3d':
        stroke(0)
        background(col[0], col[1], 255)
        rotateY(PI / 2.0)
        draw_a_wall(col, side, all_hue)
        translate(width / 2, 0)
        rotateY(-PI / 2.0)
        draw_a_wall(col, side, all_hue)
        translate(width, 0)
        rotateY(-PI / 2.0)
        draw_a_wall(col, side, all_hue)
    else:
        draw_a_wall(col, side, all_hue)


def mouseWheel(event):
    global wheel
    wheel += event.getCount() * 10
    if wheel > 10 ** 8:
        wheel %= (10 ** 8)


def keyReleased():
    global kb_x, kb_y
    #   38
    # 37 40 39
    if keyCode == 38:
        kb_y -= 20
    elif keyCode == 40:
        kb_y += 20
    elif keyCode == 37:
        kb_x -= 20
    elif keyCode == 39:
        kb_x += 20

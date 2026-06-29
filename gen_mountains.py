import random, re
def generate_mountain(width, height, detail, roughness, initial_points, color):
    points = initial_points
    for _ in range(detail):
        new_points = []
        for i in range(len(points) - 1):
            p1, p2 = points[i], points[i+1]
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2 + random.uniform(-roughness, roughness)
            new_points.extend([p1, (mid_x, mid_y)])
        new_points.append(points[-1])
        points = new_points
        roughness *= 0.5
    path = f'M0,{height} '
    for p in points:
        path += f'L{p[0]:.1f},{max(0, min(height, p[1])):.1f} '
    path += f'L{width},{height} Z'
    return f'<path d="{path}" fill="{color}" />'

random.seed(42)
width, height = 1200, 300
svg_paths = ''

# We define prominent macro peaks for each layer, then add fractal detail.
# Lower y is higher on screen.
l1_init = [(0, 180), (180, 50), (450, 160), (750, 40), (1000, 130), (1200, 190)]
l2_init = [(0, 190), (320, 70), (550, 150), (880, 60), (1050, 110), (1200, 180)]
l3_init = [(0, 220), (250, 110), (500, 200), (680, 90), (950, 170), (1200, 140)]
l4_init = [(0, 260), (120, 170), (400, 240), (820, 120), (1100, 220), (1200, 250)]

svg_paths += generate_mountain(width, height, 7, 30, l1_init, '#0a1428') + '\n      '
svg_paths += generate_mountain(width, height, 7, 28, l2_init, '#070d1b') + '\n      '
svg_paths += generate_mountain(width, height, 7, 25, l3_init, '#040810') + '\n      '
svg_paths += generate_mountain(width, height, 7, 22, l4_init, '#010204')

svg_code = f'''<div class="mountains-wrap">
    <svg viewBox="0 0 {width} {height}" preserveAspectRatio="none" style="width:100%; height:100%; display:block; position:absolute; bottom:0; left:0;">
      {svg_paths}
    </svg>
    <div class="mountain-fade"></div>
  </div>'''

with open('louella-ranes-homepage (1).html', 'r', encoding='utf-8') as f:
    c = f.read()

c = re.sub(r'<div class="mountains-wrap">.*?<div class="mountain-fade"></div>\s*</div>', svg_code, c, flags=re.DOTALL)
# Make sure height is large enough to show the peaks properly
c = c.replace('height:40vh', 'height:45vh')

with open('louella-ranes-homepage (1).html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done realistic peaks')

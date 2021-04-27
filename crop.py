import os
import re
import math
import subprocess


def crop(width, height, off_x, off_y, length, png_path, png_crop_path):
    command = ["/opt/homebrew/bin/convert", '-extract', f'{width}x{height}+{off_x}+{off_y}', '-scale', str(length),
               png_path, png_crop_path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    exit_code = process.wait()
    if exit_code > 0:
        raise Exception(f'Error cropping {svg_path}, exit code {exit_code}')


def svg_to_png(svg_path, png_path):
    command = ["/opt/homebrew/bin/convert", svg_path, png_path]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    exit_code = process.wait()
    if exit_code > 0:
        raise Exception(f'Error converting {svg_path} to {png_path}, exit code {exit_code}')


dir_name = 'out_dev'
script_path = os.path.dirname(os.path.abspath(__file__))
path = f'{script_path}/{dir_name}'
svg_path = f'{path}/22384-1.svg'
length = 576
scale = length * 2

with open(svg_path, 'r') as f:
    svg = f.read()

re_svg_width = re.compile('(?<=<svg width=").+(?=px" height=")')
re_svg_height = re.compile('(?<=px" height=").+(?=px" viewBox=")')
svg_width = float(re_svg_width.search(svg).group(0))
svg_height = float(re_svg_height.search(svg).group(0))
png_width = round(svg_width)
png_height = round(svg_height)

svg_width_quads = math.ceil(svg_width / (length * 2))
svg_height_quads = math.ceil(svg_height / (length * 2))
print(svg_width_quads)
print(svg_height_quads)

svg_to_png(svg_path, f'{path}/22384.png')
off_x = 0
off_y = 0
for y in range(1, svg_height_quads):
    off_x = 0
    for x in range(1, svg_width_quads):
        print(scale, scale, off_x, off_y)
        crop(scale, scale, off_x, off_y, length, f'{path}/22384.png', f'{path}/22384_{y}{x}.png')
        off_x = scale * x
    off_y = scale * y

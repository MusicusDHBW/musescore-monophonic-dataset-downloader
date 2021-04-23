import os
import subprocess

dir_name = 'out_dev'
files = os.listdir(dir_name)
script_path = os.path.dirname(os.path.abspath(__file__))

for file in files:
    filename = file.replace('.mscz', '')
    command_svg = ["/Applications/MuseScore 3.app/Contents/MacOS/mscore", f'{script_path}/{dir_name}/{file}', '-T', '0',
           '-o', f'{script_path}/{dir_name}/{filename}.svg']
    process_svg = subprocess.Popen(command_svg, stdout=subprocess.PIPE)
    stdout, stderr = process_svg.communicate()
    exit_code = process_svg.wait()
    print(f'Exitcode SVG: {exit_code}')
    if exit_code > 0:
        break
    svg_count = 0
    for file_new in os.listdir(dir_name):
        if file_new.endswith('.svg') and file_new.startswith(filename):
            svg_count += 1
    if svg_count > 1:
        for i in range(1, svg_count+1):
            os.remove(f'{script_path}/{dir_name}/{filename}-{i}.svg')
        continue
    command_musicxml = ["/Applications/MuseScore 3.app/Contents/MacOS/mscore", f'{script_path}/{dir_name}/{file}',
                   '-o', f'{script_path}/{dir_name}/{filename}.musicxml']
    process_musicxml = subprocess.Popen(command_musicxml, stdout=subprocess.PIPE)
    stdout, stderr = process_musicxml.communicate()
    exit_code = process_musicxml.wait()
    print(f'Exitcode XML: {exit_code}')
    if exit_code > 0:
        break

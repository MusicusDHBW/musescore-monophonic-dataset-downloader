import os
import subprocess

dir_name = 'out_train'
files = os.listdir(dir_name)
script_path = os.path.dirname(os.path.abspath(__file__))

for file in files:
    filename = file.replace('.mscz', '')
    svg_path = f'{script_path}/{dir_name}/{filename}.svg'
    try:
        command_svg = ["/Applications/MuseScore 3.app/Contents/MacOS/mscore", f'{script_path}/{dir_name}/{file}', '-T',
                       '10',
                       '-o', svg_path]
        process_svg = subprocess.Popen(command_svg, stdout=subprocess.PIPE)
        stdout, stderr = process_svg.communicate()
        exit_code = process_svg.wait()
        if exit_code > 0:
            raise Exception(f'Error converting {script_path}/{dir_name}/{file} to svg, error code {exit_code}')
        svg_count = 0
        for file_new in os.listdir(dir_name):
            if file_new.endswith('.svg') and file_new.startswith(filename):
                svg_count += 1
        if svg_count > 1:
            if svg_count >= 10:
                for i in range(1, svg_count + 1):
                    os.remove(f'{script_path}/{dir_name}/{filename}-{i:02d}.svg')
            else:
                for i in range(1, svg_count + 1):
                    os.remove(f'{script_path}/{dir_name}/{filename}-{i}.svg')
            continue
        os.rename(f'{script_path}/{dir_name}/{filename}-1.svg', svg_path)
        command_musicxml = ["/Applications/MuseScore 3.app/Contents/MacOS/mscore", f'{script_path}/{dir_name}/{file}',
                            '-o', f'{script_path}/{dir_name}/{filename}.musicxml']
        process_musicxml = subprocess.Popen(command_musicxml, stdout=subprocess.PIPE)
        stdout, stderr = process_musicxml.communicate()
        exit_code = process_musicxml.wait()
        if exit_code > 0:
            raise Exception(f'Error converting {script_path}/{dir_name}/{file} to musicxml, error code {exit_code}')

        command_png = ["/Applications/Inkscape.app/Contents/MacOS/inkscape", '--export-type=png', svg_path]
        process = subprocess.Popen(command_png, stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        exit_code = process.wait()
        if exit_code > 0:
            raise Exception(f'Error converting {svg_path} to png, exit code {exit_code}')
    except:
        if os.path.exists(f'{script_path}/{dir_name}/{filename}.mscz'):
            os.remove(f'{script_path}/{dir_name}/{filename}.mscz')
        if os.path.exists(f'{script_path}/{dir_name}/{filename}.musicxml'):
            os.remove(f'{script_path}/{dir_name}/{filename}.musicxml')
        if os.path.exists(f'{script_path}/{dir_name}/{filename}.png'):
            os.remove(f'{script_path}/{dir_name}/{filename}.png')
        if os.path.exists(f'{script_path}/{dir_name}/{filename}.svg'):
            os.remove(f'{script_path}/{dir_name}/{filename}.svg')
        if os.path.exists(f'{script_path}/{dir_name}/{filename}-1.svg'):
            os.remove(f'{script_path}/{dir_name}/{filename}-1.svg')
        with open(f'{script_path}/{dir_name}/error.log', 'a') as f:
            f.write(f'{filename} conversion\n')
        continue

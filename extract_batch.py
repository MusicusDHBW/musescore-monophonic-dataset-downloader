import os

import extract

directory = 'dataset_v2'
files = [file.replace('.musicxml', '') for file in os.listdir(directory) if file.endswith('.musicxml')]

for file in files:
    score = extract.Score()
    print(file)
    try:
        classification = score.classify(f'{directory}/{file}.svg', f'{directory}/{file}.musicxml')
    except Exception as e:
        os.remove(f'{directory}/{file}.musicxml')
        os.remove(f'{directory}/{file}.svg')
        os.remove(f'{directory}/{file}.png')
        with open(f'{directory}/error.log', 'a') as f:
            f.write(f'{file} classify: {getattr(e, "message", repr(e))}\n')
        continue
    with open(f'{directory}/{file}.coco', 'w') as f:
        f.write(classification)

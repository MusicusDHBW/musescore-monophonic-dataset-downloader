import os

import extract

directory = 'out_dev'
files = [file.replace('.musicxml', '') for file in os.listdir(directory) if file.endswith('.musicxml')]

for file in files:
    score = extract.Score()
    print(file)
    classification = score.classify(f'{directory}/{file}-1.svg', f'{directory}/{file}.musicxml')
    with open(f'{directory}/{file}.coord', 'w') as f:
        f.write(classification)

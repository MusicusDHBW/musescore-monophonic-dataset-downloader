import sys
import requests
import subprocess
import os
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    files = open(sys.argv[1], 'r').read().split('\n')
    outputDir = sys.argv[2]

    for file in files:
        idAndRef = file.split(':')
        ident = idAndRef[0]
        ref = idAndRef[1]

        url = 'https://dweb.link/ipfs/' + ref
        request = requests.get(url, allow_redirects=True)
        with open(outputDir + '/' + ident + '.mscz', 'wb') as out:
            out.write(request.content)

        #path = os.getcwd() + "\\" + outputDir + "\\" + ident
        #print(path)
        #png = path + ".png"
        #print(png)
        #mscz = path + ".mscz"
        #print(mscz)
        #command = ["MuseScore3", "-o", png, mscz]
        #print(command)
        #subprocess.run(command)
        #subprocess.run(["MuseScore3", "-o", path + "/" + ident + ".musicxml", path + "/" + ident + ".mscz"])


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

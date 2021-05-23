import sys
import requests
import subprocess
import os

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
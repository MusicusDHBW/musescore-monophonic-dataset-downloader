import sys
import re

if __name__ == '__main__':
    fileRefs = open(sys.argv[2], "r").read()
    fileIds = open(sys.argv[1], "r").read().split('\n')

    for ident in fileIds:
        pattern = re.compile('(?<=^' + ident + ',/ipfs/).+(?=,)', re.MULTILINE)
        ref = re.search(pattern, fileRefs)
        if ref:
            with open(sys.argv[3], "a") as f:
                f.write(ident + ':' + ref.group(0) + "\n")

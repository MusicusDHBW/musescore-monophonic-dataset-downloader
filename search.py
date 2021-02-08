# This is a sample Python script.
import sys
import re
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    fileRefs = open(sys.argv[2], "r").read()
    fileIds = open(sys.argv[1], "r").read().split('\n')

    for ident in fileIds:
        pattern = re.compile('(?<=^' + ident + ',/ipfs/).+(?=,)', re.MULTILINE)
        ref = re.search(pattern, fileRefs)
        if ref:
            with open(sys.argv[3], "a") as f:
                f.write(ident + ':' + ref.group(0) + "\n")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import sys
import requests
from music21 import *
import subprocess
import os
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    clefLineLoc = {
        'treble': {
            'A3': -4, 'B3': -3, 'C4': -2, 'D4': -1, 'E4': 0, 'F4': 1, 'G4': 2,
            'A4': 3, 'B4': 4, 'C5': 5, 'D5': 6, 'E5': 7, 'F5': 8, 'G5': 9, 'A5': 10, 'B5': 11, 'C6': 12
        },
        'bass': {
            'C2': -4, 'D2': -3, 'E2': -2, 'F2': -1, 'G2': 0, 'A2': 1, 'B2': 2,
            'C3': 3, 'D3': 4, 'E3': 5, 'F3': 6, 'G3': 7, 'A3': 8, 'B3': 9, 'C4': 10, 'D4': 11, 'E4': 12
        },
        'alto': {
            'B2': -4, 'C3': -3, 'D3': -2, 'E3': -1, 'F3': 0, 'G3': 1, 'A3': 2,
            'B3': 3, 'C4': 4, 'D4': 5, 'E4': 6, 'F4': 7, 'G4': 8, 'A4': 9, 'B4': 10, 'C5': 11, 'D5': 12
        },
        'tenor': {
            'C2': -4, 'D2': -3, 'E2': -2, 'F2': -1, 'G2': 0, 'A2': 1, 'B2': 2,
            'C3': 3, 'D3': 4, 'E3': 5, 'F3': 6, 'G3': 7, 'A3': 8, 'B3': 9, 'C4': 10, 'D4': 11, 'E4': 12
        }
    }

    score = converter.parse('experiement/pitch.musicxml')
    # partsStream = score.getElementsByClass(stream.Part)
    # for part in score.getElementsByClass(stream.Part):
    #     for measure in part.getElementsByClass(stream.Measure):
    #         for note in measure.getElementsByClass("Note"):
    #             print(note.step, note.duration, note.offset)
    #
    # for note in score.flat.getElementsByClass("Note"):
    #     print(note.step, note.duration, note.offset, note.octave)
    #
    # for clef in score.flat.getElementsByClass("Clef"):
    #     print(clef.name, clef.offset, clef.lowestLine, clef.line)
    #
    # for rest in score.flat.getElementsByClass("Rest"):
    #     print(rest, rest.duration, rest.offset)
    # #partsStream.show('text')
    # print("\n")
    currentClef = clefLineLoc['treble']
    for element in score.flat:
        if isinstance(element, clef.Clef):
            print("Clef: " + element.name)
            currentClef = clefLineLoc[element.name]
        if isinstance(element, note.Note):
            print("Note:", element.nameWithOctave, "Duration:", element.duration.quarterLength, "PitchLine:", currentClef[element.nameWithOctave])
        if isinstance(element, note.Rest):
            print("Rest:", element.duration.quarterLength)
        if isinstance(element, meter.TimeSignature):
            print("TimeSignature: ", element.ratioString)


    #print(len(partsStream))


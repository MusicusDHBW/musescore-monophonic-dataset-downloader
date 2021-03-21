import sys
import requests
from music21 import *
from svgelements import *
import subprocess
import os


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def bbox_to_rect(bbox, color):
    x = bbox[0]
    y = bbox[1]
    w = bbox[2] - x
    h = bbox[3] - y
    print('<rect x="' + str(x) + '" y="' + str(y) + '" width="' + str(w) + '" height="' + str(
        h) + '" style="stroke:' + color + '; fill: none"/>')


def bbox_to_dict(bbox):
    d = dict()
    d['x'] = bbox[0]
    d['y'] = bbox[1]
    d['w'] = bbox[2] - bbox[0]
    d['h'] = bbox[3] - bbox[1]
    return d


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

    svgAccidentals = list()
    svgKeysigs = list()
    svgClefs = list()
    svgRests = list()
    svgTimesigs = list()
    svgBarlines = list()

    svgNotes = list()
    svgStems = list()
    svgHooks = list()
    svgNoteDots = list()

    svg = SVG.parse('experiement/pitch_v2-1.svg')
    for element in svg.elements():
        classType = element.values.get('class')
        if classType == 'Note':
            svgNotes.append(element)
        elif classType == 'Rest':
            svgRests.append(element)
        elif classType == 'TimeSig':
            svgTimesigs.append(element)
        elif classType == 'KeySig':
            svgKeysigs.append(element)
        elif classType == 'Clef':
            svgClefs.append(element)
        elif classType == 'BarLine':
            svgBarlines.append(element)
        elif classType == 'Accidental':
            svgAccidentals.append(element)
        elif classType == 'Stem':
            svgStems.append(element)
        elif classType == 'Hook':
            svgHooks.append(element)
        elif classType == 'NoteDot':
            svgNoteDots.append(element)
    print(len(svgKeysigs))
    svgAccidentalsIter = iter(svgAccidentals)
    svgKeysigsIter = iter(svgKeysigs)
    svgClefsIter = iter(svgClefs)
    svgRestsIter = iter(svgRests)
    svgTimesigsIter = iter(svgTimesigs)
    svgBarlinesIter = iter(svgBarlines)

    svgNotesIter = iter(svgNotes)
    svgStemsIter = iter(svgStems)
    svgHooksIter = iter(svgHooks)
    svgNoteDotsIter = iter(svgNoteDots)

    score = converter.parse('experiement/pitch_v2.musicxml')

    lastClef = None
    lastKeySign = None
    lastTimeSign = None


    def add_clef():
        path = next(svgClefsIter)
        bbox_to_rect(path.bbox(), '#E68F40')


    def add_timesign():
        numerator = next(svgTimesigsIter)
        bbox_to_rect(numerator.bbox(), '#FAFC53')
        denominator = next(svgTimesigsIter)
        bbox_to_rect(denominator.bbox(), '#FAFC53')


    def add_keysign():
        global lastKeySign
        sharps = lastKeySign.sharps
        if sharps > 0:
            for x in range(0, sharps):
                path = next(svgKeysigsIter)
                bbox_to_rect(path.bbox(), '#FF47DF')
        elif sharps < 0:
            for x in range(sharps, 0):
                path = next(svgKeysigsIter)
                bbox_to_rect(path.bbox(), '#FF47DF')


    def set_clef(new_clef):
        global lastClef
        old_last_clef = lastClef
        lastClef = new_clef
        if old_last_clef is not None:
            add_clef()


    def set_keysign(new_keysign):
        global lastKeySign
        old_last_keysign = lastKeySign
        lastKeySign = new_keysign
        if old_last_keysign is not None:
            add_keysign()


    def set_timesign(new_timesign):
        global lastTimeSign
        old_last_timesign = lastTimeSign
        lastTimeSign = new_timesign
        if old_last_timesign is not None:
            add_timesign()

    partsStream = score.getElementsByClass(stream.Part)
    for part in score.getElementsByClass(stream.Part):
        mIndex = 0
        for measure in part.getElementsByClass(stream.Measure):
            # print(len(measure))
            for i in range(0, len(measure)):
                if isinstance(measure[i], layout.SystemLayout):
                    if isinstance(measure[i + 1], clef.Clef):
                        set_clef(measure[i + 1])
                        add_clef()
                        if isinstance(measure[i + 2], key.KeySignature):
                            set_keysign(measure[i + 2])
                            add_keysign()
                            if isinstance(measure[i + 3], meter.TimeSignature):
                                set_timesign(measure[i + 3])
                                add_timesign()
                        elif isinstance(measure[i + 2], meter.TimeSignature):
                            set_timesign(measure[i + 2])
                            add_timesign()

                            add_keysign()
                        else:
                            add_keysign()
                    elif isinstance(measure[i + 1], key.KeySignature):
                        set_keysign(measure[i + 1])
                        add_keysign()

                        add_clef()
                        if isinstance(measure[i + 1], meter.TimeSignature):
                            set_timesign(measure[i + 1])
                            add_timesign()
                    elif isinstance(measure[i + 1], meter.TimeSignature):
                        set_timesign(measure[i + 1])
                        add_timesign()

                        add_clef()
                        add_keysign()
                    else:
                        add_clef()
                        add_keysign()

                # if isinstance(measure[i], note.Note) or isinstance(measure[i], note.Rest):
                # print(measure[i])
            mIndex += 1

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
    elements = list()
    # for element in score.flat:
    #     print(element)
    # if isinstance(element, note.Note):
    #     duration = element.quarterLength
    #     if not (element.pitch.accidental is None):
    #         bbox_to_rect(next(svgAccidentalsIter).bbox(), '#f0f000')
    #         # print(element.nameWithOctave, "accidental:", element.pitch.accidental.name)
    #
    #     line = currentClef[element.nameWithOctave.replace('-', '').replace('#', '')]
    #     # print(str(duration) + ', ' + str(line))
    #     boxElement = next(svgNotesIter)
    #     if duration < 4.0:  # all notes with a stem
    #         boxElement += next(svgStemsIter)
    #     if duration in (3.0, 1.5, 0.75):  # all notes with a dot
    #         boxElement += next(svgNoteDotsIter)
    #     # how the fuck can I detect which notes have hooks and which beam
    #     # if duration > 1.0:
    #     #     boxElement += next(svgHooksIter)
    #     bbox_to_rect(boxElement.bbox(), '#ff0000')
    # elif isinstance(element, note.Rest):
    #     duration = element.quarterLength
    #     # print(duration)
    #     boxElement = next(svgRestsIter)
    #     # if duration in (3.0, 1.5, 0.75):  # all notes with a dot
    #     #     print('rest')
    #     #     boxElement += next(svgNoteDotsIter)
    #     bbox_to_rect(boxElement.bbox(), '#00f0f0')
    # elif isinstance(element, clef.Clef):
    #     # print("Clef: " + element.name)
    #     currentClef = clefLineLoc[element.name]
    #     boxElement = next(svgClefsIter)
    #     # bbox_to_rect(boxElement.bbox(), '#0f0f00')
    # if isinstance(element, meter.TimeSignature):
    #     # element.numerator
    #     numerator = next(svgTimesigsIter)
    #     bbox_to_rect(numerator.bbox(), '#F06C29')
    #     # element.denominator
    #     denominator = next(svgTimesigsIter)
    #     bbox_to_rect(denominator.bbox(), '#F06C29')
    # if isinstance(element, key.KeySignature):
    #     print(element)

    # print(len(partsStream))

import sys
from music21 import *
from svgelements import *

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class StaffSystem:
    def __init__(self, y):
        self.y = y
        self.notes = list()
        self.dots = list()
        self.stems = list()
        self.hooks = list()
        self.rests = list()


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


def get_staff_system_index(element, systems):
    element_y = element.bbox()[1]
    min_dist = sys.maxsize
    min_index = 0
    for i in range(len(systems)):
        dist = abs(element_y - systems[i].y)
        if dist < min_dist:
            min_dist = dist
            min_index = i
    return min_index


def sort_after_x(element):
    return element.bbox()[0]


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

    svg = SVG.parse('experiement/durations_only_dots-1.svg')
    linesIndex = 0
    staffLines = None
    systems = list()
    for element in svg.elements():
        classType = element.values.get('class')
        if classType == 'StaffLines':
            if linesIndex == 0:
                staffLines = element
                linesIndex += 1
            elif linesIndex == 4:
                staffLines += element
                linesIndex = 0
                systems.append(StaffSystem((staffLines.bbox()[3] - staffLines.bbox()[1]) / 2 + staffLines.bbox()[1]))
            else:
                staffLines += element
                linesIndex += 1

    for element in svg.elements():
        # print(element)
        classType = element.values.get('class')
        if classType == 'Note':
            systems[get_staff_system_index(element, systems)].notes.append(element)
        elif classType == 'Rest':
            systems[get_staff_system_index(element, systems)].rests.append(element)
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
            systems[get_staff_system_index(element, systems)].stems.append(element)
        elif classType == 'Hook':
            systems[get_staff_system_index(element, systems)].hooks.append(element)
        elif classType == 'NoteDot':
            systems[get_staff_system_index(element, systems)].dots.append(element)

    for system in systems:
        svgNotes.extend(sorted(system.notes, key=sort_after_x))
        svgNoteDots.extend(sorted(system.dots, key=sort_after_x))
        svgStems.extend(sorted(system.stems, key=sort_after_x))
        svgHooks.extend(sorted(system.hooks, key=sort_after_x))
        svgRests.extend(sorted(system.rests, key=sort_after_x))

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

    score = converter.parse('experiement/durations_only_dots.musicxml')

    lastClef = None
    lastKeySign = None
    lastTimeSign = None
    currentClef = clefLineLoc['treble']


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
                elif isinstance(measure[i], note.Note):
                    duration = measure[i].quarterLength
                    if not (measure[i].pitch.accidental is None):
                        bbox_to_rect(next(svgAccidentalsIter).bbox(), '#f0f000')
                    boxElement = next(svgNotesIter)
                    if duration < 4.0:  # all notes with a stem
                        boxElement += next(svgStemsIter)
                    if measure[i].duration.quarterLength in (3.0, 1.5, 0.75):  # all notes with a dot
                        boxElement += next(svgNoteDotsIter)
                    # how the fuck can I detect which notes have hooks and which beam
                    # if duration > 1.0:
                    #     boxElement += next(svgHooksIter)
                    bbox_to_rect(boxElement.bbox(), '#ff0000')
                elif isinstance(measure[i], note.Rest):
                    duration = measure[i].quarterLength
                    boxElement = next(svgRestsIter)
                    if measure[i].duration.quarterLength in (3.0, 1.5, 0.75):  # all notes with a dot
                        boxElement += next(svgNoteDotsIter)
                    bbox_to_rect(boxElement.bbox(), '#00f0f0')
            mIndex += 1

import sys
from music21 import *
from svgelements import *

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

add_pixels = 20
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

keys_alter = {1: ['F'],
              2: ['F', 'C'],
              3: ['F', 'C', 'G'],
              4: ['F', 'C', 'G', 'D'],
              5: ['F', 'C', 'G', 'D', 'A'],
              6: ['F', 'C', 'G', 'D', 'A', 'E'],
              7: ['F', 'C', 'G', 'D', 'A', 'E', 'B'],
              -1: ['B'],
              -2: ['B', 'E'],
              -3: ['B', 'E', 'A'],
              -4: ['B', 'E', 'A', 'D'],
              -5: ['B', 'E', 'A', 'D', 'G'],
              -6: ['B', 'E', 'A', 'D', 'G', 'C'],
              -7: ['B', 'E', 'A', 'D', 'G', 'C', 'F']}


class StaffSystem:
    def __init__(self, y):
        self.y = y
        self.notes = list()
        self.dots = list()
        self.stems = list()
        self.hooks = list()
        self.rests = list()
        self.clefs = list()
        self.timesigs = list()
        self.keysigs = list()
        self.accidentals = list()


def bbox_to_rect(bbox, color):
    x = bbox[0]
    y = bbox[1]
    w = bbox[2] - x
    h = bbox[3] - y
    box = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" style="stroke: {color}; fill: none"/>'
    # print(box)
    return f'{box}\n'


def bbox_to_dict(bbox):
    d = dict()
    d['x'] = bbox[0]
    d['y'] = bbox[1]
    d['w'] = bbox[2] - bbox[0]
    d['h'] = bbox[3] - bbox[1]
    return d


def bbox_to_pascal_voc(bbox, classification):
    return f'{classification} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}'


def bbox_to_choice(bbox, classification):
    toText = True
    if toText:
        return f'{bbox_to_pascal_voc(bbox, classification)}\n'
    else:
        if classification in (Score.fclef_id, Score.gclef_id, Score.cclef_id):
            return bbox_to_rect(bbox, '#1FDEDE')
        elif classification == Score.barline_id:
            return bbox_to_rect(bbox, '#F2F600')
        elif classification == Score.notes_id:
            return bbox_to_rect(bbox, '#DE1F1F')
        elif classification == Score.rests_id:
            return bbox_to_rect(bbox, '#8AFF00')
        elif classification in (Score.sharp_id, Score.flat_id, Score.natural_id):
            return bbox_to_rect(bbox, '#FFA200')
        elif classification == Score.timesig_id:
            return bbox_to_rect(bbox, '#005DFF')


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


def beam_category(beams):
    beam_type = None
    for beam in beams:
        if beam.type == 'start' and beam_type is None:
            beam_type = beam.type
        elif beam.type == 'continue' and beam_type in (None, 'start', 'stop'):
            beam_type = beam.type
        elif beam.type == 'stop' and beam_type is None:
            beam_type = beam.type
        elif beam.type == 'start' and beam_type == 'stop':
            beam_type = 'continue'
        elif beam.type == 'stop' and beam_type == 'start':
            beam_type = 'continue'
    return beam_type


def prepare_barline(barline):
    stroke_width = barline.values.get('stroke-width')
    barline_bbox = barline.bbox()
    stroke_half_width = float(stroke_width) / 2
    barline += SimpleLine(barline_bbox[0], barline_bbox[1], barline_bbox[0] - stroke_half_width, barline_bbox[1])
    barline += SimpleLine(barline_bbox[2], barline_bbox[3], barline_bbox[2] + stroke_half_width, barline_bbox[3])
    return barline


def determine_clef(clef):
    # print(clef.name)
    if clef.name == 'treble':
        return Score.gclef_id
    elif clef.name == 'bass':
        return Score.fclef_id
    elif clef.name == 'alto':
        return Score.cclef_id


class Score:
    sharp_id = 0
    flat_id = 1
    natural_id = 2
    gclef_id = 3
    fclef_id = 4
    cclef_id = 5
    barline_id = 6
    timesig_id = 7
    notes_id = 8
    rests_id = 9

    def __init__(self):
        self.svgAccidentals = list()
        self.svgKeysigs = list()
        self.svgClefs = list()
        self.svgRests = list()
        self.svgTimesigs = list()
        self.svgBarlines = list()
        self.svgNotes = list()
        self.svgStems = list()
        self.svgHooks = list()
        self.svgNoteDots = list()

        self.svgAccidentalsIter = None
        self.svgKeysigsIter = None
        self.svgClefsIter = None
        self.svgRestsIter = None
        self.svgTimesigsIter = None
        self.svgNotesIter = None
        self.svgStemsIter = None
        self.svgHooksIter = None
        self.svgNoteDotsIter = None

        self.lastClef = None
        self.lastKeySign = None
        self.lastTimeSign = None
        self.lastNote = None
        self.currentClef = clefLineLoc['treble']

        self.coords_and_classes = ''

    def classify(self, svg_file, musicxml_file):
        svg = SVG.parse(svg_file)
        linesIndex = 0
        staffLines = None
        systems = list()

        # create staff systems
        for element in svg.elements():
            classType = element.values.get('class')
            if classType == 'StaffLines':
                if linesIndex == 0:
                    staffLines = element
                    linesIndex += 1
                elif linesIndex == 4:
                    staffLines += element
                    linesIndex = 0
                    systems.append(
                        StaffSystem((staffLines.bbox()[3] - staffLines.bbox()[1]) / 2 + staffLines.bbox()[1]))
                else:
                    staffLines += element
                    linesIndex += 1
        # print(f'Systems: {len(systems)}')

        # classify elements in svg
        for element in svg.elements():
            classType = element.values.get('class')
            if classType == 'Note':
                systems[get_staff_system_index(element, systems)].notes.append(element)
            elif classType == 'Rest':
                systems[get_staff_system_index(element, systems)].rests.append(element)
            elif classType == 'TimeSig':
                systems[get_staff_system_index(element, systems)].timesigs.append(element)
            elif classType == 'KeySig':
                systems[get_staff_system_index(element, systems)].keysigs.append(element)
            elif classType == 'Clef':
                systems[get_staff_system_index(element, systems)].clefs.append(element)
            elif classType == 'BarLine':
                if element.values.get('stroke-width') is not None:
                    self.svgBarlines.append(element)
            elif classType == 'Accidental':
                systems[get_staff_system_index(element, systems)].accidentals.append(element)
            elif classType == 'Stem':
                systems[get_staff_system_index(element, systems)].stems.append(element)
            elif classType == 'Hook':
                systems[get_staff_system_index(element, systems)].hooks.append(element)
            elif classType == 'NoteDot':
                systems[get_staff_system_index(element, systems)].dots.append(element)

        # sort elements where sorting is required
        for system in systems:
            self.svgNotes.extend(sorted(system.notes, key=sort_after_x))
            self.svgNoteDots.extend(sorted(system.dots, key=sort_after_x))
            self.svgStems.extend(sorted(system.stems, key=sort_after_x))
            self.svgHooks.extend(sorted(system.hooks, key=sort_after_x))
            self.svgRests.extend(sorted(system.rests, key=sort_after_x))
            self.svgClefs.extend(sorted(system.clefs, key=sort_after_x))
            self.svgTimesigs.extend(sorted(system.timesigs, key=sort_after_x))
            self.svgKeysigs.extend(sorted(system.keysigs, key=sort_after_x))
            self.svgAccidentals.extend(sorted(system.accidentals, key=sort_after_x))

        self.svgAccidentalsIter = iter(self.svgAccidentals)
        self.svgKeysigsIter = iter(self.svgKeysigs)
        self.svgClefsIter = iter(self.svgClefs)
        self.svgRestsIter = iter(self.svgRests)
        self.svgTimesigsIter = iter(self.svgTimesigs)
        self.svgNotesIter = iter(self.svgNotes)
        self.svgStemsIter = iter(self.svgStems)
        self.svgHooksIter = iter(self.svgHooks)
        self.svgNoteDotsIter = iter(self.svgNoteDots)

        # print(f'Timesigs: {len(self.svgTimesigs)}')
        score = converter.parse(musicxml_file)

        for barline in self.svgBarlines:
            self.coords_and_classes += bbox_to_choice(prepare_barline(barline).bbox(), Score.barline_id)

        for part in score.getElementsByClass(stream.Part):
            mIndex = 0
            for measure in part.getElementsByClass(stream.Measure):
                attributes = list()
                for j in range(len(measure)):
                    if isinstance(measure[j], key.KeySignature) or \
                            isinstance(measure[j], meter.TimeSignature) or isinstance(measure[j], clef.Clef) or \
                            isinstance(measure[j], layout.SystemLayout):
                        attributes.append(measure[j])
                    elif isinstance(measure[j], note.Note) or isinstance(measure[j], note.Rest):
                        break
                if len(attributes) >= 1 and isinstance(attributes[0], layout.SystemLayout):
                    if len(attributes) >= 2 and isinstance(attributes[1], clef.Clef):
                        self.set_clef(attributes[1])
                        self.add_clef()
                        if len(attributes) >= 3 and isinstance(attributes[2], key.KeySignature):
                            self.set_keysign(attributes[2])
                            self.add_keysign()
                            if len(attributes) >= 4 and isinstance(attributes[3], meter.TimeSignature):
                                self.set_timesign(attributes[3])
                                self.add_timesign()
                        elif len(attributes) >= 3 and isinstance(attributes[2], meter.TimeSignature):
                            self.set_timesign(attributes[2])
                            self.add_timesign()

                            self.add_keysign()
                        else:
                            self.add_keysign()
                    elif len(attributes) >= 2 and isinstance(attributes[1], key.KeySignature):
                        self.set_keysign(attributes[1])
                        self.add_keysign()

                        self.add_clef()
                        if len(attributes) >= 2 and isinstance(attributes[1], meter.TimeSignature):
                            self.set_timesign(attributes[1])
                            self.add_timesign()
                    elif len(attributes) >= 2 and isinstance(attributes[1], meter.TimeSignature):
                        self.set_timesign(attributes[1])
                        self.add_timesign()

                        self.add_clef()
                        self.add_keysign()
                    else:
                        self.add_clef()
                        self.add_keysign()
                # use other solution till classification for barlines is required
                # bbox_to_rect(prepare_barline(next(svgBarlinesIter)).bbox(), '#fca103')
                for i in range(0, len(measure)):
                    # check for clefs and signatures apart from line start
                    if len(attributes) > 1 and not (isinstance(attributes[0], layout.SystemLayout) or not (
                            isinstance(measure[i], meter.TimeSignature) or
                            isinstance(measure[i], key.KeySignature) or
                            isinstance(measure[i], clef.Clef))):
                        if isinstance(measure[i], meter.TimeSignature):
                            self.set_timesign(measure[i])
                        elif isinstance(measure[i], key.KeySignature):
                            self.set_keysign(measure[i])
                        elif isinstance(measure[i], clef.Clef):
                            self.set_clef(measure[i])
                    elif isinstance(measure[i], note.Note):
                        boxElement = next(self.svgNotesIter)
                        self.coords_and_classes += bbox_to_choice(boxElement.bbox(), Score.notes_id)
                    elif isinstance(measure[i], note.Rest):
                        boxElement = next(self.svgRestsIter)
                        self.coords_and_classes += bbox_to_choice(boxElement.bbox(), Score.rests_id)
                mIndex += 1
        return self.coords_and_classes

    def add_clef(self):
        path = next(self.svgClefsIter)
        self.coords_and_classes += bbox_to_choice(path.bbox(), determine_clef(self.lastClef))

    def add_timesign(self):
        # print('timesign')
        if self.lastTimeSign.symbol == 'common':
            boxElement = next(self.svgTimesigsIter)
        else:
            boxElement = next(self.svgTimesigsIter) + next(self.svgTimesigsIter)
        self.coords_and_classes += bbox_to_choice(boxElement.bbox(), Score.timesig_id)
        # numerator = next(svg_timesigs_iter)
        # bbox_to_rect(numerator.bbox(), '#FAFC53')
        # denominator = next(svg_timesigs_iter)
        # bbox_to_rect(denominator.bbox(), '#FAFC53')

    def add_keysign(self):
        sharps = self.lastKeySign.sharps
        if sharps > 0:
            for x in range(0, sharps):
                path = next(self.svgKeysigsIter)
                self.coords_and_classes += bbox_to_choice(path.bbox(), Score.sharp_id)
        elif sharps < 0:
            for x in range(sharps, 0):
                path = next(self.svgKeysigsIter)
                self.coords_and_classes += bbox_to_choice(path.bbox(), Score.flat_id)

    def set_clef(self, new_clef):
        old_last_clef = self.lastClef
        self.lastClef = new_clef
        if old_last_clef is not None:
            self.add_clef()

    def set_keysign(self, new_keysign):
        old_last_keysign = self.lastKeySign
        self.lastKeySign = new_keysign
        if old_last_keysign is not None:
            self.add_keysign()

    def set_timesign(self, new_timesign):
        old_last_timesign = self.lastTimeSign
        self.lastTimeSign = new_timesign
        if old_last_timesign is not None:
            self.add_timesign()


if __name__ == '__main__':
    score = Score()
    print(score.classify('out_dev/569-1.svg', 'out_dev/569.musicxml'))

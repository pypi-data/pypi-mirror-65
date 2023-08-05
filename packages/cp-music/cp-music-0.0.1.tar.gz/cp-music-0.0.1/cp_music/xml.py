import xml.etree.ElementTree as ET
from cp_music import note


class MusicXml:

    def __init__(self, file):
        self._file = file
        self._tree = ET.parse(self._file)
        self._root = self._tree.getroot()
        self._stream = note.NoteStream()

    def parse(self):
        part = self._root.findall('./part')[0]

        for measure in part:
            for elem in measure:

                if elem.tag == 'note':
                    n = note.Note()

                    for note_child in elem:
                        if note_child.tag == 'duration':
                            n.duration = int(note_child.text)
                        if note_child.tag == 'voice':
                            n.voice = int(note_child.text)
                        if note_child.tag == 'type':
                            n.type = note_child.text
                        if note_child.tag == 'chord':
                            n.is_chord = True

                        if note_child.tag == 'pitch':
                            for pitch_child in note_child:
                                if pitch_child.tag == 'step':
                                    n.pitch.step = pitch_child.text
                                if pitch_child.tag == 'alter':
                                    n.pitch.alter = float(pitch_child.text)
                                if pitch_child.tag == 'octave':
                                    n.pitch.octave = int(pitch_child.text)

                    self.stream.add(n)

    def write_from_stream(self):
        i = 0
        part = self._root.findall('./part')[0]

        for measure in part:
            for elem in measure:
                if elem.tag == 'note':
                    n = self.stream.get(i)
                    for note_child in elem:
                        if note_child.tag == 'pitch':
                            for pitch_child in note_child:
                                if pitch_child.tag == 'step':
                                    pitch_child.text = n.pitch.step
                                if pitch_child.tag == 'alter':
                                    pitch_child.text = str(n.pitch.alter)
                                if pitch_child.tag == 'octave':
                                    pitch_child.text = str(n.pitch.octave)
                    i += 1

        self._tree.write(self._file)

    @property
    def stream(self):
        return self._stream

PITCH_CLASS = {
    'C': 0,
    'D': 2,
    'E': 4,
    'F': 5,
    'G': 7,
    'A': 9,
    'B': 11
}

STEP = {
    0: 'C',
    2: 'D',
    4: 'E',
    5: 'F',
    7: 'G',
    9: 'A',
    11: 'B'
}


class Note:

    def __init__(self):
        self._pitch = Pitch()
        self._duration = None
        self._voice = None
        self._type = None
        self._chord = False

    def __repr__(self):
        return '<Note duration=%s, voice=%s, type=%s, chord=%s>' % \
               (self.duration, self.voice, self.type, self.is_chord)

    @property
    def pitch(self):
        return self._pitch

    @property
    def is_rest(self):
        return self.pitch.step is None

    @property
    def duration(self):
        return self._duration

    @property
    def voice(self):
        return self._voice

    @property
    def type(self):
        return self._type

    @property
    def is_chord(self):
        return self._chord

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    @voice.setter
    def voice(self, voice):
        self._voice = voice

    @type.setter
    def type(self, type):
        self._type = type

    @is_chord.setter
    def is_chord(self, chord):
        self._chord = chord


class Pitch:
    def __init__(self):
        self._midicent = None
        self._step = None
        self._alter = None
        self._octave = None

    def __repr__(self):
        return '<Pitch step=%s, alter=%s, octave=%s>' % \
               (self.step, self.alter, self.octave)

    @property
    def step(self):
        return self._step

    @property
    def alter(self):
        return self._alter

    @property
    def octave(self):
        return self._octave

    @property
    def midicent(self):
        alter = 0

        if self.step:
            pitch_class = PITCH_CLASS[self.step]
            if self.alter:
                alter = self.alter
            return (((self.octave + 1) * 12) + pitch_class + alter) * 100
        else:
            return 0

    @step.setter
    def step(self, step):
        self._step = step

    @alter.setter
    def alter(self, alter):
        self._alter = alter

    @octave.setter
    def octave(self, octave):
        self._octave = octave

    @midicent.setter
    def midicent(self, midicent):
        self.step = self.__to_step(midicent / 100)
        self.alter = self.__to_alter(midicent / 100)
        self.octave = self.__to_octave(midicent / 100)

        self._midicent = midicent

    @classmethod
    def __to_octave(cls, midi):
        return int(((midi - (midi % 12)) / 12) - 1)

    @classmethod
    def __to_step(cls, midi):
        pitch_class = midi % 12
        while pitch_class >= 0:
            if pitch_class in STEP:
                return STEP[pitch_class]
            else:
                pitch_class -= 0.5

    @classmethod
    def __to_alter(cls, midi):
        alter = 0
        pitch_class = midi % 12

        while pitch_class >= 0:
            if pitch_class in STEP:
                return alter
            else:
                pitch_class -= 0.5
                alter += 0.5


class NoteStream:

    def __init__(self):
        self._notes = []
        self._index = 0
        self._count = -1

    def __iter__(self):
        return self

    def __next__(self):
        self._count += 1

        if self._count < len(self._notes):
            return self._notes[self._count]

        raise StopIteration

    def __repr__(self):
        return '<Stream %s> ' % self._notes

    def add(self, note):
        if isinstance(note, Note):
            self._notes.append(note)
        else:
            raise ValueError('Element must be a Note object')

    def remove(self, note):
        if isinstance(note, Note):
            self._notes.remove(note)
        else:
            raise ValueError('Element must be a Note object')

    def get(self, i):
        return self._notes[i]

    def to_matrix(self):
        matrix = []
        tmp = []
        voice = self._notes[0].voice

        for note in self._notes:

            if note.voice != voice:
                matrix.append(tmp)
                tmp = []

            midicent = note.pitch.midicent
            tmp.append(midicent)

            for i in range(note.duration - 1):
                tmp.append(0)

            voice = note.voice

        matrix.append(tmp)
        return matrix

    def update(self, matrix):
        i = 0

        for midicents in matrix:
            for midicent in midicents:
                if midicent != 0:
                    self._notes[i].pitch.midicent = midicent
                    i += 1
import unittest
from cp_music import cpm_model, note, utils
from cp_music.xml import MusicXml


class CpMusicModelTest(unittest.TestCase):

    def testGetSolution_arithmetic(self):
        m1 = [[6200, 6400, 0, 0]]
        m2 = [[6200, 6300, 0, 0]]

        model = cpm_model.CpMusicModel()
        model.createIntVarsFromMatrix(m1)

        for vars in model.vars:
            for var in vars:
                model.Add(var < 6400)

        self.assertEqual(m2, model.getSolution())

    def testGetSolution_allDifferent(self):
        m1 = [[6000, 6200, 6200, 0]]
        m2 = [[6000, 6200, 6300, 0]]

        model = cpm_model.CpMusicModel()
        model.createIntVarsFromMatrix(m1)
        model.AddAllDifferent(model.vars[0])

        self.assertEqual(m2, model.getSolution())


class NoteStreamTest(unittest.TestCase):

    def testNote_fromMidicent(self):
        n = note.Note()

        n.type = 'quarter'
        n.voice = 1
        n.duration = 2
        n.pitch.midicent = 6100

        self.assertEqual(n.pitch.step, 'C')
        self.assertEqual(n.pitch.alter, 1.0)
        self.assertEqual(n.pitch.octave, 4)
        self.assertEqual(n.type, 'quarter')
        self.assertEqual(n.voice, 1)
        self.assertEqual(n.duration, 2)
        self.assertEqual(n.is_rest, False)

    def testNote_Xml(self):
        n = note.Note()

        n.type = 'quarter'
        n.voice = 1
        n.duration = 2
        n.pitch.alter = 1.0
        n.pitch.octave = 4
        n.pitch.step = 'C'

        self.assertEqual(n.type, 'quarter')
        self.assertEqual(n.voice, 1)
        self.assertEqual(n.duration, 2)
        self.assertEqual(n.is_rest, False)
        self.assertEqual(n.pitch.midicent, 6100)


class MusicXmlTest(unittest.TestCase):

    def testParse(self):
        path = 'tests/test.musicxml'

        music_xml = MusicXml(path)
        music_xml.parse()

        for n in music_xml.stream:
            self.assertEqual(n.type, 'quarter')
            self.assertEqual(n.voice, 1)
            self.assertEqual(n.duration, 2)
            self.assertEqual(n.is_rest, False)
            self.assertEqual(n.is_chord, False)
            self.assertEqual(n.pitch.step, 'C')
            self.assertEqual(n.pitch.alter, 1.0)
            self.assertEqual(n.pitch.octave, 4)

        music_xml.write_from_stream()


class UtilsTest(unittest.TestCase):

    def testFreqToMidicent(self):
        f = [220, 440, 880]

        utils.freqToMidicent(f)

        self.assertEqual(f[0], 5700)
        self.assertEqual(f[1], 6900)
        self.assertEqual(f[2], 8100)

    def testRound_semitone(self):
        m = [6046, 6078]

        utils.round(m)

        self.assertEqual(m[0], 6000)
        self.assertEqual(m[1], 6100)

    def testRound_quarterTone(self):
        m = [6020, 6780, 6270]

        utils.round(m, acc=50)

        self.assertEqual(m[0], 6000)
        self.assertEqual(m[1], 6800)
        self.assertEqual(m[2], 6250)


if __name__ == '__main__':
    unittest.main()

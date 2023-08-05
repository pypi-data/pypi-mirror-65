from cp_music import cpm_model, xml
from itertools import product


if __name__ == '__main__':

    # list of midicent values
    midicents = [
        0, 1700, 2900, 3800, 4500, 5100, 5600, 6000,
        6400, 6700, 7000, 7300, 7600, 7800, 8100, 8300,
        8500, 8700, 8900, 9000, 9200, 9400, 9500, 9700,
        9800, 9900, 10100, 10200, 10300, 10400, 10500
    ]

    # read .musicxml file
    music_xml = xml.MusicXml('example1.musicxml')

    # parse .musicxml file
    music_xml.parse()

    # convert .musicxml file to stream and then to matrix
    matrix = music_xml.stream.to_matrix()

    # initialize new model
    model = cpm_model.CpMusicModel()

    # create IntVars from matrix
    model.createIntVarsFromMatrix(matrix)

    # create allowed assignments from midicent values
    assignments = product(midicents, repeat=len(matrix[0]))

    # add constraints
    for vars in model.vars:
        model.AddAllowedAssignments(vars, assignments)

    # get new solution matrix
    matrix = model.getSolution()

    # update stream with solution matrix
    music_xml.stream.update(matrix)

    # write contents of stream to .musicxml file
    music_xml.write_from_stream()

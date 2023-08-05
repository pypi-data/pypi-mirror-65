from ortools.sat.python import cp_model
import math


class CpMusicModel(cp_model.CpModel):

    def __init__(self):
        cp_model.CpModel.__init__(self)
        self.__solver = cp_model.CpSolver()
        self.__vars = None
        self.__matrix = None

    def createIntVarsFromMatrix(self, matrix, tone=100, inter=3):
        vars = []

        for i in matrix:
            t = []
            for j in i:
                x = self.NewIntVarFromDomain(
                    self.__domain_from_midicent(j, tone=tone, i=inter), '')
                t.append(x)
            vars.append(t)

        self.__matrix = matrix
        self.__vars = vars

    @classmethod
    def __domain_from_midicent(cls, m, tone=100,  i=3):
        d = []

        if m == 0:
            d = [0]
        else:
            m1 = m
            m2 = m
            while m < (m2 + i*tone):
                d[:0] = [m1]
                d += [m]

                m1 -= tone
                m += tone
        return cp_model.Domain.FromValues(tuple(d))

    @classmethod
    def __euclidean_distance(cls, x, y):
        dist = 0
        for i in range(len(x)):
            for j in range(len(x[0])):
                dist += math.pow(x[i][j] - y[i][j], 2)

        return math.sqrt(dist)

    def getSolution(self):
        d = []

        callback = SolutionCallback(self.__vars)
        self.__solver.SearchForAllSolutions(self, callback)

        for solution in callback.solutions:
            dist = self.__euclidean_distance(self.__matrix, solution)
            d.append(dist)

        index = d.index(min(d))

        return callback.solutions[index]

    @property
    def vars(self):
        return self.__vars


class SolutionCallback(cp_model.CpSolverSolutionCallback):
    def __init__(self, vars):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__solutions = []
        self.__vars = vars

    def on_solution_callback(self):
        s = []
        for i in self.__vars:
            t = [self.Value(j) for j in i]
            s.append(t)

        self.__solutions.append(s)

    @property
    def solutions(self):
        return self.__solutions
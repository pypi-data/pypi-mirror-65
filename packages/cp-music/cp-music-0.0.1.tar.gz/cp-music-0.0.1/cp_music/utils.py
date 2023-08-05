import math


def freqToMidicent(f):
    for i in range(len(f)):
        if f[i] != 0:
            f[i] = ((12 * math.log2(f[i] / 440)) + 69) * 100
        else:
            f[i] = 0

    return f


def transpose(m, i):
    for j in range(len(m)):
        if m[j] != 0:
            m[j] += i


def round(m, acc=100):
    for i in range(len(m)):
        a = m[i] % 100
        t = m[i] - a

        if acc == 100:
            if 0 <= a < 50:
                m[i] = t
            if 50 <= a <= 100:
                m[i] = t + 100
        elif acc == 50:
            if 0 <= a < 25:
                m[i] = t
            if 25 <= a < 75:
                m[i] = t + 50
            if 75 <= a <= 100:
                m[i] = t + 100
        else:
            raise ValueError('acc must be either 50 or 100 midicents')

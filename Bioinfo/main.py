import numpy as np
import sys

def readFASTA(filename):
    fullString = ''
    with open(filename) as file:
        lines = file.readlines()
        for i in range(1, len(lines)):
            tempLine = ''.join(lines[i].split())
            fullString += tempLine
    return fullString

def readBLOSUM(filename):
    outerDict = {}
    with open(filename) as f:
        lines = f.readlines()
        acids = lines[0].split()
        for i in range(1, len(lines)):
            splitLine = lines[i].split()
            dict = {}
            for j in range(1, len(splitLine)):
                dict[acids[j-1]] = int(splitLine[j])
            outerDict[splitLine[0]] = dict
    return outerDict

def makeMatrix(blosum, v, w, penalty, penalty_ext):
    qryMatrix = np.zeros(shape=(len(v), len(w)))
    sbjMatrix = np.zeros(shape=(len(v), len(w)))
    scoreMatrix = np.zeros(shape=(len(v)+1, len(w)+1))
    backtrack = np.zeros(shape=(len(v), len(w)))

    for i in range(1, len(v)):
        for j in range(1, len(w)):

            qryMatrix[i][j] = max(0, scoreMatrix[i-1][j] - penalty, qryMatrix[i-1][j] - penalty_ext)

            sbjMatrix[i][j] = max(0, scoreMatrix[i][j-1] - penalty, sbjMatrix[i][j-1] - penalty_ext)

            diagonal = scoreMatrix[i - 1][j - 1] + blosum[v[i]][w[j]]
            delete = qryMatrix[i - 1][j - 1] + blosum[v[i]][w[j]]
            insert = sbjMatrix[i - 1][j - 1] + blosum[v[i]][w[j]]

            scoreMatrix[i][j] = max(diagonal, 0, insert, delete)

            if scoreMatrix[i][j] == diagonal:
                backtrack[i][j] = 2
            elif scoreMatrix[i][j] == insert:
                backtrack[i][j] = 1
            elif scoreMatrix[i][j] == delete:
                backtrack[i][j] = 0
            elif scoreMatrix[i][j] == 0:
                backtrack[i][j] = 3

    return scoreMatrix, backtrack

def OutputLCS(backtrack, v, w, i, j, v_, w_):
    if i == 0 or j == 0 or backtrack[i-1][j-1] == 3:
        return v_, w_
    if backtrack[i][j] == 0:
        return OutputLCS(backtrack, v, w, i - 1, j, v[i-1]+v_, '-'+w_)
    elif backtrack[i][j] == 1:
        return OutputLCS(backtrack, v, w, i, j - 1, '-'+v_, w[j-1]+w_)
    else:
        return OutputLCS(backtrack, v, w, i - 1, j - 1, v[i-1]+v_, w[j-1]+w_)

if __name__ == "__main__":
    penalty_ext = 1
    penalty = 11
    try:
        penalty = int(sys.argv[1])
        penalty_ext = float(sys.argv[2])
    except IndexError:
        print('Use case of the program is \"python3 main.py penalty penalty_ext\"')
    v = readFASTA('human')
    w = readFASTA('yeast')

    #v = 'ATTCGTA'
    #w = 'ATGCTA'
    blosum = readBLOSUM('BLOSUM62.txt')
    scoreMatrix, backtrack = makeMatrix(blosum, v, w, penalty, 1)
    score = np.amax(scoreMatrix)
    max_indexes = np.unravel_index(np.argmax(scoreMatrix), scoreMatrix.shape)
    v_, w_ = OutputLCS(backtrack, v, w, max_indexes[0] + 1, max_indexes[1] + 1, '', '')
    width = 80
    loops = int(len(v_)/width)
    print(score)
    for i in range(loops):
        q = 'Query: '
        s = 'Sbjct: '
        m = 'Match: '
        for j in range(width):
            q += v_[(i*width)+j]
        for j in range(width):
            if v_[(i*width)+j] == w_[(i*width)+j]:
                m += v_[(i*width)+j]
            elif v_[(i*width)+j] == '-' or w_[(i*width)+j] == '-':
                m += ' '
            elif blosum[v_[(i*width)+j]][w_[(i*width)+j]] > 0:
                m += '+'
            else:
                m += " "
        for j in range(width):
            s += w_[(i*width)+j]
        print(q)
        print(m)
        print(s)
        print()
    q = 'Query: '
    s = 'Sbjct: '
    m = 'Match: '

    for j in range((loops*width), len(v_)):
        q += v_[j]
    for j in range((loops*width), len(v_)):
        if v_[j] == w_[j]:
            m += v_[j]
        elif v_[j] == '-' or w_[j] == '-':
            m += ' '
        elif blosum[v_[j]][w_[j]] > 0:
            m += '+'
        else:
            m += " "
    for j in range((loops*width), len(v_)):
        s += w_[j]
    print(q)
    print(m)
    print(s)
    print()





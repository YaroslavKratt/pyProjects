import copy
import numpy as np


def main():
    epselon = 0.0000001
    matrix = [[7.03, 1.22, 0.85, 1.135, -0.81],
              [-1.85, -12.63, 2.31, 6.99, -0.677],
              [0.2, 1.23, -6.977, 3.9, -0.033],
              [16.825, -14.6, -7.104, 77.33, 0],
              [-0.055, -1.39, -2.867, 0.67, 13]]

    rightCol = [2.1,
                0.06,
                -4.05,
                -5.68,
                -13.43]
    vector = [0.1,
              0.1,
              0.1,
              0.1,
              0.1]
    print("Матриця приведена до матриці з діагональною перевагою A = ")
    print(np.matrix(matrix))
    print("\n Початковий вектор = ")
    print(np.matrix(rightCol))
    print("\n Ітерації:")
    res = runZeidelIteration(copy.deepcopy(matrix), copy.deepcopy(rightCol), copy.deepcopy(vector), epselon)
    print("\nПеревірка: b - Ax = %s" % matrixSubtract(rightCol, matrixMultiply(matrix, res)))


def runZeidelIteration(matrix, rightCol, vector, epselon):
    preparedSystem = makeSystemForIteration(matrix, rightCol)
    readyMatrix = preparedSystem[0]
    readyCol = preparedSystem[1]
    i = 0
    while True:
        vectorNew = iteration(readyMatrix, readyCol, vector)
        i += 1
        if i <= 5:
            print(str(i) + "\t" + str(['%.2f' % elem for elem in vector]) + "\t" + str(
                round(findDelta(vector, vectorNew), 5)))
        if findDelta(vector, vectorNew) < epselon:
            break
        vector = vectorNew
    print(str(i) + "\t" + str(['%.17f' % elem for elem in vector]))
    return vector


def findDelta(vector1, vector2):
    result = 0
    for i in range(len(vector1)):
        if result < abs(vector1[i] - vector2[i]):
            result = abs(vector1[i] - vector2[i])
    return result


def iteration(matrix, rightCol, inputVector):
    result = [0 for elem in inputVector]
    for i in range(len(rightCol)):
        result[i] = rightCol[i]
        for j in range(len(rightCol)):
            result[i] += matrix[i][j] * inputVector[j] if i <= j else matrix[i][j] * result[j]
    return result


def multiply(A, B):
    rows_A = len(A)
    cols_A = len(A[0]) if type(A[0]) is list else 1
    rows_B = len(B)
    cols_B = len(B[0]) if type(B[0]) is list else 1

    if cols_A != rows_B:
        print("Різні розмірності матриць")
        return
    C = [[0 for row in range(cols_B)] for col in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C


def multiplyCol(A, B):
    rows_A = len(A)
    cols_A = len(A[0]) if type(A[0]) is list else 1
    rows_B = len(B)
    cols_B = len(B[0]) if type(B[0]) is list else 1

    if cols_A != rows_B:
        print("Різні розмірності матриць")
        return
    C = [0 for row in range(len(B))]
    for i in range(rows_A):
        for j in range(rows_B):
            C[i] += A[i][j] * B[j]
    return C


def makeSystemForIteration(matrix, rightCol):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i != j:
                matrix[i][j] /= -matrix[i][i]
        rightCol[i] /= matrix[i][i]
        matrix[i][i] = 0

    return [matrix, rightCol]


def matrixMultiply(mat1, mat2):
    result = []
    for i in range(0, len(mat1)):
        summ = 0
        for j in range(0, len(mat2)):
            summ += mat1[i][j] * mat2[j]
        result.append(summ)
    return result


def matrixSubtract(mat1, mat2):
    result = []
    for i in range(0, len(mat1)):
        result.append(mat1[i] - mat2[i])
    return result


main()

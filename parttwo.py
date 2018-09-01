import sys
from rowreduce import pretty_print

def gauss_jordan(aug, m, n):
    eps = 0.000001
    steps = []
    for i in range(m):
        pivot = i
        for j in range(i, m):
            pivot = j
            if abs(aug[j][i]) > eps:
                break
        if pivot != i:
            steps.append('SWITCH '+ str(i + 1) + ' ' + str(pivot + 1))
            for j in range(n):
                aug[i][j], aug[pivot][j] = aug[pivot][j], aug[i][j]
        # ok now we process
        piv_val = aug[i][i]
        if abs(piv_val) < eps:
            continue
        if piv_val != 1:
            steps.append('MULTIPLY '+ str(1.0/piv_val) + ' ' + str(i + 1))
        for j in range(n):
            aug[i][j] = aug[i][j] / piv_val

        for j in range(m):
            if j == i:
                continue
            ratio = aug[j][i]
            if ratio != 0:
                if ratio - int(ratio) < eps:
                    steps.append('MULTIPLY&ADD ' + str(int(ratio))+ ' ' + str(i+1)+ ' ' + str(j+1))
                else:
                    steps.append('MULTIPLY&ADD '+ str(ratio)+ ' ' + str(i + 1)+ ' ' + str(j + 1))
            for k in range(n):
                aug[j][k] = aug[j][k] - ratio * aug[i][k]
    ac_rc_zero = False
    for i in range(m):
        rc_zero = True
        for j in range(m, n):
            if aug[i][j] > eps:
                rc_zero = False
            aug[i][j] = round(aug[i][j] * 100, 2) / 100
        if rc_zero == True:
            ac_rc_zero = True

    rc_zero = False
    for i in range(m, n):
        rc_zero = True
        for j in range(m):
            if aug[j][i] > eps:
                rc_zero = False
                break
        if rc_zero == True:
            break
    return aug, rc_zero or ac_rc_zero, steps




def matmult(a,b):
    zip_b = zip(*b)
    zip_b = list(zip_b)
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b))
             for col_b in zip_b] for row_a in a]


def get_aug(mat_a, mat_b, row):
    for i in range(len(mat_a)):
        mat_a.append(mat_b[row][i])
    return mat_a


if __name__ == '__main__':

    eps = 0.000001
    try:
        file = sys.argv[1]
    except IndexError:
        sys.exit(0)

    b = []
    A = []
    X = []
    cur_line = 0
    with open(file) as f:
        for line in f:
            if cur_line == 0:
                n = int(line)
                cur_line = cur_line + 1
            else:
                A.append(map(float, line.split()))
                cur_line = cur_line + 1
    X = matmult(A, A)
    aug = []
    for row in range(len(X)):
        aug.append(get_aug(X[row], A, row))
    A, notexists, steps = gauss_jordan(X, len(A), 2*len(A))
    print(A)
    if notexists:
        print "ALAS! DIDN'T FIND ONE!"
    else:
        print "YAAY! FOUND ONE!"
        for x in A:
            for y in range(len(A), 2*len(A)):
                print x[y],
            print
    for step in steps:
        print step


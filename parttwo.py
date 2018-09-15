import random
import sys
import time

import numpy


def write_list_to_file(f, l):
    for i in range(0, len(l)):
        f.write(l[i])
        if i != len(l) - 1:
            f.write('\n')


def gauss_jordan(aug, m, n):
    steps = []
    for i in range(m):
        pivot = i, i
        found_piv = False
        for j in range(i, m):
            pivot = j, i
            if abs(aug[j][i]) > eps:
                found_piv = True
                break
        if not found_piv:
            for j in range(i, n):
                pivot = i, j
                if abs(aug[i][j])> eps:
                    found_piv = True
                    break
        if not found_piv:
            continue
        if pivot[0] != i:
            steps.append('SWITCH '+ str(i + 1) + ' ' + str(pivot + 1))
            for j in range(n):
                aug[i][j], aug[pivot[0]][j] = aug[pivot[0]][j], aug[i][j]
        # ok now we process
        piv_val = aug[pivot[0]][pivot[0]]
        if abs(piv_val) < eps:
            continue
        if piv_val != 1:
            steps.append('MULTIPLY '+ str(round(1.0/piv_val, 4)) + ' ' + str(i + 1))
        for j in range(n):
            aug[i][j] = aug[i][j] / piv_val

        for j in range(m):
            if j == i:
                continue
            ratio = aug[j][i]
            if ratio != 0:
                steps.append('MULTIPLY&ADD '+ str(round(ratio, 4))+ ' ' + str(i + 1)+ ' ' + str(j + 1))
            for k in range(n):
                aug[j][k] = aug[j][k] - ratio * aug[i][k]
    ac_rc_zero = False
    for i in range(m):
        rc_zero = True
        for j in range(m, n):
            if aug[i][j] > eps:
                rc_zero = False
            aug[i][j] = round(aug[i][j] * 100, 2) / 100
        if rc_zero:
            ac_rc_zero = True

    rc_zero = False
    for i in range(m, n):
        rc_zero = True
        for j in range(m):
            if aug[j][i] > eps:
                rc_zero = False
                break
        if rc_zero:
            break
    return aug, rc_zero or ac_rc_zero, steps


def matmult(a,b):
    zip_b = list(zip(*b))
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b))
             for col_b in zip_b] for row_a in a]


def get_aug(mat_a, mat_b, row):
    for i in range(len(mat_a)):
        mat_a.append(mat_b[row][i])
    return mat_a


if __name__ == '__main__':
    eps = 1e-7
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
    #A = random_matrix = [[int(random.random()*100) for a in range(500)] for b in range(500)]
    store_A = A

    start_time = time.time()
    X = matmult(A, A)
    print(X)
    aug = []
    for row in range(len(X)):
        aug.append(get_aug(X[row], A, row))
    start_time = time.time()
    A, notexists, steps = gauss_jordan(X, len(A), 2*len(A))
    end_time = time.time()
    my_algo = end_time - start_time
    start_time = time.time()
    y = numpy.array([numpy.array(el) for el in store_A])
    inv_np = numpy.linalg.inv(y)
    end_time = time.time()
    np = end_time - start_time
    print my_algo, np
    ans_list = []
    if notexists:
        ans_list.append("ALAS! DIDN'T FIND ONE!")
    else:
        ans_list.append("YAAY! FOUND ONE!")
        for x in A:
            inv = ''
            for y in range(len(A), 2*len(A)):
                if abs(x[y] - int(x[y])) < eps:
                    inv += str(int(x[y])) + ' '
                else:
                    inv += str(x[y]) + ' '
            ans_list.append(inv.rstrip())
    ans_list += steps
    write_list_to_file(open('output_problem2.txt', 'w'), ans_list)

import sys


def gauss_jordan(aug, m, n):
    eps = sys.float_info.epsilon
    pivot_list = []
    for i in range(m):
        pivot = i
        found_piv = False
        for j in range(i, m):
            pivot = j, i
            if abs(aug[j][i]) > eps:
                found_piv = True
                pivot_list.append(pivot[1])
                break
        if not found_piv:
            for j in range(i, n):
                pivot = i, j
                if abs(aug[i][j])> eps:
                    found_piv = True
                    pivot_list.append(pivot[1])
                    break
        if not found_piv:
            continue
        if i == 2:
            print pivot
        print pivot
        if pivot[0] != i:
            for j in range(n):
                aug[i][j], aug[pivot[0]][j] = aug[pivot[0]][j], aug[i][j]
        # ok now we process
        piv_val = aug[pivot[0]][pivot[1]]
        if abs(piv_val) < eps:
            continue
        for j in range(n):
            aug[i][j] = aug[i][j] / piv_val
        for j in range(m):
            if j == i:
                continue
            #print j, i
            ratio = aug[j][pivot[1]]
            print ratio
            for k in range(n):
                aug[j][k] = aug[j][k] - ratio * aug[i][k]
        pretty_print(aug)
    free_var = list(set(range(n - 1)) - set(pivot_list))
    free_var.sort()
    for i in range(m):
        aug[i][n - 1] = round(aug[i][n - 1] * 1000) / 1000
    return aug, pivot_list, free_var


def get_aug(mat_a, mat_b, count):
    #print(mat_a)
    mat_a.append(mat_b[count - 1])
    return mat_a


def pretty_print(mat):
    print 'Start'
    for x in mat:
        print x


def count_nonzero(arr):
    ans = 0
    for i in range(len(arr) - 1):
        if abs(arr[i]) > eps:
            ans = ans + 1
    return ans


def solve_gj_one(A, b, X):
    cur_line = 0
    with open(file) as f:
        for line in f:
            if cur_line == 0:
                b = map(float, line.split())
                cur_line = cur_line + 1
            elif cur_line <= len(b):
                augmented = get_aug(map(float, line.split()), b, cur_line)
                A.append(augmented)
                cur_line = cur_line + 1
            else:
                X = map(float, line.split())
    ans_gauss, pivots, free = gauss_jordan(A, 4, 5)
    zero = 0
    #pretty_print(ans_gauss)
    for i in range(4):
        if count_nonzero(ans_gauss[i]) == 0 and abs(ans_gauss[i][4]) > eps:
            print "NOT POSSIBLE, SNAPE IS WICKED!"

            ans_ex = False
            sys.exit(0)
        elif count_nonzero(ans_gauss[i]) == 0 and abs(ans_gauss[i][4]) < eps:
            zero = zero + 1
    for i in range(4):
        if ans_gauss[i][4] < -eps or ans_gauss[i][4] - X[i] > eps:
            print "NOT POSSIBLE, SNAPE IS WICKED!"
            ans_ex = False
            sys.exit(0)

    ans_ex = zero <= 0
    if ans_ex:
        print "EXACTLY ONE!"
        for a in ans_gauss:
            if a[4] - int(a[4]) < eps:
                print int(a[4]),
            else:
                print a[4],
    else:
        print "MORE THAN ONE"


def solve_gj_two(A, b, X):
    cur_line = 0
    n = k = 0
    with open(file) as f:
        for line in f:
            if cur_line == 0:
                n = int(line.split()[0])
                k = int(line.split()[1])
                cur_line = cur_line + 1
            elif cur_line == 1:
                b = map(float, line.split())
                cur_line = cur_line + 1
            elif cur_line <= len(b) + 1:
                augmented = get_aug(map(float, line.split()), b, cur_line - 1)
                A.append(augmented)
                cur_line = cur_line + 1
            else:
                X = map(float, line.split())
    ans_gauss, pivots, free = gauss_jordan(A, n, k + 1)
    zero = 0
    pretty_print(ans_gauss)

    for i in range(n):
        if count_nonzero(ans_gauss[i]) == 0 and abs(ans_gauss[i][k]) > eps:
            print "NOT POSSIBLE, SNAPE IS WICKED!"

            ans_ex = False
            sys.exit(0)
        elif count_nonzero(ans_gauss[i]) == 0 and abs(ans_gauss[i][k]) < eps:
            zero = zero + 1
    ans_ex = zero <= n - k
    print zero
    print n - k
    if ans_ex:
        for i in range(n):
            if ans_gauss[i][k] < -eps:
                print "NOT POSSIBLE, SNAPE IS WICKED!"
                ans_ex = False
                sys.exit(0)
    if ans_ex:
        print "EXACTLY ONE"
        for a in ans_gauss:
            if count_nonzero(a) > 0:
                if a[k] - int(a[k]) < eps:
                    print int(a[k]),
                else:
                    print a[k],
    else:
        print "MORE THAN ONE"
        l = 0
        for i in range(n - zero):
            print 'here'
            if abs(A[i][l]) > eps:
                l = i
                print l
                print "x_" + str(l+1), "=",
            else:
                l = i
                while abs(A[i][l]) < eps:
                    l = l + 1
                    if l == k:
                        continue
                print "x_" + str(l+1), "=",
            first = True
            for j in range(l + 1, k + 1):
                if j < k and abs(A[i][j]) > eps:
                    if abs(A[i][j] - int(A[i][j])) < eps:
                        coeff = str(-1* int(A[i][j]))
                    else:
                        coeff = str(-1 * A[i][j])
                    #print "Coeff", coeff
                    if coeff == "1":
                        coeff = ""
                    if coeff == "-1":
                        coeff = "-"
                    if not first:
                        if A[i][j] < 0: print "+",
                    if not first:
                        print str(coeff).replace('-', '- ') + "x_" + str(j+1),
                    else:
                        print str(coeff) + "x_" + str(j + 1),
                    first = False
                elif j == k:
                    if A[i][k] > eps:
                        print "+",
                    if not first:
                        print str(A[i][k]).replace('-', '- ')
                    else:
                        print A[i][k]
            l = l +1

        print(A)
        for i in range(n):
            if A[i][i] == 0:
                print 0,
            else: print A[i][k]


if __name__ == '__main__':

    eps = sys.float_info.epsilon
    part_one = True
    try:
        part_one = sys.argv[1].split('=')[1] == 'one'
        file = sys.argv[2]
    except IndexError:
        sys.exit(0)

    b = []
    A = []
    X = []
    if part_one:
        solve_gj_one(A, b, X)
    else:
        solve_gj_two(A, b, X)
        '''else:
            print "MORE THAN ONE"
            for i in range(n):
                if'''

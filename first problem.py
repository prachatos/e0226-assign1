import itertools
import random
import sys


def get_random_ints(free, X):
    try:
        Z = [list(range(0, int(X[fr]) + 1)) for fr in free]
    except OverflowError:
        Z = [list(range(0, min(X[fr] + 1, 600000))) for fr in free]
    pr = 1
    for x in free:
        pr *= (X[x] + 1)
    pop = min(500000, int(pr))
    if len(free) == 1:
        return [[x] for x in random.sample(Z[0], pop)]
    rsample = random.sample(list(itertools.product(*Z)), pop)
    return rsample


def get_valid_soln(new_eq, free, X):
    ans_vec = [0 for a in range(len(X))]
    found = False
    found_at = 0
    rand_set = get_random_ints(free, X)
    for x in range(0, len(rand_set)):
        for y in range(len(new_eq)):
            ans = 0
            for i in range(len(new_eq[y])):
                if i != len(new_eq[y]) - 1:
                    ans += new_eq[y][i] * rand_set[x][i]
                else:
                    ans += new_eq[y][i]
            if ans < eps or ans > X[y]:

                continue
            ans_vec[y] = ans
            if y == len(new_eq) - 1:
                found = True
                found_at = x
                break
    # this means we're done

    if found:
        i = 0
        for fr in free:
            ans_vec[fr] = rand_set[found_at][i]
            i = i + 1
        return True, ans_vec
    else:
        found_at = len(rand_set) - 1
        for y in range(len(new_eq)):
            ans = 0
            for i in range(len(new_eq[y])):
                if i != len(new_eq[y]) - 1:
                    ans += new_eq[y][i] * rand_set[found_at][i]
                else:
                    ans += new_eq[y][i]
            ans_vec[y] = ans
        return False, ans_vec


def write_list_to_file(f, l):
    for i in range(0, len(l)):
        f.write(l[i])
        if i != len(l) - 1:
            f.write('\n')


def read_file(part):
    if part == 'one':
        X = []
        b = []
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
        return A, b, X, 4, 4
    else:
        cur_line = 0
        n = k = 0
        X = []
        b = []
        with open(file) as f:
            for line in f:
                if cur_line == 0:
                    n, k = [int(x) for x in line.split()]
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
        return A, b, X, n, k


def print_general_soln(pivots, free, k):
    printed = 0
    gen_soln = ''
    for i in range(len(pivots)):
        cur_index = pivots[i]
        if printed:
            gen_soln = gen_soln + '; '
        gen_soln += "x_" + str(cur_index + 1) + " = "
        first = True
        for j in range(cur_index + 1, k + 1):
            if j < k and abs(A[i][j]) > eps:
                if abs(A[i][j] - int(A[i][j])) < eps:
                    coeff = str(-1 * int(A[i][j]))
                else:
                    coeff = str(-1 * A[i][j])
                # print "Coeff", coeff
                if coeff == "1":
                    coeff = ""
                if coeff == "-1":
                    coeff = "-"
                if not first:
                    if A[i][j] < 0:
                        gen_soln += " + "
                if not first:
                    gen_soln = gen_soln + str(coeff).replace('-', ' - ') + "x_" + str(j + 1)
                else:
                    gen_soln = gen_soln + str(coeff) + "x_" + str(j + 1)
                first = False
            elif j == k:
                if abs(A[i][j] - int(A[i][j])) < eps:
                    coeff = str(int(A[i][j]))
                else:
                    coeff = str(A[i][j])
                if A[i][k] > eps and not first:
                    gen_soln += " + "
                if not first:
                    gen_soln += str(coeff).replace('-', ' - ')
                else:
                    gen_soln += coeff
        printed += 1
    for free_var in free:
        if printed:
            gen_soln += '; '
        gen_soln += 'x_' + str(free_var + 1)

    # why am I doing this?
    if len(free) == 1:
        gen_soln += ' is a free variable'
    elif len(free) > 1:
        gen_soln += ' are free variables'
    return gen_soln


def gauss_jordan(aug, m, n):
    pivot_list = []
    for i in range(m):
        pivot = i, i
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
                if abs(aug[i][j]) > eps:
                    found_piv = True
                    pivot_list.append(pivot[1])
                    break
        if not found_piv:
            continue
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
            ratio = aug[j][pivot[1]]
            # print ratio
            for k in range(n):
                aug[j][k] = aug[j][k] - ratio * aug[i][k]
    free_var = list(set(range(n - 1)) - set(pivot_list))
    free_var.sort()
    for i in range(m):
        aug[i][n - 1] = round(aug[i][n - 1] * 1000) / 1000
    return aug, pivot_list, free_var


def get_aug(mat_a, mat_b, count):
    mat_a.append(mat_b[count - 1])
    return mat_a


def count_nonzero(arr):
    ans = 0
    for i in range(len(arr) - 1):
        if abs(arr[i]) > eps:
            ans = ans + 1
    return ans


def sum_column(A, col, n):
    sum = 0
    for i in range(n):
        sum += A[i][col]
    return sum


def val_int(v):
    if abs(v - int(round(v))) < 1e-7:
        return int(round(v))
    else:
        return v


def solve_gj_two(part):
    A, b, X, n, k = read_file(part)
    if check_for_sum_coeff:
        for i in range(k):
            if sum_column(A, i, n) - 1 >= eps:
                ans_queue.append("NOT POSSIBLE, SNAPE IS WICKED!")
                return
    ans_gauss, pivots, free = gauss_jordan(A, n, k + 1)
    zero = 0

    for i in range(n):
        if count_nonzero(ans_gauss[i]) == 0 and abs(ans_gauss[i][k]) > eps:
            ans_queue.append("NOT POSSIBLE, SNAPE IS WICKED!")

            return
        elif count_nonzero(ans_gauss[i]) == 0 and abs(ans_gauss[i][k]) < eps:
            zero = zero + 1
    ans_ex = zero <= n - k
    if ans_ex:
        for i in range(n):
            if ans_gauss[i][k] < -eps:
                ans_queue.append("NOT POSSIBLE, SNAPE IS WICKED!")
                return
    answers = ""
    if ans_ex:
        for i in range(n):
            if ans_gauss[i][k] < -eps or ans_gauss[i][k] - X[i] > eps:
                ans_queue.append("NOT POSSIBLE, SNAPE IS WICKED!")
                return
        ans_queue.append("EXACTLY ONE!")
        for a in ans_gauss:
            if count_nonzero(a) > 0:
                answers += str(val_int(a[k])) + ' '
        answers.rstrip()
        ans_queue.append(answers)
    else:
        ans_queue.append("MORE THAN ONE!")
        new_eq = []
        for br in pivots:
            new_param = []
            for fr in free:
                new_param.append(-1 * ans_gauss[br][fr])
            new_param.append(ans_gauss[br][k])
            new_eq.append(new_param)
        got_valid, soln = get_valid_soln(new_eq, free, X)
        ans_str = ''
        for val in soln:
            ans_str += str(val_int(round(val, 6))) + ' '
        ans_str.rstrip()
        ans_queue.append(ans_str)
        ans_queue.append(print_general_soln(pivots, free, k))


if __name__ == '__main__':

    check_for_sum_coeff = True
    eps = 1e-7
    part_one = True
    try:
        part_one = sys.argv[1].split('=')[1] == 'one'
        file = sys.argv[2]
    except IndexError:
        sys.exit(0)
    b = []
    A = []
    X = []
    ans_queue = []
    if part_one:
        op_file = open('output_problem1_part1.txt', 'w')
        solve_gj_two('one')
    else:
        op_file = open('output_problem1_part2.txt', 'w')
        solve_gj_two('two')
    write_list_to_file(op_file, ans_queue)

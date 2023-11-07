import numpy as np
from matplotlib import pyplot as plt
import pandas
from os import listdir
from os.path import isfile, join

def compute_path_width(mat, permutation):
    n = mat.shape[0]

    max_val = 0

    for i in range(n):
        sum_val = 0
        for j in range(i):
            for k in range(i, n):
                u = min(permutation[j], permutation[k])
                v = max(permutation[j], permutation[k])

                if mat[u,v] != 0:
                    sum_val += 1

        max_val = max(max_val, sum_val)
    
    return max_val


def find_good_ordering(mat):
    n = mat.shape[0]

    best_perm = np.arange(n)
    min_val = compute_path_width(mat, best_perm)

    M = 10

    for i in range(M):
        print(f"testing permutation #{i}")
        random_permutation = np.random.permutation(n)

        val = compute_path_width(mat, random_permutation)

        if val < min_val:
            best_perm = random_permutation
            min_val = val

    print("best val = ", min_val, "with permutation\n", best_perm)

    return best_perm


file_name = "Q_optimality.csv"

dataFrameMatA = pandas.read_csv(file_name)

matA = dataFrameMatA.to_numpy()

matA = matA[:-1,1:-1]

matA = np.array(matA, dtype=np.float32)

print(matA.shape)

n = matA.shape[0]

print("number non-zero entries", np.count_nonzero(matA))
print("ration = ", np.count_nonzero(matA) / (n*(n+1)/2))

exit(0)

# matA is the adjacency matrix
n = matA.shape[0]

perm = np.arange(n) # find_good_ordering(matA)


# manual_perm = np.array([i for i in range(20)] + [i for i in range(81, 126)] + [i for i in range(20, 81)])

manual_perm = np.array(list(range(7)) + list(range(14, 18)) + list(range(20, 81)) + list(range(7, 14)) + list(range(18, 20)) + list(range(81, 126)))

perm = manual_perm

print("val of manual perm = ", compute_path_width(matA, manual_perm))

matA[np.arange(n),:] = matA[perm,:]
matA[:,np.arange(n)] = matA[:,perm]

# make into upper triangular again
for i in range(n):
    for j in range(n-1, -1, -1):
        if i == j: continue

        elif i > j: matA[i,j] = 0

        elif i < j: matA[i,j] += matA[j,i]




matA = np.abs(matA)
matA += 1
matA = np.minimum(np.log(matA), 5.0)

plt.matshow(matA)
plt.savefig(file_name + '_permuted.png', dpi=300)



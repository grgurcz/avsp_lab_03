import sys
from decimal import Decimal, ROUND_HALF_UP
from math import sqrt, pow


def calculate_normals_matrix(pearson_matrix):
    normals_matrix = []
    for i in range(len(pearson_matrix)):
        normal = 0
        for j in range(len(pearson_matrix[i])):
            if pearson_matrix[i][j] != 'X':
                normal += pow(pearson_matrix[i][j], 2)
        normal = sqrt(normal)
        normals_matrix.append(normal)
    
    return normals_matrix


def calculate_pearson_matrix(original_matrix):
    new_matrix = []
    for i in range(len(original_matrix)):
        new_matrix.append([])
        for j in range(len(original_matrix[i])):
            new_matrix[i].append(0)
    
    for i in range(len(original_matrix)):
        ratings_avg = 0
        ratings_count = 0
        for j in range(len(original_matrix[i])):
            if original_matrix[i][j] != 'X':
                ratings_avg += original_matrix[i][j]
                ratings_count += 1
        
        ratings_avg /= ratings_count
        for j in range(len(original_matrix[i])):
            if original_matrix[i][j] != 'X':
                new_matrix[i][j] = original_matrix[i][j] - ratings_avg
    
    return new_matrix


def predict(original_matrix, matrix, normals, x, y, k):
    similarities = []
    for i in range(len(matrix)):
        current_sim = 0
        for j in range(len(matrix[i])):
            current_sim += matrix[i][j]*matrix[x][j]
        current_sim /= (normals[i]*normals[x])
        similarities.append((current_sim, original_matrix[i][y]))
    
    values_sum = 0
    similarities_sum = 0

    for sim in sorted(similarities, reverse=True):
        similarity, item = sim
        if k == 0:
            break

        if item == 'X' or similarity <= 0:
            continue

        values_sum += similarity * item
        similarities_sum += similarity
        k -= 1
    
    return Decimal(Decimal(values_sum/similarities_sum).quantize(Decimal('.001'), rounding=ROUND_HALF_UP))


def main():

    n, m = sys.stdin.readline().strip().split()
    n, m = int(n), int(m)

    item_user_matrix = []
    for i in range(n):
        item_user_matrix.append(sys.stdin.readline().strip().split())
        for j in range(m):
            if item_user_matrix[i][j] != 'X':
                item_user_matrix[i][j] = int(item_user_matrix[i][j])

    user_item_matrix = []
    for i in range(m):
        user_item_matrix.append([])
        for j in range(n):
            user_item_matrix[i].append(item_user_matrix[j][i])

    item_item_matrix = calculate_pearson_matrix(item_user_matrix)
    item_item_normals = calculate_normals_matrix(item_item_matrix)

    user_user_matrix = calculate_pearson_matrix(user_item_matrix)
    user_user_normals = calculate_normals_matrix(user_user_matrix)
    
    q = int(sys.stdin.readline().strip())

    for i in range(q):
        x, y, t, k = sys.stdin.readline().strip().split()
        x, y, t, k = int(x) - 1, int(y) - 1, int(t), int(k)
        if t == 0:
            print(predict(item_user_matrix, item_item_matrix, item_item_normals, x, y, k))
        else:
            print(predict(user_item_matrix, user_user_matrix, user_user_normals, y, x, k))



if __name__ == '__main__':
    main()
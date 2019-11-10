import random
import math
from matplotlib import pylab as pl


# Отрисовка точек и рёбер графа
def draw_vertices_and_edges(vertices_posisions, adj_matrix, weight_matrix):
    n = len(vertices_posisions)
    for i in range(n):
        pl.scatter(vertices_posisions[i][0], vertices_posisions[i][1])
        pl.text(vertices_posisions[i][0] + 0.1, vertices_posisions[i][1] + 0.1, i, fontsize=10)

    for i in range(n):
        for j in range(i):
            if adj_matrix[i][j] != 0:
                pl.plot(
                    [vertices_posisions[i][0], vertices_posisions[j][0]],
                    [vertices_posisions[i][1], vertices_posisions[j][1]])

                x = (vertices_posisions[i][0] - vertices_posisions[j][0]) / 2 + vertices_posisions[j][0]
                y = (vertices_posisions[i][1] - vertices_posisions[j][1]) / 2 + vertices_posisions[j][1]
                pl.text(x + 0.1, y + 0.1, weight_matrix[i][j], fontsize=10)

    pl.show()


# Вывод матрицы в консоль
def print_matrix(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            print(matrix[i][j], end = ",")
        print()


n = int(input('Введите количество точек:'))
k = int(input('Введите количество кластеров:'))

# Максимальное значение веса ребра при рандомной инициализации весов
max_weight_value = 10

# Отрисовка точек
vertices_pos = [
    (1 + math.cos(360 * i * math.pi / (n * 180)),
     1 + math.sin(360 * i * math.pi / (n * 180)))
    for i in range(n)]
for i in range(n):
    pl.scatter(vertices_pos[i][0], vertices_pos[i][1])

pl.show()

# Заполнение матрицы весов
weight_matrix = [[0 for j in range(n)] for i in range(n)]
for i in range(n):
    for j in range(i):
        weight_matrix[i][j] = random.randint(1, max_weight_value)
        weight_matrix[j][i] = weight_matrix[i][j]

# Вывод матрицы весов
for i in range(n):
    for j in range(n):
        print(weight_matrix[i][j], end=',')
    print()

# Матрица смежности
adj_matrix = [[0 for j in range(n)] for i in range(n)]

# Количество смежных вершин для каждой вершины (степень вершины)
vertices_degrees = [0 for i in range(n)]

# поиск наименьшего веса
min_weight = max_weight_value
min_weight_i = 0
min_weight_j = 0
for i in range(n):
    for j in range(i):
        if weight_matrix[i][j] < min_weight:
            min_weight = weight_matrix[i][j]
            min_weight_i = i
            min_weight_j = j

# Соединяем ребром найденные вершины
adj_matrix[min_weight_i][min_weight_j] = 1
adj_matrix[min_weight_j][min_weight_i] = 1
vertices_degrees[min_weight_i] += 1
vertices_degrees[min_weight_j] += 1

print()
print("first iteration:")
print_matrix(adj_matrix)

draw_vertices_and_edges(vertices_pos, adj_matrix, weight_matrix)

iteration = 2
while True:

    # Минимальная дистанция до остова
    min_dist = max_weight_value
    min_weight_i = -1
    min_weight_j = -1

    # Пробегаемся по изолированным вершинам (со степенью 0)
    for i in range(n):
        if vertices_degrees[i] == 0:

            # Считаем для вершины расстояние до остова (до ближайшей точки со степенью > 0)
            min_edge_weight = max_weight_value
            min_edge_id = -1
            for j in range(n):
                if i != j and vertices_degrees[j] != 0:
                    if weight_matrix[i][j] < min_edge_weight:
                        min_edge_weight = weight_matrix[i][j]
                        min_edge_id = j

            if min_edge_weight < min_dist:
                min_dist = min_edge_weight
                min_weight_i = i
                min_weight_j = min_edge_id

    # Если минимальное расстояние не найдено - выходим из цикла
    if min_weight_i == -1:
        break

    # Соединяем ребром найденные вершины
    adj_matrix[min_weight_i][min_weight_j] = 1
    adj_matrix[min_weight_j][min_weight_i] = 1
    vertices_degrees[min_weight_i] += 1
    vertices_degrees[min_weight_j] += 1

    print()
    print("iteration: ", iteration)
    print_matrix(adj_matrix)
    iteration += 1

    draw_vertices_and_edges(vertices_pos, adj_matrix, weight_matrix)

# Удаляем К - 1 самых длинных рёбер
for x in range(k - 1):

    # Ищем самое длинное ребро
    max_weight = 0
    max_weight_i = -1
    max_weight_j = -1
    for i in range(n):
        for j in range(i):
            if adj_matrix[i][j] == 1 and weight_matrix[i][j] > max_weight:
                max_weight = weight_matrix[i][j]
                max_weight_i = i
                max_weight_j = j

    #  Удаляем найденное ребро
    adj_matrix[max_weight_i][max_weight_j] = 0
    adj_matrix[max_weight_j][max_weight_i] = 0
    vertices_degrees[max_weight_i] -= 1
    vertices_degrees[max_weight_j] -= 1


    print()
    print("delete iteration:", x)
    print_matrix(adj_matrix)
    draw_vertices_and_edges(vertices_pos, adj_matrix, weight_matrix)
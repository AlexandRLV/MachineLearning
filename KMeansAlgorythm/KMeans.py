import random
import numpy as np
import math
from matplotlib import pylab as pl

n = int(input('Введите количество точек:'))
k = int(input('Введите количество кластеров:'))

# Цвета для точек
colors = [
    'black',
    'silver',
    'firebrick',
    'red',
    'bisque',
    'gold',
    'palegreen',
    'green',
    'aqua',
    'skyblue',
    'blue',
    'purple',
    'plum',
    'pink',
    'white']

# Массив точек
points = [(random.random(), random.random()) for i in range(n)]

# Поиск центра
center_point = [0, 0]
for i in range(n):
    center_point[0] += points[i][0]
    center_point[1] += points[i][1]
    pl.scatter(points[i][0], points[i][1], c='g')

center_point[0] /= n
center_point[1] /= n

pl.show()

# Поиск самой дальней точки, построение первичных центров по окружности
farthest_point = [0, 0]
max_distance = 0
for i in range(n):
    distances = math.hypot(center_point[0] - points[i][0], center_point[1] - points[i][1])
    if (distances > max_distance):
        max_distance = distances
        farthest_point = points[i]

# Вывод получившихся точек и первичных центров
points_to_draw = points
points_to_draw.append((center_point[0], center_point[1]))
a = np.array(points_to_draw)
pl.scatter(a[:, 0], a[:, 1])
pl.plot([center_point[0], farthest_point[0]], [center_point[1], farthest_point[1]])

# Первичные центры расположены по окружности
centers = [
    (center_point[0] + max_distance * math.cos(360 * i * math.pi / (k * 180)),
     center_point[1] + max_distance * math.sin(360 * i * math.pi / (k * 180))
     ) for i in range(k)]

for i in range(k):
    pl.scatter(centers[i][0], centers[i][1], c='pink', marker='+')

pl.show()

# Распределение по кластерам
# Каждая точка соотносится с ближайшим кластером
clusters = [[] for i in range(k)]
for i in range(n):

    distances = []
    min_distance = max_distance
    min_distance_id = 0

    for j in range(k):
        distances.append(
            math.hypot(
                centers[j][0] - points[i][0],
                centers[j][1] - points[i][1]))
        if distances[j] < min_distance:
            min_distance = distances[j]
            min_distance_id = j

    clusters[min_distance_id].append(points[i])
    pl.scatter(points[i][0], points[i][1], c=colors[min_distance_id])

for i in range(k):
    pl.scatter(centers[i][0], centers[i][1], c='pink', marker='+')

pl.show()

#поиск новых центров и распределение по ним
while True:

    #флаг
    stop = True

    #пересчитываем центры
    for i in range(k):
        new_center = [0, 0]
        cluster_len = clusters[i].__len__()
        for j in range(cluster_len):
            new_center[0] += clusters[i][j][0]
            new_center[1] += clusters[i][j][1]

        new_center[0] /= cluster_len
        new_center[1] /= cluster_len
        if centers[i][0] != new_center[0] or centers[i][1] != new_center[1]:
            stop = False
            pl.scatter(centers[i][0], centers[i][1], c='blue', marker='+')
            pl.plot([centers[i][0], new_center[0]], [centers[i][1], new_center[1]])
            centers[i] = (new_center[0], new_center[1])


    if stop:
        for i in range(k):
            pl.scatter(centers[i][0], centers[i][1], c=colors[i], marker='+')
            cluster_len = clusters[i].__len__()
            for j in range(cluster_len):
                pl.scatter(clusters[i][j][0], clusters[i][j][1], c=colors[i])
        pl.show()
        break

    for i in range(k):
        pl.scatter(centers[i][0], centers[i][1], c='pink', marker='+')
        clusters[i].clear()

    #распределяем точки по новым кластерам
    for i in range(n):
        distances = []
        min_distance = max_distance
        min_distance_id = 0
        for j in range(k):
            distances.append(math.hypot(centers[j][0] - points[i][0], centers[j][1] - points[i][1]))
            if distances[j] < min_distance:
                min_distance = distances[j]
                min_distance_id = j
        clusters[min_distance_id].append(points[i])
        pl.scatter(points[i][0], points[i][1], c=colors[min_distance_id])

    pl.show()
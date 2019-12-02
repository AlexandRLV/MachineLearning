from matplotlib import pyplot as pl
import random
import math


#Train data generator
def generate_data(numberOfClassEl, numberOfClasses):
    data = []
    for classNum in range(numberOfClasses):
        #Choose random center of 2-dimensional gaussian
        centerX, centerY = random.random() * 5.0, random.random() * 5.0
        #Choose numberOfClassEl random nodes with RMS=0.5
        for rowNum in range(numberOfClassEl):
            data.append([[random.gauss(centerX, 0.5), random.gauss(centerY, 0.5)], classNum])
    return data


def dist(point1, point2):
    return math.sqrt((point1[0] - point2[0]) * (point1[0] - point2[0]) + (point1[1] - point2[1]) * (point1[1] - point2[1]))


def sort_points_by_distance(data, point):
    new_data = []

    for i in range(len(data)):
        new_data.append((dist(data[i][0], point), data[i]))

    return sorted(new_data, key=lambda x: x[0])


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

number_of_classes = 3#int(input())
number_of_elements = 10#int(input())

total_points_count = number_of_classes * number_of_elements
k = math.floor(math.sqrt(total_points_count))

data = generate_data(number_of_elements, number_of_classes)

for i in range(len(data)):
    pl.scatter(data[i][0][0], data[i][0][1], c=colors[data[i][1]])

pl.show()

point = (random.random() * 5.0, random.random() * 5.0)

for i in range(len(data)):
    pl.scatter(data[i][0][0], data[i][0][1], c=colors[data[i][1]])

pl.scatter(point[0], point[1], c='pink', marker='+')
pl.show()

points_by_distance = sort_points_by_distance(data, point)

classes_frequency = [0 for i in range(number_of_classes)]
for i in range(k):
    classes_frequency[points_by_distance[i][1][1]] += 1

max_frequency = 0
most_often_class = 0
for i in range(number_of_classes):
    if classes_frequency[i] > max_frequency:
        max_frequency = classes_frequency[i]
        most_often_class = i

for i in range(len(data)):
    pl.scatter(data[i][0][0], data[i][0][1], c=colors[data[i][1]])

print(point)

pl.scatter(point[0], point[1], c=colors[most_often_class], marker='+')
pl.show()
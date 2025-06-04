import math
import random


def euclidean_dis(p1, p2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))


"""
1-nn classify
"""
def nearest_neighbor(train_data, test_feature, selected_feature=None):
    min_dis = float('inf')
    nearest_class = None

    if selected_feature is not None:
        test_feature = [test_feature[i] for i in selected_feature]

    # traverse all the data in set to find the nearest neighbor
    for features, class_label in train_data:
        if selected_feature is not None:
            features = [features[i] for i in selected_feature]

        dis = euclidean_dis(features, test_feature)
        if dis < min_dis:
            min_dis = dis
            nearest_class = class_label

    return nearest_class


"""
leave one out cross validation
https://en.wikipedia.org/wiki/Cross-validation_(statistics)
"""
def loocv(data, selected_feature=None):
    correct = 0 
    total = len(data)
    for i in range(total):
        test_feature, test_class = data[i]
        train_data = data[:i] + data[i+1:]

        predicted_class = nearest_neighbor(train_data, test_feature, selected_feature)
        if predicted_class == test_class:
            correct += 1

    return round(correct / total, 5)


def load_labeled_txt(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            label = parts[0] # keep string format
            features = list(map(float, parts[1:]))
            data.append((features, label))
    return data


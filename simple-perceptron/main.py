import numpy as np
import classifier.perceptron_pla_classifier as pc_pla
import classifier.perceptron_gd_classifier as pc_gd
import data_generator as dg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

training_data = "/Users/harpreetsingh/github/stats-learning/simple-perceptron/resources/data.txt"


def load_training_data(file_name):
    labels = []
    features = []
    with open(file_name, 'r') as file:
        for row in file:
            data_string = row.strip().split()
            data = []
            class_label = -1
            for i in range(len(data_string)):
                if i == 0:
                    class_label = int(data_string[i])
                    continue
                data.append(float(data_string[i]))

            labels.append(class_label)
            features.append(np.array(data))

    return np.array(features), np.array(labels)


def visualize_data(x_mat, y_vec, plane_eq):
    x_range = [int(min(x_mat[0]) - 5), int(max(x_mat[0]) + 5)]
    y_range = [int(min(x_mat[1]) - 5), int(max(x_mat[1]) + 5)]
    dg.visualize_3d_data(x_mat, y_vec, plane_eq, x_range, y_range)

    return


def run_pla_classifier(x, y):
    classifier = pc_pla.PerceptronPLAClassifier(x, y)
    print("weights: ", classifier.get_weights())

    visualize_data(x, y, classifier.get_weights())

    return


def run_gd_classifier(x, y):
    classifier = pc_gd.PerceptronGDClassifier(x, y)
    print("weights: ", classifier.get_weights())

    visualize_data(x, y, classifier.get_weights())

    return


def main():
    x, y = load_training_data(training_data)

    # run_pla_classifier(x, y)
    run_gd_classifier(x, y)

    return


if __name__ == '__main__':
    main()

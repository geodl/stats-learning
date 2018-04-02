import numpy as np
import matplotlib.pyplot as plt
import classifier.neural_network as nn
import classifier.solver as solver
import data_util as du


def main():
    # configuration
    input_size = 16
    learning_rate = 0.001
    momentum = 0.9
    num_gen = 10000
    percent_test_set = 0.20
    online_update = 1

    # training and testing data
    du.get_phoneme_data()

    all_x_train, all_y_train, pca_transform = du.get_digits_training_data(num_dimensions=input_size)
    test_data = du.get_digits_test_data(pca_transform)

    num_val = int(all_x_train.shape[0] * percent_test_set)

    x_train_test = all_x_train[0:num_val]
    y_train_test = all_y_train[0:num_val]
    x_train = all_x_train[num_val:]
    y_train = all_y_train[num_val:]

    # train neural network
    network_model = nn.FullyConnectedNetwork(input_size, [16], 10, activation="sigmoid")

    network_solver = solver.Solver(network_model,
                                   {"x_train": x_train, "y_train": y_train,
                                    "x_test": x_train_test, "y_test": y_train_test},
                                   optimization={"type": "sgd", "learn_rate": learning_rate, "momentum": momentum},
                                   num_gen=num_gen,
                                   gradient_update_online=online_update,
                                   log_level=solver.Solver.LogLevel.INFO)

    network_model = network_solver.train()

    # todo: run test data and visualize results

    return


if __name__ == '__main__':
    main()

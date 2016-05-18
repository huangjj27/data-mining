#!/usr/bin/python2
"""module alpha

chooses the best alpha

"""
from os import system

import numpy as np

import params
# get params
from params import M_PARAM_TRAIN
from params import N_FEATURE
from params import ALPHAS
from params import LAMBDA
from params import ITERS

from lr import train_lr_gd


def main():
    """  """
    train_file = open(params.X_TRAIN_FILE, 'r')
    alpha_file = open(params.ALPHA_FILE, "w")

    X_train = np.zeros((M_PARAM_TRAIN, N_FEATURE))
    y_train = np.zeros((M_PARAM_TRAIN, 1))
    for i in range(M_PARAM_TRAIN):
        a_line = train_file.readline().strip()
        a_line = a_line.split(' ')  # seperate the data

        # get the label
        y_train[i] = int(a_line[0])
        a_line.pop(0)  # throw the label away

        for pair in a_line:
            pair = pair.split(':')
            X_train[i, int(pair[0]) - 1] = float(pair[1])

    train_file.close()
    costs = []
    for alpha in ALPHAS:
        print 'alpha: %e' % alpha
        [cost, theta] = train_lr_gd('logistic', X_train, y_train, alpha, LAMBDA, ITERS)
        costs.append(cost)

    np.transpose(costs)

    for row in costs:
        for a_cost in row:
            alpha_file.write('%f ' % a_cost)
        alpha_file.write('\n')

    alpha_file.close()


if __name__ == '__main__':
    main()
    system("pause")

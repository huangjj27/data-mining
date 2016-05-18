""" logistic regression model

Copyright (c) huangjj27@SYSU (SNO: 13331087). ALL RIGHTS RESERVERD.

"""
import sys

from numpy import dot
from numpy import exp
from numpy import hstack
from numpy import log
from numpy import ones
from numpy import vstack
from numpy import zeros

from random import randint


def sigmoid(z):
    return 1 / (1 + exp(-z))


def hyphothesis_logistic(X, theta, m):
    hyphothesis = sigmoid(dot(X, theta))
    if m == 1:
        hyphothesis = hyphothesis[0, 0]

    return hyphothesis


def hyphothesis_linear(X, theta, m):
    hyphothesis = dot(X, theta)
    if m == 1:
        hyphothesis = hyphothesis[0, 0]

    return hyphothesis


hypho = {"logistic": hyphothesis_logistic, "linear": hyphothesis_linear}


def cost_linear(h, label, m):
    a_cost = (1.0 / (2 * m)) * dot((h - label).T, (h - label))
    return a_cost[0, 0]


def cost_logistic(h, label, m):
    a_cost = (-1.0 / m) * (dot(label.T, log(h)) + dot(
        (1 - label).T, log(1 - h)))
    return a_cost[0, 0]


cost = {"logistic": cost_logistic, "linear": cost_linear}


def lr_cost(lrtype, X, label, theta, a_lambda=0):
    """calculate the cost of a lr model

    Args:
        lrtype: the type of lr regression.linear or logistic
        X: the samples' feature matrix
        label: the samples' label vector
        theta: the weights of X
        a_lambda: regularation parameter

    Returns:
        J: the cost
        grad: the gradient of theta
    """

    m = label.shape[0]  # number of training exmaples

    vecReg = vstack([0, theta[1:]])  # then gets the Regularation vector
    X = hstack([ones((m, 1)), X])  # NOTE: X matrix is without bias

    # computes
    h = hypho[lrtype](X, theta, m)  # the hyphothesis vector
    J = cost[lrtype](h, label, m)  # the loss between labels and hyphothesis
    grad = (1.0 / m) * dot(X.T, (h - label))  # the grad for theta

    # regularization
    J = J + ((a_lambda + 0.0) / (2 * m)) * dot(vecReg.T, vecReg)
    grad = grad + (a_lambda + 0.0 / m) * vecReg

    return [J[0, 0], grad]


def train_lr_gd(lrtype,
                X_train,
                label,
                alpha,
                a_lambda=0,
                iters=200,
                span=1,
                batch=0):
    """train a lr model with gradient descenting

    Args:
        batch: subset of the samples
        alpha: learning rate
        iters: times for training
        X_train: sample matrix
        lrtype: the type of lr regression.linear or logistic
        label: the samples' label vector
        a_lambda: regularation parameter
        span: each span write a data

    Returns:
        cost: the cost list of each iters
        grad: the gradient of theta

    """

    # get the shape of sample matrix
    m = X_train.shape[0]
    n = X_train.shape[1]

    theta = zeros((X_train.shape[1] + 1, 1))

    cost_list = []
    for i in range(1, iters + 1):
        if 0 < batch <= m / 2:
            choosen = randint(0,
                              m / batch - 1)  # choose a batch from the X_train
            X_batch = X_train[choosen:choosen + batch]
            y_batch = label[choosen:choosen + batch]
            [J, grad] = lr_cost(lrtype, X_batch, y_batch, theta, a_lambda)
        else:
            [J, grad] = lr_cost(lrtype, X_train, label, theta, a_lambda)

        theta = theta - alpha * grad  # gradient descenting

        if i % span == 0 or i == iters:
            cost_list.append(J)
            sys.stdout.write('iter: %4d/%4d, cost: %f\r' % (i, iters, J))
    print ''

    return [cost_list, theta]

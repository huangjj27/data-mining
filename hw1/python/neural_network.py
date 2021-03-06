"""module neural network

the cost function and gradient trainning with a sample

"""
#!/usr/bin/python2
import params
import numpy as np
from lr import sigmoid


def sigmoidGradient(z):
    g = np.zeros(z.shape)
    g = sigmoid(z) * (1 - sigmoid(z))

    return g


def ReLU(vec):
    return np.maximum(0, vec)


def ReLUGradient(z):
    g = np.zeros(z.shape)
    g = (z > 0)

    return g


active = {"sigmoid": sigmoid, "ReLU": ReLU}


def a_layer(input_vec, theta, active_type):
    """
    computes output vector given a un active input vector without bias,
    the params matrix theta, and active function

    """
    # row_in, col_in = input_vec.shape
    # row_theta, col_theta = theta.shape

    # if not (row_in is col_theta):

    input_vec = np.vstack([1, input_vec])  # add bias element
    input_vec = active[active_type](input_vec)  # choose a active function.

    output_vec = np.dot(theta, input_vec)

    return output_vec

# TODO: compute a neural network cost and grad with back propagation
# def nnCost(x, y, theta, layers, a_lambda, active="sigmoid"):
#     z = [x]
#     a = []
#     params = []

#     for i in range(layers) - 1:
#         a.append(active(z[i]))
#         params.append(theta[layers[i] * layers[i + 1], 1].reshape((layers[
#             i], layers[i + 1])))
#         z.append(a_layer(z[i], params[i], active))

#     return J, grad


def nnCost(X, y, theta, input_layer_size, hidden_layer_size, a_lambda=0):
    # get the two parmas matrix
    theta1 = theta[0:hidden_layer_size * (input_layer_size + 1), 0].reshape((
        hidden_layer_size, input_layer_size + 1))
    theta2 = theta[(hidden_layer_size * (input_layer_size + 1)):, 0].reshape((
        1, hidden_layer_size + 1))

    theta1_grad = np.zeros(theta1.shape)
    theta2_grad = np.zeros(theta2.shape)
    J = 0

    m, n = X.shape
    X = np.hstack([np.ones((m, 1)), X])

    for i in range(m):
        x = X[i, :].reshape(1, n + 1).T  # a sample vector
        # forward propagation
        z_2 = np.dot(theta1, x)
        a_2 = np.vstack([1, sigmoid(z_2)])  # add bias then active

        z_3 = np.dot(theta2, a_2)  # output layer, no active
        a_3 = sigmoid(z_3)

        J += 0.5 * np.square(y[i] - a_3)  # computes cost

        # back propagation
        delta3 = a_3 - y[i]
        delta2 = np.dot(theta2[:, 1:].T, delta3) * sigmoidGradient(z_2)

        theta2_grad += np.dot(delta3, a_2.T)
        theta1_grad += np.dot(delta2, x.T)

    J /= (m + 0.0)
    theta1_grad /= (m + 0.0)
    theta2_grad /= (m + 0.0)

    grad = np.vstack([theta1_grad.flatten(1).reshape((hidden_layer_size * (
        input_layer_size + 1), 1)), theta2_grad.flatten(1).reshape((
            hidden_layer_size + 1, 1))])
    return J[0, 0], grad


def nnPredict(x, theta, input_layer_size, hidden_layer_size, a_lambda=0):
    theta1 = theta[0:hidden_layer_size * (input_layer_size + 1), 0].reshape((
        hidden_layer_size, input_layer_size + 1))
    theta2 = theta[(hidden_layer_size * (input_layer_size + 1)):, 0].reshape((
        1, hidden_layer_size + 1))

    x = np.vstack([1, x])

    # forward propagation
    z_2 = np.dot(theta1, x)
    a_2 = np.vstack([1, sigmoid(z_2)])

    z_3 = np.dot(theta2, a_2)
    a_3 = sigmoid(z_3)

    return a_3[0, 0]

import numpy as np
import matplotlib.pyplot as plt
n = 100
iterations = 1000
hidden_neurons = 100
mA = [1.0, 0.3]
mB = [0.0, -0.1]
sigmaA = 0.2
sigmaB = 0.3
step_length = 0
learning_rate = 0.001


def phi(x):
    return (2 / (1 + np.exp(-x))) - 1


def phi_prime(x):
    return ((1 + phi(x)) * (1 - phi(x))) / 2


def generate_matrices():
    X = np.zeros([3,2*n])
    # Make non linear sets as before, i used normal cuz it was fucked when i did random.rand and concat
    X[0, :n] = np.concatenate((np.random.normal(1, 1, int(n / 2)) * sigmaA - mA[0], np.random.normal(1, 1, int(n / 2)) * sigmaA + mA[0]))
    X[0,n:] = np.random.normal(0,1,n) * sigmaB + mB[0]
    X[1,:n] = np.random.normal(0,1,n) * sigmaA + mA[1]
    X[1,n:] = np.random.normal(0,1,n) * sigmaB + mB[1]
    # added biased
    X[2, :2*n] = 1.0
    # Vikter från X -> Hidden layers
    W = np.random.normal(1, 0.5, (hidden_neurons, X.shape[0]))
    # Vikter från Hidden layers -> Output, jag la till 1 så att vi kan hantera bias och matris multiplikation
    V =  np.random.normal(1,0.5,(1,hidden_neurons + 1))
    # T är som vanligt
    T = np.zeros([1,2*n])
    T[0,:n] = 1
    T[0,n:] = -1

    return X,W,V,T


def plot(X):
    plt.scatter(X[0,:n],X[1,:n])
    plt.scatter(X[0,n:],X[1,n:])
    plt.show()


# Forward pass är att gå från X till output
def forward_pass(X,W,V):
    hin = W @ X
    hout = np.concatenate((phi(hin), np.ones((1, X.shape[1]))))
    oin = V @ hout
    out = phi(oin)
    return out, hout


def back_pass(out,hout,T,V):
    delta_o = out-T * phi_prime(out)
    delta_h = (np.transpose(V) @ delta_o) * phi_prime(hout)
    # Gotta remove the last part(bias)
    delta_h = delta_h[:hidden_neurons, :]
    return delta_h, delta_o


def get_delta_weights(delta_h, delta_o, X, eta, h_out):
    delta_W = -eta * delta_h@np.transpose(X)
    delta_V = -eta * delta_o @ np.transpose(h_out)
    return delta_W, delta_V


def update_weights(V, W, delta_W, delta_V):
    V = V + delta_V
    W = W + delta_W
    return V,W


def calculate_error(X, W, T):
    return np.sum((T - W@X) ** 2) / 2


# def mean_square_error():
# def get_delta_weights_momentum
def two_layer_train(X, T, W, V, epoch, eta):
    acc_list = []
    iterations = []
    error_list = []
    for i in range(epoch):
        # print(W)
        # print(V)
        """ 
        First we get o_out(final output) and h_out (output from hidden node) with forward pass, 
            then we get the delta_h,delta_o by using back propagation, finally we set deltaW,deltaV and repeat for set epochs
        """
        prev_W, prev_V = W, V
        o_out, h_out = forward_pass(X,W,V)
        delta_h, delta_o = back_pass(o_out,h_out,T,V)
        delta_W, delta_V = get_delta_weights(delta_h, delta_o, X, eta, h_out)
        V, W = update_weights(V,W,delta_W,delta_V)
        prev_error, new_error = calculate_error(X, prev_W, T), calculate_error(X, W, T)
        error_list.append(abs(prev_error - new_error))
        acc_list.append(calc_accuracy(X, W, V, T))
        iterations.append(i)
    return W, V, error_list, acc_list, iterations


def plot_all_two_layer(X, W, V, eta=0.001, iteration=0):
    """
    Func plot_all/6
    @spec plot_all(np.array(), np.array(), boolean, boolean, integer, integer) :: void
        Plots both the perceptron line & both datasets.
        We can find the line due to the following property:
            Wx = 0
            which in our case means: w0 + w1x1 + w2x2 = 0
    """

    use_bias = True

    plt.scatter(X[0, n:], X[1, n:], color="red")
    plt.scatter(X[0, :n], X[1, :n], color="blue")
    plt.title("Computing two layer perceptron;")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.ylim(top = 1.5, bottom = -1.5)
    x_one = np.linspace(-3, 3, 200)
    y_one = 0
    if use_bias:
        bias = W[0][2]
        k = -(bias/W[0][1])/(bias/W[0][0])
        m = -bias/W[0][1]
        y_one = k*x_one + m
    else:
        """If the bias is set to False, the line is equal to y = k*x where k is equal to y/x."""
        k = W[0][0]/W[0][1]
        y_one = k*x_one

    x_two = np.linspace(-3, 3, 200)
    y_two = 0
    if use_bias:
        bias = V[0][2]
        k = -(bias/V[0][1])/(bias/V[0][0])
        m = -bias/V[0][1]
        y_two = k*x_two + m
    else:
        """If the bias is set to False, the line is equal to y = k*x where k is equal to y/x."""
        k = V[0][0]/V[0][1]
        y_two = k*x_two
    # plt3d.plot_surface(xx, yy, z, alpha=0.2)
    plt.plot(x_one, y_one, color="green")
    plt.plot(x_two, y_two, color="pink")
    plt.show()


def plot_sets(X, eta):
    """
    Func plot_all/6
    @spec plot_all(np.array(), np.array(), boolean, boolean, integer, integer) :: void
        Plots both the perceptron line & both datasets.
        We can find the line due to the following property:
            Wx = 0
            which in our case means: w0 + w1x1 + w2x2 = 0
    """

    plt.scatter(X[0, :100], X[1, :100], color="blue")
    plt.scatter(X[0, 100:], X[1, 100:], color="red")
    plt.title(f"Multi-layer perceptron learning {eta}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.ylim(top=0.5, bottom=-0.5)
    plt.show()


def calc_accuracy(X, W, V, T, non_separable = True):
    """
    Func calc_accuracy/3
    @spec calc_accuracy(np.array(), np.array(), np.array()) :: integer
        Counts how many of the input values Xi in X are classified correctly given the weight and target matrices W & T.
    """
    o_out, h_out = forward_pass(X, W, V)
    count = 0
    if non_separable:
        for i in range(2*n):
            if o_out[0][i] > 0 and T[0][i] == 1:
                count += 1
            if o_out[0][i] < 0 and T[0][i] == -1:
                count += 1
    else:
        for i in range(2*n):
            if o_out[0][i] > 0 and T[0][i] == 1:
                count += 1
            if o_out[0][i] < 0 and T[0][i] == -1:
                count += 1
    return count/(2*n)


def plot_accuracy(accuracy_list, iteration_list):
    plt.plot(iteration_list, accuracy_list, color="green")
    plt.xlabel("Number of iterations")
    plt.ylabel("Accuracy rate")
    plt.title(f"2-layer perceptron: {hidden_neurons} hidden neurons")
    plt.show()


def plot_mean_squared_error(error_list, iteration_list):
    plt.plot(iteration_list, error_list, color="green")
    plt.xlabel("Number of iterations")
    plt.ylabel("Mean Squared Error")
    plt.title(f"2-layer perceptron: {hidden_neurons} hidden neurons")
    plt.show()


X, W, V, T = generate_matrices()
plot_sets(X, learning_rate)
W, V, err_list, acc_list, it_list = two_layer_train(X, T, W, V, 10000, learning_rate)
plot_accuracy(acc_list, it_list)
plot_mean_squared_error(err_list, it_list)
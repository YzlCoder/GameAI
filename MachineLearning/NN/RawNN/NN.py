import numpy as np

# 激活函数
def relu(x):
    return np.maximum(0, x)

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)

def cross_entropy(pred, real):
    n_samples = real.shape[0]
    pred = pred.clip(1e-12, 1 - 1e-12)
    return -np.sum(real * np.log(pred)) / n_samples

def relu_deriv(x):
    return x > 0

def softmax_deriv(x):
    sx = softmax(x)
    return sx * (1 - sx)

def cross_entropy_deriv(pred, real):
    n_samples = real.shape[0]
    return pred - real



# 定义 Layer 类
class Layer:
    def __init__(self, input_size, output_size):
        self.weights = np.random.randn(input_size, output_size) * 0.1
        self.bias = np.zeros((1, output_size))
        self.input = None
        self.output = None

    def forward(self, input):
        self.input = input
        self.output = np.dot(input, self.weights) + self.bias
        return self.output

    def backward(self, output_gradient, learning_rate):
        weights_gradient = np.dot(self.input.T, output_gradient)
        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * np.mean(output_gradient, axis=0)
        return np.dot(output_gradient, self.weights.T)
# 定义神经网络
class NeuralNetwork:
    def __init__(self):
        self.layers = []
        self.activations = []

    def add_layer(self, layer, activation, activation_deriv):
        self.layers.append(layer)
        self.activations.append((activation, activation_deriv))

    def forward(self, input_data):
        output = input_data
        for i, (layer, activation) in enumerate(zip(self.layers, self.activations)):
            output = activation[0](layer.forward(output))
        return output

    def backward(self, loss_gradient, learning_rate):
        for i in reversed(range(len(self.layers))):
            layer = self.layers[i]
            activation = self.activations[i][1]
            loss_gradient = layer.backward(activation(layer.output) * loss_gradient, learning_rate)

    def train(self, x_train, y_train, epochs, learning_rate):
        training_results = []
        for epoch in range(epochs):
            output = self.forward(x_train)
            loss_gradient = cross_entropy_deriv(output, y_train)
            self.backward(loss_gradient, learning_rate)
            if epoch % 100 == 0:
                loss = cross_entropy(output, y_train)
                training_results.append((epoch, loss))
        return training_results


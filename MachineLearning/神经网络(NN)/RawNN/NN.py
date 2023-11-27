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
    return (x > 0).astype(np.float32)  # 这里将布尔数组转换为浮点型数组

def softmax_deriv(x):
    sx = softmax(x)
    return sx * (1 - sx)

def cross_entropy_deriv(pred, real):
    n_samples = real.shape[0]
    return pred - real

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

    def backward(self, output_gradient, learning_rate, max_grad_norm=None):
        weights_gradient = np.dot(self.input.T, output_gradient)
        bias_gradient = np.mean(output_gradient, axis=0)

        # 对权重梯度进行梯度裁剪
        if max_grad_norm is not None:
            grad_norm = np.linalg.norm(weights_gradient)
            if grad_norm > max_grad_norm:
                weights_gradient = weights_gradient / grad_norm * max_grad_norm

        # 使用裁剪后的梯度更新权重和偏置
        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * bias_gradient

        return np.dot(output_gradient, self.weights.T)

# 定义神经网络
class NeuralNetwork:
    def __init__(self):
        self.layers = []
        self.activations = []
        self.loss_function = (cross_entropy, cross_entropy_deriv)

    def add_layer(self, layer, activation, activation_deriv):
        self.layers.append(layer)
        self.activations.append((activation, activation_deriv))

    def set_loss(self, loss, loss_deriv):
        self.loss_function = (loss, loss_deriv)

    def forward(self, input_data):
        output = input_data
        for i, (layer, activation) in enumerate(zip(self.layers, self.activations)):
            output = activation[0](layer.forward(output))
        return output

    def backward(self, loss_gradient, learning_rate):
        for i in reversed(range(len(self.layers))):
            layer = self.layers[i]
            activation_deriv = self.activations[i][1]
            if activation_deriv is None:
                loss_gradient = layer.backward(loss_gradient, learning_rate, max_grad_norm=1.0)
            else:
                loss_gradient = layer.backward(activation_deriv(layer.output) * loss_gradient, learning_rate, max_grad_norm=1.0)

    def train(self, x_train, y_train, epochs, learning_rate, train_iter):
        for epoch in range(epochs):
            output = self.forward(x_train)
            loss_gradient = self.loss_function[1](output, y_train)
            self.backward(loss_gradient, learning_rate)
            if epoch % 1000 == 0:
                loss = self.loss_function[0](output, y_train)
                if train_iter is not None:
                    train_iter(epoch, loss)


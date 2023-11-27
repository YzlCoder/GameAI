import NN
import numpy as np

nn = NN.NeuralNetwork()
nn.add_layer(NN.Layer(2, 10), NN.relu, NN.relu_deriv)
nn.add_layer(NN.Layer(10, 10), NN.relu, NN.relu_deriv)
nn.add_layer(NN.Layer(10, 2), NN.softmax, None)
nn.set_loss(NN.cross_entropy, NN.cross_entropy_deriv)

# 训练参数
learning_rate = 0.001
epochs = 200000

def generate_dataset(num_samples):
    X = np.random.rand(num_samples, 2) * 2 - 1  # 生成 -1 到 1 之间的点
    Y = np.array([1 if x[0]**2 + x[1]**2 <= 1 else 0 for x in X])
    Y = np.eye(2)[Y]  # 转换为 one-hot 编码
    return X, Y

def train_update(epo, loss):
    print("Epochs:%d Loss:%f" % (epo, loss))


def accuracy_test(x_test, y_test, nn_test):
    # 使用训练好的模型对测试集进行前向传播
    test_output = nn_test.forward(x_test)
    # 转换 softmax 输出为类别预测
    test_predictions = np.argmax(test_output, axis=1)
    test_truth = np.argmax(Y_test, axis=1)
    # 计算准确率
    accuracy = np.mean(test_predictions == test_truth)
    print(f"Test Accuracy: {accuracy * 100:.2f}%")

# 数据生成和训练
X_train, Y_train = generate_dataset(256)
X_test, Y_test = generate_dataset(1000)

accuracy_test(X_test, Y_test, nn)

nn.train(X_train, Y_train, epochs, learning_rate, train_update)

accuracy_test(X_test, Y_test, nn)
import numpy as np
import matplotlib.pyplot as plt

"""
Perceptron
lineární klasifikátor
1. fáze učení - nastaví se váhy
2. fáze predice - skalární součin matice a dle výsledku klasifikuje
"""


class Perceptron:
    def __init__(self):
        print("Perceptron created")
        self.weights = [0]
        self.learning_rate = 1
        self.firstRun = 1

    # assign d = 1 if upper, d = -1 if lower (shoe vs t-shirt)
    def train(self, inp, d):
        localinp = inp.copy()
        localinp.insert(0, 1)
        if self.firstRun == 1:
            self.weights = np.zeros(len(localinp))
            self.firstRun = 0

        # predict what now perceptron thinks
        res = np.dot(localinp, self.weights)
        if res > 0:
            currentoutput = 1
        else:
            currentoutput = 0

        for j in range(len(self.weights)):
            # fixni prirustek - d je tady tvá skoková funkce
            self.weights[j] = self.weights[j] + self.learning_rate * (d - currentoutput) * localinp[j]

    def predict(self, inp):
        # simple dot product
        # input starts with 1
        inp.insert(0, 1)
        # skalarni soucin
        res = np.dot(inp, self.weights)
        if res > 0:
            return "upper"
        else:
            return "lower"


perceptron = Perceptron()

# POKUS 1
# i = 0
# datasetup = []
# datasetdown = []
# while i < 30:
#     randomTest = [np.random.uniform(-2, 2), np.random.uniform(-2, 2)]
#     if randomTest[0] + randomTest[1] > 1:
#         perceptron.train(randomTest, 1)
#     if randomTest[0] + randomTest[1] < 1:
#         perceptron.train(randomTest, -1)
#
#     dataset.append(randomTest)
#     i += 1

# POKUS 2
i = 0
datasetup = []
datasetdown = []
while i < 1000:
    randomTest = [np.random.uniform(-100, 100), np.random.uniform(-2, 2)]
    print(randomTest)
    if randomTest[1] > 1:
        perceptron.train(randomTest, 1)
        datasetup.append(randomTest)
    if randomTest[1] < 1:
        perceptron.train(randomTest, 0)
        datasetdown.append(randomTest)
    i = i + 1

# 100 linearly spaced numbers
x = np.linspace(-10000, 10000, 10000)

# the function

print("weights = " + str(perceptron.weights))
b = perceptron.weights[0]
w1 = perceptron.weights[1]
w2 = perceptron.weights[2]
y = -perceptron.weights[0] / perceptron.weights[2] - perceptron.weights[1] / perceptron.weights[2] * x
# y = ((-b/w2)/(b/w1))*x + (-b/w2)
# graph
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.spines['left'].set_position(('data', 0.0))
ax.spines['bottom'].set_position(('data', 0.0))
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.xlim(-10, 10)
plt.ylim(-10, 10)
plt.gca().set_aspect('equal', adjustable='box')
UP = list(zip(*datasetup))
DOWN = list(zip(*datasetdown))
plt.scatter(UP[0], UP[1], c='lightblue')
plt.scatter(DOWN[0], DOWN[1], c='red')
plt.plot(x, y)
plt.show()

perceptron.predict([0.26, 0.49])  # lower
perceptron.predict([0.9, 0.5])  # upper
perceptron.predict([0.06, 0.8])  # upper
perceptron.predict([0.8, 0.05])  # lower
perceptron.predict([-10, -10])  # lower
perceptron.predict([10, 10])  # upper
perceptron.predict([1, 1])  # upper
perceptron.predict([2, 2])  # upper

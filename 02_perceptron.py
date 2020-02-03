""" PERCEPTRON
    ----------
    Implementation of a single layer perceptron.
"""


# -------------------------------------------------------------------------------
# 0. IMPORT LIBRARIES
# -------------------------------------------------------------------------------


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as clr


# -------------------------------------------------------------------------------
# 1. DESIGN THE PERCEPTRON
# -------------------------------------------------------------------------------


class Perceptron:

    """ Perceptron classifier

    Parameters:
    ----------
    eta : float
        Learning rate (between 0.0 and 1.0)
    n_epoch : int
        Number of epochs.

    Attributed:
    ----------
    w : array, shape = [n_features, ]
        Weights after fitting, where n_features is the number of features.
    n_misclass : list
        Number of misclassifications (hence weight updates) in each epoch.
"""

    def __init__(self, eta=0.01, n_epoch=100):

        self.eta = eta
        self.n_epoch = n_epoch

    def fit(self, X, y):

        """ Fit training data

            Parameters:
            ----------
            X : array, shape = [n_samples, n_features]
                Training matrix, where n_samples is the number of samples and n_features is the number of features.
            y : array, shape = [n_samples, ]
                Target values.

            Returns:
            -------
            self : object
        """

        rgen = np.random.RandomState(seed=1)
        self.w = rgen.normal(loc=0.0, scale=0.01, size=1 + X.shape[1])
        self.n_misclass = []

        for epoch in range(self.n_epoch):

            misclass = 0

            for Xi, yi in zip(X, y):

                update = self.eta * (yi - self.predict(Xi))
                self.w[0] += update
                self.w[1:] += update * Xi
                misclass += int(update != 0.0)

            self.n_misclass.append(misclass)

        return self

    def net_input(self, X):

        """ Calculate the net input

            Parameters:
            ----------
            X : array, shape = [n_samples, n_features]
                Training matrix, where n_samples is the number of samples and n_features is the number of features.

            Returns:
            -------
            net_input : float
        """

        return self.w[0] + np.dot(X, self.w[1:])

    def predict(self, X):

        """ Return the class label after unit step function

            Parameters:
            ----------
            X : array, shape = [n_samples, n_features]
                Training matrix, where n_samples is the number of samples and n_features is the number of features.

            Returns:
            -------
            predict : int
        """

        return np.where(self.net_input(X) >= 0, 1, -1)


# -------------------------------------------------------------------------------
# 2. PREPARE THE DATA
# -------------------------------------------------------------------------------


# Import the dataset

data = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header=None)
print(data.head())


# Extract the class labels

y = data.iloc[:100, 4].to_numpy()
y = np.where(y == 'Iris-setosa', -1, 1)


# Extract the features

X = data.iloc[:100, [0,2]].to_numpy()


# Plot the features in a scatter plot

plt.figure()
plt.scatter(X[:50, 0], X[:50, 1], color='red', marker='+', label='Setosa')
plt.scatter(X[50:, 0], X[50:, 1], color='blue', marker='+', label='Versicolor')
plt.title('Scatter plot of the features')
plt.xlabel('Sepal length [cm]')
plt.ylabel('Petal length [cm]')
plt.legend(loc='upper left')
plt.savefig('images/02_perceptron/Scatter_plot_of_the_features.png')


# -------------------------------------------------------------------------------
# 3. TRAIN THE PERCEPTRON
# -------------------------------------------------------------------------------


# Initialize a perceptron object

ppn = Perceptron(eta=0.1, n_epoch=10)


# Learn from the data via the fit method

ppn.fit(X, y)


# Plot the number of misclassifications per epoch

plt.figure()
plt.plot(range(1, len(ppn.n_misclass) + 1), ppn.n_misclass, marker='o')
plt.title('Number of misclassifications per epoch')
plt.xlabel('Epoch')
plt.ylabel('Number of misclassifications')
plt.savefig('images/02_perceptron/Number_of_misclassifications_per_epoch.png')


# -------------------------------------------------------------------------------
# 4. PLOT THE DECISION BOUNDARY AND VERIFY THAT THE TRAINING SAMPLE IS CLASSIFIED CORRECTLY
# -------------------------------------------------------------------------------


# Function to plot the decision boundary

def plot_decision_regions(X, y, classifier, resolution=0.02):

    """ Create a colormap.

        Generate a matrix with two columns, where rows are all possible combinations of all numbers from min-1 to max+1 of the two series of
        features. The matrix with two columns is needed because the perceptron was trained on a matrix with such shape.

        Use the predict method of the chosen classifier (ppn) to predict the class corresponding to all the possible combinations of features
        generated in the above matrix. The predict method will use the weights learnt during the training phase: since the number of mis-
        classifications converged to zero in the training phase, we expect the perceptron to correctly classify all possible combinations of
        features.

        Reshape the vector of predictions as the X0_grid.

        Draw filled contours, where all possible combinations of features are associated to a Z, which is +1 or -1.

        To verify that the perceptron correctly classified all possible combinations of the features, plot the the original features in the
        scatter plot and verify that they fall inside the correct region.
    """

    colors = ('red', 'blue', 'green')
    cmap = clr.ListedColormap(colors[:len(np.unique(y))])

    X0_min, X0_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    X1_min, X1_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    X0_grid, X1_grid = np.meshgrid(np.arange(X0_min, X0_max, resolution), np.arange(X1_min, X1_max, resolution))
    X0X1_combs = np.array([X0_grid.ravel(), X1_grid.ravel()]).T

    Z = classifier.predict(X0X1_combs)

    Z = Z.reshape(X0_grid.shape)

    plt.figure()
    plt.contourf(X0_grid, X1_grid, Z, alpha=0.3, cmap=cmap)
    plt.xlim(X0_min, X0_max)
    plt.ylim(X1_min, X1_max)

    for pos, cl in enumerate(np.unique(y)):

        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1], alpha=0.8, color=colors[pos], marker='+', label=cl)


# Plot the decision region and the data

plot_decision_regions(X, y, classifier=ppn)
plt.title('Decision boundary and training sample')
plt.xlabel('Sepal length [cm]')
plt.ylabel('Petal length [cm]')
plt.legend(loc='upper left')
plt.savefig('images/02_perceptron/Decision_boundary_and_training_sample.png')


# -------------------------------------------------------------------------------
# 5. GENERAL
# -------------------------------------------------------------------------------


# Show plots

plt.show()

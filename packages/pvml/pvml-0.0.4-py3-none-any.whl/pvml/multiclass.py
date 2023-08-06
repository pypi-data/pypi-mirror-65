import numpy as np


#!begin1
def one_vs_rest_train(X, Y, train_fun):
    """Train a multi-class classifier using the one vs. rest strategy.

    Parameters
    ----------
    X : ndarray, shape (m, n)
        training features.
    Y : ndarray, shape (m,)
        training labels in the range 0, ..., (k - 1).
    train_fun : function that, given X and a set of binary labels, trains
        a binary classifier.  The function must return a tuple, where the
        last element is the list of loss values obtained during training,
        and all the others are the parameters of the trained classifier.

    Returns
    -------
    params : dict
        collection of (class, parameters) representing the binary classifiers.
    loss : ndarray, shape (steps,)
        average loss value after each training iteration.
    """
    k = Y.max() + 1
    m, n = X.shape
    loss = 0
    classifiers = {}
    for c in range(k):
        Ybin = (Y == c)
        result = train_fun(X, Ybin)
        classifiers[c] = result[:-1]
        loss = loss + result[-1]
    return classifiers, loss / k


def one_vs_rest_inference(X, inference_fun, params):
    """Multiclass prediction of the class labels.

    Parameters
    ----------
    X : ndarray, shape (m, n)
         input features (one row per feature vector).
    inference_fun : function that, given X and a tuple of parameters,
        returns prediction scores.
    params : dict
         parameters of the binary classifiers.

    Returns
    -------
    ndarray, shape (m,)
        predicted labels (one per feature vector) in the range 0...(k-1).
    ndarray, shape (m, k)
        classification scores.
    """
    k = len(params)
    scores = np.empty((X.shape[0], k))
    for c, p in params.items():
        scores[:, c] = inference_fun(X, *p)
    labels = np.argmax(scores, 1)
    return labels, scores
#!end1


#!begin2
def one_vs_one_train(X, Y, train_fun):
    """Train a multi-class classifier using the one vs. one strategy.

    Parameters
    ----------
    X : ndarray, shape (m, n)
        training features.
    Y : ndarray, shape (m,)
        training labels in the range 0, ..., (k - 1).
    train_fun : function that, given X and a set of binary labels, trains
        a binary classifier.  The function must return a tuple, where the
        last element is the list of loss values obtained during training,
        and all the others are the parameters of the trained classifier.

    Returns
    -------
    params : dict
        collection of ((pos, neg), parameters) representing the binary
        classifiers.
    loss : ndarray, shape (steps,)
        average loss value after each training iteration.
    """
    k = Y.max() + 1
    loss = 0
    params = {}
    # For each pair of classes...
    for pos in range(k):
        for neg in range(pos + 1, k):
            # Build a training subset
            subset = (np.logical_or(Y == pos, Y == neg)).nonzero()[0]
            Xbin = X[subset, :]
            Ybin = (Y[subset] == pos)
            # Train the classifier
            result = train_fun(Xbin, Ybin)
            params[(pos, neg)] = result[:-1]
            loss = loss + result[-1]
    return params, loss / len(params)


def one_vs_one_inference(X, inference_fun, params):
    """Multiclass prediction of the class labels.

    Parameters
    ----------
    X : ndarray, shape (m, n)
         input features (one row per feature vector).
    inference_fun : function that, given X and a tuple of parameters,
        returns binary labels.
    params : dict
         parameters of the binary classifiers.

    Returns
    -------
    ndarray, shape (m,)
        predicted labels (one per feature vector) in the range 0...(k-1).
    ndarray, shape (m, k)
        classification scores.
    """
    m = X.shape[0]
    k = 1 + max(max(classes) for classes in params)
    votes = np.zeros((m, k))
    for classes, p in params.items():
        pos, neg = classes
        Y = inference_fun(X, *p)
        votes[Y > 0, pos] += 1
        votes[Y <= 0, neg] += 1
    labels = np.argmax(votes, 1)
    return labels, votes
#!end2


if __name__ == "__main__":
    import demo
    import ksvm

    class Demo(demo.Demo):
        def binary_train(self, X, Y):
            alpha, b, loss = ksvm.ksvm_train(X, Y, self.args.kernel,
                                             self.args.kparam,
                                             self.args.lambda_,
                                             lr=self.args.lr,
                                             steps=self.args.steps)
            return (X, alpha, b, loss)

        def ova_inference(self, X, Xtrain, alpha, b):
            return ksvm.ksvm_inference(X, Xtrain, alpha, b,
                                       self.args.kernel,
                                       self.args.kparam)[1]

        def ovo_inference(self, X, Xtrain, alpha, b):
            return ksvm.ksvm_inference(X, Xtrain, alpha, b,
                                       self.args.kernel,
                                       self.args.kparam)[0]

        def train(self, X, Y):
            if self.args.strategy == "ova":
                self.params, loss = one_vs_rest_train(X, Y, self.binary_train)
            else:
                self.params, loss = one_vs_one_train(X, Y, self.binary_train)
            return loss

        def inference(self, X):
            if self.args.strategy == "ova":
                return one_vs_rest_inference(X, self.ova_inference,
                                             self.params)[0]
            else:
                return one_vs_one_inference(X, self.ovo_inference,
                                            self.params)[0]

    app = Demo()
    app.parser.add_argument("--strategy", choices=["ova", "ovo"],
                            default="ova", help="multiclass strategy")
    app.parser.add_argument("-k", "--kernel", choices=["rbf", "polynomial"],
                            default="rbf", help="Kernel function")
    app.parser.add_argument("-g", "--kparam", type=float, default=3,
                            help="Parameter of the kernel")
    app.run()

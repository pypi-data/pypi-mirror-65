import numpy as np
import svm


#!begin1
def one_vs_rest_svm_train(X, Y, lambda_, lr=1e-3, steps=1000):
    """Train a multi-class linear SVM using the one vs. rest strategy.

    Parameters
    ----------
    X : ndarray, shape (m, n)
        training features.
    Y : ndarray, shape (m,)
        training labels in the range 0, ..., (k - 1).
    lambda_ : float
        regularization coefficient.
    lr : float
        learning rate
    steps : int
        number of training steps

    Returns
    -------
    w : ndarray, shape (n, k)
        learned weights (one vector per class).
    b : ndarray, shape (k,)
        vector of biases.
    loss : ndarray, shape (steps,)
        loss value after each training iteration.
    """
    k = Y.max() + 1
    m, n = X.shape
    W = np.zeros((n, k))
    b = np.zeros(k)
    loss = np.empty((k, steps))
    for c in range(k):
        Ybin = (Y == c)
        Wbin, bbin, ls = svm.svm_train(X, Ybin, lambda_, lr=lr, steps=steps)
        W[:, c] = Wbin
        b[c] = bbin
        loss[c, :] = ls
    return W, b, loss.mean(0)


def one_vs_rest_svm_inference(X, W, b):
    """Multiclass linear SVM prediction of the class labels.

    Parameters
    ----------
    X : ndarray, shape (m, n)
         input features (one row per feature vector).
    w : ndarray, shape (n, k)
         weights (one vector per class).
    b : ndarray, shape (k,)
         vector of biases.

    Returns
    -------
    ndarray, shape (m,)
        predicted labels (one per feature vector) in the range 0...(k-1).
    ndarray, shape (m, k)
        classification scores.
    """
    logits = X @ W + b.T
    labels = np.argmax(logits, 1)
    return labels, logits
#!end1


#!begin2
def one_vs_one_svm_train(X, Y, lambda_, lr=1e-3, steps=1000):
    """Train a multi-class linear SVM using the one vs. one strategy.

    Parameters
    ----------
    X : ndarray, shape (m, n)
        training features.
    Y : ndarray, shape (m,)
        training labels in the range 0, ..., (k - 1).
    lambda_ : float
        regularization coefficient.
    lr : float
        learning rate
    steps : int
        number of training steps

    Returns
    -------
    w : ndarray, shape (n, k * (k - 1) // 2)
        learned weights (one vector per each pair of classes).
    b : ndarray, shape (k * (k - 1) // 2,)
        vector of biases.
    loss : ndarray, shape (steps,)
        loss value after each training iteration.
    """
    k = Y.max() + 1
    m, n = X.shape
    W = []
    b = []
    loss = []
    # For each pair of classes...
    for pos in range(k):
        for neg in range(pos + 1, k):
            # Build a training subset
            subset = (np.logical_or(Y == pos, Y == neg)).nonzero()[0]
            Xbin = X[subset, :]
            Ybin = (Y[subset] == pos)
            # Train the classifier
            Wbin, bbin, ls = svm.svm_train(Xbin, Ybin, lambda_, lr=lr,
                                           steps=steps)
            W.append(Wbin)
            b.append(bbin)
            loss.append(ls)
    # Convert lists into arrays
    W = np.vstack(W).T
    b = np.stack(b)
    loss = np.vstack(loss).mean(0)
    return W, b, loss


def one_vs_one_svm_inference(X, W, b):
    """Multiclass linear SVM prediction of the class labels.

    Parameters
    ----------
    X : ndarray, shape (m, n)
         input features (one row per feature vector).
    w : ndarray, shape (n, s)
         weights (one vector per pair of classes).
    b : ndarray, shape (s,)
         vector of biases.

    Returns
    -------
    ndarray, shape (m,)
        predicted labels (one per feature vector) in the range 0...(k-1).
    ndarray, shape (m, k)
        classification scores.
    """
    # 1) recover the number of classes from s = 1 + 2 + ... + k
    m = X.shape[0]
    s = b.size
    k = int(1 + np.sqrt(1 + 8 * s)) // 2
    votes = np.zeros((m, k))
    logits = X @ W + b.T
    bin_labels = (logits > 0)
    # For each pair of classes...
    j = 0
    for pos in range(k):
        for neg in range(pos + 1, k):
            votes[:, pos] += bin_labels[:, j]
            votes[:, neg] += (1 - bin_labels[:, j])
            j += 1
    labels = np.argmax(votes, 1)
    return labels, votes
#!end2


if __name__ == "__main__":
    import demo

    class Demo(demo.Demo):
        def train(self, X, Y):
            if self.args.strategy == "ova":
                w, b, loss = one_vs_rest_svm_train(X, Y,
                                                   self.args.lambda_,
                                                   lr=self.args.lr,
                                                   steps=self.args.steps)
            else:
                w, b, loss = one_vs_one_svm_train(X, Y,
                                                  self.args.lambda_,
                                                  lr=self.args.lr,
                                                  steps=self.args.steps)
            self.w = w
            self.b = b
            return loss

        def inference(self, X):
            if self.args.strategy == "ova":
                return one_vs_rest_svm_inference(X, self.w, self.b)[0]
            else:
                return one_vs_one_svm_inference(X, self.w, self.b)[0]

        def report(self, X, *args):
            super().report(X, *args)
            if X.shape[1] == 2 and self.args.draw_planes:
                for i in range(self.w.shape[1]):
                    demo.draw_linear_boundary(self.w[:, i], self.b[i],
                                              linestyle="--")

    demoapp = Demo()
    demoapp.parser.add_argument("--strategy", choices=["ova", "ovo"],
                                default="ova",
                                help="multiclass strategy")
    demoapp.parser.add_argument("--draw-planes", action="store_true",
                                help="draw hyperplanes")
    demoapp.run()

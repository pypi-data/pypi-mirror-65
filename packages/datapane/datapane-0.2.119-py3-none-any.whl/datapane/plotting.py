import typing as t

import matplotlib.pyplot as plt
import numpy as np
import sklearn

from .files import NPath, show


def precision_recall_curve(
    y_true: np.ndarray, proba: np.ndarray, file_name: t.Optional[NPath] = None
):
    """
    Draws a precision recall curve.

    Parameters
    ----------
    y_true : array, shape = [n_samples]
        True targets of binary classification in range {-1, 1} or {0, 1}.
    proba : array, shape = [n_samples]
        Probabilities for the positive class.
    file_name : NPath
        Name/path of the graph.
    """
    precision, recall, _ = sklearn.metrics.precision_recall_curve(y_true, proba)

    average_precision = sklearn.metrics.average_precision_score(y_true, proba)
    fig, ax = plt.subplots()
    ax.step(recall, precision, color="b", alpha=0.2, where="post")
    ax.fill_between(recall, precision, step="post", alpha=0.2, color="b")

    ax.xlabel("Recall")
    ax.ylabel("Precision")
    ax.ylim([0.0, 1.05])
    ax.xlim([0.0, 1.0])
    prop_positive = np.sum(y_true) / len(y_true)
    ax.plot([0, 1], [prop_positive, prop_positive], color="navy", lw=2, linestyle="--")
    ax.title("Precision-Recall curve: AP={0:0.3f}.".format(average_precision))

    show(fig, file_name)


def roc_curve(y_true: np.ndarray, proba: np.ndarray, file_name: t.Optional[NPath] = None):
    """
    Draws a ROC curve.

    Parameters
    ----------
    y_true : array, shape = [n_samples]
        True targets of binary classification in range {-1, 1} or {0, 1}.
    proba : array, shape = [n_samples]
        Probabilities for the positive class.
    file_name : NPath
        Name/path of the graph.
    """
    fpr, tpr, _ = sklearn.metrics.roc_curve(y_true, proba)
    roc_auc = sklearn.metrics.auc(fpr, tpr)

    fig, ax = plt.subplots()
    lw = 2
    ax.plot(fpr, tpr, color="darkorange", lw=lw, label="ROC curve (area = %0.3f)" % roc_auc)
    ax.plot([0, 1], [0, 1], color="navy", lw=lw, linestyle="--")
    ax.xlim([0.0, 1.0])
    ax.ylim([0.0, 1.05])
    ax.xlabel("False Positive Rate")
    ax.ylabel("True Positive Rate")
    ax.title("Receiver operating characteristic example")
    ax.legend(loc="lower right")

    show(fig, file_name)

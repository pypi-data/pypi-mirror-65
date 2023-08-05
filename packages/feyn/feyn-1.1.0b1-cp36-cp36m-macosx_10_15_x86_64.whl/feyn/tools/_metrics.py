import itertools

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix


def plot_confusion_matrix(y_true,
                          y_pred,
                          labels=None,
                          sample_weight=None,
                          title='Confusion matrix',
                          color_map=plt.cm.Blues):

    """ Plot a Confusion Matrix.

    Arguments:
        y_true {typing.Iterable} -- Expected values (Truth)
        y_pred {typing.Iterable} -- Estimated values (Guess form the Graph)

    Keyword Arguments:
        labels {typing.Iterable} -- List of labels to index the matrix (default: {None})
        sample_weight {typing.Iterable} -- Sample weights (default: {None})
        normalize {bool} -- Normalizes confusion matrix over the true (rows), predicted (columns) conditions or all the population. If None, confusion matrix will not be normalized. (default: {False})
        title {str} -- Title to show on top (default: {'Confusion matrix'})
        color_map {matplotlib.colors.LinearSegmentedColormap} -- Color map to use for the matrix (default: {plt.cm.Blues})

    Returns:
        [plot] -- matplotlib confusion matrix
    """

    if labels is None:
        labels = np.unique(y_true)

    cm = confusion_matrix(y_true, y_pred, labels, sample_weight)

    plt.title(title)
    tick_marks = range(len(labels))
    plt.xticks(tick_marks, labels, rotation=45)
    plt.yticks(tick_marks, labels)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], 'd'),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('Expected')
    plt.xlabel('Predicted')

    plt.imshow(cm, interpolation='nearest', cmap=color_map)
    plt.colorbar()
    plt.tight_layout()
    return plt.show()


def plot_regression_metrics(y_true, y_pred, title="Regression metrics"):
    """
    Plot metrics for a regression problem.
    The y-axis is the range of values in y_true and y_pred.
    The x-axis is all the samples, sorted in the order of the y_true.
    With this, you are able to see how much your prediction deviates
    from expected in the different prediction ranges.

    So, a good metric plot, would have the predicted line close and smooth
    around the predicted line.

    Normally you will see areas, where the predicted line jitter a lot scores worse
    against the test data there.


    Arguments:
        y_true {typing.Iterable} -- Expected values (Truth).
        y_pred {typing.Iterable} -- Estimated values (Guess form the Graph).

    Keyword Arguments:
        title {str} -- Title of the plot. (default: {"Regression metrics"})

    Raises:
        ValueError: When y_true and y_pred do not have same shape

    Returns:
        [type] -- [description]
    """
    if type(y_true).__name__ == "Series":
        y_true = y_true.values

    if type(y_pred).__name__ == "Series":
        y_pred = y_pred.values

    if (len(y_true) != len(y_pred)):
        raise ValueError('Size of expected and predicted are different!')
    
    sort_index = np.argsort(y_true)
    expected = y_true[sort_index]
    predicted = y_pred[sort_index]

    plt.title(title)
    plt.plot(expected, label='Expected')   
    plt.plot(predicted, label='Predicted')
    plt.xticks([])
    plt.legend()

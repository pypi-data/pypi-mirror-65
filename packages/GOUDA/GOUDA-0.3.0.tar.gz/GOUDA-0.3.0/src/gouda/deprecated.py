Add to ConfusionMatrix and remove

# Confusion Matrix utils
def underline(string):
    """Underline a string with ANSI escape characters"""
    return '\033[4m' + string + '\033[0m'


def get_specificities(confusion_matrix):
    """Return the specificity for each represented class in a 2D array as from :func:`~gouda.get_confusion_matrix`"""
    if confusion_matrix.ndim != 2:
        raise ValueError("Confusion matrix must be a 2D array")
    if confusion_matrix.shape[0] != confusion_matrix.shape[1]:
        raise ValueError("Confusion matrix must have the same height and width")
    tn = np.array([sum([confusion_matrix[j, :i].sum() + confusion_matrix[j, i + 1:].sum() for j in range(confusion_matrix.shape[0]) if j != i]) for i in range(confusion_matrix.shape[0])])
    fp = np.array([confusion_matrix[i, :].sum() - confusion_matrix[i, i].sum() for i in range(confusion_matrix.shape[0])])
    return tn / (tn + fp)


def get_sensitivities(confusion_matrix):
    """Return the sensitivity for each represented class in a 2D array as from :func:`~gouda.get_confusion_matrix`"""
    if confusion_matrix.ndim != 2:
        raise ValueError("Confusion matrix must be a 2D array")
    if confusion_matrix.shape[0] != confusion_matrix.shape[1]:
        raise ValueError("Confusion matrix must have the same height and width")
    return [confusion_matrix[i, i] / confusion_matrix[i, :].sum() if confusion_matrix[i, :].sum() > 0 else 0 for i in range(confusion_matrix.shape[0])]


def get_accuracy(confusion_matrix):
    """Return the accuracy from a 2D array as from :func:`~gouda.get_confusion_matrix`"""
    if confusion_matrix.ndim != 2:
        raise ValueError("Confusion matrix must be a 2D array")
    if confusion_matrix.shape[0] != confusion_matrix.shape[1]:
        raise ValueError("Confusion matrix must have the same height and width")
    return np.sum([confusion_matrix[i, i] for i in range(confusion_matrix.shape[0])]) / np.sum(confusion_matrix)


def get_binary_confusion_matrix(predictions, labels, threshold=0.5):
    """Get 2D array like a confusion matrix for 2-class predictions.

    Note
    ----
    * Predictions can be either boolean values or continuous probabilities
    * Rows represent expected class and columns represent predicted class
    """
    predictions = np.array(predictions)
    labels = np.array(labels)
    if predictions.ndim != 1 or labels.ndim != 1:
        raise ValueError("Predictions and labels must be lists or 1-dimensional arrays")
    if predictions.shape[0] != labels.shape[0]:
        raise ValueError("There must be an equal number of predictions and labels")
    if predictions.dtype != np.bool:
        rounded_pred = predictions > threshold
    else:
        rounded_pred = predictions
    output = np.zeros((2, 2), dtype=np.int)
    for i in range(labels.shape[0]):
        output[int(labels[i]), int(rounded_pred[i])] += 1
    return output


def get_confusion_matrix(predictions, labels, num_classes=None):
    """Get 2D array like a confusion matrix for multi-class predictions.

    Note
    ----
    * Predictions and labels will be treated as integer class labels and floats will be truncated.
    * Matrix is 0-indexed
    * Rows represent expected class and columns represent predicted class
    """
    predictions = np.array(predictions).astype(np.int)
    labels = np.array(labels).astype(np.int)
    if predictions.ndim != 1 or labels.ndim != 1:
        raise ValueError("Predictions and labels must be lists or 1-dimensional arrays")
    if predictions.shape[0] != labels.shape[0]:
        raise ValueError("There must be an equal number of predictions and labels")
    if num_classes is None:
        num_classes = labels.max() + 1
    confusion = np.zeros((num_classes, num_classes))
    for i in range(predictions.shape[0]):
        confusion[labels[i], predictions[i]] += 1
    return confusion


def print_confusion_matrix(confusion_matrix):
    """Format and print a 2D array like a confusion matrix as from :func:`~gouda.get_confusion_matrix`"""
    expected_string = u"\u2193" + " Expected"
    predicted_string = u"\u2192" + "  Predicted"
    leading_space = "            "
    confusion_string = "         "
    header_string = "".join(['|   {:1d}   '.format(i) for i in range(confusion_matrix.shape[1])])
    confusion_string += predicted_string + "\n" + expected_string + "  " + underline("        " + header_string + "| Sensitivity") + "\n"
    for i in range(confusion_matrix.shape[0]):
        correct = confusion_matrix[i, i]
        line_string = "    {:1d}   |"
        for j in range(confusion_matrix.shape[1]):
            if i == j:
                line_string += colorama.Fore.GREEN + "{:5d}  " + colorama.Style.RESET_ALL + "|"
            else:
                line_string += "{:5d}  |"
        line_string += "{:.5f}"
        line_string = line_string.format(i, *confusion_matrix[i], correct / confusion_matrix[i].sum())
        if i == confusion_matrix.shape[0] - 1:
            line_string = underline(line_string)
        confusion_string += leading_space + line_string + '\n'

    specificities = get_specificities(confusion_matrix)
    specificity_string = '        Specificity'
    for _ in range(confusion_matrix.shape[1]):
        specificity_string += ' |{:.4f}'
    confusion_string += (specificity_string + '\n').format(*specificities)
    confusion_string += "\nAccuracy: {:.4f}".format(get_accuracy(confusion_matrix))

    print(confusion_string)

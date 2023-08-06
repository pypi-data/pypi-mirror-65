import numpy as np
import warnings

def mean_bias_error(y_true, y_pred):
    #  This is wrong error function but to keep somewhat previous behavior.. 
    #  we convert it to squared_error.
    return np.mean(np.power((y_pred - y_true), 2))

def mean_absolute_error(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def mean_squared_error(y_true, y_pred):
    return np.mean(np.power((y_pred - y_true), 2))

def categorical_cross_entropy(y_true, y_pred):
    with warnings.catch_warnings():
        warnings.filterwarnings('error')
        try:
            errors = np.zeros_like(y_true)
            errors[y_true == 1] = -np.log10(y_pred[y_true == 1] + 1e-8)
            errors[y_true == 0] = -np.log10(1 - y_pred[y_true == 0] + 1e-8)
            return np.mean(errors)
        except Warning as w:
            print("Check output data. This error usually happens when you have non binary data as output.")
            raise w
            
def get_loss_function(loss_name):
    if type(loss_name).__name__ == "function":
        loss_name = loss_name.__name__
        
    if (loss_name == "mean_bias_error"):
        return mean_bias_error
    if (loss_name == "mean_absolute_error"):
        return mean_absolute_error
    if (loss_name == "mean_squared_error"):
        return mean_squared_error
    if (loss_name == "categorical_cross_entropy"):
        return categorical_cross_entropy

    raise ValueError("Unknown loss provided")
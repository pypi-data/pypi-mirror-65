import numpy as np


def resample_classes_from_dataframe(df, class_column, frac=1.0):
    import pandas as pd

    # is it a categorical column?
    if df[class_column].dtype not in [np.int, np.int16, np.int32, np.int64, np.int8, np.integer]:
        raise ValueError("Output column should be of types [np.int, np.int16, np.int32, np.int64, np.int8, np.integer, np.ca]")

    column = df[class_column]
    class_counts = column.value_counts().to_dict()

    majority_class_count = next(iter(class_counts.items()))[1]

    resampled_df = pd.DataFrame([], columns=df.columns)

    for _class in class_counts.items():
        _resampled_class = df[df[class_column] == _class[0]].sample(n = majority_class_count, replace=True)
        resampled_df = pd.concat([resampled_df, _resampled_class])

    return resampled_df.sample(frac=1.0)

def add_registers_from_dataframe(qlattice, df):
    registers = []
    for col in df.columns:
        if df[col].dtype == object:
            registers.append(qlattice.get_register(col, register_type="cat"))
        else:
            registers.append(qlattice.get_register(col, register_type="fixed"))
    
    return registers


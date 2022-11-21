import pandas as pd

import generate_dataset


def test_prepare_features():

    df0 = pd.DataFrame({"mean_power": [1, 2], "measures_number": [3, 4]})
    df1 = pd.DataFrame({"mean_power": [5, 6], "measures_number": [7, 8]})

    expected_df = pd.DataFrame(
        {
            "mean_power": [(1 * 3 + 5 * 7) / (3 + 7), (2 * 4 + 6 * 8) / (4 + 8)],
            "measures_number": [3 + 7, 4 + 8],
        }
    )
    actual_df = generate_dataset.combine_reduced_df(df0, df1)

    same = expected_df.equals(actual_df)
    assert same == True

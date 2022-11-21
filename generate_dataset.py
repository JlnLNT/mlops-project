import pandas as pd
from sklearn.model_selection import train_test_split

### This script generates the dataset for this project from the meteonet's raw data
def check_locations(df_s, tolerance=1e-2):
    station_list = df_s["number_sta"].unique()

    ## checking that all the stations contain only one location
    for station in station_list:
        lats = df_s[df_s["number_sta"] == station]["lat"].unique()
        lons = df_s[df_s["number_sta"] == station]["lon"].unique()

        lat_diff = max(abs(lats - lats[0]))
        lon_diff = max(abs(lons - lons[0]))

        if lat_diff > tolerance or lon_diff > tolerance:
            print(f"Careful, station {station} has moved during the recording period")
            print(lats)
            print(lons)


def create_reduced_df(df):
    def wind_power(ws):
        ## the power of a windmill is proportionnal to the wind veolicity to the power of 3
        return ws**3

    df["wind_power"] = df["ff"].apply(wind_power)
    mean_power = df.groupby("number_sta").mean(numeric_only=True)["wind_power"]
    measures_number = df.set_index("number_sta").notnull().groupby(level=0).sum()["ff"]
    lats = df.groupby("number_sta").mean(numeric_only=True)["lat"]
    lons = df.groupby("number_sta").mean(numeric_only=True)["lon"]
    height_stas = df.groupby("number_sta").mean(numeric_only=True)["height_sta"]

    frame = {
        "lat": lats,
        "lon": lons,
        "height_sta": height_stas,
        "mean_power": mean_power,
        "measures_number": measures_number,
    }
    df_reduced = pd.DataFrame(frame)

    return df_reduced


def combine_reduced_df(df0, df1):
    df_j = df0.join(df1, how="outer", rsuffix="1")

    if len(df0) > 0:
        mean_power = (
            df_j["mean_power"] * df_j["measures_number"]
            + df_j["mean_power1"] * df_j["measures_number1"]
        ) / (df_j["measures_number"] + df_j["measures_number1"])
        new_counts = df_j["measures_number"] + df_j["measures_number1"]

        df_j["mean_power"] = mean_power
        df_j["measures_number"] = new_counts

        for col in df_j.columns:
            if col[-1] == "1":

                df_j.drop(col, axis=1, inplace=True)

    return df_j


def process_data(df, chunk):
    check_locations(chunk)
    r_chunk = create_reduced_df(chunk)
    df = combine_reduced_df(df, r_chunk)

    return df


if __name__ == "__main__":

    YEARS = [2016, 2017]
    PATH_SAVE = "data/dataset.csv"
    df = pd.DataFrame()
    for year in YEARS:

        FILENAME = f"raw_data_meteonet/SE{year}.csv"

        CHUNKSIZE = 10**6
        for chunk in pd.read_csv(FILENAME, chunksize=CHUNKSIZE):
            df = process_data(df, chunk)

    df.to_csv(PATH_SAVE)

    ## generating test and train dataset

    df = df[df["mean_power"] < 500]  ## removing the outliers

    TEST_SIZE = 0.3
    df_train, df_test = train_test_split(df, test_size=TEST_SIZE, random_state=123)

    PATH_TRAIN = "data/train.csv"
    PATH_TEST = "data/test.csv"
    df_train.to_csv(PATH_TRAIN)
    df_test.to_csv(PATH_TEST)

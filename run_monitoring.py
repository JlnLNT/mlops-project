from generate_dataset import  
    YEARS = [2016, 2017, 2018]
    PATH_SAVE = "data/dataset.csv"
    df = pd.DataFrame()
    for year in YEARS:
                
        FILENAME = f"raw_data_meteonet/SE{year}.csv"
        
        CHUNKSIZE = 10 ** 6
        for chunk in pd.read_csv(FILENAME, chunksize=CHUNKSIZE):
            df = process_data(df, chunk)
        
    df.to_csv(PATH_SAVE)
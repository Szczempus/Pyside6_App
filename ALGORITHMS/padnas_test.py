import pandas as pd



if __name__ == "__main__":

    path = r"C:\anaconda3\envs\groot2.0\Lib\site-packages\deepforest\data\example.csv"

    df = pd.read_csv(path)
    print(df)

    for frame in df:
        print(frame["image_path"])

    pass
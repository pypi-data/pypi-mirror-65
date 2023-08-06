import pandas as pd
import sys
sys.path.append('../')
from app.src import train, transform

if __name__ == '__main__':
    data = (
        pd.read_csv('bank-additional-full.csv', delimiter=";")
            .rename(columns=str.lower)
    )

    data = transform(data)
    train(data)

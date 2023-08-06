import pandas as pd
import numpy as np
import os


class CovidDataset:
    def GetCovidRawDataFrame(self):
        basePath = os.path.dirname(os.path.abspath(__file__))
        # Load the csv file in a pandas dataframe
        columnHeaders = [
            "Region",
            "Location",
            "Lat",
            "Long",
            "Date",
            "Confirmed",
            "Deaths",
            "Recovered",
        ]
        columnTypes = {
            "Region": "str",
            "Location": "str",
            "Lat": "float",
            "Long": "float",
            "Date": "str",
            "Confirmed": "int64",
            "Deaths": "int64",
            "Recovered": "int64",
        }
        parse_dates = ["Date"]
        dataFilePath = basePath + "\\data\\covid_19_clean_complete.csv"
        print(dataFilePath)
        df = pd.read_csv(
            dataFilePath,
            sep=",",
            skiprows=1,
            names=columnHeaders,
            # dtype=columnTypes,
            parse_dates=parse_dates,
        )
        return df

    def GetCovidNpArray(self):
        processedDf = (
            self.GetCovidRawDataFrame()
            .groupby(["Location", "Date"], as_index=False)[
                "Confirmed", "Deaths", "Recovered"
            ]
            .sum()
        )
        return processedDf.to_numpy()


# Test above code

# covidData = CovidDataset()
# print(covidData.GetCovidNpArray())
# print(covidData.GetCovidRawDataFrame())

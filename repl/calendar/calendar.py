import pandas as pd
import json

data_frame = pd.read_excel("./111_Schedule.xlsx", sheet_name = None, usecols = "A, B, K")

data = {}

year_to_num = {
    "一一0年": "2021",
    "一ㄧ一年": "2022",
    "一一一年": "2022",
    "一ㄧ二年": "2023",
}

month_to_num = {
    "一月": "01",
    "二月": "02",
    "三月": "03",
    "四月": "04",
    "五月": "05",
    "六月": "06",
    "七月": "07",
    "八月": "08",
    "九月": "09",
    "十月": "10",
    "十一月": "11",
    "十二月": "12",
}

for frame in data_frame.keys():
    year = ""
    month = ""
    date = ""
    for i in range(len(data_frame[frame])):
        row = data_frame[frame].iloc[i].values
        if str(row[0]) != "nan":
            year = year_to_num[str(row[0]).replace("\n", "")]
            month = month_to_num[str(row[1]).replace("\n", "")]

        elif str(row[1]) != "nan":
            month = month_to_num[str(row[1]).replace("\n", "")]
            
        if str(row[2]) != "nan":
            date = str(row[2]).replace("\n", "").replace("（", "\n（").replace(" ", "")[1:]
            data[year + month] = date
            
with open('data.json', 'a+', encoding = "utf8") as jsonfile:
    json.dump(data, jsonfile, ensure_ascii = False, indent = 4)
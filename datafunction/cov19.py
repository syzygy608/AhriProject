from datetime import datetime, timezone, timedelta
import requests
from bs4 import BeautifulSoup

index_to_title = {
    0: "日期",
    1: "確診人數",
    4: "備註"
}
tz = timezone(timedelta(hours = +8))

def getInfo():
    response = requests.get("https://www.ccu.edu.tw/2019-nCoV_caseInfo.php")
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    tr = table.find_all("tr", limit = 5)

    for i in range(2, 5):
        td = tr[i].find_all("td")
        for j in [0, 1, 4]:
            href = td[j].find("a", href = True)
            if href != None:
                print(f"{index_to_title[j]} [相關連結](https://www.ccu.edu.tw/{href['href']})")
            else:
                text = (td[j].text).replace("*", "x")
                print(f"{index_to_title[j]} [{text}]")   

getInfo()
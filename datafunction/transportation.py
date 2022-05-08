from selenium import webdriver
from bs4 import BeautifulSoup
import time


def busID_status(busID):

    driverPATH = './chromedriver' # driver 路徑
    options = webdriver.ChromeOptions() # 使用chromedriver
    # options = webdriver.EdgeOptions() # 使用edgedriver
    # options.use_chromium = True
    options.add_argument('headless')
    options.add_argument("disable-gpu")

    edge = webdriver.Chrome(driverPATH, options = options)
    edge.get(f"https://www.taiwanbus.tw/eBUSPage/Query/QueryResult.aspx?rno={busID}",)
    # 路線編號
    # 7309: rno=73090
    #  106: rno=07460
    # 7306: rno=73060

    time.sleep(1)
    soup = BeautifulSoup(edge.page_source, 'html.parser')
    stop = soup.find_all("div", {"class": "bus-route__stop"})

    stations = []
    for tag in stop:
        name = tag.find('a', {"class": "bus-route__stop-name"})
        status = tag.find('div', {"class": "bus-route__stop-status"})
        stationdir = {"name": name.text, "time": status.text}
        stations.append(stationdir)

    return stations #stations["name"]: 站名,  stations["time"]: 進站時間

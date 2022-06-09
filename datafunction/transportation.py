from selenium import webdriver
from bs4 import BeautifulSoup
import time

from datetime import datetime,timezone,timedelta

def busID_status(ID, direction):

    driverPATH = './chromedriver' # driver 路徑
    options = webdriver.ChromeOptions() # 使用chromedriver
    options.add_argument('headless')
    options.add_argument("disable-gpu")

    edge = webdriver.Chrome(driverPATH, options = options)
    edge.get(f"https://yunbus.tw/lite/route.php?id=THB{ID}")
    # 路線編號
    # 7309: 73090
    # 7306: 73060
    time.sleep(1)
    soup = BeautifulSoup(edge.page_source, 'html.parser')
    if direction == 0:
        direction = "go"
    else:
        direction = "bk"
    fonts = soup.find("table", {"id": direction}).find_all("font")

    stations = []
    type = 0
    status = ""
    for i in range(len(fonts)):
        if not i:
            continue
        if fonts[i].string:
            if type == 0:
                type += 1
                status = fonts[i].string
            else:
                type = 0
                name = fonts[i].string
                stationdir = {"name": name, "time": status}
                stations.append(stationdir)

    return stations #stations["name"]: 站名,  stations["time"]: 進站時間

data = busID_status("73060", 1)


def train_station(stationID, direction): # stationID= 0: 民雄,  1: 嘉義. direction= 0:順行, 1:逆行
    stationPATH = ["4060-%E6%B0%91%E9%9B%84", "4080-%E5%98%89%E7%BE%A9"]

    # 現在時間
    dt = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    dt = dt.strftime("%H:%M") # 將時間轉換為 string

    driverPATH = './chromedriver' # driver 路徑
    options = webdriver.ChromeOptions() # 使用chromedriver

    options.add_argument('headless')
    options.add_argument("disable-gpu")

    edge = webdriver.Chrome(driverPATH, options = options)
    edge.get(f"https://tip.railway.gov.tw/tra-tip-web/tip/tip001/tip112/querybystationblank?rideDate=2022/05/08&station={stationPATH[stationID]}")
    time.sleep(1)
    soup = BeautifulSoup(edge.page_source, 'html.parser')
    context = soup.find_all("tbody")

    trains = []
    trs = context[direction].find_all('tr')
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds):
            name = tds[1].find('a')
            way = []
            name = name.text
            for c in tds[1].find_all('span'):
                way.append(c.text)
            way = ''.join(way)
            arriveTime = tds[2].text
            if arriveTime > dt: # 儲存還未經過的車
                train = {"name": name,
                         "way": way,
                         "time": arriveTime
                         }
                trains.append(train)

    return trains #trians["name"]: name, trians["way"]: 出發->抵達, trians["time"]: 到站時間
# print(train_station(0, 0))

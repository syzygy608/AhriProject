import time
from wsgiref.handlers import format_date_time
from datetime import datetime,timezone,timedelta
from hashlib import sha1
import hmac
import base64
import requests
import json

class Auth():
    def __init__(self):
        with open("transAPI.json", newline='') as f:
            data = json.load(f)
        self.app_id = data['app_id']
        self.app_key = data['app_key']

    def get_auth_header(self):
        xdate = format_date_time(time.mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), (f'x-date: {xdate}').encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()
        authorization = (f'hmac username="{self.app_id}", algorithm="hmac-sha1"' +
                         f', headers="x-date", signature="{signature}"')
        return {
            'Authorization': authorization,
            'x-date': xdate,
            'Accept-Encoding': 'gzip'
        }

#取得指定當日的站別時刻表資料
def train_station(stationID, direction):# stationID= 0: 民雄,  1: 嘉義. direction= 0:順行, 1:逆行
    stationPATH = ["4060", "4080"]
    auth = Auth()
    dtime = datetime.utcnow().replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=8))) # 轉換時區 -> 東八區
    dt = dtime.strftime("%Y-%m-%d") # 將時間轉換為 string
    url = f'https://ptx.transportdata.tw/MOTC/v2/Rail/TRA/DailyTimetable/Station/{stationPATH[stationID]}/{dt}?&%24format=JSON'
    response = requests.get(url, headers=auth.get_auth_header())

    dt = dtime.strftime("%H:%M") # 將時間轉換為 string
    data = response.json()
    trains = []
    for train in data:
        if train['Direction'] == direction and train['ArrivalTime'] > dt: # 指定方向，未經過得車
            t = {"type": train['TrainTypeName']['Zh_tw'][:2], # 車種
                 "id": train['TrainNo'], # 車號
                 "way": f"{train['StationName']['Zh_tw']}->{train['EndingStationName']['Zh_tw']}", # 方向
                 "time": train["ArrivalTime"] # 抵達時間
                 }
            trains.append(t)
    return trains

# def busID_status(ID, dirction):
#     busIDs = {"7309": "73090", "106": "07460", "7306": "73060"}
#
#     driverPATH = './chromedriver' # driver 路徑
#     options = webdriver.ChromeOptions() # 使用chromedriver
#     options.add_argument('headless')
#     options.add_argument("disable-gpu")
#
#     edge = webdriver.Chrome(driverPATH, options = options)
#     edge.get(f"https://www.taiwanbus.tw/eBUSPage/Query/QueryResult.aspx?rno={busIDs[ID]}")
#     # 路線編號
#     # 7309: rno=73090
#     #  106: rno=07460
#     # 7306: rno=73060
#
#     time.sleep(1)
#     soup = BeautifulSoup(edge.page_source, 'html.parser')
#     stop = soup.find_all("div", {"class": "bus-route__stop"})
#
#     stations = []
#     for tag in stop:
#         name = tag.find('a', {"class": "bus-route__stop-name"})
#         status = tag.find('div', {"class": "bus-route__stop-status"})
#         stationdir = {"name": name.text, "time": status.text}
#         stations.append(stationdir)
#
#     return stations #stations["name"]: 站名,  stations["time"]: 進站時間
#
# # print(busID_status("106"))

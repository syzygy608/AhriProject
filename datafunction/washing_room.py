from bs4 import BeautifulSoup
from selenium import webdriver
import time

def get_washing_info(place):
    options = webdriver.ChromeOptions() # 使用chromedriver
    options.add_argument('headless') # 隱藏視窗
    options.add_argument("disable-gpu")
    options.add_argument('blink-settings=imagesEnabled=false')
    edge = webdriver.Chrome('./chromedriver', options = options)
    edge.get(f"http://monitor.isesa.com.tw/monitor/?code={place}",)
    time.sleep(1)
    soup = BeautifulSoup(edge.page_source, 'html.parser')
    trs = soup.find("tbody").find_all("tr")
    cnt = [
        {"working": 0, "finish": 0, "space": 0},
        {"working": 0, "finish": 0, "space": 0}
    ]
    for tr in trs:
        tds = tr.find_all("td")
        if "W" in tds[1].text:
            if "運轉中" in tds[2].text:
                cnt[0]["working"] += 1
            elif "運轉結束" in tds[2].text:
                cnt[0]["finish"] += 1
            elif "空機" in tds[2].text:
                cnt[0]["space"] += 1
        else:
            if "運轉中" in tds[2].text:
                cnt[1]["working"] += 1
            elif "運轉結束" in tds[2].text:
                cnt[1]["finish"] += 1
            elif "空機" in tds[2].text:
                cnt[1]["space"] += 1
    return cnt

get_washing_info("ehuYvg")


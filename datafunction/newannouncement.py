import requests
import webbrowser
from bs4 import BeautifulSoup

def get_data(): # 取得最新資訊 type: list
    url = "https://www.ccu.edu.tw/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    context = soup.find(id='bulletin_feature').find_all(title="(另開新視窗)")
    news = []
    for s in context:
        t = []
        link = url + s['href'].split('/')[1].split(" ")[0]
        t.append(s.string)
        t.append(link)
        news.append(t)
    t = []
    t.append("更多")
    t.append("https://www.ccu.edu.tw/bullentin_list.php?id=1")
    news.append(t)
    return news #news[0]: 標題, news[1]:連結

def click(url): #開啟文章 (開啟瀏覽器)
    webbrowser.open_new_tab(url)

a = get_data()
print(a)
click(a[0][1])

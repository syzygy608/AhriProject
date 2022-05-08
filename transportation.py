from selenium import webdriver


driverPATH = './chromedriver'
options = webdriver.ChromeOptions()
# options = webdriver.EdgeOptions()
# options.use_chromium = True
options.add_argument('headless')
options.add_argument("disable-gpu")

edge = webdriver.Chrome(driverPATH, options = options)
# edge.get(f"http://monitor.isesa.com.tw/monitor/?code={place}",)
# time.sleep(1)
# soup = BeautifulSoup(edge.page_source, 'html.parser')
# success = soup.find_all("span", "label label-success glyphicon glyphicon-ok")
# using = soup.find_all("span", "label label-primary")
# print(using)

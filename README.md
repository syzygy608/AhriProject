# Ahri Bot
The Discord bot of information assistant for CCU using nextcord
Program Design (II) Final Project

## Local Development Steps
1. Creating Discord bot following this website [links here](https://docs.nextcord.dev/en/stable/discord.html)
2. Sign up for Weather API in this website [links here](https://opendata.cwb.gov.tw/index)
3. Sign up for Bus API in this website [links here](https://ptx.transportdata.tw/MOTC/)
4. Download webdriver for web crawler (we use chrome in this project, you can modify the code to use other browsers)
5. Add your token in step 1, 2 and 3 to env.sample and rename the file to .env
6. Run `pip install -r requirements.txt` before `python main.py`

## Package
1. Discord
    - nextcord

2. Web crawler
    - BeautifulSoup
    - requests
    - Selenium

3. Trans API
    - hashlib
    - base64

4. Calendar
    - pandas
    - openpyxl

5. Others
    - time
    - json
    - wsgiref.handlers
    - datetime
---

## Features
- weather
- useful link
- covid-19 info of CCU
- CCU news
- washing machine status
- Bus and train's info of CCU
- school calendar

## Commands
1. bot
    - 查看機器人相關介紹資訊
2. ping
    - 查看機器人延遲
3. user_info
    - 查看使用者帳號資訊
4. purge
    - 清除訊息
5. links
    - 查看常用連結
6. weather
    - 查看縣市之三天內天氣預報
7. cov19
    - 查看中正最新疫情資訊
8. news
    - 查看中正最新消息/公告
9. bus_info
    - 查看中正周邊公車資訊
10. train_info
    - 查看中正周邊火車資訊
11. calendar
    - 查看中正大學本月行事曆資訊
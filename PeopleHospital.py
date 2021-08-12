import time
from threading import Timer
from typing import List

from requests import Session, get


def get_session() -> Session:
    session = Session()
    session.headers.update(
        {
            "Host": "wx.nxrmyy.com",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63030522)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Cookie": "8aa09e8d7358040601736dc7b9d20013=null; 8aa09e8d6bb8d523016cb7a908ad00c6=2021-08-16; deptState=today; 8aa09e8d767144d501768deec0510027=today; JSESSIONID=AB49203DD4EA2D3034AF3B208BD5CEF9",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Referer": "http://wx.nxrmyy.com/nxrmyy/yygh/doctor?depId=8aa09e8d7358040601736dc7b9d20013&hoscode=3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"})

    return session


def getScheduleDoctor(session: Session, data: dict, date: List[str]):
    global i

    url = 'https://3030.ij120.zoenet.cn/api/reservation/getScheduleDoctor'
    res = session.post(url=url, data=data)

    for day in res.json()['data']['days']:
        # 遍历排班
        # print(time.asctime(time.localtime(time.time())), day, i)

        if day['workDate'] in date:
            if day['statusName'] == '预约已满':
                if i % 120 == 0:
                    msg = f"当前：{time.asctime(time.localtime(time.time()))}\n还没有{day['staffName']}的号，机器人已经为你抢了{i * 20}次，继续刷新中..."
                    get(url=f"{bot_url}?msg={msg}")
            else:
                msg = f"有空号啦，快去给挂上吧！\n当前：{time.ctime()}\n医生：{day['staffName']}\n号别：{day['registerTypeName']}\n时间：{day['display']}\n位置：{day['deptPosition']}\n状态：{day['statusName']}"
                get(url=f"{bot_url}?msg={msg}")


if __name__ == '__main__':
    bot_url = "https://push.bot.qw360.cn/room/eb375d10-f4c9-11eb-952c-5f0e0d85cd84"

    base_url = "https://wx.nxrmyy.com/nxrmyy"
    url = f"{base_url}/yygh/schedule?hoscode=3&depId=8aa09e8d7358040601736dc7b9d20013&docId=8aa0036463fda420163fda4310e01m4&hoscode=3 "

    url_select_hospital = f"{base_url}/chose?operate=yygh"


    url_hospital = f"{base_url}/yygh/department?hoscode=3&actFlag=1&hosArea=rm003&hosDistrictCode=3"
    s = get_session()
    r = s.get(
        url_select_hospital
    )

    r = s.get(
        url_hospital
    )
    print(r)

import time
from threading import Timer
from typing import List

from requests import Session, get


def get_session() -> Session:
    session = Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        })

    session.get(
        url='https://3030.ij120.zoenet.cn/org/orgIndexWX?orgCode=YCSFYBJY&appCode=AJ120_YCSFYBJY_WX&openId=oTKo6xMfX-w5qVACPRxeOZ4glJ20&token=aj11a736e24448988ce24790bbed6ffa&cardId=c94522593d36423cbf93ce5bbce71907&cardNo=640106202009103312&idCardId=640106202009103312&patientId=ae1a215a2cee99758349d653222b5884')

    return session


def getScheduleDoctor(session: Session, data: dict,date:List[str]):
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

    s = get_session()

    data_zjh = {
        "deptCode": "33902",
        "doctor": "张俊华/281",
        "doctorName": "张俊华",
        "orgId": ""
    }

    date_zjh = [
        "2021-08-07 00:00:00",
        # "2021-08-09 00:00:00",
    ]

    get(url=f"{bot_url}?msg=开始给壮壮挂{date_zjh}{data_zjh['doctorName']}的号\n避免打扰，接下来每小时提醒一次，持续监控号源中...")

    i = 17000
    while True:
        i += 1
        Timer(0.1, getScheduleDoctor, args=(s, data_zjh,date_zjh)).run()
        time.sleep(30)
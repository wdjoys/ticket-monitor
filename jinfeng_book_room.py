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

    return session


def getScheduleDoctor(session: Session, ):
    global date_old

    url = 'https://culture.chaoxing.com/api/appointment/read?id=403'

    try:
        res = session.get(url=url, ).json()
        date_now = res['data']['days']
    except BaseException:
        return



    if not date_old == date_now:

        if len(date_old) == 0:
            date_old = date_now
            return

        msg = f"@张彦青\n悦书房预约提醒！\n"

        if not date_old[0]['label'] == date_now[0]['label']:
            msg += f"已经开放了{date_now[-1]['date']}的预约！"

        else:
            msg += "预约人数变动\n"
            for i, day in enumerate(date_now):
                msg += f"{'-'*8}\n变动时间：{day['date']},{day['week']}\n"
                for j, d in enumerate(day['data']):
                    if not d['now'] == date_old[i][['data']][j]['now']:
                        msg += f"上午\n变动前：{date_old[i][['data']][j]['now']}人\n变动后：{d['now']}人"
        date_old = date_now
        get(url=f"{bot_url}?msg={msg}")


        # date_list = date_now
        #
        # date_ = date_now[-1]['date']
        # max_ = date_now[-1]['data'][0]['max']
        # now = date_now[-1]['data'][0]['now']
        # msg = f'@张彦青\n悦书房预约提醒！\n可约日期：{date_}\n最大可约：{max_} 人\n当前已约：{now} 人'
        # get(url=f"{bot_url}?msg={msg}")
if __name__ == '__main__':

    # bot_url = "https://push.bot.qw360.cn/room/eb375d10-f4c9-11eb-952c-5f0e0d85cd84"
    bot_url = " https://push.bot.qw360.cn/send/5d56b7d0-e9ec-11eb-bcea-e767e07f0bdc"

    s = get_session()

    date_old = []

    i = 0
    while True:
        i += 1
        print(i)
        getScheduleDoctor(session=s)
        time.sleep(30)

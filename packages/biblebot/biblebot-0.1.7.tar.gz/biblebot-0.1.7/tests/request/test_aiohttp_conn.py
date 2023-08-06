import asyncio
from dataclasses import field, asdict

from http.cookies import SimpleCookie

from biblebot.reqeust.aiohttp_conn import *


async def main():
    data = {"Txt_1": "ramming125", "Txt_2": "gksrlghd123", "use_type": "3"}
    resp = await Request.get(
        "https://www.cultizm.com/kor/denim/jeans/7821/a.p.c.-petit-new-standard-indigo-red-selvage-14.5oz",
        # body=data,
        verify=False,
        allow_redirects=False,
        timeout=30.0,
    )
    print(resp.text)
    print(resp.headers)
    cookies = resp.cookies

    resp = await Request.get(
        "http://kbuis.bible.ac.kr/SchoolRegMng/SR020.aspx", cookies=cookies
    )


asyncio.run(main())

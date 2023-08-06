import asyncio
from urllib.parse import quote
from biblebot.reqeust.requests_conn import *


async def main():
    data = {"Txt_1": "ramming125", "Txt_2": "gksrlghd123", "use_type": "2"}
    resp = await Request.post(
        "https://kbuis.bible.ac.kr/ble_login2.aspx",
        body=data,
        verify=False,
        allow_redirects=False,
        timeout=20.0,
    )
    print(resp.text)
    print(resp.headers)
    cookies = resp.cookies
    print(cookies)

    resp = await Request.get(
        "http://kbuis.bible.ac.kr/SchoolRegMng/SR020.aspx", cookies=cookies
    )
    print(resp.text)


asyncio.run(main())

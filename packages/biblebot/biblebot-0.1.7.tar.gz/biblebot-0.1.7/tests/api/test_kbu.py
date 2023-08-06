import asyncio
import datetime

from urllib.parse import quote

from biblebot.api.kbu import *


def encode_kbustyle(str):
    return quote(str).replace("%20", "+")


async def test_main_notice():
    response = await MainNotice.fetch()
    assert response.status == 200

    result = MainNotice.parse(response)
    print(result)
    assert result.meta["page"] == 1
    assert result.meta["keyword"] is None
    assert len(result.data["notice"]) == 20

    response = await MainNotice.fetch(page="2")
    assert response.status == 200

    result = MainNotice.parse(response)
    assert result.meta["page"] == 2
    assert result.meta["keyword"] is None
    assert len(result.data["notice"]) == 20

    keyword = "성서봇"
    encoded_keyword = quote(keyword)
    response = await MainNotice.fetch(page="1", search_keyword=keyword)
    assert response.status == 200

    result = MainNotice.parse(response)
    assert result.meta["page"] == 1
    assert result.meta["keyword"] == keyword
    assert len(result.data["notice"]) > 0
    assert encoded_keyword == result.link[-len(encoded_keyword) :]


async def test_scholarship_notice():
    response = await ScholarshipNotice.fetch()
    assert response.status == 200

    result = ScholarshipNotice.parse(response)
    assert result.meta["page"] == 1
    assert result.meta["keyword"] is None
    assert len(result.data["notice"]) == 20

    response = await ScholarshipNotice.fetch(page="2")
    assert response.status == 200

    result = ScholarshipNotice.parse(response)
    assert result.meta["page"] == 2
    assert result.meta["keyword"] is None
    assert len(result.data["notice"]) == 20

    keyword = '"푸른등대 삼성SOS장학사업 신규 장학생 선발 공고"'
    encoded_keyword = encode_kbustyle(keyword)

    response = await ScholarshipNotice.fetch(page="1", search_keyword=keyword)
    assert response.status == 200

    result = ScholarshipNotice.parse(response)
    assert result.meta["page"] == 1
    assert result.meta["keyword"] == keyword
    assert len(result.data["notice"]) > 0
    assert encoded_keyword == result.link[-len(encoded_keyword) :]


async def test_illip_notice():
    response = await IllipNotice.fetch()
    assert response.status == 200

    result = IllipNotice.parse(response)
    assert result.meta["page"] == 1
    assert result.meta["keyword"] is None
    assert len(result.data["notice"]) == 20

    response = await IllipNotice.fetch(page="2")
    assert response.status == 200

    result = IllipNotice.parse(response)
    assert result.meta["page"] == 2
    assert result.meta["keyword"] is None
    assert len(result.data["notice"]) == 20

    keyword = '"신앙훈련 공지"'
    encoded_keyword = encode_kbustyle(keyword)
    response = await IllipNotice.fetch(page="1", search_keyword=keyword)
    assert response.status == 200

    result = IllipNotice.parse(response)
    assert result.meta["page"] == 1
    assert result.meta["keyword"] == keyword
    assert len(result.data["notice"]) > 0
    assert encoded_keyword == result.link[-len(encoded_keyword) :]


async def test_notice_article():
    url = "https://www.bible.ac.kr/ko/life/notice/view/34114?p=1"
    response = await NoticeArticle.fetch(url)
    assert response.status == 200
    result = NoticeArticle.parse(response)
    assert result.title == "[학사] 2020학년도 1학기 개강 연기 안내"
    assert result.author == "김병수"
    assert result.date == datetime.datetime(2020, 2, 21, 9, 27)
    print(result)
    return result


async def main():
    await test_main_notice()
    await test_scholarship_notice()
    await test_illip_notice()
    # await test_notice_article()


asyncio.run(main())

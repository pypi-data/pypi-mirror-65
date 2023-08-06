import asyncio

from biblebot.api.intranet import *
from biblebot.api.base import ErrorData, ResourceData


async def test_login(user_id, user_pw):
    # 비밀번호 틀린 경우
    response = await Login.fetch(user_id, user_pw + "123")
    assert response.status == 200
    assert response.cookies
    result = Login.parse(response)
    assert isinstance(result, ErrorData)
    assert result.error["title"] == "비밀번호가 일치하지 않습니다."

    # 아이디가 다른 경우
    response = await Login.fetch(user_id + "1a2b3c", user_pw)
    assert response.status == 200
    assert response.cookies
    result = Login.parse(response)
    assert isinstance(result, ErrorData)
    assert result.error["title"] == "존재하지 않는 회원ID 입니다."

    # 정상 로그인
    response = await Login.fetch(user_id, user_pw)
    assert response.status == 302
    assert response.cookies
    result = Login.parse(response)
    assert isinstance(result, ResourceData)
    assert result.data["cookies"]
    assert result.data["iat"]

    return response


async def test_student_photo(cookies, sid):
    # 학번이 존재하지 않을 경우
    response = await StudentPhoto.fetch(cookies, "201509021")
    assert response.status == 200

    result = StudentPhoto.parse(response)
    assert isinstance(result, ErrorData)
    print(result)

    # 학번이 존재할 경우
    response = await StudentPhoto.fetch(cookies, sid)
    assert response.status == 200

    result = StudentPhoto.parse(response)
    assert isinstance(result, ResourceData)
    assert len(result.data["raw_image"]) > 100
    print(result)


async def test_chapel(cookies, semesters):
    for semester in semesters:
        response = await Chapel.fetch(cookies, semester=semester)
        assert response.status == 200
        result = Chapel.parse(response)
        assert isinstance(result, ResourceData)
        if semester:
            assert result.meta["selected"] == semester
        print(semester, result)


async def test_timetable(cookies, semesters):
    for semester in semesters:
        response = await Timetable.fetch(cookies, semester=semester)
        assert response.status == 200
        result = Timetable.parse(response)
        assert isinstance(result, ResourceData)
        if semester:
            assert result.meta["selected"] == semester
        print(semester, result)


async def test_course(cookies, semesters):
    for semester in semesters:
        response = await Course.fetch(cookies, semester=semester)
        assert response.status == 200
        result = Course.parse(response)
        assert isinstance(result, ResourceData)
        if semester:
            assert result.meta["selected"] == semester

        print(semester, result)


async def test_invalid_cookies():
    invalid_cookies = {"ASP.NET_SessionId": "hello"}
    response = await StudentPhoto.fetch(invalid_cookies, "201504021")
    result = StudentPhoto.parse(response)
    assert isinstance(result, ErrorData)

    response = await Chapel.fetch(invalid_cookies, semester="20191")
    assert response.status == 200
    result = Chapel.parse(response)
    assert isinstance(result, ErrorData)

    response = await Timetable.fetch(invalid_cookies, semester="20192")
    assert response.status == 200
    assert isinstance(result, ErrorData)

    response = await Course.fetch(invalid_cookies, semester="20201")
    assert response.status == 200
    result = Course.parse(response)
    assert isinstance(result, ErrorData)


async def main():
    semesters = (None, "20192", "20191", "20182", "20181", "20152", "20151")
    response = await test_login("ramming125", "gksrlghd123")
    # response.cookies["ASP.NET_SessionId"] = response.cookies["ASP.NET_SessionId"]
    # await test_student_photo(response.cookies, "201504021")
    await test_chapel(response.cookies, semesters)
    await test_timetable(response.cookies, semesters)
    await test_course(response.cookies, semesters)
    # await test_invalid_cookies()


asyncio.run(main())

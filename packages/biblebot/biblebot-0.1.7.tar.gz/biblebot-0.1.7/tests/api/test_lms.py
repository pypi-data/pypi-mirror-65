import asyncio

from biblebot.api.lms import *
from biblebot.api.base import ErrorData, ResourceData


async def test_login(user_id, user_pw):
    # 비밀번호 틀린 경우
    response = await Login.fetch(user_id, user_pw + "123")
    assert response.status == 303
    result = Login.parse(response)
    assert isinstance(result, ErrorData)
    print(result)
    # assert result.error["title"] == "비밀번호가 일치하지 않습니다."

    # 아이디가 다른 경우
    response = await Login.fetch(user_id + "1a2b3c", user_pw)
    # assert response.status == 303
    result = Login.parse(response)
    print(result)

    assert isinstance(result, ErrorData)
    # assert result.error["title"] == "존재하지 않는 회원ID 입니다."

    # 정상 로그인
    response = await Login.fetch(user_id, user_pw)
    # assert response.status == 303
    assert response.cookies
    result = Login.parse(response)
    assert isinstance(result, ResourceData)
    assert result.data["cookies"]
    assert result.data["iat"]
    print(result)

    return response


async def test_profile(cookies):
    response = await Profile.fetch(cookies)
    result = Profile.parse(response)
    assert response.status == 200
    assert result.data["sid"] == "201504021"
    assert result.data["name"] == "이경민"
    assert result.data["major"] == "컴퓨터소프트웨어학과"

    result = Profile.parse_sid(response)
    assert result.data["sid"] == "201504021"

    result = Profile.parse_name(response)
    assert result.data["name"] == "이경민"

    result = Profile.parse_major(response)
    assert result.data["major"] == "컴퓨터소프트웨어학과"


async def test_courselist(cookies):
    response = await CourseList.fetch(cookies)
    result = CourseList.parse(response)
    assert response.status == 200
    assert result.data["courses"]
    assert result.meta["selected"]
    assert result.meta["selectable"]

    response = await CourseList.fetch(cookies, semester="20192")
    result = CourseList.parse(response)
    assert response.status == 200
    assert result.meta["selected"] == "20192"
    assert result.meta["selectable"]
    print(result)

    response = await CourseList.fetch(cookies, semester="20201")
    result = CourseList.parse(response)
    assert response.status == 200
    assert result.meta["selected"] == "20201"
    assert result.meta["selectable"]
    print(result)


async def test_attendance(cookies):
    course = {
        "경건훈련": "558",
        "전도훈련Ⅵ": "656",
        "세계문명과기독교Ⅱ": "706",
        "그린IT의이해": "782",
        "네트워크프로그래밍": "820",
        "미래설계상담": "824",
        "무선및모바일통신": "834",
        "데이터마이닝과통계": "836",
    }
    response = await Attendance.fetch(cookies, "836")
    assert response.status == 200
    result = Attendance.parse(response)
    assert isinstance(result, ResourceData)

    response = await Attendance.fetch(cookies, "837")
    assert response.status == 303
    result = Attendance.parse(response)
    assert isinstance(result, ErrorData)


async def test_invalid_cookies():
    invalid_cookies = {"MoodleSession": "4cqrodtjrshs6agk4si6ga3ln3"}

    response = await Profile.fetch(invalid_cookies)
    result = Profile.parse(response)
    assert response.status == 303
    assert isinstance(result, ErrorData)

    result = Profile.parse_sid(response)
    assert isinstance(result, ErrorData)

    result = Profile.parse_name(response)
    assert isinstance(result, ErrorData)

    result = Profile.parse_major(response)
    assert isinstance(result, ErrorData)

    response = await CourseList.fetch(invalid_cookies)
    result = CourseList.parse(response)
    assert isinstance(result, ErrorData)

    response = await CourseList.fetch(invalid_cookies, semester="20192")
    result = CourseList.parse(response)
    assert isinstance(result, ErrorData)

    response = await Attendance.fetch(invalid_cookies, "836")
    result = Attendance.parse(response)
    assert isinstance(result, ErrorData)


async def main():
    response = await test_login("ramming125", "gksrlghd123")
    cookies = response.cookies
    await test_profile(cookies)
    await test_courselist(cookies)
    await test_attendance(cookies)
    await test_invalid_cookies()


asyncio.run(main())

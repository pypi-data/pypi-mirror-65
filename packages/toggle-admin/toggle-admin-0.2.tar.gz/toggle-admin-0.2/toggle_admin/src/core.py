from toggle_admin.http.requests import HTTP
from toggle_admin.src.exceptions import *

import asyncio
import re
import typing


class ToggleAdmin(HTTP):

    __data: dict = {}
    __USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"

    def __init__(
        self,
        login: typing.Union[str, int],
        password: typing.Union[str, int],
        loop: asyncio.AbstractEventLoop = None
    ):
        self.__login = str(login)
        self.__password = str(password)
        self.__loop = loop or asyncio.get_event_loop()
        self.__loop.create_task(self.vk_auth())

    async def __call__(
            self,
            peer_id: int,
            member_id: typing.Union[typing.List[int], int],
            is_admin: bool,
            gid: int = 0
    ):
        if isinstance(member_id, list):
            for member in member_id:
                self.loop.create_task(self.set_admin(peer_id, member, is_admin, gid))
        else:
            await self.set_admin(peer_id, member_id, is_admin, gid)

    async def vk_auth(self):
        ip_h, lg_h, cookies = await self.get_cookies()
        remixlhk = re.findall('remixlhk=(?P<h>[A-Za-z0-9]+);', cookies)[1]
        remixstid = re.search('remixstid=(?P<h>[A-Za-z0-9_]+);', cookies).group('h')

        payload = {
            "act": "login",
            "role": "al_frame",
            "expire": "",
            "recaptcha": "",
            "captcha_key": "",
            "captcha_sid": "",
            "_origin": "https://vk.com",
            "ip_h": ip_h,
            "lg_h": lg_h,
            "email": self.__login,
            "pass": self.__password,
            "utf-8": "1"
        }
        headers = {
            "Referer": "https://vk.com",
            "Origin": "https://vk.com",
            "Accept-Charset": "utf-8",
            "Cookie": "remixlang=0; remixlhk=%s; remixstid=%s; remixdt=0; remixflash=18.0.0; remixscreen_depth=24" % (
                remixlhk, remixstid),
            "User-Agent": self.__USER_AGENT
        }
        request, session = await self.requests.post(
            "https://login.vk.com/?act=login", data=payload, headers=headers
        )
        result = None
        if "Set-Cookie" not in request.headers:
            await session.close()
            raise InvalidAuthData("Указан неверный логин или пароль.")
        if request.status == 200:
            headers = " ".join(request.headers.getall("Set-Cookie"))
            result = re.search("remixsid=([A-Za-z0-9]+)", headers).group().split("=")[1]
            if result == "DELETED":
                await session.close()
                raise InvalidSession("Неверная сессия.")
        elif request.status != 200:
            await session.close()
            raise InvalidSession("Произошла неизвестная ошибка.")
        await session.close()

        self.__data['remixsid'] = result

    async def im_post(self, url: str, payload: dict, headers: dict = None):
        headers_original = {
            "Origin": "https://vk.com",
            "Cookie": "remixsslsid=1; remixsid=%s" % self.__data['remixsid'],
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept-Charset": "utf-8",
            "User-Agent": self.__USER_AGENT
        }
        if headers:
            headers_original.update(headers)

        request, session = await self.requests.post(url, data=payload, headers=headers_original)
        async with request:
            text = await request.text()
            if "Internal server error" in text:
                await session.close()
                raise ToggleAdminError("Произошла неизвестная ошибка.")
        await session.close()
        return text

    async def get_chat_hash(self, peer_id: int, gid: int):
        params = {"act": "a_renew_hash", "al": 1, "peers": peer_id, "gid": gid}
        response = await self.im_post("https://vk.com/al_im.php", params)
        start = response.find('":"') + 3
        index = response[start:].find('"')
        return response[start:start + index]

    async def method(self, peer_id: int, params: dict, gid: int):
        data = {"al": 1, "hash": await self.get_chat_hash(peer_id, gid), "im_v": 3, "gid": 0}
        params.update(data)
        await self.im_post("https://vk.com/al_im.php", params)

    async def set_admin(self, peer_id: int, member_id: int, is_admin: bool, gid: int):
        chat_hash = await self.get_chat_hash(peer_id, gid)
        params = {
            "act": "a_toggle_admin",
            "al": 1,
            "hash": chat_hash,
            "chat": peer_id,
            "mid": member_id,
            "is_admin": int(is_admin)
        }
        await self.method(peer_id, params, gid)

    async def get_cookies(self) -> tuple:
        response, session = await self.requests.get("https://vk.com/login")
        response.raise_for_status()
        text = await response.text()
        ip_h = re.search('"ip_h" value="(?P<h>[a-zA-Z0-9]+)"', text)
        lg_h = re.search('"lg_h" value="(?P<h>[a-zA-Z0-9]+)"', text)
        await session.close()
        return ip_h.group('h'), lg_h.group('h'), " ".join(response.headers.getall('Set-Cookie'))

    @property
    def loop(self):
        return self.__loop
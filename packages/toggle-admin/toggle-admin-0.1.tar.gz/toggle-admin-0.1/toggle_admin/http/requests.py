from aiohttp import ClientSession


class HTTPRequests:

    def __init__(self):
        pass

    @staticmethod
    async def post(url: str, data: dict = None, **kwargs):
        session = ClientSession(raise_for_status=True)
        response = await session.post(url=url, data=data, **kwargs)
        return response, session

    @staticmethod
    async def get(url: str, data: dict = None, **kwargs):
        session = ClientSession(raise_for_status=True)
        response = await session.get(url=url, data=data, **kwargs)
        return response, session


class HTTP:
    requests = HTTPRequests()
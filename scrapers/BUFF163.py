import re
import json
from bufflogin import Buff
import scrapers.const as const
from pysteamauth.auth import Steam
from pysteamauth.errors import SteamError
from playwright.async_api import async_playwright


class BUFF163:
    def __init__(self):
        self._buff = None
        self._host = 'https://buff.163.com'

    async def steam_auth(self, login: str = '', password: str = '', steamid: int = 0) -> bool:
        steam = Steam(login, password, steamid)

        try:
            await steam.login_to_steam()

            self._buff = Buff(steam)
            await self._buff.login_to_buff()

            return True
        except SteamError as error:
            return False

    async def search(self, keyword: str = '') -> list:
        endpoint = '/api/market/search/suggest'
        params = f'text={keyword}&game=csgo'

        response = await self._buff.request(f'{self._host}{endpoint}?{params}')

        try:
            data = json.loads(response)

            if data['code'] == const.OK_STATUS_RESPONSE:
                return json.loads(response)['data']['suggestions']
            else:
                raise Exception(const.SEARCH_FAILED_RESPONSE_ERROR)
        except Exception as err:
            raise Exception(const.SEARCH_FAILED_RESPONSE_ERROR)

    async def get_reference_price(self, goods_id: int = 0) -> float:
        endpoint = f'/goods/{goods_id}'
        params = f'from=market'

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(f'{self._host}{endpoint}?{params}')

            text = await page.locator('a.active').inner_text()

            await browser.close()

            price = re.findall(r"\d+\.\d+|\d+", text)[0]

            return float(price)

    async def get_sell_first_price(self, goods_id: int = 0, min_paintwear: float = 0.0, max_paintwear: float = 0.0) -> float:
        endpoint = f'/api/market/goods/sell_order'
        params = f'game=csgo&' \
                 f'goods_id={goods_id}&' \
                 f'page_num=1&' \
                 f'sort_by=default&' \
                 f'mode=&' \
                 f'allow_tradable_cooldown=1&' \
                 f'min_paintwear={min_paintwear}&' \
                 f'max_paintwear={max_paintwear}&' \
                 f'_='

        response = await self._buff.request(f'{self._host}{endpoint}?{params}')

        try:
            data = json.loads(response)

            if data['code'] == const.OK_STATUS_RESPONSE:
                return float(json.loads(response)['data']['items'][0]['price'])
            else:
                raise Exception(const.SEARCH_FAILED_RESPONSE_ERROR)
        except Exception as err:
            return 0.0
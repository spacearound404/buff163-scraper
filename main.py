import time
import traceback

import config
import asyncio
import logging
from scrapers.BUFF163 import BUFF163


logging.basicConfig(
    filename=f'{config.PATH_TO_LOGS}{str(int(time.time()))}.log',
    filemode='w',
    format='%(asctime)s %(name)s %(levelname)s: %(message)s'
)

logging.getLogger().setLevel(logging.INFO)


def formatted_write_output(line, goods_name, min_paintwear, max_paintwear, reference_price, sell_price):
    with open(config.OUTPUT_TXT_FILE_PATH, 'a') as f:
        logging.info(f'main | trying write data to file {config.OUTPUT_TXT_FILE_PATH}')

        data = f'search key: {line} | ' \
               f'name: {goods_name} | ' \
               f'range: {min_paintwear} - {max_paintwear} | ' \
               f'reference price: {reference_price} | ' \
               f'first sell price: {sell_price}\n'

        logging.info(f'main | data: {data}')

        f.write(data)


async def main():
    auth_result = False
    buff163_scraper = BUFF163()

    try:
        logging.info(f'main | trying to auth, '
                     f'login: {config.LOGIN_STEAM}, '
                     f'password: {config.PASSWORD_STEAM}, '
                     f'steamid: {config.STEAMID}'
                     )

        auth_result: bool = await buff163_scraper.steam_auth(
            login=config.LOGIN_STEAM,
            password=config.PASSWORD_STEAM,
            steamid=config.STEAMID
        )
    except Exception as err:
        logging.error(f'main | {err}')
        logging.error(f'main | {traceback.format_exc()}')

    if not auth_result:
        logging.info('main | error auth on platform')
        return None
    else:
        logging.info('main | success auth on platform')

    with open(config.INPUT_TXT_FILE_PATH, 'r') as file:
        for line in file.readlines():
            logging.info(f'main | line from {config.INPUT_TXT_FILE_PATH}: {line}')

            try:
                search_result: list = await buff163_scraper.search(line)
                logging.info(f'main | search result: {search_result}')

                for data in search_result:
                    try:
                        goods_ids: int = int(data['goods_ids'])
                        goods_name: str = data['option']

                        reference_price: float = await buff163_scraper.get_reference_price(goods_ids)
                        logging.info(f'main | reference price: {reference_price}')

                        for paintwear_quality_range in config.PAINTWEAR_QUALITY_RANGE_LIST:
                            logging.info(f'main | paintwear quality range: {paintwear_quality_range}')

                            try:
                                min_paintwear: float = paintwear_quality_range[0]
                                max_paintwear: float = paintwear_quality_range[1]

                                sell_price = await buff163_scraper.get_sell_first_price(
                                    goods_ids,
                                    min_paintwear,
                                    max_paintwear
                                )
                                logging.info(f'main | sell_price: {sell_price}')

                                additional_amount = reference_price * config.PERCETAGE_FROM_REFERENCE_PRICE
                                logging.info(f'main | percentage from ref price: {config.PERCETAGE_FROM_REFERENCE_PRICE}')
                                logging.info(f'main | additional_amount: {additional_amount}')

                                if reference_price + additional_amount <= sell_price:
                                    formatted_write_output(
                                        line,
                                        goods_name,
                                        min_paintwear,
                                        max_paintwear,
                                        reference_price,
                                        sell_price
                                    )
                            except Exception as err:
                                logging.error(f'main | error in paintwear_quality_range_list loop')
                                logging.error(f'main | {err}')
                                logging.error(f'main | {traceback.format_exc()}')
                                continue
                    except Exception as err:
                        logging.error(f'main | error in search_result loop')
                        logging.error(f'main | {err}')
                        logging.error(f'main | {traceback.format_exc()}')
                        continue
            except Exception as err:
                logging.error(f'main | error in reading data from file loop')
                logging.error(f'main | {err}')
                logging.error(f'main | {traceback.format_exc()}')
                continue


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
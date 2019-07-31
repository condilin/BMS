# !/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @author: condi
# @file: CZWCrawl.py
# @time: 19-7-17 上午11:10


import requests
import pymongo
import random
from datetime import datetime, timedelta
from time import strftime, localtime, sleep, time
from urllib import parse
from bs4 import BeautifulSoup

from requests.exceptions import ConnectionError, ReadTimeout
from CZWCrawl.config.config import cfg, USER_AGENTS, MONGO_HOST, MONGO_PORT


class CZWCrawler(object):

    def __init__(self, params_dict):

        self.__czw_index_url = 'https://www.bidcenter.com.cn'
        self.__base_url = 'https://search.bidcenter.com.cn/search?keywords={}&diqu={}&time={}&type={}&page={}'
        self.__params_dict = params_dict
        self.__keyword_list = ['玻片', '宫颈', 'HPV', '核酸', '切片', '医院', '病理', '试剂', '耗材']
        # self.__keyword_list = ['HPV']

        # url list queue
        self.__url_list_queue = []

        # db connected
        self.__mongo_client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        # self.__db = self.__mongo_client.call_for_bids
        self.__db = self.__mongo_client.call_for_bids_old

    def __get_response_soup(self, full_url, headers, timeout=None):
        """
        get response
        """

        _response = requests.get(full_url, headers=headers, timeout=timeout)
        _soup = BeautifulSoup(_response.text, 'lxml')
        return _soup

    def __get_detail_info(self, bids_detail_url, headers):
        """
        get detail info
        """

        # get and parse web source code
        try:
            # set timeout when connected was exception
            bids_detail_url = 'https:' + bids_detail_url
            detail_soup = self.__get_response_soup(bids_detail_url, headers=headers, timeout=1)

            # slide verify
            if self._selenium_slide_verify(detail_soup, bids_detail_url):
                raise ConnectionError('__get_detail_info assess exception !')

            # get detail info interface url
            detail_interface_list = detail_soup.select('.main-text > #news_contet_detail > iframe#iframe_content')
            detail_interface_url = detail_interface_list[0].attrs.get('src').strip()

            # get detail info
            final_detail_soup = self.__get_response_soup(self.__czw_index_url + detail_interface_url, headers=headers)
            detail_text_list = final_detail_soup.select('div#gethigh')
            detail_text_str = detail_text_list[0].text.strip()

            return detail_text_str

        except ReadTimeout as e1:
            print(e1)
            print('__get_detail_info function error, detail is null')
            return ''
        except ConnectionError as e2:
            print(e2)
            print('__get_detail_info function error, detail is null')
            return ''
        except Exception as e:
            print(e)
            print('__get_detail_info function error, detail is null')
            raise ConnectionError('__get_detail_info slide assess exception !')

    def _get_info(self, bids_list_soup, headers, ws, today, yesterday):
        """
        get info
        """

        # parse html
        bids_list = bids_list_soup.select('table.project_list.ftext_12 > tbody tr')

        for tr in bids_list:
            try:
                # get list info
                bids_id = tr.select('tr td.check_box > input')[0].attrs.get('value').strip()
                bids_title = '+'.join(tr.select('tr td.zb_title')[0].text.split()).replace('+收藏', '')
                bids_detail_url = tr.select('tr td.zb_title > a')[0].attrs.get('href').strip()
                bids_result = tr.select('td')[2].text.strip()
                bids_region = tr.select('tr td.list_area > a')[0].text.strip()
                bids_date = tr.select('tr td.list_time')[0].text.strip()

                # combine all info and save to db
                extract_info = {
                    'bids_id': bids_id,
                    'bids_title': bids_title,
                    'bids_detail_url': 'https:' + bids_detail_url,
                    'bids_result': bids_result,
                    'bids_region': bids_region,
                    'bids_date': bids_date
                }

                if self.__params_dict.params.time in [1, 7]:
                    if extract_info['bids_date'] in [today, yesterday]:
                        self._save_to_mongodb(extract_info, ws)
                    else:
                        ws.send('====== crawl date is: {}, not in {} and {}, so need to break, '
                                'dont continue ! ======'.format(str(extract_info['bids_date']), today, yesterday))
                        return False
                else:
                    self._save_to_mongodb(extract_info, ws)

            except IndexError as e:
                continue

        return True

    def _save_to_mongodb(self, update_info, ws):
        """
        save data to db
        """

        # only insert
        # self.__db.bids_info.insert(update_info)
        # print('successful to save an records!')

        # update if bids id exist else create new records
        self.__db.bids_info.update_one(
            {'bids_id': update_info.get('bids_id')},
            {'$set': update_info},
            upsert=True
        )
        ws.send('successful to save an records to mongodb! which bids id is {} and date is {}'.format(
            update_info.get('bids_id'), update_info.get('bids_date')
        ))

    def _wait(self, _url):
        """
        wait for sleep
        """

        # sleep
        current_page = int(_url.split('page=')[1])
        # if current_page % 5 == 0:
        #     sleep(random.choice(range(10, 20)))
        # elif current_page % 10 == 0:
        #     sleep(random.choice(range(20, 30)))
        # else:
        #     sleep(random.choice(range(1, 10)))

    def _over_page_verify(self, bids_list_soup):
        """
        over page verify
        :return:
        """

        sorry_text_catch = bids_list_soup.select('.dfind > .sorry_text > p')
        if sorry_text_catch:
            return True
        else:
            return False

    def _selenium_slide_verify(self, bids_list_soup, ws):
        """
        use selenium to crack slide verify
        :return:
        """

        error_catch = bids_list_soup.select('.xubox_page > .g-lc-hint-container.layer_pageContent > b')

        # deal the slide verify
        if error_catch:

            # handle to deal the slide verify
            ws.send('{}, 请手动打开页面进行验证！ 验证成功后, 请输入"ok" 继续!\n'.format(error_catch[0].text))
            ws.send('status_code: {}'.format('bl'))
            custom_input = ws.receive()
            custom_deal_status = True if custom_input and custom_input.lower() == 'ok' else False

            if not custom_deal_status:
                ws.send("你放弃了滑动条的验证, 因此程序终止...")
                return True
            else:
                ws.send("成功完成验证, 继续爬取数据... wait for 2s...")
                sleep(2)
                return False

        else:
            return False

    def run(self, ws):

        # get lastest date
        _today_datetime = datetime.now()
        _today = _today_datetime.strftime('%Y-%m-%d')
        _yesterday_datetime = _today_datetime - timedelta(days=1)
        _yesterday = _yesterday_datetime.strftime('%Y-%m-%d')

        try:
            start_time = time()
            # init progress status
            progress_bar = 0
            ws.send('{"progress" : "%s"}' % (str(progress_bar)))

            for keyword in self.__keyword_list:
                for diqu_id in self.__params_dict.params.diqu:
                    for page in self.__params_dict.params.page:
                        full_url = self.__base_url.format(
                            parse.quote(keyword), diqu_id, self.__params_dict.params.time,
                            self.__params_dict.params.type, page
                        )
                        ws.send('当前爬取的关键词为: {}'.format(keyword) + ', 爬取的页面url为: ' + full_url)
                        print('当前关键词为： {}'.format(keyword))

                        # get and parse web source code
                        self.__params_dict.headers['User-Agent'] = random.choice(USER_AGENTS)
                        self.__params_dict.headers.Cookie = self.__params_dict.TMPCookie.format(int(time()))
                        bids_list_soup = self.__get_response_soup(full_url, headers=self.__params_dict.headers)

                        # over page verify, if over, so break to do next region
                        if self._over_page_verify(bids_list_soup):
                            ws.send('地区id: {}, 时间: {} and {}, 数据已完成爬取 !'.format(diqu_id, _today, _yesterday))
                            print('地区id: {}, 时间: {} and {}, 数据已完成爬取 !'.format(diqu_id, _today, _yesterday))
                            break

                        # slide verify
                        if self._selenium_slide_verify(bids_list_soup, ws):
                            raise ConnectionError('assess exception !')

                        # get info
                        if self.__params_dict.params.time == 1:
                            if not self._get_info(
                                    bids_list_soup, headers=self.__params_dict.headers,
                                    ws=ws, today=_today, yesterday=_yesterday
                            ):
                                break
                        else:
                            self._get_info(
                                bids_list_soup, headers=self.__params_dict.headers,
                                ws=ws, today=_today, yesterday=_yesterday
                            )

                        # wait for sleep
                        self._wait(full_url)

                    progress_bar += 0.003367
                    ws.send('{"progress" : "%s"}' % (str(progress_bar)))

                progress_bar += 0.003367
                ws.send('{"progress" : "%s"}' % (str(progress_bar)))

            # complete
            end_time = time()
            time_consume = round((end_time - start_time) / 60, 2)
            ws.send('{"progress" : "1"}')
            ws.send('================ 已完成所有数据的爬取! 用时: {} min ================='.format(time_consume))
            print('================ 已完成所有数据的爬取! 用时: {} min ================='.format(time_consume))

        except Exception as e:
            print(e)
            ws.send('run function error !')
            raise ConnectionError(e)

        finally:
            # close db
            self.__mongo_client.close()


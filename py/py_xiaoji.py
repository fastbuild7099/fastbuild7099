# -*- coding: utf-8 -*-
# @Author  : Doubebly
# @Time    : 2025/3/18 22:56

import sys
import re
import requests
from lxml import etree
sys.path.append('..')
from base.spider import Spider


class Spider(Spider):
    def getName(self):
        return "xiaoji"

    def init(self, extend):
        self.home_url = 'https://www.minijj.com/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        return {
            'class': [{'type_id': '2', 'type_name': '電視劇'},
                      {'type_id': '1', 'type_name': '電影'},
                      {'type_id': '3', 'type_name': '經典動漫'},
                      {'type_id': '4', 'type_name': '綜藝娛樂'}],
            'filters': {}
        }

    def homeVideoContent(self):
        d = []
        try:
            res = requests.get(self.home_url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//ul[@class="update_area_lists cl"]/li[@class="i_list list_n2"]')
            for i in data_list:
                d.append(
                    {
                        'vod_id': i.xpath('./a/@href')[0],
                        'vod_name': i.xpath('//div[@class="meta-title"]/text()')[0],
                        'vod_pic': i.xpath('./a/img/@data-original')[0],
                        'vod_remarks': i.xpath('//div[@class="meta-post"]/text()')[0]
                    }
                )
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(e)
            return {'list': [], 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        url = self.home_url + f'/lm/{cid}/{page}.html'
        d = []
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//ul[@class="update_area_lists cl"]/li[@class="i_list list_n2"]')
            for i in data_list:
                d.append(
                    {
                        'vod_id': i.xpath('./a/@href')[0],
                        'vod_name': i.xpath('//div[@class="meta-title"]/text()')[0],
                        'vod_pic': i.xpath('./a/img/@data-original')[0],
                        'vod_remarks': i.xpath('//div[@class="meta-post"]/text()')[0]
                    }
                )
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(e)
            return {'list': [], 'parse': 0, 'jx': 0}

    def detailContent(self, did):
        ids = did[0]
        video_list = []
        url = self.home_url + ids
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            vod_play_from = '$$$'.join(root.xpath(
                '//ul[@class="nav nav-tabs"]/li/a/text()'))  # //ul[contains(@class, "abc")]  [@class="tab_control play_from"]
            play_list = root.xpath('//ul[@class="list-unstyled text-center play-list"]')
            vod_play_url = []
            for i in play_list:
                name_list = i.xpath('./li/a/text()')
                url_list = i.xpath('./li/a/@href')
                vod_play_url.append(
                    '#'.join([_name + '$' + _url for _name, _url in zip(name_list, url_list)])
                )
            video_list.append(
                {
                    'type_name': '',
                    'vod_id': ids,
                    'vod_name': '',
                    'vod_remarks': '',
                    'vod_year': '',
                    'vod_area': '',
                    'vod_actor': '',
                    'vod_director': '沐辰_为爱发电',
                    'vod_content': '',
                    'vod_play_from': vod_play_from,
                    'vod_play_url': '$$$'.join(vod_play_url)

                }
            )
            return {"list": video_list, 'parse': 0, 'jx': 0}
        except requests.RequestException as e:
            return {'list': [], 'msg': e}

        # return {"list": [], "msg": "来自py_dependence的detailContent"}

    def searchContent(self, key, quick, page='1'):
        d = []
        url = self.home_url + f'/ss.html'
        if page != '1':
            return {'list': [], 'parse': 0, 'jx': 0}
        try:
            res = requests.post(url, headers=self.headers, data={'wd': key})
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//ul[@class="update_area_lists cl"]/li[@class="i_list list_n2"]')
            for i in data_list:
                d.append(
                    {
                        'vod_id': i.xpath('./a/@href')[0],
                        'vod_name': i.xpath('//div[@class="meta-title"]/text()')[0],
                        'vod_pic': i.xpath('./a/img/@data-original')[0],
                        'vod_remarks': i.xpath('//div[@class="meta-post"]/text()')[0]
                    }
                )
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(e)
            return {'list': [], 'parse': 0, 'jx': 0}
        # return {"list": [], "msg": "来自py_dependence的searchContent"}

    def playerContent(self, flag, pid, vipFlags):
        play_url = 'https://gitee.com/dobebly/my_img/raw/c1977fa6134aefb8e5a34dabd731a4d186c84a4d/x.mp4'
        try:
            res = requests.get(f'{self.home_url}{pid}', headers=self.headers)
            res.encoding = 'utf-8'
            urls = re.findall(r'var\s+url\s+=\s+"(.*?)";', res.text)
            if len(urls) == 0:
                return {'url': play_url, 'parse': 0, 'jx': 0}
            return {'url': urls[0], 'parse': 0, 'jx': 0}
        except requests.RequestException as e:
            print(e)
            return {'url': play_url, 'parse': 0, 'jx': 0}
        # return {"list": [], "msg": "来自py_dependence的playerContent"}

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

if __name__ == '__main__':
    pass

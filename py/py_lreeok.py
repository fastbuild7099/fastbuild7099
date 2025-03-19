# -*- coding: utf-8 -*-
# @Author  : Doubebly
# @Time    : 2025/3/19 21:14

import sys
import requests
import hashlib
import time
import json
import re
from lxml import etree

sys.path.append('..')
from base.spider import Spider


class Spider(Spider):

    def getName(self):
        return "LreeOk"

    def init(self, extend):

        self.home_url = 'https://lreeok.vip'
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
            'class': [
                {'type_id': '1', 'type_name': '电影'},
                {'type_id': '2', 'type_name': '连续剧'},
                {'type_id': '3', 'type_name': '综艺'},
                {'type_id': '4', 'type_name': '动漫'},
                {'type_id': '5', 'type_name': '短剧'}
            ],
            'filters': {}
        }

    def homeVideoContent(self):
        d = []
        try:
            res = requests.get(self.home_url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//div[contains(@class, "public-list-box public-pic-b")]')
            for i in data_list:
                vod_remarks = i.xpath('.//div[contains(@class, "public-list-subtitle")]/text()')
                d.append(
                    {
                        'vod_id': i.xpath('./div[1]/a/@href')[0].split('/')[-1].split('.')[0],
                        'vod_name': i.xpath('./div[1]/a/@title')[0],
                        'vod_pic': i.xpath('./div[1]/a/img/@data-src')[0],
                        'vod_remarks': vod_remarks[0] if len(vod_remarks) > 0 else '',
                    }
                )
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(e)
            return {'list': [], 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        payload = {
            'type': cid,
            'class': ext.get('type') if ext.get('type') else '',
            'area': ext.get('area') if ext.get('area') else '',
            'lang': ext.get('lang') if ext.get('lang') else '',
            'version': '',
            'state': '',
            'letter': '',
            'page': page,
            'by': ext.get('by') if ext.get('by') else '',
        }
        data = self.get_data(payload)
        return {'list': data, 'parse': 0, 'jx': 0}
        # return {"list": [], "msg": "来自py_dependence的categoryContent"}

    def detailContent(self, did):
        ids = did[0]
        video_list = []
        
        try:
            res = requests.get(f'{self.home_url}/voddetail/{ids}.html', headers=self.headers)
            root = etree.HTML(res.text)
            vod_play_from = '$$$'.join(root.xpath(
                '//div[@class="swiper-wrapper"]/a/text()'))  # //ul[contains(@class, "abc")]  [@class="tab_control play_from"]
            play_list = root.xpath('//ul[@class="anthology-list-play size"]')
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
        url = self.home_url + f'/index.php/ajax/suggest?mid=1&wd={key}'
        if page != '1':
            return {'list': [], 'parse': 0, 'jx': 0}
        try:
            res = requests.get(url, headers=self.headers)
            data_list = res.json()['list']
            for i in data_list:
                d.append(
                    {
                        'vod_id': i['id'],
                        'vod_name': i['name'],
                        'vod_pic': i['pic'].replace('/img.php?url=', '') if '/img.php?url=' in i['pic'] else i['pic'],
                        'vod_remarks': '',
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

            datas = re.findall(r'player_aaaa=(.*?)</script>', res.text)
            if len(datas) == 0:
                return {'url': play_url, 'parse': 0, 'jx': 0}
            data = json.loads(datas[0])
            url = data['url']
            c = data['from']
            if c in ['qq', 'qiyi', 'youku']:
                payload = {
                    'url': "https://v.qq.com/x/cover/iuk7vpw1sftk9dh/x0026vf5iyx.html"
                }

                headers = {
                    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
                    'Accept': "application/json, text/javascript, */*; q=0.01",
                    'Accept-Encoding': "gzip, deflate, br, zstd",
                    'sec-ch-ua-platform': "\"Windows\"",
                    'X-Requested-With': "XMLHttpRequest",
                    'sec-ch-ua': "\"Chromium\";v=\"134\", \"Not:A-Brand\";v=\"24\", \"Google Chrome\";v=\"134\"",
                    'sec-ch-ua-mobile': "?0",
                    'Origin': "https://www.lreeok.vip",
                    'Sec-Fetch-Site': "same-origin",
                    'Sec-Fetch-Mode': "cors",
                    'Sec-Fetch-Dest': "empty",
                    'Accept-Language': "zh-CN,zh;q=0.9"
                }
                try:
                    response = requests.post('https://www.lreeok.vip/okplay/api_config.php', data=payload,
                                             headers=headers)
                    data = response.json()
                    if data['code'] != '200':
                        return {'url': play_url, 'parse': 0, 'jx': 0}

                    h = {
                        'User-Agent': data['user-agent'],
                        'Referer': data['referer']
                    }
                    url = data['url']
                    return {'url': url, 'parse': 0, 'jx': 0, 'header': h}
                except requests.RequestException as e:
                    print(e)
                    return {'url': play_url, 'parse': 0, 'jx': 0}
            else:
                return {'url': url, 'parse': 0, 'jx': 0, 'header': self.headers}

        except requests.RequestException as e:
            print(e)
            return {'url': play_url, 'parse': 0, 'jx': 0}
        # return {"list": [], "msg": "来自py_dependence的playerContent"}

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

    def get_data(self, payload):
        t = int(time.time())
        key = hashlib.md5(str(f'DS{t}DCC147D11943AF75').encode('utf-8')).hexdigest()
        url = self.home_url + "/index.php/api/vod"
        payload['time'] = str(t)
        payload['key'] = key
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate, br, zstd",
            'sec-ch-ua-mobile': "?0",
            'Origin': "https://lreeok.vip",
            'Sec-Fetch-Site': "same-origin",
            'Sec-Fetch-Mode': "cors",
            'Sec-Fetch-Dest': "empty",
            'Referer': "https://lreeok.vip/",
            'Accept-Language': "zh-CN,zh;q=0.9",
        }
        data = []
        try:
            res = requests.post(url, data=payload, headers=headers)
            data_list = res.json()['list']
            for i in data_list:
                data.append(
                    {
                        'vod_id': i['vod_id'],
                        'vod_name': i['vod_name'],
                        'vod_pic': i['vod_pic'],
                        'vod_remarks': i['vod_remarks'],
                    }
                )
            return data
        except requests.RequestException as e:
            print(e)
            return data


if __name__ == '__main__':
    pass

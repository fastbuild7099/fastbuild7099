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
                {'type_id': '1', 'type_name': '電影'},
                {'type_id': '2', 'type_name': '連續劇'},
                {'type_id': '3', 'type_name': '綜藝'},
                {'type_id': '4', 'type_name': '動漫'},
                {'type_id': '5', 'type_name': '短劇'}
            ],
            'filters': {
                '1': [  # 電影
                    {'key': 'class',
                     'name': '類型',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '喜劇', 'v': '喜劇'},
                               {'n': '愛情', 'v': '愛情'},
                               {'n': '恐怖', 'v': '恐怖'},
                               {'n': '動作', 'v': '動作'},
                               {'n': '科幻', 'v': '科幻'},
                               {'n': '劇情', 'v': '劇情'},
                               {'n': '戰爭', 'v': '戰爭'},
                               {'n': '警匪', 'v': '警匪'},
                               {'n': '犯罪', 'v': '犯罪'},
                               {'n': '動畫', 'v': '動畫'},
                               {'n': '奇幻', 'v': '奇幻'},
                               {'n': '武俠', 'v': '武俠'},
                               {'n': '冒險', 'v': '冒險'},
                               {'n': '槍戰', 'v': '槍戰'},
                               {'n': '懸疑', 'v': '懸疑'},
                               {'n': '驚悚', 'v': '驚悚'},
                               {'n': '經典', 'v': '經典'},
                               {'n': '青春', 'v': '青春'},
                               {'n': '文藝', 'v': '文藝'},
                               {'n': '微電影', 'v': '微電影'},
                               {'n': '古裝', 'v': '古裝'},
                               {'n': '歷史', 'v': '歷史'},
                               {'n': '運動', 'v': '運動'},
                               {'n': '農村', 'v': '農村'},
                               {'n': '兒童', 'v': '兒童'},
                               {'n': '網絡電影', 'v': '網絡電影'}]},
                    {'key': 'area',
                     'name': '地區',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '大陸', 'v': '大陸'},
                               {'n': '香港', 'v': '香港'},
                               {'n': '台灣', 'v': '台灣'},
                               {'n': '美國', 'v': '美國'},
                               {'n': '法國', 'v': '法國'},
                               {'n': '英國', 'v': '英國'},
                               {'n': '日本', 'v': '日本'},
                               {'n': '韓國', 'v': '韓國'},
                               {'n': '德國', 'v': '德國'},
                               {'n': '泰國', 'v': '泰國'},
                               {'n': '印度', 'v': '印度'},
                               {'n': '意大利', 'v': '意大利'},
                               {'n': '西班牙', 'v': '西班牙'},
                               {'n': '加拿大', 'v': '加拿大'},
                               {'n': '其他', 'v': '其他'}]},
                    {'key': 'year',
                     'name': '年份',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '2025', 'v': '2025'},
                               {'n': '2024', 'v': '2024'},
                               {'n': '2023', 'v': '2023'},
                               {'n': '2022', 'v': '2022'},
                               {'n': '2021', 'v': '2021'},
                               {'n': '2020', 'v': '2020'},
                               {'n': '2019', 'v': '2019'},
                               {'n': '2018', 'v': '2018'},
                               {'n': '2017', 'v': '2017'},
                               {'n': '2016', 'v': '2016'},
                               {'n': '2015', 'v': '2015'},
                               {'n': '2014', 'v': '2014'},
                               {'n': '2013', 'v': '2013'},
                               {'n': '2012', 'v': '2012'},
                               {'n': '2011', 'v': '2011'},
                               {'n': '2010', 'v': '2010'}]},
                    {'key': 'lang',
                     'name': '語言',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '國語', 'v': '國語'},
                               {'n': '英語', 'v': '英語'},
                               {'n': '粵語', 'v': '粵語'},
                               {'n': '閩南語', 'v': '閩南語'},
                               {'n': '韓語', 'v': '韓語'},
                               {'n': '日語', 'v': '日語'},
                               {'n': '法語', 'v': '法語'},
                               {'n': '德語', 'v': '德語'},
                               {'n': '其它', 'v': '其它'}]},
                    {'key': 'by',
                     'name': '排序',
                     'value': [{'n': '按最新', 'v': 'time'},
                               {'n': '按最熱', 'v': 'hits'},
                               {'n': '按評分', 'v': 'score'}]}
                ],
                '2': [  # 連續劇
                    {'key': 'class',
                     'name': '類型',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '古裝', 'v': '古裝'},
                               {'n': '戰爭', 'v': '戰爭'},
                               {'n': '青春偶像', 'v': '青春偶像'},
                               {'n': '喜劇', 'v': '喜劇'},
                               {'n': '家庭', 'v': '家庭'},
                               {'n': '犯罪', 'v': '犯罪'},
                               {'n': '動作', 'v': '動作'},
                               {'n': '奇幻', 'v': '奇幻'},
                               {'n': '劇情', 'v': '劇情'},
                               {'n': '歷史', 'v': '歷史'},
                               {'n': '經典', 'v': '經典'},
                               {'n': '鄉村', 'v': '鄉村'},
                               {'n': '情景', 'v': '情景'},
                               {'n': '商戰', 'v': '商戰'},
                               {'n': '網劇', 'v': '網劇'},
                               {'n': '其他', 'v': '其他'}]},
                    {'key': 'area',
                     'name': '地區',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '內地', 'v': '內地'},
                               {'n': '韓國', 'v': '韓國'},
                               {'n': '香港', 'v': '香港'},
                               {'n': '台灣', 'v': '台灣'},
                               {'n': '日本', 'v': '日本'},
                               {'n': '美國', 'v': '美國'},
                               {'n': '泰國', 'v': '泰國'},
                               {'n': '英國', 'v': '英國'},
                               {'n': '新加坡', 'v': '新加坡'},
                               {'n': '其他', 'v': '其他'}]},
                    {'key': 'year',
                     'name': '年份',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '2025', 'v': '2025'},
                               {'n': '2024', 'v': '2024'},
                               {'n': '2023', 'v': '2023'},
                               {'n': '2022', 'v': '2022'},
                               {'n': '2021', 'v': '2021'},
                               {'n': '2020', 'v': '2020'},
                               {'n': '2019', 'v': '2019'},
                               {'n': '2018', 'v': '2018'},
                               {'n': '2017', 'v': '2017'},
                               {'n': '2016', 'v': '2016'},
                               {'n': '2015', 'v': '2015'},
                               {'n': '2014', 'v': '2014'},
                               {'n': '2013', 'v': '2013'},
                               {'n': '2012', 'v': '2012'},
                               {'n': '2011', 'v': '2011'},
                               {'n': '2010', 'v': '2010'}]},
                    {'key': 'lang',
                     'name': '語言',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '國語', 'v': '國語'},
                               {'n': '英語', 'v': '英語'},
                               {'n': '粵語', 'v': '粵語'},
                               {'n': '閩南語', 'v': '閩南語'},
                               {'n': '韓語', 'v': '韓語'},
                               {'n': '日語', 'v': '日語'},
                               {'n': '其它', 'v': '其它'}]},
                    {'key': 'by',
                     'name': '排序',
                     'value': [{'n': '按最新', 'v': 'time'},
                               {'n': '按最熱', 'v': 'hits'},
                               {'n': '按評分', 'v': 'score'}]}
                ],
                '3': [  # 綜藝
                    {'key': 'class',
                     'name': '類型',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '選秀', 'v': '選秀'},
                               {'n': '情感', 'v': '情感'},
                               {'n': '訪談', 'v': '訪談'},
                               {'n': '播報', 'v': '播報'},
                               {'n': '旅遊', 'v': '旅遊'},
                               {'n': '音樂', 'v': '音樂'},
                               {'n': '美食', 'v': '美食'},
                               {'n': '紀實', 'v': '紀實'},
                               {'n': '曲藝', 'v': '曲藝'},
                               {'n': '生活', 'v': '生活'},
                               {'n': '遊戲互動', 'v': '遊戲互動'},
                               {'n': '財經', 'v': '財經'},
                               {'n': '求職', 'v': '求職'}]},
                    {'key': 'area',
                     'name': '地區',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '內地', 'v': '內地'},
                               {'n': '港台', 'v': '港台'},
                               {'n': '日韓', 'v': '日韓'},
                               {'n': '歐美', 'v': '歐美'}]},
                    {'key': 'year',
                     'name': '年份',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '2025', 'v': '2025'},
                               {'n': '2024', 'v': '2024'},
                               {'n': '2023', 'v': '2023'},
                               {'n': '2022', 'v': '2022'},
                               {'n': '2021', 'v': '2021'},
                               {'n': '2020', 'v': '2020'},
                               {'n': '2019', 'v': '2019'},
                               {'n': '2018', 'v': '2018'},
                               {'n': '2017', 'v': '2017'},
                               {'n': '2016', 'v': '2016'},
                               {'n': '2015', 'v': '2015'},
                               {'n': '2014', 'v': '2014'},
                               {'n': '2013', 'v': '2013'},
                               {'n': '2012', 'v': '2012'},
                               {'n': '2011', 'v': '2011'},
                               {'n': '2010', 'v': '2010'}]},
                    {'key': 'lang',
                     'name': '語言',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '國語', 'v': '國語'},
                               {'n': '英語', 'v': '英語'},
                               {'n': '粵語', 'v': '粵語'},
                               {'n': '閩南語', 'v': '閩南語'},
                               {'n': '韓語', 'v': '韓語'},
                               {'n': '日語', 'v': '日語'},
                               {'n': '其它', 'v': '其它'}]},
                    {'key': 'by',
                     'name': '排序',
                     'value': [{'n': '按最新', 'v': 'time'},
                               {'n': '按最熱', 'v': 'hits'},
                               {'n': '按評分', 'v': 'score'}]}
                ],
                '4': [  # 動漫
                    {'key': 'class',
                     'name': '類型',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '情感', 'v': '情感'},
                               {'n': '科幻', 'v': '科幻'},
                               {'n': '熱血', 'v': '熱血'},
                               {'n': '推理', 'v': '推理'},
                               {'n': '搞笑', 'v': '搞笑'},
                               {'n': '冒險', 'v': '冒險'},
                               {'n': '蘿莉', 'v': '蘿莉'},
                               {'n': '校園', 'v': '校園'},
                               {'n': '動作', 'v': '動作'},
                               {'n': '機戰', 'v': '機戰'},
                               {'n': '運動', 'v': '運動'},
                               {'n': '戰爭', 'v': '戰爭'},
                               {'n': '少年', 'v': '少年'},
                               {'n': '少女', 'v': '少女'},
                               {'n': '社會', 'v': '社會'},
                               {'n': '原創', 'v': '原創'},
                               {'n': '親子', 'v': '親子'},
                               {'n': '益智', 'v': '益智'},
                               {'n': '勵志', 'v': '勵志'},
                               {'n': '其他', 'v': '其他'}]},
                    {'key': 'area',
                     'name': '地區',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '國產', 'v': '國產'},
                               {'n': '日本', 'v': '日本'},
                               {'n': '歐美', 'v': '歐美'},
                               {'n': '其他', 'v': '其他'}]},
                    {'key': 'year',
                     'name': '年份',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '2025', 'v': '2025'},
                               {'n': '2024', 'v': '2024'},
                               {'n': '2023', 'v': '2023'},
                               {'n': '2022', 'v': '2022'},
                               {'n': '2021', 'v': '2021'},
                               {'n': '2020', 'v': '2020'},
                               {'n': '2019', 'v': '2019'},
                               {'n': '2018', 'v': '2018'},
                               {'n': '2017', 'v': '2017'},
                               {'n': '2016', 'v': '2016'},
                               {'n': '2015', 'v': '2015'},
                               {'n': '2014', 'v': '2014'},
                               {'n': '2013', 'v': '2013'},
                               {'n': '2012', 'v': '2012'},
                               {'n': '2011', 'v': '2011'},
                               {'n': '2010', 'v': '2010'}]},
                    {'key': 'lang',
                     'name': '語言',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '國語', 'v': '國語'},
                               {'n': '英語', 'v': '英語'},
                               {'n': '粵語', 'v': '粵語'},
                               {'n': '閩南語', 'v': '閩南語'},
                               {'n': '韓語', 'v': '韓語'},
                               {'n': '日語', 'v': '日語'},
                               {'n': '其它', 'v': '其它'}]},
                    {'key': 'by',
                     'name': '排序',
                     'value': [{'n': '按最新', 'v': 'time'},
                               {'n': '按最熱', 'v': 'hits'},
                               {'n': '按評分', 'v': 'score'}]}
                ],
                '5': [  # 短劇
                    {'key': 'year',
                     'name': '年份',
                     'value': [{'n': '全部', 'v': ''},
                               {'n': '2025', 'v': '2025'},
                               {'n': '2024', 'v': '2024'},
                               {'n': '2023', 'v': '2023'},
                               {'n': '2022', 'v': '2022'},
                               {'n': '2021', 'v': '2021'},
                               {'n': '2020', 'v': '2020'},
                               {'n': '2019', 'v': '2019'},
                               {'n': '2018', 'v': '2018'},
                               {'n': '2017', 'v': '2017'},
                               {'n': '2016', 'v': '2016'},
                               {'n': '2015', 'v': '2015'},
                               {'n': '2014', 'v': '2014'},
                               {'n': '2013', 'v': '2013'},
                               {'n': '2012', 'v': '2012'},
                               {'n': '2011', 'v': '2011'},
                               {'n': '2010', 'v': '2010'}]},
                    {'key': 'by',
                     'name': '排序',
                     'value': [{'n': '按最新', 'v': 'time'},
                               {'n': '按最熱', 'v': 'hits'},
                               {'n': '按評分', 'v': 'score'}]}
                ]
            }
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

    def detailContent(self, did):
        ids = did[0]
        video_list = []
        
        try:
            res = requests.get(f'{self.home_url}/voddetail/{ids}.html', headers=self.headers)
            root = etree.HTML(res.text)
            vod_play_from = '$$$'.join(root.xpath(
                '//div[@class="swiper-wrapper"]/a/text()'))
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
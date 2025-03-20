# -*- coding: utf-8 -*-
# @Author  : Doubebly
# @Time    : 2025/3/19 21:14

import sys
import requests
import hashlib
import time
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
import threading
import re
import json
import asyncio
import aiohttp

sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def __init__(self):
        """初始化爬蟲"""
        self.home_url = 'https://lreeok.vip'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        self.detail_cache = {}
        self.cache_lock = threading.Lock()

    def getName(self):
        return "LreeOk"

    def init(self, extend):
        pass

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
                '1': [
                    {'key': 'class', 'name': '类型', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '喜剧', 'v': '喜剧'}, {'n': '爱情', 'v': '爱情'}, {'n': '恐怖', 'v': '恐怖'},
                        {'n': '动作', 'v': '动作'}, {'n': '科幻', 'v': '科幻'}, {'n': '剧情', 'v': '剧情'}, {'n': '战争', 'v': '战争'},
                        {'n': '警匪', 'v': '警匪'}, {'n': '犯罪', 'v': '犯罪'}, {'n': '动画', 'v': '动画'}, {'n': '奇幻', 'v': '奇幻'},
                        {'n': '武侠', 'v': '武侠'}, {'n': '冒险', 'v': '冒险'}, {'n': '枪战', 'v': '枪战'}, {'n': '悬疑', 'v': '悬疑'},
                        {'n': '惊悚', 'v': '惊悚'}, {'n': '经典', 'v': '经典'}, {'n': '青春', 'v': '青春'}, {'n': '文艺', 'v': '文艺'},
                        {'n': '微电影', 'v': '微电影'}, {'n': '古装', 'v': '古装'}, {'n': '历史', 'v': '历史'}, {'n': '运动', 'v': '运动'},
                        {'n': '农村', 'v': '农村'}, {'n': '儿童', 'v': '儿童'}, {'n': '网络电影', 'v': '网络电影'}
                    ]},
                    {'key': 'area', 'name': '地区', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '大陆', 'v': '大陆'}, {'n': '香港', 'v': '香港'}, {'n': '台湾', 'v': '台湾'},
                        {'n': '美国', 'v': '美国'}, {'n': '法国', 'v': '法国'}, {'n': '英国', 'v': '英国'}, {'n': '日本', 'v': '日本'},
                        {'n': '韩国', 'v': '韩国'}, {'n': '德国', 'v': '德国'}, {'n': '泰国', 'v': '泰国'}, {'n': '印度', 'v': '印度'},
                        {'n': '意大利', 'v': '意大利'}, {'n': '西班牙', 'v': '西班牙'}, {'n': '加拿大', 'v': '加拿大'}, {'n': '其他', 'v': '其他'}
                    ]},
                    {'key': 'year', 'name': '年份', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'},
                        {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'},
                        {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'},
                        {'n': '2014', 'v': '2014'}, {'n': '2013', 'v': '2013'}, {'n': '2012', 'v': '2012'}, {'n': '2011', 'v': '2011'},
                        {'n': '2010', 'v': '2010'}
                    ]},
                    {'key': 'lang', 'name': '语言', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '国语', 'v': '国语'}, {'n': '英语', 'v': '英语'}, {'n': '粤语', 'v': '粤语'},
                        {'n': '闽南语', 'v': '闽南语'}, {'n': '韩语', 'v': '韩语'}, {'n': '日语', 'v': '日语'}, {'n': '法语', 'v': '法语'},
                        {'n': '德语', 'v': '德语'}, {'n': '其它', 'v': '其它'}
                    ]},
                    {'key': 'by', 'name': '排序', 'value': [
                        {'n': '按最新', 'v': 'time'}, {'n': '按最热', 'v': 'hits'}, {'n': '按评分', 'v': 'score'}
                    ]}
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
                d.append({
                    'vod_id': i.xpath('./div[1]/a/@href')[0].split('/')[-1].split('.')[0],
                    'vod_name': i.xpath('./div[1]/a/@title')[0],
                    'vod_pic': i.xpath('./div[1]/a/img/@data-src')[0],
                    'vod_remarks': vod_remarks[0] if vod_remarks else ''
                })
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"首頁視頻內容獲取錯誤: {e}")
            return {'list': [], 'parse': 0, 'jx': 0}

    async def fetch_detail(self, session, vod_id):
        try:
            async with session.get(f'{self.home_url}/voddetail/{vod_id}.html', headers=self.headers, timeout=aiohttp.ClientTimeout(total=10)) as res:
                text = await res.text(encoding='utf-8')
                root = etree.HTML(text)
                vod_area = root.xpath('//li[contains(., "地区：")]/text()[last()]')[0].strip() if root.xpath('//li[contains(., "地区：")]/text()[last()]') else '大陆'
                if vod_area == '大陆':
                    vod_area = root.xpath('//li/em[contains(., "地区：")]/following-sibling::text()[1]')[0].strip() if root.xpath('//li/em[contains(., "地区：")]/following-sibling::text()[1]') else '大陆'
                return {'vod_id': vod_id, 'vod_area': vod_area}
        except Exception as e:
            print(f"異步請求詳情失敗: {vod_id}, {e}")
            return {'vod_id': vod_id, 'vod_area': '大陆'}

    async def async_categoryContent(self, cid, page, filter, ext):
        ext = ext if isinstance(ext, dict) else {}
        payload = {
            'type': cid,
            'class': ext.get('class', ''),
            'area': ext.get('area', ''),
            'lang': ext.get('lang', ''),
            'year': ext.get('year', ''),
            'version': '',
            'state': '',
            'letter': '',
            'page': str(page),
            'by': ext.get('by', 'time')
        }

        try:
            data = self.get_data(payload)
            if not data:
                return {'list': [], 'parse': 0, 'jx': 0}

            # 異步獲取缺少緩存的詳情資料
            async with aiohttp.ClientSession() as session:
                tasks = []
                for item in data:
                    vod_id = str(item.get('vod_id', ''))
                    with self.cache_lock:
                        if vod_id not in self.detail_cache:
                            tasks.append(self.fetch_detail(session, vod_id))
                if tasks:
                    results = await asyncio.gather(*tasks)
                    with self.cache_lock:
                        for result in results:
                            self.detail_cache[result['vod_id']] = result

            filtered_data = []
            for item in data:
                vod_id = str(item.get('vod_id', ''))
                with self.cache_lock:
                    cached_item = self.detail_cache.get(vod_id, {})
                vod_area = cached_item.get('vod_area', item.get('vod_area', '大陆'))
                area_filter = ext.get('area', '')
                area_match = (not area_filter or area_filter in vod_area)

                if area_match:
                    filtered_data.append({
                        'vod_id': vod_id,
                        'vod_name': item.get('vod_name', ''),
                        'vod_pic': item.get('vod_pic', ''),
                        'vod_remarks': item.get('vod_remarks', '')
                    })

            return {'list': filtered_data, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"分類內容獲取錯誤: {e}")
            return {'list': [], 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        return asyncio.run(self.async_categoryContent(cid, page, filter, ext))

    def detailContent(self, did):
        ids = did[0]
        video_list = []
        try:
            res = requests.get(f'{self.home_url}/voddetail/{ids}.html', headers=self.headers, timeout=10)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)

            with self.cache_lock:
                api_data = self.detail_cache.get(ids, {})
            def extract_fallback(root, xpath, default=""):
                result = root.xpath(xpath)
                return result[0].strip() if result else default

            vod_name = extract_fallback(root, '//h3[@class="slide-info-title hide"]/text()', api_data.get('vod_name', ''))
            vod_pic = extract_fallback(root, '//div[contains(@class, "vod-img")]//img/@data-src', api_data.get('vod_pic', ''))
            vod_class = " ".join(root.xpath('//div[@class="info-parameter"]//li[contains(., "类型")]/a/text()')) if root.xpath('//div[@class="info-parameter"]//li[contains(., "类型")]/a/text()') else api_data.get('vod_class', '')
            vod_year = extract_fallback(root, '//div[@class="info-parameter"]//li[contains(., "年份")]/text()[last()]', api_data.get('vod_year', ''))
            vod_area = extract_fallback(root, '//li[contains(., "地区：")]/text()[last()]', api_data.get('vod_area', '大陆'))
            if vod_area == '大陆':
                vod_area = extract_fallback(root, '//li/em[contains(., "地区：")]/following-sibling::text()[1]', '大陆')
            vod_remarks = extract_fallback(root, '//div[@class="info-parameter"]//li[contains(., "状态")]/span/text()', api_data.get('vod_remarks', ''))
            vod_director = extract_fallback(root, '//div[@class="info-parameter"]//li[contains(., "导演")]/span/text()', api_data.get('vod_director', '未知'))
            vod_actor = extract_fallback(root, '//div[@class="info-parameter"]//li[contains(., "主演")]/span/text()', api_data.get('vod_actor', '未知'))
            vod_lang = extract_fallback(root, '//div[@class="info-parameter"]//li[contains(., "语言")]/text()[last()]', api_data.get('vod_lang', '国语'))
            vod_content = extract_fallback(root, '//div[@id="height_limit"]/text()', api_data.get('vod_content', '暫無簡介'))

            play_from, play_url = [], []
            anthology_tabs = [''.join(tab.xpath('.//text()')).strip().replace('\xa0', '') for tab in root.xpath('//div[@class="anthology-tab"]//a')]
            anthology_boxes = root.xpath('//div[contains(@class, "anthology-list-box")]')
            for i, box in enumerate(anthology_boxes):
                source_name = anthology_tabs[i] if i < len(anthology_tabs) else f"線路 {i+1}"
                play_from.append(source_name)
                urls = box.xpath('.//a/@href')
                titles = box.xpath('.//a/text()')
                play_items = []
                for j in range(len(urls)):
                    title = titles[j].strip() if j < len(titles) else f"第{j+1}集"
                    play_items.append(f"{title}${urls[j]}")
                play_url.append("#".join(play_items))

            vod_play_from = "$$$".join(play_from)
            vod_play_url = "$$$".join(play_url)

            video_list.append({
                'type_name': vod_class,
                'vod_id': ids,
                'vod_name': vod_name,
                'vod_pic': vod_pic,
                'vod_remarks': vod_remarks,
                'vod_year': vod_year,
                'vod_area': vod_area,
                'vod_actor': vod_actor,
                'vod_director': vod_director,
                'vod_content': vod_content,
                'vod_lang': vod_lang,
                'vod_play_from': vod_play_from,
                'vod_play_url': vod_play_url
            })

            with self.cache_lock:
                self.detail_cache[ids] = video_list[0]
            print(f"詳情頁結果: vod_id={ids}, vod_area={vod_area}")
            return {'list': video_list, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"詳情內容獲取錯誤: {e}")
            return {'list': [], 'msg': str(e)}

    def searchContent(self, key, quick, page='1'):
        d = []
        url = self.home_url + f'/index.php/ajax/suggest?mid=1&wd={key}'
        if page != '1':
            return {'list': [], 'parse': 0, 'jx': 0}
        try:
            res = requests.get(url, headers=self.headers)
            data_list = res.json()['list']
            for i in data_list:
                d.append({
                    'vod_id': i['id'],
                    'vod_name': i['name'],
                    'vod_pic': i['pic'].replace('/img.php?url=', '') if '/img.php?url=' in i['pic'] else i['pic'],
                    'vod_remarks': ''
                })
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"搜索內容錯誤: {e}")
            return {'list': [], 'parse': 0, 'jx': 0}

    def playerContent(self, flag, pid, vipFlags):
        play_url = 'https://gitee.com/dobebly/my_img/raw/c1977fa6134aefb8e5a34dabd731a4d186c84a4d/x.mp4'
        try:
            res = requests.get(f'{self.home_url}{pid}', headers=self.headers)
            datas = re.findall(r'player_aaaa=(.*?)</script>', res.text)
            if not datas:
                return {'url': play_url, 'parse': 0, 'jx': 0}
            data = json.loads(datas[0])
            url = data['url']
            return {'url': url, 'parse': 0, 'jx': 0, 'header': self.headers}
        except Exception as e:
            print(f"播放器內容錯誤: {e}")
            return {'url': play_url, 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        return None

    def destroy(self):
        return '正在銷毀'

    def get_data(self, payload):
        t = int(time.time())
        key = hashlib.md5(str(f'DS{t}DCC147D11943AF75').encode('utf-8')).hexdigest()
        url = self.home_url + "/index.php/api/vod"
        payload['time'] = str(t)
        payload['key'] = key
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Referer': "https://lreeok.vip/",
        }
        data = []
        try:
            res = requests.post(url, data=payload, headers=headers, timeout=10)
            print(f"API 響應: {res.text}")
            data_list = res.json()['list']
            for i in data_list:
                data.append({
                    'vod_id': i.get('vod_id', ''),
                    'vod_name': i.get('vod_name', ''),
                    'vod_pic': i.get('vod_pic', ''),
                    'vod_remarks': i.get('vod_remarks', ''),
                    'vod_class': i.get('vod_class', ''),
                    'vod_year': i.get('vod_year', ''),
                    'vod_actor': i.get('vod_actor', ''),
                    'vod_director': i.get('vod_director', ''),
                    'vod_content': i.get('vod_blurb', ''),
                    'vod_lang': i.get('vod_lang', '国语'),
                    'vod_area': i.get('vod_area', '大陆')
                })
            return data
        except Exception as e:
            print(f"API 請求錯誤: {e}")
            return data

if __name__ == '__main__':
    spider = Spider()
    
    # 測試《魔法壞女巫》
    print("\n測試《魔法壞女巫》:")
    detail = spider.detailContent(['26'])
    if detail['list']:
        print(f"vod_id: 26, vod_area: {detail['list'][0]['vod_area']}")

    # 測試《蕾拉》
    print("\n測試《蕾拉》:")
    detail = spider.detailContent(['108051'])
    if detail['list']:
        print(f"vod_id: 108051, vod_area: {detail['list'][0]['vod_area']}")

    # 測試全部地區
    print("\n測試全部地區:")
    result = spider.categoryContent('1', '1', True, {})
    for item in result['list']:
        vod_id = item['vod_id']
        detail = spider.detailContent([vod_id])
        if detail['list']:
            print(f"vod_id: {vod_id}, vod_area: {detail['list'][0]['vod_area']}")

    # 測試美國地區
    print("\n測試美國地區:")
    result = spider.categoryContent('1', '1', True, {'area': '美国'})
    for item in result['list']:
        vod_id = item['vod_id']
        detail = spider.detailContent([vod_id])
        if detail['list']:
            print(f"vod_id: {vod_id}, vod_area: {detail['list'][0]['vod_area']}")

    # 測試英國地區
    print("\n測試英國地區:")
    result = spider.categoryContent('1', '1', True, {'area': '英国'})
    for item in result['list']:
        vod_id = item['vod_id']
        detail = spider.detailContent([vod_id])
        if detail['list']:
            print(f"vod_id: {vod_id}, vod_area: {detail['list'][0]['vod_area']}")
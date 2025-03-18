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
        self.home_url = 'https://www.minijj.com'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }

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
                {'type_id': '2', 'type_name': '電視劇'},
                {'type_id': '4', 'type_name': '綜藝娛樂'},
                {'type_id': '3', 'type_name': '經典動漫'}
            ],
            'filters': {
                '1': [
                    {'name': '类型', 'key': 'type', 'value': [
                        {'n': '全部', 'v': '1'}, {'n': '動作片', 'v': '8'}, {'n': '喜劇片', 'v': '9'},
                        {'n': '愛情片', 'v': '10'}, {'n': '科幻片', 'v': '11'}, {'n': '恐怖片', 'v': '12'},
                        {'n': '戰爭片', 'v': '13'}, {'n': '劇情片', 'v': '14'}
                    ]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '大陸', 'v': 'dalu'}, {'n': '美國', 'v': 'meiguo'},
                        {'n': '香港', 'v': 'xianggang'}, {'n': '台灣', 'v': 'taiwan'}, {'n': '韓國', 'v': 'hanguo'},
                        {'n': '日本', 'v': 'riben'}, {'n': '泰國', 'v': 'taiguo'}, {'n': '新加坡', 'v': 'xinjiapo'},
                        {'n': '馬來西亞', 'v': 'malaixiya'}, {'n': '印度', 'v': 'yindu'}, {'n': '英國', 'v': 'yingguo'},
                        {'n': '法國', 'v': 'faguo'}, {'n': '加拿大', 'v': 'jianada'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2018', 'v': '2018'},
                        {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'}
                    ]}
                ],
                '2': [
                    {'name': '类型', 'key': 'type', 'value': [
                        {'n': '全部', 'v': '2'}, {'n': '大陸劇', 'v': '15'}, {'n': '香港劇', 'v': '16'},
                        {'n': '台灣劇', 'v': '918'}, {'n': '日劇', 'v': '18'}, {'n': '韓劇', 'v': '915'},
                        {'n': '美劇', 'v': '916'}, {'n': '英劇', 'v': '923'}, {'n': '歐美劇', 'v': '17'},
                        {'n': '泰劇', 'v': '922'}, {'n': '亞洲劇', 'v': '19'}
                    ]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '大陸', 'v': 'dalu'}, {'n': '美國', 'v': 'meiguo'},
                        {'n': '香港', 'v': 'xianggang'}, {'n': '台灣', 'v': 'taiwan'}, {'n': '韓國', 'v': 'hanguo'},
                        {'n': '日本', 'v': 'riben'}, {'n': '泰國', 'v': 'taiguo'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2018', 'v': '2018'},
                        {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'}
                    ]}
                ],
                '4': [
                    {'name': '类型', 'key': 'type', 'value': [
                        {'n': '全部', 'v': '4'}, {'n': '大陸綜藝', 'v': '911'}, {'n': '港台綜藝', 'v': '907'},
                        {'n': '韓綜', 'v': '908'}, {'n': '日綜', 'v': '912'}, {'n': '泰綜', 'v': '913'},
                        {'n': '歐美綜藝', 'v': '909'}
                    ]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '大陸', 'v': 'dalu'}, {'n': '香港', 'v': 'xianggang'},
                        {'n': '台灣', 'v': 'taiwan'}, {'n': '韓國', 'v': 'hanguo'}, {'n': '日本', 'v': 'riben'},
                        {'n': '泰國', 'v': 'taiguo'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2018', 'v': '2018'},
                        {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'}
                    ]}
                ],
                '3': [
                    {'name': '类型', 'key': 'type', 'value': [
                        {'n': '全部', 'v': '3'}, {'n': '國漫', 'v': '906'}, {'n': '日漫', 'v': '904'},
                        {'n': '美漫', 'v': '905'}, {'n': '其他動漫', 'v': '903'}
                    ]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '大陸', 'v': 'dalu'}, {'n': '美國', 'v': 'meiguo'},
                        {'n': '日本', 'v': 'riben'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2018', 'v': '2018'},
                        {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'}
                    ]}
                ]
            }
        }

    def homeVideoContent(self):
        data = self.get_data(self.home_url)
        return {'list': data, 'parse': 0, 'jx': 0, "倒序": "1"}

    def categoryContent(self, cid, page, filter, ext):
        type_id = ext.get('type', cid) if ext else cid
        area = ext.get('area', '') if ext else ''
        year = ext.get('year', '') if ext else ''
        print(f"ext: {ext}, type_id: {type_id}, area: {area}, year: {year}")
        url = f'{self.home_url}/lm/{type_id}/sx---{year}---{area}--{page}.html'
        print(f"Requesting URL: {url}")
        data = self.get_data(url)
        if not data:
            fallback_url = f'{self.home_url}/lm/{type_id}/{page}.html'
            print(f"Fallback URL: {fallback_url}")
            data = self.get_data(fallback_url)
        return {'list': data, 'parse': 0, 'jx': 0, "倒序": "1"}

    def detailContent(self, did):
        ids = did[0]
        video_list = []
        url = self.home_url + ids
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            vod_play_from = '$$$'.join(root.xpath('//ul[@class="nav nav-tabs"]/li/a/text()'))
            play_list = root.xpath('//ul[@class="list-unstyled text-center play-list"]')
            vod_play_url = []
            for i in play_list:
                name_list = i.xpath('./li/a/text()')
                url_list = i.xpath('./li/a/@href')
                episode_list = [_name + '$' + _url for _name, _url in zip(name_list, url_list)]
                reversed_episode_list = list(reversed(episode_list))
                vod_play_url.append('#'.join(reversed_episode_list))
            final_play_url = '$$$'.join(vod_play_url)
            vod_content = root.xpath('//p[@class="lead vod-content"]/text()')
            vod_content = vod_content[0] if vod_content else ''
            vod_name = root.xpath('//h1[@class="entry-title"]/text()')
            vod_name = vod_name[0] if vod_name else ''
            
            # 新增欄位提取（穩健版本）
            type_name = root.xpath('//meta[@name="og:video:class"]/@content')[0] if root.xpath('//meta[@name="og:video:class"]/@content') else ''
            vod_remarks = root.xpath('//h4/a/following-sibling::text()')[0].strip('[]') if root.xpath('//h4/a/following-sibling::text()') else ''
            vod_year_full = root.xpath('//dt[contains(text(), "開播")]/following-sibling::dd[1]/font/text()')[0] if root.xpath('//dt[contains(text(), "開播")]/following-sibling::dd[1]/font/text()') else ''
            vod_year = vod_year_full.split('年')[0] if vod_year_full else ''
            vod_area = root.xpath('//meta[@name="og:video:area"]/@content')[0] if root.xpath('//meta[@name="og:video:area"]/@content') else ''
            vod_actor = root.xpath('//meta[@name="og:video:actor"]/@content')[0] if root.xpath('//meta[@name="og:video:actor"]/@content') else ''
            vod_director = root.xpath('//meta[@name="og:video:director"]/@content')[0] if root.xpath('//meta[@name="og:video:director"]/@content') else '沐辰_为爱发电'

            video_list.append({
                'type_name': type_name,
                'vod_id': ids,
                'vod_name': vod_name,
                'vod_remarks': vod_remarks,
                'vod_year': vod_year,
                'vod_area': vod_area,
                'vod_actor': vod_actor,
                'vod_director': vod_director,
                'vod_content': vod_content,
                'vod_play_from': vod_play_from,
                'vod_play_url': final_play_url
            })
            print(f"detailContent result: {video_list}")
            return {"list": video_list, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"Error in detailContent: {e}")
            return {'list': [], 'msg': str(e)}

    def searchContent(self, key, quick, page='1'):
        url = self.home_url + f'/ss.html'
        if page != '1':
            return {'list': [], 'parse': 0, 'jx': 0, "倒序": "1"}
        try:
            res = requests.post(url, headers=self.headers, data={'wd': key})
            res.encoding = 'utf-8'
            data = self.get_data(res.text)
            return {'list': data, 'parse': 0, 'jx': 0, "倒序": "1"}
        except Exception as e:
            print(f"Error in searchContent: {e}")
            return {'list': [], 'parse': 0, 'jx': 0, "倒序": "1"}

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
            print(f"Error in playerContent: {e}")
            return {'url': play_url, 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

    def get_data(self, url_or_text):
        data = []
        try:
            if isinstance(url_or_text, str) and url_or_text.startswith('http'):
                res = requests.get(url_or_text, headers=self.headers)
                res.encoding = 'utf-8'
                root = etree.HTML(res.text)
            else:
                root = etree.HTML(url_or_text)
            data_list = root.xpath('//ul[@class="update_area_lists cl"]/li[@class="i_list list_n2"]')
            for i in data_list:
                vod_remarks = i.xpath('./div[@class="case_info"]/div[@class="meta-post"]/text()')
                data.append({
                    'vod_id': i.xpath('./a/@href')[0],
                    'vod_name': i.xpath('./div[@class="case_info"]/div[@class="meta-title"]/text()')[0],
                    'vod_pic': i.xpath('./a/img/@data-original')[0],
                    'vod_remarks': vod_remarks[0] if len(vod_remarks) > 0 else ''
                })
            return data
        except Exception as e:
            print(f"Error in get_data: {e}")
            return data

if __name__ == '__main__':
    pass
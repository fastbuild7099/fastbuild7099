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
    def __init__(self):
        self.home_url = 'https://lreeok.vip'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        self.detail_cache = {}

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
        # 不變，略
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
                    {'key': 'class', 'name': '类型', 'value': [{'n': '全部', 'v': ''}, {'n': '喜剧', 'v': '喜剧'}, {'n': '爱情', 'v': '爱情'}, {'n': '恐怖', 'v': '恐怖'}, {'n': '动作', 'v': '动作'}, {'n': '科幻', 'v': '科幻'}, {'n': '剧情', 'v': '剧情'}, {'n': '战争', 'v': '战争'}, {'n': '警匪', 'v': '警匪'}, {'n': '犯罪', 'v': '犯罪'}, {'n': '动画', 'v': '动画'}, {'n': '奇幻', 'v': '奇幻'}, {'n': '武侠', 'v': '武侠'}, {'n': '冒险', 'v': '冒险'}, {'n': '枪战', 'v': '枪战'}, {'n': '悬疑', 'v': '悬疑'}, {'n': '惊悚', 'v': '惊悚'}, {'n': '经典', 'v': '经典'}, {'n': '青春', 'v': '青春'}, {'n': '文艺', 'v': '文艺'}, {'n': '微电影', 'v': '微电影'}, {'n': '古装', 'v': '古装'}, {'n': '历史', 'v': '历史'}, {'n': '运动', 'v': '运动'}, {'n': '农村', 'v': '农村'}, {'n': '儿童', 'v': '儿童'}, {'n': '网络电影', 'v': '网络电影'}]},
                    {'key': 'area', 'name': '地区', 'value': [{'n': '全部', 'v': ''}, {'n': '大陆', 'v': '大陆'}, {'n': '香港', 'v': '香港'}, {'n': '台湾', 'v': '台湾'}, {'n': '美国', 'v': '美国'}, {'n': '法国', 'v': '法国'}, {'n': '英国', 'v': '英国'}, {'n': '日本', 'v': '日本'}, {'n': '韩国', 'v': '韩国'}, {'n': '德国', 'v': '德国'}, {'n': '泰国', 'v': '泰国'}, {'n': '印度', 'v': '印度'}, {'n': '意大利', 'v': '意大利'}, {'n': '西班牙', 'v': '西班牙'}, {'n': '加拿大', 'v': '加拿大'}, {'n': '其他', 'v': '其他'}]},
                    {'key': 'year', 'name': '年份', 'value': [{'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'}, {'n': '2014', 'v': '2014'}, {'n': '2013', 'v': '2013'}, {'n': '2012', 'v': '2012'}, {'n': '2011', 'v': '2011'}, {'n': '2010', 'v': '2010'}]},
                    {'key': 'lang', 'name': '语言', 'value': [{'n': '全部', 'v': ''}, {'n': '国语', 'v': '国语'}, {'n': '英语', 'v': '英语'}, {'n': '粤语', 'v': '粤语'}, {'n': '闽南语', 'v': '闽南语'}, {'n': '韩语', 'v': '韩语'}, {'n': '日语', 'v': '日语'}, {'n': '法语', 'v': '法语'}, {'n': '德语', 'v': '德语'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'by', 'name': '排序', 'value': [{'n': '按最新', 'v': 'time'}, {'n': '按最热', 'v': 'hits'}, {'n': '按评分', 'v': 'score'}]}
                ],
                # 其他類型 filters 略
            }
        }

    def homeVideoContent(self):
        # 不變，略
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
            print(f"homeVideoContent error: {e}")
            return {'list': [], 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        print(f"categoryContent called with cid={cid}, page={page}, filter={filter}, ext={ext}")
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
            'by': ext.get('by', '')
        }
        
        try:
            data = self.get_data(payload)
            print(f"從 API 取得的原始數據: {data}")
            
            if not data:
                return {'list': [], 'parse': 0, 'jx': 0}
                
            filtered_data = []
            for item in data:
                vod_id = item.get('vod_id', '')
                if vod_id not in self.detail_cache:
                    detail_result = self.detailContent([vod_id])
                    if detail_result['list']:
                        self.detail_cache[vod_id] = detail_result['list'][0]
                    else:
                        continue
                
                detail = self.detail_cache[vod_id]
                vod_class = item.get('vod_class', '')
                vod_area = detail.get('vod_area', '')
                vod_year = str(detail.get('vod_year', ''))
                vod_lang = detail.get('vod_lang', '')  # 使用新字段
                
                # 過濾條件
                class_match = not ext.get('class') or (vod_class and ext['class'] in vod_class)
                area_match = not ext.get('area') or (vod_area and ext['area'] in vod_area)
                year_match = not ext.get('year') or (vod_year and ext['year'] == vod_year)
                lang_match = not ext.get('lang') or (vod_lang and ext['lang'] in vod_lang)
                
                print(f"過濾項目 {item.get('vod_name', '未知')}: class_match={class_match}, area_match={area_match}, year_match={year_match}, lang_match={lang_match}")
                print(f"數據: class={vod_class}, area={vod_area}, year={vod_year}, lang={vod_lang}")
                
                if class_match and area_match and year_match and lang_match:
                    filtered_data.append({
                        'vod_id': vod_id,
                        'vod_name': detail.get('vod_name', item.get('vod_name', '')),
                        'vod_pic': item.get('vod_pic', ''),
                        'vod_remarks': detail.get('vod_remarks', item.get('vod_remarks', ''))
                    })
            
            print(f"過濾後的數據: {filtered_data}")
            return {'list': filtered_data, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"categoryContent error: {e}")
            return {'list': [], 'parse': 0, 'jx': 0}

    def detailContent(self, did):
        ids = did[0]
        video_list = []
        
        try:
            res = requests.get(f'{self.home_url}/voddetail/{ids}.html', headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            print(f"HTML content preview: {res.text[:500]}")

            # 改進標題提取
            vod_name = (root.xpath('//h1[@class="title"]/text()') or
                        root.xpath('//h3[@class="slide-info-title"]/text()') or
                        root.xpath('//title/text()') or [""])[0].strip()
            if ' - ' in vod_name:
                vod_name = vod_name.split(' - ')[0].strip()
            elif ',' in vod_name:
                vod_name = vod_name.split(',')[0].strip()
            print(f"Extracted vod_name: {vod_name}")

            # 提取年份、地區、備註、語言
            slide_info = root.xpath('//div[@class="slide-info hide"]')
            vod_year = slide_info[0].xpath('.//a/text()')[0] if slide_info and slide_info[0].xpath('.//a/text()') else ""
            vod_area = ""
            vod_remarks = ""
            vod_lang = ""
            for info in slide_info:
                label = info.xpath('.//strong/text()')[0] if info.xpath('.//strong/text()') else ""
                if "年份" in label:
                    vod_year = info.xpath('.//a/text()')[0] if info.xpath('.//a/text()') else ""
                elif "地区" in label:
                    vod_area = info.xpath('.//text()')[0].strip() if info.xpath('.//text()') else ""
                elif "备注" in label:
                    vod_remarks = info.xpath('.//text()')[0].strip() if info.xpath('.//text()') else "熱播中"
                elif "语言" in label:
                    vod_lang = info.xpath('.//text()')[0].strip() if info.xpath('.//text()') else ""
            # 如果語言未找到，根據演員名推測
            if not vod_lang:
                vod_actor = root.xpath('//div[@class="slide-info hide" and .//strong[contains(text(), "演员")]]//a/text()')
                vod_lang = "国语" if vod_actor and all(any(c >= '\u4e00' and c <= '\u9fff' for c in actor) for actor in vod_actor[:2]) else "未知"
            print(f"Extracted vod_year: {vod_year}, vod_area: {vod_area}, vod_remarks: {vod_remarks}, vod_lang: {vod_lang}")

            # 提取導演
            vod_director = ""
            director_slide = root.xpath('//div[@class="slide-info hide" and .//strong[contains(text(), "导演")]]//a/text()')
            if director_slide:
                vod_director = director_slide[0].strip()
            else:
                director_info = root.xpath('//div[@class="info-parameter"]//li[em[contains(text(), "导演")]]//a/text()')
                vod_director = director_info[0].strip() if director_info else "未知"
            print(f"Extracted vod_director: {vod_director}")

            # 提取主演
            actor_slide = root.xpath('//div[@class="slide-info hide" and .//strong[contains(text(), "演员")]]//a/text()')
            vod_actor = " / ".join([actor.strip() for actor in actor_slide]) if actor_slide else "未知"
            print(f"Extracted vod_actor: {vod_actor}")

            # 提取簡介
            vod_content = (root.xpath('//div[contains(@class, "content-desc")]/text()') or
                           root.xpath('//meta[@name="description"]/@content') or ["暫無簡介"])[0].strip()
            print(f"Extracted vod_content: {vod_content}")

            # 播放來源和鏈接
            vod_play_from = '$$$'.join(root.xpath('//div[@class="swiper-wrapper"]/a/text()') or [''])
            play_list = root.xpath('//ul[@class="anthology-list-play size"]')
            vod_play_url = []
            for i in play_list:
                name_list = i.xpath('./li/a/text()')
                url_list = i.xpath('./li/a/@href')
                vod_play_url.append('#'.join([f"{_name}${_url}" for _name, _url in zip(name_list, url_list)]))

            video_list.append({
                'type_name': '',
                'vod_id': ids,
                'vod_name': vod_name,
                'vod_remarks': vod_remarks,
                'vod_year': vod_year,
                'vod_area': vod_area,
                'vod_actor': vod_actor,
                'vod_director': vod_director,
                'vod_content': vod_content,
                'vod_lang': vod_lang,
                'vod_play_from': vod_play_from,
                'vod_play_url': '$$$'.join(vod_play_url)
            })
            return {"list": video_list, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"detailContent error: {e}")
            return {'list': [], 'msg': str(e)}

    def searchContent(self, key, quick, page='1'):
        # 不變，略
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
            print(f"searchContent error: {e}")
            return {'list': [], 'parse': 0, 'jx': 0}

    def playerContent(self, flag, pid, vipFlags):
        # 不變，略
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
                payload = {'url': url}
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
                    response = requests.post('https://www.lreeok.vip/okplay/api_config.php', data=payload, headers=headers)
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
                    print(f"playerContent api_config error: {e}")
                    return {'url': play_url, 'parse': 0, 'jx': 0}
            else:
                return {'url': url, 'parse': 0, 'jx': 0, 'header': self.headers}
        except requests.RequestException as e:
            print(f"playerContent error: {e}")
            return {'url': play_url, 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

    def get_data(self, payload):
        # 不變，略
        t = int(time.time())
        key = hashlib.md5(str(f'DS{t}DCC147D11943AF75').encode('utf-8')).hexdigest()
        url = self.home_url + "/index.php/api/vod"
        payload['time'] = str(t)
        payload['key'] = key
        print(f"Sending payload to {url}: {payload}")
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
            res = requests.post(url, data=payload, headers=headers, timeout=10)
            print(f"API response status: {res.status_code}")
            print(f"API response content: {res.text}")
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
                    'vod_content': i.get('vod_content', '')
                })
            return data
        except requests.RequestException as e:
            print(f"get_data request error: {e}")
            return data
        except json.JSONDecodeError as e:
            print(f"get_data JSON decode error: {e}, response text: {res.text}")
            return data
        except Exception as e:
            print(f"get_data unexpected error: {e}")
            return data


if __name__ == '__main__':
    spider = Spider()
    filters = {'class': '喜剧', 'area': '大陆', 'year': '2023', 'lang': '国语', 'by': 'time'}
    result = spider.categoryContent('1', 1, True, filters)
    print(f"Category test result: {result}")
    if result['list']:
        detail = spider.detailContent([result['list'][0]['vod_id']])
        print(f"Detail test result: {detail}")
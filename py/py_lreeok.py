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
from concurrent.futures import ThreadPoolExecutor

sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def __init__(self):
        """初始化爬蟲"""
        self.home_url = 'https://lreeok.vip'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        self.session = requests.Session()  # 重用 TCP 連接
        self.detail_cache = {}  # 詳情頁緩存
        self.api_cache = {}    # API 結果緩存

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
                '1': [  # 電影
                    {'key': 'class', 'name': '类型', 'value': [{'n': '全部', 'v': ''}, {'n': '喜剧', 'v': '喜剧'}, {'n': '爱情', 'v': '爱情'}, {'n': '恐怖', 'v': '恐怖'}, {'n': '动作', 'v': '动作'}, {'n': '科幻', 'v': '科幻'}, {'n': '剧情', 'v': '剧情'}, {'n': '战争', 'v': '战争'}, {'n': '警匪', 'v': '警匪'}, {'n': '犯罪', 'v': '犯罪'}, {'n': '动画', 'v': '动画'}, {'n': '奇幻', 'v': '奇幻'}, {'n': '武侠', 'v': '武侠'}, {'n': '冒险', 'v': '冒险'}, {'n': '枪战', 'v': '枪战'}, {'n': '悬疑', 'v': '悬疑'}, {'n': '惊悚', 'v': '惊悚'}, {'n': '经典', 'v': '经典'}, {'n': '青春', 'v': '青春'}, {'n': '文艺', 'v': '文艺'}, {'n': '微电影', 'v': '微电影'}, {'n': '古装', 'v': '古装'}, {'n': '历史', 'v': '历史'}, {'n': '运动', 'v': '运动'}, {'n': '农村', 'v': '农村'}, {'n': '儿童', 'v': '儿童'}, {'n': '网络电影', 'v': '网络电影'}]},
                    {'key': 'area', 'name': '地区', 'value': [{'n': '全部', 'v': ''}, {'n': '大陆', 'v': '大陆'}, {'n': '香港', 'v': '香港'}, {'n': '台湾', 'v': '台湾'}, {'n': '美国', 'v': '美国'}, {'n': '法国', 'v': '法国'}, {'n': '英国', 'v': '英国'}, {'n': '日本', 'v': '日本'}, {'n': '韩国', 'v': '韩国'}, {'n': '德国', 'v': '德国'}, {'n': '泰国', 'v': '泰国'}, {'n': '印度', 'v': '印度'}, {'n': '意大利', 'v': '意大利'}, {'n': '西班牙', 'v': '西班牙'}, {'n': '加拿大', 'v': '加拿大'}, {'n': '其他', 'v': '其他'}]},
                    {'key': 'year', 'name': '年份', 'value': [{'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'}, {'n': '2014', 'v': '2014'}, {'n': '2013', 'v': '2013'}, {'n': '2012', 'v': '2012'}, {'n': '2011', 'v': '2011'}, {'n': '2010', 'v': '2010'}]},
                    {'key': 'lang', 'name': '语言', 'value': [{'n': '全部', 'v': ''}, {'n': '国语', 'v': '国语'}, {'n': '英语', 'v': '英语'}, {'n': '粤语', 'v': '粤语'}, {'n': '闽南语', 'v': '闽南语'}, {'n': '韩语', 'v': '韩语'}, {'n': '日语', 'v': '日语'}, {'n': '法语', 'v': '法语'}, {'n': '德语', 'v': '德语'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'by', 'name': '排序', 'value': [{'n': '按最新', 'v': 'time'}, {'n': '按最热', 'v': 'hits'}, {'n': '按评分', 'v': 'score'}]}
                ],
                '2': [  # 連續劇
                    {'key': 'class', 'name': '类型', 'value': [{'n': '全部', 'v': ''}, {'n': '古装', 'v': '古装'}, {'n': '战争', 'v': '战争'}, {'n': '青春偶像', 'v': '青春偶像'}, {'n': '喜剧', 'v': '喜剧'}, {'n': '家庭', 'v': '家庭'}, {'n': '犯罪', 'v': '犯罪'}, {'n': '动作', 'v': '动作'}, {'n': '奇幻', 'v': '奇幻'}, {'n': '剧情', 'v': '剧情'}, {'n': '历史', 'v': '历史'}, {'n': '经典', 'v': '经典'}, {'n': '乡村', 'v': '乡村'}, {'n': '情景', 'v': '情景'}, {'n': '商战', 'v': '商战'}, {'n': '网剧', 'v': '网剧'}, {'n': '其他', 'v': '其他'}]},
                    {'key': 'area', 'name': '地区', 'value': [{'n': '全部', 'v': ''}, {'n': '内地', 'v': '内地'}, {'n': '韩国', 'v': '韩国'}, {'n': '香港', 'v': '香港'}, {'n': '台湾', 'v': '台湾'}, {'n': '日本', 'v': '日本'}, {'n': '美国', 'v': '美国'}, {'n': '泰国', 'v': '泰国'}, {'n': '英国', 'v': '英国'}, {'n': '新加坡', 'v': '新加坡'}, {'n': '其他', 'v': '其他'}]},
                    {'key': 'year', 'name': '年份', 'value': [{'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'}, {'n': '2014', 'v': '2014'}, {'n': '2013', 'v': '2013'}, {'n': '2012', 'v': '2012'}, {'n': '2011', 'v': '2011'}, {'n': '2010', 'v': '2010'}]},
                    {'key': 'lang', 'name': '语言', 'value': [{'n': '全部', 'v': ''}, {'n': '国语', 'v': '国语'}, {'n': '英语', 'v': '英语'}, {'n': '粤语', 'v': '粤语'}, {'n': '闽南语', 'v': '闽南语'}, {'n': '韩语', 'v': '韩语'}, {'n': '日语', 'v': '日语'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'by', 'name': '排序', 'value': [{'n': '按最新', 'v': 'time'}, {'n': '按最热', 'v': 'hits'}, {'n': '按评分', 'v': 'score'}]}
                ],
                '3': [  # 綜藝
                    {'key': 'class', 'name': '类型', 'value': [{'n': '全部', 'v': ''}, {'n': '选秀', 'v': '选秀'}, {'n': '情感', 'v': '情感'}, {'n': '访谈', 'v': '访谈'}, {'n': '播报', 'v': '播报'}, {'n': '旅游', 'v': '旅游'}, {'n': '音乐', 'v': '音乐'}, {'n': '美食', 'v': '美食'}, {'n': '纪实', 'v': '纪实'}, {'n': '曲艺', 'v': '曲艺'}, {'n': '生活', 'v': '生活'}, {'n': '游戏互动', 'v': '游戏互动'}, {'n': '财经', 'v': '财经'}, {'n': '求职', 'v': '求职'}]},
                    {'key': 'area', 'name': '地区', 'value': [{'n': '全部', 'v': ''}, {'n': '内地', 'v': '内地'}, {'n': '港台', 'v': '港台'}, {'n': '日韩', 'v': '日韩'}, {'n': '欧美', 'v': '欧美'}]},
                    {'key': 'year', 'name': '年份', 'value': [{'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'}, {'n': '2014', 'v': '2014'}, {'n': '2013', 'v': '2013'}, {'n': '2012', 'v': '2012'}, {'n': '2011', 'v': '2011'}, {'n': '2010', 'v': '2010'}]},
                    {'key': 'lang', 'name': '语言', 'value': [{'n': '全部', 'v': ''}, {'n': '国语', 'v': '国语'}, {'n': '英语', 'v': '英语'}, {'n': '粤语', 'v': '粤语'}, {'n': '闽南语', 'v': '闽南语'}, {'n': '韩语', 'v': '韩语'}, {'n': '日语', 'v': '日语'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'by', 'name': '排序', 'value': [{'n': '按最新', 'v': 'time'}, {'n': '按最热', 'v': 'hits'}, {'n': '按评分', 'v': 'score'}]}
                ],
                '4': [  # 動漫
                    {'key': 'class', 'name': '类型', 'value': [{'n': '全部', 'v': ''}, {'n': '情感', 'v': '情感'}, {'n': '科幻', 'v': '科幻'}, {'n': '热血', 'v': '热血'}, {'n': '推理', 'v': '推理'}, {'n': '搞笑', 'v': '搞笑'}, {'n': '冒险', 'v': '冒险'}, {'n': '萝莉', 'v': '萝莉'}, {'n': '校园', 'v': '校园'}, {'n': '动作', 'v': '动作'}, {'n': '机战', 'v': '机战'}, {'n': '运动', 'v': '运动'}, {'n': '战争', 'v': '战争'}, {'n': '少年', 'v': '少年'}, {'n': '少女', 'v': '少女'}, {'n': '社会', 'v': '社会'}, {'n': '原创', 'v': '原创'}, {'n': '亲子', 'v': '亲子'}, {'n': '益智', 'v': '益智'}, {'n': '励志', 'v': '励志'}, {'n': '其他', 'v': '其他'}]},
                    {'key': 'area', 'name': '地区', 'value': [{'n': '全部', 'v': ''}, {'n': '国产', 'v': '国产'}, {'n': '日本', 'v': '日本'}, {'n': '欧美', 'v': '欧美'}, {'n': '其他', 'v': '其他'}]},
                    {'key': 'year', 'name': '年份', 'value': [{'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'}, {'n': '2014', 'v': '2014'}, {'n': '2013', 'v': '2013'}, {'n': '2012', 'v': '2012'}, {'n': '2011', 'v': '2011'}, {'n': '2010', 'v': '2010'}]},
                    {'key': 'lang', 'name': '语言', 'value': [{'n': '全部', 'v': ''}, {'n': '国语', 'v': '国语'}, {'n': '英语', 'v': '英语'}, {'n': '粤语', 'v': '粤语'}, {'n': '闽南语', 'v': '闽南语'}, {'n': '韩语', 'v': '韩语'}, {'n': '日语', 'v': '日语'}, {'n': '其它', 'v': '其它'}]},
                    {'key': 'by', 'name': '排序', 'value': [{'n': '按最新', 'v': 'time'}, {'n': '按最热', 'v': 'hits'}, {'n': '按评分', 'v': 'score'}]}
                ],
                '5': [  # 短劇                     
                    {'key': 'year', 'name': '年份', 'value': [{'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'}, {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}, {'n': '2020', 'v': '2020'}, {'n': '2019', 'v': '2019'}, {'n': '2018', 'v': '2018'}, {'n': '2017', 'v': '2017'}, {'n': '2016', 'v': '2016'}, {'n': '2015', 'v': '2015'}, {'n': '2014', 'v': '2014'}, {'n': '2013', 'v': '2013'}, {'n': '2012', 'v': '2012'}, {'n': '2011', 'v': '2011'}, {'n': '2010', 'v': '2010'}]},
                    {'key': 'by', 'name': '排序', 'value': [{'n': '按最新', 'v': 'time'}, {'n': '按最热', 'v': 'hits'}, {'n': '按评分', 'v': 'score'}]}
                ]
            }
        }

    def homeVideoContent(self):
        d = []
        try:
            res = self.session.get(self.home_url, headers=self.headers)
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

    def categoryContent(self, cid, page, filter_flag, ext):
        """獲取分類頁內容，優化篩選速度並修復異常"""
        print(f"分類內容調用: cid={cid}, page={page}, filter_flag={filter_flag}, ext={ext}")
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
            # 獲取數據並使用緩存
            data = self.get_data(payload)
            print(f"從 API 獲取的原始數據: {data}")
            
            if not data:
                return {'list': [], 'parse': 0, 'jx': 0}

            # 並行過濾數據
            def filter_item(item):
                try:
                    vod_id = str(item.get('vod_id', ''))
                    vod_class = item.get('vod_class', '')
                    vod_year = item.get('vod_year', '')  # API 未提供，後續補充
                    vod_area = ''  # API 未提供，假設大陸
                    vod_lang = '国语'  # API 未提供，假設國語
                    
                    if vod_id not in self.detail_cache:
                        self.detail_cache[vod_id] = {}
                    
                    class_match = not ext.get('class') or (vod_class and ext['class'] in vod_class)
                    area_match = not ext.get('area') or vod_area == ext['area'] or not vod_area
                    year_match = not ext.get('year') or vod_year == ext['year'] or not vod_year
                    lang_match = not ext.get('lang') or vod_lang == ext['lang'] or not vod_lang
                    
                    print(f"過濾項目 {item.get('vod_name', '未知')}: class_match={class_match}, area_match={area_match}, year_match={year_match}, lang_match={lang_match}")
                    
                    if class_match and area_match and year_match and lang_match:
                        return {
                            'vod_id': vod_id,
                            'vod_name': item.get('vod_name', ''),
                            'vod_pic': item.get('vod_pic', ''),
                            'vod_remarks': item.get('vod_remarks', '')
                        }
                    return None
                except Exception as e:
                    print(f"過濾項目 {item.get('vod_name', '未知')} 時出錯: {e}")
                    return None

            # 使用多線程過濾，避免 filter 命名衝突
            with ThreadPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(filter_item, data))
            filtered_data = [item for item in results if item is not None]
            
            # 僅對前幾個項目獲取詳情（可根據需求調整）
            if filtered_data:
                with ThreadPoolExecutor(max_workers=8) as executor:
                    executor.map(lambda x: self.detailContent([x['vod_id']]), filtered_data[:5])  # 只處理前 5 個
            
            print(f"過濾後的數據: {filtered_data}")
            return {'list': filtered_data, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"分類內容獲取錯誤: {e}")
            return {'list': [], 'parse': 0, 'jx': 0}

    def detailContent(self, did):
        """獲取視頻詳情頁內容"""
        ids = did[0]
        video_list = []
        
        try:
            res = self.session.get(f'{self.home_url}/voddetail/{ids}.html', headers=self.headers, timeout=3)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            print(f"HTML 內容預覽: {res.text[:500]}")
            api_data = self.detail_cache.get(ids, {})

            def extract_fallback(root, xpath, default=""):
                result = root.xpath(xpath)
                return result[0].strip() if result else default

            vod_name = extract_fallback(root, '//h3[@class="slide-info-title hide"]/text()', api_data.get('vod_name', ''))
            if not vod_name:
                title = extract_fallback(root, '//title/text()')
                vod_name = title.split('》')[0] + '》' if '《' in title and '》' in title else title
            print(f"提取的標題: {vod_name}")

            vod_pic = extract_fallback(root, '//div[contains(@class, "vod-img")]//img/@data-src', api_data.get('vod_pic', ''))
            vod_year = extract_fallback(root, '//div[@class="info-parameter"]//li[contains(., "年份")]/span/text()', api_data.get('vod_year', '2023'))
            vod_area = extract_fallback(root, '//div[@class="info-parameter"]//li[contains(., "地区")]/text()', api_data.get('vod_area', '大陆'))
            vod_remarks = extract_fallback(root, '//div[@class="info-parameter"]//li[contains(., "状态")]/span/text()', api_data.get('vod_remarks', ''))
            vod_director = " / ".join(root.xpath('//div[@class="info-parameter"]//li[contains(., "导演")]/text()[last()]')) if root.xpath('//div[@class="info-parameter"]//li[contains(., "导演")]/text()[last()]') else api_data.get('vod_director', '')
            vod_actor = " / ".join(root.xpath('//div[@class="info-parameter"]//li[contains(., "主演")]/a/text()')) if root.xpath('//div[@class="info-parameter"]//li[contains(., "主演")]/a/text()') else api_data.get('vod_actor', '')
            vod_class = api_data.get('vod_class', '')
            vod_lang = extract_fallback(root, '//div[@class="info-parameter"]//li[contains(., "语言")]/text()', api_data.get('vod_lang', '国语'))
            vod_content = extract_fallback(root, '//div[@class="info-parameter"]//li[contains(., "简介")]/text()', api_data.get('vod_content', '暫無簡介'))

            play_from, play_url = [], []
            anthology_tabs = root.xpath('//div[@class="anthology-tab nav-swiper b-b br"]//a/text()')
            anthology_boxes = root.xpath('//div[@class="anthology-list-box none"]')

            for i, box in enumerate(anthology_boxes):
                if i < len(anthology_tabs):
                    source_name = anthology_tabs[i].strip().replace("\xa0", "").replace(" ", "")
                    source_name = re.sub(r'<[^>]+>', '', source_name)
                else:
                    source_name = f"線路{i+1}"
                play_from.append(source_name)

                urls = box.xpath('.//a/@href')
                titles = box.xpath('.//a/text()')
                play_url.append("#".join([f"{t.strip()}${u}" for t, u in zip(titles, urls)]))

            vod_play_from = "$$$".join(play_from)
            vod_play_url = "$$$".join(play_url)
            if not play_from:
                print(f"警告: 未找到 vod_id {ids} 的播放來源")

            print(f"提取的年份: {vod_year}, 地區: {vod_area}, 狀態: {vod_remarks}, 語言: {vod_lang}")
            print(f"提取的導演: {vod_director}")
            print(f"提取的主演: {vod_actor}")
            print(f"提取的簡介: {vod_content}")
            print(f"提取的播放來源: {vod_play_from}")
            print(f"提取的播放 URL: {vod_play_url}")

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

            self.detail_cache[ids] = video_list[0]
            result = {'list': video_list, 'parse': 0, 'jx': 0}
            print(f"詳情測試結果: {result}")
            return result
        except Exception as e:
            print(f"詳情內容獲取錯誤: {e}")
            return {'list': [], 'msg': str(e)}

    def searchContent(self, key, quick, page='1'):
        d = []
        url = self.home_url + f'/index.php/ajax/suggest?mid=1&wd={key}'
        if page != '1':
            return {'list': [], 'parse': 0, 'jx': 0}
        try:
            res = self.session.get(url, headers=self.headers)
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
            res = self.session.get(f'{self.home_url}{pid}', headers=self.headers)
            datas = re.findall(r'player_aaaa=(.*?)</script>', res.text)
            if not datas:
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
                response = self.session.post('https://www.lreeok.vip/okplay/api_config.php', data=payload, headers=headers)
                data = response.json()
                if data['code'] != '200':
                    return {'url': play_url, 'parse': 0, 'jx': 0}
                h = {'User-Agent': data['user-agent'], 'Referer': data['referer']}
                url = data['url']
                return {'url': url, 'parse': 0, 'jx': 0, 'header': h}
            else:
                return {'url': url, 'parse': 0, 'jx': 0, 'header': self.headers}
        except requests.RequestException as e:
            print(f"播放器內容錯誤: {e}")
            return {'url': play_url, 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        pass

    def destroy(self):
        self.session.close()
        return '正在銷毀'

    def get_data(self, payload):
        """優化 API 數據獲取，使用緩存"""
        t = int(time.time())
        key = hashlib.md5(str(f'DS{t}DCC147D11943AF75').encode('utf-8')).hexdigest()
        url = self.home_url + "/index.php/api/vod"
        payload['time'] = str(t)
        payload['key'] = key
        
        # 生成緩存鍵
        cache_key = hashlib.md5(str(payload).encode('utf-8')).hexdigest()
        if cache_key in self.api_cache:
            print(f"從緩存中獲取數據: {cache_key}")
            return self.api_cache[cache_key]

        print(f"發送到 {url} 的數據: {payload}")
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
            res = self.session.post(url, data=payload, headers=headers, timeout=5)
            print(f"API 響應狀態: {res.status_code}")
            print(f"API 響應內容: {res.text}")
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
                    'vod_content': i.get('vod_blurb', '')
                })
            self.api_cache[cache_key] = data
            return data
        except Exception as e:
            print(f"API 請求錯誤: {e}")
            return data

if __name__ == '__main__':
    spider = Spider()
    filters = {'class': '喜剧', 'area': '大陆', 'year': '2023', 'lang': '国语', 'by': 'time'}
    result = spider.categoryContent('1', 1, True, filters)
    print(f"分類測試結果: {result}")
    if result['list']:
        detail = spider.detailContent([result['list'][0]['vod_id']])
        print(f"詳情測試結果: {detail}")
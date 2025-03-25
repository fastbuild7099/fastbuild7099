# -*- coding: utf-8 -*-
# @Author  : Adapted for keke7.app
# @Time    : 2025/3/19

import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse  # 用於 URL 編碼
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def getName(self):
        return "可可影视"

    def init(self, extend):
        self.home_url = 'https://www.keke7.app'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://www.keke7.app/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        }
        self.image_domain = "https://vres.wbadl.cn"  # 圖片域名

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def homeContent(self, filter):
        result = {
            'class': [
                {'type_id': '1', 'type_name': '电影'},
                {'type_id': '2', 'type_name': '剧集'},
                {'type_id': '4', 'type_name': '综艺'},
                {'type_id': '3', 'type_name': '动漫'},
                {'type_id': '6', 'type_name': '短剧'}
            ],
            'filters': {
                '1': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '剧情', 'v': '剧情'},
                        {'n': '喜剧', 'v': '喜剧'},
                        {'n': '动作', 'v': '动作'}, 
                        {'n': '爱情', 'v': '爱情'},
                        {'n': '恐怖', 'v': '恐怖'}, 
                        {'n': '惊悚', 'v': '惊悚'}, 
                        {'n': '犯罪', 'v': '犯罪'},
                        {'n': '科幻', 'v': '科幻'}, 
                        {'n': '悬疑', 'v': '悬疑'},
                        {'n': '奇幻', 'v': '奇幻'},
                        {'n': '冒险', 'v': '冒险'},
                        {'n': '战争', 'v': '战争'},
                        {'n': '历史', 'v': '历史'},
                        {'n': '古装', 'v': '古装'},
                        {'n': '家庭', 'v': '家庭'},
                        {'n': '武侠', 'v': '武侠'},
                        {'n': '歌舞', 'v': '歌舞'},
                        {'n': '动画', 'v': '动画'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''}, 
                        {'n': '大陆', 'v': '中国大陆'}, 
                        {'n': '香港', 'v': '中国香港'},
                        {'n': '台湾', 'v': '中国台湾'}, 
                        {'n': '美国', 'v': '美国'}, 
                        {'n': '日本', 'v': '日本'},
                        {'n': '韩国', 'v': '韩国'}, 
                        {'n': '英国', 'v': '英国'}, 
                        {'n': '法国', 'v': '法国'}]},
                    {'name': '语言', 'key': 'language', 'value': [  # 新增語言篩選
                        {'n': '全部', 'v': ''},
                        {'n': '国语', 'v': '国语'},
                        {'n': '英语', 'v': '英语'},
                        {'n': '粤语', 'v': '粤语'},
                        {'n': '日语', 'v': '日语'},
                        {'n': '韩语', 'v': '韩语'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''}, 
                        {'n': '2025', 'v': '2025'}, 
                        {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, 
                        {'n': '2022', 'v': '2022'}, 
                        {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'}, 
                        {'n': '10年代', 'v': '2010_2019'}, 
                        {'n': '00年代', 'v': '2000_2009'},
                        {'n': '90年代', 'v': '1990_1999'},
                        {'n': '80年代', 'v': '1980_1989'},
                        {'n': '更早', 'v': '0_1979'}
                    ]},
                    {'name': '排序', 'key': 'by', 'value': [
                        {'n': '綜合排序', 'v': '1'},
                        {'n': '按時間', 'v': '2'},
                        {'n': '按熱度', 'v': '3'},
                        {'n': '按評分', 'v': '4'}
                    ]}
                ],
                '2': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''}, 
                        {'n': '剧情', 'v': '剧情'},
                        {'n': '爱情', 'v': '爱情'}, 
                        {'n': '喜剧', 'v': '喜剧'}, 
                        {'n': '犯罪', 'v': '犯罪'},
                        {'n': '悬疑', 'v': '悬疑'}, 
                        {'n': '古装', 'v': '古装'}, 
                        {'n': '动作', 'v': '动作'},
                        {'n': '家庭', 'v': '家庭'},
                        {'n': '惊悚', 'v': '惊悚'},
                        {'n': '奇幻', 'v': '奇幻'},
                        {'n': '美剧', 'v': '美剧'},
                        {'n': '韩剧', 'v': '韩剧'},
                        {'n': '科幻', 'v': '科幻'},
                        {'n': '历史', 'v': '历史'},
                        {'n': '战争', 'v': '战争'},
                        {'n': '武侠', 'v': '武侠'},
                        {'n': '言情', 'v': '言情'},
                        {'n': '恐怖', 'v': '恐怖'},
                        {'n': '冒险', 'v': '冒险'},
                        {'n': '都市', 'v': '都市'},
                        {'n': '职场', 'v': '职场'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''}, 
                        {'n': '大陆', 'v': '中国大陆'}, 
                        {'n': '香港', 'v': '中国香港'},
                        {'n': '台湾', 'v': '中国台湾'}, 
                        {'n': '美国', 'v': '美国'}, 
                        {'n': '日本', 'v': '日本'},
                        {'n': '韩国', 'v': '韩国'}, 
                        {'n': '英国', 'v': '英国'}, 
                        {'n': '法国', 'v': '法国'}]},
                    {'name': '语言', 'key': 'language', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '国语', 'v': '国语'},
                        {'n': '英语', 'v': '英语'},
                        {'n': '粤语', 'v': '粤语'},
                        {'n': '日语', 'v': '日语'},
                        {'n': '韩语', 'v': '韩语'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''}, 
                        {'n': '2025', 'v': '2025'}, 
                        {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, 
                        {'n': '2022', 'v': '2022'}, 
                        {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'}, 
                        {'n': '10年代', 'v': '2010_2019'}, 
                        {'n': '00年代', 'v': '2000_2009'},
                        {'n': '90年代', 'v': '1990_1999'},
                        {'n': '80年代', 'v': '1980_1989'},
                        {'n': '更早', 'v': '0_1979'}
                    ]},
                    {'name': '排序', 'key': 'by', 'value': [
                        {'n': '綜合排序', 'v': '1'},
                        {'n': '按時間', 'v': '2'},
                        {'n': '按熱度', 'v': '3'},
                        {'n': '按評分', 'v': '4'}
                    ]}
                ],
                '3': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''}, 
                        {'n': '动态漫画', 'v': '动态漫画'}, 
                        {'n': '剧情', 'v': '剧情'},
                        {'n': '动画', 'v': '动画'}, 
                        {'n': '喜剧', 'v': '喜剧'}, 
                        {'n': '冒险', 'v': '冒险'},
                        {'n': '动作', 'v': '动作'},
                        {'n': '奇幻', 'v': '奇幻'},
                        {'n': '科幻', 'v': '科幻'},
                        {'n': '儿童', 'v': '儿童'},
                        {'n': '搞笑', 'v': '搞笑'},
                        {'n': '爱情', 'v': '爱情'},
                        {'n': '家庭', 'v': '家庭'},
                        {'n': '短片', 'v': '短片'},
                        {'n': '热血', 'v': '热血'},
                        {'n': '益智', 'v': '益智'},
                        {'n': '悬疑', 'v': '悬疑'},
                        {'n': '经典', 'v': '经典'},
                        {'n': '校园', 'v': '校园'},
                        {'n': 'Anime', 'v': 'Anime'},
                        {'n': '运动', 'v': '运动'},
                        {'n': '亲子', 'v': '亲子'},
                        {'n': '青春', 'v': '青春'},
                        {'n': '恋爱', 'v': '恋爱'},
                        {'n': '武侠', 'v': '武侠'},
                        {'n': '惊悚', 'v': '惊悚'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''}, 
                        {'n': '大陆', 'v': '中国大陆'}, 
                        {'n': '香港', 'v': '中国香港'},
                        {'n': '台湾', 'v': '中国台湾'}, 
                        {'n': '美国', 'v': '美国'}, 
                        {'n': '日本', 'v': '日本'},
                        {'n': '韩国', 'v': '韩国'}, 
                        {'n': '英国', 'v': '英国'}, 
                        {'n': '法国', 'v': '法国'}]},
                    {'name': '语言', 'key': 'language', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '国语', 'v': '国语'},
                        {'n': '英语', 'v': '英语'},
                        {'n': '粤语', 'v': '粤语'},
                        {'n': '日语', 'v': '日语'},
                        {'n': '韩语', 'v': '韩语'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''}, 
                        {'n': '2025', 'v': '2025'}, 
                        {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, 
                        {'n': '2022', 'v': '2022'}, 
                        {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'}, 
                        {'n': '10年代', 'v': '2010_2019'}, 
                        {'n': '00年代', 'v': '2000_2009'},
                        {'n': '90年代', 'v': '1990_1999'},
                        {'n': '80年代', 'v': '1980_1989'},
                        {'n': '更早', 'v': '0_1979'}
                    ]},
                    {'name': '排序', 'key': 'by', 'value': [
                        {'n': '綜合排序', 'v': '1'},
                        {'n': '按時間', 'v': '2'},
                        {'n': '按熱度', 'v': '3'},
                        {'n': '按評分', 'v': '4'}
                    ]}
                ],
                '4': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''}, 
                        {'n': '纪录', 'v': '纪录'}, 
                        {'n': '真人秀', 'v': '真人秀'},
                        {'n': '脱口秀', 'v': '脱口秀'}, 
                        {'n': '剧情', 'v': '剧情'}, 
                        {'n': '历史', 'v': '历史'},
                        {'n': '喜剧', 'v': '喜剧'}, 
                        {'n': '传记', 'v': '传记'}, 
                        {'n': '相声', 'v': '相声'},
                        {'n': '节目', 'v': '节目'},
                        {'n': '运动', 'v': '运动'},
                        {'n': '犯罪', 'v': '犯罪'},
                        {'n': '短片', 'v': '短片'},
                        {'n': '搞笑', 'v': '搞笑'},
                        {'n': '晚会', 'v': '晚会'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''}, 
                        {'n': '大陆', 'v': '中国大陆'}, 
                        {'n': '香港', 'v': '中国香港'},
                        {'n': '台湾', 'v': '中国台湾'}, 
                        {'n': '美国', 'v': '美国'}, 
                        {'n': '日本', 'v': '日本'},
                        {'n': '韩国', 'v': '韩国'}, 
                        {'n': '英国', 'v': '英国'}, 
                        {'n': '法国', 'v': '法国'}]},
                    {'name': '语言', 'key': 'language', 'value': [
                        {'n': '全部', 'v': ''},
                        {'n': '国语', 'v': '国语'},
                        {'n': '英语', 'v': '英语'},
                        {'n': '粤语', 'v': '粤语'},
                        {'n': '日语', 'v': '日语'},
                        {'n': '韩语', 'v': '韩语'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''}, 
                        {'n': '2025', 'v': '2025'}, 
                        {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, 
                        {'n': '2022', 'v': '2022'}, 
                        {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'}, 
                        {'n': '10年代', 'v': '2010_2019'}, 
                        {'n': '00年代', 'v': '2000_2009'},
                        {'n': '90年代', 'v': '1990_1999'},
                        {'n': '80年代', 'v': '1980_1989'},
                        {'n': '更早', 'v': '0_1979'}
                    ]},
                    {'name': '排序', 'key': 'by', 'value': [
                        {'n': '綜合排序', 'v': '1'},
                        {'n': '按時間', 'v': '2'},
                        {'n': '按熱度', 'v': '3'},
                        {'n': '按評分', 'v': '4'}
                    ]}
                ],
                '6': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''}, 
                        {'n': '逆袭', 'v': '逆袭'}, 
                        {'n': '甜宠', 'v': '甜宠'},
                        {'n': '虐恋', 'v': '虐恋'}, 
                        {'n': '穿越', 'v': '穿越'}, 
                        {'n': '重生', 'v': '重生'},
                        {'n': '剧情', 'v': '剧情'}, 
                        {'n': '科幻', 'v': '科幻'}, 
                        {'n': '武侠', 'v': '武侠'},
                        {'n': '动作', 'v': '动作'},
                        {'n': '爱情', 'v': '爱情'},
                        {'n': '战争', 'v': '战争'},
                        {'n': '冒险', 'v': '冒险'},
                        {'n': '其它', 'v': '其它'}]},
                    {'name': '排序', 'key': 'by', 'value': [
                        {'n': '綜合排序', 'v': '1'},
                        {'n': '按時間', 'v': '2'},
                        {'n': '按熱度', 'v': '3'},
                        {'n': '按評分', 'v': '4'}
                    ]}
                ]
            }
        }
        print(f"Debug homeContent: {result}")
        return result

    def homeVideoContent(self):
        data = self.get_data(self.home_url)
        result = {'list': data, 'parse': 0, 'jx': 0, "倒序": "1"}
        print(f"Debug homeVideoContent: {result}")
        return result

    def categoryContent(self, cid, page, filter, ext):
        cate_id = ext.get('cateId', cid) if ext and 'cateId' in ext else cid
        class_filter = ext.get('class', '') if ext and 'class' in ext else ''
        area = ext.get('area', '') if ext and 'area' in ext else ''
        language = ext.get('language', '') if ext and 'language' in ext else ''  # 新增語言參數
        year = ext.get('year', '') if ext and 'year' in ext else ''
        by = ext.get('by', '1') if ext and 'by' in ext else '1'
        # URL 編碼中文參數
        class_filter = urllib.parse.quote(class_filter.encode('utf-8')) if class_filter else ''
        area = urllib.parse.quote(area.encode('utf-8')) if area else ''
        language = urllib.parse.quote(language.encode('utf-8')) if language else ''
        url = f'{self.home_url}/show/{cate_id}-{class_filter}-{area}-{language}-{year}-{by}-{page}.html'
        print(f"Debug: Requesting URL: {url}")
        data = self.get_data(url)
        result = {'list': data, 'parse': 0, 'jx': 0, "倒序": "1"}
        print(f"Debug categoryContent: {result}")
        return result

    def detailContent(self, did):
        ids = did[0] if did else ''
        if not ids:
            return {'list': [], 'msg': 'No ID provided'}
        
        video_list = []
        url = self.home_url + ids
        try:
            res = requests.get(url, headers=self.headers)
            if res.status_code != 200:
                print(f"Debug: Failed to fetch URL {url}, status code: {res.status_code}")
                return {'list': [], 'msg': f'HTTP Error: {res.status_code}'}
            
            soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')
            
            # 提取播放線路
            source_items = soup.select('div.source-item span.source-item-label')
            if not source_items:
                print(f"Debug: No source items found for URL: {url}")
                print(f"Debug: HTML snippet: {str(soup.select('div.source-box')[:1000])}")
                vod_play_from = "未找到播放線路"
            else:
                vod_play_from = '$$$'.join([span.text for span in source_items])
                print(f"Debug: Found source items: {vod_play_from}")
            
            # 提取集數列表（只選取非隱藏的）
            play_lists = soup.select('div.episode-list:not([style="display: none;"])')
            if not play_lists:
                print(f"Debug: No visible episode lists found for URL: {url}")
                vod_play_url = ["未找到集數"]
            else:
                vod_play_url = []
                for i, play_list in enumerate(play_lists):
                    episode_names = [a.text for a in play_list.select('a')]
                    episode_urls = [a['href'] for a in play_list.select('a')]
                    if episode_names and episode_urls:
                        episode_list = [f"{name}${self.home_url}{episode_url}" for name, episode_url in zip(episode_names, episode_urls)]
                        vod_play_url.append('#'.join(episode_list))
                    else:
                        print(f"Debug: Episode list {i} is empty")
                final_play_url = '$$$'.join(vod_play_url) if vod_play_url else "未找到播放地址"
                print(f"Debug: Found play URLs: {final_play_url}")
            
            # 其他元數據提取
            vod_name = soup.select_one('h1').text if soup.select_one('h1') else ''
            vod_content = soup.select_one('div.detail-desc').text if soup.select_one('div.detail-desc') else ''
            tags = soup.select('div.detail-tags-item')
            vod_year = tags[0].text if tags else ''
            vod_area = tags[1].text if len(tags) > 1 else ''
            vod_actor = soup.find('div', string='演员:').find_next('div').text if soup.find('div', string='演员:') else ''
            vod_director = soup.find('div', string='导演:').find_next('div').text if soup.find('div', string='导演:') else ''
            vod_remarks = soup.find('div', string='备注:').find_next('div').text if soup.find('div', string='备注:') else ''
            
            type_name = ''
            if ids.startswith('/detail/'):
                parts = ids.split('/')
                if len(parts) > 2:
                    type_name = parts[2]
            
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
            print(f"Debug detailContent result: {video_list}")
            return {"list": video_list, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"Error in detailContent: {e}")
            return {'list': [], 'msg': str(e)}

    def searchContent(self, key, quick, page='1'):
        url = f'{self.home_url}/search?k={key}&page={page}'
        try:
            res = requests.get(url, headers=self.headers)
            data = self.get_data(res.content)
            result = {'list': data, 'parse': 0, 'jx': 0, "倒序": "1"}
            print(f"Debug searchContent: {result}")
            return result
        except Exception as e:
            print(f"Error in searchContent: {e}")
            return {'list': [], 'parse': 0, 'jx': 0, "倒序": "1"}

    def playerContent(self, flag, pid, vipFlags):
        url = self.home_url + pid
        try:
            res = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')
            play_url = soup.select_one('video')['src'] if soup.select_one('video') else 'https://example.com/default.mp4'
            result = {'url': play_url, 'parse': 0, 'jx': 0}
            print(f"Debug playerContent: {result}")
            return result
        except Exception as e:
            print(f"Error in playerContent: {e}")
            return {'url': 'https://example.com/default.mp4', 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

    def get_data(self, url_or_text):
        data = []
        try:
            if isinstance(url_or_text, str) and url_or_text.startswith('http'):
                res = requests.get(url_or_text, headers=self.headers)
                if res.status_code != 200:
                    print(f"Debug: Failed to fetch URL {url_or_text}, status code: {res.status_code}")
                    print(f"Debug: Response content: {res.text[:1000]}")
                    return data
                soup = BeautifulSoup(res.content, 'html.parser', from_encoding='utf-8')
            else:
                soup = BeautifulSoup(url_or_text, 'html.parser', from_encoding='utf-8')
            
            # 提取影片列表
            items = soup.select('a.v-item')
            if not items:
                print(f"Debug: No items found in HTML for URL: {url_or_text}")
                print(f"Debug: HTML snippet: {str(soup)[:2000]}")
            for item in items:
                vod_id = item['href'] if 'href' in item.attrs else ''
                vod_name = item.select_one('div.v-item-title:not([style="display: none"])').text if item.select_one('div.v-item-title:not([style="display: none"])') else '未找到標題'
                
                img_tags = [img['data-original'] for img in item.select('div.v-item-cover img')]
                vod_pic = self.image_domain + img_tags[1] if len(img_tags) > 1 else self.image_domain + img_tags[0] if img_tags else ''
                vod_remarks = item.select_one('div.v-item-bottom span').text if item.select_one('div.v-item-bottom span') else ''
                
                data.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name.strip(),
                    'vod_pic': vod_pic,
                    'vod_remarks': vod_remarks
                })
            print(f"Debug get_data result: {data}")
            return data
        except Exception as e:
            print(f"Error in get_data: {e}")
            return data

if __name__ == '__main__':
    spider = Spider()
    spider.init({})
    # 測試首頁內容
    print(spider.homeContent(True))
    # 測試分類內容（模擬提供的完整鏈接）
    print(spider.categoryContent('1', '3', True, {'class': '喜剧', 'area': '美国', 'language': '国语', 'year': '2024', 'by': '2'}))
    # 其他測試
    print(spider.categoryContent('1', '1', True, {'year': '2023', 'by': '1'}))
    print(spider.categoryContent('1', '1', True, {'year': '2019', 'by': '3'}))
    print(spider.categoryContent('1', '1', True, {'year': '更早', 'by': '4'}))
    # 測試搜索
    print(spider.searchContent('test', False, '1'))
    # 測試詳情頁
    print(spider.detailContent(['/detail/264550.html']))
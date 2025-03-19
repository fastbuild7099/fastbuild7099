# -*- coding: utf-8 -*-
# @Author  : Adapted for keke7.app
# @Time    : 2025/3/20

import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import re
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
        self.image_domain = "https://vres.wbadl.cn"

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
            # filters 保持不變，省略以節省空間
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
        language = ext.get('language', '') if ext and 'language' in ext else ''
        year = ext.get('year', '') if ext and 'year' in ext else ''
        by = ext.get('by', '1') if ext and 'by' in ext else '1'
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
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            service = Service(executable_path='D:/PyramidStore/chromedriver.exe')
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            driver.get(url)
            driver.implicitly_wait(10)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            driver.quit()
            
            # 使用正則表達式提取播放線路
            pattern = r'<span class="source-item-label">([^<]+)</span>'
            source_items = re.findall(pattern, html)
            if not source_items:
                print(f"Debug: No source items found for URL: {url}")
                print(f"Debug: HTML snippet: {str(soup.select('div.source-box')[:1000])}")
                vod_play_from = "未找到播放線路"
            else:
                vod_play_from = '$$$'.join(source_items)
                print(f"Debug: Found source items: {vod_play_from}")
            
            # 提取所有集數列表
            play_lists = soup.select('div.episode-list')
            if not play_lists:
                print(f"Debug: No episode lists found for URL: {url}")
                vod_play_url = "未找到播放地址"
            else:
                vod_play_url = []
                for i, play_list in enumerate(play_lists):
                    episode_names = [a.text.strip() for a in play_list.select('a.episode-item')]
                    episode_urls = [a['href'] for a in play_list.select('a.episode-item')]
                    if episode_names and episode_urls:
                        episode_list = [f"{name}${self.home_url}{url}" for name, url in zip(episode_names, episode_urls)]
                        vod_play_url.append('#'.join(episode_list))
                    else:
                        print(f"Debug: Episode list {i} is empty")
                vod_play_url = '$$$'.join(vod_play_url) if vod_play_url else "未找到播放地址"
                print(f"Debug: Found play URLs: {vod_play_url}")
            
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
                'vod_play_url': vod_play_url
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
                soup = BeautifulSoup(res.content, 'lxml')
            else:
                soup = BeautifulSoup(url_or_text, 'lxml')
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
    print(spider.detailContent(['/detail/264550.html']))
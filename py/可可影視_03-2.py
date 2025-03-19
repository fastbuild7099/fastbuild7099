# -*- coding: utf-8 -*-
# @Author  : Adapted for keke7.app
# @Time    : 2025/3/19

import sys
import requests
from bs4 import BeautifulSoup
import urllib.parse

sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def getName(self):
        return "可可影视"

    def init(self, extend):
        self.home_url = 'https://www.keke7.app'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://www.keke7.app/"
        }
        self.image_domain = "https://vres.wbadl.cn"

    def getDependence(self):
        return []

    def homeContent(self, filter):
        result = {
            'class': [
                {'type_id': '1', 'type_name': '电影'},
                {'type_id': '2', 'type_name': '剧集'},
                {'type_id': '4', 'type_name': '综艺'},
                {'type_id': '3', 'type_name': '动漫'},
                {'type_id': '6', 'type_name': '短剧'}
            ]
        }
        print(f"Debug: homeContent result: {result}")
        return result

    def homeVideoContent(self):
        try:
            data = self.get_data(self.home_url)
            return {'list': data}
        except Exception as e:
            print(f"Error in homeVideoContent: {e}")
            return {'list': []}

    def categoryContent(self, cid, page, filter, ext):
        try:
            url = f'{self.home_url}/show/{cid}----{page}.html'
            print(f"Debug: Fetching category URL: {url}")
            data = self.get_data(url)
            return {'list': data}
        except Exception as e:
            print(f"Error in categoryContent: {e}")
            return {'list': []}

    def detailContent(self, did):
        print(f"Debug: Received did: {did}")
        ids = did[0] if did and isinstance(did, list) else str(did) if did else ''
        if not ids:
            print("Debug: No valid ID provided")
            return {'list': []}
        
        url = self.home_url + ids
        print(f"Debug: Fetching detail URL: {url}")
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')

            # 提取影片名稱
            vod_name = soup.select_one('h1').text if soup.select_one('h1') else '未找到標題'
            print(f"Debug: vod_name: {vod_name}")

            # 提取線路標題
            source_items = soup.select('div.source-item span.source-item-label')
            if not source_items:
                print("Debug: No source items found")
                vod_play_from = "未找到播放線路"
            else:
                vod_play_from = '$$$'.join([span.text.strip() for span in source_items])
                print(f"Debug: vod_play_from: {vod_play_from}")

            # 提取播放列表
            play_lists = soup.select('div.episode-list')
            if not play_lists:
                print("Debug: No episode lists found")
                vod_play_url = "未找到播放地址"
            else:
                vod_play_url = []
                for play_list in play_lists:
                    episode_links = play_list.select('a')
                    if not episode_links:
                        print("Debug: No episode links in this playlist")
                        continue
                    episode_list = [f"{a.text.strip()}${self.home_url}{a['href']}" for a in episode_links]
                    vod_play_url.append('#'.join(episode_list))
                vod_play_url = '$$$'.join(vod_play_url) if vod_play_url else "未找到播放地址"
                print(f"Debug: vod_play_url: {vod_play_url}")

            # 構建返回數據
            result = {
                'list': [{
                    'vod_id': ids,
                    'vod_name': vod_name,
                    'vod_play_from': vod_play_from,
                    'vod_play_url': vod_play_url
                }]
            }
            print(f"Debug: detailContent result: {result}")
            return result
        except Exception as e:
            print(f"Error in detailContent: {e}")
            print(f"Debug: Raw response snippet: {res.text[:200] if 'res' in locals() else 'No response'}")
            return {'list': []}

    def searchContent(self, key, quick, page='1'):
        try:
            url = f'{self.home_url}/search?k={urllib.parse.quote(key.encode("utf-8"))}&page={page}'
            print(f"Debug: Fetching search URL: {url}")
            data = self.get_data(url)
            return {'list': data}
        except Exception as e:
            print(f"Error in searchContent: {e}")
            return {'list': []}

    def playerContent(self, flag, pid, vipFlags):
        return {'url': 'https://example.com/test.mp4', 'parse': 0, 'jx': 0}

    def get_data(self, url):
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            items = soup.select('a.v-item')
            data = []
            for item in items:
                vod_id = item['href'] if 'href' in item.attrs else ''
                vod_name = item.select_one('div.v-item-title').text if item.select_one('div.v-item-title') else '未找到標題'
                vod_pic = self.image_domain + item.select_one('div.v-item-cover img')['data-original'] if item.select_one('div.v-item-cover img') else ''
                vod_remarks = item.select_one('div.v-item-bottom span').text if item.select_one('div.v-item-bottom span') else ''
                data.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name.strip(),
                    'vod_pic': vod_pic,
                    'vod_remarks': vod_remarks
                })
            print(f"Debug: get_data result: {data}")
            return data
        except Exception as e:
            print(f"Error in get_data: {e}")
            return []

if __name__ == '__main__':
    spider = Spider()
    spider.init({})
    print(spider.homeContent(False))
    print(spider.homeVideoContent())
    print(spider.categoryContent('1', '1', False, {}))
    print(spider.detailContent(['/detail/264550.html']))
    print(spider.searchContent('test', False, '1'))
# -*- coding: utf-8 -*-
# @Author  : Adapted for keke7.app
# @Time    : 2025/3/19

import sys
import requests
from lxml import etree
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def getName(self):
        return "可可影视"

    def init(self, extend):
        self.home_url = 'https://www.keke7.app'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
            "Referer": "https://www.keke7.app"
        }
        self.image_domain = "https://vres.wbadl.cn"  # 圖片域名

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
                {'type_id': '2', 'type_name': '剧集'},
                {'type_id': '4', 'type_name': '综艺'},
                {'type_id': '3', 'type_name': '动漫'},
                {'type_id': '6', 'type_name': '短剧'}
            ],
            'filters': {
                '1': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''}, {'n': 'Netflix', 'v': 'Netflix'}, {'n': '剧情', 'v': '剧情'},
                        {'n': '喜剧', 'v': '喜剧'}, {'n': '动作', 'v': '动作'}, {'n': '爱情', 'v': '爱情'},
                        {'n': '恐怖', 'v': '恐怖'}, {'n': '惊悚', 'v': '惊悚'}, {'n': '犯罪', 'v': '犯罪'},
                        {'n': '科幻', 'v': '科幻'}, {'n': '悬疑', 'v': '悬疑'}
                    ]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '中国大陆', 'v': '中国大陆'}, {'n': '中国香港', 'v': '中国香港'},
                        {'n': '中国台湾', 'v': '中国台湾'}, {'n': '美国', 'v': '美国'}, {'n': '日本', 'v': '日本'},
                        {'n': '韩国', 'v': '韩国'}, {'n': '英国', 'v': '英国'}, {'n': '法国', 'v': '法国'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'},
                        {'n': '2020', 'v': '2020'}, {'n': '10年代', 'v': '2010_2019'}, {'n': '00年代', 'v': '2000_2009'}
                    ]}
                ],
                '2': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''}, {'n': 'Netflix', 'v': 'Netflix'}, {'n': '剧情', 'v': '剧情'},
                        {'n': '爱情', 'v': '爱情'}, {'n': '喜剧', 'v': '喜剧'}, {'n': '犯罪', 'v': '犯罪'},
                        {'n': '悬疑', 'v': '悬疑'}, {'n': '古装', 'v': '古装'}, {'n': '动作', 'v': '动作'}
                    ]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '中国大陆', 'v': '中国大陆'}, {'n': '中国香港', 'v': '中国香港'},
                        {'n': '韩国', 'v': '韩国'}, {'n': '美国', 'v': '美国'}, {'n': '日本', 'v': '日本'}
                    ]},
                    {'name': '年份', 'key': 'year', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '2025', 'v': '2025'}, {'n': '2024', 'v': '2024'},
                        {'n': '2023', 'v': '2023'}, {'n': '2022', 'v': '2022'}, {'n': '2021', 'v': '2021'}
                    ]}
                ],
            }
        }

    def homeVideoContent(self):
        data = self.get_data(self.home_url)
        return {'list': data, 'parse': 0, 'jx': 0, "倒序": "1"}

    def categoryContent(self, cid, page, filter, ext):
        cate_id = ext.get('cateId', cid) if ext and 'cateId' in ext else cid
        class_filter = ext.get('class', '') if ext and 'class' in ext else ''
        area = ext.get('area', '') if ext and 'area' in ext else ''
        year = ext.get('year', '') if ext and 'year' in ext else ''
        by = ext.get('by', '1') if ext and 'by' in ext else '1'
        url = f'{self.home_url}/show/{cate_id}-{class_filter}-{area}----{year}-{by}-{page}.html'
        print(f"Requesting URL: {url}")
        data = self.get_data(url)
        return {'list': data, 'parse': 0, 'jx': 0, "倒序": "1"}

    def detailContent(self, did):
        ids = did[0] if did else ''
        if not ids:
            return {'list': [], 'msg': 'No ID provided'}
        
        video_list = []
        url = self.home_url + ids
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            
            vod_play_from = '$$$'.join(root.xpath('//div[@class="source-item"]/span[@class="source-item-label"]/text()'))
            play_lists = root.xpath('//div[@class="episode-list"]')
            vod_play_url = []
            for play_list in play_lists:
                episode_names = play_list.xpath('./a/text()')
                episode_urls = play_list.xpath('./a/@href')
                episode_list = [f"{name}${self.home_url}{url}" for name, url in zip(episode_names, episode_urls)]
                vod_play_url.append('#'.join(episode_list))
            final_play_url = '$$$'.join(vod_play_url)
            
            vod_name = root.xpath('//h1/text()')[0] if root.xpath('//h1/text()') else ''
            vod_content = root.xpath('//div[@class="detail-desc"]/text()')[0] if root.xpath('//div[@class="detail-desc"]/text()') else ''
            vod_year = root.xpath('//div[@class="detail-tags-item"]/text()')[0] if root.xpath('//div[@class="detail-tags-item"]/text()') else ''
            vod_area = root.xpath('//div[@class="detail-tags-item"]/text()')[1] if len(root.xpath('//div[@class="detail-tags-item"]/text()')) > 1 else ''
            vod_actor = root.xpath('//div[contains(text(), "演员:")]/following-sibling::div/text()')[0] if root.xpath('//div[contains(text(), "演员:")]/following-sibling::div/text()') else ''
            vod_director = root.xpath('//div[contains(text(), "导演:")]/following-sibling::div/text()')[0] if root.xpath('//div[contains(text(), "导演:")]/following-sibling::div/text()') else ''
            vod_remarks = root.xpath('//div[contains(text(), "备注:")]/following-sibling::div/text()')[0] if root.xpath('//div[contains(text(), "备注:")]/following-sibling::div/text()') else ''
            
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
            print(f"detailContent result: {video_list}")
            return {"list": video_list, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(f"Error in detailContent: {e}")
            return {'list': [], 'msg': str(e)}

    def searchContent(self, key, quick, page='1'):
        url = f'{self.home_url}/search?k={key}&page={page}'
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            data = self.get_data(res.text)
            return {'list': data, 'parse': 0, 'jx': 0, "倒序": "1"}
        except Exception as e:
            print(f"Error in searchContent: {e}")
            return {'list': [], 'parse': 0, 'jx': 0, "倒序": "1"}

    def playerContent(self, flag, pid, vipFlags):
        url = self.home_url + pid
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            play_url = root.xpath('//video/@src')[0] if root.xpath('//video/@src') else 'https://example.com/default.mp4'
            return {'url': play_url, 'parse': 0, 'jx': 0}
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
                # 清理 BOM 和異常編碼
                content = res.content
                if content.startswith(b'\xff\xfe\x00\x00'):  # UCS-4 LE BOM
                    content = content[4:]
                elif content.startswith(b'\xfe\xff'):  # UCS-2 BE BOM
                    content = content[2:]
                elif content.startswith(b'\xff\xfe'):  # UCS-2 LE BOM
                    content = content[2:]
                elif content.startswith(b'\xef\xbb\xbf'):  # UTF-8 BOM
                    content = content[3:]
                text = content.decode('utf-8', errors='ignore')
                root = etree.HTML(text)
            else:
                # 如果是傳入的字符串，假設已為 UTF-8
                text = url_or_text.decode('utf-8', errors='ignore') if isinstance(url_or_text, bytes) else url_or_text
                root = etree.HTML(text)
            
            # 提取影片列表
            items = root.xpath('//a[@class="v-item"]')
            for item in items:
                vod_id = item.xpath('./@href')[0] if item.xpath('./@href') else ''
                # 提取可見的標題
                vod_name = item.xpath('.//div[@class="v-item-title" and not(@style="display: none")]/text()')[0] if item.xpath('.//div[@class="v-item-title" and not(@style="display: none")]/text()') else '未找到標題'
                
                img_tags = item.xpath('.//div[@class="v-item-cover"]/img/@data-original')
                vod_pic = self.image_domain + img_tags[1] if len(img_tags) > 1 else self.image_domain + img_tags[0] if img_tags else ''
                vod_remarks = item.xpath('.//div[@class="v-item-bottom"]/span/text()')[0] if item.xpath('.//div[@class="v-item-bottom"]/span/text()') else ''
                
                data.append({
                    'vod_id': vod_id,
                    'vod_name': vod_name.strip(),
                    'vod_pic': vod_pic,
                    'vod_remarks': vod_remarks
                })
            return data
        except Exception as e:
            print(f"Error in get_data: {e}")
            return data

if __name__ == '__main__':
    spider = Spider()
    spider.init({})
    # 測試首頁內容
    print(spider.homeContent(True))
    # 測試分類內容
    print(spider.categoryContent('1', '1', True, {}))
    # 測試搜索
    print(spider.searchContent('test', False, '1'))

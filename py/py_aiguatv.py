# -*- coding: utf-8 -*-
# @Author  : Doubebly
# @Time    : 2025/3/22 21:03

import sys
import requests
from lxml import etree
import logging
import json

sys.path.append('..')
from base.spider import Spider

# 配置日誌，保持DEBUG級別
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Spider(Spider):
    def getName(self):
        return "爱瓜TV"

    def init(self, extend):
        self.home_url = 'https://aigua1.com'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Referer": "https://aigua1.com/",
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
        }
        self.image_domain = "https://vres.wbadl.cn"
        self.default_play_url = 'https://sf1-cdn-tos.huoshanstatic.com/obj/media-fe/xgplayer_doc_video/mp4/xgplayer-demo-720p.mp4'
        self.session = requests.Session()

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        video_extensions = ['.mp4', '.m3u8', '.flv', '.avi']
        return any(url.lower().endswith(ext) for ext in video_extensions)

    def manualVideoCheck(self):
        return True

    def homeContent(self, filter):
        result = {
            'class': [
                {'type_id': '2', 'type_name': '电视剧'},
                {'type_id': '1', 'type_name': '电影'},
                {'type_id': '3', 'type_name': '综艺'},
                {'type_id': '4', 'type_name': '动漫'},
                {'type_id': '32', 'type_name': '纪录片'}
            ],
            'filters': {
                '1': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '剧情', 'v': '剧情'}, {'n': '喜剧', 'v': '喜剧'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '大陆', 'v': '中国大陆'}, {'n': '美国', 'v': '美国'}]}
                ],
                '2': [
                    {'name': '剧情', 'key': 'class', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '剧情', 'v': '剧情'}, {'n': '爱情', 'v': '爱情'}]},
                    {'name': '地区', 'key': 'area', 'value': [
                        {'n': '全部', 'v': ''}, {'n': '大陆', 'v': '中国大陆'}, {'n': '韩国', 'v': '韩国'}]}
                ]
            }
        }
        logging.info(f"Debug homeContent: {json.dumps(result, ensure_ascii=False)}")
        return result

    def homeVideoContent(self):
        d = []
        try:
            res = self.session.get(self.home_url, headers=self.headers, timeout=10)
            res.raise_for_status()
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            logging.debug(f"首頁HTML片段: {res.text[:2000]}")
            
            # 嘗試匹配視頻項
            data_list = root.xpath('//div[@class="video-box-new"]/div[@class="Movie-list"]')
            if not data_list:
                logging.warning("未找到video-box-new元素，嘗試其他XPath")
                data_list = root.xpath('//div[contains(@class, "video-box")]/div[contains(@class, "list")]')
            if not data_list:
                data_list = root.xpath('//div[contains(@class, "video")]/ul/li')
            if not data_list:
                data_list = root.xpath('//li[contains(@class, "video-item")]')
            if not data_list:
                data_list = root.xpath('//div[contains(@class, "module-items")]/div[contains(@class, "module-item")]')
            
            if not data_list:
                logging.error("無法找到任何視頻列表元素，請檢查網站結構")
                return {'list': d, 'parse': 0, 'jx': 0}
            
            logging.debug(f"找到 {len(data_list)} 個視頻元素")
            for i in data_list:
                hrefs = i.xpath('.//a/@href')
                # 清理名稱中的空白字符
                names = [name.strip() for name in (i.xpath('.//a/text()') or 
                                                  i.xpath('.//span[contains(@class, "title")]/text()') or 
                                                  i.xpath('.//div[contains(@class, "name")]/text()') or 
                                                  i.xpath('.//p[contains(@class, "title")]/text()')) if name.strip()]
                pics = (i.xpath('.//img/@src') or 
                        i.xpath('.//img/@data-src') or 
                        i.xpath('.//img/@originalsrc'))
                # 嘗試更多備註路徑
                remarks = [remark.strip() for remark in (i.xpath('.//div[contains(@class, "type")]/text()') or 
                                                        i.xpath('.//span[contains(@class, "remark")]/text()') or 
                                                        i.xpath('.//div[contains(@class, "status")]/text()') or 
                                                        i.xpath('.//p[contains(@class, "note")]/text()') or 
                                                        i.xpath('.//span[contains(@class, "pic-text")]/text()')) if remark.strip()]
                
                logging.debug(f"解析結果: hrefs={hrefs}, names={names}, pics={pics}, remarks={remarks}")
                
                if hrefs and pics:
                    pic_url = pics[0]
                    if not pic_url.startswith('http'):
                        pic_url = self.image_domain + pic_url
                    elif 'baiduimgcloud' in pic_url:
                        logging.warning(f"檢測到意外域名: {pic_url}，預期為 {self.image_domain}")
                    
                    vod_id = hrefs[0].split('=')[-1] if '=' in hrefs[0] else hrefs[0].split('/')[-1]
                    vod_name = names[0] if names else "未知名稱"
                    vod_remarks = remarks[0] if remarks else ""
                    
                    d.append({
                        'vod_id': vod_id,
                        'vod_name': vod_name,
                        'vod_pic': pic_url,
                        'vod_remarks': vod_remarks
                    })
            
            logging.info(f"成功獲取 {len(d)} 條首頁視頻數據")
            return {'list': d, 'parse': 0, 'jx': 0}
        except requests.RequestException as e:
            logging.error(f"網絡錯誤: {e}")
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            logging.error(f"解析錯誤: {e}")
            return {'list': d, 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        _class = ext.get('class', '')
        _area = ext.get('area', '')
        _language = ext.get('language', '')
        _year = ext.get('year', '')
        _by = ext.get('by', '')
        url = f"{self.home_url}/video/refresh-cate?page_num={page}&sorttype=desc&channel_id={cid}&tag=0&area=0&year=0&page_size=28&sort=new"
        d = []
        try:
            res = self.session.get(url, headers=self.headers, timeout=10)
            res.raise_for_status()
            data = res.json()
            if 'data' not in data or 'list' not in data['data']:
                logging.error("API響應格式變化")
                return {'list': d, 'parse': 0, 'jx': 0}
            for i in data['data']['list']:
                d.append({
                    'vod_id': i['video_id'],
                    'vod_name': i['video_name'],
                    'vod_pic': i['cover'],
                    'vod_remarks': i['flag'],
                })
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            logging.error(f"categoryContent錯誤: {e}")
            return {'list': d, 'parse': 0, 'jx': 0}

    def detailContent(self, did):
        ids = did[0]
        url = f"{self.home_url}/video/detail?video_id={ids}"
        try:
            res = self.session.get(url, headers=self.headers, timeout=10)
            res.raise_for_status()
            root = etree.HTML(res.text)
            vod_play_from = '$$$'.join(['线路一', '线路二', '线路三'])
            play_list1 = root.xpath('//ul[contains(@class, "qy-episode-num")]')
            play_list2 = root.xpath('//ul[@id="srctab-1"]')
            
            if play_list1:
                play_list = play_list1[:-1]
            elif play_list2:
                play_list = play_list2
            else:
                logging.warning("未找到播放列表")
                play_list = []

            vod_play_url_list = []
            for i in play_list:
                name_list1 = i.xpath('.//div[@class="select-link"]/text()')
                name_list2 = i.xpath('.//span[@class="title-link"]/text()')
                name_list3 = i.xpath('./li/text()')
                name_list = name_list1 + name_list2 + name_list3
                url_list = i.xpath('./li/@data-chapter-id')
                if name_list and url_list:
                    vod_play_url_list.append(
                        '#'.join([f"{name.strip()}${ids}-{url}" for name, url in zip(name_list, url_list)])
                    )
            
            vod_play_url = '$$$'.join(vod_play_url_list * 3) if vod_play_url_list else self.default_play_url
            video_list = [{
                'type_name': '',
                'vod_id': ids,
                'vod_name': '',
                'vod_remarks': '',
's               vod_year': '',
                'vod_area': '',
                'vod_actor': '',
                'vod_director': '',
                'vod_content': '',
                'vod_play_from': vod_play_from,
                'vod_play_url': vod_play_url
            }]
            return {"list": video_list, 'parse': 0, 'jx': 0}
        except Exception as e:
            logging.error(f"detailContent錯誤: {e}")
            return {'list': [], 'msg': str(e)}

    def searchContent(self, key, quick, page='1'):
        url = f'{self.home_url}/search?k={key}&page={page}&os=pc'
        d = []
        try:
            res = self.session.get(url, headers=self.headers, timeout=10)
            res.raise_for_status()
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//a[@class="search-result-item"]')
            for i in data_list:
                href = i.xpath('./@href')[0]
                name = i.xpath('.//div[@class="title"]/text()')[0]
                pic = self.image_domain + i.xpath('.//img/@data-original')[0]
                remark = i.xpath('.//div[@class="tags"]/span[1]/text()')[0]
                d.append({
                    'vod_id': href,
                    'vod_name': name,
                    'vod_pic': pic,
                    'vod_remarks': remark
                })
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            logging.error(f"searchContent錯誤: {e}")
            return {'list': [], 'parse': 0, 'jx': 0}

    def playerContent(self, flag, pid, vipFlags):
        a = pid.split('-')
        videoId, chapterId = a[0], a[1]
        url = f"{self.home_url}/video/play-url?videoId={videoId}&sourceId=0&citycode=HKG&chapterId={chapterId}"
        try:
            res = self.session.get(url, headers=self.headers, timeout=10)
            res.raise_for_status()
            data = res.json()['data']['urlinfo']['resource_url']
            play_url = {
                '线路一': data.get('1', self.default_play_url),
                '线路二': data.get('16', self.default_play_url),
                '线路三': data.get('21', self.default_play_url)
            }.get(flag, self.default_play_url)
            return {'url': play_url, 'parse': 0, 'jx': 0, 'header': self.headers}
        except Exception as e:
            logging.error(f"playerContent錯誤: {e}")
            return {'url': self.default_play_url, 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        return None

    def destroy(self):
        self.session.close()
        return 'Spider已銷毀'

if __name__ == '__main__':
    spider = Spider()
    spider.init({})
    result = spider.homeVideoContent()
    print(json.dumps(result, ensure_ascii=False, indent=2))
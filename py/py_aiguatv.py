# -*- coding: utf-8 -*-
# @Author  : Doubebly
# @Time    : 2025/3/22 21:03


import sys
import requests
from lxml import etree, html
import re
sys.path.append('..')
from base.spider import Spider


class Spider(Spider):
    def getName(self):
        return "爱瓜TV"

    def init(self, extend):
        self.home_url = 'https://aigua1.com'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            "Referer": "https://aigua1.com/",
        }
        self.image_domain = "https://vres.wbadl.cn"  # 圖片域名

        self.default_play_url = 'https://sf1-cdn-tos.huoshanstatic.com/obj/media-fe/xgplayer_doc_video/mp4/xgplayer-demo-720p.mp4'

    def getDependence(self):
        return []

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

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
                        {'n': 'Netflix', 'v': 'Netflix'},
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
        d = []
        try:
            res = requests.get(self.home_url, headers=self.headers)
            res.encoding = 'utf-8'  # 根据实际情况设置编码
            root = etree.HTML(res.text.encode('utf-8'))
            data_list = root.xpath('//div[@class="video-box-new"]/div[@class="Movie-list"]')
            for i in data_list:
                d.append(
                    {
                        'vod_id': i.xpath('./a[@class="Movie movie-height"]/@href')[0].split('=')[-1],
                        'vod_name': i.xpath('./a[2]/text()')[0].strip(),
                        'vod_pic': i.xpath('./a[1]/img/@originalsrc')[0],
                        'vod_remarks': i.xpath('./div[@class="Movie-type02"]/div[2]/text()')[0].strip()
                    }
                )
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(e)
            return {'list': d, 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        # 剧情
        _class = ext.get('class', '')
        # 地区
        _area = ext.get('area', '')
        # 语言
        _language = ext.get('language', '')
        # 年份
        _year = ext.get('year', '')
        # 排序
        _by = ext.get('by', '')

        url = self.home_url + f'/video/refresh-cate?page_num={page}&sorttype=desc&channel_id={cid}&tag=0&area=0&year=0&page_size=28&sort=new'
        d = []
        try:
            res = requests.get(url, headers=self.headers)
            data_list = res.json()['data']['list']
            for i in data_list:
                d.append(
                    {
                        'vod_id': i['video_id'],
                        'vod_name': i['video_name'],
                        'vod_pic': i['cover'],
                        'vod_remarks': i['flag'],
                    }
                )
            return {'list': d, 'parse': 0, 'jx': 0}
        except Exception as e:
            print(e)
            return {'list': d, 'parse': 0, 'jx': 0}

    def detailContent(self, did):
        ids = did[0]
        video_list = []
        url = self.home_url + f'/video/detail?video_id={ids}'
        try:
            res = requests.get(url, headers=self.headers)
            root = etree.HTML(res.text.encode('utf-8'))
            # vod_play_from_list = root.xpath('//span[@class="source-item-label"]/text()')
            vod_play_from = '$$$'.join(['线路一', '线路二', '线路三'])
            # 电视剧
            play_list1 = root.xpath('//ul[contains(@class, "qy-episode-num")]')
            # print(play_list1)
            # 电影
            # play_list2 = root.xpath('//ul[contains(@class, "qy-play-list")]')
            play_list2 = root.xpath('//ul[@id="srctab-1"]')
            # print(play_list2)
            vod_play_url_list = []
            if len(play_list1) > 0:
                play_list = play_list1[:-1]
                # print(play_list)

            elif len(play_list2) > 0:
                play_list = play_list2
                # print(play_list)
            else:
                play_list = []

            for i in play_list:
                name_list1 = i.xpath('.//div[@class="select-link"]/text()')
                name_list2 = i.xpath('.//span[@class="title-link"]/text()')
                name_list3 = i.xpath('./li/text()')
                # print(name_list1)
                # print(name_list2)
                # print(name_list3)
                # print(name_list1 + name_list2 + name_list3)
                name_list = name_list1 + name_list2 + name_list3
                url_list = i.xpath('./li/@data-chapter-id')
                vod_play_url_list.append(
                    '#'.join([_name.strip() + '$' + f'{ids}-{_url}' for _name, _url in zip(name_list, url_list)])
                )


            # print(vod_play_url_list*3)
            vod_play_url = '$$$'.join(vod_play_url_list*3)
            # print(vod_play_url_list)
            video_list.append({
                'type_name': '',
                'vod_id': ids,
                'vod_name': '',
                'vod_remarks': '',
                'vod_year': '',
                'vod_area': '',
                'vod_actor': '',
                'vod_director': '',
                'vod_content': '',
                'vod_play_from': vod_play_from,
                'vod_play_url': vod_play_url
            })
            return {"list": video_list, 'parse': 0, 'jx': 0}

        except Exception as e:
            print(f"Error in detailContent: {e}")
            return {'list': [], 'msg': str(e)}

    def searchContent(self, key, quick, page='1'):
        # url = 'https://aigua1.com/video/search-result?keyword=%E6%96%97%E7%BD%97%E5%A4%A7%E9%99%86'
        url = f'{self.home_url}/search?k={key}&page={page}&os=pc'
        d = []
        try:
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            data_list = root.xpath('//a[@class="search-result-item"]')
            for i in data_list:
                d.append(
                    {
                        'vod_id': i.xpath('./@href')[0],
                        'vod_name': i.xpath('.//div[@class="title"]/text()')[0],
                        'vod_pic': 'https://vres.wbadl.cn' + i.xpath('.//img/@data-original')[0],
                        'vod_remarks': i.xpath('.//div[@class="tags"]/span[1]/text()')[0]
                    }
                )
            result = {'list': d, 'parse': 0, 'jx': 0}
            return result
        except Exception as e:
            print(f"Error in searchContent: {e}")
            return {'list': [], 'parse': 0, 'jx': 0}

    def playerContent(self, flag, pid, vipFlags):
        url = 'https://aigua1.com/video/play-url?videoId=230907&sourceId=0&citycode=HKG&chapterId=2916522'
        a = pid.split('-')
        videoId = a[0]
        chapterId = a[1]
        url = self.home_url + f'/video/play-url?videoId={videoId}&sourceId=0&citycode=HKG&chapterId={chapterId}'
        try:
            res = requests.get(url, headers=self.headers)
            play_url_list = res.json()['data']['urlinfo']['resource_url']
            if flag == '线路一':
                play_url = play_url_list['1']
                pass
            elif flag == '线路二':
                play_url = play_url_list['16']
            else:
                play_url = play_url_list['21']
            return {'url': play_url, 'parse': 0, 'jx': 0, 'header': self.headers}
        except Exception as e:
            print(f"Error in playerContent: {e}")
            return {'url': self.default_play_url, 'parse': 0, 'jx': 0}

    def localProxy(self, params):
        pass

    def destroy(self):
        return '正在Destroy'

if __name__ == '__main__':
    pass


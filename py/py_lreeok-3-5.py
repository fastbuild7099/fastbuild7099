import requests
from lxml import etree
import json

class LreeOkCrawler:
    def __init__(self):
        self.home_url = "https://lreeok.vip"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    # 主頁內容：返回分類列表
    def homeContent(self, filter):
        try:
            res = requests.get(self.home_url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            
            class_list = []
            nav_items = root.xpath('//div[@class="head-nav"]//a')
            for item in nav_items:
                name = item.xpath('./text()')[0].strip() if item.xpath('./text()') else ""
                type_id = item.xpath('./@href')[0].strip().replace('/vodshow/', '').replace('-----------.html', '') if item.xpath('./@href') else ""
                if name and type_id and "首页" not in name and "更多" not in name:
                    class_list.append({
                        "type_name": name,
                        "type_id": type_id
                    })

            result = {
                "class": class_list,
                "filters": {}
            }
            return json.dumps(result)
        except Exception as e:
            print(f"homeContent error: {e}")
            return json.dumps({"class": []})

    # 分類頁面內容：返回影片列表
    def categoryContent(self, tid, pg, filter, extend):
        try:
            url = f"{self.home_url}/vodshow/{tid}--------{pg}---.html"
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            
            video_list = []
            items = root.xpath('//div[@class="public-list-box"]')
            for item in items:
                vod_id = item.xpath('.//a/@href')[0].strip().replace('/voddetail/', '').replace('.html', '') if item.xpath('.//a/@href') else ""
                vod_name = item.xpath('.//a/@title')[0].strip() if item.xpath('.//a/@title') else ""
                vod_pic = item.xpath('.//img/@data-src')[0].strip() if item.xpath('.//img/@data-src') else ""
                vod_remarks = item.xpath('.//span[@class="public-list-prb"]/text()')[0].strip() if item.xpath('.//span[@class="public-list-prb"]/text()') else ""
                
                video_list.append({
                    "vod_id": vod_id,
                    "vod_name": vod_name,
                    "vod_pic": vod_pic,
                    "vod_remarks": vod_remarks
                })

            total_pages = root.xpath('//div[@class="vod-list-page"]//a[last()-1]/text()')[0].strip() if root.xpath('//div[@class="vod-list-page"]//a[last()-1]/text()') else "1"
            result = {
                "page": int(pg),
                "pagecount": int(total_pages),
                "limit": len(video_list),
                "total": int(total_pages) * len(video_list),
                "list": video_list
            }
            return json.dumps(result)
        except Exception as e:
            print(f"categoryContent error: {e}")
            return json.dumps({"list": []})

    # 詳情頁面內容：返回影片詳細信息
    def detailContent(self, did):
        ids = did[0]
        video_list = []
        
        try:
            res = requests.get(f'{self.home_url}/voddetail/{ids}.html', headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            print(f"HTML content preview: {res.text[:500]}")

            # 提取標題並清理
            vod_name = root.xpath('//h3[@class="slide-info-title hide"]/text()')[0].strip() if root.xpath('//h3[@class="slide-info-title hide"]/text()') else ""
            if not vod_name:
                title = root.xpath('//title/text()')[0].strip()
                vod_name = title.split('》')[0] + '》' if '《' in title and '》' in title else title
            print(f"Extracted vod_name: {vod_name}")

            # 提取影片信息
            info_params = root.xpath('//div[@class="info-parameter"]//ul/li')
            vod_year = ""
            vod_area = ""
            vod_remarks = ""
            vod_director = ""
            vod_actor = ""
            vod_class = ""
            vod_lang = ""
            vod_content = "暂无简介"

            for li in info_params:
                label = li.xpath('.//em[@class="cor4"]/text()')[0].strip() if li.xpath('.//em[@class="cor4"]/text()') else ""
                if "年份：" in label:
                    vod_year = li.xpath('.//text()')[1].strip() if len(li.xpath('.//text()')) > 1 else ""
                elif "地区：" in label:
                    vod_area = li.xpath('.//text()')[1].strip() if len(li.xpath('.//text()')) > 1 else ""
                elif "状态：" in label:
                    vod_remarks = li.xpath('.//span/text()')[0].strip() if li.xpath('.//span/text()') else ""
                elif "导演：" in label:
                    vod_director = " / ".join(li.xpath('.//a/text()')) if li.xpath('.//a/text()') else ""
                elif "主演：" in label:
                    vod_actor = " / ".join(li.xpath('.//a/text()')) if li.xpath('.//a/text()') else ""
                elif "类型：" in label:
                    vod_class = " ".join(li.xpath('.//a/text()')) if li.xpath('.//a/text()') else ""
                elif "语言：" in label:
                    vod_lang = li.xpath('.//text()')[1].strip() if len(li.xpath('.//text()')) > 1 else ""
                elif "简介：" in label:
                    vod_content = li.xpath('.//text()')[1].strip() if len(li.xpath('.//text()')) > 1 else "暂无简介"

            # 備用提取
            if not vod_year:
                vod_year = root.xpath('//div[@class="slide-info hide"]/span[@class="slide-info-remarks"]/a[contains(@href, "202")]/text()')[0].strip() if root.xpath('//div[@class="slide-info hide"]/span[@class="slide-info-remarks"]/a[contains(@href, "202")]') else ""
            if not vod_area:
                vod_area = root.xpath('//div[@class="slide-info hide"]/span[@class="slide-info-remarks"]/a[contains(@href, "%E9%9F%A9%E5%9B%BD") or contains(@href, "%E5%A4%A7%E9%99%86")]/text()')[0].strip() if root.xpath('//div[@class="slide-info hide"]/span[@class="slide-info-remarks"]/a[contains(@href, "%E9%9F%A9%E5%9B%BD") or contains(@href, "%E5%A4%A7%E9%99%86")]') else ""
            if not vod_remarks:
                vod_remarks = root.xpath('//div[@class="slide-info hide"]/text()[contains(., "HD") or contains(., "正片")])[0].strip().replace("备注 :", "").strip() if root.xpath('//div[@class="slide-info hide"]/text()[contains(., "HD") or contains(., "正片")]') else ""
            if not vod_class:
                vod_class = " ".join(root.xpath('//div[@class="slide-info hide"]/span[@class="slide-info-remarks"]/a[not(contains(@href, "202")) and not(contains(@href, "%E9%9F%A9%E5%9B%BD"))]/text()')) if root.xpath('//div[@class="slide-info hide"]/span[@class="slide-info-remarks"]/a[not(contains(@href, "202")) and not(contains(@href, "%E9%9F%A9%E5%9B%BD"))]') else ""

            # 提取播放來源和 URL
            play_from = []
            play_url = []
            anthology_boxes = root.xpath('//div[@class="anthology-list-box"]')
            for box in anthology_boxes:
                source_name = root.xpath('//div[@class="anthology-tab"]//a/text()')[anthology_boxes.index(box)].strip().replace("\xa0", "")
                play_from.append(source_name)
                urls = box.xpath('.//a/@href')
                titles = box.xpath('.//a/text()')
                play_url.append("#".join([f"{title}${url}" for title, url in zip(titles, urls)]))

            vod_play_from = "$$$".join(play_from)
            vod_play_url = "$$$".join(play_url)

            # 打印提取結果
            print(f"Extracted vod_year: {vod_year}, vod_area: {vod_area}, vod_remarks: {vod_remarks}, vod_lang: {vod_lang}")
            print(f"Extracted vod_director: {vod_director}")
            print(f"Extracted vod_actor: {vod_actor}")
            print(f"Extracted vod_content: {vod_content}")
            print(f"Extracted vod_play_from: {vod_play_from}")
            print(f"Extracted vod_play_url: {vod_play_url}")

            # 組裝結果
            video_list.append({
                'type_name': vod_class,
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
                'vod_play_url': vod_play_url
            })

            result = {'list': video_list, 'parse': 0, 'jx': 0}
            print(f"Detail test result: {result}")
            return json.dumps(result)
        except Exception as e:
            print(f"detailContent error: {e}")
            return json.dumps({'list': [], 'parse': 0, 'jx': 0})

    # 搜索內容：根據關鍵字返回影片列表
    def searchContent(self, key, quick):
        try:
            url = f"{self.home_url}/vodsearch/-------------.html?wd={key}"
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            
            video_list = []
            items = root.xpath('//div[@class="public-list-box"]')
            for item in items:
                vod_id = item.xpath('.//a/@href')[0].strip().replace('/voddetail/', '').replace('.html', '') if item.xpath('.//a/@href') else ""
                vod_name = item.xpath('.//a/@title')[0].strip() if item.xpath('.//a/@title') else ""
                vod_pic = item.xpath('.//img/@data-src')[0].strip() if item.xpath('.//img/@data-src') else ""
                vod_remarks = item.xpath('.//span[@class="public-list-prb"]/text()')[0].strip() if item.xpath('.//span[@class="public-list-prb"]/text()') else ""
                
                video_list.append({
                    "vod_id": vod_id,
                    "vod_name": vod_name,
                    "vod_pic": vod_pic,
                    "vod_remarks": vod_remarks
                })

            result = {"list": video_list}
            return json.dumps(result)
        except Exception as e:
            print(f"searchContent error: {e}")
            return json.dumps({"list": []})

    # 播放內容：返回播放 URL
    def playerContent(self, flag, id, vipFlags):
        try:
            url = f"{self.home_url}{id}"
            res = requests.get(url, headers=self.headers)
            res.encoding = 'utf-8'
            root = etree.HTML(res.text)
            
            # 這裡假設播放頁面有直接的播放 URL，實際可能需要解析 JS 或 iframe
            play_url = root.xpath('//iframe/@src')[0].strip() if root.xpath('//iframe/@src') else url
            result = {
                "parse": 1,  # 需要解析（假設需要嗅探）
                "playUrl": "",
                "url": play_url,
                "header": json.dumps(self.headers)
            }
            return json.dumps(result)
        except Exception as e:
            print(f"playerContent error: {e}")
            return json.dumps({"parse": 0, "url": ""})

# 測試程式碼
if __name__ == "__main__":
    crawler = LreeOkCrawler()

    # 測試主頁
    print("Testing homeContent:")
    print(crawler.homeContent(""))

    # 測試分類頁面
    print("\nTesting categoryContent:")
    print(crawler.categoryContent("1", "1", "", ""))

    # 測試詳情頁面
    print("\nTesting detailContent:")
    print(crawler.detailContent(["71690"]))

    # 測試搜索
    print("\nTesting searchContent:")
    print(crawler.searchContent("宗教与黑道", ""))

    # 測試播放
    print("\nTesting playerContent:")
    print(crawler.playerContent("悠悠资源", "/vodplay/71690-3-1.html", ""))
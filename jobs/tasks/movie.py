import datetime
import hashlib
import json
import os
import requests
import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from application import app


class JobTask():

    def __int__(self):
        self.source = "bttian"
        self.url = {
            "num": 3,
            "url": "https://www.bttian.com/show/dongzuopian--------#d#---.html",
            "save_path": "/tmp/%/" % (self.source),
        }
        self.date = datetime.date.today()

    def run(self, parmas):
        self.source = "bttian"
        self.url = {
            "num": 1,
            "url": "https://www.bttian.com/show/dongzuopian--------#d#---.html",
            "save_path": "tmp/" + self.source + "/",
        }

        self.source = "bttian"
        # self.date = str(datetime.date.today())

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

        self.getList()
        self.parseInfo()

    # 获取页面，保存到本地
    def getList(self):
        config = self.url

        print("config:", config)

        # 保存路径
        path_root = config["save_path"] + str(datetime.date.today())
        path_list = path_root + "/list"
        path_info = path_root + "/info"
        path_json = path_root + "/json"
        path_vid = path_root + "/vid"

        print(path_list, path_info, path_json, path_vid)
        self.makeSuredirs(path_root)
        self.makeSuredirs(path_list)
        self.makeSuredirs(path_info)
        self.makeSuredirs(path_json)
        self.makeSuredirs(path_vid)

        # 将请求内容的html保存到文件中
        pages = range(1, config['num'] + 1)
        for index in pages:
            tmp_path = path_list + "/" + str(index)
            tmp_url = config['url'].replace("#d#", str(index))
            app.logger.info("get list : " + tmp_url)
            if os.path.exists(tmp_path):
                print("%已经存在", tmp_url)
                continue

            tmp_content = self.getHttpContent(tmp_url)
            # print("-------------------------")
            # print(tmp_content)
            # print("-------------------------")

            self.saveContent(tmp_path, tmp_content)

            app.logger.info("正在执行: " + tmp_url)
            # 休眠
            time.sleep(0.3)

        for idx in os.listdir(path_list):
            tmp_content = self.getContent(path_list + "/" + str(idx))
            items_data = self.parseList(tmp_content)
            if not items_data:
                continue

            # 获取每一个电影的详细信息
            for item in items_data:
                tmp_json_path = path_json + "/" + item['hash']
                tmp_info_path = path_info + "/" + item['hash']
                tmp_vid_path = path_vid + "/" + item['hash']

                if not os.path.exists(tmp_json_path):
                    self.saveContent(tmp_json_path, json.dumps(item, ensure_ascii=False))

                if not os.path.exists(tmp_info_path):
                    tmp_content = self.getHttpContent(item['url'])
                    self.saveContent(tmp_info_path, tmp_content)

                # if not os.path.exists(tmp_vid_path):
                #     tmp_content = self.getHttpContent(item['vid_url'])
                #     self.saveContent(tmp_vid_path, tmp_content)

                time.sleep(0.3)

    # 解析返回content的html的详细数据
    def parseList(self, content):
        data = []
        config = self.url
        url_info = urlparse(config['url'])

        # url_domain = url_info[0] + "://" + url_info[1]

        # 解析content数据
        tmp_soup = BeautifulSoup(str(content), "html.parser")

        tmp_list = tmp_soup.select('div.mo-cols-lays.mo-back-white.mo-part-round ul li')
        print("电影总数：", len(tmp_list))
        for tmp_item in tmp_list:

            # 找到电影名称，使用CSS选择器
            tage = tmp_item.select("a.mo-situ-name.mo-fsxs-14px.mo-coxs-center.mo-comd-left.mo-wrap-arow")
            act_list = tmp_item.select(
                "span.mo-situ-desc.mo-fsxs-12px.mo-wrap-arow.mo-text-muted.mo-coxs-none.mo-comd-block")
            if len(tage) == 0 or len(act_list) == 0:
                print("解析失败")
                continue

            name = tage[0].text
            print("电影名称:", name)

            href = tage[0]['href']
            if "http:" not in href:
                href = "https://www.bttian.com" + href
                print("链接:", href)

            # 演员
            act = act_list[0].text
            print(act)

            tmp_data = {
                "name": name,
                "url": href,
                "act": act,
                # "vid_url": tmp_vid_url,
                "hash": hashlib.md5(href.encode("utf-8")).hexdigest()
            }
            data.append(tmp_data)

        return data

    # 解析详细信息
    def parseInfo(self):
        config = self.url
        path_root = config["save_path"] + str(datetime.date.today())
        path_info = path_root + "/info"
        path_json = path_root + "/json"
        path_vid = path_root + "/vid"

        # 读取数据
        for filename in os.listdir(path_info):
            tmp_json_path = path_json + "/" + filename
            tmp_info_path = path_info + "/" + filename
            # tmp_vid_path = path_vid + "/" + filename
            tmp_data = json.loads(self.getContent(tmp_json_path))
            tmp_content = self.getContent(tmp_info_path)

            print("--------------------")
            print("数据：", tmp_data)
            print("--------------------")

            soup_movie = BeautifulSoup(tmp_content, "html.parser")
            try:
                file_url1 = soup_movie.select("img.mo-part-pics")
                url1 = file_url1[0]["src"]
                print("封面:", url1)
                tmp_data["封面"] = url1

                file_url2 = soup_movie.select("a.mo-deta-play.mo-mrxs-10px.mo-part-btns.mo-lhxs-34px.mo-bord-round.mo-back-mojia.mo-cols-info")
                if len(file_url2) >= 2:
                    if file_url2[0]["href"]:
                        url2_1 = "https://www.bttian.com" + file_url2[0]["href"]
                        print("播放地址:", url2_1)
                        tmp_data["播放地址"] = url2_1

                    if file_url2[1]["href"]:
                        url2_2 = "https://www.bttian.com" + file_url2[1]["href"]
                        print("下载地址:", url2_2)
                        tmp_data["下载地址"] = url2_2

                catg_country = soup_movie.select("li.mo-cols-info.mo-cols-xs6.mo-cols-md3.mo-fsxs-14px.mo-wrap-arow.mo-ptxs-5px a")
                print("类别：", catg_country[0].text)
                print("国家：", catg_country[1].text)

                tmp_data["类别"] = catg_country[0].text
                tmp_data["国家"] = catg_country[1].text

                yaer = soup_movie.select("li.mo-cols-info.mo-cols-xs6.mo-cols-md3.mo-fsxs-14px.mo-wrap-arow.mo-ptxs-5px.mo-coxs-none.mo-coss-block a")
                print("年份：", yaer[0].text)

                tmp_data["年份"] = yaer[0].text

                dirc = soup_movie.select("li.mo-cols-info.mo-cols-xs12.mo-ptxs-5px.mo-fsxs-14px.mo-lhxs-20px.mo-lhxl-24px.mo-coxs-none.mo-comd-block.mo-text-muted")
                print(dirc[0].text)

                tmp_data["短语"] = dirc[0].text.replace("短评：", "")

                print("----------------------------------------------------")
                print("数据：", tmp_data)

                print("----------------------------------------------------")

            except:
                continue
        return True


    # 获取请求内容
    def getHttpContent(self, url):
        try:
            r = requests.get(url, headers=self.headers)
            if r.status_code != 200:
                return None

            return r.content

        except Exception:
            return None

    # 保存响应内容
    def saveContent(self, path, content):
        if content:
            with open(path, mode="w+", encoding="utf-8") as f:
                if type(content) != str:
                    content = content.decode("utf-8")

                f.write(content)
                f.flush()
                f.close()

    # 获取path的的html
    def getContent(self, path):
        if os.path.exists(path):
            with open(path, "r") as f:
                return f.read()

        return ''

    # 创建目录
    def makeSuredirs(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    #
    # def run(self, parmas):
    #     print("hello, job")
    #
    #     # url_list = ["https://www.bttian.com/show/dongzuopian--------1---.html"]
    #
    #
    #     for i in range(1,10):
    #         print("===================================================")
    #         print(i)
    #         print("===================================================")
    #
    #         url = "https://www.bttian.com/show/dongzuopian--------"+str(i)+"---.html"
    #
    #         headers = {
    #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    #         }
    #         resp = requests.get(url, headers=headers)
    #
    #         soup = BeautifulSoup(resp.content, "html.parser")
    #         # items = soup.select("div.mo-cols-lays ul li")
    #
    #         movie_divs = soup.select('div.mo-cols-lays.mo-back-white.mo-part-round ul li')
    #         # print(len(movie_divs))
    #
    #         # 遍历每个包含电影信息的div元素
    #         for movie_div in movie_divs:
    #             # 找到电影名称，使用CSS选择器
    #             tage = movie_div.select("a.mo-situ-name.mo-fsxs-14px.mo-coxs-center.mo-comd-left.mo-wrap-arow")
    #             act_list = movie_div.select(
    #                 "span.mo-situ-desc.mo-fsxs-12px.mo-wrap-arow.mo-text-muted.mo-coxs-none.mo-comd-block")
    #             # print(tage)
    #             # print(len(tage))
    #             # print(act_list)
    #             # print("")
    #             if len(tage) == 0 or len(act_list) == 0:
    #                 continue
    #
    #             name = tage[0].text
    #             print("电影名称:", name)
    #
    #             href = tage[0]['href']
    #             print("链接:", "https://www.bttian.com" + href)
    #
    #             # 演员
    #             act = act_list[0].text
    #             print(act)
    #
    #
    #             # 获取详细信息
    #             href_info = "https://www.bttian.com" + href
    #             resp_movie = requests.get(href_info, headers=headers)
    #             # print(resp_movie.content)
    #             soup_movie = BeautifulSoup(resp_movie.content, "html.parser")
    #
    #             file_url1 = soup_movie.select("img.mo-part-pics")
    #             url1 = file_url1[0]["src"]
    #             print("封面:", url1)
    #
    #             file_url2 = soup_movie.select(
    #                 "a.mo-deta-play.mo-mrxs-10px.mo-part-btns.mo-lhxs-34px.mo-bord-round.mo-back-mojia.mo-cols-info")
    #             if len(file_url2) >= 2:
    #                 if file_url2[0]["href"]:
    #                     url2_1 = "https://www.bttian.com" + file_url2[0]["href"]
    #                     print("播放地址:", url2_1)
    #
    #                 if file_url2[1]["href"]:
    #                     url2_2 = "https://www.bttian.com" + file_url2[1]["href"]
    #                     print("下载地址:", url2_2)
    #
    #             catg_country = soup_movie.select(
    #                 "li.mo-cols-info.mo-cols-xs6.mo-cols-md3.mo-fsxs-14px.mo-wrap-arow.mo-ptxs-5px a")
    #             print("类别：", catg_country[0].text)
    #             print("国家：", catg_country[1].text)
    #
    #             yaer = soup_movie.select(
    #                 "li.mo-cols-info.mo-cols-xs6.mo-cols-md3.mo-fsxs-14px.mo-wrap-arow.mo-ptxs-5px.mo-coxs-none.mo-coss-block a")
    #             print("年份：", yaer[0].text)
    #
    #             dirc = soup_movie.select(
    #                 "li.mo-cols-info.mo-cols-xs12.mo-ptxs-5px.mo-fsxs-14px.mo-lhxs-20px.mo-lhxl-24px.mo-coxs-none.mo-comd-block.mo-text-muted")
    #             print(dirc[0].text)
    #
    #             print("--------------------------")
    #

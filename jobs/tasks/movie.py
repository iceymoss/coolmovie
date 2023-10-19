import requests
from bs4 import BeautifulSoup
class JobTask():
    def run(self, parmas):
        print("hello, job")
        url = "https://www.bttian.com/bt/dianying.html"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        resp = requests.get(url, headers=headers)

        soup = BeautifulSoup(resp.content, "html.parser")
        # items = soup.select("div.mo-cols-lays ul li")

        movie_divs = soup.select('div.mo-cols-lays.mo-back-white.mo-part-round ul li')
        # print(len(movie_divs))

        # 遍历每个包含电影信息的div元素
        for movie_div in movie_divs:
            # 找到电影名称，使用CSS选择器
            tage = movie_div.select("a.mo-situ-name.mo-fsxs-14px.mo-coxs-center.mo-comd-left.mo-wrap-arow")
            act_list = movie_div.select("span.mo-situ-desc.mo-fsxs-12px.mo-wrap-arow.mo-text-muted.mo-coxs-none.mo-comd-block")
            # print(tage)
            # print(len(tage))
            # print(act_list)
            # print("")
            if len(tage) == 0 or len(act_list) == 0:
                continue

            name = tage[0].text
            print("电影名称:", name)

            href = tage[0]['href']
            print("链接:", "https://www.bttian.com"+href)

            act = act_list[0].text
            print(act)


            # 获取详细信息
            href_info = "https://www.bttian.com"+href
            resp_movie = requests.get(href_info, headers=headers)
            # print(resp_movie.content)
            soup_movie = BeautifulSoup(resp_movie.content, "html.parser")

            file_url1 = soup_movie.select("img.mo-part-pics")
            url1 = file_url1[0]["src"]
            print("封面:",url1)

            file_url2 = soup_movie.select("a.mo-deta-play.mo-mrxs-10px.mo-part-btns.mo-lhxs-34px.mo-bord-round.mo-back-mojia.mo-cols-info")
            if len(file_url2) >=2 :
                if file_url2[0]["href"]:
                    url2_1 = "https://www.bttian.com" + file_url2[0]["href"]
                    print("播放地址:", url2_1)

                if  file_url2[1]["href"] :
                    url2_2 = "https://www.bttian.com" + file_url2[1]["href"]
                    print("下载地址:", url2_2)


            catg_country = soup_movie.select("li.mo-cols-info.mo-cols-xs6.mo-cols-md3.mo-fsxs-14px.mo-wrap-arow.mo-ptxs-5px a")
            print("类别：", catg_country[0].text)
            print("国家：", catg_country[1].text)

            yaer = soup_movie.select("li.mo-cols-info.mo-cols-xs6.mo-cols-md3.mo-fsxs-14px.mo-wrap-arow.mo-ptxs-5px.mo-coxs-none.mo-coss-block a")
            print("年份：", yaer[0].text)

            dirc = soup_movie.select("li.mo-cols-info.mo-cols-xs12.mo-ptxs-5px.mo-fsxs-14px.mo-lhxs-20px.mo-lhxl-24px.mo-coxs-none.mo-comd-block.mo-text-muted")
            print(dirc[0].text)

            print("--------------------------")






















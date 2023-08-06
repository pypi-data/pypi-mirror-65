'''
For MyAnimeList, searching animes/manga/OVA using name instead of IDs

'''

from bs4 import BeautifulSoup as parse
import requests


class MALdata:


    def madeinfo(self, link):

        infos = []
        desc = []
        r= requests.get(link)
        s = parse(r.content, 'lxml')
        data1 = s.find("div", {"class": "fl-l score"}).attrs
        data1_rate = s.find("div", {"class": "fl-l score"}).get_text()
        data1_rate = data1_rate.replace(' ', '')
        data1_rate = data1_rate.replace('\n', '')
        data2_rank = s.find("span", {"class": "numbers ranked"}).get_text()
        data3_info = s.find("span",{"itemprop": "description"}).get_text()
        desc.append(data3_info)
        data4_episodes = s.find_all("div", {"class": "spaceit"})[0].get_text()
        data4_episodes = data4_episodes.replace('\n', '')
        data4_status = s.find_all("div", {"class": "spaceit"})[1].get_text()
        data4_status = data4_status.replace('\n', '')
        data4_air = s.find_all("div", {"class": "spaceit"})[2].get_text()
        data4_air = data4_air.replace('\n', '')
        data5_image = s.find("img", {"class": "lazyloaded"}, src = True)
        infos.append(data4_episodes+"\n"+data4_status+"\n"+data4_air)

        return {"users":data1["data-user"],"rating" : data1_rate, "rank": data2_rank, "inf": desc, "add": infos, "image": data5_image["src"]}
        

    def animeSearch(self, query:str = None):

        '''Getting the Result List'''

        try:
            if query == None:
                print("Missing Anime Name!")
                return

            anime_names = []
            text = query.lower()
            text = text.replace(' ', '+')
            link_anime = "https://myanimelist.net/anime.php?q="+text+"&type=0&score=0&status=0&p=0&r=0&sm=0&sd=0&sy=0&em=0&ed=0&ey=0&c[]=a&c[]=b&c[]=c&c[]=f&gx=0"
            r = requests.get(link_anime)
            s = parse(r.content, 'lxml')
            data_names = s.find_all("a", {"class": "hoverinfo_trigger fw-b fl-l"})
            refined = "None"
            for x in data_names:
                names = x.text
                anime_names.append(names)
            refined = '\n'.join(anime_names[:7])
            return refined

        except Exception as e:
            print(e)


    def animeData(self, query:str = None):

        '''Getting the links to the selected result'''

        try:
            if query == None:
                print("Missing Name!")
                return

            anime_links = []
            anime_names = []
            query = query.lower()
            text = query.replace(' ', '+')
            link_anime = "https://myanimelist.net/anime.php?q="+text+"&type=0&score=0&status=0&p=0&r=0&sm=0&sd=0&sy=0&em=0&ed=0&ey=0&c[]=a&c[]=b&c[]=c&c[]=f&gx=0"
            r = requests.get(link_anime)
            s = parse(r.content, 'lxml')
            data_links = s.find_all("a", {"class": "hoverinfo_trigger fw-b fl-l"})
            for x in data_links:
                names = x.text.lower()
                links = x["href"]
                anime_links.append(links)
                anime_names.append(names)
            anime_names = anime_names[:7]
            anime_links = anime_links[:7]
            link_found = "None"

            if query in anime_names:
                n = anime_names.index("{}".format(query))
                link_found = anime_links[n]
            
            datas = self.madeinfo(link_found)
            return datas

        except Exception as e:
            print(e)

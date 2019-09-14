import time

from tools import get_json


class BilibiliAPI:
    async def get_video_num(self, mid: int) -> int:
        nav_info = await self.get_num_json(mid)
        video_num = nav_info['video']
        return video_num

    @staticmethod
    async def get_video(mid: int) -> dict:
        video_info = await get_json(
            f'https://space.bilibili.com/ajax/member/getSubmitVideos?mid={mid}&pagesize=1&tid=0&page=1&keyword=&order=pubdate')
        video = video_info['data']['vlist'][0]
        title = video['title']
        ref = f"https://www.bilibili.com/video/av{video['aid']}"
        date = time.strftime("%Y-%m-%d", time.localtime())
        return {'Title': title,
                'Target': ref,
                'Date': date}

    @staticmethod
    async def get_num_json(mid: int) -> dict:
        nav_info = await get_json(f'https://api.bilibili.com/x/space/navnum?mid={mid}&jsonp=jsonp')
        return nav_info['data']

    async def get_article_num(self, mid: int) -> int:
        nav_info = await self.get_num_json(mid)
        article_num = nav_info['article']
        return article_num

    @staticmethod
    async def get_article(mid: int) -> dict:
        article_info = await get_json(f'https://api.bilibili.com/x/space/article?mid={mid}&jsonp=jsonp')
        article = article_info['data']['articles'][0]
        title = article['title']
        target = f'https://www.bilibili.com/read/cv{article["id"]}'
        return {'Title': title,
                'Target': target}

    @staticmethod
    async def get_live_status(mid: int) -> dict:
        live_json = await get_json(f'https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid={mid}')
        is_live = live_json['data']['liveStatus']
        title = live_json['data']['title']
        url = live_json['data']['url']
        return {'Title': title,
                'Is_live': is_live,
                'Target': url}

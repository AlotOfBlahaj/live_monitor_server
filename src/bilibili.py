import asyncio
import logging

from bilibili_api.bilibili_api import BilibiliAPI
from config import config
from daemon import VideoDaemon


class Bilibili(VideoDaemon):
    def __init__(self, user_config):
        super().__init__(user_config)
        self.API = BilibiliAPI()
        self.logger = logging.getLogger('run.bilibili')
        self.old_video_num = None
        self.old_article_num = None

    async def check(self):
        try:
            self.old_video_num = await self.API.get_video_num(self.target_id)
            self.old_article_num = await self.API.get_article_num(self.target_id)
            while True:
                video_num = await self.API.get_video_num(self.target_id)
                article_num = await self.API.get_article_num(self.target_id)
                if video_num > self.old_video_num:
                    self.logger.info('Found A new video')
                    await asyncio.sleep(10)  # 需要增加延迟，反正B站API未即时更新，防止返回上一个视频
                    video_info = await self.API.get_video(self.target_id)
                    video_info['User'] = 'bilibili'
                    video_info['Provide'] = 'Bilibili'
                    self.send_to_sub(video_info)
                    self.old_video_num = video_num
                elif article_num > self.old_article_num:
                    self.logger.warning('Found A new article')
                    await asyncio.sleep(10)
                    article_info = await self.API.get_article(self.target_id)
                    article_info['User'] = 'bilibili'
                    video_info['Provide'] = 'Bilibili'
                    self.send_to_sub(article_info)
                else:
                    self.logger.info(f'{self.target_id}:{video_num} Not found new videos')
                await asyncio.sleep(config['sec'])
        except Exception:
            self.logger.Exception('Check failed')
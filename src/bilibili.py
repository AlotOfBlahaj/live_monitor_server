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

    async def check(self):
        self.old_video_num = await self.API.get_video_num(self.target_id)
        while True:
            video_num = await self.API.get_video_num(self.target_id)
            if video_num > self.old_video_num:
                self.logger.info('Found A new video')
                await asyncio.sleep(10)  # 需要增加延迟，反正B站API未即时更新，防止返回上一个视频
                video_info = await self.API.get_video(self.target_id)
                self.set_live(video_info)
                self.old_video_num = video_num
            else:
                self.logger.info(f'{self.target_id}:{video_num} Not found new videos')
            await asyncio.sleep(config['sec'])

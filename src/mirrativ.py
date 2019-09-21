import asyncio
import logging
import time

from config import config
from daemon import VideoDaemon
from tools import get_json


class Mirrativ(VideoDaemon):

    def __init__(self, target_id):
        super().__init__(target_id)
        self.logger = logging.getLogger('run.mirrativ')
        self.module = 'Mirrativ'

    async def get_live_info(self):
        live_info = await get_json(f'https://www.mirrativ.com/api/user/profile?user_id={self.target_id}')
        nowlive = live_info['onlive']
        try:
            if nowlive:
                live_id = nowlive['live_id']
                return live_id
            return None
        except KeyError:
            self.logger.exception('Get live info error')

    @staticmethod
    async def get_hsl(is_live):
        hsl_info = await get_json(f'https://www.mirrativ.com/api/live/live?live_id={is_live}')
        title = hsl_info['shares']['twitter']['card']['title']
        steaming_url = hsl_info['streaming_url_hls']
        target = hsl_info['share_url']
        date = time.strftime("%Y-%m-%d", time.localtime())
        live_dict = {'Title': title,
                     'Ref': steaming_url,
                     'Target': target,
                     'Date': date}
        return live_dict

    async def check(self):
        while True:
            is_live = await self.get_live_info()
            if is_live:
                video_dict = await self.get_hsl(is_live)
                video_dict['Provide'] = self.module
                video_dict['User'] = self.user_config['name']
                self.send_to_sub(video_dict)
            else:
                self.logger.info(f'{self.target_id}: Not found Live')
            await asyncio.sleep(config['sec'])
